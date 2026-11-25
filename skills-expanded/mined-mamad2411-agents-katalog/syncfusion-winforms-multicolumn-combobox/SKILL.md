---
name: syncfusion-winforms-multicolumn-combobox
description: Implement and configure Syncfusion MultiColumnComboBox control in Windows Forms - an advanced combobox with multiple columns in dropdown and virtual data binding for large datasets. Use when creating dropdown lists with multiple data fields, DataSource binding, DisplayMember/ValueMember configuration, or column headers in dropdown. Covers filtered dropdown lists and replacing standard ComboBox with multi-column alternatives.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Multi-Column ComboBoxes (MultiColumnComboBox)

An advanced combobox control for Windows Forms that displays multiple columns in the dropdown list with virtual data binding support for instantaneous loading of large datasets.

## When to Use This Skill

Use this skill when you need to:
- **Multi-Column Dropdowns**: Display multiple data fields in dropdown (like DataGridView in dropdown)
- **Large Dataset Binding**: Bind to large datasources with virtual rendering for performance
- **Data Lookup**: Show related fields (ID, Name, Description, Category) in dropdown
- **Entity Selection**: Select records with multiple visible properties
- **Filtered Dropdowns**: Apply custom filtering across all columns
- **Styled Comboboxes**: Apply Office themes (2003-2019) to dropdown controls
- **DataSource Binding**: Use DataSource, DisplayMember, and ValueMember properties
- **ComboBox Replacement**: Replace standard ComboBox with richer multi-column display

## Component Overview

The **MultiColumnComboBox** is based on ComboBoxBase and provides:
- Multiple columns in dropdown list
- Virtual data binding for large datasets (instantaneous loading)
- Automatic display of all fields in datasource
- DataSource, DisplayMember, and ValueMember properties
- Column headers with ShowColumnHeader property
- Custom filtering across all columns
- Grid-based dropdown (GridListControl)
- Cannot manually add items (data binding only)

**Key Capabilities:**
- `DataSource` property for binding data (DataTable, DataView, DataSet, List<T>)
- `DisplayMember` and `ValueMember` for column selection
- `ShowColumnHeader` property for displaying column headers
- `AllowFiltering` property for enabling custom filtering
- `Style` property for applying Office visual themes
- `AlphaBlendSelectionColor` for customizing selection appearance
- `DropDownWidth` for controlling dropdown width

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** Starting new implementation, first-time setup, basic control creation

**Topics covered:**
- Assembly and namespace requirements (Syncfusion.Windows.Forms.Tools)
- Adding via designer (drag-and-drop from toolbox)
- Adding via code (programmatic creation)
- Basic MultiColumnComboBox instantiation
- Form integration
- Initial setup steps

---

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)

**When to read:** Binding to datasources, configuring DataSource/DisplayMember/ValueMember, loading data from databases or XML

**Topics covered:**
- DataSource, DisplayMember, ValueMember properties
- DataView as datasource
- OleDBDataAdapter usage with databases
- Typed DataSet population
- XML data loading (ReadXml)
- Hiding specific columns (Grid.Model.Cols.Hidden)
- Accessing DataRowView for selected items
- Complete data binding examples

---

### Multiple Columns Configuration
📄 **Read:** [references/multiple-columns.md](references/multiple-columns.md)

**When to read:** Configuring columns, enabling/disabling multi-column mode, filtering, dropdown width

**Topics covered:**
- MultiColumn property (enable/disable columns)
- ShowColumnHeader property (display column headers)
- AlphaBlendSelectionColor (selection highlight color)
- DropDownWidth property (dropdown width configuration)
- AllowFiltering property (enable custom filtering)
- Filter property (predicate-based filtering)
- Custom filter implementation
- Default filtering behavior (StartsWith on DisplayMember)

---

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)

**When to read:** Applying visual themes, customizing appearance, Office theme configuration

**Topics covered:**
- Style property (9 visual styles)
- Office2003, OfficeXP, VS2005 styles
- Office2007 with color schemes (Blue, Silver, Black)
- Metro, Office2016 variants (Colorful, White, Black, DarkGray)
- Office2007ColorTheme property
- Custom colors with ApplyManagedColors method
- Managed theme configuration
- Complete styling examples

---

### Event Handling
📄 **Read:** [references/event-handling.md](references/event-handling.md)

**When to read:** Handling selection changes, responding to user interactions, accessing selected data

**Topics covered:**
- SelectionChangedCommitted event
- SelectedValueChanged event
- SelectedIndexChanged event
- Event occurrence scenarios and order
- Accessing selected item data (DataRowView)
- Setting text based on selection
- Complete event handler examples

---

## Quick Start Example

### Multi-Column Employee Selector with Data Binding

```csharp
using Syncfusion.Windows.Forms.Tools;
using System.Data;

// Create DataTable with employee data
DataTable employeeData = new DataTable("Employees");
employeeData.Columns.Add("EmployeeID");
employeeData.Columns.Add("FirstName");
employeeData.Columns.Add("LastName");
employeeData.Columns.Add("Department");
employeeData.Columns.Add("Position");

// Add sample data
employeeData.Rows.Add("1001", "John", "Smith", "Engineering", "Developer");
employeeData.Rows.Add("1002", "Mary", "Johnson", "Sales", "Manager");
employeeData.Rows.Add("1003", "Robert", "Williams", "HR", "Specialist");
employeeData.Rows.Add("1004", "Sarah", "Davis", "Marketing", "Coordinator");

// Create and configure MultiColumnComboBox
MultiColumnComboBox employeeCombo = new MultiColumnComboBox();
employeeCombo.Location = new Point(20, 20);
employeeCombo.Size = new Size(300, 21);

// Bind data
employeeCombo.DataSource = employeeData;
employeeCombo.DisplayMember = "FirstName";
employeeCombo.ValueMember = "EmployeeID";

// Configure appearance
employeeCombo.ShowColumnHeader = true;
employeeCombo.Style = VisualStyle.Office2016Colorful;
employeeCombo.DropDownWidth = 500;

// Add to form
this.Controls.Add(employeeCombo);
```

```vbnet
Imports Syncfusion.Windows.Forms.Tools
Imports System.Data

' Create DataTable with employee data
Dim employeeData As New DataTable("Employees")
employeeData.Columns.Add("EmployeeID")
employeeData.Columns.Add("FirstName")
employeeData.Columns.Add("LastName")
employeeData.Columns.Add("Department")
employeeData.Columns.Add("Position")

' Add sample data
employeeData.Rows.Add("1001", "John", "Smith", "Engineering", "Developer")
employeeData.Rows.Add("1002", "Mary", "Johnson", "Sales", "Manager")
employeeData.Rows.Add("1003", "Robert", "Williams", "HR", "Specialist")
employeeData.Rows.Add("1004", "Sarah", "Davis", "Marketing", "Coordinator")

' Create and configure MultiColumnComboBox
Dim employeeCombo As New MultiColumnComboBox()
employeeCombo.Location = New Point(20, 20)
employeeCombo.Size = New Size(300, 21)

' Bind data
employeeCombo.DataSource = employeeData
employeeCombo.DisplayMember = "FirstName"
employeeCombo.ValueMember = "EmployeeID"

' Configure appearance
employeeCombo.ShowColumnHeader = True
employeeCombo.Style = VisualStyle.Office2016Colorful
employeeCombo.DropDownWidth = 500

' Add to form
Me.Controls.Add(employeeCombo)
```

---

## Common Patterns

### Pattern 1: Database Lookup with OleDbDataAdapter

```csharp
using System.Data.OleDb;

// Create data adapter and dataset
OleDbDataAdapter adapter = new OleDbDataAdapter(
    "SELECT CustomerID, CompanyName, ContactName, Country FROM Customers", 
    connectionString);
DataSet dataSet = new DataSet();
adapter.Fill(dataSet, "Customers");

// Bind to MultiColumnComboBox
multiColumnComboBox1.DataSource = dataSet.Tables["Customers"];
multiColumnComboBox1.DisplayMember = "CompanyName";
multiColumnComboBox1.ValueMember = "CustomerID";
multiColumnComboBox1.ShowColumnHeader = true;
multiColumnComboBox1.DropDownWidth = 600;
```

### Pattern 2: Custom Filtering by Any Column

```csharp
// Enable filtering
multiColumnComboBox1.AllowFiltering = true;

// Handle text changed for custom filter
multiColumnComboBox1.TextChanged += (sender, e) =>
{
    multiColumnComboBox1.Filter = FilterRecords;
};

// Custom filter predicate
private bool FilterRecords(object o)
{
    var item = o as DataRowView;
    if (item != null)
    {
        string searchText = multiColumnComboBox1.TextBox.Text.ToLower();
        
        // Filter by any column
        return item["ProductName"].ToString().ToLower().Contains(searchText) ||
               item["Category"].ToString().ToLower().Contains(searchText);
    }
    return false;
}
```

### Pattern 3: Hide Specific Columns and Get Selected Data

```csharp
// Load data
DataTable products = GetProductData();
multiColumnComboBox1.DataSource = products;
multiColumnComboBox1.DisplayMember = "ProductName";
multiColumnComboBox1.ValueMember = "ProductID";

// Hide internal ID columns
multiColumnComboBox1.ListBox.Grid.Model.Cols.Hidden["ProductID"] = true;
multiColumnComboBox1.ListBox.Grid.Model.Cols.Hidden["SupplierID"] = true;

// Handle selection to get all column data
multiColumnComboBox1.SelectedValueChanged += (sender, e) =>
{
    if (multiColumnComboBox1.SelectedIndex != -1)
    {
        DataRowView row = multiColumnComboBox1.Items[multiColumnComboBox1.SelectedIndex] as DataRowView;
        
        string productName = row["ProductName"].ToString();
        decimal price = Convert.ToDecimal(row["Price"]);
        string category = row["Category"].ToString();
        
        MessageBox.Show($"Selected: {productName}\nPrice: {price:C}\nCategory: {category}");
    }
};
```

---

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| **DataSource** | object | Data source for the combobox (DataTable, DataView, DataSet, List<T>) |
| **DisplayMember** | string | Name of the data source property to display in the text area |
| **ValueMember** | string | Name of the data source property to use as the value |
| **MultiColumn** | bool | Enables/disables multiple columns (true by default) |
| **ShowColumnHeader** | bool | Shows or hides column headers in dropdown |
| **AllowFiltering** | bool | Enables custom filtering support |
| **Filter** | Predicate<object> | Custom filter predicate for filtering items |
| **Style** | VisualStyle | Visual theme (Office2003, OfficeXP, VS2005, Office2007, Metro, Office2016*) |
| **Office2007ColorTheme** | Office2007Theme | Office 2007 color scheme (Blue, Silver, Black, Managed) |
| **AlphaBlendSelectionColor** | Color | Color for alpha-blended selection highlighting |
| **DropDownWidth** | int | Width of the dropdown popup in pixels |
| **ListBox.Grid** | GridListControl | Access to the underlying grid for column customization |

---

## Common Use Cases

1. **Employee Lookup**: Select employees showing ID, Name, Department, Position in dropdown
2. **Customer Selection**: Display customer records with multiple fields (Name, Company, Contact, Country)
3. **Product Catalog**: Select products showing Code, Name, Category, Price, Stock
4. **Invoice Line Items**: Choose items displaying SKU, Description, Unit Price, Available Quantity
5. **Database Record Picker**: Any scenario requiring selection from multi-field database records
6. **Master-Detail Forms**: Parent record selection with related data visible in dropdown
7. **Data Entry Assistance**: Lookup helper showing context from related fields
8. **Filtered Search**: Type-ahead search across multiple columns for faster selection

---

## Additional Resources

- [MultiColumnComboBox Control on Syncfusion Help](https://help.syncfusion.com/windowsforms/multicolumn-combobox/overview)
- [Syncfusion.Windows.Forms.Tools Namespace](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.html)
- [MultiColumnComboBox API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.MultiColumnComboBox.html)
- [ComboBoxBase API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.ComboBoxBase.html)
