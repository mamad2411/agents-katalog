---
name: syncfusion-aspnetcore-maps
description: Implement Syncfusion Maps component for ASP.NET Core to visualize geographical data. Use this when working with maps, GeoJSON files, choropleth visualizations, or spatial data display. This skill covers map layers, markers, bubbles, map providers (Bing Maps, Azure Maps, OpenStreetMap), data binding, color mapping, and user interactions like zooming and panning. Suitable for world maps, country maps, regional visualizations, and location-based data presentation.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
  platform: "ASP.NET Core"
---

# Implementing Syncfusion Maps for ASP.NET Core

The Syncfusion Maps component is a powerful tool for visualizing geographical data using Scalable Vector Graphics (SVG). It supports GeoJSON data, multiple layers, map providers (Bing, Azure, OpenStreetMap), and rich interactive features like zooming, panning, tooltips, and selection.

## When to Use This Skill

Use the Syncfusion Maps component when you need to:

- **Visualize geographical data** - Display country, state, or regional data on interactive maps
- **Create choropleth maps** - Show data distribution using color mapping across regions
- **Plot location markers** - Display points of interest, offices, stores, or custom locations
- **Render bubble maps** - Visualize quantitative data with size-based bubbles on geographical locations
- **Integrate map providers** - Use Bing Maps, Azure Maps, or OpenStreetMap as base layers
- **Show custom shapes** - Render custom GeoJSON shapes for specific regions or areas
- **Build interactive dashboards** - Create zoomable, pannable maps with tooltips and selection
- **Display navigation routes** - Show navigation lines connecting different locations
- **Overlay annotations** - Add custom HTML/text annotations on maps
- **Create multi-layer visualizations** - Combine multiple data layers on a single map

## Component Overview

**Key Capabilities:**

- 📍 **Multiple Layers** - Support for unlimited layers and sublayers with independent configuration
- 🗺️ **GeoJSON Support** - Load and render custom geographical shapes
- 🌐 **Map Providers** - Integration with Bing Maps, Azure Maps, and OpenStreetMap
- 🎨 **Color Mapping** - Visualize data with equal, range, and desaturation color schemes
- 📌 **Markers & Bubbles** - Plot locations with customizable markers and size-based bubbles
- 🏷️ **Data Labels** - Display shape names and data values with smart positioning
- 🎯 **Interactivity** - Zoom, pan, tooltip, selection, and highlight features
- 📊 **Legend** - Interactive legends for color mapping, markers, and bubbles
- ✏️ **Annotations** - Custom HTML overlays at specific coordinates
- 🌍 **Projections** - Support for 6 map projection types
- 🖨️ **Export** - Print and export maps to PNG, JPEG, SVG, PDF formats
- ♿ **Accessibility** - WCAG compliant with keyboard navigation and screen reader support

## Documentation and Navigation Guide

### Getting Started and Installation

📄 **Read:** [references/getting-started.md](references/getting-started.md)

When user needs to:
- Set up the Maps component for the first time
- Install NuGet packages and configure dependencies
- Add tag helpers and script references
- Create a basic map with GeoJSON data
- Understand the minimal setup requirements

### Layers and GeoJSON Data

📄 **Read:** [references/layers-and-geojson.md](references/layers-and-geojson.md)

When user needs to:
- Understand map layer architecture
- Work with GeoJSON format and custom shapes
- Add multiple layers or sublayers
- Load GeoJSON from files or URLs
- Configure layer visibility and ordering
- Handle layer-specific settings

### Data Binding and Population

📄 **Read:** [references/data-binding.md](references/data-binding.md)

When user needs to:
- Bind data source to map shapes
- Configure ShapeDataPath and ShapePropertyPath
- Match data records to geographical shapes
- Bind data from JSON, databases, or APIs
- Update data dynamically
- Transform data for visualization

### Markers

📄 **Read:** [references/markers.md](references/markers.md)

When user needs to:
- Add location markers to maps
- Use different marker types (Circle, Image, Letter, Template)
- Customize marker appearance (size, color, borders)
- Position markers using latitude/longitude
- Add marker tooltips and events
- Implement marker clustering
- Create custom marker templates

### Bubbles

📄 **Read:** [references/bubbles.md](references/bubbles.md)

When user needs to:
- Create bubble visualizations on maps
- Size bubbles based on data values
- Configure bubble colors and opacity
- Set minimum and maximum bubble radius
- Add bubble tooltips
- Implement multiple bubble sets
- Handle bubble selection

### Data Labels

📄 **Read:** [references/data-labels.md](references/data-labels.md)

When user needs to:
- Display labels on map shapes
- Configure label positioning and alignment
- Use smart label modes (Trim, Hide, None)
- Customize label fonts and styling
- Create template-based labels
- Handle label intersections
- Add labels to markers and bubbles

### Color Mapping

📄 **Read:** [references/color-mapping.md](references/color-mapping.md)

When user needs to:
- Apply colors to shapes based on data
- Configure equal color mapping (value-to-color)
- Set up range color mapping (min-max ranges)
- Use desaturation color mapping (gradient opacity)
- Create choropleth maps
- Define custom color palettes
- Handle accessibility and contrast

### Legend

📄 **Read:** [references/legend.md](references/legend.md)

When user needs to:
- Add legend to maps
- Configure legend positioning and alignment
- Enable interactive legend (toggle, highlight)
- Customize legend shapes and text
- Create legends for color mapping
- Add legends for markers and bubbles
- Implement legend paging for many items

### Annotations

📄 **Read:** [references/annotations.md](references/annotations.md)

When user needs to:
- Add custom HTML content to maps
- Position annotations at specific coordinates
- Create text or template-based annotations
- Style and align annotations
- Handle annotation z-index and layering
- Add dynamic annotations
- Create responsive annotations

### User Interactions

📄 **Read:** [references/user-interactions.md](references/user-interactions.md)

When user needs to:
- Enable zooming (mouse wheel, pinch, toolbar)
- Configure panning features
- Add tooltips with custom templates
- Implement shape selection and multi-selection
- Enable highlight on hover
- Handle click events
- Add navigation lines between locations
- Set zoom levels and constraints

### Map Providers Integration

📄 **Read:** [references/map-providers.md](references/map-providers.md)

When user needs to:
- Integrate Bing Maps (Road, Aerial, Hybrid)
- Set up Azure Maps with API keys
- Use OpenStreetMap (OSM) tiles
- Configure custom tile servers
- Combine providers with GeoJSON layers
- Handle provider authentication
- Compare provider features and limitations

### Advanced Features

When user needs to:
- Render polygons with custom data
- Add navigation lines with arrows
- Print or export maps to images/PDF
- Implement internationalization (i18n)
- Configure localization (l10n)
- Enable accessibility features
- Implement state persistence
- Use programmatic methods
- Optimize performance
- Migrate from EJ1 to EJ2

## Quick Start Example

### Basic Map with GeoJSON and Color Mapping

```cshtml
@using Newtonsoft.Json
@using Syncfusion.EJ2.Maps

@{
    // Load GeoJSON data
    string geoJson = System.IO.File.ReadAllText("wwwroot/scripts/MapsData/WorldMap.json");
    var worldMapData = JsonConvert.DeserializeObject(geoJson);
    
    // Load data source
    string dataJson = System.IO.File.ReadAllText("wwwroot/scripts/MapsData/population.json");
    var populationData = JsonConvert.DeserializeObject(dataJson);
    
    // Define color mapping
    var colorMapping = new List<MapsColorMapping> {
        new MapsColorMapping { From = 0, To = 100000000, Color = "#C6E7F0", Label = "< 100M" },
        new MapsColorMapping { From = 100000000, To = 500000000, Color = "#6AB7D6", Label = "100M - 500M" },
        new MapsColorMapping { From = 500000000, To = 1500000000, Color = "#1A7FA0", Label = "> 500M" }
    };
    
    var propertyPath = new[] { "name" };
}

<ejs-maps id="maps" height="600px">
    <e-maps-titlesettings text="World Population by Country">
        <e-maps-titlesettings-textstyle size="16px" fontWeight="500"></e-maps-titlesettings-textstyle>
    </e-maps-titlesettings>
    
    <e-maps-legendsettings visible="true" position="Bottom"></e-maps-legendsettings>
    
    <e-maps-layers>
        <e-maps-layer shapeData="worldMapData" 
                      dataSource="populationData"
                      shapeDataPath="Country" 
                      shapePropertyPath="propertyPath">
            <e-layersettings-shapesettings 
                fill="#E5E5E5" 
                colorValuePath="Population"
                colorMapping="colorMapping">
            </e-layersettings-shapesettings>
            
            <e-layersettings-tooltipsettings visible="true" valuePath="Country">
                <e-tooltipsettings-template>
                    <div style="padding: 8px;">
                        <strong>${Country}</strong><br/>
                        Population: ${Population}
                    </div>
                </e-tooltipsettings-template>
            </e-layersettings-tooltipsettings>
        </e-maps-layer>
    </e-maps-layers>
</ejs-maps>
```

### Map with Markers

```cshtml
@using Newtonsoft.Json
@using Syncfusion.EJ2.Maps

@{
    var worldMapData = JsonConvert.DeserializeObject(System.IO.File.ReadAllText("wwwroot/scripts/MapsData/WorldMap.json"));
    
    var cities = new[]
    {
        new { Name = "New York", Latitude = 40.7128, Longitude = -74.0060, Population = "8.4M" },
        new { Name = "Tokyo", Latitude = 35.6762, Longitude = 139.6503, Population = "13.9M" },
        new { Name = "London", Latitude = 51.5074, Longitude = -0.1278, Population = "9.0M" },
        new { Name = "Sydney", Latitude = -33.8688, Longitude = 151.2093, Population = "5.3M" }
    };
}

<ejs-maps id="maps" height="600px">
    <e-maps-zoomsettings enable="true" zoomFactor="2"></e-maps-zoomsettings>
    
    <e-maps-layers>
        <e-maps-layer shapeData="worldMapData">
            <e-layersettings-shapesettings fill="#C3E6ED"></e-layersettings-shapesettings>
            
            <e-layersettings-markersettings>
                <e-layersettings-markersetting 
                    visible="true" 
                    dataSource="cities"
                    shape="Circle"
                    fill="#FF6347"
                    height="15"
                    width="15">
                    <e-layersettings-markersetting-tooltipsettings 
                        visible="true" 
                        valuePath="Name">
                        <e-markersetting-tooltipsettings-template>
                            <div style="padding: 8px;">
                                <strong>${Name}</strong><br/>
                                Population: ${Population}
                            </div>
                        </e-markersetting-tooltipsettings-template>
                    </e-layersettings-markersetting-tooltipsettings>
                </e-layersettings-markersetting>
            </e-layersettings-markersettings>
        </e-maps-layer>
    </e-maps-layers>
</ejs-maps>
```

## API Reference

### Maps Class

The primary Maps component class with properties, methods, and events for controlling map behavior and appearance.

**Namespace:** `Syncfusion.EJ2.Maps`  
**Assembly:** `Syncfusion.EJ2.dll`  
**[Official API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html)**

#### Core Properties (63 total)

| Property | Type | Default | Description | [API Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html) |
|----------|------|---------|-------------|----------|
| AllowImageExport | bool | false | Enables or disables the export to image (PNG, JPEG, SVG) functionality in maps | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_AllowImageExport) |
| AllowPdfExport | bool | false | Enables or disables the export to PDF functionality in maps | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_AllowPdfExport) |
| AllowPrint | bool | false | Enables or disables the print functionality in maps | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_AllowPrint) |
| Annotations | List<MapsAnnotation> | null | Gets or sets the options for customizing the annotations in the maps. Annotations allow custom HTML/text overlays at specific coordinates | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Annotations) |
| Background | string | null | Gets or sets the background color of the maps container | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Background) |
| BaseLayerIndex | double | 0 | Gets or sets the index of the layer which will be the base layer. Determines which layer is visible in the maps | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_BaseLayerIndex) |
| Border | MapsBorder | null | Gets or sets the options for customizing the style properties of the maps border (width, color) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Border) |
| CenterPosition | MapsCenterPosition | null | Gets or sets the center position of the maps using latitude and longitude coordinates | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_CenterPosition) |
| Description | string | null | Gets or sets the description of the maps for assistive technology and accessibility | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Description) |
| EnablePersistence | bool | false | Enable or disable persisting component's state between page reloads. Maintains zoom level, pan position, etc. | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_EnablePersistence) |
| EnableRtl | bool | false | Enable or disable rendering component in right to left direction for RTL languages | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_EnableRtl) |
| Format | string | null | Gets or sets the format to apply internationalization for the text in the maps | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Format) |
| Height | string | null | Gets or sets the height in which the maps is to be rendered. Can be percentage or pixel value | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Height) |
| HtmlAttributes | object | null | Allows additional HTML attributes such as title, name, data-*, etc. in key-value pair format | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_HtmlAttributes) |
| Layers | List<MapsLayer> | null | Gets or sets the options to customize the layers of the maps. Supports unlimited layers and sublayers | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Layers) |
| LegendSettings | MapsLegendSettings | null | Gets or sets the options to customize the legend of the maps (position, alignment, visibility, etc.) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_LegendSettings) |
| Locale | string | "en-US" | Overrides the global culture and localization value for this component | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Locale) |
| MapsArea | MapsMapsAreaSettings | null | Gets or sets the options to customize the area around the map (background, border) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_MapsArea) |
| Margin | MapsMargin | null | Gets or sets the options to customize the margin of the maps (top, bottom, left, right) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Margin) |
| ProjectionType | ProjectionType | Mercator | Gets or sets the projection type (Mercator, EquirectangularProjection, MercatorProjection, etc.) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_ProjectionType) |
| TabIndex | double | 0 | Gets or sets the tab index value for the maps | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_TabIndex) |
| Theme | MapsTheme | Material | Gets or sets the theme styles supported for maps (Material, Fabric, HighContrast, BootstrapDark, etc.) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Theme) |
| TitleSettings | MapsTitleSettings | null | Gets or sets the options to customize the title of the maps (text, alignment, font, etc.) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_TitleSettings) |
| TooltipDisplayMode | TooltipGesture | MouseMove | Gets or sets the mode in which the tooltip is displayed (MouseMove, Click, DoubleClick) | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_TooltipDisplayMode) |
| UseGroupingSeparator | bool | false | Enables or disables the visibility state of the separator for grouping in formatted numbers | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_UseGroupingSeparator) |
| Width | string | null | Gets or sets the width in which the maps is to be rendered. Can be percentage or pixel value | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_Width) |
| ZoomSettings | MapsZoomSettings | null | Gets or sets the options to customize the zooming operations in maps | [Learn More](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.Maps.html#Syncfusion_EJ2_Maps_Maps_ZoomSettings) |

#### Maps Events (28 total)

| Event | Type | Trigger Condition | Description |
|-------|------|-------------------|-------------|
| AnimationComplete | string | null | Triggers after the animation is completed in the maps |
| AnnotationRendering | string | null | Triggers before rendering an annotation in the maps |
| BeforePrint | string | null | Triggers before the print gets started |
| BubbleClick | string | null | Triggers when performing the click operation on the bubble element in maps |
| BubbleMouseMove | string | null | Triggers when hovering the mouse on the bubble element in maps |
| BubbleRendering | string | null | Triggers before the bubble element gets rendered on the map |
| Click | string | null | Triggers when a user clicks on an element in Maps |
| DataLabelRendering | string | null | Triggers before the data-label gets rendered |
| DoubleClick | string | null | Triggers when performing the double click operation on an element in maps |
| ItemHighlight | string | null | Trigger before the shape, bubble or marker gets highlighted |
| ItemSelection | string | null | Triggers before the shape, bubble or marker gets selected |
| LayerRendering | string | null | Triggers before the maps layer gets rendered |
| LegendRendering | string | null | Triggers before the legend gets rendered |
| Load | string | null | Triggers before the maps gets rendered |
| Loaded | string | null | Triggers after the maps gets rendered |
| MarkerClick | string | null | Triggers when clicking on a marker element |
| MarkerClusterClick | string | null | Triggers when clicking the marker cluster in maps |
| MarkerClusterMouseMove | string | null | Triggers when moving the mouse over the marker cluster element |
| MarkerClusterRendering | string | null | Triggers before the maps marker cluster gets rendered |
| MarkerDragEnd | string | null | When the marker has stopped dragging on the map, this event is triggered |
| MarkerDragStart | string | null | When the marker begins to drag on the map, this event is triggered |
| MarkerMouseMove | string | null | Triggers when moving the mouse over the marker element in maps |
| MarkerRendering | string | null | Triggers before the maps marker gets rendered |
| MouseMove | string | null | This event is triggered when the mouse pointer moves over the map |
| Pan | string | null | Triggers before performing the panning operation |
| PanComplete | string | null | This event is triggered after performing the panning action |
| Resize | string | null | Triggers to notify the resize of the maps when the window is resized |
| RightClick | string | null | Triggers when performing the right click operation on an element in maps |
| ShapeHighlight | string | null | Triggers before the shape gets highlighted |
| ShapeRendering | string | null | Triggers before the maps shape gets rendered |
| ShapeSelected | string | null | Triggers when a shape is selected in the maps |
| TooltipRender | string | null | Triggers before the maps tooltip gets rendered |
| TooltipRenderComplete | string | null | Triggers after the maps tooltip gets rendered |
| Zoom | string | null | Triggers before the zoom operations such as zoom in and zoom out |
| ZoomComplete | string | null | This event is triggered after the zooming operation is completed |

### MapsLayer Class

Defines the configuration for individual map layers supporting geometry data, map providers, and data binding.

**[Official API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsLayer.html)**

#### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| DataSource | object | null | Data source for binding with shapes |
| ShapeData | object | null | GeoJSON data for rendering the shapes |
| ShapeDataPath | string | null | Property path in the data source to match with shapes |
| ShapePropertyPath | string[] | null | Property path in the shape data to match with data source |
| BubbleSettings | List<MapsBubble> | null | Configuration for bubble visualization |
| MarkerSettings | List<MapsMarker> | null | Configuration for marker visualization |
| DataLabelSettings | MapsDataLabelSettings | null | Configuration for data labels on shapes |
| NavigationLineSettings | List<MapsNavigationLine> | null | Configuration for navigation lines |
| SelectionSettings | MapsSelectionSettings | null | Configuration for shape selection |
| HighlightSettings | MapsHighlightSettings | null | Configuration for shape highlighting on hover |
| TooltipSettings | MapsTooltipSettings | null | Configuration for layer tooltips |
| ShapeSettings | MapsShapeSettings | null | Configuration for shape styling |
| Type | string | "Layer" | Layer type (Layer or SubLayer) |
| Visible | bool | true | Gets or sets the visibility of the layer |

### MapsZoomSettings Class

Manages map zoom and pan behavior.

**[Official API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsZoomSettings.html)**

#### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| Enable | bool | false | Enables or disables zooming in maps |
| ToolbarOrientation | string | "Vertical" | Specifies the orientation of zoom toolbar (Horizontal/Vertical) |
| Toolbars | string[] | null | Defines zoom toolbar buttons (Zoom, ZoomIn, ZoomOut, Pan, Reset) |
| ZoomFactor | double | 2 | Zoom factor for each zoom in or zoom out |
| MinZoom | double | 1 | Minimum zoom level |
| MaxZoom | double | 28 | Maximum zoom level |
| EnableMouseWheelZoom | bool | false | Enable zooming using mouse wheel |
| EnablePinchZoom | bool | false | Enable zooming using pinch gesture on touch devices |
| EnableSelectionZooming | bool | false | Enable zooming by selection (draw box to zoom) |
| EnableDoubleTapZoom | bool | true | Enable zooming on double tap |

### MapsShapeSettings Class

Configures appearance and behavior of shapes in the map.

**[Official API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsShapeSettings.html)**

#### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| Fill | string | "#E5E5E5" | Color to fill the shapes |
| Opacity | double | 1.0 | Opacity of shapes (0 to 1) |
| Palette | string[] | null | Color palette for color mapping |
| ColorValuePath | string | null | Property path in data source for color mapping |
| ColorMapping | List<MapsColorMapping> | null | Color mapping configuration |
| DashArray | string | "" | Defines dash pattern for shape borders |

### MapsMarker Class

Defines markers to be displayed on the map at specified coordinates.

**[Official API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsMarker.html)**

#### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| DataSource | object | null | Data source containing marker locations and properties |
| Latitude | double | null | Latitude coordinate for marker placement |
| Longitude | double | null | Longitude coordinate for marker placement |
| Shape | MarkerType | Circle | Marker shape (Circle, Rectangle, Image, Letter, Template) |
| Width | double | 20 | Width of the marker |
| Height | double | 20 | Height of the marker |
| Fill | string | "#F41747" | Fill color of the marker |
| Border | string | null | Border configuration |
| ImageUrl | string | null | Image URL for image type markers |
| TooltipSettings | MapsTooltipSettings | null | Tooltip configuration for markers |

### Related Classes (40+ classes available)

| Class | Purpose | API Link |
|-------|---------|----------|
| MapsLegendSettings | Configure and customize legend | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsLegendSettings.html) |
| MapsTooltipSettings | Configure tooltip behavior | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsTooltipSettings.html) |
| MapsBubble | Bubble visualization settings | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsBubble.html) |
| MapsColorMapping | Define color mapping rules | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsColorMapping.html) |
| MapsDataLabelSettings | Data label customization | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsDataLabelSettings.html) |
| MapsAnnotation | Annotation configuration | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsAnnotation.html) |
| MapsNavigationLine | Navigation line settings | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsNavigationLine.html) |
| MapsMarkerClusterSettings | Marker clustering configuration | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsMarkerClusterSettings.html) |
| MapsTitleSettings | Map title customization | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsTitleSettings.html) |
| MapsMargin | Margin configuration | [Link](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.MapsMargin.html) |

### Enumerations

#### ProjectionType

Defines supported map projections.

| Value | Description |
|-------|-------------|
| Mercator | Web Mercator projection (default) |
| EquirectangularProjection | Equirectangular/Plate Carée projection |
| MercatorProjection | Mercator projection |
| Miller | Miller cylindrical projection |
| NaturalEarth1 | Natural Earth 1 projection |
| NaturalEarth2 | Natural Earth 2 projection |

#### MarkerType

Defines available marker shapes.

| Value | Description |
|-------|-------------|
| Circle | Circular marker |
| Rectangle | Rectangular marker |
| Triangle | Triangular marker |
| Diamond | Diamond-shaped marker |
| Image | Custom image marker |
| Letter | Letter-based marker |
| Template | Custom template marker |

#### MapsTheme

Defines available themes.

| Value | Description |
|-------|-------------|
| Material | Material design theme |
| Fabric | Fabric design theme |
| HighContrast | High contrast theme |
| BootstrapDark | Bootstrap dark theme |
| BootstrapLight | Bootstrap light theme |

#### TooltipGesture

Defines tooltip display modes.

| Value | Description |
|-------|-------------|
| MouseMove | Display on mouse move (default) |
| Click | Display on click |
| DoubleClick | Display on double click |

#### LegendType

Defines legend types.

| Value | Description |
|-------|-------------|
| Layers | Legend for layers |
| Markers | Legend for markers |
| Bubbles | Legend for bubbles |

## Common Patterns

### Pattern 1: Choropleth Map with Data Binding

**Use Case:** Visualize statistical data across regions with color-coded shapes.

```cshtml
@{
    var colorMapping = new List<MapsColorMapping> {
        new MapsColorMapping { Value = "Low", Color = "#90EE90" },
        new MapsColorMapping { Value = "Medium", Color = "#FFD700" },
        new MapsColorMapping { Value = "High", Color = "#FF6347" }
    };
}

<e-maps-layer shapeData="@geoJsonData" 
              dataSource="@statisticsData"
              shapeDataPath="RegionName" 
              shapePropertyPath="@(new[] { "name" })">
    <e-layersettings-shapesettings 
        colorValuePath="DataLevel"
        colorMapping="colorMapping">
    </e-layersettings-shapesettings>
</e-maps-layer>
```

### Pattern 2: Interactive Map with Zoom and Selection

**Use Case:** Enable user interaction for detailed exploration.

```cshtml
<ejs-maps id="maps">
    <e-maps-zoomsettings 
        enable="true" 
        enableSelectionZooming="true"
        toolbars='new string[] {"Zoom", "ZoomIn", "ZoomOut", "Pan", "Reset"}'>
    </e-maps-zoomsettings>
    
    <e-maps-layers>
        <e-maps-layer shapeData="@mapData">
            <e-layersettings-selectionsettings 
                enable="true" 
                fill="#8B0000"
                opacity="0.5">
            </e-layersettings-selectionsettings>
            
            <e-layersettings-highlightsettings 
                enable="true" 
                fill="#FF6347">
            </e-layersettings-highlightsettings>
        </e-maps-layer>
    </e-maps-layers>
</ejs-maps>
```

### Pattern 3: Multiple Data Layers

**Use Case:** Overlay multiple data sets on a single map.

```cshtml
<e-maps-layers>
    <!-- Base layer: Country boundaries -->
    <e-maps-layer shapeData="@countryData" type="Layer">
        <e-layersettings-shapesettings fill="#E5E5E5"></e-layersettings-shapesettings>
    </e-maps-layer>
    
    <!-- Sublayer: State boundaries -->
    <e-maps-layer shapeData="@stateData" type="SubLayer">
        <e-layersettings-shapesettings fill="transparent" border-width="1"></e-layersettings-shapesettings>
    </e-maps-layer>
    
    <!-- Data layer: Markers -->
    <e-maps-layer type="Layer">
        <e-layersettings-markersettings>
            <e-layersettings-markersetting dataSource="@locations" shape="Circle"></e-layersettings-markersetting>
        </e-layersettings-markersettings>
    </e-maps-layer>
</e-maps-layers>
```

### Pattern 4: Bing Maps Integration

**Use Case:** Use Bing Maps as base layer with custom data overlay.

```cshtml
<ejs-maps id="maps">
    <e-maps-layers>
        <!-- Bing Maps base layer -->
        <e-maps-layer layerType="Bing" bingMapType="Aerial" key="YOUR_BING_MAPS_KEY">
        </e-maps-layer>
        
        <!-- Data overlay layer -->
        <e-maps-layer type="SubLayer" shapeData="@customData">
            <e-layersettings-shapesettings fill="#FF6347" opacity="0.5"></e-layersettings-shapesettings>
        </e-maps-layer>
    </e-maps-layers>
</ejs-maps>
```

## Key Properties Reference

### Essential Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `shapeData` | GeoJSON data for rendering shapes | `shapeData="worldMapData"` |
| `dataSource` | Data to bind to shapes | `dataSource="populationData"` |
| `shapeDataPath` | Property in dataSource to match shapes | `shapeDataPath="Country"` |
| `shapePropertyPath` | Property in GeoJSON to match data | `shapePropertyPath="@(new[] { "name" })"` |
| `colorValuePath` | Data property for color mapping | `colorValuePath="Population"` |
| `colorMapping` | Define color ranges/values | `colorMapping="@colorMappingList"` |

### Layer Configuration

| Property | Purpose | Common Values |
|----------|---------|---------------|
| `type` | Layer type | `Layer`, `SubLayer` |
| `layerType` | Provider type | `Geometry`, `Bing`, `OSM` |
| `visible` | Show/hide layer | `true`, `false` |
| `shapeSettings` | Shape styling | Fill, border, palette |
| `markerSettings` | Marker configuration | Shape, size, color |
| `bubbleSettings` | Bubble configuration | Size, color, radius |

### Interaction Settings

| Property | Purpose | Configuration |
|----------|---------|---------------|
| `zoomSettings` | Zoom configuration | `enable`, `zoomFactor`, `minZoom`, `maxZoom` |
| `tooltipSettings` | Tooltip configuration | `visible`, `valuePath`, `template` |
| `selectionSettings` | Selection configuration | `enable`, `fill`, `opacity` |
| `highlightSettings` | Hover highlight | `enable`, `fill`, `border` |

## Common Use Cases

### Use Case 1: Sales Dashboard by Region

Create a choropleth map showing sales performance across different regions with color-coded intensity.

**Applies:** Color mapping, data binding, legend, tooltips

### Use Case 2: Store Locator

Display retail store locations on a map with custom markers, allowing users to zoom and click for details.

**Applies:** Markers, tooltips, zooming, Bing/OSM integration

### Use Case 3: Population Density Visualization

Show population density using bubble sizes, with larger bubbles representing higher populations.

**Applies:** Bubbles, data binding, legend, color mapping

### Use Case 4: Election Results Map

Visualize election results by state/region with color coding and interactive selection.

**Applies:** Color mapping, selection, highlight, data labels, legend

### Use Case 5: Shipping Routes Visualization

Display shipping routes between cities using navigation lines with directional arrows.

**Applies:** Navigation lines, markers, annotations, layers

### Use Case 6: Weather Map Dashboard

Overlay weather data on maps with custom annotations and real-time data updates.

**Applies:** Annotations, dynamic data, multiple layers, map providers

### Use Case 7: Real Estate Property Map

Show property listings with custom markers, filtering, and detailed tooltips.

**Applies:** Markers, custom templates, tooltips, zooming, panning

## Related Components

- **Chart** - For non-geographical data visualization
- **HeatMap** - For matrix-based heat map visualization
- **TreeMap** - For hierarchical data visualization
- **Diagram** - For network and flowchart visualization

## Additional Resources

- [Syncfusion Maps Documentation](https://ej2.syncfusion.com/aspnetcore/documentation/maps/getting-started)
- [API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Maps.html)
- [GeoJSON Format Specification](https://geojson.org/)
- [Sample GeoJSON Data](https://www.syncfusion.com/downloads/support/directtrac/general/ze/WorldMap-637657487)
