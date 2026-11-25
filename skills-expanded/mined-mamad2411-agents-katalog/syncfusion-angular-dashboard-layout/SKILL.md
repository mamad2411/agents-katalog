---
name: syncfusion-angular-dashboard-layout
description: Create responsive grid-based dashboards with draggable, resizable panels. Use this skill when implementing Syncfusion Angular Dashboard Layout, creating customizable dashboard layouts, adding dynamic panels, enabling drag-drop panel repositioning, resizing panels, saving/restoring dashboard states, making dashboards responsive, or styling dashboard components with CSS customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion Angular Dashboard Layout

The **Dashboard Layout** component is a powerful grid-structured layout control that helps you create responsive, interactive dashboards with dynamic panels. Panels can be dragged, resized, added, removed, and their state can be persisted. This skill guides you through all aspects of implementing, configuring, and customizing dashboard layouts in Angular.

## When to Use This Skill

- Creating customizable dashboard layouts with multiple panels
- Implementing drag-and-drop panel repositioning
- Enabling panel resizing in multiple directions
- Dynamically adding or removing dashboard panels
- Making dashboards responsive across device sizes
- Saving and restoring dashboard layout configurations
- Styling dashboard components with CSS customization
- Integrating Syncfusion charts, grids, or other components as panel content

## Component Overview

The Dashboard Layout component provides:
- **Grid-based layout system** with configurable columns and cell dimensions
- **Drag-and-drop** support for reordering panels with visual feedback
- **Resizing** in multiple directions (east, west, north, south, etc.)
- **Floating panels** that automatically fill empty spaces
- **Responsive behavior** with custom media query breakpoints
- **State persistence** through serialize/deserialize methods
- **Dynamic panel management** with add, remove, and move operations
- **Event-driven architecture** for tracking user interactions

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Angular CLI setup and project initialization
- Installing Dashboard Layout package (Ivy and ngcc variants)
- CSS imports and theme configuration
- Two panel definition approaches (HTML attributes vs property binding)
- Basic component rendering and first dashboard creation
- Cell spacing and layout initialization

### Adding and Removing Panels
📄 **Read:** [references/adding-removing-panels.md](references/adding-removing-panels.md)
- Dynamic panel management with addPanel() method
- Removing individual panels with removePanel(id)
- Bulk removal with removeAll() method
- Panel configuration properties for dynamic generation
- Event handling and callbacks for lifecycle management

### Setting Panel Headers
📄 **Read:** [references/panel-headers.md](references/panel-headers.md)
- Configuring panel headers with header property
- Adding titles, labels, and HTML content to headers
- Styling headers with CSS customization
- Embedding Syncfusion components in panel headers
- Header interaction and user experience patterns

### Dragging and Dropping Panels
📄 **Read:** [references/dragging-and-dropping.md](references/dragging-and-dropping.md)
- Default drag-drop behavior and panel collision handling
- Drag events: dragStart, drag, dragStop
- Customizing drag handles with draggableHandle property
- Programmatic panel movement with movePanel(id, row, col)
- Disabling drag functionality with allowDragging
- Touch support and user interaction patterns

### Moving Panels Programmatically
📄 **Read:** [references/moving-panels.md](references/moving-panels.md)
- Using movePanel(id, row, col) to reposition panels
- Moving panels without user interaction
- Tracking panel movements with change events
- Swapping panel positions programmatically
- Panel rearrangement patterns and use cases

### Resizing and Floating Panels
📄 **Read:** [references/resizing-and-floating.md](references/resizing-and-floating.md)
- Enabling panel resizing with allowResizing
- Resize handles in different directions (e-south-east, e-east, e-west, e-north, e-south)
- Resize events: resizeStart, resize, resizeStop
- Programmatic resizing with resizePanel(id, sizeX, sizeY)
- Min and max size constraints (minSizeX, minSizeY, maxSizeX, maxSizeY)
- Floating behavior and automatic panel repositioning
- Disabling floating for fixed grid layouts

### Saving and Restoring State
📄 **Read:** [references/save-restore-state.md](references/save-restore-state.md)
- Serializing dashboard layout with serialize()
- Saving layout state to localStorage, sessionStorage, or backend
- Restoring layouts from persisted configuration
- Implementing layout templates and presets
- State persistence patterns and best practices

### Responsive and Adaptive Design
📄 **Read:** [references/responsive-and-adaptive.md](references/responsive-and-adaptive.md)
- Built-in responsive behavior and auto-adaptation
- Customizing responsive breakpoints with mediaQuery
- Stacked layout on mobile devices (vertical columns)
- Cell aspect ratio configuration with cellAspectRatio
- Testing responsive layouts at different resolutions
- Parent element sizing (percentage vs static dimensions)

### Configuring Cell Spacing
📄 **Read:** [references/cell-spacing-configuration.md](references/cell-spacing-configuration.md)
- Setting [horizontal, vertical] spacing with cellSpacing property
- Adjusting spacing for compact or spacious layouts
- Dynamic spacing adjustment for responsive designs
- Asymmetric spacing patterns for visual hierarchy
- Practical examples: compact dashboards, executive layouts

### Graphical Representation and Grid Lines
📄 **Read:** [references/grid-lines-and-visualization.md](references/grid-lines-and-visualization.md)
- Visualizing grid structure with showGridLines property
- Understanding grid cells, rows, columns, and spacing
- Design-time grid visualization for layout planning
- Debugging panel positioning and sizing
- Best practices for grid line usage

### Right-to-Left Language Support
📄 **Read:** [references/rtl-support.md](references/rtl-support.md)
- Enabling RTL rendering with enableRtl property
- Supporting Arabic, Hebrew, Farsi, and Urdu languages
- Dynamic RTL toggling for language switching
- HTML dir attribute integration
- CSS logical properties for RTL-aware styling
- RTL considerations with drag-drop interactions

### Styling and Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- CSS selectors for customizing panels, headers, and content
- Panel header and content styling (.e-panel-header, .e-panel-content)
- Resize handle customization (.e-resize)
- Dashboard background styling
- Panel positioning and sizing with row, col, sizeX, sizeY properties
- Min/max size constraints and grid structure
- Integrating Syncfusion components (Charts, Grids, Gauges) as panel content
- SystemJS configuration for legacy Angular setups

**For detailed examples and code samples, see:**
- [getting-started.md](references/getting-started.md) - Quick start and basic setup examples
- [Common patterns and implementation examples in specific reference files](references/)

## API Reference

### Component Properties (14 total)

#### Layout Configuration

| Property | Type | Default | Description |
|---|---|---|---|
| `columns` | number | 5 | Number of columns in the grid layout. Panels are positioned within this column-based grid. |
| `cellSpacing` | number[] | [10, 10] | Spacing between panels: [horizontal, vertical] in pixels. Creates visual separation and padding around panels. |
| `cellAspectRatio` | number | Auto (1:1) | Width/height ratio of cells. Example: 100/50 creates cells that are twice as wide as tall. |
| `mediaQuery` | string | 'max-width: 600px' | CSS media query breakpoint for responsive stacked layout. Panels stack vertically below this breakpoint. |
| `showGridLines` | boolean | false | When true, visualizes grid cells and structure for design-time debugging and layout planning. |

#### Interaction Features

| Property | Type | Default | Description |
|---|---|---|---|
| `allowDragging` | boolean | true | Enables/disables panel drag-drop functionality. When true, users can reorder panels by dragging. |
| `allowResizing` | boolean | false | Enables/disables panel resizing. When true, resize handles appear on panel edges. |
| `allowFloating` | boolean | true | Enables/disables floating behavior. When true, panels automatically move upward to fill empty spaces left by moved/resized panels. |
| `resizableHandles` | string[] | ['e-south-east'] | Array of resize handle directions: 'e-south-east', 'e-east', 'e-west', 'e-north', 'e-south', 'e-south-west'. Controls which directions users can resize panels. |
| `draggableHandle` | string | null | CSS selector string for drag handle element. If set, dragging only works when user grabs this specific element (e.g., '.e-panel-header'). |

#### Content and Styling

| Property | Type | Default | Description |
|---|---|---|---|
| `panels` | PanelModel[] | [] | Array of panel configurations defining the dashboard layout structure and content. |
| `enableRtl` | boolean | false | Enables right-to-left rendering for RTL languages (Arabic, Hebrew, Farsi, Urdu). |
| `enableHtmlSanitizer` | boolean | true | Sanitizes HTML content in panels to prevent XSS attacks. Set to false only with trusted content. |
| `enablePersistence` | boolean | false | When true, automatically saves/restores dashboard state in browser storage between page reloads. |

### Panel Properties (13 total)

| Property | Type | Default | Description |
|---|---|---|---|
| **Position & Size** | | | |
| `row` | number | 0 | Starting row position (0-based indexing) in the grid. Determines vertical placement. |
| `col` | number | 0 | Starting column position (0-based indexing) in the grid. Determines horizontal placement. |
| `sizeX` | number | 1 | Width of panel in cells. Example: sizeX=2 spans 2 grid columns. |
| `sizeY` | number | 1 | Height of panel in cells. Example: sizeY=2 spans 2 grid rows. |
| **Size Constraints** | | | |
| `minSizeX` | number | 1 | Minimum width in cells. Prevents panel from being resized smaller than this value. |
| `minSizeY` | number | 1 | Minimum height in cells. Prevents panel from being resized smaller than this value. |
| `maxSizeX` | number | null | Maximum width in cells. Null means no limit. Prevents panel from being resized larger than this value. |
| `maxSizeY` | number | null | Maximum height in cells. Null means no limit. Prevents panel from being resized larger than this value. |
| **Content** | | | |
| `id` | string | '' | Unique identifier for the panel. Required for methods like movePanel(), resizePanel(), removePanel(). |
| `header` | string \| HTMLElement \| Function | undefined | Header/title content. Can be HTML string, DOM element, or function returning content. |
| `content` | string \| HTMLElement \| Function | undefined | Main body content. Can be HTML string, DOM element, or function returning content (e.g., charts, grids). |
| **Styling & State** | | | |
| `cssClass` | string | '' | Custom CSS class names to apply to the panel for styling and theming. |
| `enabled` | boolean | true | When false, disables the panel and makes it non-interactive. |
| `zIndex` | number | 1000 | CSS z-index for layer ordering. Higher values appear on top. |

### Events (9 total)

#### Drag Events

| Event | Arguments | Description |
|---|---|---|
| `dragStart` | DragStartArgs | Fires when user begins dragging a panel. Arguments: cancel (bool to prevent drag), element (HTMLElement), event (MouseEvent\|TouchEvent). Use to validate or prevent specific drag operations. |
| `drag` | DraggedEventArgs | Fires continuously while dragging. Arguments: element (HTMLElement being dragged), event (MouseEvent\|TouchEvent), target (HTMLElement under cursor). Use for visual feedback during drag. Fires 60+ times/second—throttle expensive operations. |
| `dragStop` | DragStopArgs | Fires when drag completes/releases. Arguments: cancel (bool to revert position), element, event, panels (PanelModel[] of affected panels), target. Use to save final positions or validate drop location. |

#### Resize Events

| Event | Arguments | Description |
|---|---|---|
| `resizeStart` | ResizeArgs | Fires when resize begins. Arguments: element (HTMLElement), event (MouseEvent\|TouchEvent), isInteracted (true=user, false=programmatic), panels (PanelModel[] affected). |
| `resize` | ResizeArgs | Fires continuously during resize. Same arguments as resizeStart. Use for real-time validation or display of new dimensions. Fires frequently—throttle expensive operations. |
| `resizeStop` | ResizeArgs | Fires when resize completes. Same arguments as resize. Use to finalize panel sizes or save state. |

#### Layout Change Events

| Event | Arguments | Description |
|---|---|---|
| `change` | ChangeEventArgs | Fires when layout changes (panel added, removed, moved, resized). Arguments: addedPanels (PanelModel[]), changedPanels (PanelModel[]), isInteracted (bool), removedPanels (PanelModel[]). Use to detect and react to all layout modifications. |
| `created` | Object | Fires when dashboard component is fully initialized and rendered. Use for post-initialization setup. |
| `destroyed` | Object | Fires when dashboard component is destroyed. Use for cleanup operations. |

### Methods

#### Panel Management

| Method | Signature | Returns | Description |
|---|---|---|---|
| `addPanel` | `addPanel(panel: PanelModel)` | void | Dynamically add a new panel to the dashboard. Panel will be positioned according to its row/col properties. Triggers `change` event. |
| `removePanel` | `removePanel(panelId: string)` | void | Remove a specific panel by its ID. Triggers `change` event. Other panels may float up if allowFloating=true. |
| `removeAll` | `removeAll()` | void | Remove all panels from the dashboard. Clears the entire layout. |
| `movePanel` | `movePanel(panelId: string, row: number, col: number)` | void | Reposition a panel to a new grid location. Triggers drag-like behavior with floating if enabled. Triggers `change` event. |
| `resizePanel` | `resizePanel(panelId: string, sizeX: number, sizeY: number)` | void | Resize a panel to new dimensions (in cells). Respects minSize/maxSize constraints. Triggers resize events with isInteracted=false. Triggers `change` event. |

#### State Management

| Method | Signature | Returns | Description |
|---|---|---|---|
| `serialize` | `serialize()` | PanelModel[] | Captures and returns the current dashboard layout state as an array of PanelModel objects. Use with localStorage or database to persist user configurations. Can be used to create layout templates/presets. |

#### Component Lifecycle

| Method | Signature | Returns | Description |
|---|---|---|---|
| `updatePanel` | `updatePanel(panelId: string, panelModel: PanelModel)` | void | Update properties of an existing panel. Useful for changing header, content, or other panel properties without removing and re-adding the panel. Triggers `change` event with changedPanels. |
| `refreshDraggableHandle` | `refreshDraggableHandle()` | void | Refreshes the draggable handle selector. Call this when DOM structure changes or draggableHandle CSS selector needs to be re-evaluated. Useful after external DOM modifications. |
| `destroy` | `destroy()` | void | Destroys the Dashboard Layout component and cleans up all resources. Triggers `destroyed` event. Call before component unmounting to prevent memory leaks. |

### Event Arguments Reference

#### DragStartArgs
```typescript
{
  cancel: boolean;              // Set to true to prevent the drag operation
  element: HTMLElement;         // The panel element being dragged
  event: MouseEvent | TouchEvent; // The original browser event
}
```

#### DraggedEventArgs
```typescript
{
  element: HTMLElement;         // The panel element being dragged
  event: MouseEvent | TouchEvent; // The original browser event (fires 60+ times/sec)
  target: HTMLElement;          // The element currently under the cursor
}
```

#### DragStopArgs
```typescript
{
  cancel: boolean;              // Set to true to cancel/revert the drag
  element: HTMLElement;         // The panel element that was dragged
  event: MouseEvent | TouchEvent; // The drop/release event
  panels: PanelModel[];         // Array of panels affected by the drag (position changed)
  target: HTMLElement;          // The element at the drop location
}
```

#### ResizeArgs
```typescript
{
  element: HTMLElement;         // The panel element being resized
  event: MouseEvent | TouchEvent; // The original browser event
  isInteracted: boolean;        // true = user resize, false = programmatic resize
  panels: PanelModel[];         // Array of panels affected by the resize
}
```

#### ChangeEventArgs
```typescript
{
  addedPanels: PanelModel[];    // Panels added in this change
  changedPanels: PanelModel[];  // Panels whose position/size changed
  isInteracted: boolean;        // true = user action, false = programmatic
  removedPanels: PanelModel[];  // Panels removed in this change
}
```

**For detailed method examples and security configuration, see:**
- [adding-removing-panels.md](references/adding-removing-panels.md) - Method examples for panel management
- [styling-and-customization.md](references/styling-and-customization.md) - Security and configuration examples

## Common Use Cases

1. **Analytics Dashboard:** Display charts and metrics in resizable panels for data monitoring
2. **Admin Panel:** Dynamic widget system with add/remove and drag-drop functionality
3. **Real-time Monitoring:** Update panel content while maintaining layout state
4. **Mobile-responsive Portal:** Stacked panels on mobile, grid layout on desktop
5. **User Customizable Layout:** Allow users to save their preferred dashboard arrangement
6. **Widget Store:** Add new panels dynamically from a widget library

## Related Topics

### Component Setup & Configuration
- **Angular Module Setup:** Importing DashboardLayoutModule in standalone components
- **CSS Themes:** Available themes (material3, bootstrap5, fabric, tailwind)
- **Responsive Parent Sizing:** Percentage vs static dimensions for fluid layouts
- **Persistence & Storage:** enablePersistence vs manual serialize() approach

### Event Handling & Interaction
- **Drag Events:** dragStart (cancel drag), drag (visual feedback), dragStop (finalize)
- **Resize Events:** resizeStart, resize (continuous), resizeStop with constraint validation
- **Change Detection:** Using (change) event to track ALL layout modifications (add/remove/move/resize)
- **Event Throttling:** Performance optimization for drag (60+/sec) and resize events
- **isInteracted Property:** Distinguishing user actions from programmatic changes

### Advanced Features
- **Dynamic Panel Management:** addPanel(), removePanel(), removeAll() methods
- **Programmatic Movement:** movePanel(id, row, col) for automatic rearrangement
- **Programmatic Resizing:** resizePanel(id, sizeX, sizeY) with constraint enforcement
- **State Serialization:** serialize() method for saving/restoring layouts
- **Size Constraints:** minSizeX, minSizeY, maxSizeX, maxSizeY for panel boundaries
- **Floating Behavior:** allowFloating for automatic gap filling

### Component Integration
- **Embedding Charts:** Syncfusion Charts (Column, Line, Pie, etc.) as panel content
- **Embedding Grids:** Syncfusion Grids with data, sorting, filtering in panels
- **Embedding Gauges:** Linear and Radial Gauges for metrics and KPIs
- **Custom HTML Content:** Using Function type for dynamic content generation
- **Content Function Type:** content/header as (Function) for lazy-loaded or reactive content

### Styling & Customization
- **CSS Classes:** .e-panel-header, .e-panel-content, .e-resize, .e-dashboardlayout
- **Panel Styling:** cssClass property for custom theming per panel
- **Header Customization:** Function/HTMLElement types for dynamic headers
- **Drag Handle Customization:** draggableHandle CSS selector for restricted drag areas
- **RTL Support:** enableRtl + resizableHandles behavior with right-to-left layouts

### Performance & Optimization
- **Large Dashboard Rendering:** Techniques for 100+ panels
- **Virtual Scrolling:** When to consider alternative layouts for massive dashboards
- **Event Throttling:** Managing drag (60+/sec) and resize event frequency
- **Memory Management:** Panel cleanup on destroy event
- **Change Event Filtering:** Tracking only relevant changes (addedPanels, changedPanels, removedPanels)
