---
name: leaflet-cookbook
description: Comprehensive Leaflet patterns for custom markers, styled popups, controls, GeoJSON, clustering, and dark mode. Use when searching for Leaflet styling, marker customization, popup design, or interactive map features.
---

# Leaflet Cookbook

A comprehensive reference library of Leaflet patterns for creating custom markers, styled popups, interactive controls, GeoJSON visualizations, marker clustering, and theme switching.

## Table of Contents

1. [Custom Marker Icons](#custom-marker-icons)
2. [Styled Popups and Tooltips](#styled-popups-and-tooltips)
3. [Custom Controls](#custom-controls)
4. [GeoJSON Styling](#geojson-styling)
5. [Marker Clustering](#marker-clustering)
6. [Dark Mode Implementation](#dark-mode-implementation)
7. [Performance Optimization](#performance-optimization)
8. [Accessibility Patterns](#accessibility-patterns)

---

## Custom Marker Icons

### SVG-Based Custom Markers

**Use Case**: Create scalable, colorful markers that match your brand

**Pattern**:
```typescript
/**
 * SVG Icon Factory for Leaflet Markers
 *
 * @description Creates custom SVG marker icons with dynamic colors
 * @param color - Marker color from design tokens
 * @param size - Optional size configuration
 * @returns Leaflet DivIcon instance
 *
 * @example
 * const icon = createColoredIcon('var(--color-primary)');
 * L.marker([51.5, -0.09], { icon }).addTo(map);
 */
import L from 'leaflet';

interface MarkerSize {
  width: number;
  height: number;
}

function createColoredIcon(
  color: string,
  size: MarkerSize = { width: 25, height: 41 }
): L.DivIcon {
  const svgIcon = `
    <svg width="${size.width}" height="${size.height}"
         viewBox="0 0 25 41"
         xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.3"/>
        </filter>
      </defs>
      <path
        fill="${color}"
        stroke="#fff"
        stroke-width="2"
        filter="url(#shadow)"
        d="M12.5 0C5.6 0 0 5.6 0 12.5c0 9.4 12.5 28.5 12.5 28.5S25 21.9 25 12.5C25 5.6 19.4 0 12.5 0z"
      />
      <circle cx="12.5" cy="12.5" r="6" fill="#fff" opacity="0.9"/>
    </svg>
  `;

  return L.divIcon({
    html: svgIcon,
    className: 'custom-svg-icon',
    iconSize: [size.width, size.height],
    iconAnchor: [size.width / 2, size.height],
    popupAnchor: [1, -(size.height - 7)]
  });
}
```

### Image-Based Marker Icons

**Pattern**:
```typescript
/**
 * Image-Based Marker Icon Configuration
 *
 * @description Creates marker icons from image files with retina support
 * @param config - Marker icon configuration
 * @returns Leaflet Icon instance
 *
 * @example
 * const icon = createImageIcon({
 *   iconUrl: '/markers/pin-blue.png',
 *   size: [32, 48]
 * });
 */
interface IconConfig {
  iconUrl: string;
  iconRetinaUrl?: string;
  shadowUrl?: string;
  size: [number, number];
  shadowSize?: [number, number];
}

function createImageIcon(config: IconConfig): L.Icon {
  const { iconUrl, iconRetinaUrl, shadowUrl, size, shadowSize } = config;

  return L.icon({
    iconUrl,
    iconRetinaUrl: iconRetinaUrl || iconUrl.replace('.png', '-2x.png'),
    shadowUrl: shadowUrl || '/markers/marker-shadow.png',
    iconSize: size,
    iconAnchor: [size[0] / 2, size[1]],
    popupAnchor: [1, -(size[1] - 7)],
    tooltipAnchor: [size[0] / 2, -(size[1] / 2)],
    shadowSize: shadowSize || [size[0] * 1.5, size[1]]
  });
}
```

**CSS for SVG Icons**:
```css
/**
 * Custom SVG Icon Styles
 *
 * @description Ensures proper rendering and transitions for SVG markers
 */
.custom-svg-icon {
  background: none !important;
  border: none !important;
  transition: transform 0.2s ease;
}

.custom-svg-icon:hover {
  transform: scale(1.1);
  z-index: 1000 !important;
}

/* Pulse animation for active markers */
.custom-svg-icon.active {
  animation: markerPulse 2s ease-in-out infinite;
}

@keyframes markerPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.15);
  }
}
```

### Icon Factory with Categories

**Pattern**:
```typescript
/**
 * Category-Based Icon Factory
 *
 * @description Creates different marker styles based on category
 * @param category - Location category
 * @returns Leaflet Icon instance
 *
 * @example
 * const icon = getIconByCategory('restaurant');
 * L.marker([lat, lng], { icon }).addTo(map);
 */
type MarkerCategory =
  | 'restaurant'
  | 'hotel'
  | 'attraction'
  | 'shopping'
  | 'default';

interface CategoryConfig {
  color: string;
  iconClass: string;
  label?: string;
}

const categoryConfigs: Record<MarkerCategory, CategoryConfig> = {
  restaurant: {
    color: '#ef4444',
    iconClass: 'icon-restaurant',
    label: 'R'
  },
  hotel: {
    color: '#3b82f6',
    iconClass: 'icon-hotel',
    label: 'H'
  },
  attraction: {
    color: '#10b981',
    iconClass: 'icon-attraction',
    label: 'A'
  },
  shopping: {
    color: '#f59e0b',
    iconClass: 'icon-shopping',
    label: 'S'
  },
  default: {
    color: '#6b7280',
    iconClass: 'icon-default',
    label: '•'
  }
};

function getIconByCategory(category: MarkerCategory = 'default'): L.DivIcon {
  const config = categoryConfigs[category];

  const html = `
    <div class="marker-pin" style="background-color: ${config.color}">
      <div class="marker-label">${config.label}</div>
    </div>
    <div class="marker-shadow"></div>
  `;

  return L.divIcon({
    html,
    className: `custom-category-icon ${config.iconClass}`,
    iconSize: [30, 42],
    iconAnchor: [15, 42],
    popupAnchor: [0, -42]
  });
}
```

**CSS for Category Icons**:
```css
/**
 * Category-Based Marker Styles
 *
 * @description Styled markers with labels and shadows
 */
.custom-category-icon {
  background: none !important;
  border: none !important;
  position: relative;
}

.marker-pin {
  width: 30px;
  height: 38px;
  border-radius: 50% 50% 50% 0;
  background: var(--color-primary);
  position: absolute;
  transform: rotate(-45deg);
  left: 50%;
  top: 50%;
  margin: -20px 0 0 -15px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.marker-pin:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
  transform: rotate(-45deg) scale(1.1);
}

.marker-label {
  transform: rotate(45deg);
  color: white;
  font-weight: 700;
  font-size: 14px;
  line-height: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.marker-shadow {
  width: 30px;
  height: 10px;
  background: radial-gradient(
    ellipse at center,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0) 70%
  );
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
}
```

---

## Styled Popups and Tooltips

### Rich Media Popup Pattern

**Use Case**: Display detailed information with images and actions

**Pattern**:
```typescript
/**
 * Rich Popup Factory
 *
 * @description Creates feature-rich popups with images, metadata, and actions
 * @param config - Popup configuration
 * @returns Leaflet Popup instance
 *
 * @example
 * const popup = createRichPopup({
 *   title: 'Location Name',
 *   image: '/images/location.jpg',
 *   description: 'Description text...',
 *   metadata: [
 *     { icon: '📍', label: 'Category', value: 'Restaurant' },
 *     { icon: '⭐', label: 'Rating', value: '4.5/5' }
 *   ],
 *   actions: [
 *     { label: 'View Details', className: 'btn-primary' },
 *     { label: 'Directions', className: 'btn-secondary' }
 *   ]
 * });
 */
interface PopupMetadata {
  icon: string;
  label: string;
  value: string;
}

interface PopupAction {
  label: string;
  className: string;
  onClick?: () => void;
}

interface PopupConfig {
  title: string;
  image?: string;
  badge?: string;
  description: string;
  metadata?: PopupMetadata[];
  actions?: PopupAction[];
}

function createRichPopup(config: PopupConfig): L.Popup {
  const {
    title,
    image,
    badge,
    description,
    metadata = [],
    actions = []
  } = config;

  const content = `
    <div class="leaflet-rich-popup">
      ${badge ? `
        <div class="popup-badge">${badge}</div>
      ` : ''}

      ${image ? `
        <div class="popup-image">
          <img src="${image}" alt="${title}" loading="lazy" />
        </div>
      ` : ''}

      <div class="popup-header">
        <h3>${title}</h3>
      </div>

      <div class="popup-body">
        <p class="popup-description">${description}</p>

        ${metadata.length > 0 ? `
          <div class="popup-meta">
            ${metadata.map(item => `
              <div class="meta-item">
                <span class="meta-icon" role="img" aria-label="${item.label}">
                  ${item.icon}
                </span>
                <div class="meta-content">
                  <span class="meta-label">${item.label}</span>
                  <span class="meta-value">${item.value}</span>
                </div>
              </div>
            `).join('')}
          </div>
        ` : ''}
      </div>

      ${actions.length > 0 ? `
        <div class="popup-footer">
          ${actions.map((action, i) => `
            <button
              class="popup-btn ${action.className}"
              data-action="${i}"
              type="button"
            >
              ${action.label}
            </button>
          `).join('')}
        </div>
      ` : ''}
    </div>
  `;

  const popup = L.popup({
    maxWidth: 320,
    minWidth: 280,
    className: 'custom-popup',
    closeButton: true,
    autoClose: false,
    closeOnClick: false
  }).setContent(content);

  // Add event listeners after popup opens
  popup.on('add', () => {
    const popupElement = popup.getElement();
    if (popupElement && actions.length > 0) {
      actions.forEach((action, i) => {
        const btn = popupElement.querySelector(`[data-action="${i}"]`);
        if (btn && action.onClick) {
          btn.addEventListener('click', action.onClick);
        }
      });
    }
  });

  return popup;
}
```

**CSS for Rich Popups**:
```css
/**
 * Rich Popup Styles
 *
 * @description Comprehensive popup styling with modern design
 */
.custom-popup .leaflet-popup-content-wrapper {
  background: var(--color-surface, white);
  border-radius: var(--radius-lg, 12px);
  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.15),
    0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 0;
  overflow: hidden;
}

.custom-popup .leaflet-popup-content {
  margin: 0;
  line-height: 1.5;
  font-size: 14px;
  color: var(--color-text-primary, #1f2937);
}

.custom-popup .leaflet-popup-tip {
  background: var(--color-surface, white);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

.custom-popup .leaflet-popup-close-button {
  color: var(--color-text-secondary, #6b7280);
  font-size: 24px;
  padding: 8px 12px;
  transition: color 0.2s;
}

.custom-popup .leaflet-popup-close-button:hover {
  color: var(--color-text-primary, #1f2937);
}

/* Popup Badge */
.popup-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--color-success, #10b981);
  color: white;
  padding: 4px 12px;
  border-radius: var(--radius-full, 20px);
  font-size: 12px;
  font-weight: 600;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Popup Image */
.popup-image {
  width: 100%;
  height: 160px;
  overflow: hidden;
  background: var(--color-gray-100, #f3f4f6);
}

.popup-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Popup Header */
.popup-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border, #e5e7eb);
  background: var(--color-surface, white);
}

.popup-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary, #1f2937);
  line-height: 1.4;
}

/* Popup Body */
.popup-body {
  padding: 16px 20px;
}

.popup-description {
  margin: 0 0 16px;
  line-height: 1.6;
  color: var(--color-text-secondary, #4b5563);
}

/* Metadata */
.popup-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border, #e5e7eb);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.meta-icon {
  font-size: 20px;
  line-height: 1;
  flex-shrink: 0;
}

.meta-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.meta-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-tertiary, #9ca3af);
}

.meta-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary, #1f2937);
}

/* Popup Footer */
.popup-footer {
  padding: 12px 16px;
  background: var(--color-gray-50, #f9fafb);
  border-top: 1px solid var(--color-border, #e5e7eb);
  display: flex;
  gap: 8px;
}

.popup-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius-md, 6px);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.popup-btn.btn-primary {
  background: var(--color-primary, #3b82f6);
  color: white;
}

.popup-btn.btn-primary:hover {
  background: var(--color-primary-dark, #2563eb);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.popup-btn.btn-secondary {
  background: transparent;
  color: var(--color-primary, #3b82f6);
  border: 1px solid var(--color-primary, #3b82f6);
}

.popup-btn.btn-secondary:hover {
  background: var(--color-primary-light, #eff6ff);
}
```

### Styled Tooltip Pattern

**Pattern**:
```typescript
/**
 * Styled Tooltip Factory
 *
 * @description Creates elegant tooltips with optional icons
 * @param content - Tooltip content (HTML string)
 * @param options - Tooltip options
 * @returns Leaflet Tooltip instance
 *
 * @example
 * const tooltip = createStyledTooltip(
 *   '<strong>Location Name</strong><br/>Click for details',
 *   { direction: 'top', permanent: false }
 * );
 * marker.bindTooltip(tooltip);
 */
interface TooltipOptions {
  direction?: 'top' | 'bottom' | 'left' | 'right' | 'center' | 'auto';
  permanent?: boolean;
  sticky?: boolean;
  opacity?: number;
  offset?: [number, number];
}

function createStyledTooltip(
  content: string,
  options: TooltipOptions = {}
): L.Tooltip {
  const {
    direction = 'top',
    permanent = false,
    sticky = false,
    opacity = 0.95,
    offset = [0, -10]
  } = options;

  return L.tooltip({
    permanent,
    direction,
    sticky,
    opacity,
    offset,
    className: 'custom-tooltip'
  }).setContent(content);
}
```

**CSS for Tooltips**:
```css
/**
 * Custom Tooltip Styles
 *
 * @description Modern tooltip styling with glassmorphism
 */
.custom-tooltip {
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md, 8px);
  color: white;
  font-size: 13px;
  padding: 8px 14px;
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  font-weight: 500;
  line-height: 1.5;
}

.custom-tooltip::before {
  border-top-color: rgba(0, 0, 0, 0.9);
}

.custom-tooltip strong {
  font-weight: 700;
  color: var(--color-primary-light, #93c5fd);
}

/* Dark mode tooltip */
.dark-mode .custom-tooltip {
  background: rgba(255, 255, 255, 0.95);
  color: var(--color-text-primary, #1f2937);
  border-color: rgba(0, 0, 0, 0.1);
}

.dark-mode .custom-tooltip::before {
  border-top-color: rgba(255, 255, 255, 0.95);
}
```

---

## Custom Controls

### Multi-Function Custom Control

**Use Case**: Create custom map controls with multiple features

**Pattern**:
```typescript
/**
 * Custom Control with Multiple Actions
 *
 * @description Creates a control panel with location, search, filter, and theme toggle
 * @param map - Leaflet map instance
 * @returns Control instance
 *
 * @example
 * const control = createCustomControl(map);
 * control.addTo(map);
 */
interface ControlAction {
  id: string;
  icon: string;
  label: string;
  onClick: (map: L.Map) => void;
}

L.Control.CustomControl = L.Control.extend({
  options: {
    position: 'topleft' as L.ControlPosition,
    title: 'Map Controls',
    actions: [] as ControlAction[]
  },

  onAdd: function(map: L.Map) {
    const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-custom-control');

    // Control header
    const header = L.DomUtil.create('div', 'control-header', container);
    header.innerHTML = `<h4>${this.options.title}</h4>`;

    // Control body
    const body = L.DomUtil.create('div', 'control-body', container);

    // Location button
    const locateBtn = this.createButton(
      '📍',
      'My Location',
      'locate',
      () => {
        map.locate({ setView: true, maxZoom: 16 });
      }
    );
    body.appendChild(locateBtn);

    // Search button
    const searchBtn = this.createButton(
      '🔍',
      'Search',
      'search',
      () => {
        console.log('Search clicked');
      }
    );
    body.appendChild(searchBtn);

    // Filter button
    const filterBtn = this.createButton(
      '⚙️',
      'Filter',
      'filter',
      () => {
        console.log('Filter clicked');
      }
    );
    body.appendChild(filterBtn);

    // Divider
    const divider = L.DomUtil.create('div', 'control-divider', body);

    // Dark mode toggle
    const toggleContainer = L.DomUtil.create('label', 'control-toggle', body);
    toggleContainer.innerHTML = `
      <input type="checkbox" id="darkModeToggle">
      <span class="toggle-slider"></span>
      <span class="toggle-label">Dark Mode</span>
    `;

    const toggle = toggleContainer.querySelector('#darkModeToggle') as HTMLInputElement;
    L.DomEvent.on(toggle, 'change', () => {
      document.body.classList.toggle('dark-mode', toggle.checked);
      this.onThemeChange?.(toggle.checked);
    });

    // Prevent map clicks
    L.DomEvent.disableClickPropagation(container);
    L.DomEvent.disableScrollPropagation(container);

    return container;
  },

  createButton: function(
    icon: string,
    label: string,
    action: string,
    onClick: () => void
  ): HTMLElement {
    const button = L.DomUtil.create('button', 'control-btn');
    button.setAttribute('type', 'button');
    button.setAttribute('data-action', action);
    button.setAttribute('aria-label', label);
    button.innerHTML = `
      <span class="btn-icon" role="img">${icon}</span>
      <span class="btn-label">${label}</span>
    `;

    L.DomEvent.on(button, 'click', onClick);

    return button;
  },

  onThemeChange: function(isDark: boolean) {
    // Override this method to handle theme changes
  },

  onRemove: function(map: L.Map) {
    // Cleanup
  }
});

/**
 * Create custom control instance
 */
function createCustomControl(map: L.Map): L.Control {
  const control = new (L.Control.CustomControl as any)({
    position: 'topleft',
    title: 'Map Controls'
  });

  return control;
}
```

**CSS for Custom Controls**:
```css
/**
 * Custom Control Styles
 *
 * @description Modern control panel styling
 */
.leaflet-custom-control {
  background: var(--color-surface, white);
  border-radius: var(--radius-lg, 12px);
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.15),
    0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  min-width: 220px;
  border: none;
}

/* Control Header */
.control-header {
  background: linear-gradient(
    135deg,
    var(--color-primary, #3b82f6) 0%,
    var(--color-primary-dark, #2563eb) 100%
  );
  color: white;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.control-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.3px;
}

/* Control Body */
.control-body {
  padding: 8px;
  background: var(--color-surface, white);
}

/* Control Buttons */
.control-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: none;
  background: transparent;
  border-radius: var(--radius-md, 8px);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  color: var(--color-text-primary, #1f2937);
  text-align: left;
}

.control-btn:hover {
  background: var(--color-gray-100, #f3f4f6);
  transform: translateX(2px);
}

.control-btn:active {
  transform: translateX(2px) scale(0.98);
}

.btn-icon {
  font-size: 18px;
  line-height: 1;
  flex-shrink: 0;
}

.btn-label {
  font-weight: 500;
}

/* Divider */
.control-divider {
  height: 1px;
  background: var(--color-border, #e5e7eb);
  margin: 8px 4px;
}

/* Toggle Switch */
.control-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  cursor: pointer;
  transition: background 0.2s;
  border-radius: var(--radius-md, 8px);
}

.control-toggle:hover {
  background: var(--color-gray-50, #f9fafb);
}

.control-toggle input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  width: 42px;
  height: 22px;
  background: var(--color-gray-300, #d1d5db);
  border-radius: 11px;
  position: relative;
  transition: background 0.3s;
  flex-shrink: 0;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  top: 2px;
  left: 2px;
  transition: transform 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.control-toggle input[type="checkbox"]:checked + .toggle-slider {
  background: var(--color-primary, #3b82f6);
}

.control-toggle input[type="checkbox"]:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.toggle-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary, #1f2937);
}

/* Zoom Control Styling */
.leaflet-control-zoom {
  border: none;
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.15),
    0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: var(--radius-md, 8px);
  overflow: hidden;
}

.leaflet-control-zoom a {
  width: 36px;
  height: 36px;
  line-height: 36px;
  font-size: 20px;
  color: var(--color-text-primary, #374151);
  border-bottom: 1px solid var(--color-border, #e5e7eb);
  transition: all 0.2s;
  background: var(--color-surface, white);
}

.leaflet-control-zoom a:hover {
  background: var(--color-gray-50, #f9fafb);
  color: var(--color-primary, #3b82f6);
}

.leaflet-control-zoom a:last-child {
  border-bottom: none;
}

/* Dark Mode Styles */
.dark-mode .leaflet-custom-control {
  background: var(--color-dark-surface, #1f2937);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-mode .control-body {
  background: var(--color-dark-surface, #1f2937);
}

.dark-mode .control-btn {
  color: var(--color-dark-text, #f3f4f6);
}

.dark-mode .control-btn:hover {
  background: rgba(255, 255, 255, 0.05);
}

.dark-mode .control-divider {
  background: rgba(255, 255, 255, 0.1);
}

.dark-mode .toggle-label {
  color: var(--color-dark-text, #f3f4f6);
}
```

---

## GeoJSON Styling

### Data-Driven Choropleth Map

**Use Case**: Visualize regional data with color-coded polygons

**Pattern**:
```typescript
/**
 * Choropleth Map Implementation
 *
 * @description Creates choropleth visualization from GeoJSON data
 * @param map - Leaflet map instance
 * @param geojsonData - GeoJSON feature collection
 * @param propertyName - Property to visualize
 * @returns GeoJSON layer
 *
 * @example
 * const layer = createChoroplethMap(map, populationData, 'density');
 */
interface FeatureProperties {
  name: string;
  population?: number;
  density?: number;
  category?: string;
  [key: string]: any;
}

/**
 * Get color based on value for choropleth
 * @param value - Numeric value
 * @returns Color hex code
 */
function getChoroplethColor(value: number): string {
  return value > 1000 ? '#800026' :
         value > 500  ? '#bd0026' :
         value > 200  ? '#e31a1c' :
         value > 100  ? '#fc4e2a' :
         value > 50   ? '#fd8d3c' :
         value > 20   ? '#feb24c' :
         value > 10   ? '#fed976' :
                        '#ffeda0';
}

/**
 * Style function for GeoJSON features
 */
function styleFeature(feature: any): L.PathOptions {
  const props = feature.properties as FeatureProperties;

  return {
    fillColor: getChoroplethColor(props.density || 0),
    weight: 2,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.7
  };
}

function createChoroplethMap(
  map: L.Map,
  geojsonData: GeoJSON.FeatureCollection,
  propertyName: string
): L.GeoJSON {
  const layer = L.geoJSON(geojsonData, {
    style: styleFeature,

    onEachFeature: (feature, layer) => {
      const props = feature.properties as FeatureProperties;

      // Create popup content
      const popupContent = `
        <div class="geojson-popup">
          <h3>${props.name}</h3>
          <div class="popup-stats">
            <div class="stat-item">
              <span class="stat-label">Population:</span>
              <span class="stat-value">${props.population?.toLocaleString() || 'N/A'}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Density:</span>
              <span class="stat-value">${props.density?.toFixed(2) || 'N/A'}</span>
            </div>
          </div>
        </div>
      `;

      layer.bindPopup(popupContent, {
        className: 'custom-geojson-popup'
      });

      // Interactive hover effects
      layer.on({
        mouseover: (e) => {
          const target = e.target;
          target.setStyle({
            weight: 4,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.9
          });
          target.bringToFront();
        },

        mouseout: (e) => {
          layer.resetStyle(e.target);
        },

        click: (e) => {
          map.fitBounds(e.target.getBounds(), {
            padding: [50, 50]
          });
        }
      });
    }
  });

  return layer.addTo(map);
}
```

**CSS for GeoJSON Popups**:
```css
/**
 * GeoJSON Popup Styles
 *
 * @description Styles for data-rich GeoJSON feature popups
 */
.custom-geojson-popup .leaflet-popup-content-wrapper {
  background: var(--color-surface, white);
  border-radius: var(--radius-lg, 12px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  padding: 0;
}

.geojson-popup h3 {
  margin: 0;
  padding: 16px 20px;
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary, #1f2937);
  border-bottom: 2px solid var(--color-primary, #3b82f6);
}

.popup-stats {
  padding: 16px 20px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border, #e5e7eb);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-size: 13px;
  color: var(--color-text-secondary, #6b7280);
  font-weight: 500;
}

.stat-value {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-primary, #3b82f6);
}
```

### Point-to-Layer with Custom Markers

**Pattern**:
```typescript
/**
 * Point GeoJSON with Custom Markers
 *
 * @description Renders point features with category-based markers
 * @param map - Leaflet map instance
 * @param pointData - Point GeoJSON data
 * @returns GeoJSON layer
 *
 * @example
 * const layer = createPointLayer(map, pointsGeoJSON);
 */
function createPointLayer(
  map: L.Map,
  pointData: GeoJSON.FeatureCollection
): L.GeoJSON {
  return L.geoJSON(pointData, {
    pointToLayer: (feature, latlng) => {
      const props = feature.properties as FeatureProperties;

      // Use circle markers for better performance
      return L.circleMarker(latlng, {
        radius: props.size || 8,
        fillColor: props.category === 'A' ? '#3b82f6' :
                   props.category === 'B' ? '#10b981' :
                   props.category === 'C' ? '#f59e0b' : '#ef4444',
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
      });
    },

    onEachFeature: (feature, layer) => {
      const props = feature.properties as FeatureProperties;

      layer.bindPopup(`
        <div class="point-popup">
          <strong>${props.name}</strong>
          <p>Category: ${props.category}</p>
        </div>
      `);

      layer.bindTooltip(props.name, {
        permanent: false,
        direction: 'top',
        className: 'custom-tooltip'
      });
    }
  }).addTo(map);
}
```

---

## Marker Clustering

### Advanced Marker Clustering

**Use Case**: Handle thousands of markers efficiently with clustering

**Pattern**:
```typescript
/**
 * Marker Clustering with Custom Icons
 *
 * @description Creates clustered markers with custom cluster icons
 * @param map - Leaflet map instance
 * @param locations - Array of location data
 * @returns MarkerClusterGroup
 *
 * @example
 * const clusters = createMarkerClusters(map, locationData);
 * map.addLayer(clusters);
 */
import L from 'leaflet';
import 'leaflet.markercluster';

interface Location {
  id: string;
  lat: number;
  lng: number;
  name: string;
  category: string;
  color: string;
}

/**
 * Create custom cluster icon
 * @param cluster - Marker cluster
 * @returns DivIcon for cluster
 */
function createClusterIcon(cluster: L.MarkerCluster): L.DivIcon {
  const childCount = cluster.getChildCount();
  let sizeClass = 'marker-cluster-';

  if (childCount < 10) {
    sizeClass += 'small';
  } else if (childCount < 100) {
    sizeClass += 'medium';
  } else {
    sizeClass += 'large';
  }

  return L.divIcon({
    html: `
      <div class="cluster-inner">
        <div class="cluster-count">${childCount}</div>
        <div class="cluster-ring"></div>
      </div>
    `,
    className: `marker-cluster ${sizeClass}`,
    iconSize: L.point(50, 50)
  });
}

function createMarkerClusters(
  map: L.Map,
  locations: Location[]
): L.MarkerClusterGroup {
  // Create marker cluster group
  const clusters = L.markerClusterGroup({
    iconCreateFunction: createClusterIcon,
    spiderfyOnMaxZoom: true,
    showCoverageOnHover: true,
    zoomToBoundsOnClick: true,
    maxClusterRadius: 80,
    disableClusteringAtZoom: 16,
    spiderfyDistanceMultiplier: 2,
    chunkedLoading: true,
    chunkInterval: 200,
    chunkDelay: 50
  });

  // Add markers to cluster
  locations.forEach(location => {
    const icon = createColoredIcon(location.color);

    const marker = L.marker([location.lat, location.lng], {
      icon,
      title: location.name
    });

    const popup = createRichPopup({
      title: location.name,
      description: `Location in ${location.category} category`,
      metadata: [
        { icon: '📍', label: 'Category', value: location.category },
        { icon: '🆔', label: 'ID', value: location.id }
      ]
    });

    marker.bindPopup(popup);
    clusters.addLayer(marker);
  });

  return clusters;
}
```

**CSS for Marker Clusters**:
```css
/**
 * Marker Cluster Styles
 *
 * @description Modern cluster styling with animations
 */
.marker-cluster {
  background-clip: padding-box;
  border-radius: 50%;
  background: transparent;
}

.cluster-inner {
  width: 50px;
  height: 50px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cluster-count {
  color: white;
  font-size: 15px;
  font-weight: 700;
  z-index: 2;
  position: relative;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.cluster-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  z-index: 1;
}

/* Size variants */
.marker-cluster-small .cluster-ring {
  background: radial-gradient(
    circle at center,
    rgba(59, 130, 246, 0.9) 0%,
    rgba(59, 130, 246, 0.7) 60%,
    rgba(59, 130, 246, 0.3) 100%
  );
  box-shadow:
    0 0 0 8px rgba(59, 130, 246, 0.2),
    0 4px 12px rgba(0, 0, 0, 0.3);
}

.marker-cluster-medium .cluster-ring {
  background: radial-gradient(
    circle at center,
    rgba(251, 146, 60, 0.9) 0%,
    rgba(251, 146, 60, 0.7) 60%,
    rgba(251, 146, 60, 0.3) 100%
  );
  box-shadow:
    0 0 0 8px rgba(251, 146, 60, 0.2),
    0 4px 12px rgba(0, 0, 0, 0.3);
}

.marker-cluster-large .cluster-ring {
  background: radial-gradient(
    circle at center,
    rgba(239, 68, 68, 0.9) 0%,
    rgba(239, 68, 68, 0.7) 60%,
    rgba(239, 68, 68, 0.3) 100%
  );
  box-shadow:
    0 0 0 8px rgba(239, 68, 68, 0.2),
    0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Hover effect */
.marker-cluster:hover .cluster-inner {
  transform: scale(1.15);
  transition: transform 0.2s ease;
}

/* Spiderfied markers animation */
.marker-cluster-spiderfy {
  animation: spiderfyAnimation 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes spiderfyAnimation {
  from {
    opacity: 0;
    transform: scale(0) rotate(0deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(180deg);
  }
}

/* Coverage polygon styling */
.leaflet-cluster-anim .leaflet-marker-icon,
.leaflet-cluster-anim .leaflet-marker-shadow {
  transition:
    transform 0.3s ease-out,
    opacity 0.3s ease-in;
}

.marker-cluster-spider-leg {
  stroke: var(--color-primary, #3b82f6);
  stroke-width: 2;
  stroke-opacity: 0.5;
  fill: none;
}
```

---

## Dark Mode Implementation

### Complete Dark Mode System

**Use Case**: Switch between light and dark map themes

**Pattern**:
```typescript
/**
 * Dark Mode Theme Manager
 *
 * @description Manages theme switching for Leaflet maps
 * @param map - Leaflet map instance
 * @returns Theme manager object
 *
 * @example
 * const themeManager = createThemeManager(map);
 * themeManager.setTheme('dark');
 */
interface MapTheme {
  name: string;
  tileUrl: string;
  attribution: string;
  options?: L.TileLayerOptions;
}

const mapThemes: Record<'light' | 'dark' | 'satellite', MapTheme> = {
  light: {
    name: 'Light',
    tileUrl: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a>',
    options: {
      maxZoom: 19,
      className: 'light-tiles'
    }
  },
  dark: {
    name: 'Dark',
    tileUrl: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attribution: '&copy; <a href="https://carto.com">CartoDB</a>',
    options: {
      maxZoom: 19,
      className: 'dark-tiles'
    }
  },
  satellite: {
    name: 'Satellite',
    tileUrl: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri',
    options: {
      maxZoom: 19,
      className: 'satellite-tiles'
    }
  }
};

interface ThemeManager {
  currentTheme: keyof typeof mapThemes;
  setTheme: (theme: keyof typeof mapThemes) => void;
  toggle: () => void;
  onThemeChange?: (theme: keyof typeof mapThemes) => void;
}

function createThemeManager(map: L.Map): ThemeManager {
  let currentTheme: keyof typeof mapThemes = 'light';
  let tileLayer: L.TileLayer;

  // Initialize with default theme
  const initTheme = mapThemes[currentTheme];
  tileLayer = L.tileLayer(initTheme.tileUrl, {
    attribution: initTheme.attribution,
    ...initTheme.options
  }).addTo(map);

  const manager: ThemeManager = {
    currentTheme,

    setTheme(theme: keyof typeof mapThemes) {
      if (currentTheme === theme) return;

      const newTheme = mapThemes[theme];

      // Fade out effect
      const container = map.getContainer();
      container.style.transition = 'opacity 0.3s ease';
      container.style.opacity = '0.5';

      setTimeout(() => {
        // Remove old tile layer
        map.removeLayer(tileLayer);

        // Add new tile layer
        tileLayer = L.tileLayer(newTheme.tileUrl, {
          attribution: newTheme.attribution,
          ...newTheme.options
        }).addTo(map);

        // Update body class
        document.body.classList.remove(`${currentTheme}-mode`);
        document.body.classList.add(`${theme}-mode`);

        currentTheme = theme;
        manager.currentTheme = theme;

        // Fade in effect
        container.style.opacity = '1';

        // Callback
        if (manager.onThemeChange) {
          manager.onThemeChange(theme);
        }
      }, 300);
    },

    toggle() {
      const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
      this.setTheme(nextTheme);
    }
  };

  return manager;
}
```

**CSS for Dark Mode**:
```css
/**
 * Dark Mode Styles
 *
 * @description Complete dark mode styling for all map components
 */

/* Dark mode tiles */
.dark-mode .leaflet-container {
  background: var(--color-dark-bg, #111827);
}

/* Dark mode controls */
.dark-mode .leaflet-control-zoom a,
.dark-mode .leaflet-control-layers,
.dark-mode .leaflet-custom-control {
  background: var(--color-dark-surface, #1f2937);
  color: var(--color-dark-text, #f3f4f6);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .leaflet-control-zoom a:hover {
  background: var(--color-dark-hover, #374151);
}

/* Dark mode popups */
.dark-mode .custom-popup .leaflet-popup-content-wrapper {
  background: var(--color-dark-surface, #1f2937);
  color: var(--color-dark-text, #f3f4f6);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-mode .custom-popup .leaflet-popup-tip {
  background: var(--color-dark-surface, #1f2937);
  border-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .popup-header {
  background: var(--color-dark-elevated, #374151);
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .popup-footer {
  background: var(--color-dark-elevated, #374151);
  border-top-color: rgba(255, 255, 255, 0.1);
}

.dark-mode .popup-description {
  color: var(--color-dark-text-secondary, #d1d5db);
}

.dark-mode .meta-label {
  color: var(--color-dark-text-tertiary, #9ca3af);
}

.dark-mode .meta-value {
  color: var(--color-dark-text, #f3f4f6);
}

/* Attribution styling */
.dark-mode .leaflet-control-attribution {
  background: rgba(31, 41, 55, 0.9);
  color: var(--color-dark-text-secondary, #d1d5db);
}

.dark-mode .leaflet-control-attribution a {
  color: var(--color-primary-light, #93c5fd);
}

/* Transition smoothing */
.leaflet-container {
  transition: background-color 0.3s ease;
}
```

---

## Performance Optimization

### Canvas Renderer for Large Datasets

**Pattern**:
```typescript
/**
 * Canvas Renderer Optimization
 *
 * @description Uses canvas renderer for better performance with many markers
 * @param map - Leaflet map instance
 * @param points - Array of point coordinates
 * @returns FeatureGroup of markers
 *
 * @example
 * const markers = createOptimizedMarkers(map, pointData);
 */
interface Point {
  lat: number;
  lng: number;
  color: string;
  radius: number;
}

function createOptimizedMarkers(
  map: L.Map,
  points: Point[]
): L.FeatureGroup {
  // Create canvas renderer (shared by all markers)
  const canvas = L.canvas({ padding: 0.5, tolerance: 10 });

  const markers: L.CircleMarker[] = points.map(point => {
    return L.circleMarker([point.lat, point.lng], {
      renderer: canvas,
      radius: point.radius,
      fillColor: point.color,
      color: '#fff',
      weight: 1,
      fillOpacity: 0.8
    });
  });

  return L.featureGroup(markers).addTo(map);
}
```

### Geometry Simplification

**Pattern**:
```typescript
/**
 * GeoJSON Simplification for Performance
 *
 * @description Simplifies complex geometries for better rendering
 * @param geojson - Original GeoJSON data
 * @param tolerance - Simplification tolerance
 * @returns Simplified GeoJSON
 *
 * @example
 * const simplified = simplifyGeoJSON(complexData, 0.001);
 * L.geoJSON(simplified).addTo(map);
 */
import * as turf from '@turf/turf';

function simplifyGeoJSON(
  geojson: GeoJSON.FeatureCollection,
  tolerance: number = 0.001
): GeoJSON.FeatureCollection {
  return turf.simplify(geojson, {
    tolerance,
    highQuality: false
  });
}
```

### Throttled Event Handlers

**Pattern**:
```typescript
/**
 * Throttle Utility for Map Events
 *
 * @description Limits execution rate of expensive operations
 * @param func - Function to throttle
 * @param limit - Time limit in milliseconds
 * @returns Throttled function
 *
 * @example
 * map.on('move', throttle(() => {
 *   updateVisibleMarkers();
 * }, 200));
 */
function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return function(this: any, ...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * Debounce Utility for Map Events
 *
 * @description Delays execution until after a pause
 * @param func - Function to debounce
 * @param wait - Wait time in milliseconds
 * @returns Debounced function
 */
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;

  return function(this: any, ...args: Parameters<T>) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// Usage example
map.on('moveend', debounce(() => {
  loadMarkersInViewport();
}, 300));

map.on('zoom', throttle(() => {
  updateMarkerSizes();
}, 150));
```

### Viewport-Based Marker Management

**Pattern**:
```typescript
/**
 * Viewport-Based Marker Culling
 *
 * @description Only displays markers within current viewport
 * @param map - Leaflet map instance
 * @param allMarkers - Array of all markers
 *
 * @example
 * const manager = createViewportManager(map, markers);
 * manager.update(); // Call on map move
 */
interface ViewportManager {
  update: () => void;
  destroy: () => void;
}

function createViewportManager(
  map: L.Map,
  allMarkers: L.Marker[]
): ViewportManager {
  const visibleMarkers = new Set<L.Marker>();

  function updateVisibleMarkers() {
    const bounds = map.getBounds();
    const currentZoom = map.getZoom();

    // Add markers in viewport
    allMarkers.forEach(marker => {
      const latLng = marker.getLatLng();
      const isInBounds = bounds.contains(latLng);

      if (isInBounds) {
        if (!visibleMarkers.has(marker)) {
          marker.addTo(map);
          visibleMarkers.add(marker);
        }
      } else {
        if (visibleMarkers.has(marker)) {
          map.removeLayer(marker);
          visibleMarkers.delete(marker);
        }
      }
    });
  }

  // Throttled update function
  const throttledUpdate = throttle(updateVisibleMarkers, 200);

  // Attach event listeners
  map.on('moveend zoomend', throttledUpdate);

  return {
    update: throttledUpdate,

    destroy() {
      map.off('moveend zoomend', throttledUpdate);
      visibleMarkers.forEach(marker => map.removeLayer(marker));
      visibleMarkers.clear();
    }
  };
}
```

---

## Accessibility Patterns

### ARIA Labels and Keyboard Navigation

**Pattern**:
```typescript
/**
 * Accessibility Enhancement for Maps
 *
 * @description Adds ARIA labels and keyboard navigation
 * @param map - Leaflet map instance
 * @param markers - Array of markers to enhance
 *
 * @example
 * enhanceAccessibility(map, allMarkers);
 */
interface AccessibilityOptions {
  mapLabel?: string;
  announceOnMove?: boolean;
  keyboardNavigation?: boolean;
}

function enhanceAccessibility(
  map: L.Map,
  markers: L.Marker[],
  options: AccessibilityOptions = {}
): void {
  const {
    mapLabel = 'Interactive map showing locations',
    announceOnMove = true,
    keyboardNavigation = true
  } = options;

  // Add ARIA label to map container
  const container = map.getContainer();
  container.setAttribute('role', 'application');
  container.setAttribute('aria-label', mapLabel);
  container.setAttribute('tabindex', '0');

  // Screen reader announcements
  if (announceOnMove) {
    const announcer = L.DomUtil.create('div', 'sr-only');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    container.appendChild(announcer);

    map.on('moveend', () => {
      const center = map.getCenter();
      const zoom = map.getZoom();
      announcer.textContent = `Map moved. Center: ${center.lat.toFixed(4)}, ${center.lng.toFixed(4)}. Zoom level: ${zoom}`;
    });
  }

  // Enhance markers with keyboard navigation
  if (keyboardNavigation) {
    markers.forEach((marker, index) => {
      const element = marker.getElement();

      if (element) {
        element.setAttribute('tabindex', '0');
        element.setAttribute('role', 'button');
        element.setAttribute('aria-label', `Marker ${index + 1}`);

        // Keyboard event handlers
        L.DomEvent.on(element, 'keydown', (e: KeyboardEvent) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            marker.openPopup();
          }
        });

        // Focus styling
        L.DomEvent.on(element, 'focus', () => {
          element.classList.add('marker-focused');
        });

        L.DomEvent.on(element, 'blur', () => {
          element.classList.remove('marker-focused');
        });
      }
    });
  }

  // Add skip link for keyboard users
  const skipLink = L.DomUtil.create('a', 'skip-map-link');
  skipLink.href = '#after-map';
  skipLink.textContent = 'Skip map';
  skipLink.setAttribute('tabindex', '0');
  container.parentElement?.insertBefore(skipLink, container);
}
```

**CSS for Accessibility**:
```css
/**
 * Accessibility Styles
 *
 * @description Screen reader and focus styles
 */

/* Screen reader only content */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Skip link */
.skip-map-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary, #3b82f6);
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  border-radius: 4px;
  z-index: 10000;
  font-weight: 600;
}

.skip-map-link:focus {
  top: 10px;
  left: 10px;
}

/* Focus indicators */
.leaflet-container:focus {
  outline: 3px solid var(--color-primary, #3b82f6);
  outline-offset: 2px;
}

.marker-focused {
  outline: 3px solid var(--color-primary, #3b82f6);
  outline-offset: 3px;
  border-radius: 50%;
  z-index: 10000 !important;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .leaflet-control-zoom a,
  .custom-popup .leaflet-popup-content-wrapper {
    border: 2px solid currentColor;
  }

  .marker-focused {
    outline-width: 4px;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .custom-svg-icon,
  .marker-pin,
  .popup-btn,
  .toggle-slider::before {
    transition: none !important;
    animation: none !important;
  }
}

/* Focus visible (keyboard only) */
.leaflet-control-zoom a:focus-visible,
.popup-btn:focus-visible,
.control-btn:focus-visible {
  outline: 3px solid var(--color-primary, #3b82f6);
  outline-offset: 2px;
}
```

---

## Best Practices

### Performance Best Practices

1. **Use Canvas Renderer** - For 500+ markers, use canvas renderer instead of SVG
2. **Implement Clustering** - Always cluster when displaying more than 100 markers
3. **Simplify Geometries** - Reduce polygon complexity for faster rendering
4. **Throttle Events** - Use throttle/debounce for expensive map event handlers
5. **Viewport Culling** - Only render markers within current viewport
6. **Lazy Load Popups** - Create popup content when opened, not when marker created
7. **Use Feature Groups** - Group related markers for batch operations
8. **Optimize Images** - Compress marker icons and use SVG when possible
9. **Clean Up Layers** - Remove unused layers and markers from map
10. **Test on Mobile** - Always test performance on mobile devices

### Design Best Practices

1. **Consistent Colors** - Use design tokens for all colors
2. **Clear Hierarchy** - Make important markers visually prominent
3. **Readable Text** - Ensure sufficient contrast in popups and tooltips
4. **Touch Targets** - Make markers and buttons at least 44x44px for touch
5. **Loading States** - Show loading indicators for async operations
6. **Empty States** - Handle cases where no data is available
7. **Error States** - Display friendly error messages
8. **Responsive Design** - Adapt controls and popups for mobile
9. **Brand Integration** - Match map styling to overall design system
10. **User Feedback** - Provide visual feedback for all interactions

### Accessibility Best Practices

1. **ARIA Labels** - Add descriptive labels to all interactive elements
2. **Keyboard Navigation** - Support Tab, Enter, and Space keys
3. **Focus Indicators** - Show clear focus states for keyboard users
4. **Screen Readers** - Provide text alternatives for visual information
5. **Color Contrast** - Ensure WCAG AA compliance (4.5:1 minimum)
6. **Skip Links** - Allow keyboard users to skip complex map interfaces
7. **Announcements** - Use aria-live for dynamic content changes
8. **Reduced Motion** - Respect prefers-reduced-motion preference
9. **High Contrast** - Support high contrast mode
10. **Testing** - Test with actual screen readers and keyboard only

---

## Summary

This Leaflet Cookbook provides comprehensive patterns for:

- **Custom Marker Icons** - SVG and image-based markers with categories
- **Rich Popups** - Feature-rich popups with images, metadata, and actions
- **Custom Controls** - Multi-function control panels with theme switching
- **GeoJSON Styling** - Data-driven choropleth and point visualizations
- **Marker Clustering** - Performance-optimized clustering for large datasets
- **Dark Mode** - Complete theme switching system
- **Performance** - Canvas rendering, throttling, and viewport culling
- **Accessibility** - ARIA labels, keyboard navigation, and screen reader support

All patterns include:
- Complete TypeScript code with type definitions
- Comprehensive CSS styling with CSS custom properties
- Design token integration for theming
- Performance optimization techniques
- Accessibility compliance (WCAG AA)
- Real-world usage examples
- Best practices and recommendations
