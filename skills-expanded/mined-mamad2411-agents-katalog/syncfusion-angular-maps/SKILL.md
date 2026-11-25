---
name: syncfusion-angular-maps
description: Implement Syncfusion Angular Maps component for geographical data visualization. Use this when users need to display maps, visualize geographical data with markers and bubbles, integrate map providers like Bing or OpenStreetMap, render GeoJSON shapes, or create choropleth maps with color-coded regions. Supports interactive features like zooming, panning, layers, legends, tooltips, color mapping, and accessibility.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Maps

Comprehensive guide for implementing the Syncfusion Angular Maps component to visualize geographical data with interactive features, multiple layers, and rich customization options.

## When to Use This Skill

Use this skill when you need to:

- **Visualize geographical data** - Display statistical data on world maps, country maps, regional maps, or custom geographic shapes
- **Create interactive maps** - Build maps with zoom, pan, selection, highlighting, and tooltip interactions
- **Plot locations** - Add markers, bubbles, or annotations to highlight specific geographic points
- **Display map layers** - Work with multiple overlapping layers using GeoJSON data or map providers (Bing, OpenStreetMap, Azure)
- **Color-code regions** - Apply color mapping based on data values for choropleth/heat map visualizations
- **Custom map visualizations** - Create non-geographic visualizations like seat layouts, floor plans, or stadium maps
- **Navigation and routing** - Draw navigation lines or routes between markers
- **Export and print maps** - Generate printable or exportable map visualizations
- **Build dashboards** - Integrate maps into Angular applications for business intelligence or analytics

## Component Overview

The Syncfusion Angular Maps component (`@syncfusion/ej2-angular-maps`) is a powerful data visualization tool that renders geographical data using Scalable Vector Graphics (SVG). It supports:

- **Multiple layers and sublayers** for complex visualizations
- **GeoJSON data binding** for custom shapes and regions
- **Map providers** (Bing Maps, OpenStreetMap, Azure Maps) as base layers
- **Six projection types** (Mercator, Equirectangular, Miller, Eckert3, Eckert5, Eckert6, Winkel3, AitOff)
- **Rich visualization elements** - markers, bubbles, data labels, legends, navigation lines, annotations
- **Interactive features** - zooming, panning, tooltips, selection, highlighting
- **Responsive and accessible** design with WCAG compliance

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

When implementing Maps for the first time or setting up a new Angular project:
- Installing dependencies (@syncfusion/ej2-angular-maps package)
- Setting up Angular environment and importing MapsModule
- Creating first basic map with world map data
- Understanding module injection for features (MarkerService, BubbleService, etc.)
- Adding CSS themes and styling
- Running the application

### Layers and Data Binding

📄 **Read:** [references/layers-and-data.md](references/layers-and-data.md)

For working with map layers, shape data, and data source binding:
- Understanding layer structure and configuration
- Loading GeoJSON shape data (shapeData property)
- Binding external data sources (dataSource, shapeDataPath, shapePropertyPath)
- Creating multiple layers and sublayers
- Layer types (base layer vs sublayer)
- Switching between layers (baseLayerIndex)
- Rendering custom shapes for non-geographic visualizations
- GeometryType options (Geographic vs Normal)

### Markers

📄 **Read:** [references/markers.md](references/markers.md)

For adding and customizing location markers:
- Adding markers with latitude/longitude data
- Marker shapes (Balloon, Circle, Cross, Diamond, Image, Rectangle, Star, Triangle)
- Custom marker templates
- Marker styling (size, color, border, opacity)
- Dynamic markers with data binding
- Marker clustering
- Marker animations and transitions
- Marker tooltips and events
- Creating routes between markers

### Data Visualization Features

📄 **Read:** [references/data-visualization.md](references/data-visualization.md)

For visualizing data with bubbles, colors, labels, and legends:
- **Bubbles** - Size-based visualization for quantitative data
- **Color mapping** - Range color mapping, equal color mapping, desaturation color mapping
- **Data labels** - Displaying shape names or data values on the map
- **Legends** - Adding legends for color mapping and bubbles
- **Navigation lines** - Drawing lines between locations
- **Annotations** - Adding custom HTML content at specific positions
- Combining multiple visualization features

### User Interactions

📄 **Read:** [references/user-interactions.md](references/user-interactions.md)

For implementing interactive map behaviors:
- **Zooming** - Mouse wheel zoom, pinch zoom, double-click zoom, zoom toolbar
- **Panning** - Mouse drag and touch panning
- **Tooltips** - Layer tooltips, marker tooltips, bubble tooltips
- **Selection** - Shape selection, marker selection, bubble selection
- **Highlighting** - Hover highlight effects
- **Interactive legend** - Clicking legend items to show/hide shapes
- Event handling (click, hover, zoom, pan events)
- Touch and mobile support

### Map Providers

📄 **Read:** [references/map-providers.md](references/map-providers.md)

For integrating external map services:
- Overview of map provider support
- **Bing Maps** integration and API key configuration
- **OpenStreetMap** (OSM) integration
- **Azure Maps** integration
- Provider-specific features and limitations
- Combining map providers with shape layers
- URL templates and tile services
- Zoom level configuration

### Polygon Shapes

📄 **Read:** [references/polygon-shapes.md](references/polygon-shapes.md)

For drawing and customizing polygons:
- Adding polygon overlays to maps
- Polygon configuration and data structure
- Styling polygons (fill, border, opacity)
- Polygon events (click, hover)
- Use cases (highlighting regions, boundaries, zones)
- Dynamic polygon rendering

### Customization and Styling

📄 **Read:** [references/customization.md](references/customization.md)

For theming and visual customization:
- Built-in themes (Material, Bootstrap, Fabric, Tailwind, etc.)
- CSS customization and theme overrides
- Shape styling (fill, border, color schemes)
- Responsive design patterns
- **Map projections** - Choosing and configuring projection types
- Background customization (colors, images)
- Title and subtitle styling
- Border and margin configuration

### Localization and Internationalization

📄 **Read:** [references/localization.md](references/localization.md)

For globalizing map content:
- Internationalization (i18n) setup
- Localization (l10n) for different languages
- Right-to-left (RTL) support
- Number formatting for different locales
- Currency formatting in tooltips/labels
- Date and time formatting
- Culture-specific rendering

### Advanced Features

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

For advanced capabilities and APIs:
- **Print and Export** - Printing maps, exporting to PNG/JPEG/SVG/PDF
- **State persistence** - Saving and restoring map state
- **Public methods** - Programmatic control (refresh, print, export, etc.)
- **Events reference** - Complete list of available events
- **Creating routes** - Drawing navigation routes between markers
- **Custom path rendering** - Advanced path and line customization
- **Drilldown navigation** - Creating hierarchical map navigation

### Accessibility

📄 **Read:** [references/accessibility.md](references/accessibility.md)

For accessible map implementations:
- WCAG 2.1 compliance guidelines
- Keyboard navigation support
- ARIA attributes and roles
- Screen reader compatibility
- High contrast theme support
- Focus indicators and management
- Alternative text for shapes and markers

## Quick Start

### Installation

```bash
# Install the Maps package
npm install @syncfusion/ej2-angular-maps --save
```

### Basic Implementation

```typescript
import { Component } from '@angular/core';
import { MapsModule } from '@syncfusion/ej2-angular-maps';
import { world_map } from './world-map'; // GeoJSON data

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MapsModule],
  template: `
    <ejs-maps id='maps-container'>
      <e-layers>
        <e-layer [shapeData]='shapeData'></e-layer>
      </e-layers>
    </ejs-maps>
  `
})
export class AppComponent {
  public shapeData: object = world_map;
}
```

### With Data Binding and Color Mapping

```typescript
import { Component } from '@angular/core';
import { MapsModule } from '@syncfusion/ej2-angular-maps';
import { world_map } from './world-map';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MapsModule],
  template: `
    <ejs-maps id='maps-container'>
      <e-layers>
        <e-layer 
          [shapeData]='shapeData'
          [dataSource]='dataSource'
          shapeDataPath='Country'
          shapePropertyPath='name'
          [shapeSettings]='shapeSettings'>
        </e-layer>
      </e-layers>
    </ejs-maps>
  `
})
export class AppComponent {
  public shapeData: object = world_map;
  
  public dataSource: object[] = [
    { Country: 'United States', Population: 331002651, Code: 'US' },
    { Country: 'India', Population: 1380004385, Code: 'IN' },
    { Country: 'China', Population: 1439323776, Code: 'CN' }
  ];
  
  public shapeSettings: object = {
    colorValuePath: 'Population',
    colorMapping: [
      { from: 0, to: 100000000, color: '#C5E8B7' },
      { from: 100000001, to: 500000000, color: '#5BC85A' },
      { from: 500000001, to: 2000000000, color: '#238B45' }
    ]
  };
}
```

## Common Patterns

### Pattern 1: Map with Markers and Tooltips

```typescript
import { Component } from '@angular/core';
import { MapsModule, MarkerService, MapsTooltipService } from '@syncfusion/ej2-angular-maps';
import { world_map } from './world-map';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MapsModule],
  providers: [MarkerService, MapsTooltipService],
  template: `
    <ejs-maps id='maps-container'>
      <e-layers>
        <e-layer 
          [shapeData]='shapeData'
          [markerSettings]='markerSettings'>
        </e-layer>
      </e-layers>
    </ejs-maps>
  `
})
export class AppComponent {
  public shapeData: object = world_map;
  
  public markerSettings: object[] = [{
    visible: true,
    dataSource: [
      { latitude: 40.7128, longitude: -74.0060, name: 'New York' },
      { latitude: 51.5074, longitude: -0.1278, name: 'London' },
      { latitude: 35.6762, longitude: 139.6503, name: 'Tokyo' }
    ],
    shape: 'Circle',
    fill: '#FF6347',
    height: 15,
    width: 15,
    tooltipSettings: {
      visible: true,
      valuePath: 'name'
    }
  }];
}
```

### Pattern 2: Interactive Map with Zoom and Legend

```typescript
import { Component } from '@angular/core';
import { MapsModule, ZoomService, LegendService } from '@syncfusion/ej2-angular-maps';
import { world_map } from './world-map';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MapsModule],
  providers: [ZoomService, LegendService],
  template: `
    <ejs-maps 
      id='maps-container'
      [zoomSettings]='zoomSettings'
      [legendSettings]='legendSettings'>
      <e-layers>
        <e-layer 
          [shapeData]='shapeData'
          [dataSource]='dataSource'
          shapeDataPath='Country'
          shapePropertyPath='name'
          [shapeSettings]='shapeSettings'>
        </e-layer>
      </e-layers>
    </ejs-maps>
  `
})
export class AppComponent {
  public shapeData: object = world_map;
  
  public dataSource: object[] = [
    { Country: 'United States', Category: 'High' },
    { Country: 'Canada', Category: 'Medium' },
    { Country: 'Mexico', Category: 'Low' }
  ];
  
  public shapeSettings: object = {
    colorValuePath: 'Category',
    colorMapping: [
      { value: 'High', color: '#E74C3C' },
      { value: 'Medium', color: '#F39C12' },
      { value: 'Low', color: '#27AE60' }
    ]
  };
  
  public zoomSettings: object = {
    enable: true,
    toolbars: ['Zoom', 'ZoomIn', 'ZoomOut', 'Pan', 'Reset']
  };
  
  public legendSettings: object = {
    visible: true,
    position: 'Bottom'
  };
}
```

### Pattern 3: Multi-Layer Map with Sublayers

```typescript
import { Component } from '@angular/core';
import { MapsModule } from '@syncfusion/ej2-angular-maps';
import { world_map } from './world-map';
import { usa_map } from './usa-map';
import { california } from './california';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MapsModule],
  template: `
    <ejs-maps id='maps-container'>
      <e-layers>
        <!-- Base layer -->
        <e-layer 
          [shapeData]='usaMap'
          [shapeSettings]='baseShapeSettings'>
        </e-layer>
        
        <!-- Sublayer highlighting California -->
        <e-layer 
          type='SubLayer'
          [shapeData]='californiaMap'
          [shapeSettings]='sublayerShapeSettings'>
        </e-layer>
      </e-layers>
    </ejs-maps>
  `
})
export class AppComponent {
  public usaMap: object = usa_map;
  public californiaMap: object = california;
  
  public baseShapeSettings: object = {
    fill: '#E5E5E5',
    border: { color: '#000000', width: 0.5 }
  };
  
  public sublayerShapeSettings: object = {
    fill: '#FFD700',
    border: { color: '#FF6347', width: 2 }
  };
}
```

## Key Configuration Options

### Layer Settings
- `shapeData` - GeoJSON data for shapes
- `dataSource` - External data to bind
- `shapeDataPath` - Field in dataSource identifying shape
- `shapePropertyPath` - Field in shapeData matching dataSource
- `shapeSettings` - Visual styling for shapes
- `type` - Layer type ('Layer' or 'SubLayer')

### Shape Settings
- `fill` - Shape fill color
- `border` - Border configuration (color, width, opacity)
- `colorValuePath` - Data field for color mapping
- `colorMapping` - Array of color ranges or values
- `autofill` - Auto-generate colors for shapes

### Marker Settings
- `visible` - Show/hide markers
- `dataSource` - Marker data with latitude/longitude
- `shape` - Marker shape type
- `height` / `width` - Marker dimensions
- `template` - Custom HTML template
- `tooltipSettings` - Marker tooltip configuration

### Zoom Settings
- `enable` - Enable/disable zooming
- `zoomFactor` - Initial zoom level
- `maxZoom` / `minZoom` - Zoom limits
- `toolbars` - Zoom control buttons
- `mouseWheelZoom` - Enable mouse wheel zooming
- `pinchZooming` - Enable touch pinch zoom

### Legend Settings
- `visible` - Show/hide legend
- `position` - Legend placement (Top, Bottom, Left, Right)
- `mode` - Legend mode ('Default', 'Interactive')
- `type` - Legend type ('Layers', 'Bubbles', 'Markers')

## Common Use Cases

### Use Case 1: Sales Dashboard by Region
Create choropleth maps showing sales data across countries or states with color-coded regions, interactive tooltips, and legends. Useful for business intelligence dashboards.

### Use Case 2: Store Locator Map
Display store locations with custom marker icons, clustering for dense areas, and tooltips showing store details. Integrate with map providers for street-level detail.

### Use Case 3: Election Results Visualization
Show election results across districts/states using color mapping, with drilldown capability to explore detailed regional data.

### Use Case 4: Real-time Tracking Dashboard
Plot vehicle, shipment, or asset locations with animated markers, navigation lines showing routes, and real-time data updates.

### Use Case 5: Weather or Environmental Data
Visualize temperature, rainfall, air quality, or other environmental metrics using color gradients and data labels on geographic regions.

### Use Case 6: COVID-19 or Disease Spread Tracking
Display case counts, vaccination rates, or infection rates by region using bubble sizes and color intensity.

### Use Case 7: Flight Route Visualization
Show flight paths between cities using navigation lines, with markers for airports and interactive selection.

### Use Case 8: Custom Seating Layouts
Use custom GeoJSON shapes for non-geographic visualizations like seat selection in theaters, stadiums, or transportation.

## Module Injection Requirements

The Maps component uses feature-specific services that must be injected:

```typescript
import { 
  MapsModule,
  MarkerService,          // For markers
  BubbleService,          // For bubbles
  DataLabelService,       // For data labels
  LegendService,          // For legends
  MapsTooltipService,     // For tooltips
  ZoomService,            // For zoom and pan
  SelectionService,       // For selection
  HighlightService,       // For highlighting
  NavigationLineService,  // For navigation lines
  AnnotationsService,     // For annotations
  PolygonService          // For polygons
} from '@syncfusion/ej2-angular-maps';

@Component({
  providers: [
    MarkerService,
    LegendService,
    MapsTooltipService,
    ZoomService
    // Add only the services you need
  ]
})
```

## API Reference Documentation

### Complete API Catalog

📘 **[Full API Reference Guide](./references/api-reference.md)** - Comprehensive documentation of all Maps APIs

### Quick API Links by Category

#### Core Component
- [MapsComponent](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent) - Main maps component with 20+ properties and methods
- [print()](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#print) - Print functionality
- [export()](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#export) - Export to Image/PDF
- [refresh()](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#refresh) - Refresh map
- [addLayer()](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#addlayer) - Add layer dynamically

#### Layer Configuration
- [LayerSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/layerSettings) - Layer configuration model
- [ShapeSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/shapeSettings) - Shape styling configuration
- [shapeData](https://ej2.syncfusion.com/angular/documentation/api/maps/layerSettings#shapedata) - GeoJSON shape data
- [dataSource](https://ej2.syncfusion.com/angular/documentation/api/maps/layerSettings#datasource) - External data binding

#### Markers & Bubbles
- [MarkerSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/markerSettings) - Marker configuration
- [BubbleSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/bubbleSettings) - Bubble visualization
- [DataLabelSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/dataLabelSettings) - Data labels

#### User Interactions
- [ZoomSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/zoomSettings) - Zoom and pan configuration
- [TooltipSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/tooltipSettings) - Tooltip configuration
- [SelectionSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/selectionSettings) - Selection behavior
- [HighlightSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/highlightSettings) - Highlight behavior

#### Customization
- [LegendSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/legendSettings) - Legend configuration
- [ColorMappingSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/colorMappingSettings) - Color mapping for choropleth
- [NavigationLineSettings](https://ej2.syncfusion.com/angular/documentation/api/maps/navigationLineSettings) - Navigation lines
- [Annotation](https://ej2.syncfusion.com/angular/documentation/api/maps/annotation) - Custom annotations

#### Key Events (25+ Total)
- [load](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#load) - Before map loads
- [loaded](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#loaded) - After map loads
- [shapeSelected](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#shapeselected) - Shape selection event
- [markerClick](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#markerclick) - Marker click event
- [zoom](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#zoom) - Zoom event
- [pan](https://ej2.syncfusion.com/angular/documentation/api/maps/mapsComponent#pan) - Pan event

#### Enumerations
- [ProjectionType](https://ej2.syncfusion.com/angular/documentation/api/maps/projectionType) - Map projection types (Mercator, Miller, Eckert, etc.)
- [MarkerType](https://ej2.syncfusion.com/angular/documentation/api/maps/markerType) - Marker shapes (Balloon, Circle, Diamond, etc.)
- [LayerType](https://ej2.syncfusion.com/angular/documentation/api/maps/layerType) - Layer vs SubLayer
- [GeometryType](https://ej2.syncfusion.com/angular/documentation/api/maps/geometryType) - Geographic vs Normal

#### Event Interfaces
- [ILoadEventArgs](https://ej2.syncfusion.com/angular/documentation/api/maps/iLoadEventArgs) - Load event arguments
- [IShapeSelectedEventArgs](https://ej2.syncfusion.com/angular/documentation/api/maps/iShapeSelectedEventArgs) - Selection event args
- [IMarkerClickEventArgs](https://ej2.syncfusion.com/angular/documentation/api/maps/iMarkerClickEventArgs) - Marker click args

### Context-Specific API References

Each reference guide includes relevant API tables:
- **[getting-started.md](./references/getting-started.md)** - Core setup APIs
- **[layers-and-data.md](./references/layers-and-data.md)** - Layer and data binding APIs
- **[markers.md](./references/markers.md)** - Marker APIs and events
- **[data-visualization.md](./references/data-visualization.md)** - Bubble, color mapping, legend APIs
- **[user-interactions.md](./references/user-interactions.md)** - Zoom, pan, tooltip, selection APIs
- **[map-providers.md](./references/map-providers.md)** - Map provider APIs
- **[customization.md](./references/customization.md)** - Appearance and styling APIs
- **[accessibility.md](./references/accessibility.md)** - Accessibility-related APIs

---

## Next Steps

1. **Start with getting-started.md** to set up your first map
2. **Explore layers-and-data.md** to understand data binding
3. **Add markers.md** to plot locations
4. **Implement user-interactions.md** for zoom, pan, and tooltips
5. **Review customization.md** for styling and themes
6. **Check accessibility.md** to ensure WCAG compliance

---

**Package:** `@syncfusion/ej2-angular-maps`  
**Documentation:** [Syncfusion Angular Maps Documentation](https://ej2.syncfusion.com/angular/documentation/maps/getting-started/)  
**Demos:** [Syncfusion Angular Maps Demos](https://ej2.syncfusion.com/angular/demos/#/material/maps/default)
