---
name: syncfusion-javascript-appbar
description: Learn how to implement and configure the Syncfusion TypeScript AppBar control for navigation bars, app headers, and UI toolbars. This skill covers responsive positioning, color modes, sizing, styling, and component integration. Use when building navigation solutions that require flexible layout and styling options.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing AppBar in Syncfusion TypeScript

## When to Use This Skill

Use this skill when you need to:
- Create a responsive application header or navigation bar
- Display branding, screen titles, or navigation actions
- Build app bars with buttons, menus, or custom content
- Position bars at top, bottom, or as sticky elements
- Apply color modes (Light, Dark, Primary, Inherit)
- Customize sizing (Regular, Prominent, Dense)
- Style and theme your AppBar
- Integrate complex layouts with spacers, separators, and components
- Ensure responsive design for different screen sizes
- Implement accessibility features

## AppBar Overview

The **AppBar** (also known as action bar or nav bar) is a Syncfusion navigation component that displays information and actions related to the current application screen. It provides:

- **Flexible positioning**: Top (default), Bottom, or Sticky
- **Multiple sizing modes**: Regular, Prominent, Dense
- **Color themes**: Light, Dark, Primary, Inherit
- **Component integration**: Buttons, DropDownButtons, Menus, Sidebars
- **Layout elements**: Spacers for content distribution, Separators for grouping
- **Responsive design**: Automatic adaptation for mobile and desktop
- **Accessibility support**: ARIA attributes, keyboard navigation, semantic HTML
- **Customization**: CSS classes, custom themes, HtmlAttributes

### Key Dependencies

```ts
@syncfusion/ej2-navigations  // AppBar component
@syncfusion/ej2-base         // Base utilities
@syncfusion/ej2-buttons      // Button integration
@syncfusion/ej2-splitbuttons // DropDownButton support
```

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm package setup
- TypeScript and ES5 JavaScript approaches
- Basic AppBar initialization
- CSS imports and theme configuration
- Adding buttons and content
- First render and CDN references

### Positioning and Sticky Behavior
📄 **Read:** [references/positioning-and-sticky.md](references/positioning-and-sticky.md)
- Top AppBar (default positioning)
- Bottom AppBar positioning
- Sticky AppBar behavior (isSticky property)
- Use cases for each position
- Positioning property configuration
- ScrollView interaction

### Size and Height Modes
📄 **Read:** [references/size-and-height-modes.md](references/size-and-height-modes.md)
- Regular AppBar (default height)
- Prominent AppBar (larger height for titles/images)
- Dense AppBar (compact height)
- Height customization techniques
- When to use each mode
- CSS class application

### Color and Theme Modes
📄 **Read:** [references/color-and-theme-modes.md](references/color-and-theme-modes.md)
- Light AppBar (light background and text)
- Dark AppBar (dark background and text)
- Primary AppBar (primary brand colors)
- Inherit AppBar (inherit parent colors)
- Button inheritance with e-inherit CSS class
- Component integration (Buttons, Menu, DropDownButton)

### Styling and Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- CSS class selectors and purposes
- CssClass property for custom styling
- HtmlAttributes for ARIA labels and accessibility
- Custom theme creation
- Theme Studio integration
- CSS variable customization

### Layout Patterns and Design
📄 **Read:** [references/layout-patterns-and-design.md](references/layout-patterns-and-design.md)
- Spacer element (e-appbar-spacer) for content distribution
- Separator element (e-appbar-separator) for visual grouping
- Button and DropDownButton integration patterns
- Menu component integration
- Sidebar with TreeView integration
- Responsive design and media queries
- Complex navigation layouts

### Best Practices and Accessibility
📄 **Read:** [references/best-practices-and-accessibility.md](references/best-practices-and-accessibility.md)
- Semantic HTML structure
- ARIA attributes and accessibility
- Keyboard navigation support
- Color contrast and accessibility compliance
- Responsive breakpoints for mobile
- Performance optimization
- Common pitfalls and troubleshooting

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API documentation for all properties, methods, and events
- All 9 properties with type definitions (colorMode, cssClass, enablePersistence, enableRtl, htmlAttributes, isSticky, locale, mode, position)
- All 8 methods with parameters and return types (addEventListener, appendTo, dataBind, destroy, getRootElement, refresh, removeEventListener, inject)
- All 2 events with detailed examples (created, destroyed)
- State persistence across page reloads (enablePersistence)
- Internationalization and RTL support (locale, enableRtl)
- Event handling patterns and lifecycle management
- Complete working examples for all APIs

## Quick Start Example

### Basic AppBar Setup

**TypeScript:**
```ts
import { AppBar } from "@syncfusion/ej2-navigations";
import { Button } from "@syncfusion/ej2-buttons";

// Create AppBar with Primary color
const appbarObj: AppBar = new AppBar({
  colorMode: 'Primary'
});
appbarObj.appendTo("#appbar");

// Add buttons with inherited styling
const menuButton: Button = new Button({ 
  cssClass: 'e-inherit', 
  iconCss: 'e-icons e-menu' 
});
menuButton.appendTo('#menuBtn');

const loginButton: Button = new Button({ 
  cssClass: 'e-inherit', 
  content: 'Login' 
});
loginButton.appendTo('#loginBtn');
```

**HTML:**
```html
<!DOCTYPE html>
<html>
<head>
  <link href="url" rel="stylesheet" />
  <link href="url" rel="stylesheet" />
  <link href="url" rel="stylesheet" />
</head>
<body>
  <header id="appbar">
    <button id="menuBtn"></button>
    <div class="e-appbar-spacer"></div>
    <button id="loginBtn"></button>
  </header>
</body>
</html>
```

## Common Patterns

### Pattern 1: Navigation with Spacer
```ts
// Center title with left menu and right login
<header id="appbar">
  <button id="menu"></button>
  <span>My App</span>
  <div class="e-appbar-spacer"></div>
  <button id="login"></button>
</header>
```

### Pattern 2: Grouped Actions with Separator
```ts
// Edit actions | Format actions | Layout actions
<header id="appbar">
  <button id="cut"></button>
  <button id="copy"></button>
  <button id="paste"></button>
  <div class="e-appbar-separator"></div>
  <button id="bold"></button>
  <button id="italic"></button>
</header>
```

### Pattern 3: Prominent Header with Background
Use `mode: 'Prominent'` with background image for hero headers.

### Pattern 4: Sticky Navigation
Set `isSticky: true` for persistent header during scroll.

### Pattern 5: Bottom Navigation Bar
Set `position: 'Bottom'` for mobile-style bottom navigation.

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `colorMode` | 'Light' \| 'Dark' \| 'Primary' \| 'Inherit' | 'Light' | Sets background and text colors |
| `mode` | 'Regular' \| 'Prominent' \| 'Dense' | 'Regular' | Controls AppBar height |
| `position` | 'Top' \| 'Bottom' | 'Top' | Positions AppBar at top or bottom |
| `isSticky` | boolean | false | Makes AppBar stick during scroll |
| `cssClass` | string | '' | Applies custom CSS classes |
| `htmlAttributes` | object | {} | Sets HTML attributes (ARIA, etc.) |

## Common Use Cases

**Use Case 1: E-Commerce Header**
```ts
// Logo, navigation menu, search, cart, profile
// Sticky, Primary color, responsive layout with e-appbar-spacer
```

**Use Case 2: SPA Dashboard**
```ts
// Menu toggle, page title, notification icon, user dropdown
// Top positioned, Prominent mode for title
```

**Use Case 3: Mobile App Navigation**
```ts
// Bottom navigation bar with icons
// Dense mode, Bottom position, Light/Dark color mode
```

**Use Case 4: Document Editor**
```ts
// Grouped editing tools with separators
// Regular mode, Primary color, e-inherit buttons for consistency
```

**Use Case 5: Complex Dashboard with Sidebar**
```ts
// Menu toggle + AppBar at top + Sidebar below
// Sticky AppBar, responsive media queries
```

## Next Steps

1. **Get Started**: Read [Getting Started](references/getting-started.md) to set up your first AppBar
2. **Position Your Bar**: Choose position with [Positioning Guide](references/positioning-and-sticky.md)
3. **Select Size Mode**: Pick size with [Size Modes](references/size-and-height-modes.md)
4. **Apply Colors**: Set theme with [Color Modes](references/color-and-theme-modes.md)
5. **Style & Customize**: Customize look with [Styling](references/styling-customization.md)
6. **Design Layout**: Create complex patterns with [Layout Patterns](references/layout-patterns-and-design.md)
7. **Ensure Quality**: Follow [Best Practices](references/best-practices-and-accessibility.md)

---

**Control:** Syncfusion AppBar | **Platform:** TypeScript | **Version:** EJ2 32.1.19+
