---
name: syncfusion-winforms-checkbox
description: Guide to implement and customize the Syncfusion WinForms CheckBoxAdv control. Use this when working with advanced checkbox controls featuring three states, gradient backgrounds, custom borders, shadow text, or flexible alignment in Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing CheckBoxAdv in Windows Forms

## When to Use This Skill

Use this skill whenever the user needs to:

- Implement advanced checkbox controls in Windows Forms applications
- Create checkboxes with checked, unchecked, and indeterminate states
- Apply gradient backgrounds, custom borders, or shadow text to checkboxes
- Configure checkbox and text alignment independently
- Associate integer or string values with checkbox states
- Handle checkbox state change events
- Bind CheckBoxAdv controls to SQL database fields
- Customize checkbox appearance beyond standard Windows Forms controls
- Implement three-state checkboxes with tristate support
- Create read-only or auto-sized checkbox controls

## Component Overview

The **CheckBoxAdv** is an advanced checkbox control for Windows Forms that extends the standard CheckBox with enhanced visual and functional capabilities. It supports gradient backgrounds, custom borders (2D and 3D), shadow text, independent text and checkbox alignment, image checkboxes, and comprehensive data binding options.

### Key Capabilities

- **Three States**: Checked, Unchecked, and Indeterminate with tristate support
- **Value Association**: Bind integer and string values to each state
- **Visual Customization**: Gradient backgrounds, custom borders, shadow text
- **Flexible Alignment**: Independent positioning of text and checkbox
- **Data Binding**: Connect to SQL databases with BoolValue and IntValue properties
- **Event Handling**: Respond to CheckStateChanged and CheckedChanged events
- **Behavior Control**: AutoHeight, ReadOnlyMode, and focus rectangle options

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet packages
- Adding CheckBoxAdv via designer
- Adding CheckBoxAdv programmatically
- Required namespaces (Syncfusion.Windows.Forms.Tools)
- Basic initialization and setup
- Setting initial checkbox state

### States and Configuration
📄 **Read:** [references/states-and-values.md](references/states-and-values.md)
- CheckState property (Checked, Unchecked, Indeterminate)
- Checked property for boolean state
- Tristate property for three-state mode
- Associating integer values with states (CheckedInt, UncheckedInt, IndeterminateInt)
- Associating string values with states (CheckedString, UncheckedString, IndeterminateString)
- Using BoolValue, IntValue, and StringValue properties
- When to use each value type

### Text and Alignment
📄 **Read:** [references/text-and-alignment.md](references/text-and-alignment.md)
- Text shadow effects (TextShadow, ShadowColor, ShadowOffset)
- Text wrapping with WrapText property
- Text alignment options (TextContentAlignment)
- CheckBox alignment options (CheckAlign)
- Positioning options (TopLeft, MiddleCenter, BottomRight, etc.)
- Combining text and checkbox alignment

### Appearance and Behavior
📄 **Read:** [references/appearance-and-behavior.md](references/appearance-and-behavior.md)
- Focus rectangle visibility (DrawFocusRectangle)
- Automatic height calculation (AutoHeight)
- Read-only mode (ReadOnlyMode)
- Gradient backgrounds (BackgroundStyle, GradientStart, GradientEnd)
- Border styles (Border3DStyle, BorderStyle, BorderSingle)
- Border colors (BorderColor, HotBorderColor)
- Mouse hover effects

### Events and Interactions
📄 **Read:** [references/events.md](references/events.md)
- CheckStateChanged event
- CheckedChanged event
- Event handler patterns
- Responding to state changes
- Event timing and order
- Best practices for event handling

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding to SQL databases
- BoolValue property for bit/boolean fields
- IntValue property for integer fields
- SqlDataAdapter and DataTable usage
- Connection string configuration
- Common data binding patterns
- Troubleshooting binding issues

## Quick Start Example

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create CheckBoxAdv instance
CheckBoxAdv checkBoxAdv1 = new CheckBoxAdv();
checkBoxAdv1.Text = "Enable Feature";
checkBoxAdv1.Size = new Size(150, 25);
checkBoxAdv1.Location = new Point(20, 20);

// Set initial state
checkBoxAdv1.Checked = true;

// Add to form
this.Controls.Add(checkBoxAdv1);

// Handle state changes
checkBoxAdv1.CheckedChanged += (sender, e) => {
    MessageBox.Show($"Checkbox is now: {checkBoxAdv1.Checked}");
};
```

## Common Patterns

### Pattern 1: Three-State Checkbox

**When the user needs** a checkbox with checked, unchecked, and indeterminate states:

```csharp
CheckBoxAdv checkBoxAdv1 = new CheckBoxAdv();
checkBoxAdv1.Text = "Select All";
checkBoxAdv1.Tristate = true;
checkBoxAdv1.CheckState = CheckState.Indeterminate;

checkBoxAdv1.CheckStateChanged += (sender, e) => {
    switch(checkBoxAdv1.CheckState) {
        case CheckState.Checked:
            // Select all items
            break;
        case CheckState.Unchecked:
            // Deselect all items
            break;
        case CheckState.Indeterminate:
            // Partial selection
            break;
    }
};
```

### Pattern 2: Checkbox with Custom Styling

**When the user needs** a visually enhanced checkbox with gradient background and borders:

```csharp
CheckBoxAdv checkBoxAdv1 = new CheckBoxAdv();
checkBoxAdv1.Text = "Styled Checkbox";

// Gradient background
checkBoxAdv1.BackgroundStyle = CheckBoxAdvBackStyle.HorizontalGradient;
checkBoxAdv1.GradientStart = Color.LightBlue;
checkBoxAdv1.GradientEnd = Color.DarkBlue;

// Custom border
checkBoxAdv1.BorderStyle = BorderStyle.FixedSingle;
checkBoxAdv1.BorderColor = Color.Navy;
checkBoxAdv1.HotBorderColor = Color.Red; // On mouse hover

// Shadow text
checkBoxAdv1.TextShadow = true;
checkBoxAdv1.ShadowColor = Color.Gray;
checkBoxAdv1.ShadowOffset = new Point(2, 2);
```

### Pattern 3: Data-Bound Checkbox

**When the user needs** to bind a checkbox to a database field:

```csharp
// For boolean/bit fields
using (SqlConnection conn = new SqlConnection(connectionString)) {
    conn.Open();
    SqlDataAdapter adapter = new SqlDataAdapter("SELECT * FROM Settings", conn);
    DataTable dataTable = new DataTable();
    adapter.Fill(dataTable);
    
    checkBoxAdv1.DataBindings.Add("BoolValue", dataTable, "IsEnabled");
}

// For integer fields (values: -1, 0, 1)
checkBoxAdv1.DataBindings.Add("IntValue", dataTable, "StatusCode");
```

### Pattern 4: Read-Only Checkbox Display

**When the user needs** to display checkbox state without allowing user changes:

```csharp
CheckBoxAdv checkBoxAdv1 = new CheckBoxAdv();
checkBoxAdv1.Text = "Read-Only Status";
checkBoxAdv1.Checked = true;
checkBoxAdv1.ReadOnlyMode = true;
checkBoxAdv1.DrawFocusRectangle = false;
```

## Key Properties

### State Properties
- **Checked** (bool): Gets or sets the checked state (true/false)
- **CheckState** (CheckState): Gets or sets the state (Checked, Unchecked, Indeterminate)
- **Tristate** (bool): Enables three-state mode with user access to indeterminate

### Value Properties
- **BoolValue** (bool): Boolean representation of state (for data binding)
- **IntValue** (int): Integer representation of state
- **StringValue** (string): String representation of current state
- **CheckedInt/UncheckedInt/IndeterminateInt** (int): Integer values for each state
- **CheckedString/UncheckedString/IndeterminateString** (string): String values for each state

### Appearance Properties
- **BackgroundStyle** (CheckBoxAdvBackStyle): Background style (Default, HorizontalGradient, VerticalGradient)
- **GradientStart/GradientEnd** (Color): Gradient colors
- **BorderStyle** (BorderStyle): Border style (FixedSingle, Fixed3D, None)
- **BorderColor/HotBorderColor** (Color): Border colors
- **TextShadow** (bool): Enable text shadow
- **DrawFocusRectangle** (bool): Show focus rectangle

### Alignment Properties
- **TextContentAlignment** (ContentAlignment): Text position
- **CheckAlign** (ContentAlignment): Checkbox position

### Behavior Properties
- **AutoHeight** (bool): Automatically calculate height
- **ReadOnlyMode** (bool): Prevent user interaction
- **WrapText** (bool): Enable text wrapping

## Common Use Cases

### Use Case 1: Settings Dialog
Create checkboxes for application settings with state persistence:
- Use BoolValue for simple on/off settings
- Bind directly to configuration database
- Handle CheckedChanged to save settings immediately

### Use Case 2: List Item Selection
Implement "Select All" with indeterminate state:
- Use Tristate property for three-state behavior
- CheckState.Indeterminate for partial selections
- Update state based on child item selection

### Use Case 3: Form Validation
Create read-only checkboxes to display validation status:
- Set ReadOnlyMode = true
- Update Checked state programmatically
- Use custom colors to indicate status

### Use Case 4: Enhanced UI Design
Build visually rich checkboxes matching application theme:
- Apply gradient backgrounds
- Configure custom borders and hover effects
- Add shadow text for depth
- Position text and checkbox independently

### Use Case 5: Data Entry Forms
Bind checkboxes to database records:
- Use IntValue for status codes (0, 1, or -1)
- Use BoolValue for yes/no fields
- Associate custom integer/string values with states
