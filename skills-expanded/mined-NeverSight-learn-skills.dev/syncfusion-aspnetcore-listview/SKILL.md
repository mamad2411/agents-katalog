---
name: syncfusion-aspnetcore-listview
description: Master the Syncfusion ListView component for ASP.NET Core to create interactive, data-bound lists with advanced features like grouping, virtualization, templates, and nested navigation.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing ListView in ASP.NET Core

The ListView component is a powerful, feature-rich control that displays data in interactive hierarchical structures. It supports data binding (local and remote), grouping, nested lists, custom templates, virtualization for performance, and comprehensive keyboard accessibility.

## When to Use This Skill

Use this skill when you need to:

- **Display Interactive Lists**: Render data collections with click selection, hover effects, and visual feedback
- **Group Related Items**: Organize list items into categories using the `groupBy` field
- **Support Nested Navigation**: Create multi-level hierarchies with parent-child relationships
- **Optimize Performance**: Handle large datasets (1000+ items) with UI virtualization
- **Customize Appearance**: Apply templates for headers, items, and group titles
- **Enable Selection**: Implement single or multi-select with checkboxes
- **Handle Remote Data**: Bind to server APIs with DataManager and Query
- **Implement Keyboard Access**: Support keyboard navigation for accessibility

## Component Overview

The ListView component in Syncfusion EJ2 for ASP.NET Core uses **TagHelper syntax** and exposes core properties:

| Category | Key Properties |
|----------|----------------|
| **Data Binding** | `dataSource`, `fields`, `query` |
| **Display Control** | `template`, `headerTemplate`, `groupTemplate` |
| **User Interaction** | `showCheckBox`, `checkBoxPosition`, `sortOrder` |
| **Performance** | `enableVirtualization`, `height` |
| **Appearance** | `cssClass`, `width`, `showHeader`, `showIcon` |
| **Accessibility** | `enableRtl`, event handlers |

## Documentation and Navigation Guide

### Getting Started & Data Binding
📄 **Read:** [references/getting-started-and-data-binding.md](references/getting-started-and-data-binding.md)
- ASP.NET Core project setup and TagHelper import
- DataSource property variations (array, JSON, remote)
- Field mapping for text, id, and nested properties
- Remote data binding with DataManager and Query
- Basic ListView initialization examples

### Field Settings & Configuration
📄 **Read:** [references/field-settings-and-configuration.md](references/field-settings-and-configuration.md)
- Complete field mapping options (14 properties)
- iconCss for dynamic icon customization
- enabled, isVisible, isChecked state properties
- groupBy for categorization logic
- child property for nested list support
- Validation patterns and edge cases

### Grouping, Nested Lists & Virtualization
📄 **Read:** [references/grouping-nested-lists-virtualization.md](references/grouping-nested-lists-virtualization.md)
- Grouping items by category with groupTemplate
- Nested list navigation structure
- enableVirtualization for large datasets
- Window scroll vs container scroll modes
- Conditional rendering in templates
- Performance optimization strategies

### Templates & Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- template property for item customization
- headerTemplate and groupTemplate
- Built-in CSS classes (e-list-wrapper, e-list-avatar, e-list-badge, etc.)
- Avatar and multi-line list patterns
- Custom HTML markup in templates

### Checkboxes, Selection & Events
📄 **Read:** [references/checkboxes-selection-events.md](references/checkboxes-selection-events.md)
- showCheckBox property and positioning (Left/Right)
- select event with SelectEventArgs
- Multi-item selection patterns
- Checked state management
- Selection event handling

### Styling & Appearance
📄 **Read:** [references/styling-appearance-properties.md](references/styling-appearance-properties.md)
- cssClass for custom styling
- height and width control
- showHeader and showIcon properties
- CSS selector reference for styling
- Hover and focus state customization

### Events & Error Handling
📄 **Read:** [references/events-and-error-handling.md](references/events-and-error-handling.md)
- select, scroll, actionBegin, actionComplete events
- Event binding in TagHelper
- Remote data failure scenarios
- Error handling strategies

### Sorting, Filtering & Scrolling
📄 **Read:** [references/sorting-filtering-scrolling.md](references/sorting-filtering-scrolling.md)
- sortOrder property (Ascending, Descending)
- sortBy field mapping
- scroll event for dynamic loading
- Infinite scroll patterns
- Filter operations

### Accessibility & Keyboard Navigation
📄 **Read:** [references/accessibility-keyboard-aria.md](references/accessibility-keyboard-aria.md)
- Keyboard shortcuts (Arrow Up/Down, Select, Back)
- ARIA attributes (aria-selected, aria-level)
- enableRtl for right-to-left support
- Screen reader compatibility
- Best practices for inclusive design

### Advanced Features & Persistence
📄 **Read:** [references/advanced-features-persistence.md](references/advanced-features-persistence.md)
- enablePersistence for state retention
- animation property with AnimationSettings
- locale for localization
- disableHtmlEncode and enableHtmlSanitizer
- RTL and cultural adaptations

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete ListView properties (30+ properties documented)
- Events reference (select, scroll, actionBegin, actionComplete, actionFailure)
- Field mapping API with type signatures
- Enumerations (SortOrder, AnimationEffect, etc.)
- Method signatures for programmatic control
- Event argument types and properties

## Quick Start Example

**Basic ASP.NET Core ListView with TagHelper:**

```cshtml
@{
    ViewData["Title"] = "ListView Example";
    List<ListItem> dataSource = new List<ListItem>()
    {
        new ListItem { id = "1", text = "Artwork" },
        new ListItem { id = "2", text = "Abstract" },
        new ListItem { id = "3", text = "Modern Painting" },
        new ListItem { id = "4", text = "Ceramics" }
    };
}

<ejs-listview id="list" dataSource="dataSource" 
    showHeader="true" headerTitle="Art Gallery">
</ejs-listview>

@code {
    public class ListItem
    {
        public string id { get; set; }
        public string text { get; set; }
    }
}
```

**With Selection & Checkbox:**

```cshtml
<ejs-listview id="list" dataSource="dataSource" 
    showCheckBox="true" checkBoxPosition="Right">
</ejs-listview>
```

**With Grouping:**

```cshtml
<ejs-listview id="list" dataSource="dataSource">
    <e-listview-fieldsettings text="text" groupBy="category" id="id"></e-listview-fieldsettings>
</ejs-listview>
```

## Common Patterns

### Pattern 1: Simple Data List
Use `dataSource` with array of strings or objects; map `fields.text` for display.

### Pattern 2: Categorized Groups
Set `fields.groupBy` to organize items under category headers automatically.

### Pattern 3: Nested Hierarchies
Map `fields.child` to enable drill-down navigation through parent-child relationships.

### Pattern 4: Large Dataset Optimization
Enable `enableVirtualization="true"` to render only visible items; improves performance 10x+.

### Pattern 5: Custom Item Display
Use `template` property with `<div class="e-list-wrapper">` for rich formatting (avatars, badges, multi-line text).

### Pattern 6: Remote Data Integration
Use `dataSource` with DataManager; set `query` to filter/sort server-side; bind `fields` to match API response.

## Key Field Mappings Reference

The `fields` property controls data extraction. Common mappings:

| Field Property | Purpose | Example |
|---|---|---|
| `text` | Display text for item | `text="productName"` |
| `id` | Unique identifier | `id="productId"` |
| `groupBy` | Category/group field | `groupBy="category"` |
| `child` | Nested list data | `child="subcategories"` |
| `iconCss` | Icon class | `iconCss="iconClass"` |
| `enabled` | Enable/disable state | `enabled="isActive"` |
| `isChecked` | Checkbox state | `isChecked="isSelected"` |
| `isVisible` | Visibility state | `isVisible="isVisible"` |
| `tooltip` | Hover tooltip text | `tooltip="description"` |
| `sortBy` | Sort field | `sortBy="name"` |
| `htmlAttributes` | Custom attributes | `htmlAttributes="attributes"` |

## Common Use Cases

### Use Case 1: Product Category Browser
Group products by category; enable selection for shopping cart addition.

### Use Case 2: File/Folder Navigation
Use nested lists with icons for file explorer interface.

### Use Case 3: Task Management List
Combine checkboxes with templates for todo/task display and status tracking.

### Use Case 4: Contact Directory
Sort alphabetically; template with avatars and contact info; filter by category.

### Use Case 5: Large Data Feed (News, Logs)
Enable virtualization; implement scroll event for dynamic loading; optimize rendering.

---

**Next Steps:**
- Read [getting-started-and-data-binding.md](references/getting-started-and-data-binding.md) to set up your first ListView
- Explore [api-reference.md](api-reference.md) for complete property, event, and method documentation
- Review [templates-and-customization.md](references/templates-and-customization.md) for advanced formatting options
- Check [references/accessibility-keyboard-aria.md](references/accessibility-keyboard-aria.md) for keyboard and ARIA support
