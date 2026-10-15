---
name: syncfusion-aspnetcore-context-menu
description: Implement Syncfusion ContextMenu component in ASP.NET Core applications to display contextual menus triggered by right-click or programmatic actions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion ContextMenu

## When to Use This Skill

Use the ContextMenu component when you need to:
- **Display context-sensitive menus** triggered by right-click or long-touch on target elements
- **Create nested multi-level menus** with hierarchical menu item structures
- **Add icons and visual indicators** to menu items using CSS icon classes
- **Implement navigation links** within menu items to route to different pages
- **Handle menu item selection** with programmatic or event-driven logic
- **Customize menu appearance** with CSS classes, templates, and animations
- **Support keyboard navigation** for accessible menu interactions
- **Enable scrollable menus** for large numbers of menu items exceeding viewport
- **Apply animations** to submenu transitions with multiple effect options
- **Persist component state** between page reloads and maintain locale customization
- **Support RTL (right-to-left) rendering** for international applications
- **Render custom item templates** for complex menu item layouts beyond simple text

## Component Overview

The Syncfusion ContextMenu is a lightweight navigation component that displays a list of commands or menu items in response to user interactions, typically a right-click on a target element. It provides:

- **Target-Based Triggering**: Attach context menu to specific DOM elements via CSS selector
- **Multi-Level Nesting**: Support for submenu items nested within parent menu items  
- **Icon Support**: Apply CSS icon classes (e.g., e-icons, Font Awesome) to menu items
- **Navigation Integration**: Direct navigation via URL property on menu items
- **Rich Animations**: Multiple transition effects (SlideDown, ZoomIn, FadeIn, None) with configurable duration
- **Scrollable Content**: Enable vertical scrolling for menus exceeding viewport height
- **Template Customization**: Define custom HTML templates for complex menu item layouts
- **Event System**: Capture menu lifecycle events (beforeOpen, onOpen, select, beforeClose, onClose)
- **Item Rendering Hooks**: Use beforeItemRender event to customize individual items per render
- **Selector Filtering**: Filter target elements within a container using CSS selector patterns
- **Hover Delay**: Configure delay duration before submenu appears on hover
- **State Persistence**: Automatically restore component state on page reloads
- **Locale Support**: Override global culture for component-specific localization
- **RTL Support**: Automatic right-to-left rendering for RTL languages
- **HTML Sanitization**: Optional sanitization of untrusted HTML content in menu items
- **Submenu Behavior**: Control whether submenus open on hover or click-only

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and ASP.NET Core project setup
- NuGet package installation (Syncfusion.EJ2.AspNet.Core)
- TagHelper registration in _ViewImports.cshtml
- Stylesheet and script resource references
- Script Manager registration
- Basic ContextMenu implementation with target element
- Rendering first context menu with simple menu items
- Initial data binding with items property

### Menu Items and Data Binding
📄 **Read:** [references/menu-items-and-data-binding.md](references/menu-items-and-data-binding.md)
- MenuItem structure and required properties (text, id)
- Data binding patterns using List and JSON objects
- Menu item properties: text, id, separator, iconCss, items, url
- Creating single-level and multi-level nested menus
- Separator usage for visual grouping (separator: true)
- Dynamic menu item updates and modifications
- Local data source patterns and data transformation

### Icons, Navigation, and Customization
📄 **Read:** [references/icons-navigation-customization.md](references/icons-navigation-customization.md)
- iconCss property for adding icons to menu items
- e-icons CSS class for Syncfusion built-in icons
- URL property for navigation links in menu items
- Creating action vs navigation menu items
- Custom CSS classes for styling menu items (cssClass property)
- Hover delay configuration (hoverDelay property)
- Filter selector for target element matching (filter property)

### Animation and Scrolling
📄 **Read:** [references/animation-scrolling.md](references/animation-scrolling.md)
- animationSettings configuration for submenu transitions
- Animation effects: None, SlideDown, ZoomIn, FadeIn
- Duration and easing properties for animation timing
- enableScrolling property for handling large menu lists
- Vertical scrolling behavior for overflow menu items
- BeforeOpen event for dynamic menu height adjustment
- Performance considerations for scrollable menus

### Templates and Custom Rendering
📄 **Read:** [references/templates-customization.md](references/templates-customization.md)
- itemTemplate property for custom menu item layouts
- beforeItemRender event for individual item customization
- Rendering custom HTML within menu items
- Adding UI components (checkboxes, inputs) to menu items
- Event arguments in beforeItemRender (name property in MenuEventArgs)
- Dynamic item HTML generation based on data
- CSS customization through rendered elements

### Event Handling and Integration
📄 **Read:** [references/event-handling.md](references/event-handling.md)
- select event for menu item selection/click handling
- beforeOpen event triggered before submenu opens
- beforeClose event triggered before menu closes
- onOpen event triggered when submenu is opened
- onClose event triggered when menu closes
- beforeItemRender event for render-time customization
- created event indicating component initialization complete
- Event-driven menu operations and conditional logic

---

## Quick Start Example

**Razor Markup (Index.cshtml):**
```html
@page
@model IndexModel

<div id="target">Right-click me</div>

<ejs-contextmenu id="contextmenu" target="#target" items="Model.MenuItems"></ejs-contextmenu>
```

**PageModel (Index.cshtml.cs):**
```csharp
public class IndexModel : PageModel
{
    public List<object> MenuItems { get; set; }
    
    public void OnGet()
    {
        MenuItems = new List<object>
        {
            new { text = "Cut", id = "cut", iconCss = "e-icons e-cut" },
            new { text = "Copy", id = "copy", iconCss = "e-icons e-copy" },
            new { text = "Paste", id = "paste", iconCss = "e-icons e-paste" },
            new { separator = true },
            new { 
                text = "Font", 
                id = "font",
                items = new List<object>
                {
                    new { text = "Bold", id = "bold" },
                    new { text = "Italic", id = "italic" }
                }
            }
        };
    }
}
```

---

## Common Patterns

| Pattern | Use Case | Reference |
|---------|----------|-----------|
| **Right-Click Menu** | Context menu triggered by mouse right-click | [getting-started.md](references/getting-started.md) |
| **Hierarchical Items** | Multi-level nested menu structure | [menu-items-and-data-binding.md](references/menu-items-and-data-binding.md) |
| **Icon Support** | Menu items with visual icons | [icons-navigation-customization.md](references/icons-navigation-customization.md) |
| **Navigation Links** | Menu items as navigation shortcuts | [icons-navigation-customization.md](references/icons-navigation-customization.md) |
| **Animated Transitions** | Submenu appearance effects | [animation-scrolling.md](references/animation-scrolling.md) |
| **Scrollable Menus** | Large menu lists with overflow | [animation-scrolling.md](references/animation-scrolling.md) |
| **Custom Templates** | Complex item layouts | [templates-customization.md](references/templates-customization.md) |
| **Selection Handling** | React to item selection | [event-handling.md](references/event-handling.md) |
| **Hover Delay** | Control submenu timing | [icons-navigation-customization.md](references/icons-navigation-customization.md) |
| **RTL Support** | Right-to-left language rendering | [getting-started.md](references/getting-started.md) |

---

## Key Properties

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `target` | string | CSS selector for target element | "#menuTarget" or ".menu-area" |
| `items` | MenuItemModel[] | Array of menu item definitions | List of objects with text, id properties |
| `animationSettings` | MenuAnimationSettingsModel | Submenu open animation config | effect: "ZoomIn", duration: 500 |
| `enableScrolling` | boolean | Enable vertical scrolling for overflow | true for large menus |
| `hoverDelay` | number | Delay in ms before submenu opens on hover | 500 |
| `showcItemOnClick` | boolean | Submenu opens only on click | true to disable hover opening |
| `itemTemplate` | string or Function | Custom HTML template for items | HTML string or callback function |
| `cssClass` | string | CSS class for menu wrapper styling | "custom-context-menu dark-theme" |
| `filter` | string | CSS selector to filter target elements | ".menu-enabled" |
| `enableRtl` | boolean | Right-to-left rendering | true |
| `enablePersistence` | boolean | Preserve state on page reload | true |
| `locale` | string | Component locale override | "fr-FR" |
| `enableHtmlSanitizer` | boolean | Sanitize untrusted HTML | true (recommended for user content) |

---

## Common Use Cases

**1. File Manager Context Menu**
Attach context menu to file list for Cut, Copy, Paste, Delete, Rename operations with icons.

**2. Text Editor Toolbar**
Provide right-click access to formatting options (Bold, Italic, Underline) and text manipulation.

**3. Data Grid Row Actions**
Context menu on grid rows for Edit, View, Delete, Export operations on selected rows.

**4. Navigation Shortcuts**
Quick access menu providing links to different application sections or external resources.

**5. Multi-Language Support**
Configure locale-specific formatting and override default culture for globalized applications.

---

## Next Steps

- Review the **API Reference** for complete property and method documentation
- Combine ContextMenu with other navigation components (Toolbar, Sidebar) for comprehensive UI
- Implement keyboard shortcuts alongside context menu for enhanced accessibility
- Test RTL rendering if targeting international audiences
- Consider performance implications when rendering large menu lists (>100 items)

