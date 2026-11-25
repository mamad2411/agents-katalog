---
name: syncfusion-winui-dropdown-color-palette
description: Guide implementation of the Syncfusion WinUI DropDown Color Palette control for color selection in Windows desktop applications. Use this skill when implementing color selection dropdowns, theme color support, custom color palettes, split-mode buttons, or the More Colors dialog. Covers dropdown customization, palette structure, and color-based UI interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI DropDown Color Palette

The `SfDropDownColorPalette` control provides a rich visual interface for color selection. It displays a dropdown with selected color highlighted at the top, offers standard colors, theme colors with variants, and supports custom color palettes and additional color selection through a More Colors dialog.

## When to Use This Skill

Use this skill when you need to:
- Add color selection to your WinUI application
- Let users choose from theme and standard color palettes
- Customize available colors for your brand
- Implement a split-mode button with color selection
- Track recently selected colors
- Show color tooltips on hover
- Allow users to pick any color from a spectrum

## Control Overview

The DropDown Color Palette combines several color selection areas:

| Section | Purpose |
|---------|---------|
| Selected Color Button | Displays currently selected color; clicking opens palette |
| Automatic Color | Quick access to default color (usually black) |
| Theme Colors | Predefined theme colors with shade variants |
| Standard Colors | 10 standard colors (red, green, blue, yellow, etc.) |
| Recently Used | Colors selected from More Colors dialog |
| More Colors... | Opens spectrum dialog for any color |

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Install NuGet package (Syncfusion.Editors.WinUI)
 - Install NuGet package (Syncfusion.Editors.WinUI)
 - Note: ensure the NuGet package is updated to the latest `Syncfusion.Editors.WinUI` version via the NuGet package manager.
- Add control in XAML and C#
- Set selected color programmatically (SelectedBrush)
- Handle SelectedBrushChanged event
- Access color value in code

### Control Structure
📄 **Read:** [references/palette-structure.md](references/palette-structure.md)
- Understand each color section (selected, automatic, theme, standard, recent)
- Learn about color tooltips
- Discover More Colors option
- Understand theme variant behavior

### Dropdown Customization
📄 **Read:** [references/dropdown-customization.md](references/dropdown-customization.md)
- Change dropdown alignment (DropDownPlacement)
- Convert to split-mode button (DropDownMode = Split)
- Bind commands for button click action
- Customize header UI with templates
- Handle dropdown open/close events

### Palette Customization
📄 **Read:** [references/color-palette-customization.md](references/color-palette-customization.md)
- Add custom colors to palette
- Define custom theme color groups
- Add custom standard colors
- Remove unwanted color sections
- Integrate SfColorPalette for advanced customization

### More Colors Dialog
📄 **Read:** [references/more-colors-dialog.md](references/more-colors-dialog.md)
- Let users pick any color from spectrum
- Track recently used colors
- Differentiate recent colors from palette colors
- Customize color spectrum behavior

## Quick Start

### Basic Implementation (XAML)

```xaml
<Page
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:editors="using:Syncfusion.UI.Xaml.Editors">
    <Grid>
        <editors:SfDropDownColorPalette x:Name="colorPalette" />
    </Grid>
</Page>
```

### Basic Implementation (C#)

```csharp
using Syncfusion.UI.Xaml.Editors;

public sealed partial class MainPage : Page
{
    public MainPage()
    {
        this.InitializeComponent();
        var colorPalette = new SfDropDownColorPalette();
        grid.Children.Add(colorPalette);
    }
}
```

## Common Patterns

### Pattern 1: Set and Get Selected Color

```xaml
<editors:SfDropDownColorPalette SelectedBrush="Yellow" x:Name="palette" />
```

```csharp
// Get the selected color
var selectedBrush = palette.SelectedBrush as SolidColorBrush;
if (selectedBrush != null)
{
    Color selectedColor = selectedBrush.Color;
}

// Set a new color
palette.SelectedBrush = new SolidColorBrush(Colors.Red);
```

### Pattern 2: Respond to Color Selection Changes

```xaml
<editors:SfDropDownColorPalette 
    SelectedBrushChanged="Palette_SelectedBrushChanged"
    x:Name="palette" />
```

```csharp
private void Palette_SelectedBrushChanged(object sender, SelectedBrushChangedEventArgs e)
{
    var oldBrush = e.OldBrush as SolidColorBrush;
    var newBrush = e.NewBrush as SolidColorBrush;
    
    // Apply color somewhere
    textBlock.Foreground = newBrush;
}
```

### Pattern 3: Split Mode with Command

```xaml
<editors:SfDropDownColorPalette 
    DropDownMode="Split"
    Command="{x:Bind ApplyColorCommand}"
    x:Name="palette" />
```

```csharp
private ICommand applyColorCommand;
public ICommand ApplyColorCommand => applyColorCommand;

public void ApplyColorToSelectedText(object param)
{
    // Apply the currently selected color
    richTextBox.Document.Selection.CharacterFormat.BackgroundColor = 
        (palette.SelectedBrush as SolidColorBrush).Color;
}
```

### Pattern 4: Dropdown Alignment

```xaml
<editors:SfDropDownColorPalette 
    DropDownPlacement="BottomEdgeAlignedRight"
    x:Name="palette" />
```

**Common Placement Options:**
- `Auto` - Best available position (default)
- `BottomEdgeAlignedLeft` - Below, left-aligned
- `BottomEdgeAlignedRight` - Below, right-aligned
- `TopEdgeAlignedLeft` - Above, left-aligned
- `TopEdgeAlignedRight` - Above, right-aligned

### Pattern 5: Detect Palette Open/Close

```xaml
<editors:SfDropDownColorPalette 
    DropDownOpened="Palette_DropDownOpened"
    DropDownClosed="Palette_DropDownClosed"
    x:Name="palette" />
```

```csharp
private void Palette_DropDownOpened(object sender, EventArgs e)
{
    // Palette opened
}

private void Palette_DropDownClosed(object sender, EventArgs e)
{
    // Palette closed
}
```

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `SelectedBrush` | `Brush` | Gets/sets the currently selected color (default: Black) |
| `DropDownPlacement` | `FlyoutPlacementMode` | Position of dropdown relative to button (default: Auto) |
| `DropDownMode` | `DropDownMode` | Dropdown or Split mode (default: Dropdown) |
| `Command` | `ICommand` | Command executed when button clicked (Split mode) |
| `ContentTemplate` | `DataTemplate` | Customize selected color button appearance |
| `DropDownButtonTemplate` | `DataTemplate` | Customize dropdown arrow button (Split mode) |

## Reference Files

All detailed documentation is organized by feature:

- **getting-started.md** - Setup and basic implementation
- **palette-structure.md** - Understanding color sections
- **dropdown-customization.md** - Button and dropdown customization
- **color-palette-customization.md** - Custom color definitions
- **more-colors-dialog.md** - Spectrum picker and recent colors

---

**Ready to implement?** Choose a specific task from the Navigation Guide above and read the corresponding reference file.
