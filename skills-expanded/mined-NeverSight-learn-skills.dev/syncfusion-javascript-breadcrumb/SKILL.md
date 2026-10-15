---
name: syncfusion-javascript-breadcrumb
description: Learn to implement and configure the Syncfusion TypeScript Breadcrumb component for navigation. Use this skill when implementing breadcrumb navigation for web applications. Covers component initialization, item configuration, overflow handling, event management, and advanced customization.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
  category: Navigation Components
---

# Implementing Breadcrumb

The Breadcrumb component is a graphical user interface element that helps identify and highlight the current location within a hierarchical structure of websites. It makes users aware of their current position in a hierarchy of website links, improving navigation experience and reducing cognitive load.

## When to Use This Skill

Use this skill immediately when you need to:
- Display hierarchical navigation paths
- Show current location in a multi-level structure
- Implement breadcrumb trails in single-page applications
- Handle overflow items with different display modes
- Customize breadcrumb appearance and behavior
- Respond to user interactions with breadcrumb items
- Apply dynamic styling and templates to breadcrumb items

## Control Overview

The Breadcrumb component provides:
- **Hierarchical navigation display** - Shows navigation path from root to current location
- **Multiple overflow modes** - Menu, Collapsed, Hidden, Scroll, Wrap, None
- **Item customization** - Templates, icons, disabled states
- **Event handling** - Click events and rendering callbacks
- **RTL support** - Right-to-left direction rendering
- **State persistence** - Optional component state preservation
- **URL-based generation** - Automatic breadcrumb creation from URLs

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic breadcrumb component initialization
- Creating and populating items array
- Appending component to DOM
- Minimal working example with code
- CSS imports and theme configuration

### Component Properties Overview
📄 **Read:** [references/component-properties.md](references/component-properties.md)
- Core property reference (activeItem, cssClass, disabled, enableNavigation)
- Navigation configuration (enableActiveItemNavigation, enableNavigation)
- State management (enablePersistence, enableRtl)
- URL-based breadcrumb generation
- Property descriptions with default values
- Configuration patterns and best practices

### Item Configuration
📄 **Read:** [references/items-configuration.md](references/items-configuration.md)
- BreadcrumbItemModel interface and properties
- Item properties (id, text, url, disabled, iconCss)
- Creating and configuring breadcrumb items
- Managing item states (enabled/disabled)
- Adding icons to navigation items
- Dynamic item updates and manipulation
- Item accessibility considerations

### Templates and Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- itemTemplate property for custom item rendering
- separatorTemplate for custom separators
- Template function patterns and examples
- Custom rendering implementation
- Separator customization (default "/" and alternatives)
- CSS class customization strategies

### Overflow Modes and Behaviors
📄 **Read:** [references/overflow-modes.md](references/overflow-modes.md)
- BreadcrumbOverflowMode enum with all 6 modes
- Menu mode - submenu for overflow items
- Collapsed mode - collapsed icon with hidden items
- Hidden mode - maximum visible items approach
- Scroll mode - HTML scroll bar solution
- Wrap mode - multiple line wrapping
- None mode - single line display
- maxItems configuration with each mode

### Events and Event Handling
📄 **Read:** [references/events-handling.md](references/events-handling.md)
- itemClick event (BreadcrumbClickEventArgs)
- beforeItemRender event (BreadcrumbBeforeItemRenderEventArgs)
- created event for component initialization
- Event handler patterns and setup
- Accessing event arguments and properties
- Canceling events with cancel property
- Common event use cases and patterns

### Methods and Lifecycle
📄 **Read:** [references/methods-and-lifecycle.md](references/methods-and-lifecycle.md)
- Component lifecycle methods
- appendTo() - DOM element attachment
- destroy() - component cleanup
- dataBind() - immediate data binding
- refresh() - component re-rendering
- getRootElement() - accessing root element
- addEventListener/removeEventListener - dynamic event management
- Inject() - module injection
- Method best practices and timing

## Quick Start Example

```typescript
// Create breadcrumb component
const breadcrumbObj = new Breadcrumb({
  items: [
    { text: 'Home', url: '/' },
    { text: 'Category', url: '/category' },
    { text: 'Product', url: '/product' }
  ],
  enableNavigation: true
});

// Append to DOM
breadcrumbObj.appendTo('#breadcrumb');

// Handle item click
breadcrumbObj.itemClick = (args) => {
  console.log('Clicked item:', args.item.text);
};
```

## Common Patterns

### Pattern 1: Basic Navigation with Icons
```typescript
const breadcrumb = new Breadcrumb({
  items: [
    { text: 'Dashboard', url: '/', iconCss: 'e-icons e-home' },
    { text: 'Products', url: '/products', iconCss: 'e-icons e-package' },
    { text: 'Electronics', url: '/products/electronics' }
  ]
});
```

### Pattern 2: Overflow with Menu Mode
```typescript
const breadcrumb = new Breadcrumb({
  items: [...manyItems],
  maxItems: 4,
  overflowMode: 'Menu'
});
```

### Pattern 3: Event Handling for Navigation
```typescript
const breadcrumb = new Breadcrumb({
  items: [...items],
  itemClick: (args) => {
    // Prevent default navigation
    args.cancel = false;
    // Navigate to item URL
    window.location.href = args.item.url;
  }
});
```

### Pattern 4: Dynamic Item Updates
```typescript
breadcrumb.items = newItemsList;
breadcrumb.dataBind();
```

## Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `items` | BreadcrumbItemModel[] | [] | List of breadcrumb items to display |
| `activeItem` | string | '' | URL of the active breadcrumb item |
| `overflowMode` | string | 'Menu' | How to handle items exceeding maxItems |
| `maxItems` | number | -1 | Maximum items before overflow behavior |
| `enableNavigation` | boolean | true | Allow item navigation |
| `disabled` | boolean | false | Disable entire breadcrumb |
| `cssClass` | string | '' | Custom CSS classes for styling |
| `enableRtl` | boolean | false | Right-to-left rendering |

## Common Use Cases

**Use Case 1: Website Navigation Breadcrumb**
- Display current page location in site hierarchy
- Allow navigation to parent pages
- Show active item highlighting

**Use Case 2: E-Commerce Category Navigation**
- Show product category path
- Handle deeply nested categories with overflow
- Enable quick navigation to parent categories

**Use Case 3: Application Workspace Navigation**
- Display current module/feature path
- Show navigation history breadcrumb
- Implement dynamic path updates

**Use Case 4: File System Browser**
- Show current directory path
- Navigate through folder hierarchy
- Handle large folder structures with overflow

---

**Next Steps:** Choose a reference above to dive into specific implementation details, or run test cases to validate your breadcrumb implementation.
