---
name: syncfusion-winui-badge
description: Guide implementation of the Syncfusion WinUI Badge control (SfBadge) for displaying notification badges and status indicators. Use this skill when working with badge notifications, unread count badges, BadgeContainer, or notification overlays in WinUI applications. Covers shapes, colors, positioning, alignment, animations, and customization patterns.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Badges in WinUI

The Syncfusion WinUI Badge control (`SfBadge`) displays notifications, counts, or status indicators overlaid on other UI elements. Use badges to show unread message counts, notification indicators, status changes, or any numeric/text overlay on buttons, icons, or controls.

## When to Use This Skill

Use this skill when you need to:
- Display notification counts on buttons, icons, or UI elements
- Show unread message indicators in messaging or email interfaces
- Add status badges to user avatars or profile pictures
- Create notification overlays on navigation items
- Implement count indicators for shopping carts or lists
- Show warning, error, or success states with badges
- Position badges at specific locations on controls
- Customize badge appearance (colors, shapes, animations)
- Work with the `SfBadge` or `BadgeContainer` components

## Component Overview

**Key Capabilities:**
- Multiple shapes (Oval, Rectangle, Ellipse, Custom)
- Predefined color states (Accent, Success, Warning, Error, Information)
- Flexible positioning and alignment
- Custom content and formatting
- Animation support (Scale, Opacity)
- Works with or without `BadgeContainer`
- Complete customization (colors, fonts, strokes, rotation)

**Basic Usage Pattern:**
```xaml
<notification:BadgeContainer>
    <notification:BadgeContainer.Content>
        <Button Content="Inbox"/>
    </notification:BadgeContainer.Content>
    <notification:BadgeContainer.Badge>
        <notification:SfBadge Content="10" Fill="Success"/>
    </notification:BadgeContainer.Badge>
</notification:BadgeContainer>
```

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When you need to:
- Install and set up the Badge component
- Create your first Badge implementation
- Add Badge to buttons or other controls
- Understand BadgeContainer usage
- Set basic badge content and properties
- Learn the component structure

### Shapes and Fill Styles
📄 **Read:** [references/shapes-and-fills.md](references/shapes-and-fills.md)

When you need to:
- Change badge shape (Oval, Rectangle, Ellipse)
- Use predefined fill colors (Success, Warning, Error, etc.)
- Understand badge color states
- Create custom shapes with `CustomShape` property
- Choose appropriate visual styles for different badge types

### Alignment and Positioning
📄 **Read:** [references/alignment-positioning.md](references/alignment-positioning.md)

When you need to:
- Align badge horizontally or vertically
- Position badge inside, outside, or centered on edges
- Place badge at custom positions (0-1 range)
- Use anchor positioning
- Adjust badge content alignment
- Control padding and spacing
- Handle auto re-positioning

### Customization Options
📄 **Read:** [references/customization.md](references/customization.md)

When you need to:
- Set custom background and foreground colors
- Create completely custom badge shapes
- Customize badge UI with ContentTemplate
- Add strokes and borders
- Change text formatting (font, size, style)
- Rotate badges
- Adjust opacity
- Control badge size
- Hide or show badges

### Features and Configuration
📄 **Read:** [references/features.md](references/features.md)

When you need to:
- Add animations (Scale or Opacity)
- Format badge content with converters
- Use Badge without BadgeContainer
- Implement badges in ListView or data templates
- Apply advanced content formatting
- Handle dynamic badge scenarios

## Quick Start

### 1. Install NuGet Package

```powershell
Install-Package Syncfusion.Notifications.WinUI
```

### 2. Import Namespace

```xaml
xmlns:notification="using:Syncfusion.UI.Xaml.Notifications"
```

### 3. Basic Badge Implementation

```xaml
<notification:BadgeContainer>
    <notification:BadgeContainer.Content>
        <Button Content="Notifications" Width="120" Height="40"/>
    </notification:BadgeContainer.Content>
    <notification:BadgeContainer.Badge>
        <notification:SfBadge Content="5" Fill="Error"/>
    </notification:BadgeContainer.Badge>
</notification:BadgeContainer>
```

## Common Patterns

### Pattern 1: Unread Message Count

```xaml
<notification:BadgeContainer>
    <notification:BadgeContainer.Content>
        <Button Content="Messages" FontSize="16"/>
    </notification:BadgeContainer.Content>
    <notification:BadgeContainer.Badge>
        <notification:SfBadge Content="{x:Bind UnreadCount, Mode=OneWay}"
                             Fill="Error"
                             Shape="Ellipse"/>
    </notification:BadgeContainer.Badge>
</notification:BadgeContainer>
```

### Pattern 2: Status Indicator

```xaml
<notification:BadgeContainer>
    <notification:BadgeContainer.Content>
        <PersonPicture Width="60" Height="60" ProfilePicture="/Assets/user.png"/>
    </notification:BadgeContainer.Content>
    <notification:BadgeContainer.Badge>
        <notification:SfBadge Shape="None"
                             HorizontalPosition="0.85"
                             VerticalPosition="0.85">
            <Ellipse Width="16" Height="16" Fill="LimeGreen"/>
        </notification:SfBadge>
    </notification:BadgeContainer.Badge>
</notification:BadgeContainer>
```

### Pattern 3: Success/Warning States

```xaml
<!-- Success Badge -->
<notification:SfBadge Content="Verified" 
                     Fill="Success" 
                     Shape="Rectangle"/>

<!-- Warning Badge -->
<notification:SfBadge Content="!" 
                     Fill="Warning" 
                     Shape="Ellipse"/>

<!-- Error Badge -->
<notification:SfBadge Content="Error" 
                     Fill="Error" 
                     Shape="Oval"/>
```

### Pattern 4: Custom Formatted Count

```csharp
// Converter to format large numbers
public class CountFormatConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, string language)
    {
        if (int.TryParse(value?.ToString(), out int count))
        {
            if (count <= 99) return count.ToString();
            if (count <= 999) return "99+";
            if (count < 99999) return (count / 1000).ToString("0.#") + "K";
            return (count / 1000000).ToString("0.#") + "M";
        }
        return value;
    }
    
    public object ConvertBack(object value, Type targetType, object parameter, string language)
    {
        throw new NotImplementedException();
    }
}
```

```xaml
<Page.Resources>
    <local:CountFormatConverter x:Key="countFormatter"/>
</Page.Resources>

<notification:SfBadge Content="{x:Bind Count, Mode=OneWay, Converter={StaticResource countFormatter}}"
                     Background="Red"
                     Foreground="White"/>
```

### Pattern 5: Badge in ListView

```xaml
<ListView ItemsSource="{x:Bind MailItems}">
    <ListView.ItemTemplate>
        <DataTemplate x:DataType="local:MailItem">
            <Grid>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="Auto"/>
                </Grid.ColumnDefinitions>
                
                <TextBlock Text="{x:Bind FolderName}" 
                          VerticalAlignment="Center"/>
                
                <notification:SfBadge Grid.Column="1"
                                     Content="{x:Bind UnreadCount}"
                                     Fill="Warning"
                                     Shape="Oval"
                                     Visibility="{x:Bind HasUnread}"/>
            </Grid>
        </DataTemplate>
    </ListView.ItemTemplate>
</ListView>
```

## Key Properties

### Content and Display
- **Content** - Text or number to display in badge
- **ContentTemplate** - Custom template for badge content
- **Visibility** - Show or hide badge (Visible/Collapsed)

### Shape and Style
- **Shape** - Badge shape: Oval, Rectangle, Ellipse, None, Custom
- **Fill** - Predefined color: Accent, Success, Warning, Error, Information, Alt, Default
- **CustomShape** - Geometry for custom badge shapes
- **Background/Foreground** - Custom colors

### Positioning (with BadgeContainer)
- **HorizontalAlignment** - Left, Center, Right (default: Right)
- **VerticalAlignment** - Top, Center, Bottom (default: Top)
- **HorizontalAnchor** - Inside, Center, Outside (default: Center)
- **VerticalAnchor** - Inside, Center, Outside (default: Center)
- **HorizontalPosition** - 0 to 1 for custom positioning (default: 1)
- **VerticalPosition** - 0 to 1 for custom positioning (default: 0)

### Appearance
- **Width/Height** - Badge dimensions (default: 40x30)
- **Padding** - Internal content spacing
- **FontSize/FontFamily/FontStyle** - Text formatting
- **Stroke/StrokeThickness** - Border styling
- **Rotation** - Rotation angle in degrees
- **Opacity** - Transparency (0-1)

### Animation
- **AnimationType** - None, Scale, Opacity (animates on content change)

## Common Use Cases

1. **Email/Messaging Apps** - Unread message counts on inbox buttons
2. **E-commerce** - Item counts in shopping cart badges
3. **Social Media** - Notification counts on notification icons
4. **Status Indicators** - Online/offline/away status on avatars
5. **Navigation Menus** - New item indicators on menu items
6. **Dashboard Widgets** - Alert counts on dashboard cards
7. **Forms** - Error or warning indicators on form fields
8. **Lists** - Item counts or status on list items

## When to Use BadgeContainer vs Standalone

**Use BadgeContainer when:**
- Badge needs to overlay another control (Button, Image, Icon)
- You need automatic positioning relative to content
- You want badge to follow content when resizing

**Use standalone Badge when:**
- Badge is part of a layout (Grid, StackPanel)
- You're handling positioning with layout containers
- Using badges in ItemTemplates or DataTemplates
- You need manual position control

## Tips and Best Practices

1. **Choose appropriate Fill colors** - Use Success (green) for positive states, Warning (orange) for alerts, Error (red) for critical notifications
2. **Keep content concise** - Single digit, short text, or icon works best
3. **Use Ellipse shape for numbers** - Oval or Ellipse shapes work well for numeric counts
4. **Format large numbers** - Display "99+" for counts over 99 to avoid badge becoming too wide
5. **Consider accessibility** - Ensure sufficient color contrast between background and foreground
6. **Animate content changes** - Use Scale or Opacity animation to draw attention to updates
7. **Hide when zero** - Set Visibility to Collapsed when count is zero or null
8. **Test different sizes** - Verify badge appearance on various control sizes
9. **Use consistent positioning** - Keep badge position consistent across similar controls in your app

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Badge not visible | Check Visibility property, ensure Content is set, verify parent container size |
| Position incorrect | Review HorizontalAnchor/VerticalAnchor values, check alignment properties |
| Content cut off | Increase Width/Height or adjust Padding |
| Color not applying | Background overrides Fill - use one or the other |
| Animation not working | Animation only triggers on Content change, verify AnimationType is set |
| Badge not overlapping | Ensure using BadgeContainer, not standalone Badge |

For detailed implementation guidance, refer to the specific documentation files listed in the Navigation Guide above.
