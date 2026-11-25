---
name: syncfusion-winui-shimmer
description: Guide for implementing the Syncfusion WinUI Shimmer control to display loading placeholders and skeleton screens. Use this skill when implementing shimmer effects, skeleton screens, content loading animations, or loading placeholders during data fetching in WinUI applications. Essential for enhancing perceived performance during async operations, list loading, profile loading, article loading, or any content loading scenario requiring visual feedback.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI Shimmer

## When to Use This Skill

Use this skill when the user needs to:
- Display skeleton screens during content loading
- Show shimmer effects as loading placeholders
- Enhance perceived performance during data fetching
- Create loading animations for lists, profiles, articles, or videos
- Provide visual feedback during async content loading
- Implement modern loading UX patterns (skeleton loaders)

**Always apply this skill when the user mentions:** shimmer effects, skeleton screens, loading placeholders, content loading animations, shimmer loaders, or skeleton UI in WinUI applications.

## Component Overview

**SfShimmer** is a Syncfusion WinUI control that displays animated placeholder content (skeleton screens) during loading operations. It provides 7 built-in shimmer types and supports custom layouts to match any content structure.

**Namespace:** `Syncfusion.UI.Xaml.Core`  
**NuGet Package:** `Syncfusion.Core.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+, Windows App SDK 1.0+)

**Key Advantage:** Improves perceived performance by showing content structure while data loads, reducing user frustration during wait times.

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Namespace imports and basic initialization
- Default shimmer type (CirclePersona)
- License registration requirements
- First complete example

### Built-in Shimmer Types
📄 **Read:** [references/built-in-types.md](references/built-in-types.md)
- 7 built-in shimmer types (CirclePersona, SquarePersona, Profile, Article, Video, Feed, Shopping)
- Type property usage
- Visual descriptions and comparisons
- Choosing the right type for your content
- Switching between types

### Custom Layouts
📄 **Read:** [references/custom-layouts.md](references/custom-layouts.md)
- CustomLayout property for creating custom shimmer designs
- Using Grid, StackPanel, Rectangle elements
- Complex layout examples
- Matching shimmer to actual content structure
- Best practices and performance

### Customization Options
📄 **Read:** [references/customization.md](references/customization.md)
- Fill property (background color)
- WaveColor property (animation color)
- WaveWidth property (wave width control)
- WaveDuration property (animation speed)
- RepeatCount property (repeat views)
- Combining customizations

## Quick Start Example

```xaml
<Page
    xmlns:syncfusion="using:Syncfusion.UI.Xaml.Core">
    <Grid>
        <syncfusion:SfShimmer 
            x:Name="shimmer"
            Type="Article"
            Fill="#F6F6F6"
            WaveColor="#E0E0E0"
            RepeatCount="3"/>
    </Grid>
</Page>
```

```csharp
using Syncfusion.UI.Xaml.Core;
using Microsoft.UI;

// Create and configure Shimmer
SfShimmer shimmer = new SfShimmer
{
    Type = ShimmerType.Article,
    Fill = Colors.LightGray,
    WaveColor = Colors.White,
    RepeatCount = 3
};

// Add to UI
this.Content = shimmer;
```

## Common Patterns

### 1. Simple Profile Loading Shimmer
```xaml
<syncfusion:SfShimmer Type="Profile"/>
```

**When to use:** User profile pages, account screens, contact details loading.

### 2. Article/Blog Loading with Repeat
```xaml
<Grid>
    <syncfusion:SfShimmer 
        Type="Article"
        RepeatCount="5"
        Fill="#F5F5F5"
        WaveColor="#E0E0E0"/>
</Grid>
```

**When to use:** Blog feeds, news articles, text-heavy content loading.

### 3. Shopping/Product Grid Shimmer
```xaml
<syncfusion:SfShimmer 
    Type="Shopping"
    RepeatCount="6"
    WaveDuration="1500"/>
```

**When to use:** E-commerce product grids, shopping catalogs, item galleries.

### 4. Video/Media Feed Shimmer
```xaml
<syncfusion:SfShimmer 
    Type="Video"
    RepeatCount="4"
    Fill="#000000"
    WaveColor="#333333"/>
```

**When to use:** Video streaming apps, media galleries, YouTube-like feeds.

### 5. Conditional Shimmer Display
```xaml
<Grid>
    <!-- Shimmer while loading -->
    <syncfusion:SfShimmer 
        x:Name="shimmer"
        Type="Feed"
        Visibility="{x:Bind IsLoading, Mode=OneWay}"/>
    
    <!-- Actual content when loaded -->
    <ListView 
        x:Name="contentListView"
        Visibility="{x:Bind IsLoaded, Mode=OneWay}"
        ItemsSource="{x:Bind Items}"/>
</Grid>
```

```csharp
private bool isLoading = true;
public bool IsLoading
{
    get => isLoading;
    set
    {
        isLoading = value;
        OnPropertyChanged();
    }
}

public bool IsLoaded => !IsLoading;

private async void LoadContentAsync()
{
    IsLoading = true;
    
    try
    {
        var data = await FetchDataAsync();
        contentListView.ItemsSource = data;
    }
    finally
    {
        IsLoading = false;
    }
}
```

**When to use:** Toggle between shimmer and actual content based on loading state.

### 6. Custom Layout for Specific UI
```xaml
<syncfusion:SfShimmer>
    <syncfusion:SfShimmer.CustomLayout>
        <Grid RowSpacing="10" ColumnSpacing="15">
            <Grid.RowDefinitions>
                <RowDefinition Height="60"/>
                <RowDefinition Height="Auto"/>
                <RowDefinition Height="Auto"/>
            </Grid.RowDefinitions>
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="60"/>
                <ColumnDefinition Width="*"/>
            </Grid.ColumnDefinitions>
            
            <!-- Profile image placeholder -->
            <Ellipse Grid.Row="0" Grid.RowSpan="2" Width="60" Height="60"/>
            
            <!-- Name placeholder -->
            <Rectangle Grid.Row="0" Grid.Column="1" 
                      Height="15" RadiusX="3" RadiusY="3"
                      HorizontalAlignment="Left" Width="200"/>
            
            <!-- Description placeholder -->
            <Rectangle Grid.Row="1" Grid.Column="1" 
                      Height="12" RadiusX="3" RadiusY="3"
                      HorizontalAlignment="Left" Width="250"/>
            
            <!-- Content placeholder -->
            <Rectangle Grid.Row="2" Grid.ColumnSpan="2" 
                      Height="100" RadiusX="5" RadiusY="5"/>
        </Grid>
    </syncfusion:SfShimmer.CustomLayout>
</syncfusion:SfShimmer>
```

**When to use:** Custom content structure not matching built-in types.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Type` | ShimmerType | CirclePersona | The built-in shimmer layout type. Options: CirclePersona, SquarePersona, Profile, Article, Video, Feed, Shopping. |
| `CustomLayout` | UIElement | null | Custom layout for creating shimmer designs that match your specific content structure. |
| `Fill` | Brush | #F6F6F6 | Background color of the shimmer view (placeholder color). |
| `WaveColor` | Brush | White | Color of the animated wave that moves across the shimmer. |
| `WaveWidth` | double | 200 | Width of the animated wave in pixels. Larger values = wider wave. |
| `WaveDuration` | int | 1000 | Duration of the wave animation in milliseconds. Higher values = slower animation. |
| `RepeatCount` | int | 1 | Number of times the built-in shimmer view is repeated vertically. Useful for lists. |

## Common Use Cases

### List/Feed Loading
- Social media feeds
- News article lists
- Product catalogs
- Comment sections
- Search results

**Best Types:** Feed, Article, Shopping

### Profile/User Loading
- User profiles
- Contact cards
- Account details
- Team member displays
- About sections

**Best Types:** Profile, CirclePersona, SquarePersona

### Media Loading
- Video thumbnails
- Image galleries
- Media players
- Streaming content
- Photo albums

**Best Types:** Video, Custom layout with image placeholders

### E-commerce
- Product grids
- Shopping carts
- Product details
- Category pages
- Wishlists

**Best Types:** Shopping, Custom layouts

## Implementation Tips

1. **Match Shimmer to Content:** Design shimmer layouts that closely resemble the actual content structure for seamless transitions.

2. **Use RepeatCount for Lists:** Set `RepeatCount` to match the expected number of items visible in the viewport.

3. **Timing:** 
   - Show shimmer immediately when loading starts
   - Hide shimmer when content is ready to display
   - Typical shimmer duration: 500ms - 3000ms

4. **Color Theming:**
   - Light theme: Fill = #F6F6F6, WaveColor = White
   - Dark theme: Fill = #2C2C2C, WaveColor = #3C3C3C

5. **Performance:** Shimmer animations are GPU-accelerated. Multiple shimmers can run simultaneously without performance issues.

6. **Accessibility:** Shimmer is purely visual. Ensure screen readers announce loading state separately using live regions or status messages.

7. **Wave Speed:**
   - Fast loading (<2s): WaveDuration = 800-1000ms
   - Normal loading (2-5s): WaveDuration = 1000-1500ms
   - Slow loading (>5s): WaveDuration = 1500-2000ms

8. **Custom Layouts:** Use Rectangle elements with rounded corners (RadiusX/RadiusY) and Ellipse for circular placeholders.

## Shimmer vs Other Loading Patterns

**Use Shimmer when:**
- Content structure is known beforehand
- Loading time is 500ms - 5 seconds
- Showing list-based or structured content
- Modern app with emphasis on perceived performance

**Use BusyIndicator when:**
- Content structure is unknown
- Generic loading indication needed
- Modal/blocking operations
- Very quick (<500ms) or very long (>10s) operations

**Use ProgressBar when:**
- Determinate progress can be shown
- File uploads/downloads
- Progress percentage is available
- Sequential operations with measurable progress

## Related Documentation

- **Built-in Types:** See [references/built-in-types.md](references/built-in-types.md) for detailed comparison of all 7 shimmer types
- **Custom Layouts:** See [references/custom-layouts.md](references/custom-layouts.md) for creating custom shimmer designs
- **Customization:** See [references/customization.md](references/customization.md) for appearance and animation options
