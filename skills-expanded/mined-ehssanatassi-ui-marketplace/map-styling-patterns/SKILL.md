---
name: map-styling-patterns
description: Comprehensive map styling patterns for Leaflet, Mapbox, and GIS visualizations. Use when searching for map theming, marker styling, popup designs, or choropleth patterns.
---

# Map Styling Patterns Library

A comprehensive reference library of map styling patterns for Leaflet, Mapbox GL JS, and GIS applications with production-ready code examples.

## Table of Contents

1. [Marker Styles](#marker-styles)
2. [Popup & Tooltip Patterns](#popup--tooltip-patterns)
3. [Choropleth Maps](#choropleth-maps)
4. [Heat Maps](#heat-maps)
5. [Cluster Styles](#cluster-styles)
6. [Custom Controls](#custom-controls)
7. [Theme Systems](#theme-systems)
8. [Performance Patterns](#performance-patterns)
9. [Accessibility Patterns](#accessibility-patterns)
10. [Integration Patterns](#integration-patterns)

---

## Marker Styles

### SVG Custom Markers

**Use Case**: Create scalable, colorful markers with custom icons

**Pattern**:
```typescript
/**
 * SVG Marker Factory
 *
 * Creates custom SVG markers with dynamic colors and icons.
 * Integrates with design tokens for theming.
 *
 * @param color - Marker color from design tokens
 * @param icon - Icon name or SVG path
 * @param size - Marker size (small, medium, large)
 * @returns Leaflet DivIcon
 *
 * @example
 * const marker = createSVGMarker('var(--color-primary)', 'location', 'medium');
 * L.marker([lat, lng], { icon: marker }).addTo(map);
 */
function createSVGMarker(
  color: string = 'var(--color-primary)',
  icon?: string,
  size: 'small' | 'medium' | 'large' = 'medium'
): L.DivIcon {
  const sizes = {
    small: { width: 20, height: 33, iconSize: 12 },
    medium: { width: 25, height: 41, iconSize: 16 },
    large: { width: 30, height: 49, iconSize: 20 }
  };

  const { width, height, iconSize } = sizes[size];

  const svgIcon = `
    <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"
         xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="shadow-${color.replace(/[^a-z0-9]/gi, '')}">
          <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>
        </filter>
      </defs>
      <path
        fill="${color}"
        stroke="white"
        stroke-width="2"
        filter="url(#shadow-${color.replace(/[^a-z0-9]/gi, '')})"
        d="M${width / 2} 0C${width * 0.22} 0 0 ${height * 0.3} 0 ${height * 0.3}
           c0 ${height * 0.23} ${width / 2} ${height * 0.7} ${width / 2} ${height * 0.7}
           s${width / 2} -${height * 0.47} ${width / 2} -${height * 0.7}
           C${width} ${height * 0.3} ${width * 0.78} 0 ${width / 2} 0z"/>
      ${icon ? `
        <circle cx="${width / 2}" cy="${height * 0.3}" r="${iconSize / 2 + 2}" fill="white"/>
        <text x="${width / 2}" y="${height * 0.3}"
              text-anchor="middle"
              dominant-baseline="central"
              font-size="${iconSize}"
              fill="${color}">${icon}</text>
      ` : ''}
    </svg>
  `;

  return L.divIcon({
    html: svgIcon,
    className: 'custom-svg-marker',
    iconSize: [width, height],
    iconAnchor: [width / 2, height],
    popupAnchor: [0, -height + 5]
  });
}
```

**CSS Integration**:
```css
/**
 * SVG Marker Styles with Design Tokens
 *
 * Uses CSS custom properties for theming and animations.
 * Supports dark mode and accessibility.
 */

.custom-svg-marker {
  /* Design token integration */
  --marker-transition: var(--transition-base, 0.2s ease);
  --marker-scale-hover: var(--scale-hover, 1.1);

  cursor: pointer;
  transition: transform var(--marker-transition);
  will-change: transform;
}

.custom-svg-marker:hover {
  transform: scale(var(--marker-scale-hover)) translateY(-2px);
  z-index: 1000;
}

.custom-svg-marker:active {
  transform: scale(0.95);
}

/* Pulse animation for active markers */
.custom-svg-marker.active {
  animation: markerPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes markerPulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
    transform: scale(1.05);
  }
}

/* Accessibility: Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .custom-svg-marker {
    transition: none;
    animation: none;
  }

  .custom-svg-marker:hover {
    transform: none;
  }
}
```

---

### Marker Clustering with Categories

**Use Case**: Cluster markers by category with color-coded clusters

**Pattern**:
```typescript
/**
 * Categorical Marker Clustering
 *
 * Creates marker clusters with category-based styling.
 * Supports multiple categories with distinct colors.
 *
 * @param markers - Array of marker data with categories
 * @param categories - Category configuration
 * @returns Marker cluster group
 *
 * @example
 * const clusters = createCategoricalClusters(locations, {
 *   restaurant: { color: 'var(--color-error)', icon: '🍴' },
 *   hotel: { color: 'var(--color-primary)', icon: '🏨' }
 * });
 */
interface MarkerData {
  lat: number;
  lng: number;
  category: string;
  name: string;
  properties: Record<string, any>;
}

interface CategoryConfig {
  color: string;
  icon: string;
  label: string;
}

function createCategoricalClusters(
  markers: MarkerData[],
  categories: Record<string, CategoryConfig>
): L.MarkerClusterGroup {
  /**
   * Create custom cluster icon with category breakdown
   */
  function createClusterIcon(cluster: L.MarkerCluster): L.DivIcon {
    const childMarkers = cluster.getAllChildMarkers();
    const childCount = childMarkers.length;

    // Count markers by category
    const categoryCounts: Record<string, number> = {};
    childMarkers.forEach((marker: any) => {
      const category = marker.options.category || 'default';
      categoryCounts[category] = (categoryCounts[category] || 0) + 1;
    });

    // Determine dominant category
    let dominantCategory = 'default';
    let maxCount = 0;
    Object.entries(categoryCounts).forEach(([cat, count]) => {
      if (count > maxCount) {
        maxCount = count;
        dominantCategory = cat;
      }
    });

    const config = categories[dominantCategory] || {
      color: 'var(--color-gray-500)',
      icon: '📍'
    };

    // Size based on count
    let sizeClass = 'small';
    if (childCount >= 100) sizeClass = 'large';
    else if (childCount >= 10) sizeClass = 'medium';

    return L.divIcon({
      html: `
        <div class="cluster-marker cluster-${sizeClass}"
             style="background-color: ${config.color}">
          <div class="cluster-inner">
            <span class="cluster-count">${childCount}</span>
            <span class="cluster-icon">${config.icon}</span>
          </div>
          <div class="cluster-breakdown">
            ${Object.entries(categoryCounts)
              .map(([cat, count]) => `
                <div class="category-pill"
                     style="background-color: ${categories[cat]?.color || '#ccc'}">
                  <span>${categories[cat]?.icon || '•'}</span>
                  <span>${count}</span>
                </div>
              `)
              .join('')}
          </div>
        </div>
      `,
      className: 'marker-cluster-categorical',
      iconSize: L.point(60, 60)
    });
  }

  // Create cluster group
  const clusterGroup = L.markerClusterGroup({
    iconCreateFunction: createClusterIcon,
    spiderfyOnMaxZoom: true,
    showCoverageOnHover: true,
    zoomToBoundsOnClick: true,
    maxClusterRadius: 80,
    disableClusteringAtZoom: 16,
    animate: true,
    animateAddingMarkers: true,
    spiderfyDistanceMultiplier: 2
  });

  // Add markers to cluster
  markers.forEach(markerData => {
    const config = categories[markerData.category] || {
      color: 'var(--color-gray-500)',
      icon: '📍'
    };

    const marker = L.marker([markerData.lat, markerData.lng], {
      icon: createSVGMarker(config.color, config.icon, 'medium'),
      category: markerData.category
    } as any);

    marker.bindPopup(`
      <div class="map-popup category-${markerData.category}">
        <div class="popup-category">${config.icon} ${config.label}</div>
        <h3>${markerData.name}</h3>
        <div class="popup-properties">
          ${Object.entries(markerData.properties)
            .map(([key, value]) => `
              <div class="property-row">
                <span class="property-key">${key}:</span>
                <span class="property-value">${value}</span>
              </div>
            `)
            .join('')}
        </div>
      </div>
    `);

    clusterGroup.addLayer(marker);
  });

  return clusterGroup;
}
```

**CSS**:
```css
/**
 * Categorical Cluster Styles
 *
 * Styles for category-based marker clusters with breakdowns.
 */

.marker-cluster-categorical {
  background: none;
}

.cluster-marker {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cluster-marker:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.cluster-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  color: white;
}

.cluster-count {
  font-size: 18px;
  font-weight: 700;
  line-height: 1;
}

.cluster-icon {
  font-size: 14px;
  line-height: 1;
}

/* Size variants */
.cluster-small {
  width: 50px;
  height: 50px;
}

.cluster-medium {
  width: 60px;
  height: 60px;
}

.cluster-large {
  width: 70px;
  height: 70px;
}

.cluster-large .cluster-count {
  font-size: 20px;
}

/* Category breakdown tooltip */
.cluster-breakdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%) scale(0);
  background: white;
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  gap: 4px;
  opacity: 0;
  transition: all 0.2s ease;
  pointer-events: none;
  white-space: nowrap;
  z-index: 1000;
}

.cluster-marker:hover .cluster-breakdown {
  transform: translateX(-50%) scale(1);
  opacity: 1;
}

.category-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.category-pill span:first-child {
  font-size: 14px;
}
```

---

## Popup & Tooltip Patterns

### Rich Media Popup

**Use Case**: Display images, videos, and interactive content in popups

**Pattern**:
```typescript
/**
 * Rich Media Popup Component
 *
 * Creates feature-rich popups with media support, actions, and animations.
 * Supports images, videos, galleries, and custom content.
 *
 * @param content - Popup content configuration
 * @returns Leaflet Popup instance
 *
 * @example
 * const popup = createRichMediaPopup({
 *   title: 'Golden Gate Bridge',
 *   images: ['img1.jpg', 'img2.jpg'],
 *   description: 'Historic landmark...',
 *   actions: [
 *     { label: 'Directions', onClick: () => {} },
 *     { label: 'Save', onClick: () => {} }
 *   ]
 * });
 */
interface RichMediaPopupConfig {
  title: string;
  subtitle?: string;
  images?: string[];
  video?: string;
  description: string;
  metadata?: Array<{ icon: string; label: string; value: string }>;
  actions?: Array<{ label: string; icon?: string; onClick: () => void; variant?: 'primary' | 'secondary' }>;
  badge?: { text: string; color: string };
}

function createRichMediaPopup(config: RichMediaPopupConfig): L.Popup {
  const {
    title,
    subtitle,
    images = [],
    video,
    description,
    metadata = [],
    actions = [],
    badge
  } = config;

  // Generate gallery HTML
  const galleryHTML = images.length > 0 ? `
    <div class="popup-gallery">
      <div class="gallery-main">
        <img src="${images[0]}" alt="${title}" class="gallery-main-image" />
        ${images.length > 1 ? `
          <button class="gallery-nav gallery-prev" aria-label="Previous image">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <button class="gallery-nav gallery-next" aria-label="Next image">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
          <div class="gallery-indicators">
            ${images.map((_, i) => `
              <button class="gallery-indicator ${i === 0 ? 'active' : ''}"
                      data-index="${i}"
                      aria-label="View image ${i + 1}"></button>
            `).join('')}
          </div>
        ` : ''}
      </div>
      ${images.length > 1 ? `
        <div class="gallery-thumbnails">
          ${images.map((img, i) => `
            <img src="${img}"
                 alt="${title} ${i + 1}"
                 class="gallery-thumb ${i === 0 ? 'active' : ''}"
                 data-index="${i}" />
          `).join('')}
        </div>
      ` : ''}
    </div>
  ` : '';

  const videoHTML = video ? `
    <div class="popup-video">
      <video controls>
        <source src="${video}" type="video/mp4" />
        Your browser doesn't support video.
      </video>
    </div>
  ` : '';

  const metadataHTML = metadata.length > 0 ? `
    <div class="popup-metadata">
      ${metadata.map(item => `
        <div class="metadata-item">
          <span class="metadata-icon">${item.icon}</span>
          <div class="metadata-content">
            <span class="metadata-label">${item.label}</span>
            <span class="metadata-value">${item.value}</span>
          </div>
        </div>
      `).join('')}
    </div>
  ` : '';

  const actionsHTML = actions.length > 0 ? `
    <div class="popup-actions">
      ${actions.map((action, i) => `
        <button class="popup-action-btn ${action.variant || 'secondary'}"
                data-action-index="${i}">
          ${action.icon ? `<span class="action-icon">${action.icon}</span>` : ''}
          <span>${action.label}</span>
        </button>
      `).join('')}
    </div>
  ` : '';

  const popupHTML = `
    <div class="rich-media-popup">
      ${badge ? `<span class="popup-badge" style="background-color: ${badge.color}">${badge.text}</span>` : ''}

      ${galleryHTML || videoHTML}

      <div class="popup-content">
        <div class="popup-header">
          <h3 class="popup-title">${title}</h3>
          ${subtitle ? `<p class="popup-subtitle">${subtitle}</p>` : ''}
        </div>

        <p class="popup-description">${description}</p>

        ${metadataHTML}
      </div>

      ${actionsHTML}
    </div>
  `;

  const popup = L.popup({
    maxWidth: 350,
    minWidth: 300,
    className: 'rich-media-popup-container',
    closeButton: true,
    autoClose: false,
    closeOnClick: false
  }).setContent(popupHTML);

  // Add event listeners after popup opens
  popup.on('add', (e: any) => {
    const container = e.target.getElement();

    // Gallery navigation
    if (images.length > 1) {
      let currentIndex = 0;
      const mainImage = container.querySelector('.gallery-main-image') as HTMLImageElement;
      const indicators = container.querySelectorAll('.gallery-indicator');
      const thumbnails = container.querySelectorAll('.gallery-thumb');

      const updateGallery = (index: number) => {
        currentIndex = index;
        if (mainImage) mainImage.src = images[index];

        indicators.forEach((ind, i) => {
          ind.classList.toggle('active', i === index);
        });

        thumbnails.forEach((thumb, i) => {
          thumb.classList.toggle('active', i === index);
        });
      };

      container.querySelector('.gallery-prev')?.addEventListener('click', () => {
        const newIndex = currentIndex > 0 ? currentIndex - 1 : images.length - 1;
        updateGallery(newIndex);
      });

      container.querySelector('.gallery-next')?.addEventListener('click', () => {
        const newIndex = currentIndex < images.length - 1 ? currentIndex + 1 : 0;
        updateGallery(newIndex);
      });

      indicators.forEach((ind, i) => {
        ind.addEventListener('click', () => updateGallery(i));
      });

      thumbnails.forEach((thumb, i) => {
        thumb.addEventListener('click', () => updateGallery(i));
      });
    }

    // Action buttons
    container.querySelectorAll('.popup-action-btn').forEach((btn: Element) => {
      btn.addEventListener('click', (e: Event) => {
        const index = parseInt((e.currentTarget as HTMLElement).dataset.actionIndex || '0');
        actions[index]?.onClick();
      });
    });
  });

  return popup;
}
```

**CSS**:
```css
/**
 * Rich Media Popup Styles
 *
 * Comprehensive styling for feature-rich map popups.
 * Supports galleries, videos, and interactive elements.
 */

.rich-media-popup-container .leaflet-popup-content-wrapper {
  padding: 0;
  border-radius: var(--radius-lg, 12px);
  overflow: hidden;
  box-shadow: var(--shadow-2xl, 0 25px 50px rgba(0, 0, 0, 0.25));
}

.rich-media-popup-container .leaflet-popup-content {
  margin: 0;
  width: auto !important;
}

.rich-media-popup {
  position: relative;
  background: var(--color-surface, white);
  color: var(--color-text-primary, #1f2937);
}

/* Badge */
.popup-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Gallery */
.popup-gallery {
  position: relative;
  background: var(--color-gray-100, #f3f4f6);
}

.gallery-main {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.gallery-main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  color: var(--color-gray-900, #111827);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 5;
}

.gallery-nav:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
}

.gallery-prev {
  left: 12px;
}

.gallery-next {
  right: 12px;
}

.gallery-indicators {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
  z-index: 5;
}

.gallery-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.gallery-indicator:hover {
  background: rgba(255, 255, 255, 0.8);
}

.gallery-indicator.active {
  background: white;
  width: 24px;
  border-radius: 4px;
}

.gallery-thumbnails {
  display: flex;
  gap: 8px;
  padding: 8px;
  overflow-x: auto;
  scrollbar-width: thin;
}

.gallery-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  opacity: 0.6;
  transition: all 0.2s ease;
  flex-shrink: 0;
  border: 2px solid transparent;
}

.gallery-thumb:hover {
  opacity: 0.8;
}

.gallery-thumb.active {
  opacity: 1;
  border-color: var(--color-primary, #3b82f6);
}

/* Video */
.popup-video {
  background: #000;
}

.popup-video video {
  width: 100%;
  display: block;
}

/* Content */
.popup-content {
  padding: 16px;
}

.popup-header {
  margin-bottom: 12px;
}

.popup-title {
  margin: 0 0 4px;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.popup-subtitle {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.popup-description {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

/* Metadata */
.popup-metadata {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.metadata-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.metadata-icon {
  font-size: 20px;
  line-height: 1;
}

.metadata-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metadata-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.metadata-value {
  font-size: 14px;
  color: var(--color-text-primary);
  font-weight: 500;
}

/* Actions */
.popup-actions {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: var(--color-gray-50, #f9fafb);
  border-top: 1px solid var(--color-border, #e5e7eb);
}

.popup-action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius-md, 6px);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.popup-action-btn.primary {
  background: var(--color-primary, #3b82f6);
  color: white;
}

.popup-action-btn.primary:hover {
  background: var(--color-primary-dark, #2563eb);
  transform: translateY(-1px);
}

.popup-action-btn.secondary {
  background: white;
  color: var(--color-primary);
  border: 1px solid var(--color-border);
}

.popup-action-btn.secondary:hover {
  background: var(--color-gray-100);
}

.action-icon {
  font-size: 16px;
  line-height: 1;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .rich-media-popup {
    background: var(--color-surface-dark, #1f2937);
    color: var(--color-text-primary-dark, #f3f4f6);
  }

  .popup-title {
    color: var(--color-text-primary-dark, #f3f4f6);
  }

  .popup-description {
    color: var(--color-text-secondary-dark, #d1d5db);
  }
}
```

---

## Choropleth Maps

### Data-Driven Choropleth Pattern

**Use Case**: Create choropleth maps with data-driven coloring

**Pattern**:
```typescript
/**
 * Choropleth Map Generator
 *
 * Creates data-driven choropleth maps with custom color scales.
 * Supports multiple interpolation methods and legends.
 *
 * @param geojsonData - GeoJSON data with properties
 * @param config - Choropleth configuration
 * @returns Leaflet GeoJSON layer
 *
 * @example
 * const choropleth = createChoroplethMap(statesData, {
 *   valueProperty: 'population',
 *   colorScale: 'sequential',
 *   colors: ['#ffffcc', '#006837'],
 *   breaks: [0, 1000, 5000, 10000, 50000],
 *   legend: true
 * });
 */
interface ChoroplethConfig {
  valueProperty: string;
  colorScale: 'sequential' | 'diverging' | 'categorical';
  colors: string[];
  breaks?: number[];
  classMethod?: 'equal' | 'quantile' | 'jenks';
  nullColor?: string;
  borderColor?: string;
  borderWidth?: number;
  legend?: boolean;
  legendTitle?: string;
  interactive?: boolean;
}

function createChoroplethMap(
  geojsonData: any,
  config: ChoroplethConfig
): L.GeoJSON {
  const {
    valueProperty,
    colorScale,
    colors,
    breaks,
    classMethod = 'quantile',
    nullColor = '#ccc',
    borderColor = 'white',
    borderWidth = 2,
    legend = false,
    legendTitle = valueProperty,
    interactive = true
  } = config;

  // Calculate breaks if not provided
  const calculatedBreaks = breaks || calculateBreaks(
    geojsonData.features.map((f: any) => f.properties[valueProperty]),
    colors.length,
    classMethod
  );

  /**
   * Get color for a value
   */
  function getColor(value: number | null): string {
    if (value === null || value === undefined) return nullColor;

    for (let i = calculatedBreaks.length - 1; i >= 0; i--) {
      if (value >= calculatedBreaks[i]) {
        return colors[i] || colors[colors.length - 1];
      }
    }

    return colors[0];
  }

  /**
   * Style function
   */
  function style(feature: any): L.PathOptions {
    const value = feature.properties[valueProperty];

    return {
      fillColor: getColor(value),
      weight: borderWidth,
      opacity: 1,
      color: borderColor,
      fillOpacity: 0.7
    };
  }

  // Create GeoJSON layer
  const layer = L.geoJSON(geojsonData, {
    style,
    onEachFeature: (feature, layer) => {
      if (interactive) {
        const value = feature.properties[valueProperty];
        const formattedValue = formatValue(value);

        // Bind popup
        layer.bindPopup(`
          <div class="choropleth-popup">
            <h3>${feature.properties.name || 'Unknown'}</h3>
            <div class="popup-stat">
              <span class="stat-label">${legendTitle}:</span>
              <span class="stat-value">${formattedValue}</span>
            </div>
          </div>
        `);

        // Hover effects
        layer.on({
          mouseover: (e) => {
            const layer = e.target;
            layer.setStyle({
              weight: borderWidth + 2,
              fillOpacity: 0.9
            });
            layer.bringToFront();
          },
          mouseout: (e) => {
            const geoJsonLayer = e.target.feature.layer;
            if (geoJsonLayer) {
              (geoJsonLayer as L.GeoJSON).resetStyle(e.target);
            }
          }
        });
      }
    }
  });

  // Add legend
  if (legend && (window as any).map) {
    addChoroplethLegend((window as any).map, {
      title: legendTitle,
      breaks: calculatedBreaks,
      colors,
      position: 'bottomright'
    });
  }

  return layer;
}

/**
 * Calculate class breaks
 */
function calculateBreaks(
  values: number[],
  numClasses: number,
  method: 'equal' | 'quantile' | 'jenks'
): number[] {
  const validValues = values.filter(v => v !== null && v !== undefined);
  const sorted = validValues.sort((a, b) => a - b);

  if (method === 'equal') {
    const min = sorted[0];
    const max = sorted[sorted.length - 1];
    const interval = (max - min) / numClasses;
    return Array.from({ length: numClasses }, (_, i) => min + (i * interval));
  } else if (method === 'quantile') {
    const breaks: number[] = [];
    for (let i = 0; i < numClasses; i++) {
      const index = Math.floor((sorted.length - 1) * (i / numClasses));
      breaks.push(sorted[index]);
    }
    return breaks;
  }

  // Simplified jenks (would use a proper library in production)
  return calculateBreaks(values, numClasses, 'quantile');
}

/**
 * Format value for display
 */
function formatValue(value: number | null): string {
  if (value === null || value === undefined) return 'N/A';

  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(1)}M`;
  } else if (value >= 1000) {
    return `${(value / 1000).toFixed(1)}K`;
  }

  return value.toLocaleString();
}

/**
 * Add choropleth legend
 */
function addChoroplethLegend(
  map: L.Map,
  config: {
    title: string;
    breaks: number[];
    colors: string[];
    position: L.ControlPosition;
  }
): void {
  const legend = L.control({ position: config.position });

  legend.onAdd = function() {
    const div = L.DomUtil.create('div', 'choropleth-legend');

    div.innerHTML = `
      <h4>${config.title}</h4>
      <div class="legend-items">
        ${config.colors.map((color, i) => {
          const from = formatValue(config.breaks[i]);
          const to = i < config.colors.length - 1
            ? formatValue(config.breaks[i + 1])
            : '+';

          return `
            <div class="legend-item">
              <span class="legend-color" style="background: ${color}"></span>
              <span class="legend-label">${from} ${to !== '+' ? `- ${to}` : to}</span>
            </div>
          `;
        }).join('')}
      </div>
    `;

    L.DomEvent.disableClickPropagation(div);
    return div;
  };

  legend.addTo(map);
}
```

This comprehensive skill library is already at 1,200+ lines. I'll continue with the remaining sections to complete the map-styling-patterns skill. Would you like me to:

1. Complete this skill with remaining patterns (Heat Maps, Performance, Accessibility, etc.)
2. Move to create the next skills (leaflet-cookbook, mapbox-recipes)
3. Create the interactive commands

Let me continue to complete this comprehensive skill library!