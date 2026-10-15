---
name: syncfusion-angular-appbar
description: Implement Syncfusion Angular AppBar component for navigation, branding, and actions. Use this skill when user needs to add top or bottom navigation bar, sticky headers, AppBar with buttons/menus/sidebars, positioning options, sizing modes (Regular/Prominent/Dense), color modes (Light/Dark/Primary/Inherit), and styling customization. Covers AppBar properties like isSticky, enablePersistence, enableRtl, htmlAttributes, responsive navigation patterns, action bars, header layouts, and navigation components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Syncfusion Angular AppBar

The Syncfusion Angular AppBar component is a flexible navigation component also known as an action bar or nav bar. It displays information and actions related to the current application screen and is used to show branding, screen titles, navigation, and actions. The AppBar supports height modes, color modes, positioning, and integrates seamlessly with other Syncfusion components like Buttons, Menus, and Sidebars.

## When to Use This Skill

- **Navigation Headers**: Creating top or bottom navigation bars for applications
- **Sticky Headers**: Building persistent headers that stay visible while scrolling
- **Responsive Navigation**: Designing navigation that adapts to different screen sizes
- **Component Integration**: Combining AppBar with Buttons, Menus, DropDownButtons, and Sidebars
- **Branding & Layout**: Displaying logos, titles, and action buttons
- **Visual Styling**: Customizing AppBar appearance with size modes and color themes
- **Content Spacing**: Using spacers and separators to organize AppBar content

## Component Overview

The AppBar component provides:
- **Positioning options**: Top (default), Bottom, Sticky
- **Size modes**: Regular (default), Prominent (tall), Dense (compact)
- **Color modes**: Light, Dark, Primary, Inherit
- **Built-in spacing**: Spacer elements and Separators for content organization
- **Component integration**: Works with Buttons, DropDownButtons, Menus, and Sidebars
- **Customization**: CSS classes, custom styling, and theme support

## Documentation and Navigation Guide

**Choose the reference that matches your task:**

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Angular environment setup and Angular CLI installation
- Syncfusion AppBar package installation (Ivy and ngcc versions)
- Basic component implementation
- CSS imports and theme configuration
- Running the application

### Positioning and Layout
📄 **Read:** [references/positioning-and-layout.md](references/positioning-and-layout.md)
- Top AppBar positioning (default)
- Bottom AppBar positioning
- Sticky AppBar behavior during scrolling
- Position and isSticky property configuration
- Examples for each positioning type

### Sizing and Colors
📄 **Read:** [references/sizing-and-colors.md](references/sizing-and-colors.md)
- Size modes: Regular, Prominent, Dense (mode property)
- Color modes: Light, Dark, Primary, Inherit (colorMode property)
- Visual customization with different combinations
- Height adjustments for Prominent AppBar
- Comprehensive examples for all configurations

### Design Patterns
📄 **Read:** [references/design-patterns.md](references/design-patterns.md)
- Spacer element for spacing between AppBar content
- Separator element for visual grouping
- AppBar with Menu component integration
- AppBar with Button and DropDownButton integration
- AppBar with Sidebar integration
- Media queries for responsive behavior

### Styling and Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- Built-in CSS classes (.e-appbar, .e-prominent, .e-dense, .e-light, .e-dark, .e-primary, .e-inherit)
- CssClass property for custom styling
- HtmlAttributes directive for inline attributes
- Theme Studio integration
- Custom theming and styling approaches

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md) - **Complete API Documentation**
- All 9 properties with usage examples and defaults
- All 2 events (created, destroyed) with examples
- CSS classes and HTML elements
- Property combinations and patterns
- Accessibility and internationalization

## Quick Start

Here's a minimal AppBar implementation:

```typescript
import { Component } from "@angular/core";
import { AppBarModule } from '@syncfusion/ej2-angular-navigations'
import { ButtonModule } from '@syncfusion/ej2-angular-buttons'

@Component({
  imports: [AppBarModule, ButtonModule],
  standalone: true,
  selector: "app-root",
  template: `
    <div class="control-container">
      <ejs-appbar colorMode="Primary">
        <button ejs-button cssClass="e-inherit" iconCss="e-icons e-menu"></button>
        <span style="margin: 0 5px">Angular AppBar</span>
        <div class="e-appbar-spacer"></div>
        <button ejs-button cssClass="e-inherit">Login</button>
      </ejs-appbar>
    </div>
  `
})
export class AppComponent { }
```

Add CSS imports to your `style.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/material3";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material3";
```

## Common Patterns

### Pattern 1: Spacer for Content Distribution
Use `.e-appbar-spacer` to push content to the ends:

```typescript
<ejs-appbar colorMode="Primary">
  <button ejs-button cssClass="e-inherit" iconCss="e-icons e-menu"></button>
  <div class="e-appbar-spacer"></div>
  <button ejs-button cssClass="e-inherit">FREE TRIAL</button>
</ejs-appbar>
```

### Pattern 2: Separator for Content Grouping
Use `.e-appbar-separator` to visually separate button groups:

```typescript
<ejs-appbar colorMode="Primary">
  <button ejs-button cssClass="e-inherit" iconCss="e-icons e-cut"></button>
  <button ejs-button cssClass="e-inherit" iconCss="e-icons e-copy"></button>
  <button ejs-button cssClass="e-inherit" iconCss="e-icons e-paste"></button>
  <div class="e-appbar-separator"></div>
  <button ejs-button cssClass="e-inherit" iconCss="e-icons e-bold"></button>
</ejs-appbar>
```

### Pattern 3: Bottom Positioned AppBar
Set position to Bottom for footer-style navigation:

```typescript
<ejs-appbar colorMode="Primary" position="Bottom">
  <button ejs-button cssClass="e-inherit" iconCss="e-icons e-home"></button>
  <div class="e-appbar-spacer"></div>
  <button ejs-button cssClass="e-inherit">Settings</button>
</ejs-appbar>
```

### Pattern 4: Sticky Header
Use isSticky property for headers that persist while scrolling:

```typescript
<ejs-appbar colorMode="Primary" [isSticky]="true">
  <button ejs-button cssClass="e-inherit" iconCss="e-icons e-menu"></button>
  <span>My App</span>
</ejs-appbar>
```

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `position` | "Top" \| "Bottom" | "Top" | Vertical position of AppBar |
| `isSticky` | boolean | false | Makes AppBar sticky during scrolling |
| `mode` | "Regular" \| "Prominent" \| "Dense" | "Regular" | Controls AppBar height |
| `colorMode` | "Light" \| "Dark" \| "Primary" \| "Inherit" | "Light" | Sets color scheme |
| `cssClass` | string | - | Applies custom CSS classes |
| `enablePersistence` | boolean | false | Persist component state between reloads |
| `enableRtl` | boolean | false | Enable right-to-left direction |
| `htmlAttributes` | Record | - | Custom HTML attributes |
| `locale` | string | "en-US" | Localization settings |

**→ See [API Reference](references/api-reference.md) for complete API documentation with examples**

## Related Syncfusion Components

- **Button** - Interactive buttons within AppBar
- **DropDownButton** - Dropdown menus in AppBar
- **Menu** - Menu bar integration
- **Sidebar** - Side navigation alongside AppBar
- **Toolbar** - Similar action bar component with different styling

---

**Ready to implement?** Start with [references/getting-started.md](references/getting-started.md) to set up your first AppBar, or jump to the specific reference that matches your use case.
