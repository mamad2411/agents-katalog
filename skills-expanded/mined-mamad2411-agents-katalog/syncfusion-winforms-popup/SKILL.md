---
name: syncfusion-winforms-popup
description: Guide for implementing Syncfusion PopupControlContainer in Windows Forms applications. Use when creating custom popup panels, attaching popups to parent controls, or configuring auto-close behavior. Covers popup lifecycle, ShowPopup/HidePopup methods, event handling (BeforePopup, Popup, CloseUp), hosting child controls in popups, auto-scroll configuration, transparent popups, and advanced scenarios like ComboBoxBase hosting within popups.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Popup Controls (PopupControlContainer)

## When to Use This Skill

Use this skill when the user:
- Needs to create custom popup panels in Windows Forms applications
- Wants to attach popups to parent controls (buttons, textboxes, labels, etc.)
- Is implementing dropdown-like behavior with custom controls
- Needs to configure auto-close, auto-scroll, or keyboard navigation for popups
- Wants to handle popup lifecycle events (before showing, after showing, on close)
- Is building context menus, dropdown panels, or custom picker controls
- Needs to populate popups with child controls (buttons, grids, calendars, etc.)
- Requires transparent or resizable popup windows
- Is hosting ComboBoxBase or other complex controls within popups
- Encounters issues with popup closing behavior or focus management

## Component Overview

**PopupControlContainer** is a panel-derived control that allows you to populate it with child controls and associate it with a parent control. By default, the popup is hidden and can be shown programmatically through events like mouse clicks, button presses, or keyboard actions on the parent control.

**Key Capabilities:**
- Host any child controls (buttons, textboxes, grids, custom controls)
- Associate with any parent control
- Auto-close when clicking outside the popup
- Auto-scroll when content exceeds popup size
- Keyboard navigation with dialog keys (Enter, Esc, Tab, F4, F2)
- Event-driven lifecycle (BeforePopup, Popup, CloseUp)
- Programmatic show/hide with position control
- Resizable and transparent popup windows
- Support for nested popups (ComboBoxBase hosting)

**Common Use Cases:**
- Custom dropdown panels for textboxes or buttons
- Color pickers, date pickers, or custom selectors
- Context-sensitive toolbars or option panels
- Tooltip-like windows with interactive controls
- Custom combo box implementations

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet packages
- Adding control via designer and code
- Basic parent control association
- ShowPopup and HidePopup methods
- Complete working examples

### Popup Behavior Configuration

**Auto-Close Behavior**  
📄 **Read:** [references/auto-close-behavior.md](references/auto-close-behavior.md)
- Default auto-close on outside click
- IgnoreMouseMessages property
- PopupCloseType modes (Done, Canceled, Deactivated)
- Conditional closing scenarios

**Auto-Scroll**  
📄 **Read:** [references/autoscroll.md](references/autoscroll.md)
- Enabling automatic scrollbars
- AutoScrollMargin and AutoScrollMinSize
- Handling content overflow

**Keyboard Navigation**  
📄 **Read:** [references/keyboard-navigation.md](references/keyboard-navigation.md)
- Default dialog key behavior
- IgnoreDialogKey property
- Custom keyboard handling

### Events and Lifecycle
📄 **Read:** [references/events.md](references/events.md)
- BeforePopup event (before showing, resizing)
- Popup event (after shown, focus management)
- CloseUp event (on close, data transfer)
- Mnemonic support and focus handling
- Complete event handler examples

### Advanced Scenarios
📄 **Read:** [references/advanced-scenarios.md](references/advanced-scenarios.md)
- Hosting ComboBoxBase controls
- Creating transparent popups
- Checking popup state with IsShowing()
- BeforeCloseUp workarounds
- Edge cases and troubleshooting

## Quick Start Example

### Basic Popup Setup

```csharp
using Syncfusion.Windows.Forms;

public partial class Form1 : Form
{
    private PopupControlContainer popupControlContainer1;
    private Button button1;
    private RichTextBox richTextBox1;
    
    public Form1()
    {
        InitializeComponent();
        
        // Initialize popup container
        this.popupControlContainer1 = new PopupControlContainer();
        
        // Add child control (button in this example)
        this.button1 = new Button();
        this.button1.Text = "Click Me";
        this.button1.Location = new Point(10, 10);
        this.popupControlContainer1.Controls.Add(this.button1);
        
        // Configure popup
        this.popupControlContainer1.Size = new Size(200, 100);
        
        // Create parent control
        this.richTextBox1 = new RichTextBox();
        this.richTextBox1.Size = new Size(150, 50);
        this.richTextBox1.Location = new Point(20, 20);
        this.richTextBox1.Click += RichTextBox1_Click;
        
        // Associate popup with parent
        this.popupControlContainer1.ParentControl = this.richTextBox1;
        
        // Add controls to form
        this.Controls.Add(this.richTextBox1);
    }
    
    private void RichTextBox1_Click(object sender, EventArgs e)
    {
        // Show popup at default position
        this.popupControlContainer1.ShowPopup(Point.Empty);
    }
}
```

### Show Popup at Specific Position

```csharp
// Show at specific screen coordinates
this.popupControlContainer1.ShowPopup(new Point(100, 200));

// Show below parent control
Point location = this.richTextBox1.PointToScreen(
    new Point(0, this.richTextBox1.Height));
this.popupControlContainer1.ShowPopup(location);
```

### Hide Popup Programmatically

```csharp
// Simple hide
this.popupControlContainer1.HidePopup();

// Hide with close type
this.popupControlContainer1.HidePopup(PopupCloseType.Done);
this.popupControlContainer1.HidePopup(PopupCloseType.Canceled);
```

## Common Patterns

### Pattern 1: Conditional Auto-Close

```csharp
// Prevent auto-close on outside clicks
this.popupControlContainer1.IgnoreMouseMessages = true;

// Close only when condition is met
private void ValidateButton_Click(object sender, EventArgs e)
{
    if (ValidateInput())
    {
        this.popupControlContainer1.HidePopup(PopupCloseType.Done);
    }
}
```

### Pattern 2: Data Transfer on Close

```csharp
private void PopupControlContainer1_CloseUp(object sender, PopupClosedEventArgs e)
{
    if (e.PopupCloseType == PopupCloseType.Done)
    {
        // Transfer data from popup to parent form
        this.textBox1.Text = this.popupTextBox.Text;
    }
    else if (e.PopupCloseType == PopupCloseType.Canceled)
    {
        // Discard changes
    }
}
```

### Pattern 3: Resizable Popup

```csharp
private void PopupControlContainer1_BeforePopup(object sender, CancelEventArgs e)
{
    // Make popup resizable
    this.popupControlContainer1.PopupHost.FormBorderStyle = FormBorderStyle.SizableToolWindow;
    this.popupControlContainer1.Dock = DockStyle.Fill;
    
    // Set minimum size
    if (this.popupControlContainer1.PopupHost.Size.Width < 200)
    {
        this.popupControlContainer1.PopupHost.Size = new Size(200, 150);
    }
}
```

### Pattern 4: Transparent Popup

```csharp
private void PopupControlContainer1_BeforePopup(object sender, CancelEventArgs e)
{
    // Set opacity for transparency
    this.popupControlContainer1.PopupHost.Opacity = 0.75;
}
```

## Key Properties and Methods

### Properties

| Property | Type | Description |
|----------|------|-------------|
| **ParentControl** | Control | The control to which the popup is associated |
| **IgnoreMouseMessages** | bool | Prevents auto-close on outside clicks when true |
| **IgnoreDialogKey** | bool | Disables default keyboard closing behavior when true |
| **AutoScroll** | bool | Enables automatic scrollbars when content overflows |
| **AutoScrollMargin** | Size | Margin around scroll region |
| **AutoScrollMinSize** | Size | Minimum size for scroll region |
| **PopupHost** | Form | The host form containing the popup (access in events) |

### Methods

| Method | Description |
|--------|-------------|
| **ShowPopup(Point)** | Displays the popup at the specified screen coordinates |
| **HidePopup()** | Hides the popup |
| **HidePopup(PopupCloseType)** | Hides the popup with a specific close type |
| **IsShowing()** | Returns true if the popup is currently visible |

### Events

| Event | When Raised | Key Use Cases |
|-------|-------------|---------------|
| **BeforePopup** | Before popup is shown | Resize popup, customize appearance, cancel showing |
| **Popup** | After popup is shown | Set focus, enable mnemonics |
| **CloseUp** | When popup is closed | Transfer data, restore focus, handle close types |

## Common Use Cases

### Use Case 1: Custom Date Picker
Create a popup containing a calendar control attached to a textbox.

### Use Case 2: Color Selector Popup
Build a color picker panel that pops up when clicking a button, with OK/Cancel buttons.

### Use Case 3: Context-Sensitive Toolbar
Show a popup toolbar with formatting options when text is selected in a RichTextBox.

### Use Case 4: Multi-Select Dropdown
Create a popup with checkboxes for multi-selection, closing only when "Done" is clicked.

### Use Case 5: Cascading Popups
Host a ComboBoxBase within a popup, maintaining proper focus and preventing premature closure.

## Troubleshooting Tips

**Popup closes immediately:**
- Set `IgnoreMouseMessages = true` to prevent auto-close
- Check if `IgnoreDialogKey` needs to be enabled
- Verify event handlers aren't calling `HidePopup()` unintentionally

**Child controls don't respond to mnemonics:**
- Handle the `Popup` event and call `this.popupControlContainer1.Focus()`

**Popup appears at wrong position:**
- Use `PointToScreen()` to convert parent control coordinates to screen coordinates
- Consider parent control size and screen boundaries

**Content is cut off:**
- Enable `AutoScroll = true`
- Set appropriate `AutoScrollMinSize`
- Adjust popup size in `BeforePopup` event

**ComboBoxBase dropdown closes popup:**
- Implement custom PopupControlContainer with overridden `OnPopup()`
- Set parent-child relationship in ComboBoxBase's `DropDown` event
- See [references/advanced-scenarios.md](references/advanced-scenarios.md) for complete implementation

---

For detailed implementation guidance, code examples, and edge case handling, navigate to the appropriate reference file using the Documentation and Navigation Guide above.
