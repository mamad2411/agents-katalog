---
name: syncfusion-winforms-combobox
description: Implement and customize Syncfusion Windows Forms SfComboBox control with data binding, autocomplete, multi-selection, filtering, and tokens. Use this when working with WinForms combobox, dropdown, SfComboBox, autocomplete textbox, multi-select dropdown, token input, combobox data binding, dropdown filtering, or combobox customization in Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing ComboBoxes

This skill explains how to implement and customize the Syncfusion Windows Forms `SfComboBox` control.

## When to Use This Skill

- Use when the user needs a combobox/dropdown control in Windows Forms applications
- Use when implementing autocomplete functionality with Suggest, Append, or SuggestAppend modes
- Use when enabling multi-selection with checkboxes or token-based selection
- Use when binding combobox to data sources (lists, databases, LINQ to SQL)
- Use when implementing filtering or sorting in dropdown lists
- Use when customizing dropdown appearance, watermarks, or themes
- Use when adding custom controls to dropdown headers/footers
- Use when implementing token-based multi-selection (chip-style inputs)

## Navigation Guide

Follow the links below to open focused reference pages for each task.

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and dependencies
- Creating SfComboBox via designer or code
- Basic data binding setup
- Quick autocomplete example
- Quick multi-selection example

### Overview
📄 **Read:** [references/overview.md](references/overview.md)
- Component features and capabilities
- Comparison with ComboBoxAdv, MultiSelectionComboBox, ComboBoxAutoComplete
- API comparison table
- When to use SfComboBox vs alternatives

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- DataSource, DisplayMember, ValueMember properties
- Binding to custom objects and collections
- Binding from Microsoft Access database
- Binding from LINQ to SQL classes
- Complex data binding scenarios

### AutoComplete
📄 **Read:** [references/autocomplete.md](references/autocomplete.md)
- AutoCompleteMode: Suggest, Append, SuggestAppend
- Case-sensitive autocomplete
- AutoCompleteSuggestMode: StartsWith, Contains
- Setting autocomplete delay
- Complete code examples

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Single selection (SelectedIndex, SelectedValue, SelectedItem)
- SelectedIndexChanged and SelectedValueChanged events
- Multi-selection mode with checkboxes
- Select all feature
- Delimiter character customization
- Tooltip for selected items
- Clear button customization

### Token Support
📄 **Read:** [references/token.md](references/token.md)
- EnableToken property for chip-style selection
- Token appearance customization (TokenStyle)
- Adding and removing tokens
- Keyboard navigation for tokens
- SelectedValueChanged event for token tracking

### Filtering
📄 **Read:** [references/filtering.md](references/filtering.md)
- Filter property with custom predicates
- RefreshFilter method
- Complete filtering example
- Custom filter conditions

### Sorting
📄 **Read:** [references/sorting.md](references/sorting.md)
- SortDescriptors property
- Ascending and descending sort
- Custom comparer support

### Dropdown Customization
📄 **Read:** [references/dropdown.md](references/dropdown.md)
- MaxDropDownItems for limiting visible items
- AllowDropDownResize for resize gripper
- DropDownOpening and DropDownClosing events
- DropDownPosition customization
- DropDownWidth customization
- Loading custom header/footer controls
- Complete custom control example

### Watermark
📄 **Read:** [references/watermark.md](references/watermark.md)
- AllowNull property for null value support
- Watermark text customization
- WatermarkForeColor styling

### Appearance & Styling
📄 **Read:** [references/appearance.md](references/appearance.md)
- Visual styles and theming
- BackColor, ForeColor customization
- Border and font customization
- Office 2016 themes

### Editing
📄 **Read:** [references/editing.md](references/editing.md)
- DropDownStyle property
- Edit behavior customization
- Read-only mode

### Item Height
📄 **Read:** [references/item-height.md](references/item-height.md)
- ItemHeight property
- Customizing dropdown item heights

### Localization
📄 **Read:** [references/localization.md](references/localization.md)
- Culture-specific formatting
- Resource file integration

### UI Automation
📄 **Read:** [references/ui-automation.md](references/ui-automation.md)
- Accessibility features
- Screen reader support
- Keyboard navigation

## Quick Start

Minimal `SfComboBox` example (C#):

```csharp
using Syncfusion.WinForms.ListView;

namespace WindowsFormsApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            
            // Create SfComboBox
            SfComboBox sfComboBox1 = new SfComboBox();
            sfComboBox1.Location = new Point(20, 20);
            sfComboBox1.Size = new Size(200, 28);
            
            // Bind data
            List<string> states = new List<string> { "Alaska", "Arizona", "California", "Colorado", "Delaware" };
            sfComboBox1.DataSource = states;
            
            this.Controls.Add(sfComboBox1);
        }
    }
}
```

With autocomplete:

```csharp
sfComboBox1.AutoCompleteMode = AutoCompleteMode.SuggestAppend;
sfComboBox1.AutoCompleteSuggestMode = AutoCompleteSuggestMode.Contains;
```

With multi-selection:

```csharp
sfComboBox1.ComboBoxMode = ComboBoxMode.MultiSelection;
sfComboBox1.AllowSelectAll = true;
```

## Common Patterns

### Pattern 1: Data Binding with Custom Objects
```csharp
public class USState
{
    public string LongName { get; set; }
    public string ShortName { get; set; }
}

List<USState> states = new List<USState>
{
    new USState { LongName = "California", ShortName = "CA" },
    new USState { LongName = "Texas", ShortName = "TX" }
};

sfComboBox1.DataSource = states;
sfComboBox1.DisplayMember = "LongName";
sfComboBox1.ValueMember = "ShortName";
```

### Pattern 2: Multi-Selection with Tokens
```csharp
sfComboBox1.EnableToken = true;
sfComboBox1.Style.TokenStyle.BackColor = Color.LightBlue;
sfComboBox1.Style.TokenStyle.BorderColor = Color.Blue;
```

### Pattern 3: Custom Dropdown Header
```csharp
sfComboBox1.DropDownListView.ShowHeader = true;
TextBox searchBox = new TextBox { Height = 25 };
sfComboBox1.DropDownListView.HeaderControl = searchBox;
```

### Pattern 4: Filtering with Predicate
```csharp
sfComboBox1.DropDownListView.View.Filter = (data) =>
{
    return ((USState)data).LongName.StartsWith("C");
};
sfComboBox1.DropDownListView.View.RefreshFilter();
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| DataSource | object | Bind to IEnumerable data source |
| DisplayMember | string | Property name to display |
| ValueMember | string | Property name for value |
| AutoCompleteMode | enum | Suggest, Append, SuggestAppend, None |
| ComboBoxMode | enum | SingleSelection, MultiSelection |
| EnableToken | bool | Enable token-based selection |
| AllowSelectAll | bool | Show "Select All" in multi-select |
| Watermark | string | Placeholder text when empty |
| MaxDropDownItems | int | Max visible items in dropdown |
| ShowClearButton | bool | Show clear button when selected |
| ThemeName | string | Apply visual theme |

## Common Use Cases

### Use Case 1: Country/State Selector
Implement a country or state dropdown with autocomplete for quick selection in address forms.

### Use Case 2: Tag/Category Selection
Use multi-selection with tokens for selecting multiple tags or categories in content management systems.

### Use Case 3: Searchable Dropdown
Add a search textbox in the dropdown header to filter large lists dynamically.

### Use Case 4: Dependent Dropdowns
Implement cascading dropdowns where the second dropdown filters based on the first selection.

### Use Case 5: Custom Item Templates
Create custom visual representations for dropdown items with images or multiple text lines.

## Troubleshooting

**Issue:** Autocomplete not working
- **Solution:** Ensure `AutoCompleteMode` is set to `Suggest`, `Append`, or `SuggestAppend` (not `None`)

**Issue:** Multi-selection checkboxes not showing
- **Solution:** Set `ComboBoxMode = ComboBoxMode.MultiSelection`

**Issue:** DataSource not displaying items
- **Solution:** Verify `DisplayMember` matches a public property name in your data objects

**Issue:** Tokens not appearing
- **Solution:** Set `EnableToken = true` and select items from the dropdown

**Issue:** Dropdown not resizing
- **Solution:** Check `AllowDropDownResize` property is `true` (default)

**Issue:** SelectedValue returns null
- **Solution:** Ensure `ValueMember` is set correctly, or use `SelectedItem` directly

**Issue:** Filtering not working
- **Solution:** Call `DropDownListView.View.RefreshFilter()` after setting the Filter predicate

## Related Skills

- [implementing-syncfusion-winforms-components](../../SKILL.md) — parent library router
