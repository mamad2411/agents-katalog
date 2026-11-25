---
description: 
globs: 
alwaysApply: true
---
# Web Vibes Chrome Extension - Copilot Instructions

## Project Overview

Web Vibes is a Chrome extension that allows users to create and apply custom CSS/JavaScript "vibes" (hacks) to websites. The extension features a modern popup interface with gradient themes and a comprehensive settings system.

## Architecture Patterns

### 1. Three-Layer Architecture (Model → Repository → Service)

**ALL data management MUST follow this pattern:**

```
lib/[domain]/
├── model/
│   └── [domain].js          # Data model class
├── repo/
│   └── [domain]-repo.js     # Repository for storage operations
└── service/
    └── [domain]-service.js  # Business logic service
```

#### Model Layer Responsibilities:

- Data structure definition
- Validation methods (`isValid()`)
- Serialization (`toJSON()`, `fromJSON()`)
- Default values (`getDefaults()`)
- Static utility methods

#### Repository Layer Responsibilities:

- Chrome storage API interactions
- Storage key management
- Error handling for storage operations
- Storage usage/quota information

#### Service Layer Responsibilities:

- Business logic operations
- Data transformations
- Combining model and repository operations
- Takes repository as constructor dependency

### 2. Example Implementation Pattern

```javascript
// Model
class Settings {
  static getDefaults() {
    /* ... */
  }
  static fromJSON(data) {
    /* ... */
  }
  toJSON() {
    /* ... */
  }
  static isValid(data) {
    /* ... */
  }
}

// Repository
class SettingsRepository {
  constructor() {
    this.storageKey = "webVibesSettings";
  }
  async getSettings() {
    /* uses chrome.storage */
  }
  async saveSettings(settings) {
    /* uses chrome.storage */
  }
}

// Service
class SettingsService {
  constructor(settingsRepository) {
    this.repository = settingsRepository;
  }
  async getAllSettings() {
    return this.repository.getSettings();
  }
  async setTheme(themeKey) {
    /* business logic */
  }
}

// Usage in apps
class App {
  constructor() {
    this.repository = new SettingsRepository();
    this.service = new SettingsService(this.repository);
  }
}
```

## CSS Organization

### 1. CSS Import Hierarchy

**ALL HTML pages MUST follow this import pattern:**

```html
<head>
  <!-- Always import main.css first -->
  <link rel="stylesheet" href="main.css" />
  <!-- For root pages -->
  <link rel="stylesheet" href="../main.css" />
  <!-- For subdirectory pages -->
  <!-- Then page-specific styles -->
  <link rel="stylesheet" href="page-specific.css" />
</head>
```

### 2. main.css Structure

```css
/* External dependencies (Material Icons, fonts) */
@import url("...");

/* Base styles and CSS variables */
@import url("popup.css");

/* Global utilities and Material Icons setup */
.material-icons {
  /* proper rendering setup */
}
```

### 3. Theme System

**Dynamic theming MUST use CSS custom properties:**

```css
/* In main.css */
:root {
  --theme-gradient: linear-gradient(...); /* default */
}

.theme-cosmic-purple {
  --theme-gradient: linear-gradient(...);
}
.theme-sunset-glow {
  --theme-gradient: linear-gradient(...);
}
/* etc for all themes */

/* In component styles */
.header {
  background: var(--theme-gradient);
}
```

## File Organization

### 1. Directory Structure

```
popup/
├── main.css              # Central CSS imports
├── popup.css             # Core styles and variables
├── popup.html            # Main popup page
├── popup.js              # Main popup logic
├── CSS_README.md         # CSS documentation
└── settings/
    ├── settings.css      # Settings-specific styles
    ├── settings.html     # Settings page
    └── settings.js       # Settings page logic

lib/
├── index.js              # Library entry point
├── hack/                 # Hack domain
│   ├── model/hack.js
│   ├── repo/hack-repo.js
│   └── service/hack-service.js
└── settings/             # Settings domain
    ├── model/settings.js
    ├── repo/settings-repo.js
    ├── service/settings-service.js
    └── README.md
```

### 2. HTML Script Loading Order

**ALWAYS load in dependency order:**

```html
<!-- Model classes first -->
<script src="../lib/[domain]/model/[domain].js"></script>
<!-- Repository classes second -->
<script src="../lib/[domain]/repo/[domain]-repo.js"></script>
<!-- Service classes third -->
<script src="../lib/[domain]/service/[domain]-service.js"></script>
<!-- Application logic last -->
<script src="app.js"></script>
```

## UI/UX Standards

### 1. Material Icons Usage

**ALWAYS use Material Icons for interactive elements:**

```html
<!-- Settings button -->
<span class="material-icons">settings</span>
<!-- Back button -->
<span class="material-icons">arrow_back</span>
<!-- Checkmarks -->
<span class="material-icons">check</span>
```

### 2. Theme Implementation

**Gradient themes MUST include:**

- Name (display name)
- Gradient (CSS linear-gradient)
- Description (user-friendly description)
- Validation in Settings.isValidTheme()

```javascript
// In Settings model
static getAvailableThemes() {
  return {
    'theme-key': {
      name: 'Display Name',
      gradient: 'linear-gradient(135deg, #color1, #color2)',
      description: 'User-friendly description'
    }
  };
}
```

### 3. Settings UI Pattern

**Settings pages MUST include:**

- Back navigation with Material Icons
- Section-based organization
- Theme selector with preview tiles
- Reset to defaults functionality
- Consistent styling with main popup

## Code Quality Standards

### 1. Class Structure

**ALL classes MUST include:**

- Comprehensive JSDoc comments
- Constructor parameter validation
- Error handling with try/catch
- Consistent method naming
- Static utility methods where appropriate

### 2. Async/Await Usage

**ALWAYS use async/await, never Promises directly:**

```javascript
// Good
async getAllSettings() {
  return await this.repository.getSettings();
}

// Bad
getAllSettings() {
  return this.repository.getSettings().then(settings => settings);
}
```

### 3. Error Handling

**ALL storage operations MUST include error handling:**

```javascript
async saveSettings(settings) {
  try {
    await chrome.storage.local.set({ [this.storageKey]: settings.toJSON() });
    return settings;
  } catch (error) {
    console.error("Error saving settings:", error);
    throw error;
  }
}
```

## Browser Extension Specifics

### 1. Chrome Storage Keys

**Use consistent naming convention:**

- Settings: `"webVibesSettings"`
- Hacks: `"webVibesHacks"`
- Future domains: `"webVibес[Domain]"`

### 2. Manifest Permissions

**Extension MUST have these permissions:**

- `storage` - For Chrome storage API
- `activeTab` - For current site detection
- `scripting` - For injecting user styles/scripts

### 3. Content Security Policy

**Follow Chrome extension CSP requirements:**

- No inline scripts
- External resources via HTTPS
- Proper script loading order

## Development Workflow

### 1. Adding New Features

1. **Create Model class** with proper validation
2. **Create Repository class** for storage operations
3. **Create Service class** for business logic
4. **Update HTML** with proper script loading
5. **Add UI components** following Material Design
6. **Update CSS** with theme support if needed

### 2. Adding New Themes

1. **Add theme to Settings.getAvailableThemes()**
2. **Add CSS custom property** in main.css
3. **Test gradient** across all UI components
4. **Ensure accessibility** with proper contrast

### 3. Code Review Checklist

- [ ] Follows three-layer architecture
- [ ] Proper error handling
- [ ] JSDoc documentation
- [ ] Consistent naming
- [ ] CSS custom properties for themes
- [ ] Material Icons for UI elements
- [ ] Proper script loading order
- [ ] No hardcoded storage keys

## Future Development Notes

### 1. Extensibility Considerations

- Settings model can easily accommodate new properties
- Theme system supports unlimited gradient options
- Repository pattern allows for different storage backends
- Service layer can be extended for complex business logic

### 2. Performance Guidelines

- Minimize Chrome storage API calls
- Use CSS custom properties for dynamic theming
- Lazy load non-critical components
- Cache theme data in memory when possible

---

**Remember: Consistency is key. When in doubt, follow the patterns established in the hack and settings systems.**
