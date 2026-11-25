---
description: Use this rule whenever someone is prompting to update their game or make changes
globs: *.html
alwaysApply: false
---
# Game Development Standards

## File Structure
- All games should be contained within a single `index.html` file
- Use HTML5 Canvas for rendering
- Include all CSS and JavaScript within the same file
- Organize the file in the following sections:
  1. HTML structure
  2. CSS styles
  3. JavaScript game code

## HTML Structure Requirements
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Game Name]</title>
    <style>
      /* Game styles here */
    </style>
  </head>
  <body>
    <!-- Canvas and UI elements -->
    <script>
      /* Game code here */
    </script>
  </body>
</html>
```

## Core Game Components

### 1. Canvas Setup
```javascript
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas dimensions
canvas.width = 800;  // Standard width
canvas.height = 600; // Standard height
```

### 2. Game Loop Structure
```javascript
let lastTime = 0;
let gameState = 'start'; // start, playing, paused, gameover

function update(deltaTime) {
    if (gameState !== 'playing') return;
    // Update game logic here
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw game elements here
}

function gameLoop(timestamp) {
    const deltaTime = (timestamp - lastTime) / 16.67; // Normalize to 60 FPS
    lastTime = timestamp;

    update(deltaTime);
    draw();

    requestAnimationFrame(gameLoop);
}
```

### 3. Input Handling
- Use event listeners for keyboard input
- Include touch controls for mobile support
- Implement standard control schemes:
  - Arrow keys/WASD for movement
  - Space for primary action
  - P for pause
  - ESC for menu

### 4. Game States
- Implement consistent game states:
  - `start`: Title screen
  - `playing`: Active gameplay
  - `paused`: Pause menu
  - `gameover`: Game over screen

### 5. Mobile Support
- Include responsive design for mobile devices
- Implement touch controls when needed
- Use media queries to handle different screen sizes

## Best Practices
1. Use classes for game objects
2. Implement collision detection methods
3. Use requestAnimationFrame for the game loop
4. Normalize game speed using deltaTime
5. Include score tracking
6. Add sound support when needed
7. Implement proper game state management
8. Use consistent variable naming conventions
9. Add comments for complex logic
10. Include basic UI elements (score, lives, etc.)

## Performance Considerations
1. Limit canvas size to 800x600 for consistency
2. Optimize sprite rendering
3. Clean up unused objects
4. Implement object pooling for frequently created/destroyed objects
5. Use appropriate data structures for game objects

## Testing Requirements
1. Test on multiple browsers
2. Verify mobile compatibility
3. Check touch controls
4. Ensure consistent frame rate
5. Verify game state transitions

## Farcade SDK
1. Add these SDK calls to the game:

// When the game is fully loaded and ready to play:
window.FarcadeSDK.singlePlayer.actions.ready();

// When the game is over (replace scoreValue with the actual score):
window.FarcadeSDK.singlePlayer.actions.gameOver({ score: scoreValue });

// For haptic feedback on important interactions (like jumping or hitting obstacles):
window.FarcadeSDK.singlePlayer.actions.hapticFeedback();

// Add this to handle play again requests:
window.FarcadeSDK.on('play_again', () => {
  // Reset the game state here
  // For example: resetGame(), startNewGame(), etc.
});

// Add this to handle mute/unmute:
window.FarcadeSDK.on('toggle_mute', (data) => {
  // Set game audio based on data.isMuted
  // For example: setMuted(data.isMuted)
});

2. Make sure to call the ready event when the game is fully loaded and playable.
3. Call gameOver when the player loses or completes the game.
4. Add haptic feedback for important game events.
