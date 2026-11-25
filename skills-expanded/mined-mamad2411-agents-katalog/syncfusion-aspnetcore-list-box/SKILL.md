---
name: syncfusion-aspnetcore-list-box
description: Implement and configure Syncfusion ASP.NET Core ListBox component with selection controls. Use this when building selection interfaces with single/multiple modes, data binding, or advanced features. Covers ListBox implementation, selection state management, appearance customization, and user interaction handling.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
  component: "ListBox"
  framework: "ASP.NET Core"
  library: "Syncfusion EJ2"
---

# Implementing Syncfusion ASP.NET Core ListBox

## When to Use This Skill

Use this skill when you need to:
- **Implement ListBox control** in ASP.NET Core applications using TagHelper syntax
- **Configure selection modes** (single or multiple item selection)
- **Bind data sources** to the ListBox component
- **Apply themes and styling** to match your design
- **Handle advanced features** like drag-and-drop, dual lists, and filtering
- **Solve common tasks** like adding items, enabling scrollers, or form integration
- **Debug issues** with selection, data binding, or rendering

## Component Overview

The Syncfusion ASP.NET Core **ListBox** component is a versatile selection control that supports:

- **Single and multiple item selection** with keyboard and mouse navigation
- **Data binding** from arrays, objects, and dynamic sources
- **Advanced features**: drag-drop, templates, dual lists, sorting, grouping
- **Comprehensive theming** with built-in and custom themes
- **Full accessibility** support (WCAG compliance, keyboard navigation)
- **Rich customization** via CSS classes, properties, and events

Perfect for: dropdowns, filters, selection interfaces, permission lists, bulk operations

## Documentation and Navigation Guide

### Getting Started with ListBox
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation steps
- ASP.NET Core project setup (Razor pages, MVC)
- TagHelper registration in `_ViewImports.cshtml`
- CDN stylesheet and script configuration
- Register Syncfusion Script Manager
- Create your first ListBox control
- Initial data binding examples

### Selection Modes and User Interaction
📄 **Read:** [references/selection-modes.md](references/selection-modes.md)
- Single selection mode (radio button style)
- Multiple selection mode (checkbox style)
- Selection events (`change`, `select`, `doubleClick`)
- Keyboard navigation (arrows, space, Ctrl+A)
- Programmatic selection management
- Select-all functionality with checkboxes
- Advanced selection patterns

### Data Binding and Data Sources
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding string arrays to ListBox
- Binding complex object arrays
- Field mapping (Text and Value properties)
- Dynamic data loading via AJAX
- Real-time data updates
- Master-detail and dependent lists
- Filtering and refreshing data

### Styling, Theming, and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- Built-in themes (Material, Bootstrap, Fluent, Tailwind)
- Theme Studio integration for custom themes
- CSS class customization for ListBox elements
- Horizontal ListBox layout implementation
- Custom styling with colors, fonts, and spacing
- Responsive design patterns for mobile/tablet
- Status-based item coloring and templates

### Sorting and Grouping ListBox Data
📄 **Read:** [references/sorting-and-grouping.md](references/sorting-and-grouping.md)
- Sort items in ascending/descending order
- Group items by category or type
- Combine sorting and grouping for organized lists
- Handle complex data with group headers
- Practical examples with multiple categories
- Performance optimization for large grouped lists

### Advanced Features and Configurations
📄 **Read:** [references/features.md](references/features.md)
- Drag and drop within list and between lists
- Icons and custom item templates
- Dual list box (transfer between lists)
- Virtual scrolling for large datasets
- Scroller configuration for fixed heights
- Complex selection scenarios and patterns
- Event handling best practices

### Common Tasks and Troubleshooting
📄 **Read:** [references/howto-common-tasks.md](references/howto-common-tasks.md)
- Adding and removing items dynamically
- Enabling/disabling specific items
- Filtering ListBox data with search
- Form submission with selected values
- Scroll positioning and monitoring
- Validating user input before operations
- Performance optimization techniques
- Debugging common issues

## Quick Start Example

### 1. Install Syncfusion Package

```csharp
// Package Manager Console
Install-Package Syncfusion.EJ2.AspNet.Core -Version 25.1.35
```

### 2. Register TagHelper

```cshtml
<!-- ~/Pages/_ViewImports.cshtml -->
@addTagHelper *, Syncfusion.EJ2
```

### 3. Add Theme and Scripts

```cshtml
<!-- ~/Pages/Shared/_Layout.cshtml -->
<head>
    <link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/25.1.35/fluent.css" />
</head>
<body>
    <!-- Content -->
    <script src="https://cdn.syncfusion.com/ej2/25.1.35/dist/ej2.min.js"></script>
    <ejs-scripts></ejs-scripts>
</body>
```

### 4. Create Basic ListBox

```csharp
// ~/Pages/Index.cshtml.cs
public class IndexModel : PageModel
{
    public List<string> Fruits { get; set; }
    
    public void OnGet()
    {
        Fruits = new List<string> { "Apple", "Banana", "Cherry", "Date" };
    }
}
```

```cshtml
<!-- ~/Pages/Index.cshtml -->
@page
@model IndexModel

<ejs-listbox id="fruitBox" dataSource="@Model.Fruits"></ejs-listbox>
```

## Common Patterns

### Pattern 1: Single Selection (Like Radio Buttons)

```cshtml
<ejs-listbox id="categoryBox" 
             dataSource="@Model.Categories"
             selectionSettings="@(new Syncfusion.EJ2.DropDowns.ListBoxSelectionSettings 
             { 
                 Mode = Syncfusion.EJ2.DropDowns.SelectionMode.Single 
             })"
             change="onCategoryChange">
</ejs-listbox>

<script>
    function onCategoryChange(args) {
        console.log('Selected: ' + args.text);
    }
</script>
```

**Use when:** User picks one option (category, department, status)

### Pattern 2: Multiple Selection (Like Checkboxes)

```cshtml
<ejs-listbox id="tagsBox" 
             dataSource="@Model.Tags"
             selectionSettings="@(new Syncfusion.EJ2.DropDowns.ListBoxSelectionSettings 
             { 
                 Mode = Syncfusion.EJ2.DropDowns.SelectionMode.Multiple,
                 CheckboxPosition = Syncfusion.EJ2.DropDowns.CheckBoxPosition.Before
             })">
</ejs-listbox>
```

**Use when:** User selects multiple options (permissions, features, filters)

### Pattern 3: With Search Filter

```cshtml
<input type="text" id="searchBox" placeholder="Search..." />
<ejs-listbox id="searchableList" dataSource="@Model.Items"></ejs-listbox>

<script>
    const allItems = @Html.Raw(System.Text.Json.JsonSerializer.Serialize(Model.Items));
    
    document.getElementById('searchBox').addEventListener('keyup', function(e) {
        var listbox = document.getElementById('searchableList').ej2_instances[0];
        var term = e.target.value.toLowerCase();
        listbox.dataSource = allItems.filter(item => 
            item.toLowerCase().includes(term)
        );
    });
</script>
```

**Use when:** Long lists need filtering (employees, products, permissions)

### Pattern 4: Dual List (Transfer Between Lists)

```cshtml
<div style="display: flex; gap: 20px;">
    <div>
        <label>Available</label>
        <ejs-listbox id="availableBox" dataSource="@Model.Available"></ejs-listbox>
    </div>
    <div>
        <button onclick="moveRight()">→</button>
        <button onclick="moveLeft()">←</button>
    </div>
    <div>
        <label>Selected</label>
        <ejs-listbox id="selectedBox" dataSource="@Model.Selected"></ejs-listbox>
    </div>
</div>
```

**Use when:** Transferring items between lists (permissions, features, users)

## Key Properties and Methods

### Essential Properties

| Property | Type | Purpose |
|----------|------|---------|
| `dataSource` | IEnumerable | Data to display in the list |
| `value` | string/array | Currently selected value(s) |
| `selectionSettings` | ListBoxSelectionSettings | Configure selection behavior |
| `fields` | ListBoxFieldSettings | Map object properties to text/value/groupBy |
| `sortOrder` | SortOrder | Sort items: None, Ascending, Descending |
| `cssClass` | string | Custom CSS class for styling |
| `allowDragAndDrop` | bool | Enable drag-drop reordering |
| `height` | string | Fixed height with scroll |

### Common Methods

```javascript
var listbox = document.getElementById('listBox').ej2_instances[0];

// Get/set value
listbox.value;                    // Get selected value(s)
listbox.value = 'newValue';       // Set selected

// Selection operations
listbox.selectAll();              // Select all items
listbox.clearSelection();         // Deselect all
listbox.selectItemsByRange(0, 3); // Select range

// Data operations
listbox.refresh();                // Refresh UI after data change
listbox.destroy();                // Clean up component
```

## Common Use Cases

| Use Case | Selection | Features | Example |
|----------|-----------|----------|---------|
| **Category Picker** | Single | None | Store category preference |
| **Bulk Permissions** | Multiple | Checkboxes | Assign permissions to users |
| **Product Filter** | Multiple | Search | E-commerce filtering |
| **Feature Toggle** | Multiple | Drag-sort | Set feature priority |
| **Employee Selector** | Multiple | Search, Templates | Team assignment |
| **Report Fields** | Multiple | Dual lists | Include/exclude fields |

## Key Features at a Glance

- ✓ **Single/Multiple Selection** - Choose one or many items
- ✓ **Data Binding** - Connect to arrays, objects, databases
- ✓ **Sorting** - Alphabetical ordering (ascending/descending)
- ✓ **Grouping** - Organize items by category or type
- ✓ **Drag & Drop** - Reorder items or transfer between lists
- ✓ **Templates** - Customize item display with HTML
- ✓ **Theming** - 7+ built-in themes + custom themes
- ✓ **Filtering** - Search and filter data
- ✓ **Keyboard Nav** - Full keyboard support for accessibility
- ✓ **Virtual Scroll** - Handle thousands of items efficiently
- ✓ **Events** - Change, select, scroll events
- ✓ **Responsive** - Works on desktop, tablet, mobile

## Troubleshooting Quick Links

**Problem** → **Solution**
- "ListBox not showing" → Check [Getting Started](references/getting-started.md#stylesheet-and-script-resources)
- "Data not binding" → See [Data Binding](references/data-binding.md#field-mapping)
- "Events not firing" → Read [Selection Modes](references/selection-modes.md#selection-events)
- "Styling looks wrong" → Visit [Styling Guide](references/styling-and-appearance.md#built-in-themes)
- "Sorting not working" → Check [Sorting & Grouping](references/sorting-and-grouping.md#troubleshooting)
- "Grouping not working" → Read [Sorting & Grouping Guide](references/sorting-and-grouping.md#grouping-items)
- "Performance slow" → Check [Features - Scroller](references/features.md#scroller-configuration)
- "Drag-drop not working" → Review [Features - Drag & Drop](references/features.md#drag-and-drop)

## Next Steps

1. **New to ListBox?** Start with [Getting Started](references/getting-started.md)
2. **Need selection control?** Go to [Selection Modes](references/selection-modes.md)
3. **Working with data?** Read [Data Binding](references/data-binding.md)
4. **Organizing large lists?** Visit [Sorting & Grouping](references/sorting-and-grouping.md)
5. **Styling your list?** Visit [Styling & Appearance](references/styling-and-appearance.md)
6. **Advanced features?** Explore [Advanced Features](references/features.md)
7. **Solving problems?** Check [Common Tasks](references/howto-common-tasks.md)

---

## See Also

- **Parent Library** → [Implementing Syncfusion ASP.NET Core Components](../..)
- **Component Category** → [Dropdowns](..)
- **Syncfusion Docs** → [Official ListBox Documentation](https://www.syncfusion.com/aspnet-core-ui-controls/listbox)
