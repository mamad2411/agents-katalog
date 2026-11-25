---
name: syncfusion-winforms-autocomplete
description: Guides implementation of the Syncfusion WinForms AutoComplete control for text input with auto-suggestion functionality. Use when users want to add autocomplete textboxes, implement auto-suggestion features, create search boxes with suggestions, enable URL/email autocomplete, or build type-ahead search functionality in Windows desktop applications. Covers data binding, customization, filtering, multi-column dropdowns, events, and all AutoComplete-specific features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion WinForms AutoComplete Control

The AutoComplete control provides auto-suggestion functionality for text input fields in Windows Forms applications. It displays a dropdown list of suggestions as users type, enabling faster data entry and improved user experience with intelligent text completion.

## When to Use This Skill

Use the AutoComplete control when you need to:
- Add auto-suggestion to text input fields
- Implement type-ahead search functionality
- Create search boxes with intelligent suggestions
- Enable URL or email address autocomplete
- Build forms with frequently repeated input
- Provide filtered suggestions from large datasets
- Implement custom dropdown behaviors with multi-column displays

## Installation

### NuGet Installation

```bash
Install-Package Syncfusion.Tools.Windows
```

### Assembly Reference

Add reference to:
- `Syncfusion.Tools.Windows.dll`
- `Syncfusion.Shared.Base.dll`

## Quick Start

### Basic Setup

```csharp
using System;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Tools;

namespace AutoCompleteDemo
{
    public partial class Form1 : Form
    {
        private AutoComplete autoComplete1;
        
        public Form1()
        {
            InitializeComponent();
            
            // Create AutoComplete control
            autoComplete1 = new AutoComplete();
            autoComplete1.Location = new System.Drawing.Point(20, 20);
            autoComplete1.Size = new System.Drawing.Size(200, 20);
            autoComplete1.ParentForm = this;
            
            // Add data source
            autoComplete1.DataSource = new string[] 
            { 
                "Australia", 
                "Austria", 
                "Brazil", 
                "Canada", 
                "China" 
            };
            
            // Add to form
            this.Controls.Add(autoComplete1);
        }
    }
}
```

### Designer Setup

1. Drag `AutoComplete` control from Toolbox to Form
2. Set the `ParentForm` property to current form
3. Configure `DataSource` through Properties window or code
4. Customize appearance and behavior through Properties

## Core Concepts

### Data Source
The AutoComplete control can bind to various data sources:
- String arrays
- Generic collections (List<T>, ArrayList)
- DataTable and DataSet
- Custom objects with IList interface

### Parent Form
The `ParentForm` property must be set to enable the control to display the dropdown suggestion list. This associates the AutoComplete with the parent form's container.

### Filtering
Built-in filtering automatically matches user input against the data source, displaying relevant suggestions as the user types.

## Navigation Guide

### 🚀 Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly references
- Creating WinForms application
- Adding AutoComplete control via Designer
- Adding AutoComplete control programmatically
- Basic configuration and setup
- Running the application

### 📊 Working with Data Sources
📄 **Read:** [references/datasource.md](references/datasource.md)
- Binding to string collections
- Binding to DataTable and DataSet
- Binding to custom objects
- Multiple data sources
- Setting data source at design time
- Dynamic data source updates

### 🎨 Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Visual styles and themes
- Font and color customization
- Border styles
- Dropdown appearance
- Auto-size configuration
- Column appearance in dropdown
- Highlight matching text
- Custom rendering

### 🔧 Working with AutoComplete
📄 **Read:** [references/working-with-autocomplete.md](references/working-with-autocomplete.md)
- Auto-complete modes (Suggest, Append, SuggestAppend)
- Character casing
- Loading behavior
- Auto-population
- Default suggestions
- Clearing and resetting values
- Programmatic selection

### 📑 Multi-Column Dropdown
📄 **Read:** [references/multicolumn-dropdown.md](references/multicolumn-dropdown.md)
- Enabling multi-column mode
- Column configuration
- Column headers
- Column width and sizing
- Displaying multiple fields
- Custom column formatting
- Images in dropdown items
- Grid-like appearance

### ⚡ Events
📄 **Read:** [references/autocomplete-events.md](references/autocomplete-events.md)
- AutoCompleteCustomize event
- AutoCompleteValueChanged event
- BeforeCustomization event
- Handling user selections
- Validating input
- Custom event handlers

### 🎯 Overview
📄 **Read:** [references/overview.md](references/overview.md)
- Feature overview
- Use cases and scenarios
- Component architecture
- Performance considerations
- Best practices

## Common Patterns

### Pattern 1: Simple String AutoComplete
```csharp
AutoComplete autoComplete1 = new AutoComplete();
autoComplete1.Location = new System.Drawing.Point(20, 20);
autoComplete1.Size = new System.Drawing.Size(200, 20);
autoComplete1.ParentForm = this;

// Add string data
autoComplete1.DataSource = new string[] 
{
    "John", "Jane", "Bob", "Alice", "Charlie"
};

this.Controls.Add(autoComplete1);
```

### Pattern 2: DataTable Binding
```csharp
AutoComplete autoComplete1 = new AutoComplete();
autoComplete1.ParentForm = this;

// Create DataTable
DataTable dt = new DataTable();
dt.Columns.Add("Name", typeof(string));
dt.Columns.Add("Email", typeof(string));
dt.Rows.Add("John Doe", "john@example.com");
dt.Rows.Add("Jane Smith", "jane@example.com");

autoComplete1.DataSource = dt;
autoComplete1.DisplayMember = "Name";

this.Controls.Add(autoComplete1);
```

### Pattern 3: Multi-Column Display
```csharp
AutoComplete autoComplete1 = new AutoComplete();
autoComplete1.ParentForm = this;
autoComplete1.Style = AutoCompleteStyle.Default;

// Create DataTable with multiple columns
DataTable dt = new DataTable();
dt.Columns.Add("Name", typeof(string));
dt.Columns.Add("Country", typeof(string));
dt.Columns.Add("City", typeof(string));

dt.Rows.Add("John Doe", "USA", "New York");
dt.Rows.Add("Jane Smith", "UK", "London");
dt.Rows.Add("Bob Johnson", "Canada", "Toronto");

autoComplete1.DataSource = dt;

// Configure columns
autoComplete1.Columns.Add(new AutoCompleteDataColumnInfo("Name", 100));
autoComplete1.Columns.Add(new AutoCompleteDataColumnInfo("Country", 80));
autoComplete1.Columns.Add(new AutoCompleteDataColumnInfo("City", 80));

this.Controls.Add(autoComplete1);
```

### Pattern 4: Custom Filtering with Events
```csharp
AutoComplete autoComplete1 = new AutoComplete();
autoComplete1.ParentForm = this;
autoComplete1.DataSource = GetDataSource();

// Handle custom filtering
autoComplete1.AutoCompleteControl.ItemsListBox.DrawItem += 
    new DrawItemEventHandler(ItemsListBox_DrawItem);

void ItemsListBox_DrawItem(object sender, DrawItemEventArgs e)
{
    if (e.Index >= 0)
    {
        // Custom drawing logic
        e.DrawBackground();
        e.Graphics.DrawString(
            autoComplete1.AutoCompleteControl.ItemsListBox.Items[e.Index].ToString(),
            e.Font,
            Brushes.Black,
            e.Bounds);
        e.DrawFocusRectangle();
    }
}

this.Controls.Add(autoComplete1);
```

### Pattern 5: URL/Email AutoComplete
```csharp
AutoComplete autoComplete1 = new AutoComplete();
autoComplete1.ParentForm = this;
autoComplete1.Size = new System.Drawing.Size(300, 20);

// Common URLs
autoComplete1.DataSource = new string[]
{
    "http://www.syncfusion.com",
    "http://www.google.com",
    "http://www.microsoft.com",
    "http://www.github.com"
};

// Enable append mode for URL completion
autoComplete1.AutoCompleteMode = AutoCompleteMode.SuggestAppend;

this.Controls.Add(autoComplete1);
```

## Key Properties Reference

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `DataSource` | object | null | Data source for suggestions (array, DataTable, etc.) |
| `ParentForm` | Form | null | Parent form containing the control (required) |
| `AutoCompleteMode` | AutoCompleteMode | Suggest | Behavior mode: None, Suggest, Append, SuggestAppend |
| `DisplayMember` | string | "" | Property name to display from data source |
| `ValueMember` | string | "" | Property name for internal value |
| `Columns` | AutoCompleteDataColumnInfoCollection | - | Column configuration for multi-column display |
| `Style` | AutoCompleteStyle | Default | Visual style of the control |
| `Text` | string | "" | Current text value |
| `SelectedValue` | object | null | Currently selected value |
| `CharacterCasing` | CharacterCasing | Normal | Text casing: Normal, Upper, Lower |
| `LoadOnDemand` | bool | false | Load suggestions on demand |
| `AutoCompleteControl` | AutoCompletePopup | - | Access to underlying popup control |

## Events

Common events for the AutoComplete control:

- **AutoCompleteValueChanged**: Triggered when selected value changes
- **AutoCompleteCustomize**: Before displaying the dropdown list
- **BeforeCustomization**: Before applying customization
- **TextChanged**: When text content changes
- **SelectedIndexChanged**: When selection changes
- **GotFocus**: When control receives focus
- **LostFocus**: When control loses focus

## Best Practices

1. **Always Set ParentForm**: The `ParentForm` property is mandatory for the dropdown to work properly

2. **Use Appropriate Mode**: Choose the right `AutoCompleteMode`:
   - `Suggest`: Show dropdown only
   - `Append`: Auto-complete text only
   - `SuggestAppend`: Both dropdown and text completion

3. **Optimize Large Datasets**: Use `LoadOnDemand` for large data sources to improve performance

4. **Multi-Column for Complex Data**: Use multi-column display when showing related information

5. **Handle Events Properly**: Use `AutoCompleteValueChanged` to respond to user selections

6. **Clear Data Appropriately**: Call `ResetItems()` or set `DataSource = null` to clear suggestions

7. **Consider Character Casing**: Set `CharacterCasing` based on data type (e.g., Upper for state codes)

8. **Theme Consistency**: Use matching visual styles across all Syncfusion controls

## Visual Styles

The control supports multiple visual themes:
- Default
- Office2016Colorful
- Office2016White
- Office2016Black
- Office2016DarkGray
- Metro
- Office2007
- Office2010
- VS2010

```csharp
autoComplete1.Style = AutoCompleteStyle.Office2016Colorful;
```

## Framework Support

- .NET Framework 4.5 and above
- .NET 6.0, .NET 7.0, .NET 8.0 (Windows)
- .NET Core 3.1 (Windows)

## Additional Resources

- [Syncfusion AutoComplete Documentation](https://help.syncfusion.com/windowsforms/autocomplete/overview)
- [API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.AutoComplete.html)
- [Knowledge Base Articles](https://www.syncfusion.com/kb/windowsforms/autocomplete)
- [GitHub Samples](https://github.com/syncfusion/winforms-demos)

## Related Controls

- **ComboBoxAdv**: Advanced combo box with more customization options
- **TextBoxExt**: Extended text box with additional features
- **AutoCompleteControl**: Standalone popup control for custom scenarios
- **MultiColumnComboBox**: Dedicated multi-column dropdown control

## Troubleshooting

**Issue**: Dropdown doesn't appear
- Ensure `ParentForm` property is set
- Check that `DataSource` contains valid data
- Verify control is added to form's Controls collection

**Issue**: Multi-column not displaying
- Set appropriate `AutoCompleteStyle`
- Add columns to `Columns` collection
- Ensure DataSource has matching column names

**Issue**: Performance issues with large datasets
- Enable `LoadOnDemand` property
- Reduce the number of columns displayed
- Consider filtering data source before binding

**Issue**: Styling not applied
- Ensure Syncfusion theme DLLs are referenced
- Apply style after setting DataSource
- Check for conflicting custom drawing code
