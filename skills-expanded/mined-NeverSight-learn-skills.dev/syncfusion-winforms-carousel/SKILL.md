---
name: syncfusion-winforms-carousel
description: Guides implementation of the Syncfusion WinForms Carousel control for creating 3D circular conveyors with rotating objects. Use this when creating interactive image galleries, product showcases, or 3D item displays with carousel paths. Covers image slides, rotation control, touch interactions, and visual customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion WinForms Carousel Control

The Carousel control is a circular conveyor that displays and rotates objects in a 3D interface. It provides interactive navigation for images, custom controls, and various carousel path options for creating engaging visual displays.

## When to Use This Skill

Use the Carousel control when you need to:
- Create interactive 3D image galleries or product showcases
- Display rotating panels with custom controls
- Implement circular navigation for items or images
- Build image slide shows with carousel effects
- Create product viewers with multiple angle displays
- Implement touch-enabled rotating interfaces
- Design orbital or linear item arrangements
- Build visual dashboards with rotating components
- Create engaging UI presentations with 3D effects

## Installation

### NuGet Installation

```bash
Install-Package Syncfusion.Tools.Windows
```

### Assembly References

Add references to:
- `Syncfusion.Grid.Base`
- `Syncfusion.Grid.Windows`
- `Syncfusion.Shared.Base`
- `Syncfusion.Shared.Windows`
- `Syncfusion.Tools.Base`
- `Syncfusion.Tools.Windows`

## Quick Start

### Basic Carousel with Custom Controls

```csharp
using System;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Tools;

namespace CarouselDemo
{
    public partial class Form1 : Form
    {
        private Carousel carousel1;
        
        public Form1()
        {
            InitializeComponent();
            
            // Create Carousel
            carousel1 = new Carousel();
            carousel1.Size = new System.Drawing.Size(600, 400);
            carousel1.Location = new System.Drawing.Point(50, 50);
            
            // Create custom controls (e.g., buttons)
            for (int i = 1; i <= 6; i++)
            {
                ButtonAdv button = new ButtonAdv();
                button.Text = "Item " + i;
                button.Size = new System.Drawing.Size(100, 80);
                button.BackColor = System.Drawing.Color.FromArgb(22, 165, 220);
                button.ForeColor = System.Drawing.Color.White;
                
                // Add to both Controls and Items collections
                carousel1.Controls.Add(button);
                carousel1.Items.Add(button);
            }
            
            // Add to form
            this.Controls.Add(carousel1);
        }
    }
}
```

### Basic Carousel with Images

```csharp
using Syncfusion.Windows.Forms.Tools;

// Enable image slides
carousel1.ImageSlides = true;

// Create and add images
for (int i = 1; i <= 6; i++)
{
    CarouselImage carouselImage = new CarouselImage();
    carouselImage.ItemImage = Image.FromFile($"Images/image{i}.png");
    
    carousel1.ImageListCollection.Add(carouselImage);
}
```

## Core Concepts

### Carousel Paths
The control supports multiple path arrangements: Default (elliptical), Orbital, Oval, and Linear. Each path provides different visual layouts for items.

### Image Slides Mode
Enable `ImageSlides = true` to work specifically with images. Images can be added via `ImageListCollection`, `ImageList` property, or `FilePath` property.

### Custom Controls
Any WinForms control can be added to the carousel. Controls must be added to both `Controls` and `Items` collections.

### Perspective and Speed
Control the visual depth with `Perspective` property and rotation speed with `TransitionSpeed` property.

### Touch Interactions
The carousel responds to touch gestures: pan/flick for rotation, pinch/stretch for perspective adjustments.

## Navigation Guide

### 🚀 Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and dependencies
- Adding Carousel via Designer
- Adding Carousel via code
- Adding custom controls to carousel
- Adding images to carousel
- Initial setup and configuration

### 🛤️ Carousel Paths
📄 **Read:** [references/carousel-paths.md](references/carousel-paths.md)
- Default (elliptical) path
- Orbital path layout
- Oval path layout
- Linear path arrangement
- Choosing the right path for your scenario
- Path property configuration

### 🖼️ Image Slides
📄 **Read:** [references/image-slides.md](references/image-slides.md)
- Enabling ImageSlides mode
- Adding images via ImageListCollection
- Adding images via ImageList property
- Adding images via FilePath property
- CarouselImage class usage
- Image management best practices

### 🎨 Visual Configuration
📄 **Read:** [references/visual-configuration.md](references/visual-configuration.md)
- Perspective property (zoom control)
- TransitionSpeed property (rotation speed)
- ShowImageShadow property
- ShowImagePreview property
- ImageHighlightColor property
- ImageShadeColor property
- Combining visual effects

### 🔄 Rotation Behavior
📄 **Read:** [references/rotation-behavior.md](references/rotation-behavior.md)
- RotateAlways property for continuous rotation
- Auto-play configuration
- Controlling rotation programmatically
- Stopping and starting rotation

### 👆 Touch Interactions
📄 **Read:** [references/touch-interactions.md](references/touch-interactions.md)
- Touch support overview
- Pan and flick gestures for rotation
- Pinch and stretch for perspective control
- Touch vs mouse interactions

## Common Patterns

### Pattern 1: Product Image Gallery
```csharp
// Create image-based carousel for product showcase
Carousel productCarousel = new Carousel();
productCarousel.ImageSlides = true;
productCarousel.CarouselPath = CarouselPath.Default;
productCarousel.Perspective = 4.5f;
productCarousel.TransitionSpeed = 2.0f;
productCarousel.ShowImagePreview = true;
productCarousel.ShowImageShadow = true;

// Add product images
foreach (string imagePath in Directory.GetFiles("Products", "*.jpg"))
{
    CarouselImage img = new CarouselImage();
    img.ItemImage = Image.FromFile(imagePath);
    productCarousel.ImageListCollection.Add(img);
}

this.Controls.Add(productCarousel);
```

### Pattern 2: Auto-Rotating Dashboard Panels
```csharp
// Create auto-rotating carousel with custom controls
Carousel dashboardCarousel = new Carousel();
dashboardCarousel.CarouselPath = CarouselPath.Orbital;
dashboardCarousel.RotateAlways = true;
dashboardCarousel.TransitionSpeed = 1.5f;
dashboardCarousel.Perspective = 3.0f;

// Add dashboard panels
Panel salesPanel = CreateDashboardPanel("Sales", salesData);
Panel inventoryPanel = CreateDashboardPanel("Inventory", inventoryData);
Panel reportsPanel = CreateDashboardPanel("Reports", reportData);

dashboardCarousel.Controls.Add(salesPanel);
dashboardCarousel.Items.Add(salesPanel);
dashboardCarousel.Controls.Add(inventoryPanel);
dashboardCarousel.Items.Add(inventoryPanel);
dashboardCarousel.Controls.Add(reportsPanel);
dashboardCarousel.Items.Add(reportsPanel);

this.Controls.Add(dashboardCarousel);
```

### Pattern 3: Linear Navigation Strip
```csharp
// Create linear carousel for horizontal navigation
Carousel navigationCarousel = new Carousel();
navigationCarousel.CarouselPath = CarouselPath.Linear;
navigationCarousel.TransitionSpeed = 3.0f;
navigationCarousel.Size = new Size(800, 150);
navigationCarousel.Dock = DockStyle.Top;

// Add navigation buttons
string[] sections = { "Home", "Products", "Services", "About", "Contact" };
foreach (string section in sections)
{
    ButtonAdv navButton = new ButtonAdv();
    navButton.Text = section;
    navButton.Size = new Size(120, 100);
    navButton.ButtonStyle = ButtonAppearance.Metro;
    
    navigationCarousel.Controls.Add(navButton);
    navigationCarousel.Items.Add(navButton);
}

this.Controls.Add(navigationCarousel);
```

### Pattern 4: Touch-Enabled Photo Viewer
```csharp
// Create touch-friendly image carousel
Carousel photoViewer = new Carousel();
photoViewer.ImageSlides = true;
photoViewer.CarouselPath = CarouselPath.Oval;
photoViewer.Perspective = 5.0f;
photoViewer.TransitionSpeed = 2.5f;
photoViewer.ShowImagePreview = true;
photoViewer.ImageHighlightColor = Color.Gold;
photoViewer.Dock = DockStyle.Fill;

// Load photos from folder
photoViewer.FilePath = Application.StartupPath + "\\Photos";

this.Controls.Add(photoViewer);
// Touch gestures (pan, flick, pinch, stretch) work automatically
```

### Pattern 5: Themed Carousel with Custom Colors
```csharp
// Create visually customized carousel
Carousel themedCarousel = new Carousel();
themedCarousel.ImageSlides = true;
themedCarousel.CarouselPath = CarouselPath.Default;
themedCarousel.BackColor = Color.FromArgb(30, 30, 30);
themedCarousel.Perspective = 4.0f;
themedCarousel.TransitionSpeed = 2.0f;

// Apply custom visual effects
themedCarousel.ShowImageShadow = true;
themedCarousel.ShowImagePreview = true;
themedCarousel.ImageHighlightColor = Color.FromArgb(255, 215, 0); // Gold
themedCarousel.ImageShadeColor = Color.FromArgb(100, 100, 100);   // Gray

// Add images
foreach (var image in imageCollection)
{
    CarouselImage carouselImg = new CarouselImage();
    carouselImg.ItemImage = image;
    themedCarousel.ImageListCollection.Add(carouselImg);
}

this.Controls.Add(themedCarousel);
```

## Key Properties Reference

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `CarouselPath` | CarouselPath | Default | Path layout: Default, Orbital, Oval, Linear |
| `ImageSlides` | bool | false | Enable image-specific mode |
| `Items` | CarouselItemCollection | - | Collection of items to display |
| `ImageListCollection` | CarouselImageCollection | - | Collection of CarouselImage objects |
| `FilePath` | string | "" | Folder path to load images from |
| `Perspective` | float | 0 | Zoom level of elliptical view |
| `TransitionSpeed` | float | 0 | Rotation speed multiplier |
| `RotateAlways` | bool | false | Enable continuous auto-rotation |
| `ShowImageShadow` | bool | false | Display shadows for images |
| `ShowImagePreview` | bool | false | Show preview of selected image at center |
| `ImageHighlightColor` | Color | - | Color for highlighting selected image |
| `ImageShadeColor` | Color | - | Color for shading background images |

## Carousel Path Options

| Path | Description | Use Case |
|------|-------------|----------|
| **Default** | Normal elliptical arrangement | General carousels, balanced layouts |
| **Orbital** | Orbital curve arrangement | Space-themed displays, scientific UIs |
| **Oval** | Oval structure arrangement | Wide displays, horizontal emphasis |
| **Linear** | Horizontal linear arrangement | Navigation strips, horizontal galleries |

## Best Practices

1. **Choose Appropriate Path**: Select carousel path based on layout needs (Default for general use, Linear for horizontal navigation)

2. **Add to Both Collections**: Custom controls must be added to both `Controls` and `Items` collections

3. **Enable ImageSlides for Images**: Set `ImageSlides = true` when working exclusively with images

4. **Optimize Image Count**: Keep image count reasonable (6-12 items) for smooth performance

5. **Set Appropriate Speed**: Use TransitionSpeed 1.5-3.0 for comfortable viewing; higher values for quick browsing

6. **Use Perspective Wisely**: Perspective values 3.0-5.0 work well for most scenarios

7. **Image Sizing**: Ensure images are reasonably sized (compress large images) for performance

8. **Touch-First Design**: Design for touch if targeting touch devices; gestures work automatically

9. **Test Auto-Rotation**: If using RotateAlways, ensure TransitionSpeed allows comfortable viewing

10. **Visual Feedback**: Use ImageHighlightColor to clearly indicate selected item

## Framework Support

- .NET Framework 4.5 and above
- .NET 6.0, .NET 7.0, .NET 8.0 (Windows)
- .NET Core 3.1 (Windows)

## Additional Resources

- [Syncfusion Carousel Documentation](https://help.syncfusion.com/windowsforms/carousel/overview)
- [API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.Carousel.html)
- [Knowledge Base Articles](https://www.syncfusion.com/kb/windowsforms/carousel)
- [GitHub Samples](https://github.com/syncfusion/winforms-demos)

## Related Controls

- **CarouselImage**: Class for defining carousel image items
- **ButtonAdv**: Enhanced button often used as carousel items
- **PictureBox**: Standard image control
- **Panel**: Container control for grouping custom content

## Troubleshooting

**Issue**: Items not appearing in carousel
- Ensure items are added to both `Controls` and `Items` collections
- Verify carousel size is sufficient to display items
- Check that items have appropriate size properties set

**Issue**: Images not displaying
- Confirm `ImageSlides = true` is set
- Verify image paths are correct
- Check that images are added to `ImageListCollection`

**Issue**: Carousel not rotating
- If using RotateAlways, ensure it's set to true
- Check TransitionSpeed is set to a positive value
- Verify control is visible and enabled

**Issue**: Touch gestures not working
- Ensure application targets touch-enabled framework version
- Test on actual touch device (not mouse simulation)
- Check that carousel is in focus

**Issue**: Performance issues with many items
- Reduce number of items (keep to 6-12 items)
- Compress large images before adding
- Lower TransitionSpeed if rotation is choppy
- Consider disabling ShowImageShadow if performance is critical
