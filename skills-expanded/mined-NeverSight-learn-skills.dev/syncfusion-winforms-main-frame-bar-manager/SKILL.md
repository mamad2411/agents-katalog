---
name: syncfusion-winforms-main-frame-bar-manager
description: Comprehensive guide for implementing Syncfusion MainFrameBarManager menu and toolbar system in Windows Forms. Use when creating menus, toolbars, command bars, or menu structures. Covers hierarchical menu models, BarItem types, interactive features, keyboard support, MDI integration, and state persistence for building professional menu-driven applications with shortcuts, mnemonics, tooltips, and customizable toolbars.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinForms MainFrameBarManager

## When to Use This Skill

The MainFrameBarManager component is essential when you need to:
- Create hierarchical menu structures (File, Edit, View menus with submenus)
- Build customizable toolbars and command bars
- Add keyboard shortcuts and mnemonics to menu items
- Implement context menus and interactive tooltips
- Support MDI (Multiple Document Interface) applications with merged menus
- Persist menu and toolbar state between application sessions
- Enable end-users to customize menu layout at runtime

This component follows the XP Menus Framework pattern, providing a professional, enterprise-grade menu management system for Windows Forms applications.

## Quick Start Example

```csharp
// Create MainFrameBarManager
MainFrameBarManager mainFrameBarManager1 = new MainFrameBarManager();
mainFrameBarManager1.Style = Syncfusion.Windows.Forms.VisualStyle.Office2016Colorful;
mainFrameBarManager1.Form = this;

// Create a bar (menu container)
Bar fileBar = new Syncfusion.Windows.Forms.Tools.XPMenus.Bar();
fileBar.BarName = "File";
fileBar.Caption = "File";
fileBar.Manager = mainFrameBarManager1;

// Create parent menu item
ParentBarItem fileMenu = new ParentBarItem();
fileMenu.Text = "&File";

// Create sub-menu items
BarItem newItem = new BarItem() { Text = "&New" };
BarItem openItem = new BarItem() { Text = "&Open" };
BarItem exitItem = new BarItem() { Text = "E&xit" };

// Assign shortcuts and mnemonics
newItem.Shortcut = Shortcut.CtrlN;
openItem.Shortcut = Shortcut.CtrlO;
exitItem.Shortcut = Shortcut.AltF4;

// Build hierarchy
fileMenu.Items.AddRange(new BarItem[] { newItem, openItem, exitItem });
fileBar.Items.Add(fileMenu);

// Add to manager
mainFrameBarManager1.Items.AddRange(new BarItem[] { fileMenu, newItem, openItem, exitItem });
mainFrameBarManager1.Bars.Add(fileBar);
mainFrameBarManager1.Categories.Add("Menu");
```

## Common Patterns

### Pattern 1: Creating Multi-Level Menus
Create nested ParentBarItems for submenus (File → Recent → Document1). Group related items under parent containers.

### Pattern 2: Adding Interactive Controls
Use DropDownBarItem with PopupControlContainer for color pickers, ComboBoxBarItem for selections, TextBoxBarItem for input fields.

### Pattern 3: Implementing Customization
Enable AutoPersistCustomization to allow users to rearrange menu items and save their preferences automatically.

### Pattern 4: MDI Application Integration
Use MainFrameBarManager for parent forms and ChildFrameBarManager for child forms. Call RegisterMdiChildTypes() for automatic menu merging.

### Pattern 5: Keyboard Navigation
Assign Shortcut properties and use & symbol in Text for mnemonics (e.g., "&Save" creates Alt+S).

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| **Form** | Form | Associates the menu manager with the parent form |
| **Style** | VisualStyle | Sets the visual style (Office2016, XPBlue, etc.) |
| **Bars** | BarCollection | Collection of Bar instances (menus, toolbars) |
| **Items** | BarItemCollection | All BarItem instances managed by this manager |
| **Categories** | StringCollection | Categories for organizing menu items in customization UI |
| **AutoLoadToolBarPositions** | bool | Auto-loads saved toolbar positions on startup |
| **AutoPersistCustomization** | bool | Auto-saves menu and toolbar customizations |
| **DetachedCommandBars** | CommandBarCollection | Collection of detachable CommandBar instances |

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package setup and assembly references
- Creating MainFrameBarManager instance
- Setting visual styles and form association
- License key configuration

### Building Menus
📄 **Read:** [references/menu-items-via-code.md](references/menu-items-via-code.md)
- Creating Bar instances programmatically
- Adding BarItem and ParentBarItem
- Child item hierarchies and sub-menus
- Event handler setup with code examples

📄 **Read:** [references/menu-items-via-designer.md](references/menu-items-via-designer.md)
- Designer-based menu creation (drag-and-drop)
- Customize dialog for bars and items
- Visual arrangement through UI
- Automatic assembly reference injection

### Menu Item Types & Features
📄 **Read:** [references/menu-item-types.md](references/menu-item-types.md)
- BarItem (basic clickable items)
- ParentBarItem (submenu containers)
- DropDownBarItem (custom popup controls)
- ComboBoxBarItem (dropdown selections)
- StaticBarItem (label-like display items)
- TextBoxBarItem (text input fields)
- ToolBarListBarItem (toolbar customization options)

### Interactive Features
📄 **Read:** [references/interactive-features.md](references/interactive-features.md)
- SuperTooltip setup and appearance customization
- Context menu integration
- Tooltip visibility control
- Advanced tooltip editor configuration

### Keyboard & Accessibility
📄 **Read:** [references/keyboard-support.md](references/keyboard-support.md)
- Assigning keyboard shortcuts to menu items
- Mnemonic text implementation with & symbol
- ShowMnemonicUnderlinesAlways property
- Keyboard navigation patterns

### State Persistence & MDI
📄 **Read:** [references/state-persistence-mdi.md](references/state-persistence-mdi.md)
- Enabling state persistence with AutoLoadToolBarPositions
- Automatic customization serialization
- MDI parent/child form integration
- ChildFrameBarManager and menu merging
- RegisterMdiChildTypes() for explicit merging
- MDI merge behavior matrix

### Detachable Toolbars
📄 **Read:** [references/detachable-command-bars.md](references/detachable-command-bars.md)
- CommandBar creation and docking
- DockState property configuration
- Adding to DetachedCommandBars collection
- Designer vs. code-based approaches

## Common Use Cases

**File Menu:** Create a standard File menu with New, Open, Save, Recent Documents, and Exit items using ParentBarItem hierarchy.

**Toolbar:** Use multiple Bar instances with different BarNames to create separate toolbars, each docked to different positions.

**Search Bar:** Add TextBoxBarItem or ComboBoxBarItem to toolbar for search/filter functionality.

**Color Picker in Menu:** Use DropDownBarItem with PopupControlContainer containing ColorPickerUIAdv control.

**Localized Menus:** Set Text property to localized strings; mnemonics and shortcuts work across all languages.

**Custom Shortcuts:** Assign Shortcut.None to items without shortcuts, or use custom key combinations via Shortcut enum.

## Quick Links

- [Syncfusion WinForms Menu API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.XPMenus.MainFrameBarManager.html)
- [BarItem API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.XPMenus.BarItem.html)
- [Bar Component Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.XPMenus.Bar.html)
