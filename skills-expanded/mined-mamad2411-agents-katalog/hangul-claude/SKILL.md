# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Hangul Drawing Practice** web application - an educational game that teaches users how to write Korean characters (Hangul) through interactive stroke-by-stroke drawing practice.

## Tech Stack

- **Pure client-side HTML5 application** - No build process or server required
- **Phaser 3** (v3.70.0) - Game framework loaded from CDN
- **Vanilla JavaScript** - No transpilation needed
- **CSS3** with 8-bit retro aesthetic using Press Start 2P font

## Development Commands

Since this is a static site with no build process:

```bash
# Run locally with Python
python -m http.server

# Or with Node.js
npx serve

# Or simply open index.html in a browser
```

## Architecture

The application consists of three main files:

1. **index.html** - UI structure with start screen and game container
2. **game.js** - Core game logic (1048 lines) containing:
   - Character database with stroke definitions for consonants and vowels
   - Phaser game scene setup and rendering
   - Drawing validation logic using distance-based stroke matching
   - Score/level progression system
   - Audio management for background music and sound effects
3. **style.css** - 8-bit retro styling

### Key Game Components

- **Character Data Structure** (game.js:1-300): Each character contains:
  - `char`: The Korean character
  - `romanization`: English representation
  - `strokeCount`: Number of strokes
  - `strokes`: Array of stroke objects with type ('line' or 'circle') and coordinates

- **Drawing Validation** (game.js:597-743): 
  - Uses distance-based matching between user input and reference strokes
  - Validates stroke order and completion
  - Provides visual feedback for correct/incorrect strokes

- **Game States**:
  - Start screen with fullscreen prompt
  - Main game loop with character presentation
  - Drawing validation and scoring
  - Level progression and character cycling

### Audio System

- 5 background music tracks (song0.mp3 - song4.mp3) that cycle automatically
- Success sound effect (success.mp3)
- Mute/unmute functionality
- Music track selection

## Testing

No automated tests exist. Manual testing involves:
1. Opening the game in a browser
2. Drawing characters and verifying stroke validation
3. Testing audio controls and level progression
4. Checking responsive behavior and fullscreen mode

## Common Tasks

When modifying character data:
- Edit the `hangulData` object in game.js:1-300
- Ensure stroke coordinates fit within the 500x500 canvas
- Test stroke validation tolerances if adding complex strokes

When adjusting game difficulty:
- Modify `checkDistance` tolerance in game.js:728
- Adjust score multipliers in `checkDrawing()` function
- Change level progression thresholds in game.js:755