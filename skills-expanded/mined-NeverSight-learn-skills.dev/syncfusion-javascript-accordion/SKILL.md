---
name: syncfusion-javascript-accordion
description: Build collapsible navigation panels with the Syncfusion TypeScript Accordion component. Use this skill when implementing vertical accordion menus, expanding/collapsing content panels, multi-step wizards, data-driven panels with dynamic content, tabbed navigation alternatives, or nested hierarchical content structures. Covers initialization, expand modes, animations, icons, templates, styling, data binding, and advanced use cases like form wizards.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Syncfusion TypeScript Accordion

The Accordion is a vertically collapsible content panel component that displays one or more expandable/collapsible panels. It supports single or multiple expand modes, custom animations, icons, templates, and data binding.

## When to Use This Skill

**Use this skill when your user needs to:**

- Build responsive accordion menus for navigation
- Create expandable content sections to reduce page height
- Implement multi-step wizards or forms with validation
- Display hierarchical data in collapsible panels
- Customize accordion appearance with icons, animations, and styling
- Load accordion content dynamically from data sources or AJAX
- Integrate accordion with other components (TreeView, forms, etc.)
- Create complex UI patterns like shopping cart steps or FAQ sections

## Navigation and Documentation Guide

### 📚 Documentation Structure

The skill is organized into focused reference files covering different aspects:

#### **Fundamentals**
📄 **[Getting Started](references/getting-started.md)**
- Installation and setup with npm packages
- Items array initialization
- HTML markup initialization
- CSS imports and theme configuration
- Basic working examples

📄 **[Expand Modes](references/expand-modes.md)**
- Single vs Multiple expand modes
- Expand behavior and toggling
- Initial expanded state
- When to use each mode
- Common workflow patterns

#### **Customization & Styling**
📄 **[Customization and Styling](references/customization-styling.md)**
- CSS customization guide and selectors
- Header, item, and content styling
- Icon integration (built-in and Font Awesome)
- Animation effects and timing
- Hover states and selected item styling

#### **Data & Content**
📄 **[Data Loading and Content](references/data-loading.md)**
- Dynamic item loading
- Items array approach
- DataSource binding approach
- AJAX content loading
- Nested accordions
- TreeView integration

📄 **[Templates](references/templates.md)**
- Header templates
- Item templates
- Template data binding
- Dynamic template switching
- Performance optimization

#### **Advanced Topics**
📄 **[Advanced Features](references/advanced-features.md)**
- All methods (addItem, removeItem, enableItem, expandItem, hideItem, select, refresh, etc.)
- All events (expanding, expanded, clicked, created, destroyed)
- Event arguments and properties
- State management
- Event listeners
- RTL support and accessibility

📄 **[Advanced Use Cases](references/advanced-use-cases.md)**
- Multi-step form wizards
- Conditional validation workflows
- Shopping cart checkout flow
- Progress tracking
- Best practices

#### **Complete Reference**
📄 **[API Reference](references/api-reference.md)** ⭐ **START HERE FOR COMPLETE API**
- All properties documented with types and defaults
- All methods with parameters and examples
- All events and event arguments
- Animation configuration
- Complete code examples

## Quick Start Example

```typescript
import { Accordion } from '@syncfusion/ej2-navigations';

// Initialize Accordion with items array
const accordion = new Accordion({
    items: [
        { 
            header: 'Getting Started', 
            content: 'Learn the basics of Accordion component',
            expanded: true 
        },
        { 
            header: 'Features', 
            content: 'Explore rich features like templates and data binding' 
        },
        { 
            header: 'API Reference', 
            content: 'Complete list of properties, events, and methods' 
        }
    ],
    // Use animation object, not enableAnimation boolean
    animation: {
        expand: { effect: 'SlideDown', duration: 400, easing: 'ease-in' },
        collapse: { effect: 'SlideUp', duration: 400, easing: 'ease-out' }
    }
});

accordion.appendTo('#accordion-element');
```

## Common Patterns

### Pattern 1: Single Open Panel (Tabs-like Behavior)
```typescript
const accordion = new Accordion({
    expandMode: 'Single',
    items: [
        { header: 'Tab 1', content: 'Content 1', expanded: true },
        { header: 'Tab 2', content: 'Content 2' },
        { header: 'Tab 3', content: 'Content 3' }
    ]
});
```

### Pattern 2: Multiple Open Panels
```typescript
const accordion = new Accordion({
    expandMode: 'Multiple',  // Default
    items: [
        { header: 'Section A', content: 'Content A', expanded: true },
        { header: 'Section B', content: 'Content B', expanded: true },
        { header: 'Section C', content: 'Content C' }
    ]
});
```

### Pattern 3: Accordion with Icons
```typescript
const accordion = new Accordion({
    items: [
        { 
            header: 'Sports', 
            iconCss: 'e-sports e-acrdn-icons',
            content: 'Athletic activities content'
        },
        { 
            header: 'Games', 
            iconCss: 'e-games e-acrdn-icons',
            content: 'Gaming activities content'
        }
    ]
});
```

### Pattern 4: Dynamically Manage Items
```typescript
const accordion = new Accordion({
    items: [...],
    created: (args) => {
        // Disable item at index 2 initially
        accordion.enableItem(2, false);
        
        // After some action, enable it
        setTimeout(() => {
            accordion.enableItem(2, true);
        }, 2000);
    }
});
```

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `items` | AccordionItem[] | [] | Array of accordion items with header, content, and options |
| `dataSource` | object[] \| DataManager | - | External data source (items array, OData, JSON, AJAX) |
| `expandMode` | 'Single' \| 'Multiple' | 'Multiple' | Single or Multiple expand mode |
| `headerTemplate` | string | - | Custom HTML template for item headers |
| `itemTemplate` | string | - | Custom HTML template for entire items |
| `expandedIndices` | number[] | [] | Indices of items to expand initially |
| `animation` | AnimationSettings | {expand: {}, collapse: {}} | Animation with effect, duration, easing |
| `height` | string \| number | auto | Height of accordion container |
| `width` | string \| number | 100% | Width of accordion container |
| `enableRtl` | boolean | false | Right-to-left text direction |
| `enablePersistence` | boolean | false | Persist expanded state in localStorage |
| `enableHtmlSanitizer` | boolean | true | Sanitize HTML for security |

## Essential Imports

```typescript
// Main component
import { Accordion } from '@syncfusion/ej2-navigations';

// Optional: Enable ripple effect
import { enableRipple } from '@syncfusion/ej2-base';
enableRipple(true);

// CSS styles (choose one theme)
import '@syncfusion/ej2-base/styles/fluent2.css';
import '@syncfusion/ej2-navigations/styles/fluent2.css';
```

## Next Steps

- Explore data binding patterns in **Data Loading and Content**
- Learn template syntax in **Templates** for custom UI
- Implement form wizards in **Advanced Use Cases**
- Check **Advanced Features** for event handling and state management
