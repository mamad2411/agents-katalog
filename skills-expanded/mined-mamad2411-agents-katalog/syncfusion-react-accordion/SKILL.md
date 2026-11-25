---
name: syncfusion-react-accordion
description: |
  Guide users to implement Syncfusion React Accordion component for collapsible content panels. Use this skill whenever the user needs to create expandable/collapsible sections, accordion layouts, tabbed content panels, multi-step forms, FAQs, or navigation with expandable items. Covers component setup, expand modes, animations, dynamic content loading, styling, events, lifecycle, React hooks integration, and complete API reference.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Navigation Components"
---

# Implementing Syncfusion React Accordion

The React Accordion component provides a clean, organized way to display content in collapsible panels. It's perfect for creating expandable content sections, FAQs, multi-step forms, and navigation menus with minimal code.

## Component Overview

The Accordion component renders a stack of collapsible panels where:
- Each panel has a header (clickable to toggle) and content area
- Headers can be simple text or custom templates
- Content can be static, dynamic, or rendered from other React components
- Supports single expand mode (one panel at a time) or multiple (many panels at once)
- Built-in animations for smooth expand/collapse transitions
- Full keyboard navigation and accessibility support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** First time setting up the Accordion component
- Package installation (@syncfusion/ej2-react-navigations)
- CSS imports and theme configuration (Tailwind, Bootstrap)
- Two initialization methods (Items API vs HTML markup)
- Item configuration (header, content, cssClass, disabled, expanded)
- Basic component setup with examples
- First render and minimal working example

### Expand Modes
📄 **Read:** [references/expand-modes.md](references/expand-modes.md)

**When to read:** Controlling which panels expand at the same time
- Single expand mode (only one panel open at a time)
- Multiple expand mode (default, many panels can be open)
- Setting initial expanded state with `expandedIndices` property
- Toggle behavior on header click
- Use cases for choosing each mode
- Keeping single pane open always pattern

### Animation Effects
📄 **Read:** [references/animation-effects.md](references/animation-effects.md)

**When to read:** Customizing panel transitions and visual effects
- Default animations (SlideDown for expand, SlideUp for collapse)
- Choosing from available animation effects (FadeIn, ZoomIn, etc.)
- Configuring easing and duration properties
- Separate expand/collapse animation control
- Disabling animations entirely
- Performance considerations

### Content Loading
📄 **Read:** [references/content-loading.md](references/content-loading.md)

**When to read:** Loading content dynamically or from external sources
- Loading accordion items dynamically with `addItem()` method
- Loading content from data sources (dataSource property)
- Fetching content via HTTP requests and POST
- Template-based rendering (headerTemplate, itemTemplate)
- Rendering other React components inside panels
- Lazy loading and deferred content patterns

### Events & Lifecycle
📄 **Read:** [references/events-lifecycle.md](references/events-lifecycle.md)

**When to read:** Handling user interactions and component lifecycle
- Component lifecycle events (created, destroyed)
- Expand/collapse events (expanding, expanded)
- Click event handling (clicked)
- Event arguments and properties
- Preventing default actions with event.cancel
- Real-world event patterns and examples

### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)

**When to read:** Customizing appearance and integrating with design systems
- CSS classes for styling (header, panel, content areas)
- Built-in theme options and theme switching
- Custom styling with CSS and utilities (Tailwind, Bootstrap)
- RTL (right-to-left) support
- Responsive design patterns
- Using cssClass property for custom styling

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

**When to read:** Building complex layouts and optimizing performance
- Component methods (expandItem, enableItem, hideItem, etc.)
- Nested accordions and hierarchical structures
- React hooks integration (useState, useRef, useEffect)
- Keyboard navigation behavior
- Accessibility features (ARIA attributes, screen readers)
- Performance optimization for large accordion lists
- Custom expand/collapse action patterns

---

## Quick Start Example

Basic accordion with three collapsible panels:

```jsx
import React from 'react';
import { AccordionComponent, AccordionItemDirective, AccordionItemsDirective } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';
import '@syncfusion/ej2-react-navigations/styles/tailwind3.css';

export default function App() {
  return (
    <AccordionComponent expandMode='Multiple'>
      <AccordionItemsDirective>
        <AccordionItemDirective 
          header='HTML' 
          content='HTML is a markup language used to create web pages.' 
        />
        <AccordionItemDirective 
          header='CSS' 
          content='CSS is used to style HTML elements and create layouts.' 
        />
        <AccordionItemDirective 
          header='JavaScript' 
          content='JavaScript adds interactivity to web applications.' 
        />
      </AccordionItemsDirective>
    </AccordionComponent>
  );
}
```

## Common Patterns

### Pattern 1: FAQ Section (Single Expand Mode)
Questions automatically collapse when a new one is opened:

```jsx
<AccordionComponent expandMode='Single'>
  <AccordionItemsDirective>
    <AccordionItemDirective header='What is React?' content='React is a JavaScript library for building UIs with components.' />
    <AccordionItemDirective header='What is JSX?' content='JSX is a syntax extension for writing HTML-like code in JavaScript.' />
  </AccordionItemsDirective>
</AccordionComponent>
```

### Pattern 2: Persistent Expansion (Multiple Mode)
All panels can remain expanded simultaneously:

```jsx
<AccordionComponent expandMode='Multiple'>
  <AccordionItemsDirective>
    <AccordionItemDirective expanded={true} header='Features' content='...' />
    <AccordionItemDirective expanded={true} header='Installation' content='...' />
  </AccordionItemsDirective>
</AccordionComponent>
```

### Pattern 3: Default Expanded State
Pre-expand specific panels on load:

```jsx
<AccordionItemDirective 
  expanded={true}
  header='Quick Start' 
  content='This section opens by default.' 
/>
```

---

## Key Props & Methods

### Component Properties

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `expandMode` | 'Single' \| 'Multiple' | Control single/multiple panel expansion | 'Multiple' |
| `expandedIndices` | number[] | Array of indices for initially expanded items | [] |
| `animation` | AnimationSettings | Expand/collapse animation config | SlideDown/SlideUp |
| `dataSource` | Object[] | Array of items for data binding | [] |
| `headerTemplate` | string \| function | Custom header template for all items | null |
| `itemTemplate` | string \| function | Custom item template for rendering | null |
| `height` | string \| number | Component height in px/% | 'auto' |
| `width` | string \| number | Component width in px/% | '100%' |
| `enableHtmlSanitizer` | boolean | Sanitize untrusted HTML content | true |
| `enablePersistence` | boolean | Persist expanded state between reloads | false |
| `enableRtl` | boolean | Enable right-to-left layout | false |
| `locale` | string | Locale code for internationalization | '' |

### Item Properties

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `header` | string | Item header text (accepts HTML) | - |
| `content` | string | Item content text (accepts HTML) | - |
| `expanded` | boolean | Set initial expanded state for item | false |
| `disabled` | boolean | Disable specific accordion item | false |
| `cssClass` | string | Custom CSS classes for item | - |

### Component Methods

| Method | Parameters | Purpose |
|--------|-----------|---------|
| `addItem()` | item, index (optional) | Add new accordion item(s) |
| `removeItem()` | index | Remove item at specified index |
| `enableItem()` | index, isEnable | Enable/disable specific item |
| `hideItem()` | index, isHidden | Show/hide specific item |
| `expandItem()` | isExpand, index (optional) | Expand/collapse items |
| `select()` | index | Set focus to item header |
| `destroy()` | none | Remove component from DOM |

---

## Common Use Cases

| Use Case | Mode | Key Feature |
|----------|------|------------|
| FAQ Section | Single | Only one question visible at a time |
| Settings Panel | Multiple | Check multiple options simultaneously |
| Multi-Step Form | Single | Guide user through steps sequentially |
| Content Organizer | Multiple | Browse multiple topics at once |
| Navigation Menu | Single | Tree-like hierarchical navigation |
| Data Dashboard | Multiple | View multiple data sections together |

---

## Next Steps

1. **Start with Getting Started** to set up your first Accordion
2. **Choose Expand Mode** based on your use case
3. **Add Animations** for polish and user feedback
4. **Load Content Dynamically** if using data sources
5. **Customize Styling** to match your design system
6. **Explore Advanced Features** for complex scenarios

Need help? Check the specific reference files above based on what you're trying to build!
