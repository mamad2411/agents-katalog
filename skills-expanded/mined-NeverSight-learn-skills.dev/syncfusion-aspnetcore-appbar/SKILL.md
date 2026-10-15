---
name: syncfusion-aspnetcore-appbar
description: Implement Syncfusion AppBar component to provide consistent top-level navigation and actions in your ASP.NET Core applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion AppBar

## When to Use This Skill

Use the AppBar component when you need to:
- **Create top or bottom navigation bars** with consistent branding and action placement
- **Display application titles and branding** with sizing flexibility (regular, prominent, or dense modes)
- **Provide multiple color themes** to match application design (light, dark, primary, or inherited colors)
- **Support responsive layouts** that adapt to different screen sizes with media queries
- **Integrate navigation elements** like menus, buttons, and sidebars using the inheritance system
- **Implement sticky/fixed positioning** for persistent access to top-level actions during scrolling
- **Support right-to-left (RTL) languages** with built-in directional support

## Component Overview

The Syncfusion AppBar is a flexible header component that displays information and actions related to the current application screen. It provides:

- **Positioning Options**: Top (default) or bottom placement
- **Size Flexibility**: Regular (default), Prominent (larger), or Dense (compressed) heights
- **Color Modes**: Light, Dark, Primary, or Inherit from parent
- **Sticky Support**: Fixed positioning during page scrolling via `isSticky` property
- **Content Layout**: Spacer and Separator elements for organizing content
- **Component Integration**: Seamless styling for nested Button, DropDownButton, Menu, and TextBox via `e-inherit` CSS class
- **Responsive Design**: Full media query support for adaptive layouts
- **Localization**: Custom locale support with RTL rendering

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements verification
- Project creation using Microsoft Templates or Syncfusion Extension
- NuGet package installation and configuration
- Tag Helper registration in _ViewImports.cshtml
- Stylesheet and script references (CDN setup)
- Script Manager registration
- Basic AppBar implementation
- First render and verification

### Positioning and Layout
📄 **Read:** [references/positioning.md](references/positioning.md)
- Top positioning behavior (default)
- Bottom positioning with `position="Bottom"` property
- Sticky positioning for fixed headers with `isSticky="true"`
- Combining position with responsive design
- Real-world navigation patterns and use cases

### Sizing Modes
📄 **Read:** [references/sizing-modes.md](references/sizing-modes.md)
- Regular mode (default height, `mode="Regular"`)
- Prominent mode for larger content (`mode="Prominent"`)
- Dense mode for compact layouts (`mode="Dense"`)
- Use case guidance and content adaptation per mode
- Height customization strategies

### Color and Theme Modes
📄 **Read:** [references/color-modes.md](references/color-modes.md)
- Light mode (default appearance, `colorMode="Light"`)
- Dark mode for contrast (`colorMode="Dark"`)
- Primary mode for brand colors (`colorMode="Primary"`)
- Inherit mode for parent element colors (`colorMode="Inherit"`)
- Integration with CSS theme system

### Design Patterns and Layouts
📄 **Read:** [references/design-layouts.md](references/design-layouts.md)
- Spacer element for dynamic content distribution
- Separator element for visual content grouping
- Media queries for responsive AppBar design
- Component integration patterns (Menu, Button, DropDownButton with `e-inherit`)
- SideBar integration and toggle patterns
- Real-world design examples and best practices

### Customization and Advanced Features
📄 **Read:** [references/customization.md](references/customization.md)
- CSS class customization via `cssClass` property
- HTML attributes configuration via `htmlAttributes`
- Right-to-left (RTL) support with `enableRtl="true"`
- Component state persistence with `enablePersistence="true"`
- Locale customization for internationalization
- Advanced styling and edge cases

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All properties with type information and usage
- Event declarations with proper TagHelper binding syntax
- Enumeration values for position, mode, and color
- Code examples for APIs not covered in other references
- API summary and cross-references

## Quick Start Example

Create a basic AppBar with navigation buttons:

```html
<div class="col-lg-12 control-section default-appbar-section">
    <ejs-appbar id="defaultAppBar" colorMode="Primary">
        <e-content-template>
            <ejs-button aria-label="menu" id="menuButton" cssClass="e-inherit" iconCss="e-icons e-menu"></ejs-button>
            <span class="regular" style="margin:0 5px">My Application</span>
            <div class="e-appbar-spacer"></div>
            <ejs-button id="trialButton" cssClass="e-inherit" content="Get Started"></ejs-button>
        </e-content-template>
    </ejs-appbar>
</div>
```

**Key Elements:**
- `colorMode="Primary"` - Uses primary brand color theme
- `<e-content-template>` - Container for AppBar content
- `cssClass="e-inherit"` - Buttons inherit AppBar colors
- `<div class="e-appbar-spacer"></div>` - Pushes content to opposite sides

## Common Patterns

### Pattern 1: Top Navigation with Title and Actions
```html
<ejs-appbar id="navAppBar" position="Top">
    <e-content-template>
        <!-- Left: Logo/Menu -->
        <ejs-button iconCss="e-icons e-menu" cssClass="e-inherit"></ejs-button>
        <!-- Center: Title -->
        <span style="margin: 0 auto;">Dashboard</span>
        <!-- Right: User Actions -->
        <div class="e-appbar-spacer"></div>
        <ejs-button content="Profile" cssClass="e-inherit"></ejs-button>
    </e-content-template>
</ejs-appbar>
```

### Pattern 2: Sticky Header for Persistent Navigation
```html
<ejs-appbar id="stickyAppBar" isSticky="true" colorMode="Dark">
    <e-content-template>
        <!-- Sticky content remains visible during scroll -->
    </e-content-template>
</ejs-appbar>
```

### Pattern 3: Prominent Mode for Feature Headers
```html
<ejs-appbar id="prominentAppBar" mode="Prominent" colorMode="Primary">
    <e-content-template>
        <!-- Larger area for rich content, titles, images -->
    </e-content-template>
</ejs-appbar>
```

## Key Properties Overview

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `position` | AppBarPosition | Top | Placement: Top or Bottom |
| `mode` | AppBarMode | Regular | Height: Regular, Prominent, or Dense |
| `colorMode` | AppBarColor | Light | Theme: Light, Dark, Primary, or Inherit |
| `isSticky` | boolean | false | Fixed positioning during scroll |
| `cssClass` | string | - | Custom CSS classes for styling |
| `enableRtl` | boolean | false | Right-to-left language support |
| `enablePersistence` | boolean | false | State persistence between page reloads |
| `locale` | string | en-US | Custom culture and localization |
| `htmlAttributes` | Record | - | Additional HTML attributes |

## Common Use Cases

1. **E-Commerce Header**: Top sticky AppBar with logo, search, and cart icon
2. **Dashboard Navigation**: Prominent AppBar with breadcrumbs and quick actions
3. **Mobile Navigation**: Dense AppBar with bottom positioning for touch-friendly layouts
4. **Admin Panel**: Dark themed AppBar with user menu and notification badges
5. **Content Platform**: Featured article header using Prominent mode with image background

---

**Next Steps:**
- For setup instructions, read [Getting Started Guide](references/getting-started.md)
- For design decisions, read [Positioning](references/positioning.md) and [Sizing Modes](references/sizing-modes.md)
- For complete API details, read [API Reference](references/api-reference.md)
