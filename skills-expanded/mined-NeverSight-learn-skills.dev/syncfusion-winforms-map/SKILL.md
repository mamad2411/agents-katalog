---
name: syncfusion-winforms-map
description: Implementation guide for Syncfusion WinForms Maps control - a geographical data visualization component that displays statistical and regional data using shape files, bubbles, markers, and interactive features. Use this when working with WinForms Maps, geographical maps in Windows Forms, shape file visualization, choropleth maps, or bubble maps. This skill covers map layers, zooming/panning, geographical data binding, ESRI shape files, and building location-based desktop applications with interactive maps.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Maps in Windows Forms

The Syncfusion WinForms Maps control is a powerful geographical data visualization component that renders shape files and displays statistical information with interactive features like zooming, panning, tooltips, and selection.

## When to Use This Skill

Use the Maps control when you need to:

- **Geographical Visualization**: Display geographical data on world maps, country maps, or regional maps
- **Statistical Maps**: Create choropleth maps showing statistical data by region (population, sales, demographics)
- **Bubble Maps**: Visualize data using bubbles of varying sizes on map locations
- **Multi-Layer Maps**: Combine multiple geographical layers (e.g., world map with highlighted regions)
- **Interactive Maps**: Enable user interaction with tooltips, selection, zooming, and panning
- **Dashboard Integration**: Add map visualizations to desktop dashboard applications
- **Location Analytics**: Build applications that analyze and display location-based data

## Component Overview

**Key Features:**
- Shape file rendering (.shp, .dbf, .shx)
- Multiple layer support with SubShapeFileLayers
- Data binding with ItemSource
- Bubble visualization with size and color mapping
- Legend support with customizable positioning
- Interactive features: tooltips, selection, zooming, panning
- Annotations for custom markers
- Extensive customization options for colors, strokes, and fills

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet installation
- Key concepts and map structure
- Shape file description and requirements
- Adding shape files as embedded resources
- Uri property configuration
- Creating your first map
- Basic implementation example

### Layers and Shape Files
📄 **Read:** [references/layers.md](references/layers.md)
- ShapeFileLayer architecture
- Adding multiple layers (MultiLayer support)
- SubShapeFileLayer usage
- LayoutType configuration (Default vs Tile)
- ItemSource data binding
- ShapeIDPath and ShapeIDTableField mapping
- Layer customization

### Bubbles
📄 **Read:** [references/bubbles.md](references/bubbles.md)
- Adding bubbles to maps
- BubbleSetting properties (AutoFillColors, MaxSize, MinSize)
- ValuePath and ColorValuePath configuration
- Range color mapping for bubbles
- StrokeThickness and Fill customization
- Bubble visualization examples

### Legends
📄 **Read:** [references/legends.md](references/legends.md)
- Legend visibility (ShowLegend)
- Legend positioning (Position, PositionX, PositionY)
- Legend header and title
- Legend categories (layers vs bubbles)
- LegendType and LegendIcon
- Legend shape customization

### User Interaction
📄 **Read:** [references/user-interaction.md](references/user-interaction.md)
- Tooltip support (ShowToolTip)
- Single and multiple selection
- EnableSelection and SelectionMode
- SelectedShapeColor customization
- Zooming with ZoomFactor and ZoomLevel
- Panning and navigation
- ShapeSelected event handling

### Map Points
📄 **Read:** [references/map-points.md](references/map-points.md)
- Point shape files and geometries
- Loading point data layers
- Point vs polygon vs polyline shapes
- Styling point markers
- Point data binding
- Multiple point layers

### Annotations
📄 **Read:** [references/annotations.md](references/annotations.md)
- Adding custom annotations
- Latitude and Longitude positioning
- AnnotationDrawing event
- Custom markers and icons
- Annotation collections
- Drawing custom graphics on maps

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Map appearance styling
- Shape fill and stroke customization
- Color value paths
- FillSetting configuration
- ColorMappings for ranges
- Theme integration
- Advanced styling techniques

## Quick Start

### Step 1: Install NuGet Package

```bash
Install-Package Syncfusion.Maps.WinForms
```

### Step 2: Add Shape Files to Project

1. Add shape files (e.g., `world1.shp`, `world1.dbf`, `world1.shx`) to your project
2. Select files in Solution Explorer
3. Set **Build Action** to **Embedded Resource**
4. Set **Copy to Output Directory** to **Copy if newer** (optional)

### Step 3: Basic Map Implementation

```csharp
using System;
using System.Drawing;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Maps;

namespace WinFormsMapsExample
{
    public partial class Form1 : Form
    {
        private Maps mapsControl;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Create Maps control
            mapsControl = new Maps();
            mapsControl.Name = "mapsControl";
            mapsControl.Size = new Size(880, 585);
            mapsControl.Dock = DockStyle.Fill;
            mapsControl.MapBackgroundBrush = new SolidBrush(Color.White);

            // Create and configure shape layer
            ShapeFileLayer shapeLayer = new ShapeFileLayer();
            shapeLayer.Uri = "world1.shp";  // Shape file name
            
            // Add layer to map
            mapsControl.Layers.Add(shapeLayer);
            
            // Add control to form
            this.Controls.Add(mapsControl);
        }
    }
}
```

## Common Patterns

### Pattern 1: Data-Bound Map with Statistical Visualization

```csharp
private void CreateDataBoundMap()
{
    // Prepare data
    MapViewModel model = new MapViewModel();
    
    // Create shape layer
    ShapeFileLayer shapeLayer = new ShapeFileLayer();
    shapeLayer.Uri = "world1.shp";
    
    // Bind data
    shapeLayer.ItemSource = model.Countries;
    shapeLayer.ShapeIDPath = "NAME";            // Property in data model
    shapeLayer.ShapeIDTableField = "NAME";      // Column in .dbf file
    
    // Configure shape display
    shapeLayer.ShapeSetting.ShapeValuePath = "Population";
    shapeLayer.ShapeSetting.ShapeColorValuePath = "Population";
    shapeLayer.ShapeSetting.ShapeDisplayValuePath = "NAME";
    
    // Style settings
    shapeLayer.ShapeSetting.ShapeFill = "#E5E5E5";
    shapeLayer.ShapeSetting.ShapeStroke = "#C1C1C1";
    shapeLayer.ShapeSetting.ShapeStrokeThickness = 1.5;
    
    // Enable features
    shapeLayer.ShowToolTip = true;
    shapeLayer.EnableSelection = true;
    
    mapsControl.Layers.Add(shapeLayer);
}

// Data Model
public class Country
{
    public string NAME { get; set; }
    public double Population { get; set; }
}
```

### Pattern 2: Multi-Layer Map

```csharp
private void CreateMultiLayerMap()
{
    // Base world layer
    ShapeFileLayer worldLayer = new ShapeFileLayer();
    worldLayer.Uri = "world1.shp";
    worldLayer.ShapeSetting.ShapeFill = "#E5E5E5";
    worldLayer.ShapeSetting.ShapeStroke = "#C1C1C1";
    worldLayer.ShapeSetting.ShapeStrokeThickness = 0.5;

    // Highlighted region 1
    SubShapeFileLayer africaLayer = new SubShapeFileLayer();
    africaLayer.Uri = "africa.shp";
    africaLayer.ShapeSetting.ShapeFill = "#8DCEFF";
    africaLayer.ShapeSetting.ShapeStroke = "#2F8CEA";
    africaLayer.ShapeSetting.ShapeStrokeThickness = 0.5;

    // Highlighted region 2
    SubShapeFileLayer australiaLayer = new SubShapeFileLayer();
    australiaLayer.Uri = "australia.shp";
    australiaLayer.ShapeSetting.ShapeFill = "#FFA07A";
    australiaLayer.ShapeSetting.ShapeStroke = "#FF6347";
    australiaLayer.ShapeSetting.ShapeStrokeThickness = 0.5;

    // Add sublayers to main layer
    worldLayer.SubShapeFileLayers.Add(africaLayer);
    worldLayer.SubShapeFileLayers.Add(australiaLayer);
    
    mapsControl.Layers.Add(worldLayer);
}
```

### Pattern 3: Bubble Map with Color Ranges

```csharp
private void CreateBubbleMap()
{
    ShapeFileLayer shapeLayer = new ShapeFileLayer();
    shapeLayer.Uri = "world1.shp";
    shapeLayer.ItemSource = GetCountries();
    shapeLayer.ShapeIDPath = "NAME";
    shapeLayer.ShapeIDTableField = "NAME";

    // Configure bubbles
    shapeLayer.BubbleSetting.AutoFillColors = false;
    shapeLayer.BubbleSetting.MaxSize = 70;
    shapeLayer.BubbleSetting.MinSize = 25;
    shapeLayer.BubbleSetting.ValuePath = "Population";
    shapeLayer.BubbleSetting.ColorValuePath = "Population";

    // Define color ranges
    shapeLayer.BubbleSetting.ColorMappings = 
        new System.Collections.ObjectModel.ObservableCollection<ColorMapping>
        {
            new RangeColorMapping 
            { 
                From = 1000000000, 
                To = 2000000000, 
                Color = Color.FromArgb(127, 32, 188, 238) 
            },
            new RangeColorMapping 
            { 
                From = 500000000, 
                To = 1000000000, 
                Color = Color.FromArgb(127, 167, 206, 56) 
            },
            new RangeColorMapping 
            { 
                From = 100000000, 
                To = 500000000, 
                Color = Color.FromArgb(127, 241, 178, 26) 
            },
            new RangeColorMapping 
            { 
                From = 0, 
                To = 100000000, 
                Color = Color.FromArgb(127, 235, 115, 124) 
            }
        };

    mapsControl.Layers.Add(shapeLayer);
}
```

### Pattern 4: Interactive Map with Events

```csharp
private void CreateInteractiveMap()
{
    ShapeFileLayer shapeLayer = new ShapeFileLayer();
    shapeLayer.Uri = "world1.shp";
    shapeLayer.ItemSource = GetCountries();
    shapeLayer.ShapeIDPath = "Country";
    shapeLayer.ShapeIDTableField = "NAME";
    
    // Enable interaction
    shapeLayer.ShowToolTip = true;
    shapeLayer.EnableSelection = true;
    shapeLayer.SelectionMode = SelectionModes.Multiple;
    
    // Style selected shapes
    shapeLayer.ShapeSetting.SelectedShapeColor = Color.Orange;
    
    // Enable zooming
    mapsControl.ZoomFactor = 1.0f;
    mapsControl.ZoomLevel = 1;
    
    // Subscribe to events
    mapsControl.ShapeSelected += MapsControl_ShapeSelected;
    
    mapsControl.Layers.Add(shapeLayer);
}

private void MapsControl_ShapeSelected(object sender, ShapeSelectedEventArgs e)
{
    if (e.Data != null)
    {
        foreach (Country country in e.Data)
        {
            Console.WriteLine($"Selected: {country.Country}");
        }
    }
}
```

## Key Properties

### Maps Control Properties

| Property | Type | Description |
|----------|------|-------------|
| `Layers` | LayerCollection | Collection of ShapeFileLayers |
| `MapBackgroundBrush` | Brush | Background color of the map |
| `MapItemsShape` | MapItemShapes | Shape of map items (Circle, Diamond, etc.) |
| `ZoomFactor` | float | Zoom level factor |
| `ZoomLevel` | int | Zoom level multiplier |
| `SelectedMapShapes` | Collection | Currently selected shapes |

### ShapeFileLayer Properties

| Property | Type | Description |
|----------|------|-------------|
| `Uri` | string | Path to shape file (.shp) |
| `ItemSource` | object | Data source for binding |
| `ShapeIDPath` | string | Property name in data model |
| `ShapeIDTableField` | string | Column name in .dbf file |
| `ShowToolTip` | bool | Enable/disable tooltips |
| `EnableSelection` | bool | Enable/disable selection |
| `SelectionMode` | SelectionModes | Single or Multiple selection |
| `ShowLegend` | bool | Show/hide legend |
| `LayoutType` | LayoutType | Default or Tile layout |
| `SubShapeFileLayers` | Collection | Additional shape layers |

### ShapeSetting Properties

| Property | Type | Description |
|----------|------|-------------|
| `ShapeFill` | string/Color | Fill color for shapes |
| `ShapeStroke` | string/Color | Stroke color for shapes |
| `ShapeStrokeThickness` | double | Border thickness |
| `ShapeValuePath` | string | Property for value binding |
| `ShapeColorValuePath` | string | Property for color mapping |
| `SelectedShapeColor` | Color | Color for selected shapes |

### BubbleSetting Properties

| Property | Type | Description |
|----------|------|-------------|
| `AutoFillColors` | bool | Auto-generate bubble colors |
| `MaxSize` | double | Maximum bubble size |
| `MinSize` | double | Minimum bubble size |
| `ValuePath` | string | Property for bubble size |
| `ColorValuePath` | string | Property for bubble color |
| `ColorMappings` | Collection | Range-based color mappings |

## Common Use Cases

### Use Case 1: Population Density Map
Display world population by country with color-coded regions based on population ranges.

### Use Case 2: Sales Territory Map
Visualize sales data by region with bubbles representing sales volume and colors indicating performance tiers.

### Use Case 3: Election Results Map
Show election results by state/province with color-coded winners and tooltips displaying vote counts.

### Use Case 4: Regional Analytics Dashboard
Create a dashboard with multiple map layers showing different data dimensions (demographics, economic indicators, etc.).

### Use Case 5: Location-Based Application
Build a desktop application that highlights specific locations with custom annotations and allows users to interact with map regions.

## Troubleshooting

**Issue: Shape files not loading**
- Verify files are added as **Embedded Resources**
- Check that Uri matches the shape file name exactly
- Ensure .dbf file is included with .shp file

**Issue: Data not binding to shapes**
- Confirm ShapeIDPath matches property in data model
- Verify ShapeIDTableField matches column in .dbf file
- Check that values match exactly (case-sensitive)

**Issue: Colors not displaying correctly**
- Set `AutoFillColors = false` when using ColorMappings
- Ensure color ranges cover all data values
- Verify ColorValuePath points to correct property

**Issue: Selection not working**
- Set `EnableSelection = true`
- Configure `SelectionMode` (Single or Multiple)
- Ensure shapes have bound data for selection