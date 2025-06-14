from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import uuid
import re
import shutil
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory

# Import name_generator functions for local generation
from name_generator import generate_team_name, generate_batch, get_random_team_name

# Global variables to track generated names and avoid repetition
RECENT_GENERATED_NAMES = set()
MAX_RECENT_NAMES = 100  # How many recent names to remember

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'fll_team_name_generator_secret_key_2025'  # Less secure but easier to manage

# Print startup message
print("Starting FLL Team Name Generator...")

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
    """Generate a team name locally using our word combination system"""
    # Use the function from name_generator.py
    result = get_random_team_name()
    print(f"Generated local name: {result['name']}")
    return result


# Track the last API request time for rate limiting
from datetime import datetime
last_api_request_time = datetime.now()

def generate_team_name(batch_mode=False, session_id=None):
    """Generate a team name using the word combination system.
    
    Args:
        batch_mode (bool): Whether this is part of a batch generation
        session_id (str): Optional session ID (kept for API compatibility)
        
    Returns:
        dict: A dictionary with name and description
    """
    global RECENT_GENERATED_NAMES, last_api_request_time
    
    # Enforce cooldown period between generations (0.5 seconds)
    current_time = datetime.now()
    time_since_last_request = (current_time - last_api_request_time).total_seconds()
    if time_since_last_request < 0.5:  # 0.5-second cooldown
        import time
        time.sleep(0.5 - time_since_last_request)
    
    # Update the last request time
    last_api_request_time = datetime.now()
    
    # Load existing names to avoid duplicates
    names = load_names()
    existing_names = [name["name"] for name in names]
    
    # If we're in batch mode, we want to avoid any names we've generated recently
    # to ensure variety in the batch
    avoid_names = RECENT_GENERATED_NAMES.union(set(existing_names)) if batch_mode else set(existing_names)
    
    print("Generating team name using word combination system...")
    
    # Generate a name using our new name generator
    for _ in range(5):  # Try up to 5 times to avoid duplicates
        name_data = get_random_team_name()
        
        # Check if this name is in our avoid list
        if name_data["name"].lower() not in [name.lower() for name in avoid_names]:
            # Add to recent names
            RECENT_GENERATED_NAMES.add(name_data["name"])
            if len(RECENT_GENERATED_NAMES) > MAX_RECENT_NAMES:
                # Remove oldest name (convert to list first for pop)
                recent_names_list = list(RECENT_GENERATED_NAMES)
                recent_names_list.pop(0)
                RECENT_GENERATED_NAMES = set(recent_names_list)
            
            # Add batch-related fields if in batch mode
            if batch_mode:
                name_data["selected"] = False
                name_data["batch_id"] = None  # Will be set by the caller
                
            print(f"Generated team name: {name_data['name']}")
            return name_data
        
    # If we couldn't generate a unique name after 5 tries, add a random suffix
    name_data = get_random_team_name()
    name_data["name"] = f"{name_data['name']} {random.randint(1, 99)}"
    
    # Add to recent names
    RECENT_GENERATED_NAMES.add(name_data["name"])
    if len(RECENT_GENERATED_NAMES) > MAX_RECENT_NAMES:
        # Remove oldest name (convert to list first for pop)
        recent_names_list = list(RECENT_GENERATED_NAMES)
        recent_names_list.pop(0)
        RECENT_GENERATED_NAMES = set(recent_names_list)
    
    # Add batch-related fields if in batch mode
    if batch_mode:
        name_data["selected"] = False
        name_data["batch_id"] = None  # Will be set by the caller
    
    print(f"Generated team name with random suffix: {name_data['name']}")
    return name_data

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
    
    # Get session ID from request if available - handle both JSON and form data
    try:
        if request.is_json:
            data = request.get_json() or {}
        else:
            # Handle form data or empty requests
            data = {}
    except Exception as e:
        print(f"Error parsing request data: {str(e)}")
        data = {}
        
    session_id = data.get('session_id')
    
    # If no session ID provided, create a new one
    if not session_id:
        session_id = str(uuid.uuid4())
        print(f"Created new session ID: {session_id}")
    else:
        print(f"Using provided session ID: {session_id}")
    
    # Generate name (session_id kept for API compatibility but not used)
    result = generate_team_name()
    
    # Add a timestamp to the response for debugging
    result["timestamp"] = current_time
    
    # Add unique ID
    result['id'] = str(uuid.uuid4())
    
    # Initialize votes to 0
    result['votes'] = 0
    
    # Include session ID in response
    result['session_id'] = session_id
    
    return jsonify({
        'success': True,
        'name': result
    })

@app.route('/api/generate-batch', methods=['POST'])
def api_generate_batch():
    """API endpoint to generate a batch of team names using our word combination system"""
    print("API endpoint called: /api/generate-batch")
    # Add a timestamp to ensure we get a fresh response
    import time
    current_time = time.time()
    print(f"Request time: {current_time}")
    
    try:
        # Get parameters from request - handle both JSON and form data
        try:
            if request.is_json:
                data = request.get_json() or {}
            else:
                # Handle form data or empty requests
                data = {}
        except Exception as e:
            print(f"Error parsing request data: {str(e)}")
            data = {}
            
        batch_size = data.get('count', 20)  # Default to 20 names
        
        # Limit to reasonable number
        batch_size = min(max(batch_size, 5), 50)  # Between 5 and 50
        
        print(f"Generating {batch_size} team names in one batch...")
        
        # Load existing names to avoid duplicates
        existing_names = load_names()
        existing_name_strings = [name["name"] for name in existing_names]
        
        # Use our new batch generation function from name_generator.py
        batch_names = generate_batch(count=batch_size, existing_names=existing_name_strings)
        
        print(f"Successfully generated {len(batch_names)} team names")
        
        # Ensure all names have required fields
        global RECENT_GENERATED_NAMES, MAX_RECENT_NAMES
        
        for name in batch_names:
            # Clean the team name if needed
            if 'name' in name:
                name['name'] = clean_team_name(name['name'])
            
            # Add to recent names set to avoid repetition
            RECENT_GENERATED_NAMES.add(name['name'])
            
            # Keep the set at a reasonable size
            if len(RECENT_GENERATED_NAMES) > MAX_RECENT_NAMES:
                # Remove oldest items (convert to list, remove first items, convert back)
                temp_list = list(RECENT_GENERATED_NAMES)
                RECENT_GENERATED_NAMES = set(temp_list[-MAX_RECENT_NAMES:])
        
        # Get the batch ID from the first name (all should have the same batch ID)
        batch_id = batch_names[0].get('batch_id') if batch_names else generate_batch_id()
        
        return jsonify({
            'success': True,
            'names': batch_names,
            'batch_id': batch_id
        })
    except Exception as e:
        print(f"Error generating batch: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

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

@app.route('/api/vote', methods=['POST'])
def api_vote():
    data = request.json
    name_id = data.get('id')
    
    if not name_id:
        return jsonify({"success": False, "error": "No ID provided"}), 400
    
    # Initialize user votes in session if needed
    if 'voted_names' not in session:
        session['voted_names'] = []
    
    names = load_names()
    
    for name in names:
        if name['id'] == name_id:
            # Check if user has already voted for this name
            if name_id in session['voted_names']:
                # Remove vote
                session['voted_names'].remove(name_id)
                name['votes'] = max(0, name['votes'] - 1)
                user_voted = False
            else:
                # Add vote
                session['voted_names'].append(name_id)
                name['votes'] = name['votes'] + 1
                user_voted = True
            
            # Save changes
            session.modified = True
            save_names(names)
            
            return jsonify({
                "success": True, 
                "votes": name['votes'],
                "user_voted": user_voted
            })
    
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
    
    # Initialize user votes in session if needed
    if 'voted_names' not in session:
        session['voted_names'] = []
    
    # Add user_voted flag to each name
    for name in names:
        name['user_voted'] = name['id'] in session['voted_names']
    
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
