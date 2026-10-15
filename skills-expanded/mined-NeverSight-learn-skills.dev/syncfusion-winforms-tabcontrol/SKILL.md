---
name: syncfusion-winforms-tabcontrol
description: Guide for implementing Syncfusion TabControlAdv in Windows Forms applications. Use when creating tabbed interfaces, organizing content in tabs, or building professional tab navigation systems. Covers tab pages, tab styling, close buttons, drag-drop tabs, tab customization, and appearance options for TabControlAdv-based applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Tab Controls (TabControlAdv)

The TabControlAdv is an advanced Windows Forms tab control that enables organizing visual content in a compact, tabbed interface. It extends the standard TabControl with extensive appearance customization, navigation features, editing capabilities, and styling options.

## When to Use This Skill

Use this skill when you need to:
- Implement tabbed interfaces in Windows Forms applications
- Add TabControlAdv with multiple TabPageAdv items
- Customize tab appearance, colors, fonts, or styles
- Enable tab editing, drag-and-drop, or close buttons
- Configure tab navigation with TabPrimitives
- Handle tab events (selection, closing, editing, etc.)
- Apply Office, Metro, or Visual Studio themes to tabs
- Implement scrolling, tooltips, or multi-line tabs
- Persist tab state (order, active page) across sessions

## Component Overview

**TabControlAdv** provides:
- **Tab Alignment**: Top, Bottom, Left, Right positioning
- **Navigation Support**: TabPrimitives for first/last/next/previous navigation
- **Editing Support**: Runtime tab header text editing
- **Icons Support**: Images in tab headers
- **Drag and Drop**: Rearrange tabs via drag-and-drop
- **Close Buttons**: Individual or global close buttons for tabs
- **ToolTips**: Standard and SuperToolTips for tabs
- **Styling**: 15+ built-in themes (2D, 3D, Metro, Office, VS styles)
- **Serialization**: Save and load tab states
- **Scrolling**: Smooth scrolling when tabs overflow

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet packages
- Adding TabControlAdv through designer
- Adding control manually in code
- Creating and adding tabs (TabPageAdv)
- Adding controls to tab pages
- Basic tab placement configuration

### Alignment and Layout
📄 **Read:** [references/alignment-layout.md](references/alignment-layout.md)
- Tab alignment (Top, Bottom, Left, Right)
- Text alignment within tabs
- Multi-line tab support
- RTL (Right-to-Left) support
- Rotating tabs and text
- TabGap spacing

### Appearance and Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Background colors and images
- Active and inactive tab colors
- Font and forecolor settings
- Border styles and colors
- Tab styles (2D, 3D, Metro, Office themes)
- SizeMode options (Normal, Fixed, ShrinkToFit, FillToRight)

### Interactive Features
📄 **Read:** [references/interactive-features.md](references/interactive-features.md)
- Close button settings
- Tooltip and SuperTooltip support
- Scroll buttons and scrollbars
- Middle-click to close tabs
- Auto-scroll configuration

### Tab Navigation
📄 **Read:** [references/tab-navigation.md](references/tab-navigation.md)
- TabPrimitives overview
- Navigation control types (FirstTab, LastTab, NextTab, PreviousTab, etc.)
- DropDown and Close primitives
- Custom primitives
- Creating TabPrimitives programmatically

### Customization and Editing
📄 **Read:** [references/customization-editing.md](references/customization-editing.md)
- Renaming tab headers at runtime (LabelEdit)
- Drag-and-drop tab reordering (UserMoveTabs)
- Padding and spacing
- Tab page border styles
- Animated GIF images in tabs
- Preventing specific tabs from moving

### Serialization
📄 **Read:** [references/serialization.md](references/serialization.md)
- PersistTabState property
- Automatic tab state persistence
- Saving tab order and active page

### Events and Event Handling
📄 **Read:** [references/events.md](references/events.md)
- Edit events (BeforeEdit, AfterEdit)
- Selection events (SelectedIndexChanging, SelectedIndexChanged)
- Tab primitive click events
- DrawItem for custom rendering
- Tab page events (Closed, Closing)
- Other events (Paint, BackgroundImageChanged, etc.)

## Quick Start Example

### Basic Implementation

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create TabControlAdv
TabControlAdv tabControlAdv1 = new TabControlAdv();
tabControlAdv1.Size = new Size(400, 300);

// Create and add tab pages
TabPageAdv tabPage1 = new TabPageAdv();
tabPage1.Text = "Home";
tabPage1.ImageIndex = 0; // Optional icon

TabPageAdv tabPage2 = new TabPageAdv();
tabPage2.Text = "Settings";

tabControlAdv1.TabPages.Add(tabPage1);
tabControlAdv1.TabPages.Add(tabPage2);

// Add to form
this.Controls.Add(tabControlAdv1);
```

### With Styling and Features

```csharp
// Apply Office 2016 theme
tabControlAdv1.TabStyle = typeof(TabRendererOffice2016Colorful);

// Enable features
tabControlAdv1.ShowTabCloseButton = true;
tabControlAdv1.UserMoveTabs = true;
tabControlAdv1.LabelEdit = true;
tabControlAdv1.ShowToolTips = true;

// Customize appearance
tabControlAdv1.ActiveTabColor = Color.FromArgb(255, 255, 255);
tabControlAdv1.InactiveTabColor = Color.FromArgb(240, 240, 240);
tabControlAdv1.ActiveTabFont = new Font("Segoe UI", 9F, FontStyle.Bold);
```

## Common Patterns

### Pattern 1: Tabbed Document Interface

```csharp
// Create tab control for documents
TabControlAdv documentTabs = new TabControlAdv();
documentTabs.Dock = DockStyle.Fill;
documentTabs.ShowTabCloseButton = true;
documentTabs.ShowCloseButtonForActiveTabOnly = true;

// Add document tabs dynamically
void AddDocumentTab(string title, Control content)
{
    TabPageAdv docTab = new TabPageAdv();
    docTab.Text = title;
    docTab.Controls.Add(content);
    content.Dock = DockStyle.Fill;
    documentTabs.TabPages.Add(docTab);
    documentTabs.SelectedTab = docTab;
}

// Handle tab closing
documentTabs.SelectedTab.Closing += (sender, e) =>
{
    var result = MessageBox.Show("Save changes?", "Close", 
        MessageBoxButtons.YesNoCancel);
    if (result == DialogResult.Cancel)
        e.Cancel = true;
};
```

### Pattern 2: Navigation Tabs with Icons

```csharp
// Setup image list
ImageList tabImages = new ImageList();
tabImages.Images.Add("home", Properties.Resources.HomeIcon);
tabImages.Images.Add("settings", Properties.Resources.SettingsIcon);
tabControlAdv1.ImageList = tabImages;

// Create tabs with icons
TabPageAdv homeTab = new TabPageAdv();
homeTab.Text = "Home";
homeTab.ImageIndex = 0;

TabPageAdv settingsTab = new TabPageAdv();
settingsTab.Text = "Settings";
settingsTab.ImageIndex = 1;

// Configure alignment
tabControlAdv1.ImageAlignmentR = RelativeImageAlignment.LeftOfText;
```

### Pattern 3: Tab Navigation Controls

```csharp
// Enable navigation primitives
tabControlAdv1.TabPrimitivesHost.Visible = true;

// Add navigation buttons
tabControlAdv1.TabPrimitivesHost.TabPrimitives.Add(
    new TabPrimitive(TabPrimitiveType.FirstTab, null, Color.Empty, true, 1, "First"));
tabControlAdv1.TabPrimitivesHost.TabPrimitives.Add(
    new TabPrimitive(TabPrimitiveType.PreviousTab, null, Color.Empty, true, 1, "Previous"));
tabControlAdv1.TabPrimitivesHost.TabPrimitives.Add(
    new TabPrimitive(TabPrimitiveType.NextTab, null, Color.Empty, true, 1, "Next"));
tabControlAdv1.TabPrimitivesHost.TabPrimitives.Add(
    new TabPrimitive(TabPrimitiveType.LastTab, null, Color.Empty, true, 1, "Last"));
tabControlAdv1.TabPrimitivesHost.TabPrimitives.Add(
    new TabPrimitive(TabPrimitiveType.DropDown, null, Color.Empty, true, 1, "DropDown"));
```

### Pattern 4: Handling Tab Selection

```csharp
// Prevent selection of specific tab
tabControlAdv1.SelectedIndexChanging += (sender, e) =>
{
    if (e.NewSelectedIndex == 2) // Prevent selecting 3rd tab
    {
        e.Cancel = true;
        MessageBox.Show("This tab is disabled");
    }
};

// React to selection changes
tabControlAdv1.SelectedIndexChanged += (sender, e) =>
{
    var selectedTab = tabControlAdv1.SelectedTab;
    Console.WriteLine($"Selected tab: {selectedTab.Text}");
    // Load content for selected tab
};
```

## Key Properties

### Core Properties
| Property | Type | Description |
|----------|------|-------------|
| `TabPages` | Collection | Collection of TabPageAdv items |
| `SelectedIndex` | int | Index of currently selected tab |
| `SelectedTab` | TabPageAdv | Currently selected tab page |
| `Alignment` | TabAlignment | Tab position (Top, Bottom, Left, Right) |
| `Multiline` | bool | Allow tabs in multiple rows |

### Appearance Properties
| Property | Type | Description |
|----------|------|-------------|
| `TabStyle` | Type | Theme renderer (2D, 3D, Metro, Office, VS styles) |
| `ActiveTabColor` | Color | Background color of active tab |
| `InactiveTabColor` | Color | Background color of inactive tabs |
| `ActiveTabFont` | Font | Font for active tab text |
| `SizeMode` | TabSizeMode | Tab sizing mode |

### Feature Properties
| Property | Type | Description |
|----------|------|-------------|
| `ShowTabCloseButton` | bool | Show close button on tabs |
| `UserMoveTabs` | bool | Enable drag-drop tab reordering |
| `LabelEdit` | bool | Enable runtime tab text editing |
| `ShowToolTips` | bool | Enable tooltips on tabs |
| `ShowScroll` | bool | Show scroll buttons when tabs overflow |

### Navigation Properties
| Property | Type | Description |
|----------|------|-------------|
| `TabPrimitivesHost` | TabPrimitivesHost | Container for navigation buttons |
| `SwitchPagesForDialogKeys` | bool | Enable Ctrl+Tab navigation |

## Common Use Cases

### Use Case 1: Application Settings Dialog
Create a tabbed settings dialog with categories like "General", "Appearance", "Advanced":
- Use `Alignment = TabAlignment.Left` for vertical tabs
- Apply consistent styling with `TabStyle`
- Add icons to tabs with `ImageList`

### Use Case 2: Multi-Document Editor
Build a document editor with closeable tabs:
- Enable `ShowTabCloseButton = true`
- Handle `Closing` event to prompt for unsaved changes
- Use `UserMoveTabs = true` for reordering

### Use Case 3: Wizard Interface
Create a step-by-step wizard with disabled tab selection:
- Use `SelectedIndexChanging` to control navigation
- Apply custom colors to indicate progress
- Show/hide tabs based on wizard flow

### Use Case 4: Dashboard with Sections
Organize dashboard content into sections:
- Use `Multiline = true` for many tabs
- Apply `SizeMode.FillToRight` for uniform tab widths
- Enable `ShowScroll` for overflow handling

## Assembly References

Required assemblies:
- `Syncfusion.Shared.Base.dll`
- `Syncfusion.Shared.Windows.dll`
- `Syncfusion.Tools.Base.dll`
- `Syncfusion.Tools.Windows.dll`

For Grid controls in tabs, also add:
- `Syncfusion.Grid.Base.dll`
- `Syncfusion.Grid.Windows.dll`

