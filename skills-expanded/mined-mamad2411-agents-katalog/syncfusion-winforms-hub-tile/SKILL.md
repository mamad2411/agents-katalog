---
name: syncfusion-winforms-hub-tile
description: Guide for implementing Syncfusion HubTile control in Windows Forms applications. Use when creating live tile functionality with animated content tiles similar to Windows 8/Windows Phone, including slide, rotate, or pulse transitions. Covers dashboard tiles, live notifications, animated status displays, Windows 8-style UI with automatic animations, banners, and visual updates.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing HubTiles

## When to Use This Skill

Use this skill when the user needs to implement Syncfusion **HubTile control** in a Windows Forms application. HubTile provides live tile functionality with animated transitions similar to Windows 8 and Windows Phone.

### Common Use Cases
1. **Dashboard tiles** - Live-updating dashboard panels with animated content
2. **Application launchers** - Windows 8-style start screen tiles
3. **Status displays** - Animated status indicators with transitions
4. **Live notifications** - Content tiles that update with slide/rotate/pulse effects
5. **Media libraries** - Music/Video tiles with pulsing animations
6. **News feeds** - Tiles that transition between content updates
7. **KPI panels** - Key performance indicators with animated updates
8. **Navigation menus** - Interactive tile-based navigation similar to Windows Phone

**When NOT to use:** For static buttons or panels without animation needs, use standard Button or Panel controls. For data grids or tables, use DataGridView or Syncfusion GridControl.

## Component Overview

Syncfusion **HubTile** is a content control that functions as **live tiles** with automatic animations. Content updates are shown through various transition effects, similar to Windows 8 and Windows Phone live tiles.

**Key components:**
- Title area (top)
- Content/Image area (center)
- Footer area (bottom)
- Optional Banner overlay

### Tile Types

HubTile supports **three animation styles**:

#### 1. DefaultTile
Provides notifications through **slide transition effects** (Bottom-to-Top, Top-to-Bottom, Left-to-Right, Right-to-Left).

**Use when:**
- Displaying sequential content updates
- News or status feeds
- Content that flows in a specific direction

#### 2. RotateTile
Animates by **rotating the tile** horizontally or vertically, flipping to show alternate content.

**Use when:**
- Showing front/back content (e.g., question/answer)
- Dual-state displays
- Content that benefits from flip animation

#### 3. PulsingTile
Creates a **zoom in/out effect**, similar to Windows Phone Music and Video tiles.

**Use when:**
- Media content (music, videos, photos)
- Drawing attention to content
- Creating dynamic visual interest

## Documentation and Navigation Guide

### Installation and Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When user needs to set up HubTile for the first time. Covers:
- Assembly references (Syncfusion.Tools.Windows.dll, Syncfusion.Shared.Base.dll)
- NuGet package installation
- Namespace imports (Syncfusion.Windows.Forms.Tools)
- Designer and code-based setup
- Creating basic tile
- Adding images, title, and footer
- Framework support (.NET Framework 4.5+, .NET 6.0-8.0)

### DefaultTile (Slide Transitions)
📄 **Read:** [references/default-tile.md](references/default-tile.md)

When user needs tiles with slide transition effects. Covers:
- DefaultTile configuration
- Title, Footer, and ImageSource properties
- Transition effects (BottomToTop, TopToBottom, LeftToRight, RightToLeft)
- SlideTransition property
- ImageTransitionSpeed control
- TurnLiveTileOn property
- Complete transition examples

### RotateTile (Flip Animations)
📄 **Read:** [references/rotate-tile.md](references/rotate-tile.md)

When user needs tiles that rotate/flip. Covers:
- RotateTile configuration
- Horizontal and vertical rotation
- RotationTransition property
- TileFlipDirection (Horizontal, Vertical)
- RotationTransitionSpeed control
- Front/back content setup
- Complete rotation examples

### PulsingTile (Zoom Effects)
📄 **Read:** [references/pulsing-tile.md](references/pulsing-tile.md)

When user needs tiles with zoom animations. Covers:
- PulsingTile configuration
- Zoom in/out effects
- PulseDuration property (interval control)
- PulseScale property (zoom level)
- Image translation effects
- Media tile styling
- Complete pulsing examples

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)

When user wants to customize tile appearance. Covers:
- Banner visibility and customization
- Banner text, icons, and colors
- Selection markers (Windows 8 style)
- SelectionMarkerColor property
- Hovered border colors
- EnableHoverColor property
- Expand on hover functionality
- Tile press behavior (slide effect)
- EnableTileSlideEffect property
- Complete styling examples

### Freezing and Control
📄 **Read:** [references/freezing-control.md](references/freezing-control.md)

When user needs to pause/resume tile animations. Covers:
- IsFrozen property
- Stopping animations programmatically
- Dynamic freeze/unfreeze
- Use cases for freezing (loading, user interaction)
- State management
- Complete control examples

## Quick Start Examples

### DefaultTile with Slide Transition

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create HubTile
HubTile newsTile = new HubTile();
newsTile.Size = new Size(200, 200);
newsTile.Location = new Point(20, 20);

// Set tile type
newsTile.TileType = HubTileType.DefaultTile;

// Configure content
newsTile.Title.Text = "Breaking News";
newsTile.Title.TextColor = Color.White;
newsTile.Footer.Text = "CNN";
newsTile.Footer.TextColor = Color.White;
newsTile.BackColor = Color.FromArgb(17, 158, 218);

// Set background image
newsTile.ImageSource = Image.FromFile("news.jpg");

// Enable live tile with transition
newsTile.TurnLiveTileOn = true;
newsTile.SlideTransition = TransitionDirection.BottomToTop;
newsTile.ImageTransitionSpeed = 3;

// Add to form
this.Controls.Add(newsTile);
```

### RotateTile with Flip Animation

```csharp
// Create rotating tile
HubTile rotateTile = new HubTile();
rotateTile.Size = new Size(200, 200);
rotateTile.Location = new Point(240, 20);

// Set tile type
rotateTile.TileType = HubTileType.RotateTile;

// Configure content
rotateTile.Title.Text = "Weather";
rotateTile.Title.TextColor = Color.White;
rotateTile.Footer.Text = "72°F Sunny";
rotateTile.Footer.TextColor = Color.White;
rotateTile.BackColor = Color.FromArgb(255, 140, 0);

// Configure rotation
rotateTile.TurnLiveTileOn = true;
rotateTile.RotationTransition = TileFlipDirection.Horizontal;
rotateTile.RotationTransitionSpeed = 2;

// Add image
rotateTile.ImageSource = Image.FromFile("weather.jpg");

this.Controls.Add(rotateTile);
```

### PulsingTile for Media

```csharp
// Create pulsing tile
HubTile mediaTile = new HubTile();
mediaTile.Size = new Size(200, 200);
mediaTile.Location = new Point(460, 20);

// Set tile type
mediaTile.TileType = HubTileType.PulsingTile;

// Configure content
mediaTile.Title.Text = "Now Playing";
mediaTile.Title.TextColor = Color.White;
mediaTile.Footer.Text = "Music";
mediaTile.Footer.TextColor = Color.White;
mediaTile.BackColor = Color.FromArgb(139, 0, 139);

// Configure pulsing effect
mediaTile.TurnLiveTileOn = true;
mediaTile.PulseDuration = 2;
mediaTile.PulseScale = 1.5f;

// Add album art
mediaTile.ImageSource = Image.FromFile("album.jpg");

this.Controls.Add(mediaTile);
```

## Tile Type Selection Guide

| Need | Use This Type | Why |
|------|--------------|-----|
| Sequential content updates | **DefaultTile** | Smooth slide transitions show progression |
| Directional flow (news feed) | **DefaultTile** (BottomToTop) | Natural reading flow for updates |
| Dual-state content | **RotateTile** | Flip reveals alternate information |
| Front/back content | **RotateTile** | Perfect for question/answer, info/details |
| Media content display | **PulsingTile** | Matches Windows Phone music/video style |
| Draw attention | **PulsingTile** | Zoom effect creates visual interest |
| Static animated tile | Any type with `IsFrozen = false` | Automatic animations |
| Interactive tile | DefaultTile + `EnableTileSlideEffect` | Press feedback effect |

## Common Patterns

### Pattern 1: Dashboard with Multiple Tile Types

```csharp
// Create dashboard layout
FlowLayoutPanel dashboard = new FlowLayoutPanel();
dashboard.Dock = DockStyle.Fill;
dashboard.BackColor = Color.FromArgb(30, 30, 30);
dashboard.Padding = new Padding(10);

// News tile (DefaultTile with slide)
HubTile newsTile = CreateDefaultTile("News", "Latest Updates", Color.FromArgb(17, 158, 218));
newsTile.SlideTransition = TransitionDirection.BottomToTop;
dashboard.Controls.Add(newsTile);

// Weather tile (RotateTile with flip)
HubTile weatherTile = CreateRotateTile("Weather", "72°F", Color.FromArgb(255, 140, 0));
weatherTile.RotationTransition = TileFlipDirection.Horizontal;
dashboard.Controls.Add(weatherTile);

// Media tile (PulsingTile with zoom)
HubTile mediaTile = CreatePulsingTile("Music", "Now Playing", Color.FromArgb(139, 0, 139));
mediaTile.PulseScale = 1.3f;
dashboard.Controls.Add(mediaTile);

this.Controls.Add(dashboard);
```

### Pattern 2: Tile with Banner Notification

```csharp
HubTile notificationTile = new HubTile();
notificationTile.TileType = HubTileType.DefaultTile;
notificationTile.Size = new Size(200, 200);

// Main content
notificationTile.Title.Text = "Messages";
notificationTile.Footer.Text = "Inbox";
notificationTile.BackColor = Color.FromArgb(0, 120, 215);

// Enable banner
notificationTile.ShowBanner = true;
notificationTile.Banner.Text = "5 new messages";
notificationTile.Banner.TextColor = Color.White;
notificationTile.BannerColor = Color.FromArgb(255, 0, 0);

// Optional banner icon
notificationTile.ShowBannerIcon = true;
notificationTile.BannerIcon = Image.FromFile("notification.png");

// Enable transition
notificationTile.TurnLiveTileOn = true;
notificationTile.SlideTransition = TransitionDirection.LeftToRight;
```

### Pattern 3: Interactive Tile with Hover Effects

```csharp
HubTile interactiveTile = new HubTile();
interactiveTile.TileType = HubTileType.DefaultTile;
interactiveTile.Size = new Size(200, 200);

// Content
interactiveTile.Title.Text = "Documents";
interactiveTile.Footer.Text = "Recent Files";
interactiveTile.BackColor = Color.FromArgb(0, 150, 136);

// Enable hover effects
interactiveTile.EnableHoverColor = true;
interactiveTile.HoveredBorderColor = Color.White;
interactiveTile.ExpandOnHover = true;

// Enable press effect
interactiveTile.EnableTileSlideEffect = true;

// Selection marker
interactiveTile.IsSelectionMarked = true;
interactiveTile.SelectionMarkerColor = Color.Yellow;

// Click handler
interactiveTile.Click += (s, e) => {
    MessageBox.Show("Tile clicked!");
};
```

### Pattern 4: Freeze/Unfreeze on Interaction

```csharp
HubTile controlledTile = new HubTile();
controlledTile.TileType = HubTileType.RotateTile;
controlledTile.TurnLiveTileOn = true;

// Freeze on mouse enter
controlledTile.MouseEnter += (s, e) => {
    controlledTile.IsFrozen = true;
};

// Unfreeze on mouse leave
controlledTile.MouseLeave += (s, e) => {
    controlledTile.IsFrozen = false;
};
```

## Key Properties

### Common Properties (All Tile Types)

| Property | Type | Description |
|----------|------|-------------|
| `TileType` | HubTileType | DefaultTile, RotateTile, or PulsingTile |
| `TurnLiveTileOn` | bool | Enable/disable animations |
| `IsFrozen` | bool | Freeze animations temporarily |
| `Title.Text` | string | Title text (top of tile) |
| `Title.TextColor` | Color | Title text color |
| `Footer.Text` | string | Footer text (bottom of tile) |
| `Footer.TextColor` | Color | Footer text color |
| `ImageSource` | Image | Background image |
| `BackColor` | Color | Tile background color |

### DefaultTile Properties

| Property | Type | Description |
|----------|------|-------------|
| `SlideTransition` | TransitionDirection | BottomToTop, TopToBottom, LeftToRight, RightToLeft |
| `ImageTransitionSpeed` | int | Transition speed (1-10, higher = faster) |
| `ShowBanner` | bool | Display banner overlay |
| `Banner.Text` | string | Banner notification text |
| `BannerColor` | Color | Banner background color |
| `ShowBannerIcon` | bool | Display icon in banner |
| `BannerIcon` | Image | Banner icon image |
| `IsSelectionMarked` | bool | Show selection marker (Windows 8 style) |
| `SelectionMarkerColor` | Color | Selection marker border color |
| `EnableHoverColor` | bool | Enable hover border highlight |
| `HoveredBorderColor` | Color | Border color on hover |
| `ExpandOnHover` | bool | Expand tile on mouse hover |
| `EnableTileSlideEffect` | bool | Slide effect on mouse press |

### RotateTile Properties

| Property | Type | Description |
|----------|------|-------------|
| `RotationTransition` | TileFlipDirection | Horizontal or Vertical rotation |
| `RotationTransitionSpeed` | int | Rotation speed (1-10, higher = faster) |

### PulsingTile Properties

| Property | Type | Description |
|----------|------|-------------|
| `PulseDuration` | int | Interval between zoom in/out (seconds) |
| `PulseScale` | float | Zoom level (1.0 = 100%, 2.0 = 200%) |

## Common Use Cases

### 1. Application Dashboard
**Scenario:** Windows 8-style start screen with multiple app tiles  
**Solution:** FlowLayoutPanel with multiple HubTiles using different tile types and transitions

### 2. Live News Feed
**Scenario:** News tiles that slide in updates from bottom  
**Solution:** DefaultTile with BottomToTop transition, periodic content updates via timer

### 3. Media Library
**Scenario:** Music/Video tiles with pulsing animations  
**Solution:** PulsingTile with appropriate PulseScale and album/video art

### 4. Status Monitor
**Scenario:** System status tiles that rotate to show details  
**Solution:** RotateTile with front showing status icon, back showing detailed metrics

### 5. Notification Center
**Scenario:** Tiles with banner notifications for alerts  
**Solution:** DefaultTile with ShowBanner enabled, update Banner.Text dynamically

### 6. Interactive Menu
**Scenario:** Touch-friendly navigation tiles  
**Solution:** DefaultTile with EnableTileSlideEffect, ExpandOnHover, and click handlers

## Best Practices

1. **Choose appropriate tile type** - DefaultTile for sequential content, RotateTile for dual-state, PulsingTile for media
2. **Set reasonable transition speeds** - Speed 2-4 provides smooth animations without being jarring
3. **Use consistent sizing** - Standard Windows 8 tiles are 150x150, 310x150, or 310x310
4. **Apply cohesive color schemes** - Use related colors for tiles in same category
5. **Enable live tiles selectively** - Don't animate all tiles simultaneously to avoid distraction
6. **Provide clear title/footer** - Help users identify tile purpose at a glance
7. **Use banners for urgent notifications** - Reserve banner space for important updates
8. **Freeze on interaction** - Consider freezing tiles when user hovers to prevent distraction
9. **Test transition directions** - Ensure slide direction matches content flow logic
10. **Handle click events** - Make tiles interactive with meaningful click actions

## Tile Styling Guidelines

### Windows 8 Color Palette
```csharp
// Microsoft-inspired colors
Color TealBlue = Color.FromArgb(0, 120, 215);      // Default blue
Color LimeGreen = Color.FromArgb(16, 137, 62);     // Success/positive
Color OrangeRed = Color.FromArgb(202, 80, 16);     // Warning
Color CrimsonRed = Color.FromArgb(232, 17, 35);    // Error/urgent
Color Purple = Color.FromArgb(107, 105, 214);      // Media/entertainment
Color Teal = Color.FromArgb(0, 153, 188);          // Information
```

### Size Recommendations
```csharp
// Small tile (single)
Size smallTile = new Size(150, 150);

// Wide tile (horizontal)
Size wideTile = new Size(310, 150);

// Large tile
Size largeTile = new Size(310, 310);
```
