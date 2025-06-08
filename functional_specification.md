# Functional Specification: FLL Team Name Generator and Voting App

## Overview

This application is a minimal, responsive web app built using Flask, JavaScript, HTML, CSS, and Gemini API. It allows users to generate AI-powered team names and descriptions for a FIRST LEGO League (FLL) Challenge and vote on their favorites.

## 1. Features Summary

### 1.1 Welcome Screen
- Welcome message with app description
- Two main actions:
  - **Start Generating**: Begins AI name generation
  - **Add Custom Name**: Opens a form to add a user-created team name and description
- Custom name form includes:
  - Team name input field (required)
  - Description text area (optional)
  - Submit and Cancel buttons
- Success/error feedback when adding a custom name
- Route: `/`

### 1.2 Name Generation Screen
- Large, AI-generated team name display
- Short, creative description from Gemini API
- Three buttons:
  - **Yes**: saves name + description to a JSON-based favorites list
  - **No**: skips name and generates another
  - **Generate**: generates a new name without saving
- Top-right button: **Vote** → navigates to voting screen
- Route: `/generate`

### 1.3 Voting Screen
- Grid layout showing all saved names and descriptions as tiles
- Users can click to toggle a vote (highlighted state)
- Vote count indicator on each tile (basic tallying)
- Top-right button: **Generate** → navigates back to generation screen
- Route: `/vote`

## 2. Design Requirements

### 2.1 UI/UX Principles
- Mobile-first responsive design
- No external CSS frameworks (e.g., Bootstrap)
- All CSS in separate file
- LEGO-inspired subtle color accents (red, yellow, blue)
- Large font for team names, modern typefaces for readability
- Clear button labels and animations/transitions for feedback

### 2.2 Visual Hierarchy
- Team name: primary visual focus
- Description: secondary
- Buttons: aligned below main content (not floating)

## 3. Technical Requirements

### 3.1 Front-End
- HTML5, Vanilla JavaScript, CSS (external stylesheet)
- Jinja templating for server-side rendering
- Buttons trigger asynchronous fetch requests for name generation
- Minimal JS framework use

### 3.2 Back-End
- Flask (Python)
- Routes:
  - `/`: welcome page
  - `/generate`: name generation and selection
  - `/vote`: voting interface
  - `/api/generate_name`: POST → calls Gemini API with prompt
  - `/api/save_name`: POST → saves accepted name to JSON file (both AI and custom names)
  - `/api/vote_toggle`: POST → toggles vote count for name
  - `/api/add_custom_name`: POST → adds user-submitted custom name to JSON file

### 3.3 AI Integration
- Gemini API used for:
  - Team name generation (fun, creative, child-appropriate tone)
  - Short description generation
- Gemini prompts will be refined iteratively

### 3.4 Data Storage
- JSON file (e.g., `names.json`) format:
```json
[
  {
    "name": "Galactic Builders",
    "description": "Innovators exploring beyond the LEGO cosmos!",
    "votes": 2,
    "source": "ai"
  },
  {
    "name": "Custom Team Name",
    "description": "Our amazing team created by students!",
    "votes": 0,
    "source": "user"
  }
]
```
- The `source` field helps track whether the name was AI-generated (`"ai"`) or user-submitted (`"user"`)

## 4. Non-Functional Requirements

### 4.1 Performance
- All actions (generate, vote, save) occur with minimal lag
- API call loading indicator to show status

### 4.2 Usability
- Accessible language and layout for primary school-aged users
- Tested on mobile (iOS, Android), tablet, and desktop

### 4.3 Maintainability
- Modular code structure
- Clear documentation of all routes and files

### 4.4 Security
- No user authentication needed
- Sanitize input/output to prevent injection
- Configuration (including Gemini API key) stored in `config.py`
  - Note: For production use, consider moving sensitive data to environment variables
