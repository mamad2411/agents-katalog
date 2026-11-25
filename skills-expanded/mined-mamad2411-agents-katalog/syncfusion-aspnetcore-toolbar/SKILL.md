---
name: syncfusion-aspnetcore-toolbar
description: A simple toolbar component that organizes command buttons and responsive controls into a horizontal interface. Ideal for document editors, content management systems, and application headers to trigger actions and manage user workflows efficiently.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing ASP.NET Core Toolbar

The Syncfusion Toolbar is a command-driven navigation component that organizes buttons, input controls, and custom templates into a responsive horizontal container. It's ideal for application headers, document editors, and toolbars that need to handle responsive overflow with scrollable or popup modes.

## When to Use This Skill

Use this skill when you need to:

- **Create command bars** for editors, dashboards, or application headers
- **Build responsive toolbars** that handle overflow with scrollable or popup modes
- **Integrate button controls** with icons, text, and custom templates
- **Add input components** like textboxes, dropdowns, or radio buttons to a toolbar
- **Customize toolbar behavior** with tooltips, alignment, and keyboard navigation
- **Manage item visibility** with overflow priority and popup customization
- **Toggle states and actions** with custom buttons and event handling

## Component Overview

The Toolbar control provides:

- **Item Types**: Buttons (default), Separators, and Input containers
- **Responsive Modes**: Scrollable (default with navigation arrows) and Popup overflow
- **Template Support**: HTML-based rendering with item-wise customization
- **Styling Options**: CSS classes, icons (prefix/suffix), width control, and themes
- **Event Handling**: Click events, creation/destroy events, and keyboard navigation
- **Keyboard Support**: Tab navigation with configurable tabIndex and arrow key support

## Documentation and Navigation Guide

Navigate to the reference files below to explore specific features and implementation patterns:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation and setup
- TagHelper registration and configuration
- CSS and script resource inclusion
- Basic toolbar creation with items
- First working examples with icons and text

### Item Configuration
📄 **Read:** [references/item-configuration-guide.md](references/item-configuration-guide.md)
- Button items with text, icons, and width properties
- Separator items and behavior constraints
- Input items for integrated components (NumericTextBox, DropDownList, RadioButton)
- Tab key navigation with tabIndex property
- Complete property tables and examples

### Responsive Modes and Overflow
📄 **Read:** [references/responsive-modes-and-overflow.md](references/responsive-modes-and-overflow.md)
- Scrollable mode with navigation arrows and swipe support
- Popup mode with command priority system
- Overflow property options (show, hide, none)
- ShowAlwaysInPopup for permanent popup items
- ShowTextOn property for button text visibility
- Real-world responsive examples

### Templates and Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- HTML-based template rendering structure
- Item templates using strings and query selectors
- Popup customization with e-overflow-show and e-overflow-hide classes
- Button text modes (e-popup-text, e-toolbar-text)
- Menu component integration
- CSS class customization patterns

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Toggle button implementation and state management
- Tooltip integration with tooltipText property
- Command customization with htmlAttributes and cssClass
- Scroll step customization for navigation
- Item-wise custom templates with complex controls
- Event arguments and handler implementation

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete Toolbar properties and their defaults
- All supported events with signatures
- Item configuration properties
- Overflow and alignment enumerations
- Method signatures for programmatic control
- TagHelper-compliant code examples for each API

## Quick Start Example

Basic toolbar with buttons and separator:

```html
<!-- In ~/Pages/_ViewImports.cshtml -->
@addTagHelper *, Syncfusion.EJ2

<!-- In ~/Pages/Shared/_Layout.cshtml (head) -->
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/{{ site.ej2version }}/dist/ej2.min.js"></script>

<!-- In ~/Pages/Shared/_Layout.cshtml (body, end) -->
<ejs-scripts></ejs-scripts>

<!-- In ~/Pages/Index.cshtml -->
<ejs-toolbar id="toolbar" width="600px">
    <e-toolbar-items>
        <e-toolbar-item text="Cut" prefixIcon="e-cut-icon tb-icons" tooltipText="Cut"></e-toolbar-item>
        <e-toolbar-item text="Copy" prefixIcon="e-copy-icon tb-icons" tooltipText="Copy"></e-toolbar-item>
        <e-toolbar-item text="Paste" prefixIcon="e-paste-icon tb-icons" tooltipText="Paste"></e-toolbar-item>
        <e-toolbar-item type="Separator"></e-toolbar-item>
        <e-toolbar-item text="Bold" prefixIcon="e-bold-icon tb-icons" tooltipText="Bold"></e-toolbar-item>
        <e-toolbar-item text="Italic" prefixIcon="e-italic-icon tb-icons" tooltipText="Italic"></e-toolbar-item>
    </e-toolbar-items>
</ejs-toolbar>
```

## Common Patterns

**Icon-only buttons with tooltips:**
Use `prefixIcon` with `tooltipText` for minimal visual footprint with affordance.

**Responsive overflow with priority:**
Set `overflow="show"` for always-visible buttons and `overflow="hide"` for secondary actions that move to popup.

**Input controls in toolbar:**
Use `type="Input"` to embed components like DropDownList or NumericTextBox for filtering or configuration.

**Custom templates:**
Use `template` property with HTML strings or query selectors for complex custom controls.

**Tab navigation:**
Set `tabIndex` on items to enable Tab/Shift+Tab keyboard navigation in addition to arrow keys.

## Key Properties

- **`width`**: Sets toolbar container width (pixels or percentage)
- **`overflowMode`**: Controls responsive behavior - `Scrollable` (default) or `Popup`
- **`scrollStep`**: Distance to scroll when navigation arrows are clicked
- **`allowKeyboard`**: Enables keyboard navigation (default: true)
- **`enableCollision`**: Enables popup collision detection
- **`cssClass`**: Applies custom CSS classes to the toolbar root

## Item Configuration Quick Reference

| Item Type | Use Case | Key Properties |
|-----------|----------|----------------|
| **Button** | Command actions | `text`, `prefixIcon`, `suffixIcon`, `width`, `tooltipText` |
| **Separator** | Visual dividers | `type: "Separator"` |
| **Input** | Embedded components | `type: "Input"`, `template` |
| **Custom** | Complex controls | `type: "Button"`, `template` |

## Common Use Cases

- **Text Editor Toolbar**: Cut, Copy, Paste, formatting buttons with separators
- **Dashboard Filter Bar**: DropDownList and DatePicker for filtering data
- **Application Header**: Branding + navigation buttons + user menu
- **Media Player Controls**: Play, Pause, Stop, Volume with custom templates
- **Document Tools**: Save, Print, Export with responsive overflow handling

---

**Start with [Getting Started Guide](references/getting-started.md) to set up your first toolbar.**
