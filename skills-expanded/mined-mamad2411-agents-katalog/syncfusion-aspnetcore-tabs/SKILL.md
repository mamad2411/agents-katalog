---
name: syncfusion-aspnetcore-tabs
description: Implement tabbed navigation interfaces in ASP.NET Core using Syncfusion Tab component for organizing and switching between content sections. Use this skill when implementing tab-based navigation, multi-panel content organization, wizards, or any scenario requiring organized content sections with header-based selection.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Core Tabs

The Syncfusion Tab component provides a navigation control for organizing content into separate, selectable tabs. Each tab consists of a header and associated content that appears when the tab is selected.

## When to Use This Skill

- Organizing related content into logical sections with tab navigation
- Creating wizard interfaces with step-by-step progression
- Building collapsible accordion-like interfaces
- Implementing drag-and-drop reorderable tab items
- Setting up stateful tab selection with persistence
- Customizing header styles, positions, and animations
- Loading content dynamically or from external sources

## Component Overview

**Key Features:**
- HeaderPlacement: Top, Bottom, Left, or Right positioning
- Content loading modes: Init (all), Demand (lazy-load), Dynamic (replace)
- Drag-and-drop reordering with event callbacks
- Animation configuration for smooth transitions
- RTL support and localization
- State persistence across page reloads
- Keyboard navigation (Tab key support)
- Height management: None, Auto, Content, or Fill

**Core Properties:**
- `items`: Array of TabItem objects defining headers and content
- `selectedItem`: Index of the active tab
- `heightAdjustMode`: Controls content panel height behavior
- `allowDragAndDrop`: Enable/disable drag reordering
- `headerPlacement`: Position of tab headers
- `enablePersistence`: Save/restore selected tab on reload
- `loadOn`: Content loading strategy (Init/Demand/Dynamic)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation and setup
- Tag Helper configuration
- CSS/script references (CDN and NPM)
- Basic Tab initialization with TagHelper
- JSON items collection vs HTML element binding

### Tab Configuration and Content
📄 **Read:** [references/tab-content-rendering.md](references/tab-content-rendering.md)
- Tab header structure and customization
- Content rendering modes (HTML, Partial View, External POST, Templates)
- Dynamic content loading and population
- Content templates and inline rendering

### Tab Interaction Features
📄 **Read:** [references/tab-interaction.md](references/tab-interaction.md)
- Tab selection programmatically and via user interaction
- Click handlers and selection events
- Keyboard navigation with Tab key support
- Drag-and-drop reordering between tabs
- Nested tabs and hierarchical structures

### Styling and Layout
📄 **Read:** [references/styling-layout.md](references/styling-layout.md)
- CSS class customization (e-fill, e-background, e-accent)
- Tab height and content height adjustment modes
- Horizontal scrolling and popup overflow modes
- Header icon positioning and orientations
- Responsive design patterns

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- State persistence configuration
- Localization and internationalization
- RTL (right-to-left) support
- Animation customization (previous/next effects)
- Collapsible tabs and wizard patterns
- API methods for programmatic control

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API documentation
- All properties with types and defaults
- Event signatures and parameters
- Methods for runtime manipulation

## Quick Start Example

Basic Tab with three items using TagHelper syntax:

```cshtml
@using Syncfusion.EJ2.Navigations;

<ejs-tab id="ej2Tab">
    <e-tab-tabitems>
        <e-tab-tabitem header="@(new TabHeader { Text = "Home" })" content="Welcome to home tab"></e-tab-tabitem>
        <e-tab-tabitem header="@(new TabHeader { Text = "Profile" })" content="Your profile information"></e-tab-tabitem>
        <e-tab-tabitem header="@(new TabHeader { Text = "Settings" })" content="Adjust your settings"></e-tab-tabitem>
    </e-tab-tabitems>
</ejs-tab>
```

## Common Patterns

### Lazy-Loading Content (Demand Mode)
```cshtml
<ejs-tab id="ej2Tab" loadOn="ContentLoad.Demand">
    <e-tab-tabitems>
        <e-tab-tabitem header="@(new TabHeader { Text = "Tab1" })" content="Content loads on demand"></e-tab-tabitem>
        <e-tab-tabitem header="@(new TabHeader { Text = "Tab2" })" content="Second tab content"></e-tab-tabitem>
    </e-tab-tabitems>
</ejs-tab>
```

### Dynamic Content Only (Dynamic Mode)
```cshtml
<ejs-tab id="ej2Tab" loadOn="ContentLoad.Dynamic">
    <!-- Only the selected tab's content is in DOM -->
</ejs-tab>
```

### Drag-and-Drop Reordering
```cshtml
<ejs-tab id="ej2Tab" allowDragAndDrop="true">
    <!-- Tab items can be dragged and reordered -->
</ejs-tab>
```

### Header Positioning (Vertical Navigation)
```cshtml
<ejs-tab id="ej2Tab" headerPlacement="@HeaderPosition.Left">
    <!-- Headers appear on the left side -->
</ejs-tab>
```

### Height Management
```cshtml
<ejs-tab id="ej2Tab" heightAdjustMode="@HeightStyles.Auto">
    <!-- Content height auto-adjusts to tallest panel -->
</ejs-tab>
```

### State Persistence
```cshtml
<ejs-tab id="ej2Tab" enablePersistence="true" selectedItem="1">
    <!-- Selected tab index is saved and restored across page loads -->
</ejs-tab>
```

## Key Events

| Event | Trigger | Use Case |
|-------|---------|----------|
| `selecting` | Before tab selection | Validate tab change or prevent selection |
| `selected` | After tab selection | Perform actions on tab switch, detect user vs programmatic selection |
| `adding` | Before adding tab item | Validate new item before insertion |
| `added` | After adding tab item | Update UI after new tab is added |
| `removing` | Before removing tab item | Confirm deletion or cleanup data |
| `removed` | After removing tab item | Update state after removal |
| `onDragStart` | Before drag operation | Prevent dragging specific items |
| `dragging` | During drag operation | Provide visual feedback |
| `dragged` | After drop operation | Update data or move to external source |
| `created` | Component initialized | Initialize related controls |
| `destroyed` | Component destroyed | Clean up resources |

## Integration Checklist

- [ ] NuGet package installed: `Syncfusion.EJ2.AspNet.Core`
- [ ] Tag Helper registered in `_ViewImports.cshtml`
- [ ] CSS theme referenced in layout (CDN or NPM)
- [ ] Script manager `<ejs-scripts>` in layout body
- [ ] Tab component ID is unique per page
- [ ] Content strategy chosen (Init/Demand/Dynamic)
- [ ] Height mode configured for your layout
- [ ] Events wired if dynamic behavior needed
- [ ] Persistence enabled if tab state should survive reload
- [ ] Accessibility verified (keyboard navigation)

---

**Next Steps:** Review the specific reference files based on your feature requirements. Start with getting-started.md for basic setup, then explore advanced features and API reference as needed.
