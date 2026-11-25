---
name: syncfusion-aspnetcore-dropdown-tree
description: Implement the Syncfusion ASP.NET Core DropDownTree component to bind hierarchical and self-referential data, enable checkbox selection, customize templates, implement keyboard accessibility, and handle tree interactions when building multi-level dropdown selections.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
---

# Implementing Syncfusion DropDownTree Component

The Syncfusion DropDownTree control is a dropdown component that displays hierarchical tree data structures, allowing users to select single or multiple values from a tree hierarchy. It combines the features of a traditional dropdown list with the hierarchical organization of a tree structure, making it ideal for applications requiring organized, nested data selection.

## When to Use This Skill

Use this skill when you need to:

- **Display hierarchical data** in a dropdown format where items have parent-child relationships
- **Enable tree-based selection** with expand/collapse node functionality
- **Support multi-selection** with checkbox or keyboard navigation
- **Implement custom templates** for item display, headers, footers, and selected value representation
- **Bind data** from local JavaScript arrays, remote servers (OData, Web API), or lazy-load on demand
- **Maintain accessibility** with keyboard support (arrow keys, Enter, Space) and ARIA attributes
- **Localize the component** for different cultures and languages
- **Prevent node selection** for parent nodes while allowing child selection

## Key Features Overview

The DropDownTree component provides comprehensive functionality for tree-based dropdown selection:

- **Data Binding Options**: Hierarchical data, self-referential data structures, remote data services with DataManager adaptors
- **Selection Modes**: Single selection, multi-selection with checkboxes, delimiter-separated display, chip/box mode, or custom templates
- **Keyboard Navigation**: Full keyboard support with arrow keys, Enter, Space, Home, End, Alt+Up/Down, Escape
- **Custom Templates**: Item templates, value templates, header templates, footer templates, no-records templates, action-failure templates
- **Tree Configuration**: Expand behavior (click, double-click, auto), load on demand (lazy loading), auto-check parent-child dependencies
- **Accessibility**: WAI-ARIA compliant with listbox roles, treeitem roles, ARIA attributes, screen reader support
- **Filtering**: Real-time search with configurable filter types (StartsWith, EndsWith, Contains), case sensitivity, accent handling
- **Persistence**: State retention across browser sessions
- **RTL Support**: Right-to-left rendering for Arabic, Hebrew, and other RTL languages

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Platform setup and prerequisites
- NuGet package installation
- Script and stylesheet references
- Tag helper configuration
- Basic DropDownTree initialization
- First rendering example with data binding
- Building blocks needed before advanced features

### Data Binding and Hierarchy
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Hierarchical data source binding with nested array structures
- Self-referential data structures with parent-value relationships
- Remote data binding with DataManager and adaptors (OData, ODataV4, WebAPI, URL)
- Load on demand (lazy loading) for large datasets
- Field mapping configuration (text, value, child, parentValue, hasChildren)
- Query support for remote data filtering
- Preventing node selection with the selectable property

### Selection and Checkbox Features
📄 **Read:** [references/checkbox-and-selection.md](references/checkbox-and-selection.md)
- Enabling checkbox mode with showCheckBox property
- Multi-selection with allowMultiSelection property
- Auto-check dependency with parent-child synchronization
- Select All functionality in popup header
- Display modes (Default, Delimiter, Box, Custom) for selected items
- Custom template for selected item representation
- Check state management and prevention for disabled children
- Controlling expand behavior and tree interaction modes

### Templates and Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Item template for customizing list item appearance
- Value template for customizing selected value display
- Header template for popup header customization
- Footer template for popup footer customization
- No records template for empty search results
- Action failure template for remote data errors
- Custom template modes (Default, Delimiter, Box, Custom) for multi-selection display
- CSS class customization and HTML attribute mapping
- Styling and visual customization techniques

### Properties and Configuration
📄 **Read:** [references/properties-and-configuration.md](references/properties-and-configuration.md)
- Complete property reference including filtering, appearance, behavior, data settings
- Expand behavior configuration (Auto, Click, DblClick, None)
- Filter types and filter bar customization
- Float label types and placeholder text
- Persistence and state management
- RTL and locale settings
- Icon CSS and image URL mapping
- HTML attributes and CSS class application
- Destruction behavior when popup closes

### Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Change event and value tracking
- Selection events (select/unselect actions)
- Before open/popup events for preventing or customizing popup display
- Data bound event for remote data completion
- Filtering event for custom filter implementation
- Keyboard interaction event handling
- Focus and blur events for state management
- Event arguments and properties available in handlers

### Accessibility and Globalization
📄 **Read:** [references/accessibility-and-globalization.md](references/accessibility-and-globalization.md)
- Keyboard navigation shortcuts and interaction patterns
- ARIA attributes and WAI-ARIA compliance
- Screen reader support and accessible markup
- Focus management and keyboard event handling
- Localization and culture-specific text customization
- RTL (right-to-left) language support
- Multi-language string customization
- Accessibility best practices for dropdown trees

## Quick Start Example

### Basic Initialization

```html
<!-- ASP.NET Core Razor Template -->
@{
    var treeData = new List<TreeNode>
    {
        new TreeNode { Id = "1", Text = "Item 1" },
        new TreeNode { Id = "2", Text = "Item 2", Children = new List<TreeNode>
        {
            new TreeNode { Id = "3", Text = "Child 1" },
            new TreeNode { Id = "4", Text = "Child 2" }
        }}
    };
}

<ejs-dropdowntree id="tree" placeholder="Select an item">
    <e-dropdowntree-fields dataSource="@treeData" text="Text" value="Id" child="Children"></e-dropdowntree-fields>
</ejs-dropdowntree>
```

### With Checkbox Support

```html
<ejs-dropdowntree id="treeCheckbox" showCheckBox="true">
    <e-dropdowntree-fields dataSource="@treeData" text="Text" value="Id" child="Children"></e-dropdowntree-fields>
</ejs-dropdowntree>
```

### With Templates

```html
@{
    var itemTemp = "<span>${Text} (${Id})</span>";
    var valueTemp = "<span>Selected: ${Text}</span>";
}

<ejs-dropdowntree id="treeTemplate" itemTemplate="@itemTemp" valueTemplate="@valueTemp">
    <e-dropdowntree-fields dataSource="@treeData" text="Text" value="Id" child="Children"></e-dropdowntree-fields>
</ejs-dropdowntree>
```

## Common Patterns

### Pattern 1: Hierarchical Organization Categories
**Scenario**: Display product categories in a hierarchical structure

```html
<ejs-dropdowntree id="categories" placeholder="Select Category">
    <e-dropdowntree-treeSettings expandOn="true"></e-dropdowntree-treeSettings>
    <e-dropdowntree-fields dataSource="@CategoryHierarchy" text="CategoryName" value="CategoryId" child="SubCategories"></e-dropdowntree-fields>
</ejs-dropdowntree>
```

### Pattern 2: Multi-Select with Checkboxes
**Scenario**: Allow users to select multiple items with automatic parent-child dependency

```html
<ejs-dropdowntree id="multiSelect" showCheckBox="true" allowMultiSelection="true" mode="Box">
    <e-dropdowntree-treeSettings autoCheck="true"></e-dropdowntree-treeSettings>
    <e-dropdowntree-fields dataSource="@DataSource" text="Text" value="Id" child="Children"></e-dropdowntree-fields>
</ejs-dropdowntree>
```

### Pattern 3: Lazy Loading Large Datasets
**Scenario**: Load only visible nodes to improve performance with large trees

```html
<ejs-dropdowntree id="lazyLoad">
    <e-dropdowntree-treeSettings loadOnDemand="true"></e-dropdowntree-treeSettings>
    <e-dropdowntree-fields dataSource="@RemoteDataManager" text="Name" value="Id" child="Children" hasChildren="HasChild"></e-dropdowntree-fields>
</ejs-dropdowntree>
```

### Pattern 4: Remote Data with Filtering
**Scenario**: Fetch tree data remotely and enable real-time search
**C# (TreeViewController.cs)**:
```csharp
public ActionResult RemoteData()
{
    DropDownTreeFields parentData = new DropDownTreeFields();
    DropDownTreeFields childData = new DropDownTreeFields();
    object data = new DataManager
    {
        Url = "https://services.odata.org/V4/Northwind/Northwind.svc",
        Adaptor = "ODataV4Adaptor",
        CrossDomain = true
    };
    // Parent data mapping
    parentData.Query = "new ej.data.Query().from('Employees').select('EmployeeID,FirstName,Title').take(5)";
    parentData.Value = "EmployeeID";
    parentData.Text = "FirstName";
    parentData.HasChildren = "EmployeeID";
    parentData.Child = childData;
    parentData.DataSource = data;
    // Child data mapping  
    childData.Query = "new ej.data.Query().from('Orders').select('OrderID,EmployeeID,ShipName').take(5)";
    childData.Value = "OrderID";
    childData.Text = "ShipName";
    childData.ParentValue = "EmployeeID";
    childData.DataSource = data;
    ViewBag.remoteFields = parentData;
    return View();
}
```
```html

<ejs-dropdowntree id="remoteFilter" allowFiltering="true" filterType="StartsWith">
    <e-dropdowntree-fields child="ViewBag.child" query="new ej.data.Query().from('Employees').select('EmployeeID,FirstName,Title').take(5)" value="EmployeeID" text="FirstName" hasChildren="EmployeeID">
        <e-data-manager url="https://services.odata.org/V4/Northwind/Northwind.svc" adaptor="ODataV4Adaptor" crossDomain="true"></e-data-manager>
    </e-dropdowntree-fields>
</ejs-dropdowntree>
```

### Pattern 5: Custom Display Modes
**Scenario**: Display selected multiple items in chip format

```html
<ejs-dropdowntree id="chipMode" showCheckBox="true" allowMultiSelection="true" mode="Box" delimiterChar=",">
    <e-dropdowntree-fields dataSource="@DataSource" text="Text" value="Id" child="Children"></e-dropdowntree-fields>
</ejs-dropdowntree>
```

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `dataSource` | DataManager \| Array | - | Specifies the data items for the DropDownTree |
| `fields` | FieldsModel | - | Maps data source fields to DropDownTree properties |
| `value` | string[] | - | Gets/sets the currently selected value(s) |
| `text` | string | - | Gets the currently selected item text |
| `showCheckBox` | boolean | false | Enables checkbox mode for multiple selection |
| `allowMultiSelection` | boolean | false | Enables multi-selection without checkboxes |
| `allowFiltering` | boolean | false | Enables filter bar for searching items |
| `enabled` | boolean | true | Enables/disables the component |
| `readonly` | boolean | false | Sets read-only state |
| `mode` | Mode | 'Default' | Display mode for selected items (Default, Delimiter, Box, Custom) |
| `treeSettings` | TreeSettings | - | Configures tree expansion and selection behavior |
| `itemTemplate` | string \| Function | - | Template for customizing item display |
| `valueTemplate` | string \| Function | - | Template for customizing selected value display |
| `headerTemplate` | string \| Function | - | Template for popup header |
| `footerTemplate` | string \| Function | - | Template for popup footer |
| `noRecordsTemplate` | string \| Function | - | Template when no items found |
| `actionFailureTemplate` | string \| Function | - | Template when remote data fails |
| `customTemplate` | string \| Function | - | Custom template for selected items with mode='Custom' |
| `placeholder` | string | - | Watermark text for input element |
| `floatLabelType` | FloatLabelType | 'Never' | Label floating behavior |
| `locale` | string | 'en' | Culture for localization |
| `enableRtl` | boolean | false | Right-to-left rendering |
| `enablePersistence` | boolean | false | Persist state across sessions |
| `cssClass` | string | - | CSS class for styling |
| `filterType` | TreeFilterType | 'StartsWith' | Search filter algorithm |
| `ignoreCase` | boolean | true | Case-insensitive search |
| `ignoreAccent` | boolean | false | Ignore diacritical marks in search |

## Common Use Cases

1. **Organizational Hierarchies**: Display employee reporting structures, department hierarchies
2. **File System Navigation**: Show folder structures with expandable directories
3. **Category Selection**: Product categories with subcategories for e-commerce
4. **Geographic Hierarchies**: Country-State-City nested selections
5. **Permission/Role Hierarchies**: Multi-level permission or role selection
6. **Task Breakdown Structures**: Project tasks organized hierarchically
7. **Localization Selection**: Language families and specific languages
8. **Feature/Module Selection**: Application features organized by module and feature

---

**Next Steps**: Choose a reference document above based on your current task. Each reference file contains detailed examples, property explanations, and implementation guidelines specific to that feature area.
