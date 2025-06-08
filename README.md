# FLL Team Name Generator

A lightweight, AI-powered web app that generates and displays FLL team names and allows users to save and vote on them. Designed to be minimal, child-friendly, and intuitive for the 2025-2026 UNEARTHED season.

## Features

- Generate creative team names using Google's Gemini API
- Add custom team names
- Vote on favorite names
- Simple, responsive interface suitable for classroom use
- No login required

## Project Structure

```
FLL_team_name_generator/
├── app.py                  # Main Flask application
├── config.py               # Configuration with API keys
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── main.js         # Frontend interactivity
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Welcome screen
│   ├── generate.html       # Name generation screen
│   └── vote.html           # Voting screen
└── data/                   # Data storage
    └── names.json          # JSON data store (created automatically)
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Gemini API key (already configured in config.py)

### Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python app.py
```

3. Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

## Usage

1. **Welcome Screen**: Choose to generate AI names or add your own custom team name
2. **Generate Screen**: View AI-generated team names and descriptions
   - Click "Yes! Save This" to add a name to your collection
   - Click "No, Skip" to reject the current name
   - Click "Generate New" to get a new suggestion
3. **Vote Screen**: View all saved names and vote for your favorites

## Configuration

All configuration is managed through `config.py`, which contains the Gemini API key.

## Notes

- This application is designed for educational purposes
- No user authentication is required
- Data is stored locally in a JSON file

## Credits

Created for Richard Johnson Anglican College's FIRST LEGO League teams participating in the 2025-2026 UNEARTHED season.
