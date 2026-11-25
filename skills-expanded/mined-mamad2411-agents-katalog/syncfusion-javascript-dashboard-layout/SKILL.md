---
name: syncfusion-javascript-dashboard-layout
description: Build responsive dashboard layouts with drag-and-drop panels, dynamic resizing, and state persistence. Guide users to implement DashboardLayout control with panel management, dragging, resizing, floating, and persistence features. Includes event handling, dynamic panel addition/removal, and comprehensive API reference.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Controls"
---

# Implementing Syncfusion TypeScript Dashboard Layout

The **DashboardLayout** is a powerful grid-based layout component that enables creating interactive dashboard interfaces with draggable, resizable panels. It supports dynamic panel management, floating layouts, state persistence, and responsive behavior through media queries. Users can rearrange panels, resize them in multiple directions, and save/restore layout configurations.

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies
- Setting up with HTML attributes or script
- Basic panel configuration (rows, columns, cell spacing)
- Running your first dashboard application

### Panel Configuration
📄 **Read:** [references/panel-configuration.md](references/panel-configuration.md)
- Defining panel properties (sizeX, sizeY, row, col)
- Panel headers and content templates
- CSS classes and styling
- Programmatic panel sizing and positioning

### Dragging and Moving Panels
📄 **Read:** [references/dragging-and-moving.md](references/dragging-and-moving.md)
- Enabling/disabling drag functionality
- Customizing drag handles (draggableHandle)
- Panel collision detection and reordering
- Drag events (dragStart, drag, dragStop)

### Moving Panels Programmatically
📄 **Read:** [references/moving-panels.md](references/moving-panels.md)
- Using movePanel() method for programmatic positioning
- Swapping panels and layout reorganization
- Priority-based and column-based arrangements
- Restoring saved layout configurations

### Resizing Panels
📄 **Read:** [references/resizing-panels.md](references/resizing-panels.md)
- Enabling/disabling resize functionality
- Configurable resize handles (e-south-east, e-east, e-west, e-north, e-south)
- Resize events and event arguments
- Programmatic resizing with resizePanel() method

### Panel Manipulation
📄 **Read:** [references/panel-manipulation.md](references/panel-manipulation.md)
- Dynamically adding panels with addPanel()
- Removing panels with removePanel()
- Removing all panels with removeAll()
- Serializing panel layout with serialize()

### Floating and Responsive Layouts
📄 **Read:** [references/floating-and-responsive.md](references/floating-and-responsive.md)
- Enabling floating to fill empty spaces automatically
- Media query for responsive stacking behavior
- Cell aspect ratio configuration
- Adaptive layouts for different screen sizes

### Persistence and State Management
📄 **Read:** [references/persistence-and-state.md](references/persistence-and-state.md)
- Saving layout configuration with serialize()
- Restoring layouts from saved state
- State persistence with enablePersistence
- localStorage integration for browser sessions

### Events Handling
📄 **Read:** [references/events-handling.md](references/events-handling.md)
- Lifecycle events (created, destroyed)
- Drag events with DragStartArgs, DraggedEventArgs, DragStopArgs
- Resize events with ResizeArgs
- Change event for panel position updates

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All DashboardLayout properties and their usage
- All Panel properties and configuration options
- Complete event signatures with arguments
- All methods with parameters and examples
- Type definitions and enumerations

## Quick Start

```typescript
import { DashboardLayout } from '@syncfusion/ej2-layouts';

// Initialize Dashboard Layout with 5 columns
let dashboard: DashboardLayout = new DashboardLayout({
    cellSpacing: [10, 10],
    columns: 5,
    panels: [
        { 
            'id': 'Panel1',
            'sizeX': 2, 
            'sizeY': 2, 
            'row': 0, 
            'col': 0, 
            content: '<div class="content">Panel 1</div>' 
        },
        { 
            'id': 'Panel2',
            'sizeX': 3, 
            'sizeY': 2, 
            'row': 0, 
            'col': 2, 
            content: '<div class="content">Panel 2</div>' 
        }
    ]
});

// Render to container
dashboard.appendTo('#dashboard_layout');
```

## Common Patterns

### Pattern 1: Enable Full Interactivity

```typescript
const dashboard = new DashboardLayout({
    allowDragging: true,      // Enable drag and reorder
    allowResizing: true,       // Enable resize
    allowFloating: true,       // Auto-fill empty spaces
    cellSpacing: [10, 10],
    columns: 6,
    panels: [
        { 'sizeX': 2, 'sizeY': 2, 'row': 0, 'col': 0, content: '<div>Widget 1</div>' },
        { 'sizeX': 2, 'sizeY': 2, 'row': 0, 'col': 2, content: '<div>Widget 2</div>' }
    ]
});
dashboard.appendTo('#dashboard');
```

### Pattern 2: Handle Drag Events

```typescript
const dashboard = new DashboardLayout({
    columns: 5,
    dragStart: (args) => console.log('Drag started on panel:', args.element),
    drag: (args) => console.log('Dragging panel...'),
    dragStop: (args) => {
        console.log('Drag completed. Modified panels:', args.panels);
    },
    panels: [...] // panel configuration
});
dashboard.appendTo('#dashboard');
```

### Pattern 3: Save and Restore Layout

```typescript
const dashboard = new DashboardLayout({
    columns: 5,
    panels: [...]
});
dashboard.appendTo('#dashboard');

// Save current layout
const savedLayout = dashboard.serialize();

// Later: Restore layout
dashboard.panels = savedLayout;
```

### Pattern 4: Responsive Dashboard

```typescript
const dashboard = new DashboardLayout({
    columns: 6,
    mediaQuery: '(max-width: 600px)',  // Stack panels below 600px
    enablePersistence: true,            // Remember user layout
    panels: [...]
});
dashboard.appendTo('#dashboard');
```

## Key Concepts

### Grid System
- Panels are positioned on a grid using `row`, `col`, `sizeX`, and `sizeY`
- `columns` defines the total grid columns available
- `cellSpacing` controls horizontal and vertical spacing between panels

### Panel Sizing
- `sizeX`: Width in grid cells (e.g., sizeX: 2 means 2 columns wide)
- `sizeY`: Height in grid cells
- `minSizeX/maxSizeX` and `minSizeY/maxSizeY`: Constrain resize operations

### Interaction
- **Dragging**: Reorder panels when allowDragging = true
- **Resizing**: Change panel size with handles (e-south-east, e-east, etc.)
- **Floating**: Panels move up to fill empty cells when allowFloating = true

### Events
- **dragStart/drag/dragStop**: Monitor and control drag operations
- **resizeStart/resize/resizeStop**: Monitor and control resize operations
- **change**: Fired when panel positions update
- **created/destroyed**: Lifecycle events

## When to Use DashboardLayout

✅ **Perfect for:**
- Analytics and reporting dashboards
- Customizable widget layouts
- Data monitoring interfaces
- User-configurable UI layouts
- Real-time data visualization hubs

❌ **Not ideal for:**
- Static, fixed layouts
- Simple page layouts (use CSS Grid or Flexbox)
- Single-column layouts

---

**Next Steps:**
1. Choose your use case from the navigation guide
2. Read the relevant reference file
3. Check the API reference for complete property/method documentation
4. Review code examples for your specific scenario

For complete API documentation, see [references/api-reference.md](references/api-reference.md).
