---
name: syncfusion-javascript-context-menu
description: A comprehensive guide for implementing Syncfusion TypeScript ContextMenu component. Use this skill when building context menus that appear on right-click or touch-hold, including features like nested menus, dynamic items, animations, events, styling, and data binding. This skill covers everything from basic setup to advanced features like scrolling, accessibility, and custom templates.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing ContextMenu

The **ContextMenu** is a graphical user interface component that appears on user right-click/touch-hold action. It provides support for nested menu items, custom templates, dynamic content, animations, and comprehensive event handling—making it ideal for building contextual actions in web applications.

## Key Features

- **Nested/Multilevel Menus** - Create hierarchical menu structures
- **Dynamic Item Management** - Add, remove, enable, or disable items at runtime
- **Rich Styling & Templates** - Custom CSS, icons, and HTML templates
- **Event Handling** - Complete lifecycle events (beforeOpen, onOpen, onClose, select, etc.)
- **Animations** - Configurable opening/closing animations with multiple effects
- **Data Binding** - Populate menus from data sources
- **Scrolling** - Automatic scrolling for large menus with HScroll/VScroll
- **Accessibility** - WCAG compliance, keyboard navigation, ARIA support
- **RTL Support** - Right-to-left layout for international applications

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Install dependencies and configure development environment
- Add ContextMenu to your project
- Basic component initialization with HTML and TypeScript
- First working example with separators
- Running and testing your application

### Menu Structure & Templates
📄 **Read:** [references/menu-structure.md](references/menu-structure.md)
- Create template-based menu structures
- Build multilevel and nested menus
- Define separators and item grouping
- Configure FieldSettings for data mapping
- Custom item structure patterns

### Menu Items Management
📄 **Read:** [references/menu-items.md](references/menu-items.md)
- Dynamically add or remove menu items
- Enable and disable items programmatically
- Use insertBefore() and insertAfter() methods
- Manage item state and visibility
- Batch item operations

### Interactions & Events
📄 **Read:** [references/interactions.md](references/interactions.md)
- Open and close ContextMenu programmatically
- Handle lifecycle events (beforeOpen, onOpen, onClose, beforeClose)
- Respond to item selection (select event)
- Integrate dialogs triggered by menu clicks
- Configure animation effects and timing
- Manage menu positioning and hover delays

### Styling & Appearance
📄 **Read:** [references/styling.md](references/styling.md)
- Apply CSS styling and custom themes
- Add icons to menu items with iconCss
- Implement URL navigation with href
- Enable right-to-left (RTL) layout
- Apply custom CSS classes
- Format text with underline characters

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Populate menus from data sources
- Bind to JSON arrays and collections
- Update menu items dynamically from server
- Map data fields using FieldSettings
- Real-time menu content updates

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Implement scrollable menus with HScroll/VScroll
- Configure MenuOpenType (Auto, Hover, Click)
- Apply element filters for selective menu triggering
- Enable/disable HTML sanitization for security
- Configure persistence and locale settings
- Accessibility features and ARIA attributes

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property documentation (~40 core properties)
- MenuItem structure and configuration
- Available methods (open, close, enableItems, removeItems, hideItems, etc.)
- Event interfaces and event data structures
- Animation effects and menu open types
- Type definitions and enums

## Quick Start Example

**HTML:**
```html
<div>
  <div id="contextmenutarget" style="border: 1px solid #ccc; padding: 20px; width: 300px; height: 200px;">
    Right-click here to open the context menu
  </div>
  <ul id="contextmenu"></ul>
</div>
```

**TypeScript:**
```typescript
import { ContextMenu } from '@syncfusion/ej2-navigations';

// Define menu items
const menuItems = [
  { text: 'Cut' },
  { text: 'Copy' },
  { text: 'Paste' },
  { separator: true },
  { text: 'Link' },
  { text: 'Share' }
];

// Initialize ContextMenu
const contextMenu = new ContextMenu({
  items: menuItems,
  target: '#contextmenutarget'
});

contextMenu.appendTo('#contextmenu');
```

## Common Patterns

### Pattern 1: Nested Menu Structure
```typescript
const menuItems = [
  { 
    text: 'Edit',
    items: [
      { text: 'Cut' },
      { text: 'Copy' },
      { text: 'Paste' }
    ]
  },
  { 
    text: 'View',
    items: [
      { text: 'Zoom In' },
      { text: 'Zoom Out' }
    ]
  }
];

const contextMenu = new ContextMenu({
  items: menuItems,
  target: '#target'
});
```

### Pattern 2: Handling Menu Item Selection
```typescript
const contextMenu = new ContextMenu({
  items: menuItems,
  target: '#target',
  select: (args) => {
    console.log('Selected: ' + args.item.text);
    // Perform action based on selected item
  }
});
```

### Pattern 3: Dynamic Item Addition
```typescript
// Add new items after initialization
const newItems = [{ text: 'New Option' }];
contextMenu.insertAfter(newItems, 'Edit');
```

### Pattern 4: Animation Configuration
```typescript
const contextMenu = new ContextMenu({
  items: menuItems,
  target: '#target',
  animationSettings: {
    duration: 400,
    easing: 'ease',
    effect: 'SlideDown'  // SlideDown, ZoomIn, FadeIn, etc.
  }
});
```

### Pattern 5: Icons and Navigation
```typescript
const menuItems = [
  { 
    text: 'Edit',
    iconCss: 'e-icons e-edit'
  },
  { 
    text: 'Delete',
    iconCss: 'e-icons e-delete'
  },
  { 
    text: 'External Link',
    url: 'url'
  }
];
```

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `items` | MenuItemModel[] | Menu items configuration |
| `target` | string | CSS selector for triggering element |
| `animationSettings` | MenuAnimationSettingsModel | Animation behavior |
| `cssClass` | string | Custom CSS classes |
| `enableScrolling` | boolean | Enable scrollbar for long menus |
| `enableRtl` | boolean | Right-to-left layout support |
| `showItemOnClick` | boolean | Submenu opens on click (vs hover) |
| `hoverDelay` | number | Delay before submenu appears (ms) |
| `filter` | string | CSS selector to filter target elements |
| `itemTemplate` | string/Function | Custom template for menu items |

## Common Use Cases

1. **File Operations** - Cut, Copy, Paste, Delete on files/folders
2. **Editor Menus** - Formatting options in text editors
3. **Grid Row Actions** - Actions on table/grid rows
4. **Application Menus** - General app context menus
5. **Nested Actions** - Multi-level operations (Edit → Format)
6. **Dynamic Content** - Load menu items from server
7. **Custom Styling** - Themed context menus matching app design
8. **Accessibility** - Keyboard navigation and screen reader support
