---
name: syncfusion-winui-dropdown-color-picker
description: Guide for implementing Syncfusion WinUI DropDown Color Picker control for interactive color selection with dropdown functionality. Use this skill when implementing color selection with dropdown, color editing modes (RGB/HSV/HSL/CMYK/Hex), customizable dropdown placement, split button modes, or color picker flyout customization in WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI DropDown Color Picker

The WinUI DropDown Color Picker (`SfDropDownColorPicker`) is a versatile control for color selection and editing. It displays a color spectrum as a dropdown button with support for multiple color channel modes, opacity adjustment, and extensive customization options.

## When to Use This Skill

- **User needs**: Interactive color selection UI with dropdown behavior
- **User needs**: Support for multiple color formats (RGB, HSV, HSL, CMYK, Hexadecimal)
- **User needs**: Customizable dropdown placement and split button mode
- **User needs**: Embedded color picker customization within a dropdown
- **User needs**: Color change event handling and color binding
- **User needs**: Custom header UI or dropdown button styling

## Component Overview

### Key Features
- **Color Editing**: Drag to select colors or enter values manually in RGB, HSV, HSL, CMYK, or Hex formats
- **Hue Spectrum Slider**: Quickly select hue values
- **Color Channel Modes**: Switch between RGB, HSV, HSL, and CMYK color spaces
- **Split Mode**: Optional button + dropdown arrow separation
- **Dropdown Customization**: Control placement (full, center, left, right, top, bottom)
- **Opacity Control**: Adjust alpha/transparency values
- **Event Handling**: SelectedBrushChanged, DropDownOpened, DropDownClosed events
- **Custom Templates**: Customize header and dropdown button UI

### Required NuGet Package
- `Syncfusion.Editors.WinUI`
 
 **Note:** Ensure you update the `Syncfusion.Editors.WinUI` NuGet package to the latest available version via the NuGet package manager before building or releasing your application.

### Namespace
- `Syncfusion.UI.Xaml.Editors`

## Documentation and Navigation Guide

Choose the reference guide based on your task:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet setup
- Creating projects with DropDown Color Picker
- Basic XAML and C# implementation
- Programmatic color selection
- Interactive color selection
- Color channel switching (RGB, HSV, HSL, CMYK)
- Opacity and alpha value adjustment
- Hexadecimal color editor usage

### Color Picker Customization
📄 **Read:** [references/color-picker-customization.md](references/color-picker-customization.md)
- Customizing the embedded color picker
- Using AttachedFlyout and DropDownFlyout
- Brush type options (SolidColorBrush, LinearGradientBrush, etc.)
- Size and appearance customization
- Embedded color picker examples

### Dropdown Modes and Placement
📄 **Read:** [references/dropdown-modes-and-placement.md](references/dropdown-modes-and-placement.md)
- Dropdown placement modes
- DropDownPlacement property usage
- Split mode (button + dropdown arrow)
- Command binding in split mode
- Dropdown vs. full dropdown behavior
- Custom header UI styling

### Events and Commands
📄 **Read:** [references/events-and-commands.md](references/events-and-commands.md)
- SelectedBrushChanged event
- OldBrush and NewBrush properties
- DropDownOpened and DropDownClosed events
- Command binding patterns
- Event handling code examples

### Header and UI Customization
📄 **Read:** [references/header-and-ui-customization.md](references/header-and-ui-customization.md)
- ContentTemplate for selected color button
- DropDownButtonTemplate for dropdown button
- Custom UI styling in XAML
- Split mode custom headers
- DataContext binding patterns
- Complete template examples

## Quick Start Example

### Basic Implementation (XAML)

```xaml
<Page xmlns:editors="using:Syncfusion.UI.Xaml.Editors">
    <Grid>
        <editors:SfDropDownColorPicker x:Name="colorPicker" 
                                       SelectedBrush="Blue" />
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
        
        SfDropDownColorPicker colorPicker = new SfDropDownColorPicker();
        colorPicker.SelectedBrush = new SolidColorBrush(Colors.Blue);
        
        grid.Children.Add(colorPicker);
    }
}
```

### Listening to Color Changes

```csharp
// Subscribe to color change event
colorPicker.SelectedBrushChanged += ColorPicker_SelectedBrushChanged;

private void ColorPicker_SelectedBrushChanged(object sender, SelectedBrushChangedEventArgs e)
{
    var oldColor = e.OldBrush;
    var newColor = e.NewBrush;
    
    // Apply the selected color
    myElement.Background = newColor;
}
```

## Common Use Cases

### 1. Theme Color Selector
Allow users to select application theme colors:
```csharp
// User selects a color → apply to app background
SfDropDownColorPicker themeColorPicker = new SfDropDownColorPicker();
themeColorPicker.SelectedBrushChanged += (s, e) => 
{
    Window.Current.Content.Background = e.NewBrush;
};
```

### 2. Split Button Mode for Direct Application
Apply last selected color with button click, open dropdown to change:
```xaml
<editors:SfDropDownColorPicker DropDownMode="Split"
                               Command="{x:Bind ApplyColorCommand}" />
```

### 3. Custom Color Editor Interface
Embed specific color picker configuration:
```xaml
<editors:SfDropDownColorPicker>
    <FlyoutBase.AttachedFlyout>
        <editors:DropDownFlyout>
            <editors:SfColorPicker BrushTypeOptions="LinearGradientBrush" 
                                   Width="250" />
        </editors:DropDownFlyout>
    </FlyoutBase.AttachedFlyout>
</editors:SfDropDownColorPicker>
```

### 4. Positioned Dropdown (Top-Right)
Control where the color picker opens:
```xaml
<editors:SfDropDownColorPicker DropDownPlacement="TopEdgeAlignedRight" />
```

## Key Properties

| Property | Type | Purpose | Common Values |
|----------|------|---------|----------------|
| `SelectedBrush` | `Brush` | Currently selected color | `Colors.Blue`, `new SolidColorBrush()` |
| `DropDownMode` | `enum` | Dropdown behavior | `Dropdown`, `Split` |
| `DropDownPlacement` | `FlyoutPlacementMode` | Position of dropdown | `Full`, `Top`, `Bottom`, `Left`, `Right` |
| `Command` | `ICommand` | Command triggered on button click | Custom ICommand implementation |

## Common Patterns

### Pattern 1: Color Binding to UI Element
```csharp
// When color is selected, immediately apply to target element
void ColorPicker_SelectedBrushChanged(object sender, SelectedBrushChangedEventArgs e)
{
    targetRectangle.Fill = e.NewBrush;
}
```

### Pattern 2: Validating Color Selection
```csharp
void ColorPicker_SelectedBrushChanged(object sender, SelectedBrushChangedEventArgs e)
{
    // Validate color meets requirements
    if (IsValidColor(e.NewBrush))
    {
        ApplyColor(e.NewBrush);
    }
    else
    {
        colorPicker.SelectedBrush = e.OldBrush; // Revert
    }
}
```

### Pattern 3: Split Mode with Custom Command
```csharp
public ICommand QuickApplyCommand => new RelayCommand(() =>
{
    // Apply current selected color without opening dropdown
    ApplySelectedColorToTextSelection();
});
```

## Next Steps

- **Start with**: [getting-started.md](references/getting-started.md) to set up basic DropDown Color Picker
- **Then explore**: Other reference guides based on your specific needs
- **For production**: Review all guides for complete customization capabilities
