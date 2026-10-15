---
name: syncfusion-javascript-common
description: Common utilities and features for Syncfusion JavaScript controls. Use this skill when the user needs to implement animations, drag-and-drop, state persistence, RTL support, localization, globalization, security, templates, and advanced features for Syncfusion JavaScript controls.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Common Features"
---

# Common Features in Syncfusion JavaScript Controls

Syncfusion JavaScript controls include comprehensive common utilities and features that enhance user experience, ensure cross-cultural support, and provide foundational capabilities across all controls. This skill covers installation setup, animations, globalization, state management, and security considerations for building robust JavaScript applications.

## Table of Contents

- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Features](#common-features)

## Documentation and Navigation Guide

### Getting Started & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Webpack Setup - Integrating Syncfusion controls with Webpack bundler
- Electron Setup - Using Syncfusion controls in Electron desktop applications
- Cordova Setup - Integrating controls in Apache Cordova mobile apps
- Ionic Setup - Configuring Syncfusion controls for Ionic framework
- Meteor Setup - Setting up controls in Meteor.js applications
- SharePoint Setup - Deploying Syncfusion controls in SharePoint environments

---

### Globalization

📄 **Read:** [references/globalization.md](references/globalization.md)
- Right-to-left (RTL) support for Arabic, Hebrew, Persian languages
- Localization (l10n) for multi-language support
- Internationalization (i18n) with CLDR data
- Number and currency formatting
- Date and time formatting

---

### Advanced Features

📄 **Read:** [references/advanced-features.md](references/advanced-features.md))
- Animation effects (FadeIn, ZoomOut, SlideUp, etc.)
- Animation timing (duration, delay, global settings)
- Drag-and-drop interactions (Draggable, Droppable)
- Template customization and optimization
- State persistence with enablePersistence
- Security best practices and HTML sanitization
---

## Quick Start

### Install Syncfusion JavaScript Package

```bash
npm install @syncfusion/ej2-grids@latest --save
```

> **Note:** The `@syncfusion/ej2-base` package is a dependency for all Syncfusion controls and will be automatically installed when you install any Syncfusion JavaScript package. You don't need to explicitly add it to your `package.json` file.

### Import Styles

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-grids/styles/tailwind3.css";
```

### Register License Key

**Step 1:** Set the environment variable:

```bash
# Windows
setx SYNCFUSION_LICENSE "Your_License_Key_Here"

# Mac/Linux
export SYNCFUSION_LICENSE='Your_License_Key_Here'
```

**Step 2:** Activate the license using NPX command:

```bash
npx syncfusion-license activate
```

> **Note:** For alternative license registration methods, kindly refer to the [Syncfusion license key registration documentation](https://ej2.syncfusion.com/documentation/licensing/license-key-registration).

### Basic Control Setup

```typescript
import { Grid, Page } from '@syncfusion/ej2-grids';

const data: Object[] = [
  { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
  { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 }
];

const grid: Grid = new Grid({
  dataSource: data,
  allowPaging: true,
  columns: [
    { field: 'OrderID', width: 100 },
    { field: 'CustomerID', width: 100 },
    { field: 'Freight', width: 100, format: 'C2' }
  ]
});

// Inject required services
Grid.Inject(Page);

grid.appendTo('#grid');
```

```html
<div id="grid"></div>
```

## Common Features

### Enable State Persistence

```typescript
import { Grid } from '@syncfusion/ej2-grids';

const grid: Grid = new Grid({
  dataSource: data,
  enablePersistence: true
});

grid.appendTo('#grid');
```

### Enable RTL Support

```typescript
import { enableRtl } from '@syncfusion/ej2-base';
import { ListView } from '@syncfusion/ej2-lists';

// Global RTL enablement
enableRtl(true);

// OR per-control
const listView: ListView = new ListView({
  enableRtl: true
});
listView.appendTo('#listview');
```

### Add Animation Effects

```typescript
import { Animation } from '@syncfusion/ej2-base';

const element: HTMLElement | null = document.getElementById('element');

if (element) {
  const animation: Animation = new Animation({ 
    duration: 5000, 
    delay: 2000 
  });
  animation.animate(element, { name: 'FadeOut' });
}
```

### Implement Drag-and-Drop

```typescript
import { Draggable, Droppable } from '@syncfusion/ej2-base';

const draggableElement: HTMLElement | null = document.getElementById('draggable');
const droppableElement: HTMLElement | null = document.getElementById('droppable');

if (draggableElement && droppableElement) {
  const draggable: Draggable = new Draggable(draggableElement, { 
    clone: false 
  });
  
  const droppable: Droppable = new Droppable(droppableElement, {
    drop: (e: DropEventArgs) => {
      if (e.droppedElement) {
        e.droppedElement.textContent = 'Dropped!';
      }
    }
  });
}
```

```html
<div id="draggable">Drag me</div>
<div id="droppable">Drop here</div>
```