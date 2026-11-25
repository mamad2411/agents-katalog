---
name: syncfusion-winforms-docking-manager
description: Guide to implement Syncfusion WinForms DockingManager control for Visual Studio-style dockable windows and layouts. Use this when creating docked, floating, or tabbed windows with advanced layout management. Covers dock states, auto-hide functionality, caption customization, and serialization in WinForms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinForms Docking Manager

The DockingManager control implements an architecture that allows panels to be docked at any part of form, creating Visual Studio-style dockable windows. Dock panels can be interactively dragged, resized, floated, auto-hidden, tabbed, and arranged in complex layouts at runtime.

## When to Use This Skill

Use this skill when you need to:

- **Create Visual Studio-style docking layouts** with dockable panels and windows
- **Implement multiple dock states**: docked, floating, auto-hide, tabbed, MDI, or TDI windows
- **Build document-based applications** with TDI (Tabbed Document Interface) or MDI (Multiple Document Interface)
- **Add caption buttons** (close, pin, menu, maximize) to docked windows
- **Persist dock layouts** across application sessions using serialization
- **Handle dock events** for activation, state changes, and user interactions
- **Customize appearance** with visual styles, themes, and colors
- **Manage nested or linked docking managers** for complex layouts
- **Implement drag-and-drop docking** with visual feedback and hints

## Component Overview

**DockingManager** transforms any control into a fully-featured docking window with:

- **Dock States**: Docked (Left, Right, Top, Bottom), Floating, Auto-Hide, Tabbed, Fill
- **Document Windows**: TDI (Tabbed Documents) and MDI (Multiple Documents)
- **Caption Buttons**: Close, Pin (Auto-Hide), Menu, Maximize, Restore, and custom buttons
- **Visual Styles**: Metro, Office2016 (Colorful, White, DarkGray, Black), VS2010, Office2007/2010
- **Serialization**: Save/load dock state to XML, binary, memory stream, or isolated storage
- **Events**: 25+ events for dock state changes, activation, dragging, context menus
- **Advanced Features**: Nested managers, linked managers, dock restrictions, tab groups

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly deployment
- Creating DockingManager instance
- Adding dock child windows with SetEnableDocking
- Setting dock labels and icons
- Basic docking setup and configuration

### Dock States and Layouts
📄 **Read:** [references/dock-states.md](references/dock-states.md)
- Dock state overview (Docked, Float, Auto-Hide, Tabbed, Fill)
- DockControl function to change states programmatically
- Setting dock sides (Left, Right, Top, Bottom, Tabbed)
- Detecting and managing dock states
- Dock ability restrictions

### Document Windows (TDI/MDI)
📄 **Read:** [references/document-windows.md](references/document-windows.md)
- TDI (Tabbed Document Interface) implementation
- MDI (Multiple Document Interface) setup
- EnableDocumentMode property
- DockAsDocument function for adding document tabs
- Window modes (Tool vs Document behavior)
- Creating and managing document tab groups
- Freezing document state

### Caption Buttons and Customization
📄 **Read:** [references/caption-buttons.md](references/caption-buttons.md)
- Default caption buttons (Close, Pin, Menu, Maximize, Restore)
- Show/hide specific buttons with Set/Get functions
- Adding custom caption buttons to CaptionButtons collection
- Button click handling and events
- Customizing button appearance and colors
- Button tooltips and SuperTooltips

### Floating Windows
📄 **Read:** [references/floating-windows.md](references/floating-windows.md)
- Creating floating windows with FloatControl
- Floating by user drag interaction
- Enabling/disabling float functionality
- Floating window properties (border, size, location)
- Maximize floating windows
- Float-only windows (prevent re-docking)
- Show custom buttons in floating state

### Auto-Hide Windows
📄 **Read:** [references/auto-hide-windows.md](references/auto-hide-windows.md)
- Auto-hide functionality overview
- SetAutoHideMode function
- Auto-hide programmatically or by user pin button
- Changing auto-hide side with DockControlInAutoHideMode
- Auto-hide on load with SetAutoHideOnLoad
- Animation settings and speed
- Auto-hide tab customization
- Auto-hide selection style (MouseHover vs Click)

### Tabbed Windows
📄 **Read:** [references/tabbed-windows.md](references/tabbed-windows.md)
- Tabbing windows together with Tabbed dock style
- Creating tab groups at design time and runtime
- Tab alignment options (Top, Bottom, Left, Right)
- Tab reordering with AllowTabsMoving
- Preventing tabbing with DockAbility
- Tab position management with Set/GetTabPosition
- Tab scroll buttons

### Appearance and Visual Styles
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Visual styles (Default, Metro, Office2016, VS2010, Office2007/2010)
- Office color schemes (Blue, Silver, Black, Managed)
- Custom colors for Office2007/2010
- Caption customization (background, foreground, font)
- Border colors and splitter customization
- Dock tab appearance (colors, fonts, height)
- Document tab styling
- Auto-hide tab styling
- Drag provider styles (VS2005, VS2008, VS2010, VS2012, Office2016)
- Right-to-left support

### Serialization and State Persistence
📄 **Read:** [references/serialization.md](references/serialization.md)
- Auto serialization with PersistState property
- SaveDockState and LoadDockState functions
- Serialize to XML file
- Serialize to binary file
- Serialize to memory stream for database storage
- Serialize to isolated storage
- Serialize specific controls only
- Restore to designer initial state

### Docking Events
📄 **Read:** [references/docking-events.md](references/docking-events.md)
- DockControlActivated and DockControlDeactivated
- DockStateChanged and DockStateChanging
- AutoHideAnimationStart and AutoHideAnimationStop
- DragAllow, DragFeedbackStart, DragFeedbackStop
- DockContextMenu and AutoHideTabContextMenu
- ControlMaximizing, Maximized, Restored, Minimized
- DockVisibilityChanged and DockVisibilityChanging
- NewDockStateBeginLoad and NewDockStateEndLoad
- PreviewDockHints for restricting dock sides
- TabGroupCreating and TabGroupCreated
- TransferredToManager and TransferringFromManager

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Nested docking managers (child manager within parent)
- Linked managers (drag between managers)
- Dock ability restrictions (SetDockAbility, SetOuterDockAbility)
- Size constraints (minimum size, freeze resizing)
- Prevent closing and docking operations
- Context menu customization (add/remove items)
- Splitter width and color customization
- Design-time docking features
- Localization support

## Quick Start Example

### Basic Docking Setup

```csharp
using Syncfusion.Windows.Forms.Tools;

public partial class Form1 : Form
{
    private DockingManager dockingManager1;
    private Panel solutionExplorer;
    private Panel toolbox;
    private Panel properties;
    private Panel output;

    public Form1()
    {
        InitializeComponent();
        
        // Create DockingManager
        this.dockingManager1 = new DockingManager(this.components);
        this.dockingManager1.HostControl = this;
        
        // Create dock panels
        this.solutionExplorer = new Panel();
        this.toolbox = new Panel();
        this.properties = new Panel();
        this.output = new Panel();
        
        // Add panels to form
        this.Controls.AddRange(new Control[] { 
            solutionExplorer, toolbox, properties, output 
        });
        
        // Enable docking for all panels
        this.dockingManager1.SetEnableDocking(solutionExplorer, true);
        this.dockingManager1.SetEnableDocking(toolbox, true);
        this.dockingManager1.SetEnableDocking(properties, true);
        this.dockingManager1.SetEnableDocking(output, true);
        
        // Set dock labels
        this.dockingManager1.SetDockLabel(solutionExplorer, "Solution Explorer");
        this.dockingManager1.SetDockLabel(toolbox, "Toolbox");
        this.dockingManager1.SetDockLabel(properties, "Properties");
        this.dockingManager1.SetDockLabel(output, "Output");
        
        // Arrange dock positions
        this.dockingManager1.DockControl(solutionExplorer, this, DockingStyle.Right, 250);
        this.dockingManager1.DockControl(toolbox, this, DockingStyle.Left, 200);
        this.dockingManager1.DockControl(properties, solutionExplorer, DockingStyle.Tabbed, 200);
        this.dockingManager1.DockControl(output, this, DockingStyle.Bottom, 150);
        
        // Apply visual style
        this.dockingManager1.VisualStyle = VisualStyle.Office2016Colorful;
    }
}
```

## Common Patterns

### Creating Document Windows (TDI)

```csharp
// Enable document mode
this.dockingManager1.EnableDocumentMode = true;

// Add document tabs in NewDockStateEndLoad event
this.dockingManager1.NewDockStateEndLoad += (s, e) =>
{
    this.dockingManager1.DockAsDocument(document1);
    this.dockingManager1.DockAsDocument(document2);
};

// Set window mode (Tool allows dock/float, Document allows float only)
this.dockingManager1.SetWindowMode(document1, WindowMode.Document);
```

### Changing Dock States Programmatically

```csharp
// Dock a control to specific side
this.dockingManager1.DockControl(panel1, this, DockingStyle.Left, 200);

// Float a control at specific location
Rectangle bounds = new Rectangle(100, 100, 300, 400);
this.dockingManager1.FloatControl(panel1, bounds);

// Auto-hide a control
this.dockingManager1.SetAutoHideMode(panel1, true);

// Tab control with another
this.dockingManager1.DockControl(panel2, panel1, DockingStyle.Tabbed, 200);
```

### Customizing Caption Buttons

```csharp
// Hide close button for specific control
this.dockingManager1.SetCloseButtonVisibility(panel1, false);

// Hide pin (auto-hide) button
this.dockingManager1.SetAutoHideButtonVisibility(panel1, false);

// Add custom caption button
CaptionButton customBtn = new CaptionButton();
customBtn.Name = "CustomButton";
customBtn.ImageIndex = 3; // From ImageList
customBtn.Type = CaptionButtonType.Custom;
this.dockingManager1.CaptionButtons.Add(customBtn);

// Customize button colors
this.dockingManager1.ActiveCaptionButtonForeColor = Color.Red;
this.dockingManager1.InActiveCaptionButtonForeColor = Color.Gray;
```

### Serialization (Save/Load Layout)

```csharp
using Syncfusion.Runtime.Serialization;

// Enable auto-save on close
this.dockingManager1.PersistState = true;

// Save to XML file manually
AppStateSerializer serializer = new AppStateSerializer(
    SerializeMode.XMLFile, "DockLayout");
this.dockingManager1.SaveDockState(serializer);
serializer.PersistNow();

// Load from XML file
AppStateSerializer serializer = new AppStateSerializer(
    SerializeMode.XMLFile, "DockLayout");
this.dockingManager1.LoadDockState(serializer);

// Save to memory stream (for database)
MemoryStream ms = new MemoryStream();
AppStateSerializer serializer = new AppStateSerializer(
    SerializeMode.BinaryFmtStream, ms);
this.dockingManager1.SaveDockState(serializer);
serializer.PersistNow();
// Store ms.ToArray() in database
```

### Handling Dock Events

```csharp
// Track dock state changes
this.dockingManager1.DockStateChanged += (s, e) =>
{
    foreach (Control ctrl in e.Controls)
    {
        Console.WriteLine($"{ctrl.Name} state changed");
    }
};

// Prevent specific dock operations
this.dockingManager1.DockStateChanging += (s, e) =>
{
    if (e.NewState == DockState.Float && e.Controls[0] == panel1)
    {
        e.Cancel = true; // Prevent panel1 from floating
    }
};

// Handle control activation
this.dockingManager1.DockControlActivated += (s, e) =>
{
    Console.WriteLine($"{e.Control.Name} activated");
};

// Restrict dock sides dynamically
this.dockingManager1.PreviewDockHints += (s, e) =>
{
    if (e.DraggingTarget == panel2)
    {
        // Only allow right docking on panel2
        e.DockAbility = DockAbility.Right;
    }
};
```

### Restricting Dock Abilities

```csharp
// Restrict where control can dock (inner docking)
this.dockingManager1.SetDockAbility(panel1, DockAbility.Top | DockAbility.Bottom);

// Restrict where control can dock in client area (outer docking)
this.dockingManager1.SetOuterDockAbility(panel1, 
    DockAbility.Left | DockAbility.Right);

// Make control float-only (cannot re-dock)
this.dockingManager1.SetFloatOnly(panel1, true);

// Disable floating for specific control
this.dockingManager1.SetAllowFloating(panel1, false);
```

### Customizing Appearance

```csharp
// Set visual style
this.dockingManager1.VisualStyle = VisualStyle.Office2016Colorful;

// Customize active caption colors
this.dockingManager1.ActiveCaptionBackground = new BrushInfo(
    GradientStyle.Horizontal, Color.DarkBlue, Color.LightBlue);
this.dockingManager1.ActiveCaptionForeGround = Color.White;

// Customize dock tab colors
this.dockingManager1.DockTabBackColor = Color.LightGray;
this.dockingManager1.ActiveDockTabBackColor = Color.White;
this.dockingManager1.DockTabForeColor = Color.Black;

// Customize document tab colors
this.dockingManager1.DocumentWindowSettings.TabBackColor = Color.SteelBlue;
this.dockingManager1.DocumentWindowSettings.ActiveTabBackColor = Color.Green;
this.dockingManager1.DocumentWindowSettings.TabHeight = 38;

// Set drag provider style
this.dockingManager1.DragProviderStyle = DragProviderStyle.VS2012;
```

## Key Properties and Methods

### Essential Properties

- **HostControl**: Gets/sets the parent control hosting the docking layout
- **EnableDocumentMode**: Enable TDI (Tabbed Document Interface) mode
- **PersistState**: Enable automatic save/load of dock state
- **VisualStyle**: Set appearance theme (Metro, Office2016, VS2010, etc.)
- **DragProviderStyle**: Set drag hint style (VS2005, VS2008, VS2010, VS2012)
- **AutoHideEnabled**: Enable/disable auto-hide (pin) functionality
- **AllowTabsMoving**: Enable tab reordering by drag-and-drop
- **ShowCaption**: Show/hide caption bar for all dock windows
- **CaptionButtons**: Collection of caption buttons (Close, Pin, Menu, etc.)

### Essential Methods

**Adding Dock Children:**
- `SetEnableDocking(Control, bool)`: Enable docking for a control
- `SetDockLabel(Control, string)`: Set caption label text
- `SetDockIcon(Control, Icon)`: Set caption icon

**Changing Dock States:**
- `DockControl(Control, Control, DockingStyle, int)`: Dock control at specific side
- `FloatControl(Control, Rectangle)`: Float control at location
- `SetAutoHideMode(Control, bool)`: Set auto-hide state
- `SetAsMDIChild(Control, bool)`: Convert to MDI child window
- `DockAsDocument(Control)`: Add as TDI document tab

**State Management:**
- `GetDockStyle(Control)`: Get current dock style
- `IsFloating(Control)`: Check if control is floating
- `GetAutoHideMode(Control)`: Check if control is auto-hidden
- `IsMDIMode(Control)`: Check if control is MDI child
- `IsTabbed(Control)`: Check if control is tabbed

**Serialization:**
- `SaveDockState()`: Save to isolated storage
- `SaveDockState(AppStateSerializer)`: Save to file/stream
- `LoadDockState()`: Load from isolated storage
- `LoadDockState(AppStateSerializer)`: Load from file/stream

**Caption Buttons:**
- `SetCloseButtonVisibility(Control, bool)`: Show/hide close button
- `SetAutoHideButtonVisibility(Control, bool)`: Show/hide pin button
- `SetMenuButtonVisibility(Control, bool)`: Show/hide menu button

**Restrictions:**
- `SetDockAbility(Control, DockAbility)`: Restrict inner docking sides
- `SetOuterDockAbility(Control, DockAbility)`: Restrict outer docking sides
- `SetFloatOnly(Control, bool)`: Make control float-only
- `SetAllowFloating(Control, bool)`: Enable/disable floating

## Common Use Cases

### 1. Visual Studio-Style IDE Layout
Create solution explorer, toolbox, properties, and output windows with docking, floating, and auto-hide capabilities.

### 2. Document Editing Application
Implement tabbed document interface (TDI) for multiple document editing with tool windows around the edges.

### 3. Dashboard Layout Manager
Build customizable dashboard with dockable widget panels that users can arrange and persist.

### 4. Multi-Panel Data Viewer
Display multiple data grids, charts, and details panels with flexible docking and tabbing.

### 5. Application with Persistent Layout
Save and restore user's preferred window arrangement across sessions using serialization.

### 6. MDI Application Modernization
Convert traditional MDI applications to modern docking interface with floating and tabbed documents.

### 7. Custom Development Tools
Build code editors, debuggers, or design tools with dockable windows similar to Visual Studio.