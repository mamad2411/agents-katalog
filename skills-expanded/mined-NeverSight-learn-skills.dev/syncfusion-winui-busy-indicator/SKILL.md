---
name: syncfusion-winui-busy-indicator
description: Guide for implementing the Syncfusion WinUI BusyIndicator control to display loading indicators and progress status. Use this skill when implementing loading indicators, showing progress status, indicating background operations, or creating waiting screens in WinUI applications. Essential for async data loading, file operations, API calls, and any scenario requiring user notification during processing tasks.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI BusyIndicator

## When to Use This Skill

Use this skill when the user needs to:
- Display a loading indicator during background operations
- Show busy/waiting status to users during async tasks
- Indicate progress for data loading, file operations, or API calls
- Create modal or inline loading animations
- Provide visual feedback during lengthy operations
- Implement any scenario requiring "please wait" indicators

**Always apply this skill when the user mentions:** loading indicators, busy indicators, progress animations, waiting screens, async operation feedback, or background task notifications in WinUI applications.

## Component Overview

**SfBusyIndicator** is a Syncfusion WinUI control that displays predefined animated indicators to show busy/loading status. It provides 8 built-in animation types and extensive customization options for size, color, duration, and content.

**Namespace:** `Syncfusion.UI.Xaml.Notifications`  
**NuGet Package:** `Syncfusion.Notifications.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+, Windows App SDK 1.0+)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Namespace imports and basic initialization
- IsActive property for controlling visibility
- License registration requirements
- First complete example

### Animation Types
📄 **Read:** [references/animation-types.md](references/animation-types.md)
- 8 built-in animation types (DottedCircularFluent, DottedCircle, DottedLinear, etc.)
- AnimationType property usage
- Visual examples and comparisons
- Choosing the right animation for your UI
- Default animation (DottedCircularFluent)

### Content and Positioning
📄 **Read:** [references/content.md](references/content.md)
- BusyContent property for custom messages
- BusyContentPosition (Top, Bottom, Left, Right)
- BusyContentTemplate for advanced customization
- Custom DataTemplate examples
- Content display best practices

### Customization Options
📄 **Read:** [references/customization.md](references/customization.md)
- SizeFactor property (adjusting indicator size)
- DurationFactor property (animation speed control)
- Color property (indicator color customization)
- Combining customization properties
- Performance considerations

## Quick Start Example

```xaml
<Page
    xmlns:notification="using:Syncfusion.UI.Xaml.Notifications">
    <Grid>
        <notification:SfBusyIndicator 
            x:Name="busyIndicator"
            IsActive="True"
            AnimationType="DottedCircularFluent"
            BusyContent="Loading..."
            BusyContentPosition="Bottom"
            Color="DodgerBlue"
            SizeFactor="0.5"/>
    </Grid>
</Page>
```

```csharp
using Syncfusion.UI.Xaml.Notifications;

// Create and configure BusyIndicator
SfBusyIndicator busyIndicator = new SfBusyIndicator
{
    IsActive = true,
    AnimationType = BusyIndicatorAnimationType.DottedCircularFluent,
    BusyContent = "Loading...",
    BusyContentPosition = BusyIndicatorContentPosition.Bottom,
    Color = new SolidColorBrush(Colors.DodgerBlue),
    SizeFactor = 0.5
};

// Add to UI
this.Content = busyIndicator;
```

## Common Patterns

### 1. Simple Loading Indicator
```xaml
<notification:SfBusyIndicator 
    IsActive="True"
    BusyContent="Loading..."/>
```

**When to use:** Basic loading feedback without customization.

### 2. Async Data Loading with Code-Behind
```xaml
<Grid>
    <notification:SfBusyIndicator 
        x:Name="busyIndicator"
        IsActive="{x:Bind ViewModel.IsLoading, Mode=OneWay}"
        AnimationType="DottedCircle"
        BusyContent="Loading data..."/>
</Grid>
```

```csharp
private async void LoadDataAsync()
{
    busyIndicator.IsActive = true;
    
    try
    {
        await FetchDataFromApiAsync();
    }
    finally
    {
        busyIndicator.IsActive = false;
    }
}
```

**When to use:** Control busy state programmatically during async operations.

### 3. Custom Animation with Content
```xaml
<notification:SfBusyIndicator 
    IsActive="True"
    AnimationType="LinearFluent"
    BusyContent="Please wait..."
    BusyContentPosition="Top"
    Color="OrangeRed"
    SizeFactor="0.7"/>
```

**When to use:** Need specific animation style with custom positioning and colors.

### 4. Modal Overlay Loading Screen
```xaml
<Grid>
    <!-- Main content -->
    <StackPanel>
        <TextBlock Text="Application Content"/>
        <!-- Other UI elements -->
    </StackPanel>
    
    <!-- Overlay BusyIndicator -->
    <Grid x:Name="loadingOverlay" 
          Background="#80000000"
          Visibility="{x:Bind IsProcessing, Mode=OneWay}">
        <notification:SfBusyIndicator 
            IsActive="True"
            AnimationType="DoubleCircle"
            BusyContent="Processing..."
            Color="White"/>
    </Grid>
</Grid>
```

**When to use:** Block UI interaction during critical operations.

### 5. Custom Content Template
```xaml
<notification:SfBusyIndicator IsActive="True" AnimationType="DottedCircle">
    <notification:SfBusyIndicator.BusyContentTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Spacing="10">
                <TextBlock Text="⏳" FontSize="24"/>
                <TextBlock Text="Loading data..." 
                          FontSize="16" 
                          FontWeight="SemiBold"/>
            </StackPanel>
        </DataTemplate>
    </notification:SfBusyIndicator.BusyContentTemplate>
</notification:SfBusyIndicator>
```

**When to use:** Need rich content beyond simple text messages.

### 6. Slow Animation for Subtle Feedback
```xaml
<notification:SfBusyIndicator 
    IsActive="True"
    AnimationType="SingleCircle"
    DurationFactor="0.9"
    SizeFactor="0.3"
    Color="Gray"/>
```

**When to use:** Provide subtle background activity indication without distracting users.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `IsActive` | bool | false | Controls whether the indicator is visible and animating. Set to `true` to show, `false` to hide. |
| `AnimationType` | BusyIndicatorAnimationType | DottedCircularFluent | The animation style. Options: DottedCircularFluent, DottedCircle, DottedLinear, DoubleCircle, LinearBox, LinearFluent, LinearOscillatingBox, SingleCircle. |
| `BusyContent` | object | null | The content displayed below/above/beside the indicator (typically a message). |
| `BusyContentPosition` | BusyIndicatorContentPosition | Bottom | Position of content relative to indicator. Options: Top, Bottom, Left, Right. |
| `BusyContentTemplate` | DataTemplate | null | Custom template for the busy content. Allows rich content beyond simple text. |
| `SizeFactor` | double | 0.5 | Controls the size of the indicator. Range: 0.0 to 1.0. Higher values = larger indicator. |
| `DurationFactor` | double | 0.5 | Controls animation speed. Range: 0.0 to 1.0. Higher values = slower animation. |
| `Color` | Brush | System accent color | The color of the animated indicator elements. |

## Common Use Cases

### Data Loading Scenarios
- Fetching data from REST APIs or databases
- Loading large datasets into grids or lists
- Refreshing dashboard content
- Initializing application data on startup

**Best Animation:** DottedCircularFluent, DottedCircle

### File Operations
- Uploading/downloading files
- Reading/writing large files
- Importing/exporting data
- Processing documents

**Best Animation:** LinearFluent, LinearBox

### Long-Running Calculations
- Complex data analysis
- Report generation
- Image processing
- Search operations

**Best Animation:** DoubleCircle, SingleCircle

### Background Tasks
- Synchronization operations
- Cache updates
- Background service communication
- Scheduled tasks

**Best Animation:** LinearOscillatingBox, DottedLinear (subtle)

## Implementation Tips

1. **Binding IsActive:** Use data binding to ViewModel boolean properties for clean MVVM patterns.

2. **Overlay Pattern:** For modal loading, use a Grid with semi-transparent background containing the BusyIndicator.

3. **Performance:** BusyIndicator animations are GPU-accelerated. No performance concerns for multiple instances.

4. **Accessibility:** The control automatically handles accessibility features. Custom content should include proper accessibility properties.

5. **Threading:** Always activate/deactivate BusyIndicator on the UI thread. Use `DispatcherQueue` if updating from background threads.

6. **User Experience:** 
   - Show BusyIndicator immediately for operations expected to take >500ms
   - Always hide when operation completes (use try-finally blocks)
   - Position content appropriately for the UI context
   - Choose animation types that match your app's design language

## Related Documentation

- **Animation Types:** See [references/animation-types.md](references/animation-types.md) for detailed comparison of all 8 animation styles
- **Content Customization:** See [references/content.md](references/content.md) for template examples and positioning strategies
- **Customization:** See [references/customization.md](references/customization.md) for size, speed, and color options
