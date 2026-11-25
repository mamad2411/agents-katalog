---
name: syncfusion-winui-rating
description: Guide for implementing the Syncfusion WinUI Rating (SfRating) control to collect user ratings and feedback on a numeric scale. Use this when implementing star ratings, user reviews, or feedback collection in WinUI 3. This skill covers precision modes (full, half, exact), custom templates, tooltips, and read-only rating display.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Rating Control (SfRating)

The Syncfusion WinUI Rating control (`SfRating`) provides an intuitive interface for users to provide or view ratings on a numeric scale. Perfect for reviews, feedback systems, and rating displays, it supports various precision modes, custom templates, and extensive styling options.

## When to Use This Skill

Use the Rating control when you need to:
- **Collect user feedback** - Gather ratings for products, services, movies, or applications
- **Display existing ratings** - Show average ratings or user scores in read-only mode
- **Create review systems** - Build comprehensive review and rating interfaces
- **Implement feedback forms** - Add rating inputs to surveys and feedback forms
- **Show satisfaction levels** - Display emoji-based or star-based satisfaction scales
- **Support precision ratings** - Allow whole, half, or exact decimal ratings

**Trigger keywords:** rating, stars, star rating, SfRating, review, feedback, score, user rating, half star, precision, emoji rating, satisfaction, product rating

## Component Overview

**Control:** `SfRating`  
**Namespace:** `Syncfusion.UI.Xaml.Editors`  
**NuGet Package:** `Syncfusion.Editors.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+)

### Key Capabilities
- **Flexible initialization** - Use Items collection or ItemsCount property
- **Precision modes** - Full (whole), Half (0.5 increments), or Exact (any decimal)
- **Custom templates** - Stars, hearts, emojis, images, or custom shapes
- **Styling options** - Customize rated/unrated appearance, size, and orientation
- **Read-only mode** - Display ratings without allowing user interaction
- **Tooltip support** - Show rating values on hover with custom formatting
- **Clear functionality** - Allow users to reset their ratings
- **Placeholder values** - Display average ratings before user input
- **Accessibility** - Full keyboard navigation and screen reader support

## Documentation and Navigation Guide

### Getting Started and Basic Usage
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing Syncfusion.Editors.WinUI NuGet package
- Creating WinUI 3 desktop application
- Importing Syncfusion.UI.Xaml.Editors namespace
- Initializing SfRating control in XAML and C#
- Using Items collection approach with SfRatingItem
- Using ItemsCount approach (simpler method)
- Setting rating values programmatically
- First complete rating implementation

### Precision Modes
📄 **Read:** [references/precision.md](references/precision.md)
- Understanding Precision property
- Full precision mode (whole numbers only: 1, 2, 3, etc.)
- Half precision mode (half increments: 1.5, 2.5, 3.5, etc.)
- Exact precision mode (any decimal value: 2.7, 3.2, etc.)
- User interaction behavior for each mode
- Choosing the right precision for your use case
- Examples demonstrating each precision type

### Customization Options
📄 **Read:** [references/customization.md](references/customization.md)
- Styling rated and unrated items (RatedItemStyle, UnratedItemStyle)
- Controlling item size (ItemSize property)
- Changing orientation (horizontal or vertical)
- Read-only mode for display purposes (IsReadOnly)
- Clearing ratings functionality (IsClearEnabled)
- Showing placeholder values (PlaceholderValue)
- Combining multiple customization options
- Complete real-world styling examples

### Templates and Custom Visuals
📄 **Read:** [references/templates.md](references/templates.md)
- ItemTemplateSelector overview
- Creating path-based templates (hearts, custom shapes)
- Implementing image-based templates (emoji ratings)
- Using font icons as rating items
- Building custom DataTemplateSelector classes
- Managing selected vs unselected states
- Complete emoji rating implementation
- Complete heart rating implementation

### Tooltip Features
📄 **Read:** [references/tooltip-features.md](references/tooltip-features.md)
- Enabling tooltips on hover (EnableToolTip property)
- Formatting tooltip content (ToolTipFormat property)
- Using standard numeric format strings
- Creating custom format patterns
- Enhancing user feedback with tooltips
- Accessibility benefits of tooltips
- Theme-adaptive tooltip styling

## Quick Start Example

### Basic 5-Star Rating

**XAML:**
```xml
<Page
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:syncfusion="using:Syncfusion.UI.Xaml.Editors">
    
    <Grid>
        <syncfusion:SfRating Value="3" ItemsCount="5"/>
    </Grid>
</Page>
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Editors;

// Create rating control
SfRating rating = new SfRating();
rating.Value = 3;
rating.ItemsCount = 5;
```

## Common Patterns

### 1. Standard 5-Star Rating

```xml
<syncfusion:SfRating Value="4" ItemsCount="5"/>
```

### 2. Half-Star Rating System

```xml
<syncfusion:SfRating 
    Value="3.5" 
    ItemsCount="5" 
    Precision="Half"/>
```

### 3. Read-Only Rating Display

```xml
<StackPanel>
    <TextBlock Text="Average Rating:"/>
    <syncfusion:SfRating 
        Value="4.2" 
        ItemsCount="5" 
        Precision="Exact"
        IsReadOnly="True"/>
</StackPanel>
```

### 4. Rating with Tooltip

```xml
<syncfusion:SfRating 
    Value="3" 
    ItemsCount="5"
    EnableToolTip="True"
    ToolTipFormat="0.0"/>
```

### 5. Larger Rating Items

```xml
<syncfusion:SfRating 
    Value="4" 
    ItemsCount="5"
    ItemSize="40"/>
```

### 6. Vertical Rating

```xml
<syncfusion:SfRating 
    Value="3" 
    ItemsCount="5"
    Orientation="Vertical"/>
```

### 7. Rating with Placeholder

```xml
<syncfusion:SfRating 
    ItemsCount="5"
    PlaceholderValue="3.5"/>
```

### 8. Clearable Rating

```xml
<syncfusion:SfRating 
    Value="4" 
    ItemsCount="5"
    IsClearEnabled="True"/>
```

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Value` | double | 0 | Current rating value |
| `ItemsCount` | int | 5 | Number of rating items to display |
| `Precision` | RatingPrecision | Full | Rating accuracy (Full/Half/Exact) |
| `ItemSize` | double | 24 | Size of each rating item |
| `Orientation` | Orientation | Horizontal | Layout direction (Horizontal/Vertical) |
| `IsReadOnly` | bool | false | Prevents user interaction |
| `IsClearEnabled` | bool | true | Allows clearing the rating |
| `PlaceholderValue` | double | 0 | Initial display value before user rating |
| `EnableToolTip` | bool | false | Show value on hover |
| `ToolTipFormat` | string | null | Format string for tooltip content |
| `RatedItemStyle` | Style | null | Style for filled/selected items |
| `UnratedItemStyle` | Style | null | Style for empty/unselected items |
| `ItemTemplateSelector` | DataTemplateSelector | null | Custom visual templates |

### Property Usage Tips

**Value vs PlaceholderValue:**
- `Value`: User's actual rating
- `PlaceholderValue`: Shows average/suggested rating before user interaction

**Precision Modes:**
- **Full**: Reviews, simple ratings (1, 2, 3, 4, 5)
- **Half**: Product ratings, more granular feedback (3.5, 4.0, 4.5)
- **Exact**: Analytics displays, precise averages (4.23, 3.87)

**IsReadOnly:**
- Use `true` for displaying ratings (product listings, reviews summary)
- Use `false` for collecting ratings (review forms, feedback)

**IsClearEnabled:**
- `true`: User can remove their rating by clicking first star again
- `false`: Once set, rating cannot be cleared (only changed)

## Common Use Cases

### Product Review System

```xml
<StackPanel>
    <TextBlock Text="Rate this product:" FontWeight="Bold"/>
    <syncfusion:SfRating 
        x:Name="ProductRating"
        Value="0" 
        ItemsCount="5"
        Precision="Half"
        EnableToolTip="True"
        ToolTipFormat="0.0"
        ValueChanged="ProductRating_ValueChanged"/>
</StackPanel>
```

```csharp
private void ProductRating_ValueChanged(object sender, ValueChangedEventArgs e)
{
    // Save rating to database
    SaveProductRating(e.NewValue);
}
```

### Average Rating Display

```xml
<Grid>
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="Auto"/>
        <ColumnDefinition Width="Auto"/>
    </Grid.ColumnDefinitions>
    
    <syncfusion:SfRating 
        Grid.Column="0"
        Value="{Binding AverageRating}" 
        ItemsCount="5"
        Precision="Exact"
        IsReadOnly="True"
        ItemSize="20"/>
    
    <TextBlock 
        Grid.Column="1"
        Text="{Binding AverageRating, StringFormat='({0:0.0})'}"
        VerticalAlignment="Center"
        Margin="10,0,0,0"/>
</Grid>
```

### Satisfaction Survey

```xml
<StackPanel Spacing="15">
    <TextBlock Text="How satisfied are you with our service?"/>
    <syncfusion:SfRating 
        Value="3" 
        ItemsCount="5"
        ItemSize="50"
        EnableToolTip="True"/>
</StackPanel>
```

### Movie Rating Interface

```xml
<StackPanel>
    <TextBlock Text="Rate this movie:" FontSize="16"/>
    <syncfusion:SfRating 
        Value="0" 
        ItemsCount="5"
        Precision="Half"
        ItemSize="35"
        EnableToolTip="True"
        ToolTipFormat="0.0 stars"/>
</StackPanel>
```

## Best Practices

### User Experience
- **Precision selection**: Use Full for simple ratings, Half for products, Exact for display only
- **Clear feedback**: Enable tooltips to show exact values
- **Appropriate sizing**: Use 24-32px for standard forms, 40-50px for prominent ratings
- **Placeholder values**: Show average ratings to guide user expectations
- **Allow clearing**: Enable `IsClearEnabled` unless rating is mandatory

### Visual Design
- **Consistent styling**: Use the same style across your application
- **Adequate spacing**: Ensure items don't overlap or feel cramped
- **Theme adaptation**: Test in both light and dark themes
- **Color contrast**: Ensure filled items are clearly distinguishable from empty
- **Custom templates**: Use recognizable icons (stars, hearts, thumbs)

### Accessibility
- **Enable tooltips**: Helps all users understand exact values
- **Keyboard support**: Rating control supports arrow key navigation
- **Read-only indication**: Make it clear when ratings are display-only
- **Label association**: Always include descriptive text labels
- **Screen readers**: Control announces current value and range

### Performance
- **ItemsCount**: Use 5 for standard ratings, 10 maximum for performance
- **Templates**: Simple templates perform better than complex images
- **Data binding**: Bind to ViewModel properties for reactive updates

### Common Mistakes to Avoid
- ❌ Using Exact precision with user input (difficult to control precisely)
- ❌ Forgetting to set `IsReadOnly="True"` for display ratings
- ❌ Not providing labels or context for the rating
- ❌ Using too many items (>10 becomes hard to use)
- ❌ Omitting tooltips on Half/Exact precision ratings
- ❌ Not importing Syncfusion.UI.Xaml.Editors namespace

## Troubleshooting

**Rating value not updating:**
- Verify `IsReadOnly` is `false`
- Check if `Value` is bound correctly (TwoWay binding)
- Ensure ValueChanged event is hooked up

**Stars not displaying:**
- Confirm NuGet package is installed
- Verify namespace import: `xmlns:syncfusion="using:Syncfusion.UI.Xaml.Editors"`
- Check if Syncfusion license is registered

**Half-star not showing:**
- Set `Precision="Half"`
- Ensure Value uses .5 increments (3.5, 4.0, 4.5)

**Custom template not appearing:**
- Verify DataTemplateSelector is properly implemented
- Check if templates are defined in Resources
- Ensure ItemTemplateSelector property is set

**Tooltip not visible:**
- Set `EnableToolTip="True"`
- Check if mouse hover is triggering (test with different elements)

## Events

**ValueChanged:**
```csharp
private void Rating_ValueChanged(object sender, ValueChangedEventArgs e)
{
    double oldValue = e.OldValue;
    double newValue = e.NewValue;
    
    // Handle rating change
    Debug.WriteLine($"Rating changed from {oldValue} to {newValue}");
}
```

## Related Components

- **Slider** - Alternative numeric input for continuous values
- **ComboBox** - Alternative for discrete choices
- **CheckBox** - For binary feedback (like/dislike)
- **TextBox** - For detailed written reviews

---

**Need more details?** Read the reference files linked in the Navigation Guide above for comprehensive documentation and examples.
