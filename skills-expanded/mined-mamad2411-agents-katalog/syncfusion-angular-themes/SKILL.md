---
name: syncfusion-angular-themes
description: Use this skill when users need to apply themes, customize appearance, switch dark mode, use CSS variables, configure icons, or modify visual styling for Syncfusion Angular components. Covers icon library, size modes, and Theme Studio integration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Theming and Appearance"
---

# Themes in Syncfusion Angular Components

Syncfusion Angular components provide comprehensive theming support with modern, customizable themes. This skill guides you through applying themes, customizing appearance, implementing dark mode, using CSS variables, managing icons, and creating custom themes for consistent, professional Angular applications.

## Table of Contents

- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Patterns](#common-patterns)

## Documentation and Navigation Guide

### Built-in Themes
📄 **Read:** [references/built-in-themes.md](references/built-in-themes.md)
- Available 10+ themes
- Applying themes via npm packages, CDN, or individual component styles
- Optimized (lite) CSS files for reduced bundle size
- Theme comparison and selection guide
- Legacy theme support

### Dark Mode Implementation
📄 **Read:** [references/dark-mode.md](references/dark-mode.md)
- Global dark mode with `e-dark-mode` class
- Per-component dark mode
- Runtime theme switching with checkboxes or toggle buttons

### CSS Variables Customization
📄 **Read:** [references/css-variables.md](references/css-variables.md)
- CSS variable structure for each theme (Material 3, Fluent 2, Bootstrap 5.3, Tailwind 3.4)
- Customizing primary, success, warning, danger, info colors
- Runtime color modification with TypeScript
- Theme-specific variable formats (RGB vs hex values)
- Material 3 color system (primary, secondary, tertiary, surface)

### Icon Library
📄 **Read:** [references/icons.md](references/icons.md)
- Setting up the icon library (npm or CDN)
- Using icons with `e-icons` class
- Icon sizing (small, medium, large)
- Customizing icon color and appearance
- Available icon sets per theme

### Size Modes
📄 **Read:** [references/advanced-theming.md](references/advanced-theming.md)
- Normal vs touch (bigger) size modes
- Enabling size modes globally or per-component
- Runtime size mode switching

### Advanced Features
📄 **Read:** [references/advanced-theming.md](references/advanced-theming.md)
- Component styling integration
- Theme Studio for custom theme creation

## Quick Start

### Install and Apply a Theme

**Step 1: Install Syncfusion Angular Package**

```bash
npm install @syncfusion/ej2-angular-buttons@latest --save
```

**Step 2: Import Theme CSS**

```css
/* src/styles.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

Or use CDN (ensure version matches your npm packages):

```html
<!-- angular.json - Add to styles array -->
"styles": [
  "https://cdn.syncfusion.com/ej2/32.1.19/tailwind3.css"
]
```

## Common Patterns

### Pattern 1: Apply Dark Mode Globally

```typescript
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div>
      <ejs-checkbox 
        label="Enable Dark Mode" 
        [checked]="isDarkMode" 
        (change)="handleDarkModeToggle($event)">
      </ejs-checkbox>
      <ejs-button cssClass="e-primary">Sample Button</ejs-button>
    </div>
  `
})
export class AppComponent {
  isDarkMode = false;

  handleDarkModeToggle(event: any): void {
    this.isDarkMode = event.checked ?? false;
    
    if (this.isDarkMode) {
      document.body.classList.add('e-dark-mode');
    } else {
      document.body.classList.remove('e-dark-mode');
    }
  }
}
```

### Pattern 2: Customize Primary Color with CSS Variables

**For Fluent 2 Theme:**

```css
/* src/styles.css */
:root {
  --color-sf-primary: #ff6b35;  /* Custom orange */
}
```

**For Material 3 Theme (uses RGB values):**

```css
/* src/styles.css */
:root {
  --color-sf-primary: 255, 107, 53;  /* RGB: Custom orange */
}
```

### Pattern 3: Enable Touch Mode Globally

```html
<!-- index.html -->
<body class="e-bigger">
  <app-root></app-root>
</body>
```

Or per-component:

```typescript
<ejs-button cssClass="e-bigger">Touch-Friendly Button</ejs-button>
```

### Pattern 4: Use Optimized CSS for Faster Loading

```css
/* src/styles.css - Lite version without bigger mode styles */
@import "@syncfusion/ej2/tailwind3-lite.css";
```

### Pattern 5: Use Icons from Syncfusion Library

**Install icons package:**

```bash
npm install @syncfusion/ej2-icons/@latest
```

**Import icon styles:**

```css
/* src/styles.css */
@import "../node_modules/@syncfusion/ej2-icons/styles/tailwind3.css";
```

**Use icons in components:**

```html
<span class="e-icons e-cut"></span>
<span class="e-icons e-medium e-copy"></span>
<span class="e-icons e-large e-paste"></span>
```
