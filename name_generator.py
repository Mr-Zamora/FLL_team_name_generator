"""FLL Team Name Generator - Name Generation Module

This module contains all the logic for generating team names using word combinations
from the word_components.json file. It replaces the previous prompt engineering
approach with a deterministic but random word combination system.
"""

import json
import os
import random
from datetime import datetime

# Constants
COMPONENTS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'word_components.json')

# Cache for word components
_word_components = None

def load_word_components():
    """
    Load word components from the JSON file.
    
    Returns:
        dict: The word components dictionary
    """
    global _word_components
    
    if _word_components is None:
        try:
            with open(COMPONENTS_FILE, 'r') as f:
                _word_components = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading word components: {str(e)}")
            # Provide minimal fallback if file can't be loaded
            _word_components = {
                "prefixes": [{"word": "Tech", "category": "tech", "compatibility": ["tech"]}],
                "suffixes": [{"word": "Team", "category": "group", "compatibility": ["tech"]}],
                "nouns": [{"word": "Robots", "category": "tech", "compatibility": ["tech"]}],
                "animals": [{"word": "Eagles", "category": "animal", "compatibility": ["nature"]}],
                "adjectives": [{"word": "Creative", "category": "trait", "compatibility": ["abstract"]}],
                "description_templates": ["A creative robotics team!"]
            }
    
    return _word_components

def find_compatible_words(word_type, compatibility=None):
    """
    Find words from a specific type that match the given compatibility.
    
    Args:
        word_type (str): The type of word to find (prefixes, suffixes, etc.)
        compatibility (list, optional): List of compatibility tags to match
        
    Returns:
        list: List of compatible words
    """
    components = load_word_components()
    
    if word_type not in components:
        return []
    
    if not compatibility:
        return components[word_type]
    
    return [
        word for word in components[word_type]
        if any(tag in word.get("compatibility", []) for tag in compatibility)
    ]

def generate_team_name(existing_names=None):
    """
    Generate a team name using word combinations.
    
    Args:
        existing_names (list, optional): List of existing names to avoid duplicates
        
    Returns:
        dict: A dictionary with name and description
    """
    components = load_word_components()
    existing_names = existing_names or []
    
    # Choose a name pattern randomly
    patterns = [
        generate_prefix_suffix,
        generate_prefix_noun,
        generate_adjective_animal,
        generate_prefix_animal
    ]
    
    # Try up to 10 times to generate a unique name
    for _ in range(10):
        generator_func = random.choice(patterns)
        name_data = generator_func()
        
        # Check if name already exists - handle both string and dict formats
        name_exists = False
        for existing in existing_names:
            if isinstance(existing, dict) and existing.get("name"):
                if name_data["name"].lower() == existing["name"].lower():
                    name_exists = True
                    break
            elif isinstance(existing, str):
                if name_data["name"].lower() == existing.lower():
                    name_exists = True
                    break
        
        if not name_exists:
            return name_data
    
    # If we couldn't generate a unique name, add a random number to make it unique
    name_data = random.choice(patterns)()
    name_data["name"] = f"{name_data['name']} {random.randint(1, 99)}"
    return name_data

def generate_prefix_suffix():
    """Generate a team name using prefix + suffix pattern"""
    components = load_word_components()
    
    prefix = random.choice(components["prefixes"])
    
    # Find compatible suffixes
    compatible_suffixes = find_compatible_words("suffixes", prefix.get("compatibility"))
    if not compatible_suffixes:
        compatible_suffixes = components["suffixes"]
    
    suffix = random.choice(compatible_suffixes)
    
    # Get a random adjective for the description
    adjective = random.choice(components["adjectives"])
    
    name = f"{prefix['word']} {suffix['word']}"
    description = generate_description(prefix, suffix, adjective)
    
    return {
        "name": name,
        "description": description,
        "generation_method": "word_combination"
    }

def generate_prefix_noun():
    """Generate a team name using prefix + noun pattern"""
    components = load_word_components()
    
    prefix = random.choice(components["prefixes"])
    
    # Find compatible nouns
    compatible_nouns = find_compatible_words("nouns", prefix.get("compatibility"))
    if not compatible_nouns:
        compatible_nouns = components["nouns"]
    
    noun = random.choice(compatible_nouns)
    
    # Get a random adjective for the description
    adjective = random.choice(components["adjectives"])
    
    name = f"{prefix['word']} {noun['word']}"
    description = generate_description(prefix, noun, adjective)
    
    return {
        "name": name,
        "description": description,
        "generation_method": "word_combination"
    }

def generate_adjective_animal():
    """Generate a team name using adjective + animal pattern"""
    components = load_word_components()
    
    adjective = random.choice(components["adjectives"])
    
    # Find compatible animals
    compatible_animals = find_compatible_words("animals", adjective.get("compatibility"))
    if not compatible_animals:
        compatible_animals = components["animals"]
    
    animal = random.choice(compatible_animals)
    
    name = f"{adjective['word']} {animal['word']}"
    description = generate_description(adjective, animal)
    
    return {
        "name": name,
        "description": description,
        "generation_method": "word_combination"
    }

def generate_prefix_animal():
    """Generate a team name using prefix + animal pattern"""
    components = load_word_components()
    
    prefix = random.choice(components["prefixes"])
    
    # Find compatible animals
    compatible_animals = find_compatible_words("animals", prefix.get("compatibility"))
    if not compatible_animals:
        compatible_animals = components["animals"]
    
    animal = random.choice(compatible_animals)
    
    # Get a random adjective for the description
    adjective = random.choice(components["adjectives"])
    
    name = f"{prefix['word']} {animal['word']}"
    description = generate_description(prefix, animal, adjective)
    
    return {
        "name": name,
        "description": description,
        "generation_method": "word_combination"
    }

def generate_description(word1, word2, adjective=None):
    """
    Generate a description using a template that matches the team name structure.
    
    Args:
        word1 (dict): First word component
        word2 (dict): Second word component
        adjective (dict, optional): Adjective to use in description
        
    Returns:
        str: Generated description
    """
    components = load_word_components()
    
    # If no adjective provided, get one
    if not adjective:
        adjective = random.choice(components["adjectives"])
    
    # Determine which word is prefix/suffix for template
    prefix_word = word1.get("word", "Team")
    suffix_word = word2.get("word", "Builders")
    
    if "category" in word1 and word1["category"] in ["trait", "abstract"]:
        adjective_word = word1.get("word", "Creative")
    else:
        adjective_word = adjective.get("word", "Creative")
    
    # Determine animal and noun words if needed
    has_animal = False
    animal_word = ""
    has_noun = False
    noun_word = ""
    
    # Check if the team name contains an animal
    if "category" in word1 and word1["category"] == "animal":
        has_animal = True
        animal_word = word1.get("word", "Eagles")
    elif "category" in word2 and word2["category"] == "animal":
        has_animal = True
        animal_word = word2.get("word", "Eagles")
    
    # Check if the team name contains a noun
    if "category" in word1 and word1["category"] in ["tech", "mechanics", "building"]:
        has_noun = True
        noun_word = word1.get("word", "Robots")
    elif "category" in word2 and word2["category"] in ["tech", "mechanics", "building"]:
        has_noun = True
        noun_word = word2.get("word", "Robots")
    
    # Filter templates based on team name structure
    suitable_templates = []
    for template in components["description_templates"]:
        # If team has an animal, include templates with {animal}
        if has_animal and "{animal}" in template:
            suitable_templates.append(template)
        # If team has a noun, include templates with {noun} or {nouns}
        elif has_noun and ("{noun}" in template or "{nouns}" in template):
            suitable_templates.append(template)
        # Include templates that only use {prefix}, {suffix}, and {adjective}
        elif not ("{animal}" in template or "{noun}" in template or "{nouns}" in template):
            suitable_templates.append(template)
    
    # If no suitable templates found, use generic ones
    if not suitable_templates:
        suitable_templates = [
            "{prefix} {suffix}: {adjective} problem solvers building the future with LEGO robotics!",
            "The {adjective} {prefix} {suffix} constructing tomorrow's innovations through creative engineering!",
            "Combining {adjective} thinking with robotic expertise to solve challenging problems!"
        ]
    
    # Select a random template from suitable ones
    template = random.choice(suitable_templates)
    
    # Replace placeholders in template
    description = template.replace("{prefix}", prefix_word)
    description = description.replace("{suffix}", suffix_word)
    description = description.replace("{adjective}", adjective_word)
    description = description.replace("{animal}", animal_word)
    description = description.replace("{noun}", noun_word)
    description = description.replace("{nouns}", noun_word)
    
    return description

def generate_batch(count=20, existing_names=None):
    """
    Generate a batch of team names.
    
    Args:
        count (int): Number of names to generate
        existing_names (list, optional): List of existing names to avoid duplicates
        
    Returns:
        list: List of generated name dictionaries
    """
    existing_names = existing_names or []
    batch = []
    
    # Generate unique batch ID
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    random_suffix = ''.join(random.choices('0123456789abcdef', k=8))
    batch_id = f"{timestamp}-{random_suffix}"
    
    # Generate names
    for _ in range(count):
        # Get a name that doesn't exist in existing_names or already generated batch
        name_data = None
        for attempt in range(5):  # Try up to 5 times
            temp_data = generate_team_name()
            
            # Check if this name is already in existing names or batch
            if temp_data["name"].lower() not in [n.lower() for n in existing_names] and \
               temp_data["name"].lower() not in [n["name"].lower() for n in batch]:
                name_data = temp_data
                break
        
        # If we couldn't find a unique name, add a random suffix
        if name_data is None:
            name_data = generate_team_name()
            name_data["name"] = f"{name_data['name']} {random.randint(1, 99)}"
        
        # Add metadata
        name_data["id"] = generate_unique_id()
        name_data["batch_id"] = batch_id
        name_data["timestamp"] = datetime.now().timestamp()
        name_data["selected"] = False
        name_data["votes"] = 0
        
        batch.append(name_data)
    
    return batch

def generate_unique_id():
    """Generate a unique ID for a team name"""
    import uuid
    return str(uuid.uuid4())

def get_random_team_name():
    """
    Get a single random team name.
    
    Returns:
        dict: A dictionary with name and description
    """
    name_data = generate_team_name()
    
    # Add metadata
    name_data["id"] = generate_unique_id()
    name_data["timestamp"] = datetime.now().timestamp()
    name_data["votes"] = 0
    
    return name_data
