---
name: syncfusion-aspnetcore-accordion
description: Implement Syncfusion Accordion component for organizing expandable navigation and content sections with single or multiple pane expansion support.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Syncfusion Accordion

## When to Use This Skill

use this skill when users need to:
- Organize content into collapsible sections
- Build FAQ or help sections with expandable items
- Create tabbed-like navigation with accordion panes
- Implement progressive disclosure of content
- Build hierarchical nested accordion structures
- Configure single or multiple expand modes
- Load accordion content dynamically from data sources
- Customize accordion animations and interactions
- Integrate accordion with ASP.NET Core applications

The Accordion component is the ideal choice whenever you need vertically stacked, collapsible content panels that display one or more panels at a time.

## Component Overview

The Syncfusion Accordion is a vertically collapsible content panel control that:

- Supports **Single** and **Multiple** expand modes
- Handles static items and data-bound content
- Enables nested accordion structures for hierarchical content
- Provides animation configuration for expand/collapse actions
- Fires lifecycle events (created, expanding, expanded, collapsing, collapsed, clicked)
- Supports content loading from partial views or via POST requests
- Allows programmatic control through public methods like `expandItem()`
- Maintains state persistence across page reloads
- Provides RTL support and HTML sanitization

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- System prerequisites and NuGet package installation
- TagHelper registration for ASP.NET Core
- Stylesheet and script resource configuration
- Creating your first Accordion control
- Understanding AccordionItem structure and markup patterns

### Expand Modes & Behavior
📄 **Read:** [references/expand-modes.md](references/expand-modes.md)
- Single expand mode: mutually exclusive item expansion
- Multiple expand mode: independent item expansion (default)
- Toggle behavior and user interactions
- Keeping a single pane open always
- Expand mode configuration examples

### Data Binding & Dynamic Content
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Static item binding with AccordionItem elements
- DataSource property and dynamic data binding
- OData service integration with DataManager
- Mapping header and content properties from data
- Handling complex data structures

### Advanced Content Loading
📄 **Read:** [references/content-loading.md](references/content-loading.md)
- Loading content from partial views
- Lazy loading strategies for performance
- Dynamic content rendering and updates
- POST-based content requests
- Content refresh and state management

### Customization & Animation
📄 **Read:** [references/customization-animation.md](references/customization-animation.md)
- Configuring expand/collapse animations
- Animation settings: effect, duration, easing
- Event handling: expanding, expanded, collapsing, collapsed
- Programmatic expand/collapse with `expandItem()` method
- Advanced interaction patterns and sequential operations

### Nested Accordion Structures
📄 **Read:** [references/nested-accordion.md](references/nested-accordion.md)
- Creating multi-level accordion hierarchies
- Referencing nested accordion elements
- Content element ID references
- Performance considerations at scale

### Complete API Reference
📄 **Read:** [api-reference.md](references/api-reference.md)
- All properties, methods, and events available
- AccordionItem configuration options
- Animation settings and event arguments
- Non-duplicative reference to skill files for detailed guidance

## Quick Start Example

```cshtml
<!-- Add Accordion in your Razor page -->
<div class="control_wrapper accordion-control-section">
    <ejs-accordion id="myAccordion" expand-mode="Multiple">
        <e-accordion-accordionitems>
            <e-accordion-accordionitem expanded="true" 
                header="Getting Started" 
                content="Learn the basics of Accordion component integration">
            </e-accordion-accordionitem>
            <e-accordion-accordionitem 
                header="Features" 
                content="Explore expand modes, data binding, and customization options">
            </e-accordion-accordionitem>
            <e-accordion-accordionitem 
                header="Advanced Topics" 
                content="Discover nested accordions, animations, and event handling">
            </e-accordion-accordionitem>
        </e-accordion-accordionitems>
    </ejs-accordion>
</div>
```

This creates a basic accordion with three items, the first one expanded by default.

## Common Patterns

### FAQ Section with Single Expand Mode
Use `Single` expand mode when only one FAQ answer should be visible at a time:
```cshtml
<ejs-accordion expand-mode="Single">
```

### Documentation with Multiple Panels Open
Use `Multiple` expand mode (default) to allow readers to compare multiple sections simultaneously.

### Dynamic Content Loading
Bind accordion items to a DataSource for dynamic content:
```cshtml
<ejs-accordion data-source="Model.AccordionItems">
```

### Keeping One Panel Always Open
In Single mode, configure the `expanding` event to prevent the last open item from being collapsed.

## Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `expandMode` | `Single` \| `Multiple` | `Multiple` | Controls whether one or multiple items can be expanded simultaneously |
| `items` | `AccordionItemModel[]` | `[]` | Array of accordion items to display |
| `dataSource` | `Object[]` | `[]` | Binds dynamic data to accordion items |
| `expandedIndices` | `number[]` | `[]` | Specifies which items are expanded on initial load |
| `height` | `string` \| `number` | `auto` | Sets accordion container height |
| `width` | `string` \| `number` | `100%` | Sets accordion container width |
| `animation` | `AccordionAnimationSettingsModel` | Configured | Customizes expand/collapse animations |
| `enablePersistence` | `boolean` | `false` | Persists expanded state across page reloads |
| `enableHtmlSanitizer` | `boolean` | `true` | Sanitizes untrusted HTML content |

## When to Use Each Expand Mode

**Single Mode**: Use when content is mutually exclusive or only one section should be visible at once (e.g., step-by-step wizards, radio button-like behavior).

**Multiple Mode**: Use when users need to view multiple sections simultaneously (e.g., FAQ sections, documentation, feature lists).

---

**Next Steps:** Select a reference file based on your needs, or start with Getting Started for a complete setup walkthrough.
