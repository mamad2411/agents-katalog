---
name: syncfusion-winforms-splitbutton
description: Guide for implementing Syncfusion WinForms SplitButton control - a hybrid button with dropdown menu. Use this when creating controls that combine button and dropdown functionality, toggle modes with menu options, or Office-style split buttons. Covers dynamic caption updates, custom button rendering, and toggle mode configuration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Split Buttons

## When to Use This Skill

Use this skill when users need to implement Syncfusion SplitButton control in WinForms applications. This control is ideal for:

- **Button-Dropdown Hybrid:** Creating controls that combine a primary button action with a dropdown menu of related options
- **Command Variations:** Providing a default action with alternative variations (e.g., Save with Save As, Send options)
- **Toggle with Options:** Implementing toggle buttons that also provide dropdown menu choices
- **Dynamic Button Text:** Updating button caption based on user selection from dropdown items
- **Office-Style UI:** Building interfaces that match Microsoft Office split button patterns
- **Custom Rendered Buttons:** Creating fully customized button appearances using ISplitButtonRenderer

The SplitButton control provides two button modes (Normal and Toggle), dynamic caption management, built-in Office2016 themes, and extensive customization through custom renderers.

## Component Overview

The **SplitButton** control is a hybrid control that behaves like a button with an integrated dropdown menu. When clicked on the button portion, it executes a primary action. When clicked on the dropdown arrow, it displays a menu of additional options. This pattern is commonly seen in applications like Microsoft Word (Save/Save As) or Outlook (Reply/Reply All).

**Key Capabilities:**
- Two button modes: Normal (standard click) and Toggle (checked/unchecked state)
- DropDown items management (Add/Remove items dynamically)
- Static or dynamic button captions (set text or use selected dropdown item as caption)
- Six built-in visual styles: Office2016White, Office2016Black, Office2016DarkGray, Office2016Colorful, Metro, Default
- ISplitButtonRenderer interface for complete button customization
- ToolStripProfessionalRenderer for dropdown items appearance customization
- DropDownItemClicked event for handling item selection

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**Read this first** for basic setup and implementation:
- Assembly references and NuGet package installation
- Adding SplitButton through Designer (drag and drop from toolbox)
- Adding SplitButton through Code (programmatic creation)
- Adding and removing dropdown items using DropDownItems collection
- Basic configuration and minimal working examples

### Button Modes and States
📄 **Read:** [references/button-modes.md](references/button-modes.md)

**Use when** users need different button behaviors:
- Normal mode for standard button click actions
- Toggle mode for checked/unchecked state buttons
- ButtonMode property configuration (Normal vs Toggle)
- IsButtonChecked property for controlling toggle state
- Mode-specific click events and state management

### Button Caption Management
📄 **Read:** [references/button-caption.md](references/button-caption.md)

**Use when** users need to:
- Set static button text using Text property
- Update button caption dynamically from dropdown item selection
- Handle DropDownItemClicked event to update caption
- Display selected item text as button label

### Visual Styles and Theming
📄 **Read:** [references/visual-styles.md](references/visual-styles.md)

**Use when** users want to:
- Apply built-in Office2016 themes (White, Black, DarkGray, Colorful)
- Use Metro or Default visual styles
- Match button appearance to application theme
- Set Style or ThemeName properties

### Advanced Customization
📄 **Read:** [references/advanced-customization.md](references/advanced-customization.md)

**Use when** users require:
- Custom button rendering using ISplitButtonRenderer interface
- Custom border, text, or arrow drawing (DrawBorder, DrawText, DrawArrow methods)
- Dropdown items appearance customization using DropDownRenderer
- Custom ToolStripProfessionalRenderer implementation
- Override methods: OnRenderItemText, OnRenderImageMargin, OnRenderItemImage, OnRenderToolStripBackground, OnRenderToolStripBorder

## Quick Start Example

Here's a minimal example showing how to create a SplitButton with dropdown items:

**Designer Approach:**
1. Drag **SplitButton** from toolbox to form
2. Set `Text` property to "Actions"
3. Use `DropDownItems` property editor to add items
4. Set `Style` property to "Office2016Colorful"

**Code Approach (C#):**
```csharp
using Syncfusion.Windows.Forms.Tools;

// Create SplitButton
SplitButton splitButton = new SplitButton();
splitButton.Text = "Save";
splitButton.Size = new Size(120, 40);
splitButton.Location = new Point(20, 20);
splitButton.Style = SplitButtonVisualStyle.Office2016Colorful;

// Add dropdown items
ToolStripMenuItem saveItem = new ToolStripMenuItem("Save");
ToolStripMenuItem saveAsItem = new ToolStripMenuItem("Save As...");
ToolStripMenuItem saveAllItem = new ToolStripMenuItem("Save All");

splitButton.DropDownItems.Add(saveItem);
splitButton.DropDownItems.Add(saveAsItem);
splitButton.DropDownItems.Add(saveAllItem);

// Add to form
this.Controls.Add(splitButton);
```

**Code Approach (VB.NET):**
```vb
Imports Syncfusion.Windows.Forms.Tools

' Create SplitButton
Dim splitButton As New SplitButton()
splitButton.Text = "Save"
splitButton.Size = New Size(120, 40)
splitButton.Location = New Point(20, 20)
splitButton.Style = SplitButtonVisualStyle.Office2016Colorful

' Add dropdown items
Dim saveItem As New ToolStripMenuItem("Save")
Dim saveAsItem As New ToolStripMenuItem("Save As...")
Dim saveAllItem As New ToolStripMenuItem("Save All")

splitButton.DropDownItems.Add(saveItem)
splitButton.DropDownItems.Add(saveAsItem)
splitButton.DropDownItems.Add(saveAllItem)

' Add to form
Me.Controls.Add(splitButton)
```

## Common Patterns

### Pattern 1: Dynamic Caption from Selected Item
Update button text when user selects a dropdown item:

```csharp
private void splitButton1_DropDownItemClicked(object sender, ToolStripItemClickedEventArgs e)
{
    // Set button caption to selected item text
    splitButton1.Text = e.ClickedItem.Text;
}
```

### Pattern 2: Toggle Mode Button
Create a toggle button with dropdown options:

```csharp
splitButton1.ButtonMode = ButtonMode.Toggle;
splitButton1.IsButtonChecked = false; // Initially unchecked

// Check if button is toggled
if (splitButton1.IsButtonChecked)
{
    // Perform checked state action
}
```

### Pattern 3: Adding Items Dynamically
Add or remove dropdown items at runtime:

```csharp
// Add new item
ToolStripMenuItem newItem = new ToolStripMenuItem("New Option");
splitButton1.DropDownItems.Add(newItem);

// Remove specific item
splitButton1.DropDownItems.Remove(existingItem);

// Remove by index
splitButton1.DropDownItems.RemoveAt(0);
```

### Pattern 4: Themed Button
Apply Office2016 theme to match application:

```csharp
// Set visual style
splitButton1.Style = SplitButtonVisualStyle.Office2016Colorful;

// Or use ThemeName property
splitButton1.ThemeName = "Office2019Colorful";
```

## Key Properties

**Essential Properties:**

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Text` | string | Button caption text | Set static button label or update from selected item |
| `ButtonMode` | ButtonMode | Normal or Toggle mode | Toggle for checked/unchecked state, Normal for standard click |
| `IsButtonChecked` | bool | Toggle state (checked/unchecked) | Control or query toggle button state |
| `DropDownItems` | ToolStripItemCollection | Collection of dropdown menu items | Add, remove, or manage dropdown options |
| `Style` | SplitButtonVisualStyle | Visual appearance style | Apply Office2016White/Black/DarkGray/Colorful, Metro, or Default |
| `ThemeName` | string | Theme name for styling | Apply Office2019 or custom themes |
| `Renderer` | ISplitButtonRenderer | Custom button renderer | Implement custom drawing for button appearance |
| `DropDownRenderer` | ToolStripRenderer | Custom dropdown renderer | Customize dropdown items appearance |

**Important Events:**

| Event | Description | When to Use |
|-------|-------------|-------------|
| `Click` | Fired when button portion is clicked | Handle primary button action |
| `DropDownItemClicked` | Fired when dropdown item is selected | Update caption or perform item-specific action |

## Common Use Cases

### Use Case 1: Save Button with Save As Option
Implement a split button like Microsoft Word's Save button:
- Primary button saves current file
- Dropdown provides "Save As", "Save All", "Save Copy" options
- Read [getting-started.md](references/getting-started.md) for setup
- Read [button-caption.md](references/button-caption.md) for dynamic text updates

### Use Case 2: View Toggle with Layout Options
Create a toggle button for view modes with layout variations:
- Toggle mode for on/off view state
- Dropdown items for layout options (Grid, List, Details)
- Read [button-modes.md](references/button-modes.md) for toggle configuration
- Read [getting-started.md](references/getting-started.md) for item management

### Use Case 3: Themed Toolbar Button
Build split buttons matching Office 2016/2019 theme:
- Apply Office2016Colorful or Office2019Colorful theme
- Match application's overall design language
- Read [visual-styles.md](references/visual-styles.md) for theme application

### Use Case 4: Custom Branded Button
Create fully customized split button with company branding:
- Custom colors, borders, and arrow icon
- Custom dropdown appearance
- Read [advanced-customization.md](references/advanced-customization.md) for ISplitButtonRenderer implementation

## Decision Guide

**Choose SplitButton when:**
- Users need a primary action with related alternatives
- Button caption should change based on selection
- Toggle behavior is needed alongside dropdown options
- Office-style UI patterns are desired

**Consider alternatives when:**
- Only dropdown menu is needed → Use ComboBox or DropDownButton
- Simple button without menu → Use standard Button control
- Multiple independent actions → Use separate Button controls or ButtonAdv

**Platform Note:**
This skill covers Syncfusion Essential Studio for Windows Forms. For other platforms:
- **WPF:** Use Syncfusion WPF SplitButton (different implementation)
- **ASP.NET:** Use Syncfusion ASP.NET SplitButton controls
- **Blazor/MAUI/React:** Refer to platform-specific split button documentation
