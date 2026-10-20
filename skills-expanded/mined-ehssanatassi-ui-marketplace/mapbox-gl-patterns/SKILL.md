---
name: mapbox-gl-patterns
description: Comprehensive Mapbox GL JS patterns for custom styles, 3D visualization, animations, and data-driven maps. Use when searching for Mapbox styling, 3D buildings, heat maps, or advanced map visualizations.
---

# Mapbox GL JS Patterns Library

A comprehensive reference library of Mapbox GL JS patterns for creating custom map styles, 3D visualizations, animations, and data-driven maps.

## Table of Contents

1. [Custom Map Styles](#custom-map-styles)
2. [Data-Driven Styling](#data-driven-styling)
3. [Custom Markers and Popups](#custom-markers-and-popups)
4. [3D Buildings and Terrain](#3d-buildings-and-terrain)
5. [Animated Layers](#animated-layers)
6. [Heat Maps](#heat-maps)
7. [Performance Optimization](#performance-optimization)
8. [Theme Switching](#theme-switching)

---

## Custom Map Styles

### Basic Custom Style Pattern

**Use Case**: Create branded map styles matching your design system

**Pattern**:
```typescript
/**
 * Custom Mapbox GL JS Map Initialization
 *
 * @description Initialize map with custom style matching brand colors
 * @param container - Container element ID
 * @param styleUrl - Custom style URL or inline style object
 * @returns Mapbox Map instance
 *
 * @example
 * const map = initializeCustomMap('map', {
 *   style: customDarkStyle,
 *   center: [-74.5, 40],
 *   zoom: 9
 * });
 */
import mapboxgl from 'mapbox-gl';

mapboxgl.accessToken = 'YOUR_MAPBOX_ACCESS_TOKEN';

interface MapConfig {
  style: string | object;
  center: [number, number];
  zoom: number;
  pitch?: number;
  bearing?: number;
  antialias?: boolean;
}

function initializeCustomMap(
  container: string,
  config: MapConfig
): mapboxgl.Map {
  const map = new mapboxgl.Map({
    container,
    style: config.style,
    center: config.center,
    zoom: config.zoom,
    pitch: config.pitch || 0,
    bearing: config.bearing || 0,
    antialias: config.antialias !== false
  });

  return map;
}
```

### Inline Custom Style Definition

**Pattern**:
```typescript
/**
 * Custom Mapbox Style Object
 *
 * @description Complete style definition with custom layers and colors
 * @type {mapboxgl.Style}
 *
 * @example
 * const map = new mapboxgl.Map({
 *   style: customDarkStyle
 * });
 */
const customDarkStyle: mapboxgl.Style = {
  version: 8,
  name: 'Custom Dark Style',
  metadata: {
    'mapbox:autocomposite': true,
    'mapbox:type': 'template'
  },
  sources: {
    'mapbox-streets': {
      type: 'vector',
      url: 'mapbox://mapbox.mapbox-streets-v8'
    }
  },
  layers: [
    {
      id: 'background',
      type: 'background',
      paint: {
        'background-color': '#1a1a2e'
      }
    },
    {
      id: 'water',
      type: 'fill',
      source: 'mapbox-streets',
      'source-layer': 'water',
      paint: {
        'fill-color': '#16213e',
        'fill-opacity': 0.8
      }
    },
    {
      id: 'parks',
      type: 'fill',
      source: 'mapbox-streets',
      'source-layer': 'landuse',
      filter: ['==', 'class', 'park'],
      paint: {
        'fill-color': '#0f3460',
        'fill-opacity': 0.6
      }
    },
    {
      id: 'roads',
      type: 'line',
      source: 'mapbox-streets',
      'source-layer': 'road',
      paint: {
        'line-color': '#e94560',
        'line-width': 2,
        'line-opacity': 0.7
      }
    },
    {
      id: 'buildings',
      type: 'fill-extrusion',
      source: 'mapbox-streets',
      'source-layer': 'building',
      paint: {
        'fill-extrusion-color': '#533483',
        'fill-extrusion-height': ['get', 'height'],
        'fill-extrusion-base': ['get', 'min_height'],
        'fill-extrusion-opacity': 0.6
      }
    }
  ]
};
```

---

## Data-Driven Styling

### Choropleth Map with Expressions

**Use Case**: Visualize geographic data with color-coded regions

**Pattern**:
```typescript
/**
 * Data-Driven Choropleth Layer
 *
 * @description Creates choropleth visualization using Mapbox expressions
 * @param map - Mapbox map instance
 * @param sourceId - GeoJSON source ID
 * @param propertyName - Property to visualize
 *
 * @example
 * addChoroplethLayer(map, 'population-data', 'density');
 */
function addChoroplethLayer(
  map: mapboxgl.Map,
  sourceId: string,
  propertyName: string
): void {
  map.on('load', () => {
    // Add GeoJSON source
    map.addSource(sourceId, {
      type: 'geojson',
      data: '/data/regions.geojson'
    });

    // Add choropleth layer with data-driven colors
    map.addLayer({
      id: `${sourceId}-layer`,
      type: 'fill',
      source: sourceId,
      paint: {
        // Use interpolate expression for smooth color gradients
        'fill-color': [
          'interpolate',
          ['linear'],
          ['get', propertyName],
          0, '#ffffcc',
          10, '#ffeda0',
          20, '#fed976',
          50, '#feb24c',
          100, '#fd8d3c',
          200, '#fc4e2a',
          500, '#e31a1c',
          1000, '#bd0026',
          2000, '#800026'
        ],
        // Hover opacity with feature-state
        'fill-opacity': [
          'case',
          ['boolean', ['feature-state', 'hover'], false],
          0.9,
          0.7
        ],
        'fill-outline-color': '#ffffff'
      }
    });

    // Add interactive hover effect
    let hoveredStateId: string | number | null = null;

    map.on('mousemove', `${sourceId}-layer`, (e) => {
      if (e.features && e.features.length > 0) {
        if (hoveredStateId !== null) {
          map.setFeatureState(
            { source: sourceId, id: hoveredStateId },
            { hover: false }
          );
        }
        hoveredStateId = e.features[0].id!;
        map.setFeatureState(
          { source: sourceId, id: hoveredStateId },
          { hover: true }
        );
      }
    });

    map.on('mouseleave', `${sourceId}-layer`, () => {
      if (hoveredStateId !== null) {
        map.setFeatureState(
          { source: sourceId, id: hoveredStateId },
          { hover: false }
        );
      }
      hoveredStateId = null;
    });
  });
}
```

### Category-Based Circle Markers

**Pattern**:
```typescript
/**
 * Category-Based Point Visualization
 *
 * @description Creates circle markers with colors based on category
 * @param map - Mapbox map instance
 * @param sourceId - Point data source ID
 *
 * @example
 * addCategoryMarkers(map, 'poi-data');
 */
function addCategoryMarkers(
  map: mapboxgl.Map,
  sourceId: string
): void {
  map.on('load', () => {
    map.addSource(sourceId, {
      type: 'geojson',
      data: '/data/points.geojson'
    });

    map.addLayer({
      id: `${sourceId}-circles`,
      type: 'circle',
      source: sourceId,
      paint: {
        // Size based on population
        'circle-radius': [
          'interpolate',
          ['linear'],
          ['get', 'population'],
          0, 4,
          1000, 8,
          10000, 16,
          100000, 32
        ],
        // Color based on category
        'circle-color': [
          'match',
          ['get', 'category'],
          'urban', '#3b82f6',
          'suburban', '#10b981',
          'rural', '#f59e0b',
          '#6b7280' // default color
        ],
        'circle-stroke-width': 2,
        'circle-stroke-color': '#ffffff',
        'circle-opacity': 0.8
      }
    });
  });
}
```

---

## Custom Markers and Popups

### HTML Custom Marker Pattern

**Use Case**: Create rich, branded markers with HTML/CSS

**Pattern**:
```typescript
/**
 * Custom HTML Marker Factory
 *
 * @description Creates custom markers using HTML elements
 * @param color - Marker color from design tokens
 * @param label - Optional text label
 * @returns HTML marker element
 *
 * @example
 * const el = createCustomMarker('var(--color-primary)', 'A');
 * new mapboxgl.Marker({ element: el })
 *   .setLngLat([lng, lat])
 *   .addTo(map);
 */
function createCustomMarker(
  color: string,
  label?: string
): HTMLElement {
  const el = document.createElement('div');
  el.className = 'custom-mapbox-marker';
  el.style.backgroundColor = color;

  if (label) {
    el.innerHTML = `
      <div class="marker-content">
        <span class="marker-label">${label}</span>
      </div>
      <div class="marker-arrow"></div>
    `;
  }

  return el;
}
```

**CSS**:
```css
/**
 * Custom Mapbox Marker Styles
 *
 * @description Styled HTML markers with animations
 */
.custom-mapbox-marker {
  width: 40px;
  height: 40px;
  border-radius: 50% 50% 50% 0;
  background: var(--color-primary, #3b82f6);
  transform: rotate(-45deg);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.custom-mapbox-marker:hover {
  transform: rotate(-45deg) scale(1.1);
}

.marker-content {
  transform: rotate(45deg);
  color: white;
  font-weight: 700;
  font-size: 16px;
}

/* Pulse animation */
.custom-mapbox-marker.active::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50% 50% 50% 0;
  background: inherit;
  animation: markerPulse 2s infinite;
}

@keyframes markerPulse {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 0;
  }
}
```

### Rich Popup Pattern

**Pattern**:
```typescript
/**
 * Rich Media Popup Factory
 *
 * @description Creates styled popups with images and actions
 * @param config - Popup configuration
 * @returns Mapbox Popup instance
 *
 * @example
 * const popup = createRichPopup({
 *   title: 'Location Name',
 *   image: 'photo.jpg',
 *   description: 'Description...',
 *   actions: [{ label: 'View', onClick: () => {} }]
 * });
 */
interface PopupConfig {
  title: string;
  image?: string;
  description: string;
  metadata?: Array<{ icon: string; label: string; value: string }>;
  actions?: Array<{ label: string; onClick: () => void }>;
}

function createRichPopup(config: PopupConfig): mapboxgl.Popup {
  const { title, image, description, metadata = [], actions = [] } = config;

  const popupHTML = `
    <div class="mapbox-rich-popup">
      ${image ? `
        <div class="popup-image">
          <img src="${image}" alt="${title}" />
        </div>
      ` : ''}

      <div class="popup-content">
        <h3 class="popup-title">${title}</h3>
        <p class="popup-description">${description}</p>

        ${metadata.length > 0 ? `
          <div class="popup-metadata">
            ${metadata.map(item => `
              <div class="metadata-item">
                <span class="metadata-icon">${item.icon}</span>
                <div>
                  <span class="metadata-label">${item.label}</span>
                  <span class="metadata-value">${item.value}</span>
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}
      </div>

      ${actions.length > 0 ? `
        <div class="popup-actions">
          ${actions.map((action, i) => `
            <button class="popup-btn" data-action="${i}">
              ${action.label}
            </button>
          `).join('')}
        </div>
      ` : ''}
    </div>
  `;

  const popup = new mapboxgl.Popup({
    className: 'custom-mapbox-popup',
    closeButton: true,
    closeOnClick: false,
    maxWidth: '320px',
    offset: 25
  }).setHTML(popupHTML);

  // Add event listeners after popup opens
  popup.on('open', () => {
    const popupElement = popup.getElement();
    actions.forEach((action, i) => {
      const btn = popupElement?.querySelector(`[data-action="${i}"]`);
      btn?.addEventListener('click', action.onClick);
    });
  });

  return popup;
}
```

**CSS**:
```css
/**
 * Rich Popup Styles
 *
 * @description Modern popup styling with animations
 */
.custom-mapbox-popup .mapboxgl-popup-content {
  padding: 0;
  border-radius: var(--radius-lg, 12px);
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  min-width: 280px;
}

.mapbox-rich-popup {
  background: var(--color-surface, white);
}

.popup-image {
  width: 100%;
  height: 160px;
  overflow: hidden;
}

.popup-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.popup-content {
  padding: 16px;
}

.popup-title {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.popup-description {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

.popup-metadata {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.metadata-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.metadata-icon {
  font-size: 20px;
}

.metadata-label {
  display: block;
  font-size: 12px;
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metadata-value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.popup-actions {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: var(--color-gray-50);
  border-top: 1px solid var(--color-border);
}

.popup-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius-md, 6px);
  background: var(--color-primary);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.popup-btn:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
}
```

---

## 3D Buildings and Terrain

### 3D Terrain and Buildings Pattern

**Use Case**: Add realistic 3D visualization to maps

**Pattern**:
```typescript
/**
 * Add 3D Terrain and Buildings
 *
 * @description Enables 3D terrain and extruded buildings
 * @param map - Mapbox map instance
 * @param exaggeration - Terrain height exaggeration multiplier
 *
 * @example
 * add3DVisualization(map, 1.5);
 */
function add3DVisualization(
  map: mapboxgl.Map,
  exaggeration: number = 1.5
): void {
  map.on('load', () => {
    // Add 3D terrain source
    map.addSource('mapbox-dem', {
      type: 'raster-dem',
      url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
      tileSize: 512,
      maxzoom: 14
    });

    // Set terrain
    map.setTerrain({
      source: 'mapbox-dem',
      exaggeration
    });

    // Add 3D buildings layer
    map.addLayer({
      id: '3d-buildings',
      source: 'composite',
      'source-layer': 'building',
      filter: ['==', 'extrude', 'true'],
      type: 'fill-extrusion',
      minzoom: 15,
      paint: {
        // Color based on height
        'fill-extrusion-color': [
          'interpolate',
          ['linear'],
          ['get', 'height'],
          0, '#e0e0e0',
          50, '#b0b0b0',
          100, '#808080',
          200, '#606060'
        ],
        // Animated height appearance
        'fill-extrusion-height': [
          'interpolate',
          ['linear'],
          ['zoom'],
          15, 0,
          15.05, ['get', 'height']
        ],
        'fill-extrusion-base': [
          'interpolate',
          ['linear'],
          ['zoom'],
          15, 0,
          15.05, ['get', 'min_height']
        ],
        'fill-extrusion-opacity': 0.8,
        'fill-extrusion-vertical-gradient': true
      }
    });

    // Add atmospheric sky
    map.addLayer({
      id: 'sky',
      type: 'sky',
      paint: {
        'sky-type': 'atmosphere',
        'sky-atmosphere-sun': [0.0, 90.0],
        'sky-atmosphere-sun-intensity': 15
      }
    });
  });
}
```

---

## Animated Layers

### Pulse Animation Pattern

**Use Case**: Highlight points of interest with pulsing animation

**Pattern**:
```typescript
/**
 * Animated Pulse Layer
 *
 * @description Creates pulsing circle animation for markers
 * @param map - Mapbox map instance
 * @param layerId - Layer ID to animate
 *
 * @example
 * addPulseAnimation(map, 'active-locations');
 */
function addPulseAnimation(
  map: mapboxgl.Map,
  layerId: string
): void {
  let radius = 5;
  let growing = true;

  function pulse() {
    if (growing) {
      radius += 0.5;
      if (radius >= 20) growing = false;
    } else {
      radius -= 0.5;
      if (radius <= 5) growing = true;
    }

    map.setPaintProperty(layerId, 'circle-radius', radius);
    requestAnimationFrame(pulse);
  }

  pulse();
}
```

### Animated Route Pattern

**Pattern**:
```typescript
/**
 * Animated Route Line
 *
 * @description Animates a line to show movement/flow
 * @param map - Mapbox map instance
 * @param routeData - GeoJSON LineString data
 *
 * @example
 * animateRoute(map, routeGeoJSON);
 */
function animateRoute(
  map: mapboxgl.Map,
  routeData: GeoJSON.Feature<GeoJSON.LineString>
): void {
  map.on('load', () => {
    map.addSource('route', {
      type: 'geojson',
      data: routeData
    });

    map.addLayer({
      id: 'route-line',
      type: 'line',
      source: 'route',
      paint: {
        'line-color': '#3b82f6',
        'line-width': 4,
        'line-dasharray': [0, 4, 3]
      }
    });

    // Animate the line
    let offset = 0;
    function animate() {
      offset = (offset + 0.5) % 7;
      map.setPaintProperty('route-line', 'line-dasharray', [0, offset, 7 - offset]);
      requestAnimationFrame(animate);
    }

    animate();
  });
}
```

---

## Heat Maps

### Basic Heat Map Pattern

**Use Case**: Visualize point density

**Pattern**:
```typescript
/**
 * Heat Map Visualization
 *
 * @description Creates heat map with custom color gradient
 * @param map - Mapbox map instance
 * @param sourceId - Point data source
 * @param weightProperty - Property for weight calculation
 *
 * @example
 * addHeatMap(map, 'earthquake-data', 'magnitude');
 */
function addHeatMap(
  map: mapboxgl.Map,
  sourceId: string,
  weightProperty: string
): void {
  map.on('load', () => {
    map.addSource(sourceId, {
      type: 'geojson',
      data: '/data/points.geojson'
    });

    map.addLayer({
      id: `${sourceId}-heat`,
      type: 'heatmap',
      source: sourceId,
      maxzoom: 15,
      paint: {
        // Weight based on property
        'heatmap-weight': [
          'interpolate',
          ['linear'],
          ['get', weightProperty],
          0, 0,
          6, 1
        ],
        // Intensity by zoom level
        'heatmap-intensity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          0, 1,
          15, 3
        ],
        // Custom color gradient
        'heatmap-color': [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0, 'rgba(33, 102, 172, 0)',
          0.2, 'rgb(103, 169, 207)',
          0.4, 'rgb(209, 229, 240)',
          0.6, 'rgb(253, 219, 199)',
          0.8, 'rgb(239, 138, 98)',
          1, 'rgb(178, 24, 43)'
        ],
        // Radius by zoom
        'heatmap-radius': [
          'interpolate',
          ['linear'],
          ['zoom'],
          0, 2,
          15, 20
        ],
        // Fade out at high zoom
        'heatmap-opacity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          7, 1,
          15, 0
        ]
      }
    });

    // Add circle layer for high zoom
    map.addLayer({
      id: `${sourceId}-point`,
      type: 'circle',
      source: sourceId,
      minzoom: 7,
      paint: {
        'circle-radius': [
          'interpolate',
          ['linear'],
          ['get', weightProperty],
          0, 2,
          6, 20
        ],
        'circle-color': [
          'interpolate',
          ['linear'],
          ['get', weightProperty],
          0, '#ffffb2',
          3, '#feb24c',
          5, '#f03b20',
          7, '#bd0026'
        ],
        'circle-stroke-color': 'white',
        'circle-stroke-width': 1,
        'circle-opacity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          7, 0,
          15, 1
        ]
      }
    });
  });
}
```

---

## Performance Optimization

### Vector Tiles vs GeoJSON

**Pattern**:
```typescript
/**
 * Optimized Large Dataset Handling
 *
 * @description Uses vector tiles for better performance
 * @param map - Mapbox map instance
 * @param tilesetId - Mapbox tileset ID
 *
 * @example
 * addVectorTileLayer(map, 'username.tileset-id');
 */
function addVectorTileLayer(
  map: mapboxgl.Map,
  tilesetId: string
): void {
  map.on('load', () => {
    map.addSource('large-dataset', {
      type: 'vector',
      url: `mapbox://${tilesetId}`
    });

    map.addLayer({
      id: 'large-dataset-layer',
      type: 'fill',
      source: 'large-dataset',
      'source-layer': 'data-layer',
      paint: {
        'fill-color': ['get', 'color'],
        'fill-opacity': 0.7
      }
    });
  });
}
```

### Clustering Pattern

**Pattern**:
```typescript
/**
 * Point Clustering for Performance
 *
 * @description Clusters points for better rendering performance
 * @param map - Mapbox map instance
 * @param sourceId - Point data source
 *
 * @example
 * addClusteredPoints(map, 'locations');
 */
function addClusteredPoints(
  map: mapboxgl.Map,
  sourceId: string
): void {
  map.on('load', () => {
    map.addSource(sourceId, {
      type: 'geojson',
      data: '/data/points.geojson',
      cluster: true,
      clusterMaxZoom: 14,
      clusterRadius: 50
    });

    // Clusters
    map.addLayer({
      id: 'clusters',
      type: 'circle',
      source: sourceId,
      filter: ['has', 'point_count'],
      paint: {
        'circle-color': [
          'step',
          ['get', 'point_count'],
          '#51bbd6',
          100,
          '#f1f075',
          750,
          '#f28cb1'
        ],
        'circle-radius': [
          'step',
          ['get', 'point_count'],
          20,
          100,
          30,
          750,
          40
        ]
      }
    });

    // Cluster count
    map.addLayer({
      id: 'cluster-count',
      type: 'symbol',
      source: sourceId,
      filter: ['has', 'point_count'],
      layout: {
        'text-field': '{point_count_abbreviated}',
        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
        'text-size': 12
      }
    });

    // Unclustered points
    map.addLayer({
      id: 'unclustered-point',
      type: 'circle',
      source: sourceId,
      filter: ['!', ['has', 'point_count']],
      paint: {
        'circle-color': '#11b4da',
        'circle-radius': 8,
        'circle-stroke-width': 1,
        'circle-stroke-color': '#fff'
      }
    });
  });
}
```

---

## Theme Switching

### Animated Theme Transition Pattern

**Pattern**:
```typescript
/**
 * Smooth Theme Switching
 *
 * @description Switches map style with smooth transition
 * @param map - Mapbox map instance
 * @param newStyle - New style URL or object
 *
 * @example
 * switchTheme(map, 'mapbox://styles/mapbox/dark-v11');
 */
function switchTheme(
  map: mapboxgl.Map,
  newStyle: string | object
): void {
  // Save current view
  const center = map.getCenter();
  const zoom = map.getZoom();
  const bearing = map.getBearing();
  const pitch = map.getPitch();

  // Fade out
  map.getCanvas().style.transition = 'opacity 0.3s';
  map.getCanvas().style.opacity = '0';

  setTimeout(() => {
    // Switch style
    map.setStyle(newStyle);

    // Restore view after style loads
    map.once('styledata', () => {
      map.jumpTo({ center, zoom, bearing, pitch });

      // Fade in
      map.getCanvas().style.opacity = '1';
    });
  }, 300);
}
```

---

## Best Practices

1. **Use Vector Tiles** - For large datasets, use vector tiles instead of GeoJSON
2. **Implement Clustering** - Cluster points when displaying many markers
3. **Optimize Expressions** - Use efficient Mapbox expressions for styling
4. **Lazy Load Data** - Load data as needed based on viewport
5. **Use Feature State** - For interactive styling instead of updating layers
6. **Debounce Events** - Throttle expensive operations on map events
7. **Clean Up Layers** - Remove unused layers and sources
8. **Test Performance** - Use browser DevTools to profile rendering
9. **Optimize Images** - Compress sprites and textures
10. **Consider Mobile** - Test on mobile devices for touch interactions

## Accessibility Considerations

```typescript
/**
 * Accessibility Enhancements
 *
 * @description Add ARIA labels and keyboard navigation
 */
function enhanceAccessibility(map: mapboxgl.Map): void {
  const container = map.getContainer();

  // ARIA labels
  container.setAttribute('role', 'application');
  container.setAttribute('aria-label', 'Interactive map');

  // Keyboard navigation for popups
  map.on('open', (e) => {
    const popup = e.target;
    const popupElement = popup.getElement();

    if (popupElement) {
      popupElement.setAttribute('role', 'dialog');
      popupElement.setAttribute('aria-live', 'polite');

      // Focus close button
      const closeButton = popupElement.querySelector('.mapboxgl-popup-close-button');
      if (closeButton instanceof HTMLElement) {
        closeButton.focus();
      }
    }
  });
}
```

---

## Summary

This Mapbox GL JS patterns library provides:

- **Custom map styles** with brand integration
- **Data-driven visualizations** using expressions
- **3D terrain and buildings** for realistic views
- **Smooth animations** and transitions
- **Heat maps** for density visualization
- **Performance optimization** patterns
- **Accessibility** enhancements
- **Theme switching** capabilities

All patterns include:
- Complete TypeScript code
- Swagger/OpenAPI documentation
- Design token integration
- Performance considerations
- Accessibility compliance
- Real-world examples
