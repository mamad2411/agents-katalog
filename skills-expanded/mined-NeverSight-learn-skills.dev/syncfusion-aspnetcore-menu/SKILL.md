---
name: syncfusion-aspnetcore-menu
description: Implement Syncfusion Core Menu component to display hierarchical navigational menus with support for data binding, icons, animations, and rich event handling for user interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Menu Component

When you need to build a navigational menu system with hierarchical items, icons, animations, and event handling, this skill provides complete guidance for using the Syncfusion Core Menu component.

## When to Use This Skill

Use this skill when you need to:
- Display hierarchical navigation menus with nested items
- Bind menu data from arrays or self-referential structures
- Customize menu appearance with icons, animations, and styling
- Handle user interactions (click, selection, open/close)
- Support accessibility features (RTL, hamburger mode, scrolling)
- Create responsive menu layouts with dynamic item management

## Component Overview

The Menu is a graphical user interface component that serves as a navigation header for applications or sites. It supports:

- **Data Binding**: Hierarchical or self-referential data structures
- **Customization**: Icons, templates, animations, styling via CSS
- **User Interaction**: Events for open, close, select, and item render
- **Accessibility**: RTL support, persistence, keyboard navigation
- **Advanced Features**: Hamburger mode, scrolling, hover effects

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Creating your first menu
- Basic item structure (hierarchical)
- CSS imports and themes
- TagHelper syntax fundamentals

### Menu Items and Data Binding
📄 **Read:** [references/menu-items-and-data-binding.md](references/menu-items-and-data-binding.md)
- Item structure (MenuItemModel)
- Items property with inline arrays
- Hierarchical data binding
- Self-referential data structure
- FieldSettings mapping for custom data

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- cssClass property for custom styling
- Theme customization
- Template support for advanced layouts
- Menu item styling patterns
- Animation configuration

### Icons, Sub-menus, and Hierarchy
📄 **Read:** [references/icons-submenus-and-hierarchy.md](references/icons-submenus-and-hierarchy.md)
- Adding icons with iconCss
- Creating sub-menus with nested items
- Multi-level hierarchies
- Separator items
- Organizing complex menu structures

### Events and User Interactions
📄 **Read:** [references/events-and-user-interactions.md](references/events-and-user-interactions.md)
- Event names: beforeOpen, beforeClose, onOpen, onClose, select, beforeItemRender, created
- Event handler patterns
- BeforeOpenCloseMenuEventArgs properties
- OpenCloseMenuEventArgs properties
- MenuEventArgs properties
- Conditional logic in events

### Methods and Public API
📄 **Read:** [references/methods-and-public-api.md](references/methods-and-public-api.md)
- Lifecycle methods (appendTo, refresh, destroy, dataBind)
- Item management (enableItems, hideItems, showItems, setItem, getItemIndex)
- Item insertion/removal (insertAfter, insertBefore, removeItems)
- Hamburger mode control (open, close)
- Event handling (addEventListener, removeEventListener)
- Module injection (Inject)
- Practical implementation patterns
- Best practices for method usage

### Orientation and Accessibility
📄 **Read:** [references/orientation-and-accessibility.md](references/orientation-and-accessibility.md)
- Horizontal vs Vertical orientation
- RTL (enableRtl) support
- Hamburger mode for responsive design
- Persistence (enablePersistence)
- Scrolling (enableScrolling) for large menus
- HTML sanitization (enableHtmlSanitizer)

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property reference
- Event declarations
- MenuAnimationSettingsModel options
- FieldSettingsModel configuration
- MenuItem properties
- Enum values (Orientation, MenuEffect)

## Quick Start Example

Create a basic menu with three vertical items:

```html
@{
    List<object> menuItems = new List<object>();
    menuItems.Add(new { text = "File" });
    menuItems.Add(new { text = "Edit" });
    menuItems.Add(new { text = "View" });
}

<ejs-menu id="menu" items="menuItems"></ejs-menu>
```

With sub-menus:

```html
@{
    var menuItems = new List<object> {
        new {
            text = "File",
            items = new List<object> {
                new { text = "New" },
                new { text = "Open" },
                new { text = "Save" }
            }
        },
        new {
            text = "Edit",
            items = new List<object> {
                new { text = "Cut" },
                new { text = "Copy" },
                new { text = "Paste" }
            }
        }
    };
}

<ejs-menu id="menu" items="menuItems"></ejs-menu>
```

## Common Patterns

### Pattern 1: Data Binding with Fields Mapping
When you have custom data structures, map fields using the `fields` property:

```html
<ejs-menu id="menu" items="ViewBag.menuData" fields="ViewBag.menuFields"></ejs-menu>
```

Controller:
```csharp
var menuFields = new { text = "name", children = "submenu", iconCss = "icon" };
```

### Pattern 2: Event Handling
Attach event handlers to respond to user interactions:

```html
<ejs-menu id="menu" 
    items="menuItems"
    select="onMenuSelect"
    beforeOpen="onBeforeOpen">
</ejs-menu>
```

### Pattern 3: Horizontal Menu with Icons
Create a horizontal menu with icon support:

```html
<ejs-menu id="menu" 
    items="menuItems"
    orientation="Horizontal"
    enableRtl="false">
</ejs-menu>
```

### Pattern 4: RTL and Accessibility
Enable accessibility features for different locales:

```html
<ejs-menu id="menu" 
    items="menuItems" 
    locale="ar-AE"
    enableRtl="true"
    enablePersistence="true">
</ejs-menu>
```

## Key Properties Summary

| Property | Type | Purpose |
|----------|------|---------|
| `items` | MenuItemModel[] | Menu items array |
| `orientation` | Orientation | Horizontal or Vertical (default: Vertical) |
| `fields` | FieldSettingsModel | Data binding field mappings |
| `cssClass` | string | Custom CSS class for styling |
| `enableRtl` | boolean | Right-to-left text direction |
| `enablePersistence` | boolean | Persist state between page reloads |
| `enableScrolling` | boolean | Enable scrolling for overflow content |
| `hamburgerMode` | boolean | Responsive mobile menu mode |
| `animationSettings` | MenuAnimationSettingsModel | Sub-menu animation configuration |
| `hoverDelay` | number | Milliseconds before sub-menu opens on hover |
| `template` | string \| Function | Custom item template |

## Common Use Cases

**Navigation Header**: Create a multi-level site navigation menu with icons and styling

**Application Menu Bar**: Implement traditional File/Edit/View menu bar with keyboard support

**Mobile Navigation**: Use hamburger mode for responsive mobile navigation

**Contextual Menu**: Display dynamic menus based on user actions and data

**Localized Menu**: Support multiple languages and RTL layouts

---

**Next Steps:** Select a reference file above based on your needs. Start with getting-started.md if you're new to the Menu component.
