---
name: syncfusion-aspnetcore-sidebar
description: |
  Implement the Syncfusion ASP.NET Core Sidebar component to create responsive, collapsible navigation containers 
  that adapt seamlessly to mobile and desktop layouts.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion ASP.NET Core Sidebar

The Sidebar component is an expandable or collapsible navigation container that acts as a side panel to display 
primary or secondary content alongside the main content area. It provides flexible positioning, multiple expansion 
types, and responsive behavior ideal for modern web applications.

## When to Use This Skill

Use this skill when you need to:

- **Create responsive navigation menus** that collapse on mobile and expand on desktop
- **Implement collapsible sidebars** with smooth animations and transitions
- **Build docked sidebar panels** that reserve persistent space with icon-only views
- **Handle sidebar state management** with open/close methods and event callbacks
- **Customize sidebar behavior** with media queries, gestures, and backdrop overlays
- **Integrate with ASP.NET Core applications** using TagHelper syntax and server-side binding

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- ASP.NET Core project creation with Razor pages
- TagHelper registration in _ViewImports.cshtml
- Adding CSS/script resources via CDN or local
- First working sidebar implementation
- Script manager registration

### Understanding Sidebar Types
📄 **Read:** [references/sidebar-types.md](references/sidebar-types.md)
- Sidebar type enumeration (Over, Push, Slide, Auto)
- Over type: floating sidebar above content
- Push type: sidebar pushes main content aside
- Slide type: sidebar slides without resizing content
- Auto type: responsive type selection by screen resolution
- Changing types at runtime with dataBind()
- Type selection best practices

### Managing Sidebar State
📄 **Read:** [references/managing-state.md](references/managing-state.md)
- isOpen property for initial state
- show() method to open the sidebar programmatically
- hide() method to close the sidebar
- toggle() method for open/close switching
- Controlling sidebar from button clicks
- State initialization and persistence
- Toggle patterns with UI buttons

### Positioning and Sizing
📄 **Read:** [references/positioning-and-sizing.md](references/positioning-and-sizing.md)
- position property (Left or Right placement)
- width property for custom sidebar dimensions
- target property for custom context targeting
- Placing sidebar inside specific containers
- Responsive sizing strategies
- Width in pixels vs auto-sizing
- Multiple sidebars in different positions

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- enableDock property for docked state mode
- dockSize configuration for reserved space
- closeOnDocumentClick for dismiss-on-click behavior
- showBackdrop overlay when sidebar is open
- enableGestures for touch swipe control
- mediaQuery for responsive breakpoint control
- enablePersistence for state preservation across page reloads

### Events and Callbacks
📄 **Read:** [references/events-and-callbacks.md](references/events-and-callbacks.md)
- change event: fires on expand/collapse state changes
- open event: fires when sidebar opens
- close event: fires when sidebar closes
- created event: fires on component initialization
- destroyed event: fires on component destruction
- ChangeEventArgs structure with event details
- EventArgs properties for event handling
- Binding events with TagHelper syntax

### Internationalization and RTL
📄 **Read:** [references/internationalization.md](references/internationalization.md)
- enableRtl property for right-to-left layouts
- RTL sidebar positioning (right-aligned by default)
- Mirror positioning and alignment
- RTL animation and positioning behavior
- Multi-language sidebar content
- Combining RTL with positioning properties

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- animate property to enable/disable transitions
- zIndex property for layering control with overlays
- CSS class customization and theming
- Backdrop styling and opacity
- Animation duration and easing configuration
- Theme integration
- Custom styling best practices

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All 15 properties with types and defaults
- All 11 methods with signatures and descriptions
- All 5 events with their argument types
- Type enumerations (SidebarType, SidebarPosition)
- Event argument structures (ChangeEventArgs, EventArgs)
- Cross-references to feature documentation
- Usage examples for each API

## Quick Start Example

Here's a minimal Sidebar implementation with a toggle button:

```cshtml
<ejs-sidebar id="default-sidebar" type="Push" isOpen="false">
    <e-content-template>
        <div style="padding: 20px;">
            <h3>Sidebar Menu</h3>
            <p>Navigation items go here</p>
        </div>
    </e-content-template>
</ejs-sidebar>

<div style="padding: 20px;">
    <ejs-button id="toggleBtn" content="Toggle Sidebar" onclick="toggleSidebar()"></ejs-button>
    <h2>Main Content</h2>
    <p>Your page content appears here</p>
</div>

<script>
var sidebar;

document.addEventListener('DOMContentLoaded', function () {
    sidebar = document.getElementById('default-sidebar').ej2_instances[0];
});

function toggleSidebar() {
    sidebar.toggle();
}
</script>
```

## Common Patterns

### Pattern 1: Mobile-Responsive Navigation
Use `type="Auto"` to automatically switch between Over (mobile) and Push (desktop) based on screen resolution:

```cshtml
<ejs-sidebar id="navbar" type="Auto" isOpen="false">
    <!-- Navigation items -->
</ejs-sidebar>
```

### Pattern 2: Docked Sidebar with Icons
Enable docking with reserved space for icon-only view:

```cshtml
<ejs-sidebar id="dockedbar" 
             enableDock="true" 
             dockSize="60px" 
             type="Push">
    <!-- Icon items -->
</ejs-sidebar>
```

### Pattern 3: Backdrop with Overlay
Show content overlay when sidebar opens:

```cshtml
<ejs-sidebar id="overlaybar" 
             type="Over" 
             showBackdrop="true" 
             closeOnDocumentClick="true">
    <!-- Content -->
</ejs-sidebar>
```

### Pattern 4: Right-Positioned Sidebar
Place sidebar on the right side:

```cshtml
<ejs-sidebar id="rightbar" position="Right" type="Push">
    <!-- Right-side navigation -->
</ejs-sidebar>
```

### Pattern 5: Custom Width Sidebar
Set specific width in pixels:

```cshtml
<ejs-sidebar id="custombar" type="Push" width="320px">
    <!-- Content with 320px width -->
</ejs-sidebar>
```

## Key Properties Overview

| Property | Type | Purpose |
|----------|------|---------|
| `type` | SidebarType | Controls how sidebar expands (Over/Push/Slide/Auto) |
| `position` | SidebarPosition | Sidebar placement (Left/Right) |
| `isOpen` | boolean | Initial open/closed state |
| `width` | string/number | Sidebar width ('auto', '300px', or number) |
| `enableDock` | boolean | Enables docked state mode |
| `dockSize` | string/number | Width when docked ('auto', '60px', or number) |
| `animate` | boolean | Enable/disable expansion animations |
| `enableGestures` | boolean | Enable touch swipe to expand/collapse |
| `mediaQuery` | string | CSS media query for responsive behavior |
| `showBackdrop` | boolean | Show overlay when sidebar is open |
| `closeOnDocumentClick` | boolean | Close sidebar when clicking outside |
| `enableRtl` | boolean | Right-to-left layout support |
| `zIndex` | string/number | Layering for overlay mode (default: 1000) |
| `target` | HTMLElement/string | Container for sidebar (custom context) |
| `enablePersistence` | boolean | Preserve state across page reloads |

## Common Use Cases

- **Admin Dashboards**: Multi-section dashboards with collapsible navigation
- **E-Commerce Sites**: Filter sidebars that collapse on mobile
- **Documentation Sites**: Table of contents sidebars
- **Application Menus**: Docked icon-based navigation that expands on hover
- **Mobile Apps**: Hamburger menus that slide from the side
- **Content Management**: Expandable editor sidebars
- **Data Tables**: Filtering and column selection sidebars

## Next Steps

1. **Start with [Getting Started](references/getting-started.md)** to install and configure
2. **Choose your [Sidebar Type](references/sidebar-types.md)** based on your layout needs
3. **Learn [State Management](references/managing-state.md)** to control open/close behavior
4. **Explore [Advanced Features](references/advanced-features.md)** for docking and responsiveness
5. **Reference [Complete API](references/api-reference.md)** for all properties and methods

---

## Component Overview

The Sidebar component is built on the Syncfusion EJ2 framework and provides:
- Four expansion types with automatic responsive selection
- Touch gesture support for mobile devices
- State persistence across page reloads
- Event system for open/close/change lifecycle
- Customizable positioning and sizing
- Backdrop overlay for modal-like behavior
- RTL and internationalization support
- Smooth animations and transitions
- Full TagHelper integration with ASP.NET Core

For detailed implementation examples and advanced scenarios, refer to the reference guides above.
