---
name: syncfusion-winui-segmented-control
description: Guide for implementing the Syncfusion WinUI Segmented Control for creating mutually exclusive option selectors. Use this skill when implementing segmented controls, segment pickers, tab selectors, or mutually exclusive option selectors in WinUI applications. Essential for segment-based navigation, filter toggles, view switchers, button groups with single selection, or any scenario requiring mutually exclusive selection from 2+ options in WinUI.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI Segmented Control

## When to Use This Skill

Use this skill when the user needs to:
- Create a segmented control or segment picker UI
- Implement mutually exclusive option selection
- Build tab-like navigation without full TabControl
- Create filter bars or view mode switchers
- Display 2+ linear options where only one can be selected
- Add animated selection transitions (slide effect)
- Create custom segment styles (ellipse, circle, top indicator)
- Implement keyboard navigation for segment selection
- Disable specific segments conditionally
- Support both light and dark themes

**Always apply this skill when the user mentions:** segmented control, segment picker, option selector, filter bar, view switcher, tab selector, mutually exclusive buttons, or segment-based navigation in WinUI applications.

## Component Overview

**SfSegmentedControl** is a Syncfusion WinUI control that provides a simple way to choose from a linear set of two or more segments, each functioning as a mutually exclusive option. It offers a clean alternative to radio buttons or tabs with built-in slide animation, custom styling, and theme support.

**Namespace:** `Syncfusion.UI.Xaml.Editors`  
**NuGet Package:** `Syncfusion.Editors.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+, Windows App SDK 1.0+)

**Key Advantage:** Provides a modern, iOS-style segmented picker with slide animation, shadow effects, and extensive customization—ideal for compact option selection without complex UI.

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup (Syncfusion.Editors.WinUI)
- Namespace imports (Syncfusion.UI.Xaml.Editors)
- Basic SfSegmentedControl initialization
- Populating with string collections (inline x:String items)
- Populating with business objects (ItemsSource, DisplayMemberPath)
- ItemTemplate for custom UI (icons, images, text)
- First complete example with ViewModel
- License registration

### Selection Features
📄 **Read:** [references/selection.md](references/selection.md)
- SelectedIndex property for programmatic selection
- SelectedSegmentStyle customization
- Shadow effects on selected items (HasShadow, ShadowColor)
- Selection animations (Slide vs None)
- SelectionAnimationType property
- Keyboard navigation (Arrow keys, Tab, Enter)
- SelectionChanged event with NewValue and OldValue
- Handling selection programmatically

### Disabling Items
📄 **Read:** [references/disable-items.md](references/disable-items.md)
- SetItemEnabled method for conditional disabling
- Disabling segments by index
- Visual appearance of disabled items
- Preventing user interaction with specific segments
- Common patterns (form validation, conditional availability)

### UI Customization
📄 **Read:** [references/ui-customization.md](references/ui-customization.md)
- BorderThickness and ItemBorderThickness
- CornerRadius customization for control and items
- BorderBrush color customization
- ItemContainerStyle for per-item styling
- ItemTemplateSelector for conditional templates
- ItemContainerStyleSelector for conditional styles
- Custom templates (ellipse, circle, image+text, top indicator)
- Advanced styling patterns

### Theme Support
📄 **Read:** [references/themes.md](references/themes.md)
- RequestedTheme in App.xaml (Dark/Light)
- Theme-aware customization using keys
- 12 theme resource keys for complete control
- SyncfusionSegmentedControl* theme keys
- Light and Dark theme examples
- ResourceDictionary.ThemeDictionaries structure

## Quick Start Example

### Basic Segmented Control with Strings

```xaml
<Window xmlns:syncfusion="using:Syncfusion.UI.Xaml.Editors">
    <Grid>
        <syncfusion:SfSegmentedControl 
            x:Name="segmentedControl"
            HorizontalAlignment="Center"
            VerticalAlignment="Center"
            SelectedIndex="0">
            <x:String>Day</x:String>
            <x:String>Week</x:String>
            <x:String>Month</x:String>
            <x:String>Year</x:String>
        </syncfusion:SfSegmentedControl>
    </Grid>
</Window>
```

### With Business Objects and ViewModel

```csharp
// ViewModel
public class SegmentedViewModel
{
    public ObservableCollection<PeriodModel> Periods { get; set; }
    
    public SegmentedViewModel()
    {
        Periods = new ObservableCollection<PeriodModel>
        {
            new PeriodModel { Name = "Day" },
            new PeriodModel { Name = "Week" },
            new PeriodModel { Name = "Month" },
            new PeriodModel { Name = "Year" }
        };
    }
}

public class PeriodModel
{
    public string Name { get; set; }
}
```

```xaml
<syncfusion:SfSegmentedControl 
    ItemsSource="{Binding Periods}"
    DisplayMemberPath="Name"
    SelectedIndex="2"/>
```

## Common Patterns

### 1. View Mode Switcher
```xaml
<syncfusion:SfSegmentedControl SelectedIndex="0" SelectionChanged="ViewMode_Changed">
    <x:String>List</x:String>
    <x:String>Grid</x:String>
    <x:String>Timeline</x:String>
</syncfusion:SfSegmentedControl>
```

```csharp
private void ViewMode_Changed(object sender, SegmentSelectionChangedEventArgs e)
{
    string selectedMode = e.NewValue as string;
    UpdateViewMode(selectedMode);
}
```

**When to use:** Switching between different display modes or layouts.

### 2. Filter Bar with Selection
```xaml
<syncfusion:SfSegmentedControl 
    ItemsSource="{Binding FilterOptions}"
    DisplayMemberPath="Label"
    SelectedIndex="{Binding SelectedFilterIndex, Mode=TwoWay}"/>
```

**When to use:** Filtering data by category with visible selection state.

### 3. Custom Icon Segments with ItemTemplate
```xaml
<syncfusion:SfSegmentedControl ItemsSource="{Binding Items}">
    <syncfusion:SfSegmentedControl.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal">
                <Path Data="{Binding Icon}" Fill="{Binding IconColor}" Width="16" Height="16"/>
                <TextBlock Text="{Binding Name}" Margin="6,0,0,0"/>
            </StackPanel>
        </DataTemplate>
    </syncfusion:SfSegmentedControl.ItemTemplate>
</syncfusion:SfSegmentedControl>
```

**When to use:** Segments with icons or images for better visual recognition.

### 4. Disabled Segments for Unavailable Options
```csharp
segmentedControl.SetItemEnabled(2, false); // Disable "Premium" option
segmentedControl.SetItemEnabled(3, false); // Disable "Enterprise" option
```

**When to use:** Conditionally disabling options based on user permissions or app state.

### 5. Custom Selection Style with Shadow
```xaml
<syncfusion:SfSegmentedControl SelectedIndex="1">
    <syncfusion:SfSegmentedControl.SelectedSegmentStyle>
        <Style TargetType="syncfusion:SelectedSegmentBorder">
            <Setter Property="Background" Value="#6C58EA"/>
            <Setter Property="HasShadow" Value="True"/>
            <Setter Property="ShadowColor" Value="#6C58EA"/>
            <Setter Property="CornerRadius" Value="8"/>
        </Style>
    </syncfusion:SfSegmentedControl.SelectedSegmentStyle>
</syncfusion:SfSegmentedControl>
```

**When to use:** Adding visual depth and modern appearance to selected segments.

### 6. No Animation for Instant Selection
```xaml
<syncfusion:SfSegmentedControl 
    SelectionAnimationType="None"
    SelectedIndex="0">
    <x:String>Option 1</x:String>
    <x:String>Option 2</x:String>
    <x:String>Option 3</x:String>
</syncfusion:SfSegmentedControl>
```

**When to use:** When slide animation feels too slow or distracting for rapid selections.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `ItemsSource` | IEnumerable | null | Collection of items to display as segments. |
| `DisplayMemberPath` | string | null | Property path to display from business objects. |
| `ItemTemplate` | DataTemplate | null | Custom template for rendering each segment item. |
| `SelectedIndex` | int | 0 | Index of the currently selected segment (0-based). |
| `SelectedItem` | object | null | Currently selected item from ItemsSource. |
| `SelectionAnimationType` | SegmentSelectionAnimationType | Slide | Animation type (Slide or None) for selection transitions. |
| `SelectedSegmentStyle` | Style | Default | Style for the selected segment border (SelectedSegmentBorder target). |
| `ItemContainerStyle` | Style | Default | Style for each SfSegmentedItem container. |
| `ItemTemplateSelector` | DataTemplateSelector | null | Selector for conditional item templates. |
| `ItemContainerStyleSelector` | StyleSelector | null | Selector for conditional item styles. |
| `BorderThickness` | Thickness | 1 | Border thickness of the control. |
| `ItemBorderThickness` | Thickness | 0,0,1,0 | Border thickness between segment items. |
| `CornerRadius` | CornerRadius | 0 | Corner radius of the control. |
| `BorderBrush` | Brush | Default | Border color of the control. |

## Key Events

| Event | Description |
|-------|-------------|
| `SelectionChanged` | Fired when selection changes. Provides NewValue and OldValue in SegmentSelectionChangedEventArgs. |

## Key Methods

| Method | Description |
|--------|-------------|
| `SetItemEnabled(int index, bool isEnabled)` | Enables or disables a segment item at the specified index. |

## Common Use Cases

### View Switchers
- List/Grid/Timeline view toggles
- Calendar view modes (Day/Week/Month/Year)
- Map view types (Standard/Satellite/Hybrid)
- Chart types (Line/Bar/Pie)

**Best Approach:** Use string items or DisplayMemberPath with SelectionChanged event handler.

### Filter Bars
- Status filters (All/Active/Completed/Archived)
- Priority filters (Low/Medium/High/Critical)
- Category filters (Documents/Images/Videos/Audio)
- Time period filters (Today/Week/Month/Year)

**Best Approach:** Bind to ObservableCollection, use SelectedIndex with two-way binding.

### Settings Toggles
- Privacy levels (Public/Friends/Private)
- Notification preferences (All/Important/None)
- Language selection (English/Spanish/French)
- Theme selection (Auto/Light/Dark)

**Best Approach:** Use SelectionChanged to update app settings immediately.

### Tab-like Navigation
- Compact section navigation (Info/Details/Reviews)
- Form step indicators (Personal/Address/Payment)
- Profile tabs (Posts/About/Photos)

**Best Approach:** Use with custom ItemTemplate for icons, disable animation for instant switching.

### Dashboard Controls
- Date range selectors (1D/1W/1M/3M/1Y)
- Data source toggles (Local/Cloud/All)
- Report type selectors
- Comparison mode toggles

**Best Approach:** Enable shadow effects, use custom colors matching dashboard theme.

## Implementation Tips

1. **Item Count:** Best for 2-7 segments. More items may require scrolling or alternative control.

2. **Selection Handling:** Use SelectionChanged event for immediate reactions. Bind SelectedIndex for MVVM.

3. **Disabled Items:** Use SetItemEnabled() after ItemsSource is set. Call in Loaded event if binding to ViewModel.

4. **Custom Styling:** Set ItemContainerStyle for uniform spacing. Use SelectedSegmentStyle for selection appearance.

5. **Animation:** Slide animation (default) provides smooth transitions. Use None for instant selection in forms.

6. **Keyboard Support:** Arrow keys navigate, Enter selects. Ensure TabIndex is set for proper focus flow.

7. **Theme Support:** Use theme keys in Resources for consistent Light/Dark theme appearance.

8. **ItemTemplate:** Use for icons, images, or complex layouts. Keep templates simple for performance.

9. **Border Customization:** Set ItemBorderThickness="0" for seamless segments. Use BorderThickness for outer border.

10. **CornerRadius:** Match control and item CornerRadius for consistent rounded appearance.

## Related Documentation

- **Getting Started:** See [references/getting-started.md](references/getting-started.md) for setup and basic usage
- **Selection:** See [references/selection.md](references/selection.md) for selection features and events
- **Disable Items:** See [references/disable-items.md](references/disable-items.md) for conditional segment disabling
- **UI Customization:** See [references/ui-customization.md](references/ui-customization.md) for styling and templates
- **Themes:** See [references/themes.md](references/themes.md) for theme support and customization keys
