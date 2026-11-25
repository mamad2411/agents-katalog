---
name: syncfusion-winui-shadow
description: Guide for implementing the Syncfusion WinUI Shadow (SfShadow) control to add depth and elevation effects to UI elements. Use this skill when implementing shadow effects, applying shadows to buttons/images/shapes, creating visual depth and elevation, or adding drop shadows for UI layering in WinUI 3. Covers installation, basic usage, and customization options including shadow color, blur, offset, and corner radius for material design depth effects.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Shadow Control (SfShadow)

The Syncfusion WinUI Shadow control (`SfShadow`) applies customizable shadow effects to any framework element, creating visual depth and helping users distinguish overlapping UI elements. Shadow effects enhance the user interface by adding dimension and visual hierarchy following modern design principles.

## When to Use This Skill

Use the Shadow control when you need to:
- **Add depth to UI elements** - Apply shadows to buttons, cards, panels, or images
- **Create visual hierarchy** - Differentiate layers and elevations in the interface
- **Enhance material design** - Implement elevation effects for modern UI patterns
- **Improve UX clarity** - Help users identify interactive or important elements
- **Add polish to designs** - Create professional, appealing user interfaces

**Trigger keywords:** shadow, SfShadow, depth, elevation, drop shadow, blur effect, visual depth, layering, material design, overlapping elements

## Component Overview

**Control:** `SfShadow`  
**Namespace:** `Syncfusion.UI.Xaml.Core`  
**NuGet Package:** `Syncfusion.Core.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+)

### Key Capabilities
- Apply shadows to any framework element (buttons, images, shapes, paths)
- Customize shadow color with alpha transparency
- Control blur intensity for soft or sharp shadows
- Adjust shadow position with X/Y offsets
- Match shadow corners to element corner radius
- Enable/disable shadows dynamically
- Automatic theme support (light/dark modes)

## Documentation and Navigation Guide

### Getting Started and Basic Usage
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing Syncfusion.Core.WinUI NuGet package
- Creating WinUI 3 desktop application
- Importing Syncfusion.UI.Xaml.Core namespace
- Initializing SfShadow control in XAML and C#
- Applying shadows to buttons
- Applying shadows to images
- Applying shadows to shapes and paths
- Complete code examples for each scenario

### Customization Options
📄 **Read:** [references/customization.md](references/customization.md)
- Changing shadow color (Color property)
- Adjusting blur radius (BlurRadius property)
- Setting corner radius (ShadowCornerRadius property)
- Positioning shadows (OffsetX, OffsetY properties)
- Enabling/disabling shadows (EnableShadow property)
- Default values for all properties
- Combining multiple customizations
- Advanced visual effects

## Quick Start Example

### Basic Shadow for Button

**XAML:**
```xml
<Page
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:syncfusion="using:Syncfusion.UI.Xaml.Core">
    
    <Grid>
        <syncfusion:SfShadow>
            <Button Height="50" Width="100" Content="Click Me"/>
        </syncfusion:SfShadow>
    </Grid>
</Page>
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Core;

// Create shadow control
SfShadow shadow = new SfShadow();

// Create button
Button button = new Button();
button.Height = 50;
button.Width = 100;
button.Content = "Click Me";

// Add button to shadow
shadow.Content = button;
```

## Common Patterns

### 1. Elevated Button with Custom Shadow

```xml
<syncfusion:SfShadow 
    Color="DarkBlue" 
    BlurRadius="10" 
    OffsetX="5" 
    OffsetY="5">
    <Button Height="50" Width="120" Content="Action"/>
</syncfusion:SfShadow>
```

### 2. Card with Soft Shadow

```xml
<syncfusion:SfShadow 
    BlurRadius="15" 
    OffsetX="0" 
    OffsetY="8"
    ShadowCornerRadius="8">
    <Border 
        Background="White" 
        CornerRadius="8" 
        Padding="20">
        <TextBlock Text="Card Content"/>
    </Border>
</syncfusion:SfShadow>
```

### 3. Image with Shadow Effect

```xml
<syncfusion:SfShadow 
    BlurRadius="12" 
    OffsetX="4" 
    OffsetY="4">
    <Image 
        Height="150" 
        Width="150" 
        Source="/Assets/photo.png"/>
</syncfusion:SfShadow>
```

### 4. Circular Button with Matching Shadow

```xml
<syncfusion:SfShadow 
    ShadowCornerRadius="25"
    BlurRadius="8"
    OffsetX="3"
    OffsetY="3">
    <Button 
        Height="50" 
        Width="50" 
        CornerRadius="25"
        Content="+"
        FontSize="24"/>
</syncfusion:SfShadow>
```

### 5. Star Rating with Shadows

```xml
<StackPanel Orientation="Horizontal">
    <syncfusion:SfShadow>
        <Path Data="M44.5 4L54.0608 33.4114H85L59.9696 51.5886L69.5304 81L44.5 62.8228L19.4696 81L29.0304 51.5886L4 33.4114H34.9392L44.5 4Z" 
              Fill="#FFD700"/>
    </syncfusion:SfShadow>
    <!-- Repeat for more stars -->
</StackPanel>
```

### 6. Conditionally Enabled Shadow

```xml
<syncfusion:SfShadow EnableShadow="{Binding IsElevated}">
    <Button Content="Toggle Shadow"/>
</syncfusion:SfShadow>
```

```csharp
// Toggle shadow programmatically
shadow.EnableShadow = false; // Disable shadow
shadow.EnableShadow = true;  // Enable shadow
```

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Content` | object | null | The UI element to apply shadow to |
| `Color` | Color | Black (25% alpha) | Shadow color with transparency |
| `BlurRadius` | double | 8 | Blur intensity (higher = softer shadow) |
| `ShadowCornerRadius` | double | 0 | Corner radius of the shadow |
| `OffsetX` | double | 4 | Horizontal shadow offset (+ = right, - = left) |
| `OffsetY` | double | 4 | Vertical shadow offset (+ = down, - = up) |
| `EnableShadow` | bool | true | Show or hide shadow effect |

### Property Usage Tips

**Color:**
- Use semi-transparent colors for realistic shadows
- Match shadow color to background for subtle effects
- Use darker shadows for higher elevations

**BlurRadius:**
- 0-5: Sharp, close shadows (low elevation)
- 8-12: Standard elevation shadows
- 15+: Soft, distant shadows (high elevation)

**Offsets:**
- Equal X/Y: Diagonal shadow (balanced depth)
- X=0, Y>0: Drop shadow (common pattern)
- Negative values: Shadow above/left of element

**ShadowCornerRadius:**
- Should match the content's CornerRadius
- Creates seamless shadow appearance
- Essential for rounded buttons/cards

## Common Use Cases

### Material Design Elevation Levels

**Level 1 (Resting):**
```xml
<syncfusion:SfShadow OffsetX="0" OffsetY="2" BlurRadius="4">
    <Button Content="Resting"/>
</syncfusion:SfShadow>
```

**Level 2 (Raised):**
```xml
<syncfusion:SfShadow OffsetX="0" OffsetY="4" BlurRadius="8">
    <Button Content="Raised"/>
</syncfusion:SfShadow>
```

**Level 3 (Elevated):**
```xml
<syncfusion:SfShadow OffsetX="0" OffsetY="8" BlurRadius="16">
    <Button Content="Elevated"/>
</syncfusion:SfShadow>
```

### Hover Effect with Shadow

```xml
<Button.Style>
    <Style TargetType="Button">
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="Button">
                    <syncfusion:SfShadow x:Name="ButtonShadow" OffsetY="2" BlurRadius="4">
                        <ContentPresenter/>
                    </syncfusion:SfShadow>
                    <ControlTemplate.Triggers>
                        <Trigger Property="IsMouseOver" Value="True">
                            <Setter TargetName="ButtonShadow" Property="OffsetY" Value="8"/>
                            <Setter TargetName="ButtonShadow" Property="BlurRadius" Value="16"/>
                        </Trigger>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
</Button.Style>
```

### Gallery with Image Shadows

```xml
<ItemsControl ItemsSource="{Binding Photos}">
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <syncfusion:SfShadow 
                BlurRadius="10" 
                OffsetX="4" 
                OffsetY="4"
                Margin="10">
                <Image Source="{Binding ImagePath}" Height="150" Width="150"/>
            </syncfusion:SfShadow>
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>
```

## Best Practices

### Performance
- Use shadows sparingly on frequently updated elements
- Consider disabling shadows during animations if performance is impacted
- Reduce blur radius for better performance in lists with many items

### Visual Design
- **Consistent elevation**: Use the same shadow settings for elements at the same elevation level
- **Natural light source**: Position shadows as if light comes from top-left (OffsetX=4, OffsetY=4)
- **Subtle shadows**: Avoid harsh shadows; use transparency and blur
- **Theme adaptation**: Test shadows in both light and dark themes

### Accessibility
- Don't rely solely on shadows to convey information
- Ensure sufficient color contrast regardless of shadow
- Provide alternative visual cues for shadow-based depth

### Common Mistakes to Avoid
- ❌ Setting `ShadowCornerRadius` without matching content's `CornerRadius`
- ❌ Using opaque black shadows (always add transparency)
- ❌ Excessive blur radius on many elements (performance impact)
- ❌ Inconsistent shadow directions across the UI
- ❌ Forgetting to import Syncfusion.UI.Xaml.Core namespace

## Troubleshooting

**Shadow not visible:**
- Verify `EnableShadow` is `true`
- Check if shadow offset is sufficient (try increasing OffsetX/OffsetY)
- Ensure blur radius is greater than 0
- Verify shadow isn't same color as background
- Check if content has transparent background

**Shadow appears clipped:**
- Add margin/padding around SfShadow
- Increase parent container size
- Verify ClipToBounds is not set to true on parent

**Performance issues:**
- Reduce number of shadows in view
- Decrease blur radius
- Use EnableShadow to conditionally show shadows
- Consider virtualization for lists with shadowed items

## Related Components

- **Border** - Combine with SfShadow for card-like containers
- **Button** - Common target for shadow effects
- **Image** - Apply shadows to photos and icons
- **Shapes/Paths** - Create custom shadowed graphics

---

**Need more details?** Read the reference files linked in the Navigation Guide above for comprehensive documentation and examples.
