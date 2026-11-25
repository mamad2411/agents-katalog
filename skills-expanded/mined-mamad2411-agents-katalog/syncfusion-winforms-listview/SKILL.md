---
name: syncfusion-winforms-listview
description: Guide for implementing Syncfusion SfListView control in Windows Forms for creating list-based UIs with data binding, grouping, sorting, filtering, and selection capabilities. Use when building applications with item collections, Explorer views, contact lists, or product catalogs with sortable/filterable lists. Covers data binding, checkbox lists, grouped lists, filtered lists, and rich data display for list interfaces.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing ListView

Guide for implementing Syncfusion® Windows Forms ListView (SfListView) — a high-performance list control for creating rich list-based user interfaces with data binding, grouping, sorting, filtering, selection modes, checkbox selection, and extensive customization options.

## When to Use This Skill

Use this skill when you need to:
- **Create list views** with data binding to collections in Windows Forms applications
- **Display item collections** with grouping, sorting, and filtering capabilities
- **Implement item selection** with single or multiple selection modes
- **Add checkbox selection** for multi-item operations
- **Build searchable lists** with filtering and sorting
- **Create grouped lists** with expandable/collapsible groups
- **Customize item appearance** with templates, styles, and themes
- **Support accessibility** with UIAutomation and keyboard navigation
- **Build data-driven UIs** similar to file explorers, contact lists, or product catalogs
- **Handle large datasets** with optimized view recycling

This skill covers complete ListView implementation including setup, data binding, selection, data operations, customization, and advanced features.

## Component Overview

The **SfListView** control is a high-performance list view control that provides:

- **Data Binding** - Support for IEnumerable data sources with automatic refresh
- **Selection Modes** - Single, multiple, or none with events
- **Checkbox Selection** - Multi-select with checkbox, select all, recursive checking
- **Grouping** - Organize items by property with expandable groups
- **Sorting** - Ascending/descending sort with custom comparers
- **Filtering** - Filter items by criteria with live updates
- **Item Sizing** - Auto-fit or fixed item heights
- **Customization** - Styles, templates, themes (Office 2016)
- **Header/Footer** - Custom header and footer views
- **Scrollbar Customization** - Appearance and behavior
- **Localization** - Multi-language support
- **Accessibility** - UIAutomation support for screen readers

### Control Structure

```
SfListView
├── Header View (optional) - Top content area
├── Groups - Collapsible item groups
│   ├── Group Header - Group title and expand/collapse
│   └── Items - Data items in group
├── Items - Flat list of data-bound items
└── Footer View (optional) - Bottom content area
```

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and dependencies
- Adding SfListView via designer and code
- Creating data object classes
- Basic data binding with DataSource
- First list view example

### Data Binding

📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding to IEnumerable data sources
- DataSource property configuration
- DisplayMember and ValueMember
- ObservableCollection for live updates
- Refreshing data programmatically
- Data source change handling

### Selection

📄 **Read:** [references/selection.md](references/selection.md)
- SelectionMode (None, One, MultiSimple, MultiExtended)
- SelectedItem and SelectedItems properties
- SelectedIndex and SelectedIndices
- SelectionChanged event
- Programmatic selection
- Selection appearance customization

📄 **Read:** [references/checkbox-selection.md](references/checkbox-selection.md)
- CheckBoxMode property
- CheckedItems collection
- CheckedIndices property
- CheckStateChanged event
- Select all functionality
- Recursive checking in grouped lists
- Checkbox appearance customization

### Data Operations

📄 **Read:** [references/data-operations.md](references/data-operations.md)
- Grouping items by property
- GroupDescriptor configuration
- Sorting items (ascending, descending)
- Custom sort comparers
- Filtering with predicates
- Filter criteria and conditions
- LiveDataUpdateMode for real-time updates

### Customization

📄 **Read:** [references/appearance.md](references/appearance.md)
- Style property customization
- ItemStyle and GroupHeaderStyle
- Theme support (Office 2016, etc.)
- Colors, fonts, and borders
- DrawItem event for custom rendering
- Selection colors and focus indicators

📄 **Read:** [references/item-sizing-headers.md](references/item-sizing-headers.md)
- ItemHeight property
- GroupHeaderHeight property
- AutoFitMode (Height, DynamicHeight)
- Header view customization
- Footer view customization
- Dynamic height calculation

### Advanced Features

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Localization and culture support
- UIAutomation for accessibility
- Scrollbar customization
- Performance optimization techniques
- View recycling strategy
- Memory management

## Quick Start Example

### Basic ListView with Data Binding

```csharp
using System;
using System.Collections.Generic;
using System.Windows.Forms;
using Syncfusion.WinForms.ListView;

namespace ListViewDemo
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            InitializeListView();
        }
        
        private void InitializeListView()
        {
            // Create and configure ListView
            SfListView listView = new SfListView();
            listView.Dock = DockStyle.Fill;
            listView.Size = new Size(400, 500);
            
            // Set data source
            listView.DataSource = GetCountryData();
            listView.DisplayMember = "CountryName";
            
            // Enable selection
            listView.SelectionMode = Syncfusion.WinForms.ListView.Enums.SelectionMode.One;
            listView.SelectionChanged += ListView_SelectionChanged;
            
            // Add to form
            this.Controls.Add(listView);
        }
        
        private List<CountryInfo> GetCountryData()
        {
            return new List<CountryInfo>
            {
                new CountryInfo { CountryName = "United States", Continent = "North America" },
                new CountryInfo { CountryName = "Canada", Continent = "North America" },
                new CountryInfo { CountryName = "Germany", Continent = "Europe" },
                new CountryInfo { CountryName = "Japan", Continent = "Asia" },
                new CountryInfo { CountryName = "Australia", Continent = "Oceania" }
            };
        }
        
        private void ListView_SelectionChanged(object sender, EventArgs e)
        {
            if (sender is SfListView listView && listView.SelectedItem != null)
            {
                var selected = listView.SelectedItem as CountryInfo;
                MessageBox.Show($"Selected: {selected.CountryName}");
            }
        }
    }
    
    public class CountryInfo
    {
        public string CountryName { get; set; }
        public string Continent { get; set; }
    }
}
```

## Common Patterns

### Pattern 1: Grouped and Sorted List

```csharp
// Create ListView
SfListView listView = new SfListView();
listView.DataSource = GetCountryData();
listView.DisplayMember = "CountryName";

// Add grouping by continent
listView.View.GroupDescriptors.Add(new GroupDescriptor()
{
    PropertyName = "Continent"
});

// Add sorting by country name
listView.View.SortDescriptors.Add(new SortDescriptor()
{
    PropertyName = "CountryName",
    Direction = Syncfusion.Data.ListSortDirection.Ascending
});
```

### Pattern 2: Checkbox Selection with Select All

```csharp
// Enable checkbox mode
listView.CheckBoxMode = CheckBoxMode.Default;

// Handle checked items changes
listView.CheckStateChanged += (s, e) =>
{
    MessageBox.Show($"Checked items: {listView.CheckedItems.Count}");
};

// Add Select All button
Button selectAllBtn = new Button { Text = "Select All" };
selectAllBtn.Click += (s, e) =>
{
    // Check all items
    for (int i = 0; i < listView.View.Items.Count; i++)
    {
        listView.SetItemCheckState(i, CheckState.Checked);
    }
};
```

### Pattern 3: Filtered and Searchable List

```csharp
// Add TextBox for search
TextBox searchBox = new TextBox();
searchBox.TextChanged += (s, e) =>
{
    string searchText = searchBox.Text.ToLower();
    
    // Apply filter
    listView.View.Filter = item =>
    {
        if (item is CountryInfo country)
        {
            return country.CountryName.ToLower().Contains(searchText);
        }
        return false;
    };
    
    // Refresh view
    listView.View.RefreshFilter();
};
```

### Pattern 4: Custom Item Styling

```csharp
// Customize item appearance
listView.Style.ItemStyle.BackColor = Color.White;
listView.Style.ItemStyle.HoverBackColor = Color.LightBlue;
listView.Style.ItemStyle.SelectedItemBackColor = Color.Blue;
listView.Style.ItemStyle.SelectedItemForeColor = Color.White;
listView.Style.ItemStyle.Font = new Font("Segoe UI", 10f);

// Customize group headers
listView.Style.GroupHeaderStyle.BackColor = Color.LightGray;
listView.Style.GroupHeaderStyle.ForeColor = Color.Black;
listView.Style.GroupHeaderStyle.Font = new Font("Segoe UI", 10f, FontStyle.Bold);
```

### Pattern 5: ObservableCollection with Live Updates

```csharp
using System.Collections.ObjectModel;
using System.ComponentModel;

public class CountryViewModel : INotifyPropertyChanged
{
    private ObservableCollection<CountryInfo> countries;
    
    public ObservableCollection<CountryInfo> Countries
    {
        get { return countries; }
        set
        {
            countries = value;
            OnPropertyChanged(nameof(Countries));
        }
    }
    
    public CountryViewModel()
    {
        Countries = new ObservableCollection<CountryInfo>
        {
            new CountryInfo { CountryName = "USA", Continent = "North America" }
        };
    }
    
    // Add item - ListView updates automatically
    public void AddCountry(CountryInfo country)
    {
        Countries.Add(country);
    }
    
    public event PropertyChangedEventHandler PropertyChanged;
    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

// Bind to ListView
var viewModel = new CountryViewModel();
listView.DataSource = viewModel.Countries;
listView.DisplayMember = "CountryName";
```

## Key Properties

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| **DataSource** | object | Gets/sets the data source (IEnumerable) |
| **DisplayMember** | string | Property name to display in items |
| **ValueMember** | string | Property name for item values |
| **SelectedItem** | object | Currently selected item |
| **SelectedItems** | List<object> | Collection of selected items |
| **CheckedItems** | List<object> | Collection of checked items |

### Selection Properties

| Property | Type | Description |
|----------|------|-------------|
| **SelectionMode** | SelectionMode | None, One, MultiSimple, MultiExtended |
| **SelectedIndex** | int | Index of selected item |
| **SelectedIndices** | List<int> | Indices of selected items |
| **AllowMultiSelection** | bool | Enable multiple selection |

### Checkbox Properties

| Property | Type | Description |
|----------|------|-------------|
| **CheckBoxMode** | CheckBoxMode | None, Default, SelectAll |
| **CheckedIndices** | List<int> | Indices of checked items |
| **RecursiveCheckState** | bool | Enable recursive checking in groups |
| **ShowCheckBox** | bool | Show/hide checkboxes |

### Appearance Properties

| Property | Type | Description |
|----------|------|-------------|
| **Style** | ListViewStyle | Overall style configuration |
| **ItemHeight** | int | Height of each item |
| **GroupHeaderHeight** | int | Height of group headers |
| **AutoFitMode** | AutoFitMode | None, Height, DynamicHeight |

### Data Operation Properties

| Property | Type | Description |
|----------|------|-------------|
| **View** | DataView | Access to grouping, sorting, filtering |
| **LiveDataUpdateMode** | LiveDataUpdateMode | AllowDataShaping, AllowSummary, Default |

### Events

| Event | Description |
|-------|-------------|
| **SelectionChanged** | Fired when selection changes |
| **CheckStateChanged** | Fired when checkbox state changes |
| **ItemsSourceChanged** | Fired when DataSource changes |
| **DrawItem** | Custom drawing for items |
| **QueryItemHeight** | Dynamic item height calculation |

## Common Use Cases

### 1. Contact List Application
Display contacts with grouping by first letter, search functionality, and selection for actions.

### 2. Product Catalog Browser
Show products with filtering by category, sorting by price, and checkbox selection for cart.

### 3. File Explorer View
Create file/folder lists with icons, grouping by type, sorting by name/date/size.

### 4. Task Management Lists
Display tasks with checkbox completion, grouping by priority/status, filtering by date.

### 5. Email Client Inbox
Show email messages with selection, sorting by date, filtering by read/unread status.

### 6. Customer Order Lists
Display orders with grouping by status, sorting by date, selection for details.

### 7. Settings Configuration UI
Create lists of settings with checkbox selection for enable/disable features.

### 8. Data Grid Alternative
Use ListView for simpler list-based data display without complex grid features.

## Related Components

- **DataGrid** - For tabular data with columns
- **TreeView** - For hierarchical data structures
- **ComboBox** - For dropdown selection from list
- **CheckedListBox** - Simple checkbox list without advanced features

## Best Practices

1. **Data Binding**
   - Use ObservableCollection for automatic UI updates
   - Implement INotifyPropertyChanged for item property changes
   - Set DisplayMember and ValueMember for clarity

2. **Performance**
   - Enable view recycling (enabled by default)
   - Use AutoFitMode carefully with large datasets
   - Avoid custom DrawItem for simple scenarios
   - Use filtering/grouping instead of recreating data source

3. **Selection**
   - Handle SelectionChanged event for user actions
   - Use appropriate SelectionMode for use case
   - Clear selection when data source changes if needed

4. **Grouping and Filtering**
   - Use View.GroupDescriptors for grouping
   - Set View.Filter predicate for filtering
   - Call RefreshFilter() after changing filter criteria
   - Use SortDescriptors for consistent ordering

5. **Customization**
   - Use Style properties before custom drawing
   - Apply themes for consistent appearance
   - Use ItemStyle and GroupHeaderStyle for basic customization
   - Only use DrawItem for complex custom rendering

6. **Accessibility**
   - Enable UIAutomation support
   - Provide meaningful DisplayMember values
   - Support keyboard navigation
   - Test with screen readers

## Troubleshooting

### Items Not Displaying
- Verify DataSource is set and not null
- Check DisplayMember matches property name (case-sensitive)
- Ensure data objects are public properties
- Verify ListView size is not zero

### Selection Not Working
- Check SelectionMode is not None
- Verify SelectionChanged event is subscribed
- Ensure items are enabled
- Check if AllowMultiSelection matches SelectionMode

### Grouping/Filtering Not Applied
- Call View.RefreshFilter() after filter changes
- Check GroupDescriptor PropertyName is correct
- Verify data property exists and is accessible
- Ensure LiveDataUpdateMode is appropriate

### Performance Issues
- Reduce AutoFitMode usage for large lists
- Avoid complex DrawItem logic
- Use view recycling (default behavior)
- Consider virtualization for very large datasets

### Checkbox Issues
- Verify CheckBoxMode is not None
- Check RecursiveCheckState setting for grouped lists
- Use CheckStateChanged event, not SelectionChanged
- Ensure CheckedItems vs SelectedItems distinction

---

**Next Steps:** Navigate to specific reference documents based on your implementation needs. Start with [getting-started.md](references/getting-started.md) for initial setup, then explore data binding, selection, and data operations as needed.
