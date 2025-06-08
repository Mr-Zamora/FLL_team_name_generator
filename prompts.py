"""
FLL Team Name Generator - Prompt Engineering Module

This module contains all prompt templates and prompt engineering logic used for
generating team names with the Gemini API. Separating these prompts makes it
easier to experiment with different prompt strategies without changing the
core application code.
"""

# Constants for prompt engineering
DEFAULT_TEMPERATURE = 1.0  # Increased for more creativity
DEFAULT_TOP_P = 0.98      # Increased for more diversity
DEFAULT_TOP_K = 60        # Increased for more options
DEFAULT_MAX_OUTPUT_TOKENS = 100

# Base prompt templates
TEAM_NAME_SYSTEM_PROMPT = """You are a creative assistant that specializes in generating fun, 
engaging, and appropriate team names for FIRST LEGO League (FLL) robotics competitions. 
FLL teams consist of students aged 9-16 who build and program LEGO robots to solve challenges."""

TEAM_NAME_USER_PROMPT = """Generate a HIGHLY CREATIVE and UNIQUE team name for a FIRST LEGO League robotics team.
The name should be:
- Appropriate for students aged 9-16
- Related to robotics, technology, engineering, innovation, or science
- Catchy, memorable, and ORIGINAL (2-3 words maximum)
- Positive and inspiring
- AVOID common, generic team names like "Tech Titans", "Code Crafters", "Brick Builders", "Logic Legends", etc.

Be EXTREMELY CREATIVE! Use unexpected word combinations, clever wordplay, or unique metaphors.
Examples of creative names: "Quantum Quokkas", "Neon Neurons", "Pixel Pirates", "Atomic Acrobats"

IMPORTANT: DO NOT USE JSON FORMAT IN YOUR RESPONSE.

Respond in the following format exactly:

TEAM NAME: [your team name here]
DESCRIPTION: [your description here]

Example response:
TEAM NAME: Circuit Navigators
DESCRIPTION: Charting new paths through technology while building innovative LEGO robot solutions!

Never include quotes, curly braces, or any JSON formatting in your response."""

BATCH_VARIATION_PROMPT = """Generate a HIGHLY CREATIVE and UNIQUE team name for a FIRST LEGO League robotics team.
This name MUST be COMPLETELY DIFFERENT from common team names.

The name should be:
- Appropriate for students aged 9-14
- Related to robotics, technology, engineering, innovation, or science
- Catchy, memorable, and ORIGINAL (2-3 words maximum)
- Positive and inspiring
- ABSOLUTELY AVOID common, generic team names like "Tech Titans", "Code Crafters", "Brick Builders", "Logic Legends", "Robo Rangers", "Gear Geniuses", "Algorithm Aces", etc.

Be EXTREMELY CREATIVE! Use unexpected word combinations, clever wordplay, or unique metaphors.
Examples of creative names: "Quantum Quokkas", "Neon Neurons", "Pixel Pirates", "Atomic Acrobats", "Binary Bandits", "Cyber Cyclones"

IMPORTANT: DO NOT USE JSON FORMAT IN YOUR RESPONSE.

Respond in the following format exactly:

TEAM NAME: [your team name here]
DESCRIPTION: [your description here]

Example response:
TEAM NAME: Circuit Navigators
DESCRIPTION: Charting new paths through technology while building innovative LEGO robot solutions!

Never include quotes, curly braces, or any JSON formatting in your response."""

# Advanced prompt templates
THEMED_PROMPT_TEMPLATE = """Generate a creative and unique team name for a FIRST LEGO League robotics team.
The name should be:
- Appropriate for students aged 9-14
- Related to robotics, technology, engineering, or innovation
- Catchy and memorable (2-3 words maximum)
- Positive and inspiring
- Original (avoid common team names)
- Incorporate elements related to the theme: {theme}

IMPORTANT: DO NOT USE JSON FORMAT IN YOUR RESPONSE.

Respond in the following format exactly:

TEAM NAME: [your team name here]
DESCRIPTION: [your description here]

Example response:
TEAM NAME: Circuit Navigators
DESCRIPTION: Charting new paths through technology while building innovative LEGO robot solutions!

Never include quotes, curly braces, or any JSON formatting in your response."""

STYLE_PROMPT_TEMPLATE = """Generate a creative and unique team name for a FIRST LEGO League robotics team.
The name should be:
- Appropriate for students aged 9-16
- Related to robotics, technology, engineering, or innovation
- Catchy and memorable (2-3 words maximum)
- Positive and inspiring
- Original (avoid common team names)
- Use a {style} style or tone

IMPORTANT: DO NOT USE JSON FORMAT IN YOUR RESPONSE.

Respond in the following format exactly:

TEAM NAME: [your team name here]
DESCRIPTION: [your description here]

Example response:
TEAM NAME: Circuit Navigators
DESCRIPTION: Charting new paths through technology while building innovative LEGO robot solutions!

Never include quotes, curly braces, or any JSON formatting in your response.

Example response format:
{
  "name": "Circuit Navigators",
  "description": "Circuit Navigators: Charting new paths through technology while building innovative LEGO robot solutions!"
}"""

# Local fallback name generation
LOCAL_TEAM_NAME_OPTIONS = [
    {
        "name": "Quantum Quokkas",
        "description": "Hopping through quantum possibilities with adorable precision."
    },
    {
        "name": "Neon Neurons",
        "description": "Illuminating the competition with bright ideas and neural networks."
    },
    {
        "name": "Pixel Pirates",
        "description": "Sailing the digital seas and capturing victory one pixel at a time."
    },
    {
        "name": "Atomic Acrobats",
        "description": "Performing amazing technical feats with atomic precision."
    },
    {
        "name": "Binary Bandits",
        "description": "Stealing the show with ones and zeros and innovative solutions."
    },
    {
        "name": "Cyber Cyclones",
        "description": "Swirling up powerful tech solutions with unstoppable force."
    },
    {
        "name": "Flux Foxes",
        "description": "Cleverly adapting to any challenge with quick thinking and agility."
    },
    {
        "name": "Cosmic Coders",
        "description": "Programming solutions that are out of this world."
    },
    {
        "name": "Laser Lemurs",
        "description": "Leaping through challenges with laser-focused precision."
    },
    {
        "name": "Digital Dolphins",
        "description": "Navigating the sea of technology with intelligence and teamwork."
    },
    {
        "name": "Nano Ninjas",
        "description": "Stealthily solving problems with tiny but powerful solutions."
    },
    {
        "name": "Quantum Quills",
        "description": "Writing the future of robotics with quantum-inspired innovation."
    },
    {
        "name": "Sonic Squirrels",
        "description": "Gathering ideas at lightning speed and building with quick precision."
    },
    {
        "name": "Hologram Heroes",
        "description": "Projecting excellence in every dimension of robotics."
    },
    {
        "name": "Nebula Knights",
        "description": "Defending innovation across the galaxy of STEM challenges."
    },
    {
        "name": "Prism Pandas",
        "description": "Reflecting multiple perspectives with strength and creativity."
    },
    {
        "name": "Vector Velociraptors",
        "description": "Racing toward solutions with unstoppable momentum and precision."
    },
    {
        "name": "Techno Toucans",
        "description": "Adding colorful innovation to the world of robotics."
    },
    {
        "name": "Gamma Geckos",
        "description": "Sticking to challenges with unwavering determination."
    },
    {
        "name": "Photon Phoenixes",
        "description": "Rising from challenges with brilliant flashes of innovation."
    },
    {
        "name": "Laser Builders",
        "description": "Building with laser-like precision and focus."
    },
    {
        "name": "Robotic Rebels",
        "description": "Breaking boundaries and defying limits in robotics."
    }
]

# Function to get a prompt based on parameters
def get_team_name_prompt(batch_mode=False, theme=None, style=None):
    """
    Get the appropriate prompt for team name generation based on parameters.
    
    Args:
        batch_mode (bool): Whether this is part of a batch generation
        theme (str, optional): A theme to incorporate into the name
        style (str, optional): A specific style for the name
        
    Returns:
        dict: A dictionary with system_prompt and user_prompt keys
    """
    system_prompt = TEAM_NAME_SYSTEM_PROMPT
    
    if theme:
        user_prompt = THEMED_PROMPT_TEMPLATE.format(theme=theme)
    elif style:
        user_prompt = STYLE_PROMPT_TEMPLATE.format(style=style)
    elif batch_mode:
        user_prompt = BATCH_VARIATION_PROMPT
    else:
        user_prompt = TEAM_NAME_USER_PROMPT
        
    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    }

# Function to get generation parameters
def get_generation_parameters(creativity_level="medium"):
    """
    Get the appropriate generation parameters based on creativity level.
    
    Args:
        creativity_level (str): Level of creativity - "low", "medium", or "high"
        
    Returns:
        dict: A dictionary with generation parameters
    """
    if creativity_level == "low":
        return {
            "temperature": 0.6,
            "top_p": 0.85,
            "top_k": 30,
            "max_output_tokens": 100
        }
    elif creativity_level == "high":
        return {
            "temperature": 0.9,
            "top_p": 0.98,
            "top_k": 50,
            "max_output_tokens": 100
        }
    else:  # medium (default)
        return {
            "temperature": DEFAULT_TEMPERATURE,
            "top_p": DEFAULT_TOP_P,
            "top_k": DEFAULT_TOP_K,
            "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS
        }

# Function to get a random local team name
def get_random_local_team_name():
    """
    Get a random team name from the local options list.
    
    Returns:
        dict: A dictionary with name and description
    """
    import random
    return random.choice(LOCAL_TEAM_NAME_OPTIONS)
