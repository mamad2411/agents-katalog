---
name: syncfusion-react-menu
description: |
  Create and configure the Syncfusion React Menu navigation component for hierarchical menu structures, 
  dropdowns, and context menus. Use this skill whenever the user needs to implement menus, navigation bars, 
  dropdown menus, hamburger menus, mobile menus, sub-menu positioning, menu item interactions, data-binding menus, 
  RTL menu layouts, menu customization with icons/separators, event handling, or advanced features like 
  scrollable menus, persistence, and item state management.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Navigation Components"
---

# Implementing the Syncfusion React Menu Component

The Syncfusion React Menu component is a flexible, feature-rich navigation control for creating hierarchical menu structures with support for icons, separators, animations, accessibility, hamburger mode, scrolling, event handling, and item state management. Use it to build navigation bars, dropdown menus, context menus, mobile-responsive menus, and complex hierarchical navigation systems.

## When to Use This Skill

- **Building navigation menus:** File menus, application menus, main navigation bars
- **Dropdown menus:** User action menus, context-sensitive options
- **Sub-menu systems:** Multi-level hierarchical navigation
- **Hamburger/mobile menus:** Responsive menu for mobile devices
- **Menu customization:** Adding/removing items, icons, separators, custom styling
- **Event handling:** Detecting menu item clicks, open/close events, item state changes
- **Data-driven menus:** Binding menus to JSON data structures (hierarchical or self-referential)
- **Item state management:** Enabling/disabling, showing/hiding, updating menu items
- **Accessibility:** Creating keyboard-navigable, screen reader-friendly menus
- **RTL support:** Right-to-left language menus
- **Scrollable menus:** Large menus with horizontal/vertical scrolling
- **Persistence:** Saving menu state across page reloads

## Component Overview

### Key Capabilities

- **Hierarchical menus** with unlimited nesting levels
- **Data binding** to hierarchical or self-referential JSON data
- **Icon and separator support** for visual organization
- **Event system** for click, open, close, and render interactions
- **Animation effects** with configurable timing and easing
- **Keyboard navigation** and WCAG accessibility compliance
- **RTL support** for right-to-left languages
- **Responsive layout** with horizontal and vertical scrolling
- **Item state management** - dynamically add, remove, enable/disable, show/hide items
- **Hamburger mode** for mobile-responsive menus
- **State persistence** - save and restore menu state across page reloads
- **HTML sanitization** for security
- **Hover delay** control for sub-menu timing
- **Custom CSS classes** for flexible styling

### When to Choose Menu Over Alternatives

| Component | Best For |
|-----------|----------|
| **Menu** | Hierarchical navigation, dropdown menus, file menus, hamburger menus |
| **Navbar** | Linear top navigation |
| **Sidebar** | Fixed side navigation panel |
| **Tabs** | Flat content sections with switching |

## Quick Start

```jsx
import { MenuComponent, MenuItemModel } from '@syncfusion/ej2-react-navigations';
import React from 'react';

function App() {
  const menuItems: MenuItemModel[] = [
    {
      text: 'File',
      items: [
        { text: 'New' },
        { text: 'Open' },
        { text: 'Save' }
      ]
    },
    {
      text: 'Edit',
      items: [
        { text: 'Cut' },
        { text: 'Copy' },
        { text: 'Paste' }
      ]
    }
  ];

  return (
    <MenuComponent items={menuItems}></MenuComponent>
  );
}

export default App;
```

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup with Vite/Create React App
- CSS imports and theme configuration
- Creating basic menu with MenuItemModel
- MenuComponent integration in React
- First render and initialization
- Ripple effects
- **When to read:** Starting a new Menu implementation, setting up project

### Properties and Configuration
📄 **Read:** [references/properties-and-configuration.md](references/properties-and-configuration.md)
- All MenuComponent properties with descriptions
- Default values and accepted types
- Configuration examples for each property
- animationSettings, cssClass, enableHtmlSanitizer, enablePersistence
- enableRtl, enableScrolling, hamburgerMode, hoverDelay
- locale, orientation, showItemOnClick, target, title
- **When to read:** Configuring component behavior, setting animations, enabling features

### Methods and API
📄 **Read:** [references/methods-api.md](references/methods-api.md)
- All MenuComponent methods with detailed documentation
- insertBefore(), insertAfter(), removeItems() - item manipulation
- enableItems(), hideItems(), showItems() - item state management
- getItemIndex(), setItem() - item access and updates
- open(), close() - hamburger mode control
- destroy() - cleanup
- Complete code examples for every method
- **When to read:** Dynamically manipulating menu items, controlling menu state

### Events and Callbacks
📄 **Read:** [references/events-and-callbacks.md](references/events-and-callbacks.md)
- All event types with complete documentation
- Event arguments: MenuEventArgs, BeforeOpenCloseMenuEventArgs, OpenCloseMenuEventArgs
- select, beforeOpen, beforeClose, onOpen, onClose events
- beforeItemRender and created lifecycle events
- Event handling patterns and callback examples
- **When to read:** Responding to user interactions, handling lifecycle events

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Hierarchical data binding
- Self-referential data structures
- JSON data mapping with FieldSettingsModel
- Complex nested data hierarchies
- Dynamic data updates and modifications
- Real-time data from APIs
- **When to read:** Populating menus from data sources

### Menu Item Customization
📄 **Read:** [references/menu-items-customization.md](references/menu-items-customization.md)
- Adding menu items with insertBefore/insertAfter
- Removing items with removeItems
- Enabling/disabling items with enableItems
- Showing/hiding items with showItems/hideItems
- Custom HTML attributes
- Separator support
- **When to read:** Dynamically managing menu structure

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- Icon integration and positioning
- Separator rendering and customization
- Mnemonic UI creation (keyboard shortcuts)
- RTL (Right-to-left) support
- Custom CSS classes and theme integration
- Animation settings and effects
- Dark mode support
- **When to read:** Customizing appearance, theming

### Hamburger and Mobile Mode
📄 **Read:** [references/hamburger-mode.md](references/hamburger-mode.md)
- Hamburger mode setup and configuration
- Mobile responsive implementation
- hamburgerMode, target, title properties
- open() and close() methods
- Integration with Sidebar and Accordion
- Mobile-first design patterns
- **When to read:** Building mobile-responsive menus

### Use Case Scenarios
📄 **Read:** [references/use-case-scenarios.md](references/use-case-scenarios.md)
- Scrollable menu implementation
- Menu in Toolbar integration
- Hamburger menu with Sidebar
- Mobile view with ListView
- Context menu patterns
- Dynamic data-driven menus
- **When to read:** Building specific menu patterns for real-world scenarios

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG compliance standards
- WAI-ARIA attributes
- Keyboard navigation patterns
- Screen reader support
- Focus management
- Color contrast guidelines
- Testing accessibility
- **When to read:** Ensuring menu is accessible to all users

## Quick Start Example

```jsx
import { MenuComponent, MenuItemModel } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

function App() {
  // Define menu structure
  const menuItems: MenuItemModel[] = [
    {
      text: 'File',
      items: [
        { text: 'New' },
        { text: 'Open' },
        { text: 'Save' },
        { separator: true },
        { text: 'Exit' }
      ]
    },
    {
      text: 'Edit',
      items: [
        { text: 'Cut' },
        { text: 'Copy' },
        { text: 'Paste' }
      ]
    },
    {
      text: 'Help'
    }
  ];

  return (
    <MenuComponent items={menuItems}></MenuComponent>
  );
}

export default App;
```

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `items` | MenuItemModel[] | [] | Menu items to render |
| `fields` | FieldSettingsModel | - | Data field mappings |
| `hamburgerMode` | boolean | false | Enable mobile hamburger view |
| `enableScrolling` | boolean | true | Allow scrolling for large menus |
| `enablePersistence` | boolean | false | Save state across sessions |
| `enableRtl` | boolean | false | Right-to-left text support |
| `orientation` | Orientation | Horizontal | Layout direction |
| `animationSettings` | MenuAnimationSettings | - | Animation configuration |
| `hoverDelay` | number | 400 | Sub-menu hover delay (ms) |
| `showItemOnClick` | boolean | false | Show items only on click |
| `enableHtmlSanitizer` | boolean | true | Sanitize HTML content |
| `cssClass` | string | - | Custom CSS classes |
| `locale` | string | 'en-US' | Culture/language setting |
| `target` | string | - | Element selector for hamburger |
| `title` | string | - | Hamburger mode title text |

## Key Methods Reference

| Method | Parameters | Purpose |
|--------|-----------|---------|
| `insertBefore()` | item, selector | Insert before a menu item |
| `insertAfter()` | item, selector | Insert after a menu item |
| `removeItems()` | selectors | Remove items by selector |
| `enableItems()` | selectors, enable | Enable/disable items |
| `showItems()` | selectors | Show hidden items |
| `hideItems()` | selectors | Hide visible items |
| `setItem()` | item, selector | Update item properties |
| `getItemIndex()` | selector | Get item index in menu |
| `open()` | - | Open hamburger menu |
| `close()` | - | Close hamburger menu |
| `destroy()` | - | Cleanup component |

## Key Events Reference

| Event | Trigger | Argument Type |
|-------|---------|---------------|
| `select` | Menu item clicked | MenuEventArgs |
| `beforeOpen` | Before sub-menu opens | BeforeOpenCloseMenuEventArgs |
| `beforeClose` | Before sub-menu closes | BeforeOpenCloseMenuEventArgs |
| `onOpen` | After sub-menu opens | OpenCloseMenuEventArgs |
| `onClose` | After sub-menu closes | OpenCloseMenuEventArgs |
| `beforeItemRender` | Before item renders | BeforeItemRenderEventArgs |
| `created` | Component initialized | Object |

## Common Patterns

### Pattern 1: Responding to Menu Item Selection

```jsx
const handleMenuSelect = (args) => {
  console.log(`Selected: ${args.item.text}`);
  // Handle the selected menu item
};

<MenuComponent 
  items={menuItems} 
  select={handleMenuSelect}
></MenuComponent>
```

### Pattern 2: Dynamically Adding Menu Items

```jsx
let menuObj: MenuComponent;

const addMenuItem = () => {
  menuObj.insertAfter([{ text: 'New Item' }], 'File');
};

<MenuComponent 
  ref={(menu) => (menuObj = menu)} 
  items={menuItems}
></MenuComponent>
```

### Pattern 3: Disabling Menu Items

```jsx
const handleBeforeOpen = (args) => {
  if (args.item.text === 'Save') {
    args.item.disabled = true; // Disable based on condition
  }
};

<MenuComponent 
  items={menuItems} 
  beforeOpen={handleBeforeOpen}
></MenuComponent>
```

## Key Learning Path

1. **Start Here:** [references/getting-started.md](references/getting-started.md) - Setup and basic menu creation
2. **Add Data:** [references/data-binding.md](references/data-binding.md) - Bind menus to data sources
3. **Handle Interaction:** [references/events-and-callbacks.md](references/events-and-callbacks.md) - Respond to user actions
4. **Dynamic Control:** [references/methods-api.md](references/methods-api.md) - Manipulate menus programmatically
5. **Advanced Features:** [references/hamburger-mode.md](references/hamburger-mode.md) - Mobile-responsive patterns
6. **Real-World Patterns:** [references/use-case-scenarios.md](references/use-case-scenarios.md) - Production implementations

## All Reference Files

### Fundamentals
- [getting-started.md](references/getting-started.md) - Installation, setup, MenuItemModel structure
- [properties-and-configuration.md](references/properties-and-configuration.md) - All 24+ component properties

### Data & State
- [data-binding.md](references/data-binding.md) - Hierarchical and self-referential binding
- [menu-items-customization.md](references/menu-items-customization.md) - Dynamic item management

### Interaction & Control
- [events-and-callbacks.md](references/events-and-callbacks.md) - Event system and callbacks
- [methods-api.md](references/methods-api.md) - All methods for programmatic control

### Presentation & UX
- [styling-and-appearance.md](references/styling-and-appearance.md) - Icons, themes, animations
- [orientation-and-layout.md](references/orientation-and-layout.md) - Horizontal/vertical layouts
- [hamburger-mode.md](references/hamburger-mode.md) - Mobile hamburger menus
- [accessibility.md](references/accessibility.md) - WCAG compliance and keyboard navigation

### Legacy (Original Files)
- [events-and-interactions.md](references/events-and-interactions.md) - Basic event handling (see events-and-callbacks.md for comprehensive documentation)

### Real-World Implementation
- [use-case-scenarios.md](references/use-case-scenarios.md) - 8 complete patterns: file menus, toolbars, sidebars, dashboards, mobile apps, etc.

## Related Skills

- [Implementing Sidebar](../implementing-sidebar/) - Side navigation panels
- [Implementing AppBar](../implementing-appbar/) - Top navigation/application bars
- [Implementing Tabs](../implementing-tabs/) - Tab-based content switching
- [Implementing Accordion](../implementing-accordion/) - Expandable content sections
- [Implementing ListView](../implementing-listview/) - List-based navigation
