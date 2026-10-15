---
name: syncfusion-angular-breadcrumb
description: Guide for implementing Syncfusion Angular Breadcrumb components for navigation trails. Covers installation, data binding, navigation setup, icons, overflow modes, and template customization. Use this when building breadcrumb navigation that displays user location in hierarchies, enables clicking parent items for navigation, adds icons for visual context, or customizes appearance with templates.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Angular Breadcrumb

The Breadcrumb component provides a navigation aid that displays the user's current location within a hierarchy of pages or sections. It offers clickable links to parent levels and visually represents the breadcrumb trail.

## When to Use This Skill

Use this skill when you need to:
- Implement breadcrumb navigation trails in Angular applications
- Display user location within page hierarchies
- Enable navigation to parent sections
- Add icons and visual enhancements to breadcrumb items
- Handle overflow with multiple display modes
- Customize breadcrumb appearance with templates
- Configure data binding for breadcrumb items

## Component Overview

The Syncfusion Angular Breadcrumb component (`ejs-breadcrumb`) is part of the `@syncfusion/ej2-angular-navigations` package. It displays a series of links in hierarchical order, with each item representing a navigation level. The component supports:

- **Multiple data binding approaches**: items as directives, URL-based, or static configuration
- **Icon support**: font icons, images, and SVG graphics
- **Navigation control**: enable/disable, open in new tabs, last-item navigation
- **Overflow handling**: 6 different modes for space-constrained layouts
- **Template customization**: item templates and separator customization
- **Event handling**: beforeItemRender for dynamic customization

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Module imports and enableRipple configuration
- Basic breadcrumb component rendering
- Adding items with e-breadcrumb-items directive
- Enabling and disabling navigation functionality
- CSS imports and theme application

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Items as tag directives with properties
- Generating items from current URL
- Static URL configuration for breadcrumb items
- Using the url property to bind navigation paths
- beforeItemRender event for customization
- Customizing generated item text

### Icons and Visual Enhancements
📄 **Read:** [references/icons-and-visuals.md](references/icons-and-visuals.md)
- Adding font icons using iconCss property
- Using image icons in breadcrumb items
- SVG icon implementation
- Icon positioning (left and right alignment)
- Icon-only items without text
- First-item-only icon patterns

### Navigation Configuration
📄 **Read:** [references/navigations.md](references/navigations.md)
- Relative URL configuration
- Absolute URL configuration
- enableNavigation property control
- enableActiveItemNavigation for last-item navigation
- Opening breadcrumb items in new tabs or pages
- Link target and navigation behavior

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All properties, methods, and events for breadcrumb
- BreadcrumbItemModel details
- BreadcrumbBeforeItemRenderEventArgs and BreadcrumbClickEventArgs
- Component methods like destroy

### Overflow Handling
📄 **Read:** [references/overflow-handling.md](references/overflow-handling.md)
- maxItems and overflowMode properties
- Collapsed mode for compact display
- Menu mode with dropdown submenus
- Wrap mode for multi-line layouts
- Scroll mode with horizontal scrollbar
- Hidden mode with dynamic visibility
- None mode for no overflow handling

### Templates and Customization
📄 **Read:** [references/templates-customization.md](references/templates-customization.md)
- itemTemplate for custom item rendering
- separatorTemplate for custom separators
- Custom separator icons and styling
- Conditional item templates
- Component integration (e.g., ChipList)
- Advanced CSS customization

## Quick Start Example

Basic breadcrumb with items and navigation:

```ts
import { BreadcrumbModule } from '@syncfusion/ej2-angular-navigations';
import { Component } from '@angular/core';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

@Component({
  imports: [BreadcrumbModule],
  standalone: true,
  selector: 'app-root',
  template: `<div class="e-section-control">
    <ejs-breadcrumb [enableNavigation]="true">
      <e-breadcrumb-items>
        <e-breadcrumb-item iconCss="e-icons e-home" url="url"></e-breadcrumb-item>
        <e-breadcrumb-item text="Products" url="url"></e-breadcrumb-item>
        <e-breadcrumb-item text="Electronics" url="url"></e-breadcrumb-item>
        <e-breadcrumb-item text="Laptops" url="url"></e-breadcrumb-item>
      </e-breadcrumb-items>
    </ejs-breadcrumb>
  </div>`
})
export class AppComponent {}
```

## Common Patterns

### Disable Navigation
Set `enableNavigation="false"` to prevent clicking items:
```html
<ejs-breadcrumb [enableNavigation]="false">
  <e-breadcrumb-items>
    <e-breadcrumb-item text="Home"></e-breadcrumb-item>
  </e-breadcrumb-items>
</ejs-breadcrumb>
```

### Add Icons to Items
Use `iconCss` with Syncfusion icon classes:
```html
<e-breadcrumb-item iconCss="e-icons e-home" text="Home"></e-breadcrumb-item>
```

### Handle Overflow
Use `maxItems` and `overflowMode` for space-constrained layouts:
```html
<ejs-breadcrumb [maxItems]="3" overflowMode="Menu">
```

### Enable Last Item Navigation
Allow clicking the active/last item:
```html
<ejs-breadcrumb [enableActiveItemNavigation]="true">
```

### Customize Separators
Replace default separators with custom icons:
```html
<ng-template #separatorTemplate>
  <span class='e-bicons e-arrow'></span>
</ng-template>
```

## Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `items` | Array | - | Array of BreadcrumbItemModel items |
| `url` | String | - | Static URL to generate items from path |
| `enableNavigation` | Boolean | true | Enable/disable item click navigation |
| `enableActiveItemNavigation` | Boolean | false | Allow clicking the active/last item |
| `maxItems` | Number | - | Maximum items to display before overflow |
| `overflowMode` | String | 'Menu' | Overflow handling mode |
| `itemTemplate` | Template | - | Template for custom item rendering |
| `separatorTemplate` | Template | - | Template for custom separators |
| `cssClass` | String | - | CSS class for styling |
| `beforeItemRender` | Event | - | Event before item rendering |

## Common Use Cases

1. **E-commerce Navigation**: Show product hierarchy (Home > Categories > Subcategory > Product)
2. **File System Browser**: Display folder path with accessible parent folders
3. **Documentation Site**: Breadcrumb trail through documentation hierarchy
4. **Blog Navigation**: Show post category and current article location
5. **Admin Dashboard**: Display section and subsection location
6. **Multi-step Forms**: Show form progress and completion steps

---

**Next Steps:**
- Read getting-started.md to set up the breadcrumb component
- Choose a data binding approach from data-binding.md
- Enhance with icons from icons-and-visuals.md
- Configure navigation from navigations.md
- Handle overflow with overflow-handling.md
- Customize templates from templates-customization.md
