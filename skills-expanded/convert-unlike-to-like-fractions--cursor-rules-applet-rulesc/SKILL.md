---
description: EdTech Interactive Math Applets - Mandatory Company Requirements
globs:
  - "**/*.jsx"
  - "**/*.js" 
  - "**/*.css"
  - "**/*.html"
  - "**/data.js"
  - "**/index.html"
alwaysApply: true
---

# Interactive Math Applets - EdTech Company Rules

You are an expert React developer building interactive educational math applets for an EdTech company. These applets must follow strict mandatory requirements with NO modifications allowed.

## PROJECT STRUCTURE REQUIREMENTS

### Entry Point & File Structure
- **MANDATORY**: Main entry file MUST be named `index.html`
- **MANDATORY**: Translation file MUST be named `data.js` 
- **MANDATORY**: Must export using `const appData = { ... }` (NOT export default)
- **MANDATORY**: All assets MUST be in `assets/` folder
- **MANDATORY**: Asset names MUST be lowercase or camelCase only

### Folder Structure
```
project-root/
├── index.html              ✅ MANDATORY
├── data.js                 ✅ MANDATORY  
├── assets/                 ✅ MANDATORY
│   ├── images/
│   ├── audio/
│   └── fonts/
├── components/
├── hooks/
└── utils/
```

### Offline Requirements
- **FORBIDDEN**: No CDN calls, script imports, or external NPM builds
- **FORBIDDEN**: No online dependencies
- **MANDATORY**: Must work fully offline
- Bundle all libraries (React, etc.) inline in index.html

## REACT COMPONENT ARCHITECTURE

### Framework Requirements
- **MANDATORY**: React framework for DOM management, hooks, context, and state
- **MANDATORY**: Must work in React Native (TV app variant)
- **MANDATORY**: Support touch, mouse, stylus inputs

### Interactive Elements Requirements
- **MANDATORY**: Audio feedback for ALL interactions requiring student attention
- **MANDATORY**: Action buttons MUST include tap/hand animation and pulsating/glow effects
- **MANDATORY**: Text in interactive elements MUST have `pointer-events: none` and shadows

### Component Naming Conventions
- Components: `ComponentName.jsx` (PascalCase)
- Hooks: `useHookName.js` (camelCase starting with 'use')
- Utilities: `helperFunctions.js` (camelCase)

### Component Structure Template
```jsx
const ComponentName = ({ 
  onTouch, 
  onMouse, 
  onStylus,
  audioFeedback = true,
  children 
}) => {
  const handleInteraction = (event) => {
    if (audioFeedback) {
      playInteractionSound();
    }
    // Handle touch, mouse, stylus
  };

  return (
    <div 
      className="component-container"
      onClick={handleInteraction}
      onTouchStart={handleInteraction}
    >
      <span 
        style={{ 
          pointerEvents: 'none',
          textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
        }}
      >
        {children}
      </span>
    </div>
  );
};
```

## TRANSLATION & CONTENT STRUCTURE

### Data.js Structure
```javascript
const appData = {
  en: {
    "standard-ui": {
      buttons: { next: "Next", prev: "Previous", check: "Check" },
      labels: { score: "Score", timer: "Time" },
      instructions: { click_next: "Click Next" }
    },
    "content-ui": {
      dialogs: { intro: "Welcome! Let's learn subtraction." },
      feedback: { positive: "Awesome work!", negative: "Keep trying!" },
      questions: { q_place_value_01: "What is the value of 5 in 52?" }
    }
  }
  // Other locales follow same structure
};

export default appData; // Use this exact export
```

### Key Naming Rules
- **MANDATORY**: Use snake_case for ALL keys (not camelCase)
- **MANDATORY**: Keys must be stable - never rename after publishing
- **MANDATORY**: Use ICU placeholders: `{name}`, `{count, plural, one {# item} other {# items}}`
- **MANDATORY**: Separate standard-ui (reusable) from content-ui (applet-specific)

## DESIGN SYSTEM REQUIREMENTS

### Typography
- **MANDATORY**: Font family MUST be `Arial, sans-serif`

### Color Palette (Use EXACT hex values)
```css
/* Correctness Colors */
--color-correct-base: #219150;
--color-correct-light: #58D98B;
--color-correct-dark: #0d803d;

/* Wrongness Colors */
--color-wrong-base: #FF6F61;
--color-wrong-light: #FF8F83;
--color-wrong-dark: #D4574C;

/* Buttons/Sliders - Gold */
--color-gold-base: #F1C40F;
--color-gold-light: #F5D54D;
--color-gold-dark: #BFA70B;

/* Objects & Highlights */
--color-orange-base: #FF7F3F;
--color-blue-base: #3498DB;
--color-pink-base: #FF4D6D;
--color-purple-base: #9B59B6;
--color-aqua-base: #1ABC9C;
--color-rose-base: #E84393;
--color-yellow-base: #FF9F1A;
--color-sand-base: #D2B48C;
--color-white-base: #FFFFFF;
```

### Responsive Design
- **MANDATORY**: Must work seamlessly across 16:9 form factors
- **MANDATORY**: Test at exact resolutions: 960×540, 1920×1080, 3840×2160
- **MANDATORY**: No overflows - no horizontal or vertical scrollbars
```css
html, body {
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}
```

### Animation Requirements
```css
/* MANDATORY: Action buttons */
.action-button {
  transition: transform 0.2s ease;
  animation: pulse 2s infinite;
  box-shadow: 0 0 10px rgba(241, 196, 15, 0.5);
}

.action-button:active {
  transform: scale(0.95);
}

@keyframes pulse {
  0% { box-shadow: 0 0 10px rgba(241, 196, 15, 0.5); }
  50% { box-shadow: 0 0 20px rgba(241, 196, 15, 0.8); }
  100% { box-shadow: 0 0 10px rgba(241, 196, 15, 0.5); }
}

/* MANDATORY: Smooth transitions between scenes */
.scene-transition {
  transition: all 0.3s ease-in-out;
}
```

### Text in Interactive Elements
```css
.interactive-text {
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  pointer-events: none; /* MANDATORY */
}
```

## ASSET MANAGEMENT

### Asset Organization
```
assets/
├── images/
│   ├── icons/
│   ├── backgrounds/
│   └── ui-elements/
├── audio/
│   ├── feedback/
│   └── interactions/
└── fonts/
```

### Asset Naming
- **MANDATORY**: lowercase or camelCase only
- ✅ CORRECT: `button-primary.png`, `buttonPrimary.png`, `audio-correct.mp3`
- ❌ WRONG: `Button_Primary.PNG`, `AUDIO-CORRECT.MP3`

## CODING GUIDELINES

### General Principles
- Build for exact storyboard replication - NO modifications allowed
- Always implement audio feedback for student interactions
- Use clamp() for responsive scaling: `clamp(min, preferred, max)`
- Test across all three mandatory resolutions
- Ensure offline functionality

### Common Patterns
- Use CSS custom properties for the mandatory color palette
- Implement proper focus management for accessibility
- Handle all input types (touch, mouse, stylus) in event handlers
- Apply smooth transitions between all app states/scenes

### Error Prevention
- Never use external CDNs or online resources
- Always disable pointer events on text inside interactive elements
- Ensure action buttons have both tap animations and glow effects
- Use exact color hex values from the mandatory palette
- Follow snake_case for all translation keys

Remember: These are strict requirements from the EdTech company. Do NOT suggest modifications or alternatives - implement exactly as specified.