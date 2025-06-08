# Gemini AI Integration Guide

This document provides a comprehensive guide on integrating Google's Gemini AI into your projects, including model selection, configuration, and best practices.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup & Installation](#setup--installation)
3. [Model Selection](#model-selection)
4. [Basic Implementation](#basic-implementation)
5. [Advanced Configuration](#advanced-configuration)
6. [Prompt Engineering](#prompt-engineering)
7. [Error Handling](#error-handling)
8. [Performance Optimization](#performance-optimization)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8+
- Google Cloud account
- Gemini API key (from [Google AI Studio](https://makersuite.google.com/))
- Basic knowledge of Python and web development

## Setup & Installation

1. Install the required package:
   ```bash
   pip install google-generativeai
   ```

2. Set up your API key (never commit this to version control):
   - Create a `config.py` file in your project root
   - Add your API key:
     ```python
     # config.py
     GEMINI_API_KEY = "your-api-key-here"
     ```
   - Add `config.py` to your `.gitignore`

## Model Selection

### Available Models

| Model Name | Description | Best For | Max Tokens |
|------------|-------------|----------|------------|
| `gemini-1.5-pro` | Most capable model for complex tasks | Advanced reasoning, coding, instruction following | 1M |
| `gemini-1.5-flash` | Optimized for speed and efficiency | Fast responses, simple tasks | 1M |
| `gemini-1.0-pro` | General purpose model | Text generation, Q&A | 30K |
| `gemini-1.0-pro-vision` | Multimodal model | Image + text tasks | 30K |

### Choosing the Right Model

- **For text generation with reasoning**: `gemini-1.5-pro`
- **For fast responses**: `gemini-1.5-flash`
- **For multimodal inputs**: `gemini-1.0-pro-vision`
- **For cost-effective text generation**: `gemini-1.0-pro`

## Basic Implementation

```python
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_response(prompt):
    """Generate a response using Gemini AI"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Example usage
prompt = "Generate a creative team name for a robotics competition"
response = generate_response(prompt)
print(response)
```

## Advanced Configuration

### Safety Settings

```python
from google.generativeai.types import HarmCategory, HarmBlockThreshold

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

response = model.generate_content(
    prompt,
    safety_settings=safety_settings
)
```

### Generation Configuration

```python
generation_config = {
    "temperature": 0.9,  # Higher temperature for more creativity
    "top_p": 0.95,      # Nucleus sampling parameter
    "top_k": 40,        # Top-k sampling
    "max_output_tokens": 30,  # Shorter output for team names
}

response = model.generate_content(
    prompt,
    generation_config=generation_config,
    safety_settings=safety_settings
)
```

## Prompt Engineering

### Best Practices

1. **Be Specific**
   ```
   Bad: "Generate a team name"
   Good: "Generate a creative and unique team name for a high school robotics team competing in the FIRST LEGO League. The theme is SPACE EXPLORATION. The name should be 2-3 words maximum and appeal to 12-16 year olds."
   ```

2. **Use System Messages** (for chat models)
   ```python
   model = genai.GenerativeModel('gemini-1.5-pro')
   chat = model.start_chat(history=[])
   
   response = chat.send_message("""You are a creative naming assistant for robotics teams. 
   Generate names that are fun, memorable, and appropriate for all ages.""")
   ```

3. **Provide Examples**
   ```
   Generate a team name similar to these examples:
   - Quantum Quokkas
   - RoboRaptors
   - Circuit Storm
   - The Build Brigade
   ```

4. **Control Output Format**
   ```
   Generate 5 team names in this JSON format:
   {
     "names": ["name1", "name2", ...],
     "themes": ["theme1", "theme2", ...],
     "descriptions": ["description1", "description2", ...]
   }
   ```

## Error Handling

```python
def safe_generate(prompt, max_retries=3):
    """Generate content with retry logic"""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if response.text:
                return response.text
        except Exception as e:
            if "quota" in str(e).lower():
                raise Exception("API quota exceeded. Please check your usage limits.")
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return None
            time.sleep(1)  # Wait before retry
    return None
```

## Performance Optimization

1. **Batch Processing**
   ```python
   prompts = ["prompt 1", "prompt 2", "prompt 3"]
   responses = [model.generate_content(prompt) for prompt in prompts]
   ```

2. **Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_cached_response(prompt):
       return model.generate_content(prompt)
   ```

3. **Rate Limiting**
   ```python
   import time
   from ratelimit import limits, sleep_and_retry
   
   # 60 calls per minute
   CALLS = 60
   PERIOD = 60
   
   @sleep_and_retry
   @limits(calls=CALLS, period=PERIOD)
   def limited_generate(prompt):
       return model.generate_content(prompt)
   ```

## Security Considerations

1. **Never expose API keys**
   - Use environment variables or config files
   - Add sensitive files to `.gitignore`
   
2. **Input Sanitization**
   ```python
   import re
   
   def sanitize_input(text):
       # Remove any HTML/JS tags
       sanitized = re.sub(r'<[^>]+>', '', text)
       # Limit length
       return sanitized[:1000]
   ```

3. **Content Moderation**
   ```python
   def is_content_safe(text):
       response = model.generate_content(
           f"Is this content appropriate for all ages? Respond with 'yes' or 'no' only.\n\n{text}"
       )
       return response.text.strip().lower() == 'yes'
   ```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify the API key is correct
   - Check if the key has the required permissions
   - Ensure billing is enabled on your Google Cloud account

2. **Rate Limiting**
   - Implement exponential backoff
   - Cache responses when possible
   - Monitor usage in Google Cloud Console

3. **Content Blocking**
   - Review safety settings
   - Adjust `HarmBlockThreshold` if needed
   - Add more context to your prompts

4. **Model Not Responding**
   - Check your internet connection
   - Verify the model name is correct
   - Try with a simpler prompt

### Debugging Tips

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Print the full response object
print(response)

# Check for safety ratings
for rating in response.safety_ratings:
    print(f"{rating.category.name}: {rating.probability.name}")
```

## Example: Team Name Generator

```python
import google.generativeai as genai
from config import GEMINI_API_KEY
import time
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def setup_gemini():
    """Initialize and configure the Gemini model"""
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Safety settings as a list of dictionaries
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    ]
    
    # Initialize the model with safety settings
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        safety_settings=safety_settings
    )

def generate_team_name():
    """Generate a team name using Gemini API with fallbacks"""
    model = setup_gemini()
    
    try:
        # Create a prompt with specific instructions
        prompt = """
        Create ONE unique and creative team name for a FIRST LEGO League robotics team (ages 9-16).
        
        IMPORTANT: Create a DIVERSE range of names. Only 30% of names should relate to the UNEARTHED archaeology theme.
        The other 70% should focus on:
        - Technology and innovation
        - Robotics and engineering
        - Creativity and problem-solving
        - Teamwork and collaboration
        - Science and discovery in general
        
        Return ONLY the team name - no quotes, no explanation, no additional text.
        """
        
        # Add randomness to prevent caching
        timestamp = time.time()
        random_seed = random.randint(1000, 9999)
        timestamp_prompt = f"{prompt}\n\nTimestamp: {timestamp}\nRandom: {random_seed}"
        
        # Set generation parameters
        generation_config = {
            "temperature": 0.9,  # Higher temperature for more creativity
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 30,
        }
        
        # Generate the team name with timeout
        def call_api():
            return model.generate_content(
                contents=timestamp_prompt,
                generation_config=generation_config
            )
        
        with ThreadPoolExecutor() as executor:
            future = executor.submit(call_api)
            try:
                response = future.result(timeout=10)  # 10 second timeout
                
                if hasattr(response, 'text') and response.text and len(response.text.strip()) > 0:
                    team_name = response.text.strip()
                    return {
                        "name": team_name,
                        "generation_method": "gemini"
                    }
            except TimeoutError:
                print("Gemini API call timed out")
                
        # Fallback to local generation if Gemini fails
        return generate_local_name()
        
    except Exception as e:
        print(f"Error generating team name: {e}")
        return generate_local_name()

def generate_local_name():
    """Generate a team name locally without using the API"""
    # Local fallback implementation
    first_parts = ["Quantum", "Robo", "Tech", "Nova", "Cyber", "Mecha", "Neo", "Titan", "Aero", "Nano"]
    second_parts = ["Pioneers", "Innovators", "Builders", "Creators", "Explorers", "Inventors", "Makers"]
    
    name = f"{random.choice(first_parts)} {random.choice(second_parts)}"
    return {
        "name": name,
        "description": f"A team of creative builders and problem solvers!",
        "generation_method": "local"
    }
```

## Resources

- [Gemini API Documentation](https://ai.google.dev/)
- [Google AI Studio](https://makersuite.google.com/)
- [Gemini Safety Settings](https://ai.google/gemini-api/docs/safety-settings)
- [Prompt Engineering Guide](https://ai.google.dev/docs/prompt_best_practices)

## Version History

- **1.0.0** - Initial guide created
- **1.1.0** - Added advanced configuration and error handling
- **1.2.0** - Added security considerations and troubleshooting

---

*Note: Always refer to the official Gemini API documentation for the most up-to-date information and best practices.*
