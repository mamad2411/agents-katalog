---
name: syncfusion-winforms-radial-menu
description: Guide for implementing Syncfusion RadialMenu control in Windows Forms applications. Use when creating circular context menus, hierarchical radial navigation, or touch-friendly circular menu interfaces. Covers RadialColorPalette for color pickers, RadialFontListBox for font selection, RadialMenuSlider for numeric input, and Office 2016 themed menus for modern circular navigation beyond standard context menus.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing RadialMenu in Syncfusion WinForms

This skill guides you in implementing **Syncfusion WinForms RadialMenu** control—a circular hierarchical context menu with specialized elements like color palettes, font selectors, and numeric sliders.

## When to Use This Skill

Use this skill when the user needs to:

- Implement **circular context menus** with hierarchical structure
- Create **touch-friendly radial navigation** for tablet/touch applications
- Add **RadialColorPalette** for color selection in radial layout
- Implement **RadialFontListBox** for font family selection
- Add **RadialMenuSlider** for numeric value input (min/max range)
- Apply **Office 2016 themes** (Colorful, White, DarkGray, Black)
- Create **custom context menus** with checkboxes and radio buttons
- Enable **keyboard shortcuts** with SuperAccelerator (Alt+key)
- Implement **submenu hierarchies** in circular layout
- Customize **visual appearance** (colors, rim, arc, display styles)
- Replace **standard context menus** with modern radial alternatives

RadialMenu is ideal for touch-enabled applications, graphics editors, and applications requiring quick access to contextual commands in a circular layout.

## Component Overview

**RadialMenu** is a circular hierarchical menu control that displays commands in a radial layout. It serves as a modern context menu with specialized input elements. Key capabilities:

- **Hierarchical Structure**: Menu items with submenu support (drill-down navigation)
- **RadialMenuItem**: Standard menu items with checkbox/radio button modes
- **RadialColorPalette**: Color picker integrated into radial menu
- **RadialFontListBox**: Font family selector in radial layout
- **RadialMenuSlider**: Numeric slider for value ranges
- **Office 2016 Themes**: 5 professional built-in visual styles
- **Customizable Styling**: Colors, rim thickness, arc gaps, display modes
- **Keyboard Support**: SuperAccelerator for Alt+key shortcuts
- **Touch Optimization**: Large touch targets in circular layout
- **Tooltips**: Hover tooltips for menu items

**Key Difference from Standard ContextMenu:**
RadialMenu provides a circular layout optimized for touch, with specialized elements (color palette, font list, slider) and modern Office 2016 themes.

## Documentation and Navigation Guide

### Getting Started and Basic Setup

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when users need:
- Assembly dependencies and NuGet package installation
- Namespace: Syncfusion.Windows.Forms.Tools
- Creating RadialMenu via designer or code
- Adding to form and making visible
- Adding basic menu items to Items collection
- Understanding control hierarchy
- Complete minimal working example

### Menu Items and Hierarchical Structure

📄 **Read:** [references/menu-items-and-structure.md](references/menu-items-and-structure.md)

Read this reference when users need:
- Creating RadialMenuItem instances
- Hierarchical menus with submenu items
- CheckMode property (None, CheckBox, RadioButton)
- GroupName for radio button grouping
- Building nested menu structures
- Click event handling
- Examples: checkbox items, radio groups, submenus

### Special Elements (Color Palette, Font List, Slider)

📄 **Read:** [references/special-elements.md](references/special-elements.md)

Read this reference when users need:
- RadialColorPalette for color selection
- RadialFontListBox for font family selection
- RadialMenuSlider for numeric value input
- MinimumValue and MaximumValue configuration
- Color/font/value selection event handling
- Integration with main menu items
- Complete examples for each element type

### Styling and Appearance Customization

📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)

Read this reference when users need:
- Drill region colors (OuterArcColor, OuterArcHighLightedColor)
- Outer rim customization (RimBackground, OuterRimThickness)
- Arc gap configuration (OuterArcGap)
- DisplayStyle (Text, Image, TextAboveImage, ImageAboveText)
- Image size customization (MenuItemImageSize, ImageSize)
- Center icon configuration (Icon property)
- Custom styling examples

### Themes and Visual Styles

📄 **Read:** [references/themes-and-styles.md](references/themes-and-styles.md)

Read this reference when users need:
- Style property overview
- Office 2016 themes (Colorful, White, DarkGray, Black)
- Default theme
- Theme comparison and selection guide
- Applying themes at runtime
- Theme best practices

### Advanced Features and Configuration

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

Read this reference when users need:
- WedgeCount property (slice count configuration)
- MenuVisibility property for initial display
- PersistPreviousState for state restoration
- ImageList configuration (ImageListAdv)
- UseIndexBasedOrder for item arrangement
- Keyboard support with SuperAccelerator
- Accelerator key configuration (Alt+key)
- ShowTooltip property and tooltip customization
- Advanced configuration examples

## Quick Start Example

Here's a minimal example creating a RadialMenu with menu items:

```csharp
using Syncfusion.Windows.Forms.Tools;
using System;
using System.Drawing;
using System.Windows.Forms;

public class RadialMenuExample : Form
{
    private RadialMenu radialMenu1;
    
    public RadialMenuExample()
    {
        // Create RadialMenu
        radialMenu1 = new RadialMenu();
        radialMenu1.Visible = true;
        radialMenu1.Style = RadialMenuStyle.Office2016Colorful;
        
        // Create menu items
        RadialMenuItem editItem = new RadialMenuItem();
        editItem.Text = "Edit";
        
        RadialMenuItem cutItem = new RadialMenuItem();
        cutItem.Text = "Cut";
        
        RadialMenuItem copyItem = new RadialMenuItem();
        copyItem.Text = "Copy";
        
        RadialMenuItem pasteItem = new RadialMenuItem();
        pasteItem.Text = "Paste";
        
        // Add items to menu
        radialMenu1.Items.Add(editItem);
        radialMenu1.Items.Add(cutItem);
        radialMenu1.Items.Add(copyItem);
        radialMenu1.Items.Add(pasteItem);
        
        // Add menu to form
        this.Controls.Add(radialMenu1);
        
        this.Text = "RadialMenu Example";
        this.Size = new Size(500, 400);
    }
}
```

**Result:** A circular menu with 4 items (Edit, Cut, Copy, Paste) in Office 2016 Colorful theme.

## Common Patterns

### Context Menu with Submenu

**Pattern:** Create a radial context menu with hierarchical submenus.

```csharp
// Create main RadialMenu
RadialMenu contextMenu = new RadialMenu();
contextMenu.Visible = true;
contextMenu.Style = RadialMenuStyle.Office2016Colorful;

// Create main menu item with submenu
RadialMenuItem formatItem = new RadialMenuItem();
formatItem.Text = "Format";

// Create submenu items
RadialMenuItem boldItem = new RadialMenuItem();
boldItem.Text = "Bold";
boldItem.Click += (s, e) => ApplyBoldFormatting();

RadialMenuItem italicItem = new RadialMenuItem();
italicItem.Text = "Italic";
italicItem.Click += (s, e) => ApplyItalicFormatting();

// Add submenu items to parent
formatItem.Items.Add(boldItem);
formatItem.Items.Add(italicItem);

// Add to main menu
contextMenu.Items.Add(formatItem);
this.Controls.Add(contextMenu);
```

**When:** User needs hierarchical menu navigation with drill-down to submenus.

### Color Picker Menu

**Pattern:** Add color selection capability to radial menu.

```csharp
// Create RadialMenu
RadialMenu menu = new RadialMenu();
menu.Visible = true;
menu.Style = RadialMenuStyle.Office2016Colorful;

// Create RadialColorPalette
RadialColorPalette colorPalette = new RadialColorPalette();
colorPalette.Text = "Color";
colorPalette.ColorSelected += (s, e) => 
{
    // Handle color selection
    Color selectedColor = e.Color;
    ApplyColor(selectedColor);
};

// Add color palette to menu
menu.Items.Add(colorPalette);
this.Controls.Add(menu);
```

**When:** User needs color selection integrated into radial menu (graphics apps, text editors).

### Format Toolbar Menu with Slider

**Pattern:** Combine font selector, color picker, and size slider.

```csharp
// Create RadialMenu
RadialMenu formatMenu = new RadialMenu();
formatMenu.Visible = true;
formatMenu.Style = RadialMenuStyle.Office2016White;
formatMenu.WedgeCount = 3; // Reserve space for 3 items

// Font list
RadialFontListBox fontList = new RadialFontListBox();
fontList.Text = "Font";
fontList.SelectedFontChanged += (s, e) => 
{
    ApplyFont(fontList.SelectedFont);
};

// Color palette
RadialColorPalette colorPalette = new RadialColorPalette();
colorPalette.Text = "Color";

// Size slider
RadialMenuSlider sizeSlider = new RadialMenuSlider();
sizeSlider.Text = "Size";
sizeSlider.MinimumValue = 8;
sizeSlider.MaximumValue = 72;
sizeSlider.SliderValueChanged += (s, e) => 
{
    ApplyFontSize((int)sizeSlider.SliderValue);
};

// Add all elements
formatMenu.Items.Add(fontList);
formatMenu.Items.Add(colorPalette);
formatMenu.Items.Add(sizeSlider);

this.Controls.Add(formatMenu);
```

**When:** User needs comprehensive formatting controls in a compact radial menu.

## Key Properties

### Core Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Visible` | bool | Show/hide RadialMenu | Control visibility |
| `Style` | RadialMenuStyle | Visual theme | Apply Office 2016 themes |
| `Items` | Collection | Menu items collection | Add RadialMenuItem, palette, etc. |
| `WedgeCount` | int | Maximum visible menu slices | Reserve space for items |
| `MenuVisibility` | bool | Display menu on load | Show menu initially |

### Styling Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `OuterArcColor` | Color | Drill region color (normal) | Customize arc appearance |
| `OuterArcHighLightedColor` | Color | Drill region color (hover) | Customize hover effect |
| `RimBackground` | Color | Outer rim color | Customize rim appearance |
| `OuterRimThickness` | int | Rim thickness in pixels | Adjust rim size |
| `OuterArcGap` | int | Gap between rim and arc | Adjust spacing |
| `DisplayStyle` | DisplayStyle | Text/image layout | Control item appearance |
| `MenuItemImageSize` | Size | Image size for all items | Set uniform image size |
| `Icon` | Image | Center icon | Add custom center icon |

### Advanced Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `PersistPreviousState` | bool | Restore previous menu state | Maintain navigation state |
| `ImageList` | ImageListAdv | Image collection | Provide custom images |
| `UseIndexBasedOrder` | bool | Index-based item ordering | Control item positions |
| `ShowToolTip` | bool | Enable tooltips | Show item descriptions |

### RadialMenuItem Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Text` | string | Menu item text | Display item label |
| `ImageIndex` | int | Image index from ImageList | Add item icon |
| `CheckMode` | CheckMode | None/CheckBox/RadioButton | Enable checking behavior |
| `GroupName` | string | Radio button group | Group radio buttons |
| `Items` | Collection | Submenu items | Create hierarchical menus |

## Common Use Cases

### Graphics and Image Editors

Radial context menus for editing tools:
- Color palette for fill/stroke colors
- Font selector for text tools
- Size slider for brush/pen size
- Edit commands (cut, copy, paste)

### Touch-Enabled Applications

Touch-optimized circular menus:
- Large touch targets in radial layout
- Quick access to common commands
- Submenu navigation with drill-down
- Tablet/stylus friendly interface

### Text Editors and Word Processors

Formatting context menus:
- Font family selection
- Text color picker
- Font size slider
- Style toggles (bold, italic, underline)

### CAD and Design Applications

Design tool context menus:
- Object manipulation commands
- Layer controls
- Snapping options
- View controls

## Implementation Checklist

When implementing RadialMenu, ensure:

- ✅ **Required assemblies** referenced (Syncfusion.Tools.Windows.dll, etc.)
- ✅ **Namespace** included (Syncfusion.Windows.Forms.Tools)
- ✅ **RadialMenu instance** created and configured
- ✅ **Visible property** set to true (or toggled on demand)
- ✅ **Style property** set for theme (Office2016Colorful recommended)
- ✅ **Menu items** added to Items collection
- ✅ **Click event handlers** added for menu items
- ✅ **WedgeCount** configured if using many items
- ✅ **ImageList** configured if using custom icons
- ✅ **Testing** with mouse and touch (if applicable)

## Troubleshooting Quick Reference

**Issue:** RadialMenu not visible
- Set `Visible = true`
- Ensure menu is added to form's Controls
- Check Location property is within form bounds
- Verify form has focus

**Issue:** Menu items not appearing
- Check Items collection is populated
- Verify WedgeCount >= item count
- Ensure items have Text or ImageIndex set
- Check DisplayStyle property

**Issue:** Submenu navigation not working
- Add items to parent's Items collection (not menu's Items)
- Ensure child items have Text property set
- Check hierarchical structure is correct

**Issue:** Images not displaying
- Configure ImageList property
- Set ImageIndex on menu items
- Verify images exist in ImageListAdv
- Check DisplayStyle includes images

**Issue:** Keyboard shortcuts not working
- Add SuperAccelerator component
- Use SetAccelerator method for each item
- Ensure form has focus
- Press Alt key to activate

**Issue:** Color palette/font list not showing
- Create RadialColorPalette or RadialFontListBox instance
- Add to menu's Items collection (not RadialMenuItem)
- Check Text property is set
- Verify ImageIndex if using custom icons

## Summary

RadialMenu provides circular hierarchical menu functionality with:

- **Circular Layout**: Touch-optimized radial menu structure
- **Specialized Elements**: Color palette, font list, numeric slider
- **Office 2016 Themes**: 5 professional visual styles
- **Hierarchical Navigation**: Submenu support with drill-down
- **Customizable Styling**: Colors, rim, arc, display modes
- **Keyboard Support**: Alt+key shortcuts via SuperAccelerator

Use RadialMenu when touch-friendly circular context menus, specialized input elements (color/font/slider), or modern themed menus are needed for creating intuitive and accessible navigation in WinForms applications.
