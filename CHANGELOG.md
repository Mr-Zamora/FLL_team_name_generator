# Changelog

All notable changes to the FLL Team Name Generator project will be documented in this file.

## [1.0.0] - 2025-06-09

### Changed
- **Major architectural change:** Completely replaced Gemini API with a local rule-based name generator
- Implemented a modular name_generator.py module with four name generation patterns:
  - prefix + suffix
  - prefix + noun
  - adjective + animal
  - prefix + animal
- Added word_components.json with structured word components and compatibility tags
- Removed all external API dependencies for improved reliability and performance
- Fixed JSON decoding errors in API endpoints with robust request handling
- Fixed UnboundLocalError for RECENT_GENERATED_NAMES with proper global variable declaration

### Removed
- Removed all Gemini API code, imports, and prompt engineering
- Removed config.py with API keys
- Removed prompts.py module
- Removed all Gemini API documentation files
- Removed google-generativeai dependency from requirements.txt

### Security
- Eliminated dependency on external API keys

## [0.3.2] - 2025-06-08

### Added
- Name tracking system to prevent duplicate team names across generations
- Expanded creative theme suggestions list with 10 additional themes
- Memory of up to 100 recently generated names to ensure diversity

### Changed
- Switched from `gemini-1.5-pro` to faster `gemini-2.0-flash-lite` model for improved generation speed
- Enhanced fallback name generation with 20 highly creative animal-themed team names
- Improved prompt engineering to explicitly avoid previously used names
- Optimized batch generation process for better performance

## [0.3.1] - 2025-06-08

### Added
- Team name tips section on welcome page with 6 informative cards and icons
- Automatic backup functionality for reset operations
- Backup information display on reset page

### Changed
- Improved text readability in tip cards with better contrast
- Enhanced user experience with interactive card styling

## [0.3.0] - 2025-06-08

### Added
- "Add Custom Name" button and modal on batch and vote pages for consistent functionality
- Hidden admin reset page (accessible via /reset) with options to remove zero-vote names or all names
- Confirmation dialogs for destructive actions on the reset page
- Improved navigation button spacing for better visual hierarchy
- New `prompts.py` module to separate prompt engineering from application logic

### Changed
- Refactored code to use modular prompt engineering approach
- Enhanced UI consistency with standardized button spacing
- Improved font consistency across the application
- Updated API endpoints to support admin reset functionality

## [0.2.0] - 2025-06-08

### Added
- Batch generation feature to create 20 team names at once
- New batch selection screen with grid layout
- Selection toggle functionality for choosing multiple names
- Finalization screen with confirmation and preview of selected names
- Smooth transitions and animations between screens
- Enhanced API handling for multiple name generation
- Batch tracking in data model

### Changed
- Updated welcome screen to focus on batch generation
- Modified data structure to support batch identification
- Improved UI/UX with visual feedback for selection
- Enhanced error handling for batch API requests
- Updated navigation flow between screens

## [0.1.0] - 2025-06-07

### Initial Implementation

#### Project Setup
- Created basic project structure with directories for templates, static assets, and data
- Added `requirements.txt` with necessary dependencies:
  - Flask 2.3.3
  - google-generativeai 0.3.1
  - Werkzeug 2.3.7
  - Jinja2 3.1.2
  - MarkupSafe 2.1.3
  - itsdangerous 2.1.2
- Created comprehensive `README.md` with project overview, setup instructions, and usage guide

#### Documentation Updates
- Updated `product_requirements_document.md` to specify the use of `config.py` for configuration
- Updated `functional_specification.md` to document security approach using `config.py`
- Updated `gemini_prompt_engineering.md` to include configuration details

#### Backend Implementation
- Created main Flask application (`app.py`) with the following features:
  - Core routes for welcome, generation, and voting screens
  - API endpoints for name generation, saving, voting, and custom name addition
  - Integration with Gemini API for AI-powered name generation
  - JSON-based data persistence with automatic file creation
  - Error handling and fallback mechanisms for API failures
  - Helper functions for data management

#### Frontend Implementation
- Created HTML templates:
  - `base.html`: Base template with common structure and navigation
  - `index.html`: Welcome screen with options to generate names or add custom names
  - `generate.html`: Name generation interface with save/skip functionality
  - `vote.html`: Voting interface with grid layout of saved names
- Implemented CSS styling (`style.css`):
  - LEGO-inspired color scheme (red, yellow, blue)
  - Responsive design for mobile, tablet, and desktop
  - Custom components including cards, buttons, modals, and loading indicators
  - Consistent typography and spacing
- Added JavaScript functionality (`main.js`):
  - Global notification system
  - Input sanitization helpers
  - Console logging for debugging

#### Features Implemented
- **Welcome Screen**:
  - Introduction to the application
  - Navigation to name generation
  - Modal form for adding custom team names
- **Name Generation**:
  - AI-powered team name generation using Gemini API
  - Team description generation
  - Options to save, skip, or generate new names
  - Loading indicators during API calls
- **Voting System**:
  - Display of all saved team names
  - Vote toggling functionality
  - Sorting by vote count
  - Source badges to distinguish AI vs. custom names
- **Data Management**:
  - JSON-based storage in `data/names.json`
  - Unique IDs for each team name
  - Timestamps for creation tracking
  - Vote counting mechanism

#### Security Considerations
- Input sanitization to prevent XSS attacks
- Gemini API key stored in `config.py` (as specified)
- No user authentication required (as per requirements)

#### UI/UX Design
- Child-friendly interface with clear, readable text
- Consistent visual language across all screens
- Feedback mechanisms for user actions
- Loading states for asynchronous operations
- Responsive design for all device sizes

### Known Issues
- None reported yet

### Future Enhancements (Planned for Next Versions)
- Voting leaderboard view
- Export voted names to PDF
- Custom prompt entry for name themes
- Ability to edit/remove custom names
- Store multiple user sessions using localStorage
- Add sound or animation for selected names
