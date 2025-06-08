# Gemini API Reference

This document provides a concise reference for using the Gemini API in the FLL Team Name Generator project.

## Table of Contents
- [Authentication](#authentication)
- [Model Configuration](#model-configuration)
- [Content Generation](#content-generation)
- [Safety Settings](#safety-settings)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Example Implementation](#example-implementation)

## Authentication

```python
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key='YOUR_API_KEY')
```

## Model Configuration

### Model Selection
```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    safety_settings=SAFETY_SETTINGS
)
```

### Generation Configuration
```python
generation_config = {
    "temperature": 0.9,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 30,
    "candidate_count": 1
}
```

## Safety Settings

```python
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
```

## Content Generation

### Basic Generation
```python
response = model.generate_content(
    "Generate a creative team name for FIRST LEGO League",
    generation_config=generation_config
)
print(response.text)
```

### Streaming Response
```python
response = model.generate_content(
    "Generate a creative team name for FIRST LEGO League",
    stream=True
)

for chunk in response:
    print(chunk.text)
```

## Error Handling

### Basic Error Handling
```python
try:
    response = model.generate_content(prompt)
    if not response.text:
        raise ValueError("Empty response from API")
    return response.text
except Exception as e:
    print(f"Error generating content: {str(e)}")
    return None
```

### Timeout Handling
```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def generate_with_timeout(prompt, timeout=10):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(model.generate_content, prompt)
        try:
            response = future.result(timeout=timeout)
            return response.text
        except TimeoutError:
            print("Request timed out")
            return None
```

## Rate Limiting

Implement a simple cooldown between requests:

```python
import time

last_request_time = 0
REQUEST_COOLDOWN = 2  # seconds

def rate_limited_generate(prompt):
    global last_request_time
    
    # Enforce cooldown
    elapsed = time.time() - last_request_time
    if elapsed < REQUEST_COOLDOWN:
        time.sleep(REQUEST_COOLDOWN - elapsed)
    
    try:
        response = model.generate_content(prompt)
        last_request_time = time.time()
        return response.text
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

## Example Implementation

Here's a complete example that ties everything together:

```python
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

# Configuration
GEMINI_API_KEY = "your-api-key-here"
genai.configure(api_key=GEMINI_API_KEY)

# Model and safety settings
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

GENERATION_CONFIG = {
    "temperature": 0.9,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 30,
    "candidate_count": 1
}

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=GENERATION_CONFIG,
    safety_settings=SAFETY_SETTINGS
)

# Rate limiting
last_request_time = 0
REQUEST_COOLDOWN = 2  # seconds

def generate_team_name(theme=None, timeout=10):
    """Generate a team name with optional theme."""
    global last_request_time
    
    # Enforce cooldown
    elapsed = time.time() - last_request_time
    if elapsed < REQUEST_COOLDOWN:
        time.sleep(REQUEST_COOLDOWN - elapsed)
    
    # Build prompt
    prompt = "Generate a creative, inspiring team name for FIRST LEGO League"
    if theme:
        prompt += f" with the theme '{theme}' in mind."
    
    try:
        # Generate with timeout
        with ThreadPoolExecutor() as executor:
            future = executor.submit(
                model.generate_content,
                prompt,
                generation_config=GENERATION_CONFIG
            )
            response = future.result(timeout=timeout)
            
            last_request_time = time.time()
            
            if not response.text:
                raise ValueError("Empty response from API")
                
            return {
                'name': response.text.strip(),
                'generation_method': 'gemini',
                'success': True
            }
            
    except TimeoutError:
        return {
            'error': 'Request timed out',
            'success': False
        }
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }
```

## Best Practices

1. **API Key Security**:
   - Never commit API keys to version control
   - Use environment variables or secure secret management
   - Rotate keys regularly

2. **Error Handling**:
   - Always implement timeouts
   - Have fallback mechanisms
   - Log errors for debugging

3. **Rate Limiting**:
   - Implement cooldown between requests
   - Handle rate limit errors gracefully
   - Consider implementing exponential backoff for retries

4. **Content Safety**:
   - Always use appropriate safety settings
   - Review and adjust thresholds based on your use case
   - Implement additional content filtering if needed

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify API key is correct
   - Check if the API key has the necessary permissions
   - Ensure the `google-generativeai` package is up to date

2. **Timeout Errors**:
   - Increase the timeout value
   - Check network connectivity
   - Implement retry logic

3. **Content Filtering**:
   - Review safety settings
   - Check the response for `safety_ratings`
   - Adjust prompt if needed

## Resources

- [Official Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Python Client Library](https://github.com/google-gemini/generative-ai-python)
- [Safety Settings Guide](https://ai.google.dev/gemini-api/docs/safety-settings)

---
*Last Updated: June 2024*
