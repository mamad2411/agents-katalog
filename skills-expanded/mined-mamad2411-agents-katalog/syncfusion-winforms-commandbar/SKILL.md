---
name: syncfusion-winforms-commandbar
description: Implement the CommandBar control in Windows Forms to create customizable toolbars, rebars, and status bars with docking, floating, and state persistence capabilities. The CommandBar provides Office-like UI organization with support for hosting multiple controls, user layout customization, and serializable state management.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Windows Forms CommandBar

The CommandBar control provides a complete framework for creating and hosting toolbars, rebars, and status bars similar to Visual Studio and Office interfaces. It supports docking, floating windows, state persistence, and hosting custom controls.

## When to use this skill

Use CommandBar when you need to:
- Create customizable toolbars and status bars
- Implement Office-like UI with docking/floating capabilities
- Allow users to reposition and rearrange bars
- Save and restore bar layout state across sessions
- Host controls like dropdowns, textboxes, and buttons
- Build complex multi-bar command frameworks

## CommandBar overview

CommandBar operates through the CommandBarController component which manages multiple CommandBar instances. Each bar can host controls, dock to form sides, float as separate windows, and fire events during state transitions. Bars can be serialized to preserve user customization.

## Documentation and navigation guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly dependencies and NuGet setup
- Adding CommandBar via designer and code
- Creating CommandBarController with HostForm
- Adding child controls (single and multiple)
- Code-first initialization patterns

### Appearance Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Customizing buttons (close, chevron, dropdown)
- Cursor and gripper visibility control
- Background color customization (docked bar and CommandBar)
- Text display settings and font styling
- Visual property configuration

### Interactive Features
📄 **Read:** [references/interactive-features.md](references/interactive-features.md)
- Floating bars and float mode wrapping
- Docking modes and dock state management
- Dock border restrictions
- Event handling (state changed, wrapping, closing)
- Complete event subscription examples

### Hosting Controls
📄 **Read:** [references/hosting-controls.md](references/hosting-controls.md)
- Integrating PopupMenu for dropdown functionality
- Adding XPToolBar for menu items
- Designer vs code-based integration
- Container patterns for complex layouts

### Serialization
📄 **Read:** [references/serialization.md](references/serialization.md)
- Persistence support and state management
- AppStateSerializer class usage
- XML, Binary, Registry, and IsolatedStorage formats
- Load and save workflows
- State restoration on application launch

## Quick start example

```csharp
using Syncfusion.Windows.Forms.Tools;
using System.Windows.Forms;

public partial class Form1 : Form
{
    private CommandBarController commandBarController1;
    private CommandBar commandBar1;

    public Form1()
    {
        InitializeComponent();
        
        // Create controller
        commandBarController1 = new CommandBarController();
        commandBarController1.HostForm = this;
        
        // Create command bar
        commandBar1 = new CommandBar();
        commandBar1.Text = "Main Toolbar";
        commandBarController1.CommandBars.Add(commandBar1);
        
        // Add child controls
        TextBox textBox1 = new TextBox();
        commandBar1.Controls.Add(textBox1);
    }
}
```

## Common patterns

### Office-like layout
- Use Top CommandBar for main menu items (via XPToolBar)
- Use additional CommandBars for formatting toolbars
- Enable user to dock/float each bar independently
- Set AllowedDockBorders to restrict positioning

### Responsive toolbars
- Enable FloatModeWrapping for space-constrained layouts
- Use chevron to handle overflow items
- Implement dynamic control addition based on context

### Persistent state
- Enable PersistState on CommandBarController
- Load state in Form_Load event
- Save state in Form_Closing event
- Use serialization format matching your storage preference

## Key properties

**CommandBarController**
- `HostForm` - The form containing all command bars (required)
- `CommandBars` - Collection of CommandBar instances
- `PersistState` - Enable/disable state persistence
- `BackColor` - Color of docked bar area
- `Style` - Visual appearance (Office, Metro, etc.)

**CommandBar**
- `Text` - Display name in dock/float mode
- `DockState` - Current position (Top, Bottom, Left, Right)
- `DisableDocking` - Prevent docking (force float mode)
- `DisableFloating` - Prevent floating (force docked mode)
- `AllowedDockBorders` - Restrict docking to specific sides
- `FloatModeWrapping` - Enable content wrapping in float mode
- `HideGripper` - Hide drag handle
- `HideCloseButton` - Hide close button in float mode
- `HideChevron` - Hide overflow menu button

## Common use cases

**1. Visual Studio-like interface**
- Multiple docked toolbars with different functions
- Floating tool windows
- Save user layout preferences
- Restore on application restart

**2. Customizable dashboard**
- Allow users to show/hide specific bars
- Reposition bars as needed
- Preserve layout in settings
- Different layouts for different modes

**3. Single toolbar with multiple controls**
- Host textbox for search
- Host dropdown for filtering
- Host buttons for actions
- Responsive to window resizing

**4. Status bar implementation**
- Dock CommandBar to bottom
- Add status labels and progress indicators
- Disable floating/moving (DisableDocking = true)
- Update content based on application state
