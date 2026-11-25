---
name: syncfusion-aspnetcore-breadcrumb
description: Display hierarchical navigation paths with the ASP.NET Core Breadcrumb control. Use this skill when implementing breadcrumb navigation, handling item binding, configuring overflow behavior, or customizing templates and icons.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Breadcrumb Navigation in ASP.NET Core

The Breadcrumb component displays a hierarchical navigation path that helps users understand their location within your application. It enables navigation through parent pages and supports flexible data binding, templates, icons, and overflow handling.

## When to Use This Skill

Use this skill when you need to:
- Display a hierarchical navigation breadcrumb in your ASP.NET Core application
- Bind breadcrumb items from a collection or generate them from the current URL
- Customize breadcrumb appearance using templates, icons, or CSS classes
- Handle breadcrumb item clicks and render events
- Implement overflow behavior for long breadcrumb trails
- Support RTL rendering or disable specific items

## Component Overview

The Breadcrumb component is a navigation UI element that:
- Shows the current page position in a hierarchical structure
- Allows users to navigate to parent-level pages
- Renders items with optional icons, templates, and separators
- Supports multiple overflow modes (Collapsed, Hidden, Menu, Wrap, Scroll, None)
- Triggers events for item rendering and clicks
- Works with ASP.NET Core TagHelper syntax

**Key Properties:**
- `items` - Array of BreadcrumbItem objects to display
- `url` - Automatically generate items from a URL path
- `activeItem` - Mark a specific item as currently active
- `enableNavigation` - Control whether items are navigable
- `overflowMode` + `maxItems` - Handle long breadcrumb trails
- `itemTemplate` + `separatorTemplate` - Customize rendering

**Key Events:**
- `beforeItemRender` - Fires before each item renders (for customization)
- `itemClick` - Fires when a breadcrumb item is clicked
- `created` - Fires after the component is fully initialized

## Documentation and Navigation Guide

Choose the reference file that matches your implementation need:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Setting up Syncfusion.EJ2.AspNet.Core package
- Registering TagHelper and adding resources
- Creating your first breadcrumb control
- Binding items collection
- Controlling item navigation

### Data Binding and Items
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding items using e-breadcrumb-items tag directive
- Generating items from the current page URL
- Generating items from a static URL
- Using beforeItemRender to customize generated items
- Dynamic item binding patterns

### Navigation and URLs
📄 **Read:** [references/navigation.md](references/navigation.md)
- Defining relative and absolute URLs
- Enabling navigation for the active (last) item
- Controlling which items trigger navigation
- Using beforeItemRender for URL manipulation
- Handling navigation events with itemClick

### Icons and Visual Elements
📄 **Read:** [references/icons.md](references/icons.md)
- Adding font icons with iconCss property
- Using image files as icons
- Displaying SVG icons
- Positioning icons (left vs. right)
- Combining icons with item text

### Templates and Customization
📄 **Read:** [references/templates.md](references/templates.md)
- Customizing item appearance with itemTemplate
- Customizing separators with separatorTemplate
- Using conditional logic in templates
- Integrating other components (like chips) in templates
- Template event binding patterns

### Overflow and Responsive Display
📄 **Read:** [references/overflow-modes.md](references/overflow-modes.md)
- Understanding overflow modes and maxItems
- Collapsed mode (shows first/last only)
- Hidden mode (progressive reveal)
- Menu mode (submenu overflow)
- Wrap mode (multiple lines)
- Scroll mode (HTML scrollbar)
- None mode (single line, no truncation)

### Advanced Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Applying CSS classes to the component
- RTL (right-to-left) rendering
- Disabling items and the component
- Persisting breadcrumb state
- Using beforeItemRender for advanced customization

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All properties, methods, and events
- Event argument structures
- Overflow mode enumeration
- Examples for less-covered APIs

## Quick Start Example

Here's a minimal breadcrumb implementation:

```cshtml
<!-- In _Layout.cshtml or _ViewImports.cshtml -->
@addTagHelper *, Syncfusion.EJ2

<!-- In your page (e.g., Index.cshtml) -->
<ejs-breadcrumb>
    <e-breadcrumb-items>
        <e-breadcrumb-item text="Home" url="~/"></e-breadcrumb-item>
        <e-breadcrumb-item text="Products" url="~/products"></e-breadcrumb-item>
        <e-breadcrumb-item text="Electronics" url="~/products/electronics"></e-breadcrumb-item>
        <e-breadcrumb-item text="Laptops"></e-breadcrumb-item>
    </e-breadcrumb-items>
</ejs-breadcrumb>
```

**What this does:**
- Renders 4 breadcrumb items
- First 3 items are navigable (have URLs)
- Last item (Laptops) is the current page, not navigable
- Breadcrumb displays: Home > Products > Electronics > Laptops

## Common Patterns

### Pattern 1: URL-Based Generation
Let the Breadcrumb automatically generate items from the page URL:

```cshtml
<ejs-breadcrumb url="https://example.com/products/electronics/laptops">
</ejs-breadcrumb>
```

**When to use:** When you want automatic breadcrumbs that follow the URL structure.

### Pattern 2: Controlling Navigation
Disable navigation entirely or only for the active item:

```cshtml
<ejs-breadcrumb enableNavigation="false">
    <!-- Items won't be clickable -->
</ejs-breadcrumb>

<ejs-breadcrumb enableActiveItemNavigation="true">
    <!-- Last item becomes clickable when URL is set -->
</ejs-breadcrumb>
```

### Pattern 3: Handling Overflow
Use overflow modes for long breadcrumb trails:

```cshtml
<ejs-breadcrumb overflowMode="Collapsed" maxItems="3">
    <!-- Only first/last shown, others hidden in icon -->
</ejs-breadcrumb>
```

### Pattern 4: Item Click Handling
Respond to item clicks with the itemClick event:

```cshtml
<ejs-breadcrumb itemClick="OnBreadcrumbItemClick">
    <e-breadcrumb-items>
        <e-breadcrumb-item text="Home" url="~/"></e-breadcrumb-item>
        <e-breadcrumb-item text="Dashboard" url="~/dashboard"></e-breadcrumb-item>
    </e-breadcrumb-items>
</ejs-breadcrumb>
```

In your C# handler:
```csharp
public void OnBreadcrumbItemClick(BreadcrumbClickEventArgs args)
{
    // Handle item click
    var clickedItem = args.Item;
}
```

## Key Properties Summary

| Property | Type | Purpose |
|----------|------|---------|
| `items` | BreadcrumbItemModel[] | Collection of breadcrumb items to display |
| `url` | string | Auto-generate items from a URL path |
| `activeItem` | string | URL/identifier of the currently active item |
| `enableNavigation` | boolean | Allow/prevent item navigation (default: true) |
| `enableActiveItemNavigation` | boolean | Make the last item navigable (default: false) |
| `maxItems` | number | Threshold for triggering overflow behavior |
| `overflowMode` | string | How to display items beyond maxItems (Collapsed, Hidden, Menu, Wrap, Scroll, None) |
| `itemTemplate` | string \| Function | Custom template for item rendering |
| `separatorTemplate` | string \| Function | Custom template for separators |
| `enableRtl` | boolean | Render right-to-left (default: false) |
| `disabled` | boolean | Disable the entire component (default: false) |
| `cssClass` | string | Apply CSS classes to the component |
| `enablePersistence` | boolean | Persist component state between page reloads |

## Common Use Cases

**Use Case 1: E-Commerce Breadcrumb**
Navigate through product categories: Home > Electronics > Laptops > Gaming Laptops

**Use Case 2: File Browser**
Show file path: Root > Documents > Projects > MyProject

**Use Case 3: Multi-Step Form**
Indicate form progress: Step 1 > Step 2 > Step 3 (Current)

**Use Case 4: Documentation Site**
Navigate documentation hierarchy: Docs > API > Components > Breadcrumb

**Use Case 5: Admin Dashboard**
Show user path: Dashboard > Users > Admin > Edit Profile

---

## Next Steps

1. **Get Started:** Follow [Getting Started](references/getting-started.md) for installation and basic setup
2. **Bind Data:** Use [Data Binding](references/data-binding.md) to connect breadcrumb items
3. **Customize:** Explore [Templates](references/templates.md) and [Icons](references/icons.md) for personalization
4. **Optimize:** Handle long trails with [Overflow Modes](references/overflow-modes.md)
5. **Reference:** Check [API Reference](references/api-reference.md) for complete API details

For detailed implementation patterns, event handling, and advanced scenarios, see the corresponding reference files.
