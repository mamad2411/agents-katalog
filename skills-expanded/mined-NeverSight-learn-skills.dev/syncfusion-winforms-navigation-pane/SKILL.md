---
name: syncfusion-winforms-navigation-pane
description: Guide for implementing Syncfusion GroupBar (Navigation Pane) control in Windows Forms applications. Use when creating Outlook-style navigation, hierarchical sidebar navigation, collapsible group containers, or toolbox-style interfaces. Covers stacked navigation panes, Office 2007/2010/2016 themed navigation, nested GroupBar containers, and categorized control collections for structured navigation layouts.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Navigation Panes (GroupBar) in Syncfusion WinForms

This skill guides you in implementing **Syncfusion WinForms GroupBar** (Navigation Pane) control—an Outlook-style navigation container that displays hierarchical groups with collapsible sections and child item collections.

## When to Use This Skill

Use this skill when the user needs to:

- Implement **Outlook-style navigation panes** (similar to Microsoft Outlook sidebar)
- Create **hierarchical sidebar navigation** with collapsible groups
- Build **toolbox-style interfaces** (like Visual Studio .NET toolbox)
- Add **categorized control collections** with GroupBarItems
- Implement **GroupView** for displaying child items within groups
- Enable **StackedMode** for navigation pane at bottom (Outlook-style)
- Apply **Office 2007/2010/2016 themes** and Metro styles
- Create **nested GroupBar** (GroupBar within GroupBar)
- Add **in-place renaming** of navigation items
- Implement **serialization** to save/restore navigation layout
- Customize **headers, borders, colors, and animations**
- Replace **standard panels** with themed navigation containers

GroupBar is ideal for applications requiring categorized navigation, toolbox-style interfaces, or Outlook-inspired sidebar layouts.

## Component Overview

**GroupBar** (Navigation Pane) is a container control that displays multiple groups (GroupBarItems) where only one selected group's content is visible at a time. It works with **GroupView** to display child items. Key capabilities:

- **GroupBarItem**: Tab-like navigation items (groups/categories)
- **GroupView**: Client control for displaying child items within groups
- **GroupViewItem**: Individual child items within a GroupView
- **StackedMode**: Navigation pane mode (like Outlook) with collapsible stack
- **Office Themes**: Office 2007/2010/2016, Metro, Office2016Colorful/White/DarkGray/Black
- **Nested GroupBar**: Host GroupBar within another GroupBar
- **Serialization**: Save/restore layout state and item positions
- **Customizable Appearance**: Headers, borders, colors, fonts, animations
- **In-Place Renaming**: Edit GroupBarItem names at runtime
- **Localization**: Multi-language support

**Key Difference from Standard Panel/TabControl:**
GroupBar provides Outlook-style navigation with GroupView integration, StackedMode for collapsible navigation pane, Office themes, and hierarchical item display capabilities.

## Additional Resources

**Assembly:** Syncfusion.Shared.Base.dll  
**Namespace:** Syncfusion.Windows.Forms.Tools  
**NuGet Package:** Syncfusion.Shared.Base
**Minimum .NET Framework:** 4.5  

## Documentation and Navigation Guide

### Getting Started and Basic Setup

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when users need:
- Assembly dependencies and NuGet package installation
- Namespace: Syncfusion.Windows.Forms.Tools
- Creating GroupBar via designer or code
- Adding GroupBarItems to the control
- Basic GroupBar configuration
- Understanding GroupBar structure
- Complete minimal working example

### GroupBar Items and Structure

📄 **Read:** [references/groupbar-items-and-structure.md](references/groupbar-items-and-structure.md)

Read this reference when users need:
- Creating GroupBarItem instances
- Text property for item labels
- Image property for item icons
- Client property (linking to GroupView)
- GroupBarItems collection management
- Item selection and navigation
- GroupBarItemSelected event handling
- Complete group navigation examples

### GroupView and Child Items

📄 **Read:** [references/groupview-and-child-items.md](references/groupview-and-child-items.md)

Read this reference when users need:
- GroupView overview (client control for groups)
- Creating GroupView instances
- GroupViewItem for child items
- Adding items to GroupViewItems collection
- Linking GroupView to GroupBarItem.Client
- Item selection in GroupView
- GroupViewItem click events
- Building toolbox-style interfaces

### Stacked Mode (Navigation Pane)

📄 **Read:** [references/stacked-mode.md](references/stacked-mode.md)

Read this reference when users need:
- StackedMode property (Outlook-style navigation)
- Navigation pane at bottom
- HeaderHeight property for collapsed state
- Navigation between stacked items
- Expanded/collapsed state management
- Serialization of stacked layout
- Complete Outlook clone example

### Visual Styles and Themes

📄 **Read:** [references/visual-styles-and-themes.md](references/visual-styles-and-themes.md)

Read this reference when users need:
- VisualStyle property overview
- Office2007 theme (Blue, Silver, Black, Managed)
- Office2007Outlook theme
- Office2010 theme (Blue, Silver, Black, Managed)
- Metro theme
- Office2016 themes (Colorful, White, DarkGray, Black)
- Managed colors for custom branding
- Theme comparison and selection
- Applying themes at runtime

### Appearance Customization

📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)

Read this reference when users need:
- Header customization (colors, fonts, height)
- Border settings (styles, colors)
- Text alignment and settings
- Image display configuration
- Tooltip settings
- Cursor customization
- Animation settings
- Custom colors and gradients

### Advanced Features and Configuration

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

Read this reference when users need:
- Nested GroupBar support (GroupBar in GroupBar)
- In-place renaming of GroupBarItems
- Serialization of layout state
- Localization support
- Link selection in GroupView
- Custom control hosting
- Event handling (GroupBarItemSelected, etc.)
- Complex navigation scenarios

## Quick Start Example

Here's a minimal example creating a GroupBar with items and child content:

```csharp
using Syncfusion.Windows.Forms.Tools;
using System;
using System.Drawing;
using System.Windows.Forms;

public class GroupBarExample : Form
{
    private GroupBar groupBar1;
    
    public GroupBarExample()
    {
        // Create GroupBar
        groupBar1 = new GroupBar();
        groupBar1.Dock = DockStyle.Left;
        groupBar1.Width = 200;
        
        // Create GroupBarItems
        GroupBarItem mailItem = new GroupBarItem();
        mailItem.Text = "Mail";
        
        GroupBarItem calendarItem = new GroupBarItem();
        calendarItem.Text = "Calendar";
        
        GroupBarItem contactsItem = new GroupBarItem();
        contactsItem.Text = "Contacts";
        
        // Add items to GroupBar
        groupBar1.GroupBarItems.AddRange(new GroupBarItem[] {
            mailItem,
            calendarItem,
            contactsItem
        });
        
        // Add GroupBar to form
        this.Controls.Add(groupBar1);
        
        this.Text = "GroupBar Example";
        this.Size = new Size(600, 400);
    }
}
```

**Result:** A left-docked navigation pane with 3 groups (Mail, Calendar, Contacts) similar to Microsoft Outlook.

## Common Patterns

### Outlook-Style Navigation with GroupView

**Pattern:** Create an Outlook-inspired navigation pane with child items.

```csharp
// Create GroupBar
GroupBar groupBar = new GroupBar();
groupBar.Dock = DockStyle.Left;
groupBar.Width = 220;
groupBar.VisualStyle = VisualStyle.Office2016Colorful;

// Create GroupBarItem
GroupBarItem mailItem = new GroupBarItem();
mailItem.Text = "Mail Folders";

// Create GroupView for child items
GroupView mailView = new GroupView();
mailView.Name = "MailView";
mailView.GroupViewItems.AddRange(new GroupViewItem[] {
    new GroupViewItem("Inbox", 0, true, null, "Inbox"),
    new GroupViewItem("Drafts", 1, true, null, "Drafts"),
    new GroupViewItem("Sent Items", 2, true, null, "Sent"),
    new GroupViewItem("Deleted Items", 3, true, null, "Deleted")
});

// Link GroupView to GroupBarItem
mailItem.Client = mailView;
groupBar.Controls.Add(mailView);
groupBar.GroupBarItems.Add(mailItem);

// Handle item click
mailView.GroupViewItemSelected += (s, e) => {
    string folderName = e.Item.Text;
    LoadMailFolder(folderName);
};

this.Controls.Add(groupBar);
```

**When:** User needs Outlook-style mail navigation with folder hierarchy.

### Visual Studio Toolbox Clone

**Pattern:** Create a toolbox-style interface with categorized controls.

```csharp
// Create GroupBar for toolbox
GroupBar toolbox = new GroupBar();
toolbox.Dock = DockStyle.Left;
toolbox.Width = 200;
toolbox.VisualStyle = VisualStyle.Office2010;

// Create "Windows Forms" category
GroupBarItem winFormsItem = new GroupBarItem();
winFormsItem.Text = "Windows Forms";

GroupView winFormsView = new GroupView();
winFormsView.GroupViewItems.AddRange(new GroupViewItem[] {
    new GroupViewItem("Button", 0, true, null, "Button"),
    new GroupViewItem("TextBox", 1, true, null, "TextBox"),
    new GroupViewItem("Label", 2, true, null, "Label"),
    new GroupViewItem("ComboBox", 3, true, null, "ComboBox")
});

// Create "Data" category
GroupBarItem dataItem = new GroupBarItem();
dataItem.Text = "Data";

GroupView dataView = new GroupView();
dataView.GroupViewItems.AddRange(new GroupViewItem[] {
    new GroupViewItem("DataSet", 0, true, null, "DataSet"),
    new GroupViewItem("DataTable", 1, true, null, "DataTable"),
    new GroupViewItem("BindingSource", 2, true, null, "BindingSource")
});

// Link and add
winFormsItem.Client = winFormsView;
dataItem.Client = dataView;

toolbox.Controls.Add(winFormsView);
toolbox.Controls.Add(dataView);

toolbox.GroupBarItems.Add(winFormsItem);
toolbox.GroupBarItems.Add(dataItem);

this.Controls.Add(toolbox);
```

**When:** User needs a categorized toolbox with collapsible sections like Visual Studio.

### Stacked Navigation Pane (Outlook Mode)

**Pattern:** Enable Outlook-style stacked navigation with bottom pane.

```csharp
// Create GroupBar in stacked mode
GroupBar navPane = new GroupBar();
navPane.Dock = DockStyle.Left;
navPane.Width = 220;
navPane.StackedMode = true; // Enable Outlook-style navigation
navPane.VisualStyle = VisualStyle.Office2016White;

// Create multiple GroupBarItems
GroupBarItem mailItem = new GroupBarItem();
mailItem.Text = "Mail";

GroupBarItem calendarItem = new GroupBarItem();
calendarItem.Text = "Calendar";

GroupBarItem contactsItem = new GroupBarItem();
contactsItem.Text = "Contacts";

GroupBarItem tasksItem = new GroupBarItem();
tasksItem.Text = "Tasks";

// Add all items
navPane.GroupBarItems.AddRange(new GroupBarItem[] {
    mailItem,
    calendarItem,
    contactsItem,
    tasksItem
});

// Handle item selection
navPane.GroupBarItemSelected += (s, e) => {
    string selectedSection = e.Item.Text;
    LoadSection(selectedSection);
};

this.Controls.Add(navPane);
```

**When:** User needs Outlook-style navigation with stacked items and bottom navigation pane.

## Key Properties

### Core Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `GroupBarItems` | Collection | Collection of GroupBarItem instances | Add navigation groups |
| `SelectedItem` | GroupBarItem | Currently selected item | Get/set active group |
| `StackedMode` | bool | Enable Outlook-style stacked navigation | Outlook-like layout |
| `VisualStyle` | VisualStyle | Visual theme | Apply Office themes |
| `HeaderHeight` | int | Height of GroupBar header | Customize header size |

### GroupBarItem Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Text` | string | Item display text | Set group label |
| `Image` | Image | Item icon image | Add visual identifier |
| `Client` | Control | Client control (typically GroupView) | Link content to item |
| `Selected` | bool | Whether item is selected | Check/set selection |

### GroupView Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `GroupViewItems` | Collection | Child items in the view | Add child items |
| `SelectedItem` | GroupViewItem | Currently selected child | Get/set selected child |
| `Name` | string | Identifier for the view | Reference the view |

### Styling Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `VisualStyle` | VisualStyle | Theme (Office2007/2010/2016/Metro) | Apply themes |
| `Office2007Theme` | Office2007Theme | Office2007 color scheme | Blue/Silver/Black/Managed |
| `Office2010Theme` | Office2010Theme | Office2010 color scheme | Blue/Silver/Black/Managed |
| `BorderStyle` | BorderStyle | Border appearance | Customize borders |
| `BackColor` | Color | Background color | Custom backgrounds |

### Advanced Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `AllowCollapse` | bool | Allow collapsing groups | Enable collapse behavior |
| `AllowInPlaceEditing` | bool | Enable item renaming | Runtime editing |
| `AnimateCollapse` | bool | Animate collapse/expand | Smooth transitions |
| `ShowToolTips` | bool | Display tooltips | Show item descriptions |

## Common Use Cases

### Email Client Navigation

Outlook-style navigation with mail folders:
- Mail folders (Inbox, Drafts, Sent, Deleted)
- Calendar view with appointments
- Contacts list with categories
- Tasks with priority sections

### IDE Toolbox Interfaces

Visual Studio-style toolboxes:
- Categorized control collections
- Component categories (Data, Layout, Controls)
- Collapsible sections
- Drag-drop tool selection

### Document Management Systems

Hierarchical document navigation:
- Document categories and folders
- Project hierarchies
- File type groupings
- Archive sections

### Settings and Configuration Panels

Categorized settings navigation:
- General settings section
- Account preferences
- Advanced options
- Theme customization

## Implementation Checklist

When implementing GroupBar (Navigation Pane), ensure:

- ✅ **Required assemblies** referenced (Syncfusion.Shared.Base.dll)
- ✅ **Namespace** included (Syncfusion.Windows.Forms.Tools)
- ✅ **GroupBar instance** created and configured
- ✅ **GroupBarItems** added to GroupBarItems collection
- ✅ **GroupView** created if displaying child items
- ✅ **Client property** set to link GroupView to GroupBarItem
- ✅ **Visual style** applied (VisualStyle property)
- ✅ **Dock property** set for proper layout (typically DockStyle.Left)
- ✅ **Event handlers** added for item selection
- ✅ **Testing** with multiple items and navigation

## Troubleshooting Quick Reference

**Issue:** GroupBar not visible
- Check if GroupBar is added to form's Controls
- Set Dock property (DockStyle.Left recommended)
- Verify Width property is sufficient (200-250 pixels typical)
- Ensure form has space for docked control

**Issue:** GroupBarItems not appearing
- Verify items are added to GroupBarItems collection
- Check Text property is set on each item
- Ensure GroupBar.Visible = true
- Verify items are not collapsed/hidden

**Issue:** Child items (GroupViewItems) not displaying
- Create GroupView instance
- Add GroupViewItems to GroupView.GroupViewItems collection
- Set GroupBarItem.Client = groupView
- Add GroupView to GroupBar.Controls collection

**Issue:** StackedMode not working
- Set StackedMode = true
- Ensure multiple GroupBarItems exist (need 2+ for stacking)
- Check HeaderHeight property (0 hides header)
- Verify visual style supports stacked mode

**Issue:** Theme not applying
- Set VisualStyle property to desired theme
- For Office2007/2010, set corresponding theme property (Office2007Theme, Office2010Theme)
- For managed colors, call ApplyManagedColors method
- Ensure Syncfusion.Shared.Base assembly is referenced

**Issue:** GroupView selection not working
- Handle GroupViewItemSelected event
- Check GroupView.SelectedItem property
- Ensure GroupViewItems have unique identifiers
- Verify click events are wired up

## Summary

GroupBar (Navigation Pane) provides Outlook-style navigation functionality with:

- **Hierarchical Navigation**: GroupBarItem groups with GroupView child items
- **Stacked Mode**: Outlook-style navigation pane with collapsible sections
- **Office Themes**: Office 2007/2010/2016, Metro, and custom themes
- **Nested Support**: GroupBar within GroupBar capability
- **Serialization**: Save/restore layout state
- **Customizable Appearance**: Headers, borders, colors, animations

Use GroupBar when Outlook-style navigation, toolbox interfaces, categorized hierarchies, or themed navigation containers are needed for creating professional and organized WinForms applications.
