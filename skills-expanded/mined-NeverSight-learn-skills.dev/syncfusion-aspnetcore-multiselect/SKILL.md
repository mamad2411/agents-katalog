---
name: syncfusion-aspnetcore-multiselect
description: Complete guide to implementing the Syncfusion MultiSelect component in ASP.NET Core applications with tag helpers, data binding, filtering, templates, checkboxes, and accessibility for building advanced dropdown selection forms.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdown Controls"
  platform: "ASP.NET Core"
  framework: "Syncfusion.EJ2.AspNet.Core"
---

# Implementing MultiSelect in ASP.NET Core

The MultiSelect is an advanced dropdown component that enables users to select multiple values from a predefined list with features like filtering, templates, checkboxes, grouping, and full accessibility support. This skill guides you through implementing MultiSelect in ASP.NET Core applications using Syncfusion's tag helper syntax.

## When to Use This Skill

Use this skill when you need to:
- Create dropdown fields where users can select multiple options
- Add search/filter functionality to large option lists
- Display selected items as chips with remove capability
- Implement checkboxes for clear multi-selection UI
- Bind to local arrays or remote data sources
- Customize list item appearance with templates
- Group related options by category
- Ensure WCAG 2.2 accessibility compliance
- Handle complex selection scenarios (cascading, custom values)

## Key Features

| Feature | Use Case |
|---------|----------|
| **Multiple Selection** | Select multiple values from dropdown list |
| **Filtering & Search** | Search through large lists efficiently |
| **Checkboxes** | Visual indication of multi-select with checkbox mode |
| **Data Binding** | Local arrays or remote data sources |
| **Templates** | Customize item appearance and selected value display |
| **Grouping** | Organize options into logical categories |
| **Sorting** | Alphabetically sort options (ascending/descending) |
| **Chip Display** | Show selected items as removable chips |
| **Custom Values** | Allow users to add custom selection values |
| **Virtual Scrolling** | Efficiently handle 1000+ item lists |
| **Cascading** | Link multiple MultiSelect components |
| **WCAG Compliance** | Built-in accessibility for screen readers, keyboard nav |
| **Events** | Respond to selection changes, opens, closes |

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements
- Installing Syncfusion.EJ2.AspNet.Core NuGet package
- Configuring TagHelper in _ViewImports.cshtml
- Adding stylesheets and script resources via CDN
- Registering the script manager
- Creating your first MultiSelect
- Running and testing the application

### Tag Helper Syntax
📄 **Read:** [references/tag-helper-syntax.md](references/tag-helper-syntax.md)
- MultiSelect tag helper structure and properties
- Essential properties (Placeholder, Value, Readonly, Disabled)
- Data source binding basics
- Event binding in tag helpers
- CSS class customization
- Best practices and common patterns

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding to local array of strings
- Binding to array of objects
- Complex object binding with nested fields
- Remote data sources with DataManager
- Field mapping (text, value, groupBy)
- Dynamic data loading and refresh patterns

### Filtering and Search
📄 **Read:** [references/filtering-and-search.md](references/filtering-and-search.md)
- Built-in search box functionality
- Filter type options (contains, startswith, endswith)
- Custom filter logic with server-side filtering
- Filter templates for advanced search UI
- NoRecordsTemplate handling
- Search performance optimization

### Templates and Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Item template customization
- Value template (selected items display)
- Header and footer templates
- Group header templates
- Icon integration in items
- CSS styling and class customization

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Checkbox mode for enhanced multi-selection UI
- Grouping items by category
- Sorting options (ascending/descending)
- Custom value support (create new values)
- Chip customization and removal
- Virtual scrolling for large datasets
- Cascading MultiSelect patterns

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 Level AA compliance
- Keyboard navigation (Arrow keys, Tab, Enter, Escape)
- ARIA attributes and roles
- Screen reader support
- Focus management best practices
- Testing accessibility with tools

## Quick Start Example

Here's a minimal MultiSelect implementation:

```razor
<!-- _ViewImports.cshtml -->
@addTagHelper *, Syncfusion.EJ2

<!-- View file -->
<ejs-multiselect id="multiselect" 
    dataSource="ViewBag.DataSource" 
    fields-text="Name" 
    fields-value="Id"
    placeholder="Select options">
</ejs-multiselect>
```

```csharp
// Controller
public IActionResult Index()
{
    List<SelectData> data = new List<SelectData>
    {
        new SelectData { Id = "1", Name = "Option 1" },
        new SelectData { Id = "2", Name = "Option 2" },
        new SelectData { Id = "3", Name = "Option 3" }
    };
    ViewBag.DataSource = data;
    return View();
}
```

## Common Patterns

### Pattern 1: Simple String Array
Select from a list of string values:
```razor
<ejs-multiselect id="skills" 
    dataSource="ViewBag.SkillsList" 
    placeholder="Select skills">
</ejs-multiselect>
```

### Pattern 2: Object Array with Custom Display
```razor
<ejs-multiselect id="products" 
    dataSource="ViewBag.ProductList"
    fields-text="ProductName"
    fields-value="ProductId"
    placeholder="Select products">
</ejs-multiselect>
```

### Pattern 3: With Checkboxes
```razor
<ejs-multiselect id="languages" 
    dataSource="ViewBag.LanguageList"
    fields-text="Language"
    fields-value="LanguageCode"
    mode="CheckBox"
    placeholder="Select languages">
</ejs-multiselect>
```

### Pattern 4: Filtered Selection
```razor
<ejs-multiselect id="countries" 
    dataSource="ViewBag.CountryList"
    fields-text="CountryName"
    fields-value="CountryCode"
    allowFiltering="true"
    filterType="Contains"
    placeholder="Search and select countries">
</ejs-multiselect>
```

## Key Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `dataSource` | Array | List of data items |
| `fields-text` | string | Field name for display text |
| `fields-value` | string | Field name for data value |
| `placeholder` | string | Hint text when empty |
| `value` | string[] | Initially selected values |
| `allowFiltering` | boolean | Enable search/filter box |
| `filterType` | string | Filter type (StartsWith, Contains, EndsWith) |
| `mode` | string | Selection mode (Default, CheckBox, Delimiter) |
| `readonly` | boolean | Prevent editing |
| `disabled` | boolean | Disable the control |
| `showSelectAll` | boolean | Show select all checkbox |
| `maximumSelectionLength` | number | Max selectable items |
| `delayUpdateOn` | string | Event to trigger updates |
| `fields-groupBy` | string | Group items by field |

## Common Use Cases

### Use Case 1: Role Selection in Admin Panel
Users select multiple roles to assign to administrators:
- Display all available roles
- Filter as user types
- Show selections as chips
- Validate selection count

### Use Case 2: Product Category Filter
E-commerce site filtering products by multiple categories:
- Group categories by parent
- Show item count per category
- Virtual scroll for 1000+ items
- Remember selections

### Use Case 3: Team Member Assignment
Assign multiple team members to projects:
- Search by name
- Show department grouping
- Display avatar in selection chips
- Prevent self-assignment

### Use Case 4: Tag Selection
Blog/content tagging with MultiSelect:
- Allow custom tag creation
- Show tag count/popularity
- Group by category
- Auto-complete suggestions

## Best Practices

1. **Always provide clear labels** - Label the MultiSelect with associated `<label>` element
2. **Set reasonable default selections** - Pre-select logical defaults when appropriate
3. **Use filtering for large lists** - Enable filtering when >10 items
4. **Validate on server** - Never trust client-side validation alone
5. **Handle empty state** - Provide clear message when no items selected
6. **Group related items** - Use groupBy for lists >20 items
7. **Limit selection count** - Use maximumSelectionLength to prevent abuse
8. **Test keyboard navigation** - Ensure all features accessible via keyboard
9. **Provide accessible labels** - Use proper ARIA attributes
10. **Monitor performance** - Virtual scroll for 1000+ items

## Next Steps

1. **Start with Getting Started** - Follow setup instructions
2. **Implement a simple example** - Create basic MultiSelect binding
3. **Add filtering** - Enable search functionality
4. **Customize templates** - Enhance appearance with templates
5. **Handle selection events** - Respond to user selections
6. **Test accessibility** - Verify keyboard and screen reader support

---

**Ready to learn?** Start with [Getting Started](references/getting-started.md) →
