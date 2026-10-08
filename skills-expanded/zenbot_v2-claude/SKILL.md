# ZenBot Project Guide

## Project Overview
ZenBot is an AI-powered meditation guide web application that generates personalized guided meditations using OpenAI's GPT-4 and text-to-speech capabilities. It runs entirely in the browser for privacy.

## Project Structure
```
zenbot_v2/
├── index.html          # Main application page
├── debug.html          # Debug/testing page
├── sw.js              # Service worker for offline capability
├── test.sh            # Test script
├── prompt_template.txt # Template for meditation prompts
├── assets/
│   └── meditation-bell.mp3  # Sound effects
├── css/
│   └── styles.css     # Application styles
└── js/
    ├── api.js         # OpenAI API integration
    ├── audio.js       # Audio playback and controls
    └── main.js        # Main application logic
```

## Key Technologies
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **APIs**: OpenAI GPT-4 (text generation), OpenAI TTS (text-to-speech)
- **Audio**: Web Audio API for precise playback control
- **Offline**: Service Workers for offline capability
- **Deployment**: GitHub Pages static hosting

## Development Guidelines

### Version Management
- **IMPORTANT**: Always update the VERSION constant in `js/main.js` when making changes
- Version format: Major.Minor (e.g., '2.2')
- Update version for any feature additions, bug fixes, or significant changes
- Version is displayed in the UI for debugging purposes

### Testing
- Run tests using: `./test.sh`
- No package.json - this is a pure vanilla JS project
- Test in both desktop and mobile browsers

### Code Style
- Vanilla JavaScript (no frameworks)
- ES6+ features supported
- Modular structure with separate files for API, audio, and main logic

### Key Features to Maintain
1. Privacy-first: API keys never stored server-side
2. Browser-based: All processing happens client-side
3. Mobile-friendly: Must work on mobile browsers
4. Offline capability: Service worker implementation
5. Audio controls: Full playback control (play, pause, resume, stop, skip forward/back)
6. Progress tracking: Visual progress bar for meditation playback
7. Enhanced iOS compatibility: Special handling for iOS audio restrictions

## Important Files

### Main Application Logic
- `js/main.js`: Core application logic and UI interactions
- `js/api.js`: OpenAI API integration for GPT-4 and TTS
- `js/audio.js`: Audio playback management and controls

### User Interface
- `index.html`: Main application interface
- `css/styles.css`: Application styling

### Configuration
- `prompt_template.txt`: Template for generating meditation prompts

## API Integration
- Uses OpenAI's GPT-4 for generating meditation scripts
- Uses OpenAI's Text-to-Speech API for converting scripts to audio
- API key is provided by the user and stored only in session storage (optional)

## Deployment
The application is designed to be deployed as a static site on GitHub Pages at:
`https://[USERNAME].github.io/zenbot`

## Privacy & Security
- No server-side storage of API keys
- All API calls made directly from browser
- Optional session storage for convenience
- No user data collection or tracking

## Common Tasks

### Adding New Features
1. Maintain vanilla JS approach (no frameworks)
2. Keep privacy-first design
3. Ensure mobile compatibility
4. Test offline functionality

### Debugging
- Use `debug.html` for testing individual components
- Check browser console for API errors
- Verify Service Worker registration for offline mode

### Updating Prompts
- Modify `prompt_template.txt` to change meditation generation patterns
- Keep prompts focused on meditation and mindfulness

## Recent Updates (v2.2)
- Added skip forward/backward buttons (30 second intervals)
- Implemented visual progress bar for meditation playback
- Enhanced audio controls with better mobile support
- Improved iOS audio compatibility with special handling
- Updated to GPT-5 model for meditation generation
- Refined meditation prompts for clearer guidance and better pacing

## Notes
- This is a static site with no backend
- All functionality runs in the browser
- Designed for simplicity and privacy
- Currently using GPT-5 model for meditation generation