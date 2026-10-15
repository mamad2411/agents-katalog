---
name: syncfusion-winforms-editable-listbox
description: Implement and configure Syncfusion Windows Forms EditableList controls for inline list editing. Use this when working with editable list boxes, list controls with add/edit/delete capabilities, or AutoComplete integration. Covers setup, data binding, appearance customization, and styling.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms EditableList

A comprehensive guide for implementing and customizing the EditableList control - a powerful list box component that enables inline editing, item management, and rich customization options for Windows Forms applications.

## When to Use This Skill

Use this skill when the user needs to:

- **Implement an EditableList control** in Windows Forms applications
- **Enable inline editing** of list items directly within the list box
- **Manage dynamic lists** where users can add, edit, or delete items at runtime
- **Populate lists** from DataSource or manual entry
- **Integrate AutoComplete** functionality with the editing TextBox
- **Customize appearance** including embedded controls, scrolling, and layout
- **Apply modern themes** (Metro, Office2016) to the editable list
- **Handle editing events** and user interactions
- **Configure dock padding** and control sizing
- **Set up embedded controls** (Button, TextBox, ListBox) within EditableList

The EditableList control is ideal for scenarios requiring user-editable collections, form data entry, tag management, or any interface where inline list editing improves usability.

## Component Overview

The **EditableList** (also known as Editable ListBox) is a composite control that combines a ListBox, TextBox, and optional Button to provide inline editing capabilities. Users can select items and edit them directly within the list interface.

**Key Capabilities:**
- **Inline Editing**: Click an item to edit it directly in-place
- **DataSource Binding**: Connect to data sources or populate manually
- **Embedded Controls**: Access and configure child Button, TextBox, and ListBox
- **AutoComplete Integration**: Add intelligent text suggestions during editing
- **Modern Styling**: Support for Metro and Office2016 themes with color schemes
- **Flexible Layout**: AutoScroll, dock padding, and size configuration
- **Visual Customization**: Control button visibility and appearance

**Embedded Controls:**
- **Button**: Optional button for additional actions (controlled by WantButton property)
- **TextBox**: Used for inline editing of selected items
- **ListBox**: Contains the list items with full ListBox functionality

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly deployment
- Adding control via Visual Studio designer
- Adding control programmatically via code
- Required namespace imports
- Basic initialization and setup
- Understanding embedded controls

### Populating and Editing the List
📄 **Read:** [references/populating-editing.md](references/populating-editing.md)
- Populating via DataSource binding
- Manual population through property editor
- Runtime editing workflow
- Item selection and inline editing process
- ListBox.Items manipulation
- Complete code examples (C# and VB.NET)

### Appearance and Behavior Configuration
📄 **Read:** [references/appearance-behavior.md](references/appearance-behavior.md)
- Embedded controls overview and access
- AutoScroll configuration for large lists
- Dock padding for layout control
- WantButton property for button visibility
- Control sizing and positioning
- Practical configuration examples

### AutoComplete Integration
📄 **Read:** [references/autocomplete-integration.md](references/autocomplete-integration.md)
- Setting up AutoComplete component
- Associating AutoComplete with EditableList TextBox
- DataSource configuration for suggestions
- AutoCompleteModes options
- Form load event implementation
- Complete integration example

### Styling and Theming
📄 **Read:** [references/styling-themes.md](references/styling-themes.md)
- Visual styles (Default, Metro, Office2016)
- Applying Style property
- Office2016 color schemes (Colorful, White, DarkGray, Black)
- Theme consistency across forms
- Complete styling code examples

## Quick Start

### Basic Implementation (Designer)

1. **Add Control via Toolbox:**
   - Open your form in Visual Studio designer
   - Locate EditableList in the toolbox (Syncfusion Controls section)
   - Drag and drop onto your form
   - Assemblies are added automatically

2. **Configure in Properties Window:**
   - Set Size, Location, and other basic properties
   - Expand ListBox property to configure items
   - Set Style property for modern appearance

### Basic Implementation (Code)

```csharp
using Syncfusion.Windows.Forms.Tools;

namespace MyWinFormsApp
{
    public partial class Form1 : Form
    {
        private EditableList editableList1;
        
        public Form1()
        {
            InitializeComponent();
            SetupEditableList();
        }
        
        private void SetupEditableList()
        {
            // Create and initialize
            this.editableList1 = new EditableList();
            this.editableList1.Location = new System.Drawing.Point(20, 20);
            this.editableList1.Size = new System.Drawing.Size(300, 200);
            
            // Populate items
            this.editableList1.ListBox.Items.AddRange(new object[] {
                "Item 1",
                "Item 2", 
                "Item 3"
            });
            
            // Apply modern style
            this.editableList1.Style = Syncfusion.Windows.Forms.Appearance.Office2016;
            
            // Add to form
            this.Controls.Add(this.editableList1);
        }
    }
}
```

```vbnet
Imports Syncfusion.Windows.Forms.Tools

Public Class Form1
    Private editableList1 As EditableList
    
    Public Sub New()
        InitializeComponent()
        SetupEditableList()
    End Sub
    
    Private Sub SetupEditableList()
        ' Create and initialize
        Me.editableList1 = New EditableList()
        Me.editableList1.Location = New System.Drawing.Point(20, 20)
        Me.editableList1.Size = New System.Drawing.Size(300, 200)
        
        ' Populate items
        Me.editableList1.ListBox.Items.AddRange(New Object() {
            "Item 1",
            "Item 2",
            "Item 3"
        })
        
        ' Apply modern style
        Me.editableList1.Style = Syncfusion.Windows.Forms.Appearance.Office2016
        
        ' Add to form
        Me.Controls.Add(Me.editableList1)
    End Sub
End Class
```

## Common Patterns

### Pattern 1: DataSource Binding

```csharp
// Bind to a data source
List<string> dataSource = new List<string>();
dataSource.Add("Product A");
dataSource.Add("Product B");
dataSource.Add("Product C");

this.editableList1.ListBox.DataSource = dataSource;
```

### Pattern 2: Runtime Editing Workflow

```
User Interaction:
1. Click on an item to select it
2. Click again to enter edit mode (TextBox appears)
3. Edit the text in the TextBox
4. Change focus (click elsewhere, press Tab)
5. List updates automatically with edited value
```

### Pattern 3: Enable AutoScroll for Large Lists

```csharp
// Enable automatic scrollbars
this.editableList1.AutoScroll = true;
this.editableList1.AutoScrollMargin = new System.Drawing.Size(2, 2);
this.editableList1.AutoScrollMinSize = new System.Drawing.Size(3, 3);
```

### Pattern 4: Show Button While Editing

```csharp
// Display button on the right during editing
this.editableList1.WantButton = true;

// Handle button click if needed
this.editableList1.Button.Click += (s, e) => {
    MessageBox.Show("Button clicked!");
};
```

### Pattern 5: Apply Modern Theme

```csharp
// Apply Office2016 theme with color scheme
this.editableList1.Style = Syncfusion.Windows.Forms.Appearance.Office2016;
this.editableList1.Office2016ColorScheme = ScrollBarOffice2016ColorScheme.Colorful;
```

## Key Properties and Events

### Essential Properties

| Property | Description | Example |
|----------|-------------|---------|
| **ListBox** | Access to embedded ListBox control | `editableList1.ListBox.Items.Add("Item")` |
| **TextBox** | Access to editing TextBox control | `editableList1.TextBox.Text` |
| **Button** | Access to optional button control | `editableList1.Button.Click += Handler` |
| **WantButton** | Show/hide button during editing | `editableList1.WantButton = true` |
| **AutoScroll** | Enable automatic scrollbars | `editableList1.AutoScroll = true` |
| **Style** | Visual appearance style | `editableList1.Style = Appearance.Office2016` |
| **DockPadding** | Padding for docked controls | `editableList1.DockPadding.All = 5` |

### Common Events

Access events through embedded controls:

```csharp
// ListBox events
this.editableList1.ListBox.SelectedIndexChanged += ListBox_SelectedIndexChanged;
this.editableList1.ListBox.Click += ListBox_Click;

// TextBox events
this.editableList1.TextBox.TextChanged += TextBox_TextChanged;
this.editableList1.TextBox.Leave += TextBox_Leave;

// Button events (if WantButton = true)
this.editableList1.Button.Click += Button_Click;
```

## Common Use Cases

### Use Case 1: Tag Management System
User needs to manage tags where users can add, edit, and remove tags inline.
→ Use DataSource binding + enable inline editing + add item selection handling

### Use Case 2: Dynamic Category List
User wants a settings form where categories can be edited directly in the list.
→ Use manual item population + WantButton for delete functionality + style for modern UI

### Use Case 3: Email Recipient List
User needs an editable list of email addresses with autocomplete suggestions.
→ Use AutoComplete integration + DataSource for suggestions + validation on TextBox.Leave

### Use Case 4: Todo List Manager
User wants a simple todo list with inline editing capabilities.
→ Use basic setup + runtime editing + handle ListBox events for task completion

### Use Case 5: Preferences Editor
User needs a form where users can edit configuration values in a list format.
→ Use DataSource binding + themed appearance + dock padding for layout

## Tips and Best Practices

1. **Use DataSource for Dynamic Data**: Bind to collections for automatic updates
2. **Handle TextBox.Leave Event**: Validate input when editing completes
3. **Enable AutoScroll**: For lists with many items to prevent overflow
4. **Apply Consistent Theming**: Use the same Style across all controls in your form
5. **Access Embedded Controls**: Configure Button, TextBox, ListBox for full customization
6. **Consider AutoComplete**: Improves user experience for predictable inputs
7. **Test Editing Flow**: Ensure click-to-edit behavior works smoothly
8. **Set Appropriate Sizes**: Give adequate height for comfortable item viewing and editing

## Troubleshooting

**Issue**: Items not editable
→ Ensure proper focus handling and check if TextBox is accessible

**Issue**: Scrollbars not appearing
→ Set AutoScroll = true and configure AutoScrollMinSize

**Issue**: Theme not applying
→ Verify Style property is set and Office2016ColorScheme for Office2016 style

**Issue**: AutoComplete not working
→ Check AutoComplete.SetAutoComplete() is called with correct parameters in Form_Load

**Issue**: Button not visible during editing
→ Set WantButton = true property
