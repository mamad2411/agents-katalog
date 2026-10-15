---
name: syncfusion-winforms-tile-layout
description: Guide for implementing Syncfusion TileLayout control in Windows Forms applications. Use when creating Windows 8 Metro-style tile interfaces, grouped tile containers, live tiles with rotating images/text using ImageStreamer, drag-and-drop reordering, or dashboard-style layouts with customizable positioning and appearance.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing TileLayout in Syncfusion WinForms

This skill guides you in implementing **Syncfusion WinForms TileLayout** control—a Windows 8 Start screen-inspired container that holds tile items organized in groups, supports drag-and-drop reordering, live tiles with rotating content, and flexible layout customization.

## When to Use This Skill

Use this skill when the user needs to:

- Create **Windows 8 Metro-style tile interfaces** with grouped tiles
- Implement **dashboard layouts** with draggable, rearrangeable tiles
- Build **live tile displays** with rotating images or text using ImageStreamer
- Design **grouped tile containers** organized by logical categories (LayoutGroups)
- Add **drag-and-drop tile reordering** at runtime within or between groups
- Create **customizable tile layouts** with margins, alignment, and positioning
- Implement **modern, touch-friendly interfaces** with tile-based navigation
- Build **application launchers** or **start screens** with tile-based menus
- Display **photo galleries** or **media collections** in tile format
- Create **status dashboards** with multiple information tiles

TileLayout is ideal for modern applications requiring flexible, visual, tile-based interfaces similar to Windows 8/10 Start screens.

## Component Overview

**TileLayout** is a container control that manages a collection of tiles organized into **LayoutGroups**. Each LayoutGroup contains **ImageStreamer** items that act as individual tiles. The control provides:

- **LayoutGroups**: Logical grouping of tiles with optional titles
- **ImageStreamer Items**: Live tiles that can display rotating images/text
- **Drag-and-Drop**: Runtime reordering of tiles within/between groups
- **Layout Customization**: Margins, alignment, row direction control
- **Appearance Options**: Themes, flat parent form, group title display
- **Matrix Positioning**: Automatic tile arrangement in responsive grid

**Key Hierarchy:**
```
TileLayout (Container)
└── LayoutGroup(s) (Groups)
    └── ImageStreamer(s) (Individual Tiles)
```

## Documentation and Navigation Guide

### Getting Started and Basic Setup

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when users need:
- Assembly dependencies and NuGet packages required
- Creating TileLayout via designer or code
- Adding LayoutGroups to organize tiles
- Adding ImageStreamer items to groups
- Basic configuration for first implementation
- Complete minimal working example
- Understanding the TileLayout hierarchy

### Layout Customization

📄 **Read:** [references/layout-customization.md](references/layout-customization.md)

Read this reference when users need:
- Alignment property (Near, Far, Center)
- Horizontal margins (HorzNearMargin, HorzFarMargin)
- Vertical margins (TopMargin, BottomMargin)
- ReverseRows to change layout direction
- MainLayout property configuration
- Custom positioning and spacing
- Responsive layout behavior

### Appearance and Styling

📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)

Read this reference when users need:
- SetParentFormFlat for flat form appearance
- ShowGroupTitle to display group names
- IgnoreThemeBackground for custom BackColor
- Theme integration and styling
- Visual customization options
- Professional appearance configuration

### ImageStreamer Live Tiles

📄 **Read:** [references/image-streamer-tiles.md](references/image-streamer-tiles.md)

Read this reference when users need:
- Adding images to ImageStreamer tiles
- SlideShow and SliderSpeed for animation
- ShowNavigator for navigation controls
- ImageStreamDirection (5 directions: LeftToRight, RightToLeft, TopToBottom, BottomToTop, HorizontalFlip)
- ImageStreamerType (Normal vs DoubleHorizontal)
- InternalBackColor for tile background
- Creating live, rotating tiles with images/text
- Configuring tile animations and transitions

### Drag and Drop

📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)

Read this reference when users need:
- Drag-and-drop within LayoutGroups
- Drag-and-drop between different groups
- Runtime tile reordering by users
- User interaction patterns
- Restrictions and best practices

## Quick Start Example

Here's a minimal example creating a TileLayout with two groups and live tiles:

```csharp
using Syncfusion.Windows.Forms.Tools;
using System;
using System.Drawing;
using System.Windows.Forms;

public class TileLayoutExample : Form
{
    private TileLayout tileLayout1;
    private LayoutGroup layoutGroup1;
    private LayoutGroup layoutGroup2;
    private ImageStreamer imageStreamer1;
    private ImageStreamer imageStreamer2;
    
    public TileLayoutExample()
    {
        // Create TileLayout
        tileLayout1 = new TileLayout();
        tileLayout1.Dock = DockStyle.Fill;
        tileLayout1.ShowGroupTitle = true;
        
        // Create first LayoutGroup
        layoutGroup1 = new LayoutGroup();
        layoutGroup1.Text = "Photos";
        layoutGroup1.BackColor = ColorTranslator.FromHtml("#fa8c6f5");
        
        // Create second LayoutGroup
        layoutGroup2 = new LayoutGroup();
        layoutGroup2.Text = "Documents";
        layoutGroup2.BackColor = ColorTranslator.FromHtml("#fa8c6f5");
        
        // Create ImageStreamer tiles with images
        imageStreamer1 = new ImageStreamer();
        imageStreamer1.SlideShow = true;
        imageStreamer1.SliderSpeed = 100;
        imageStreamer1.Images.Add(Image.FromFile("image1.jpg"));
        imageStreamer1.Images.Add(Image.FromFile("image2.jpg"));
        
        imageStreamer2 = new ImageStreamer();
        imageStreamer2.InternalBackColor = Color.LightBlue;
        imageStreamer2.Images.Add(Image.FromFile("doc1.png"));
        
        // Add ImageStreamers to LayoutGroups
        layoutGroup1.Controls.Add(imageStreamer1);
        layoutGroup2.Controls.Add(imageStreamer2);
        
        // Add LayoutGroups to TileLayout
        tileLayout1.Controls.Add(layoutGroup1);
        tileLayout1.Controls.Add(layoutGroup2);
        
        // Add TileLayout to form
        this.Controls.Add(tileLayout1);
        this.Size = new Size(800, 600);
        this.Text = "TileLayout Example";
    }
}
```

**Result:** A tile layout with two groups ("Photos" and "Documents"), each containing live tiles with rotating images.

## Common Patterns

### Dashboard with Multiple Tile Groups

**Pattern:** Create a dashboard with multiple grouped sections for different content types.

```csharp
// Create main TileLayout
var tileLayout = new TileLayout();
tileLayout.Dock = DockStyle.Fill;
tileLayout.ShowGroupTitle = true;
tileLayout.MainLayout.TopMargin = 20;
tileLayout.MainLayout.HorzNearMargin = 20;

// Create groups for different categories
var socialGroup = new LayoutGroup { Text = "Social" };
var newsGroup = new LayoutGroup { Text = "News" };
var mediaGroup = new LayoutGroup { Text = "Media" };

// Add multiple tiles to each group
for (int i = 0; i < 4; i++)
{
    var tile = new ImageStreamer();
    tile.Images.Add(GetImage($"social{i}.png"));
    tile.SlideShow = true;
    socialGroup.Controls.Add(tile);
}

tileLayout.Controls.Add(socialGroup);
tileLayout.Controls.Add(newsGroup);
tileLayout.Controls.Add(mediaGroup);
```

**When:** User needs organized dashboard with multiple categories of tiles.

### Live Tiles with Custom Animation

**Pattern:** Configure ImageStreamer tiles with rotating content and custom animation direction.

```csharp
// Create live tile with multiple images
var liveTile = new ImageStreamer();
liveTile.SlideShow = true;
liveTile.SliderSpeed = 150; // Slower animation
liveTile.ShowNavigator = true; // Show navigation arrows
liveTile.ImageStreamDirection = ImageStreamer.StreamDirection.BottomToTop;

// Add multiple images for rotation
liveTile.Images.Add(Image.FromFile("slide1.png"));
liveTile.Images.Add(Image.FromFile("slide2.png"));
liveTile.Images.Add(Image.FromFile("slide3.png"));
liveTile.InternalBackColor = Color.FromArgb(0, 120, 215); // Modern blue

layoutGroup.Controls.Add(liveTile);
```

**When:** User needs tiles with automatically rotating content (news feeds, photo galleries, status displays).

### Customized Layout Positioning

**Pattern:** Control tile layout with custom margins and alignment.

```csharp
// Configure MainLayout for custom positioning
tileLayout.MainLayout.Alignment = FlowAlignment.Center;
tileLayout.MainLayout.HorzNearMargin = 50;  // Left margin
tileLayout.MainLayout.HorzFarMargin = 50;   // Right margin
tileLayout.MainLayout.TopMargin = 30;       // Top margin
tileLayout.MainLayout.BottomMargin = 30;    // Bottom margin
tileLayout.MainLayout.ReverseRows = false;  // Standard flow
```

**When:** User needs centered layouts, custom spacing, or specific positioning.

## Key Properties

### TileLayout Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `ShowGroupTitle` | bool | Shows/hides group titles | Display category names above groups |
| `SetParentFormFlat` | bool | Applies flat look to parent form | Modern, minimalist appearance |
| `IgnoreThemeBackground` | bool | Use BackColor instead of theme | Custom background colors |
| `MainLayout.Alignment` | FlowAlignment | Near, Center, Far alignment | Control tile group positioning |
| `MainLayout.HorzNearMargin` | int | Left margin (pixels) | Custom left spacing |
| `MainLayout.HorzFarMargin` | int | Right margin (pixels) | Custom right spacing |
| `MainLayout.TopMargin` | int | Top margin (pixels) | Custom top spacing |
| `MainLayout.BottomMargin` | int | Bottom margin (pixels) | Custom bottom spacing |
| `MainLayout.ReverseRows` | bool | Reverse layout direction | Right-to-left or bottom-to-top flow |

### LayoutGroup Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Text` | string | Group title text | Label for tile category |
| `BackColor` | Color | Group background color | Visual distinction between groups |
| `Items` | Collection | ImageStreamer items in group | Access/manage tiles in group |

### ImageStreamer (Tile) Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Images` | ImageCollection | Collection of images to display | Add images for live tiles |
| `SlideShow` | bool | Enable image rotation | Animate tiles with multiple images |
| `SliderSpeed` | int | Animation speed (ms) | Control rotation speed |
| `ShowNavigator` | bool | Show navigation arrows | Allow manual image navigation |
| `ImageStreamDirection` | StreamDirection | Animation direction | Control slide direction |
| `Type` | ImageStreamerType | Normal or DoubleHorizontal | Display 1 or 2 images |
| `InternalBackColor` | Color | Tile background color | Customize individual tile colors |

## Common Use Cases

### Application Launcher

Create a Windows 8-style start screen with app tiles:
- Group apps by category (Productivity, Media, Games)
- Each tile shows app icon
- Click tile to launch application
- Drag-and-drop to reorder favorites

### Photo Gallery Dashboard

Display photo collections in tile format:
- Group photos by album/date
- ImageStreamers show rotating photos
- SlideShow for automatic cycling
- Click to view full-size image

### Status Monitoring Dashboard

Real-time status display with live tiles:
- Group by system/service type
- Tiles show current status/metrics
- Auto-update with new data
- Color-coded tiles for status (green/yellow/red)

### News/Social Feed Aggregator

Display multiple content feeds:
- Group by feed source (News, Twitter, RSS)
- Tiles rotate through recent items
- Click tile to open full article
- Automatic refresh at intervals

## Implementation Checklist

When implementing TileLayout, ensure:

- ✅ **Required assemblies** referenced (Syncfusion.Tools.Windows.dll, etc.)
- ✅ **TileLayout** created and added to form (typically docked)
- ✅ **LayoutGroups** added to organize tiles by category
- ✅ **ImageStreamer items** added to LayoutGroups as tiles
- ✅ **Images loaded** into ImageStreamer.Images collection
- ✅ **SlideShow/SliderSpeed** configured for live tiles
- ✅ **Layout margins/alignment** customized if needed
- ✅ **Group titles** shown/hidden appropriately
- ✅ **Drag-and-drop** enabled (default behavior)
- ✅ **Event handlers** added for tile clicks if needed

## Troubleshooting Quick Reference

**Issue:** Tiles not appearing
- Ensure ImageStreamer.Images collection has at least one image
- Check LayoutGroup.Controls contains ImageStreamer instances
- Verify TileLayout.Controls contains LayoutGroups

**Issue:** SlideShow not animating
- Set `ImageStreamer.SlideShow = true`
- Ensure multiple images in Images collection
- Check SliderSpeed is reasonable value (50-200 ms)

**Issue:** Drag-and-drop not working
- Drag-and-drop is enabled by default
- Ensure not handling conflicting mouse events
- Check tiles are ImageStreamer controls, not other types

**Issue:** Layout not centered/aligned properly
- Use `MainLayout.Alignment` property
- Adjust HorzNearMargin/HorzFarMargin for horizontal positioning
- Set TopMargin/BottomMargin for vertical spacing

**Issue:** Theme background overriding custom colors
- Set `IgnoreThemeBackground = true`
- Then apply custom BackColor to TileLayout/LayoutGroups
