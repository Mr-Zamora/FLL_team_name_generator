from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai
import json
import os
import uuid
import time
import random
import threading
import re
import shutil
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datetime import datetime
from config import GEMINI_API_KEY
from prompts import get_team_name_prompt, get_generation_parameters, get_random_local_team_name

# Global variables to track generated names and avoid repetition
RECENT_GENERATED_NAMES = set()
MAX_RECENT_NAMES = 100  # How many recent names to remember

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
print(f"Configuring Gemini API with key: {GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:] if len(GEMINI_API_KEY) > 8 else ''}")

# Test if the API key is valid before proceeding
try:
    # Configure the Gemini API with the API key
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Test if the API is working
    print("Testing Gemini API connection...")
    model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-05-20")
    test_response = model.generate_content("Hello, are you working?")
    print(f"API test successful: {test_response.text[:20]}...")
    
    # Set safety settings to allow creative content while maintaining appropriateness
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    ]
    
    # Create the model we'll use with safety settings
    print("Creating Gemini model instance...")
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",  # Using the faster model for better performance
        safety_settings=safety_settings
    )
    
    # Test the model
    test_generation = model.generate_content("Generate a short team name for a robotics team.")
    print(f"Model test successful: {test_generation.text}")
    print("Gemini model initialized successfully")
    
    # Flag to indicate if Gemini API is working
    GEMINI_WORKING = True
    
except Exception as e:
    print(f"ERROR with Gemini API: {str(e)}")
    print("Will fall back to local generation")
    GEMINI_WORKING = False
    model = None

# Ensure data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
NAMES_FILE = os.path.join(DATA_DIR, 'names.json')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Create backups directory if it doesn't exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Initialize names.json if it doesn't exist
if not os.path.exists(NAMES_FILE):
    with open(NAMES_FILE, 'w') as f:
        json.dump([], f)

# Helper functions
def load_names():
    try:
        with open(NAMES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_names(names):
    with open(NAMES_FILE, 'w') as f:
        json.dump(names, f, indent=2)
        
def create_backup():
    """Create a timestamped backup of the current names.json file"""
    try:
        # Check if the names file exists
        if not os.path.exists(NAMES_FILE):
            return None
            
        # Generate timestamp for the backup filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_filename = f"names-{timestamp}.json.bak"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Copy the current file to the backup location
        import shutil
        shutil.copy2(NAMES_FILE, backup_path)
        
        print(f"Created backup: {backup_path}")
        return backup_filename
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return None
        
def clean_team_name(name):
    """Clean team name by removing any JSON formatting"""
    if not name:
        return name
    
    # Remove JSON formatting artifacts
    cleaned = name
    # Remove quotes around the name
    if cleaned.startswith('"') and cleaned.endswith('"'):
        cleaned = cleaned[1:-1]
    
    # Remove JSON object notation if present
    import re
    # Pattern to match JSON object with name field
    json_pattern = r'^\s*{\s*"name"\s*:\s*"(.+?)".*}\s*$'
    match = re.match(json_pattern, cleaned)
    if match:
        cleaned = match.group(1)
    
    return cleaned

def generate_batch_id():
    """Generate a unique batch ID using timestamp and random string"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    random_suffix = str(uuid.uuid4())[:8]
    return f"{timestamp}-{random_suffix}"

def generate_local_name():
    """Generate a team name locally without using the API"""
    # Use the function from prompts.py
    result = get_random_local_team_name()
    print(f"Generated local name: {result['name']}")
    return result


# Track the last API request time
from datetime import datetime
last_api_request_time = datetime.now()

def generate_team_name(batch_mode=False):
    """Generate a team name using Gemini API with fallbacks"""
    global last_api_request_time
    
    # Enforce cooldown period between API calls (2 seconds)
    current_time = datetime.now()
    time_since_last_request = (current_time - last_api_request_time).total_seconds()
    if time_since_last_request < 2:  # 2-second cooldown
        import time
        time.sleep(2 - time_since_last_request)
    
    # Update the last request time
    last_api_request_time = datetime.now()
    
    # Track which generation method we're using
    generation_method = "gemini"
    
    # If Gemini API is not working, use local generation immediately
    if not GEMINI_WORKING or model is None:
        print("Gemini API not available, using local generation")
        result = generate_local_name()
        result["generation_method"] = "local"
        
        # Add batch-related fields if in batch mode
        if batch_mode:
            result["selected"] = False
            result["batch_id"] = None  # Will be set by the caller
            
        return result
    
    try:
        print("Attempting to generate team name with Gemini API...")
        
        # Get prompts from the prompts module
        prompts = get_team_name_prompt(batch_mode=batch_mode)
        system_prompt = prompts["system_prompt"]
        user_prompt = prompts["user_prompt"]
        
        # Add randomness to ensure diverse results
        timestamp = time.time()
        random_seed = random.randint(1000, 9999)
        
        # Add a randomness instruction to encourage diversity
        creativity_boost = [
            "Be wildly creative and avoid common patterns!",
            "Think outside the box with this team name!",
            "Create something truly unique and unexpected!",
            "Surprise me with an original team name concept!",
            "Use unexpected word combinations for maximum creativity!"
        ]
        
        # Add a random theme suggestion to increase diversity
        themes = [
            "space exploration", "quantum physics", "digital art", 
            "ocean technology", "sustainable innovation", "musical robots",
            "data visualization", "artificial intelligence", "virtual reality",
            "nanotechnology", "renewable energy", "biomimicry",
            "cosmic phenomena", "marine biology", "geometric patterns",
            "mythological creatures", "weather phenomena", "ancient civilizations",
            "futuristic transportation", "optical illusions", "molecular gastronomy"
        ]
        
        # Add specific instruction to avoid repetition
        avoid_names = ", ".join(list(RECENT_GENERATED_NAMES)[:10]) if RECENT_GENERATED_NAMES else "Tech Titans, Code Crafters, Brick Builders"
        avoid_instruction = f"\n\nIMPORTANT: DO NOT generate any of these previously used names: {avoid_names}"
        
        # Select random creativity boost and theme
        selected_boost = random.choice(creativity_boost)
        selected_theme = random.choice(themes)
        
        timestamp_prompt = f"{user_prompt}\n\n{selected_boost}\nConsider incorporating elements of {selected_theme} if it inspires you.{avoid_instruction}\n\nTimestamp: {timestamp}\nRandom: {random_seed}"
        
        print("Sending request to Gemini API for team name generation...")
        
        # Get generation parameters from prompts.py
        generation_config = get_generation_parameters(creativity_level="high")
        
        # Set a timeout for the API call
        import threading
        from concurrent.futures import ThreadPoolExecutor, TimeoutError
        
        def call_api():
            return model.generate_content(
                contents=timestamp_prompt,
                generation_config=generation_config
            )
        
        # Use ThreadPoolExecutor to set a timeout
        with ThreadPoolExecutor() as executor:
            future = executor.submit(call_api)
            try:
                response = future.result(timeout=10)  # 10 second timeout
                
                # Check if we got a valid response
                if hasattr(response, 'text') and response.text and len(response.text.strip()) > 0:
                    response_text = response.text.strip()
                    print(f"Raw response from Gemini API: {response_text}")
                    
                    # Parse the new format (TEAM NAME: and DESCRIPTION:)
                    team_name = None
                    description = None
                    
                    # Look for TEAM NAME: pattern
                    name_match = re.search(r'TEAM NAME:\s*(.+?)(?:\n|$)', response_text)
                    if name_match:
                        team_name = name_match.group(1).strip()
                    
                    # Look for DESCRIPTION: pattern
                    desc_match = re.search(r'DESCRIPTION:\s*(.+?)(?:\n|$)', response_text)
                    if desc_match:
                        description = desc_match.group(1).strip()
                    
                    # If we found both parts, we can skip generating a description separately
                    if team_name and description:
                        print(f"Successfully parsed team name: {team_name}")
                        print(f"Successfully parsed description: {description}")
                        
                        # Clean the team name to remove any JSON formatting that might have slipped through
                        team_name = clean_team_name(team_name)
                        
                        # Create the result directly
                        result = {
                            "name": team_name,
                            "description": description,
                            "generation_method": generation_method
                        }
                        return result
                    else:
                        # If we couldn't parse the format, just use the whole response as the team name
                        team_name = response_text
                        print(f"Could not parse formatted response, using raw text as team name: {team_name}")
                else:
                    print(f"ERROR: Empty or invalid response from Gemini API")
                    # Fall back to local generation
                    generation_method = "local"
                    result = generate_local_name()
                    return result
            except TimeoutError:
                print("Gemini API call timed out after 10 seconds")
                generation_method = "local"
                result = generate_local_name()
                return result
        
        # Generate description for the team name
        try:
            print(f"Generating description for team name: {team_name}")
            # Use a themed prompt for the description
            description_prompt = f"""
            Write a short, engaging description (10-15 words) for a FIRST LEGO League team named "{team_name}".
            
            IMPORTANT: Match the description to the team name's theme. If the name relates to technology, focus on that.
            If it relates to archaeology/UNEARTHED, focus on that theme. Make the description fit the name.
            
            Audience: Children aged 9-16
            Tone: Positive, encouraging, fun
            
            Return ONLY the description - no quotes, no explanation.
            """
            
            # Get generation parameters from prompts.py with medium creativity
            description_config = get_generation_parameters(creativity_level="medium")
            
            # Add randomness to prevent caching
            random_seed = random.randint(1000, 9999)
            timestamp = time.time()
            description_prompt = f"{description_prompt}\n\nTimestamp: {timestamp}\nRandom: {random_seed}"
            
            # Set a timeout for the description API call
            with ThreadPoolExecutor() as executor:
                future = executor.submit(lambda: model.generate_content(
                    contents=description_prompt,
                    generation_config=description_config
                ))
                try:
                    desc_response = future.result(timeout=5)  # 5 second timeout
                    
                    if hasattr(desc_response, 'text') and desc_response.text and len(desc_response.text.strip()) > 0:
                        description = desc_response.text.strip()
                        print(f"Successfully generated description: {description}")
                    else:
                        print("Empty description response, using fallback")
                        raise Exception("Empty description response")
                except TimeoutError:
                    print("Description API call timed out")
                    raise Exception("Description API timeout")
                
        except Exception as e:
            print(f"Error generating description: {str(e)}")
            # If we got a name from Gemini but description failed, mark as mixed
            if generation_method == "gemini":
                generation_method = "mixed"
            
            # Use our local description generator
            descriptions = [
                "Unearthing the past to build a better future!",
                "Connecting ancient wisdom with modern innovation!",
                "Exploring history's mysteries with LEGO ingenuity!",
                "Digging deep to discover creative solutions!",
                "Building bridges between past discoveries and future technology!",
                "Excavating ideas to construct tomorrow's innovations!",
                "Uncovering the building blocks of history with modern engineering!",
                "Where archaeological discovery meets LEGO creativity!",
                "Piecing together the past with the technology of tomorrow!",
                "Engineering excellence inspired by historical innovations!"
            ]
            
            description = random.choice(descriptions)
        
        # Clean the team name to remove any JSON formatting
        cleaned_name = clean_team_name(team_name)
        
        result = {
            "name": cleaned_name,
            "description": description,
            "generation_method": generation_method
        }
        
        print(f"Final result: {result}")
        return result
        
    except Exception as e:
        print(f"Error in main generate_team_name function: {str(e)}")
        print("Falling back to local name generation")
        
        # Use our local name generator as a reliable fallback
        result = generate_local_name()
        result["generation_method"] = "local_fallback"
        return result

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/batch')
def batch():
    return render_template('batch.html')

@app.route('/finalize')
def finalize():
    return render_template('finalize.html')

@app.route('/vote')
def vote():
    names = load_names()
    return render_template('vote.html', names=names)

@app.route('/reset')
def reset():
    # Hidden admin reset page - not linked from anywhere
    return render_template('reset.html')

# API Endpoints
@app.route('/api/generate-name', methods=['POST'])
def api_generate_name():
    """API endpoint to generate a new team name"""
    print("API endpoint called: /api/generate-name")
    # Add a timestamp to ensure we get a fresh response
    import time
    current_time = time.time()
    print(f"Request time: {current_time}")
    
    # Generate name with timestamp to avoid caching
    result = generate_team_name()
    
    # Add a timestamp to the response for debugging
    result["timestamp"] = current_time
    
    # Add unique ID
    result['id'] = str(uuid.uuid4())
    
    # Initialize votes to 0
    result['votes'] = 0
    
    return jsonify({
        'success': True,
        'name': result
    })

@app.route('/api/generate-batch', methods=['POST'])
def api_generate_batch():
    """API endpoint to generate a batch of team names"""
    print("API endpoint called: /api/generate-batch")
    # Add a timestamp to ensure we get a fresh response
    import time
    current_time = time.time()
    print(f"Request time: {current_time}")
    
    # Function to check if a name is too similar to existing names
    def is_too_similar(new_name, existing_names):
        """Check if a name is an exact duplicate of existing names"""
        if not new_name or not existing_names:
            return False
            
        # Convert to lowercase for comparison
        new_name_lower = new_name.lower()
        
        # Only check for exact matches to speed up generation
        for name_obj in existing_names:
            if isinstance(name_obj, dict):
                existing_name = name_obj.get('name', '').lower()
            else:
                existing_name = str(name_obj).lower()
                
            if existing_name == new_name_lower:
                return True
        
        return False
    
    # Generate batch of names
    batch_size = 20
    batch_id = generate_batch_id()
    batch_names = []
    
    # Load existing names to check for duplicates
    try:
        existing_names = load_names()
    except:
        existing_names = []
    
    # Keep track of names generated in this batch to avoid duplicates
    current_batch_names = []
    
    # Generate all names at once for maximum speed
    print(f"Generating {batch_size} team names in one batch...")
    
    # Generate names all at once
    for i in range(batch_size):
        try:
            print(f"Generating name {i+1}/{batch_size}...")
            result = generate_team_name(batch_mode=True)
            
            # Clean the team name
            result['name'] = clean_team_name(result['name'])
            
            # Track this name to avoid duplicates in future generations
            global RECENT_GENERATED_NAMES
            RECENT_GENERATED_NAMES.add(result['name'])
            
            # Keep the set at a reasonable size
            if len(RECENT_GENERATED_NAMES) > MAX_RECENT_NAMES:
                # Remove oldest items (convert to list, remove first items, convert back)
                temp_list = list(RECENT_GENERATED_NAMES)
                RECENT_GENERATED_NAMES = set(temp_list[-MAX_RECENT_NAMES:])
            
            # Add common fields
            result['timestamp'] = current_time
            result['id'] = str(uuid.uuid4())
            result['votes'] = 0
            result['batch_id'] = batch_id
            result['selected'] = False
            
            batch_names.append(result)
            
            # No delay needed with flash-lite model
            
        except Exception as e:
            print(f"Error generating team name: {str(e)}")
            continue
            
    # If we didn't get enough names, fill with some defaults
    if len(batch_names) < batch_size:
        print(f"Only generated {len(batch_names)} names, adding {batch_size - len(batch_names)} default names")
        
        # Use our creative names from prompts.py to fill in any gaps
        from prompts import LOCAL_TEAM_NAME_OPTIONS
        
        # Get a random sample of names we haven't used yet
        available_defaults = []
        for name_obj in LOCAL_TEAM_NAME_OPTIONS:
            if name_obj["name"] not in RECENT_GENERATED_NAMES:
                available_defaults.append(name_obj)
        
        # If we've used all our defaults, just use them all again
        if not available_defaults:
            available_defaults = LOCAL_TEAM_NAME_OPTIONS
            
        # Shuffle to get random order
        random.shuffle(available_defaults)
        default_names = available_defaults
        
        # Add as many default names as needed
        for i in range(min(batch_size - len(batch_names), len(default_names))):
            name_data = default_names[i]
            batch_names.append({
                "id": str(uuid.uuid4()),
                "name": name_data["name"],
                "description": name_data["description"],
                "votes": 0,
                "batch_id": batch_id,
                "selected": False,
                "timestamp": current_time,
                "generation_method": "default"
            })
    
    return jsonify({
        'success': True,
        'batch_id': batch_id,
        'names': batch_names
    })

@app.route('/api/save', methods=['POST'])
def api_save():
    """API endpoint to save a team name"""
    print("API endpoint called: /api/save")
    try:
        data = request.get_json()
        name_data = data.get('name', {})
        
        if not name_data:
            return jsonify({
                'success': False,
                'error': 'No name data provided'
            }), 400
        
        # Load existing names
        names = load_names()
        
        # Check if this name already exists (by ID if provided)
        name_id = name_data.get('id')
        if name_id:
            for i, existing_name in enumerate(names):
                if existing_name.get('id') == name_id:
                    # Update existing name
                    names[i] = name_data
                    save_names(names)
                    return jsonify({'success': True, 'updated': True})
        
        # Add new name
        names.append(name_data)
        save_names(names)
        
        return jsonify({'success': True, 'updated': False})
    except Exception as e:
        print(f"Error saving name: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save-shortlist', methods=['POST'])
def api_save_shortlist():
    """API endpoint to save multiple selected team names from a batch"""
    print("API endpoint called: /api/save-shortlist")
    try:
        data = request.get_json()
        selected_names = data.get('names', [])
        
        if not selected_names:
            return jsonify({
                'success': False,
                'error': 'No names provided'
            }), 400
        
        # Load existing names
        names = load_names()
        
        # Track which names were added vs updated
        added_count = 0
        updated_count = 0
        saved_names = []
        
        # Process each selected name
        for selected_name in selected_names:
            name_id = selected_name.get('id')
            if not name_id:
                continue
                
            # Check if name already exists
            found = False
            for i, existing_name in enumerate(names):
                if existing_name.get('id') == name_id:
                    # Update existing name
                    names[i] = selected_name
                    updated_count += 1
                    saved_names.append(selected_name)
                    found = True
                    break
            
            # Add new name if not found
            if not found:
                names.append(selected_name)
                added_count += 1
                saved_names.append(selected_name)
        
        # Save updated names list
        save_names(names)
        
        return jsonify({
            'success': True, 
            'added': added_count, 
            'updated': updated_count,
            'saved_names': saved_names
        })
    except Exception as e:
        print(f"Error saving shortlist: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes for custom name and getting names moved to avoid duplication

@app.route('/api/vote', methods=['POST'])
def api_vote():
    data = request.json
    name_id = data.get('id')
    
    if not name_id:
        return jsonify({"success": False, "error": "No ID provided"}), 400
    
    names = load_names()
    
    for name in names:
        if name['id'] == name_id:
            # Toggle vote (increment or decrement)
            if data.get('remove', False):
                name['votes'] = max(0, name['votes'] - 1)
            else:
                name['votes'] = name['votes'] + 1
            
            save_names(names)
            return jsonify({"success": True, "votes": name['votes']})
    
    return jsonify({"success": False, "error": "Name not found"}), 404

@app.route('/api/add-custom-name', methods=['POST'])
def api_add_custom_name():
    """API endpoint to add a custom team name"""
    print("API endpoint called: /api/add-custom-name")
    data = request.json
    
    if not data.get('name'):
        return jsonify({"success": False, "error": "Name is required"}), 400
    
    names = load_names()
    
    # Create new custom name entry
    new_name = {
        "id": str(uuid.uuid4()),
        "name": data.get('name'),
        "description": data.get('description', "A custom team name created by our team!"),
        "votes": 0,
        "source": "user",
        "created_at": datetime.now().isoformat()
    }
    
    names.append(new_name)
    save_names(names)
    
    return jsonify({"success": True, "name": new_name})

@app.route('/api/names', methods=['GET'])
def api_get_names():
    names = load_names()
    return jsonify(names)

@app.route('/api/remove-zero-votes', methods=['POST'])
def remove_zero_votes():
    try:
        # Load current names
        names = load_names()
        
        # Create backup before making changes
        backup_file = create_backup()
        
        # Count before removal
        total_before = len(names)
        
        # Filter out names with 0 votes
        names = [name for name in names if name.get('votes', 0) > 0]
        
        # Count after removal
        removed_count = total_before - len(names)
        
        # Save updated list
        save_names(names)
        
        return jsonify({
            'success': True,
            'message': f'Successfully removed {removed_count} team names with 0 votes.',
            'removed_count': removed_count,
            'backup_file': backup_file
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/remove-all-names', methods=['POST'])
def remove_all_names():
    try:
        # Load current names to get count
        names = load_names()
        removed_count = len(names)
        
        # Create backup before making changes
        backup_file = create_backup()
        
        # Save empty list
        save_names([])
        
        return jsonify({
            'success': True,
            'message': f'Successfully removed all {removed_count} team names.',
            'removed_count': removed_count,
            'backup_file': backup_file
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
