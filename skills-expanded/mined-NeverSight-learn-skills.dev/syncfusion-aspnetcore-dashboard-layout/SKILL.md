---
name: syncfusion-aspnetcore-dashboard-layout
description: Implement responsive, resizable, and draggable panel layouts with the Syncfusion ASP.NET Core Dashboard Layout component.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Dashboard Layout

The Syncfusion Dashboard Layout control is a powerful grid-based layout system that allows developers to create interactive dashboards with flexible panel management capabilities. Panels can be arranged in a customizable grid, resized, dragged, reordered, and dynamically added or removed to meet dynamic dashboard requirements.

## When to Use This Skill

Use the Dashboard Layout control when you need to:

- **Create grid-based dashboards** with a flexible panel structure
- **Enable drag-and-drop functionality** to allow users to reorder panels
- **Implement responsive layouts** that adapt to different screen sizes
- **Add resizable panels** with min/max size constraints
- **Enable floating panels** to automatically fill empty grid cells
- **Manage panel state** and maintain layout persistence across sessions
- **Handle dynamic panel operations** (add, remove, move, update panels)
- **Customize panel headers and content** with HTML or templates
- **Support RTL layouts** for right-to-left language support

## Component Overview

The Dashboard Layout consists of:

1. **Main Container** - The grid-based layout that holds panels
2. **Panels** - Individual grid cells that contain content
3. **Grid System** - Configurable columns and cell spacing
4. **Interaction Features** - Dragging, resizing, and dynamic operations
5. **State Management** - Persistence and serialization capabilities

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- ASP.NET Core project configuration
- TagHelper registration and setup
- Resource references (styles and scripts)
- Basic Dashboard Layout initialization
- Two initialization methods (content template vs tag helper)

### Core Configuration
📄 **Read:** [references/configuring-layouts.md](references/configuring-layouts.md)
- Grid system setup with columns property
- Cell spacing and aspect ratio configuration
- Panel positioning using row and column properties
- Layout structure and grid cell management
- Complete working examples with code

### Panel Management
📄 **Read:** [references/panel-operations.md](references/panel-operations.md)
- Adding panels dynamically with addPanel method
- Removing panels and clearing layout (removePanel, removeAll)
- Moving panels to different positions (movePanel)
- Updating existing panels (updatePanel)
- Resizing panels with sizeX, sizeY properties
- Applying min/max size constraints to panels

### Interaction Features
📄 **Read:** [references/dragging-and-dropping.md](references/dragging-and-dropping.md)
- Enabling drag-and-drop with allowDragging property
- Understanding drag event lifecycle (dragStart, drag, dragStop)
- Customizing drag handlers with draggableHandle selector
- Panel collision detection and adaptive repositioning
- Handling drag events with proper event binding

### Panel Resizing
📄 **Read:** [references/resizing-panels.md](references/resizing-panels.md)
- Enabling resize functionality with allowResizing property
- Configuring resizable handles with resizableHandles property
- Understanding resize event lifecycle (resizeStart, resize, resizeStop)
- Setting minimum and maximum panel size constraints
- Handling resize events in your application

### Responsive Behavior
📄 **Read:** [references/responsive-layouts.md](references/responsive-layouts.md)
- Implementing floating panels with allowFloating property
- Configuring responsive breakpoints with mediaQuery
- Automatic panel stacking for mobile devices
- RTL support with enableRtl property
- Adapting layouts to different screen resolutions

### State & Persistence
📄 **Read:** [references/state-and-persistence.md](references/state-and-persistence.md)
- Enabling state persistence with enablePersistence property
- Serializing dashboard configuration (serialize method)
- Component lifecycle events (created, destroyed)
- Managing state across page reloads
- HTML sanitization for security

### Complete API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- All Dashboard Layout properties with descriptions and defaults
- Complete method signatures and usage examples
- Event definitions and event argument types
- Panel model properties and constraints
- Cross-references to detailed feature documentation

## Quick Start Example

Here's a minimal example of creating a Dashboard Layout with two panels using proper camelCase API properties:

```html
@{
    var cellSpacing = new double[] { 10, 10 };
}

<ejs-dashboardlayout id="dashboard" allowDragging="true" allowResizing="true" 
                      allowFloating="true" columns="6" cellSpacing="@cellSpacing">
    <e-dashboardlayout-panels>
        <e-dashboardlayout-panel id="panel1" sizeX="3" sizeY="2" row="0" col="0" 
                                 header="<div>Sales Report</div>" 
                                 content="<div class='content'>Sales data content goes here</div>">
        </e-dashboardlayout-panel>
        <e-dashboardlayout-panel id="panel2" sizeX="3" sizeY="2" row="0" col="3" 
                                 header="<div>Revenue Chart</div>" 
                                 content="<div class='content'>Revenue chart content goes here</div>">
        </e-dashboardlayout-panel>
    </e-dashboardlayout-panels>
</ejs-dashboardlayout>
```

## Common Patterns

### Pattern 1: Enable All Interactions
Enable dragging, resizing, and floating for maximum interactivity:

```html
<ejs-dashboardlayout id="dashboard" allowDragging="true" allowResizing="true" 
                      allowFloating="true" columns="4">
    <e-dashboardlayout-panels>
        <e-dashboardlayout-panel id="panel1" sizeX="2" sizeY="1" row="0" col="0" 
                                 header="<div>Panel 1</div>" 
                                 content="<div class='content'>Content</div>">
        </e-dashboardlayout-panel>
    </e-dashboardlayout-panels>
</ejs-dashboardlayout>
```

### Pattern 2: Responsive Breakpoint
Configure layout to stack panels on mobile devices:

```html
<ejs-dashboardlayout id="responsive-dashboard" mediaQuery="(max-width: 768px)" 
                      columns="6" allowFloating="true">
    <e-dashboardlayout-panels>
        <e-dashboardlayout-panel id="panel1" sizeX="3" sizeY="2" row="0" col="0" 
                                 content="<div>Panel 1</div>">
        </e-dashboardlayout-panel>
        <e-dashboardlayout-panel id="panel2" sizeX="3" sizeY="2" row="0" col="3" 
                                 content="<div>Panel 2</div>">
        </e-dashboardlayout-panel>
    </e-dashboardlayout-panels>
</ejs-dashboardlayout>
```

### Pattern 3: Dynamic Panel Operations
Add panels programmatically based on user actions - covered in Panel Management reference.

### Pattern 4: Persist User Layout
Save and restore dashboard configuration across sessions - covered in State & Persistence reference.

## Key Properties Overview

| Property | Type | Purpose | Default |
|----------|------|---------|---------|
| `columns` | number | Number of grid columns | 1 |
| `cellSpacing` | number[] | Spacing between panels [horizontal, vertical] | [5, 5] |
| `allowDragging` | boolean | Enable drag-and-drop | true |
| `allowResizing` | boolean | Enable panel resizing | false |
| `allowFloating` | boolean | Auto-fill empty cells | true |
| `draggableHandle` | string | CSS selector for drag handle | null |
| `resizableHandles` | string[] | Resize handle directions | ['e-south-east'] |
| `mediaQuery` | string | Responsive breakpoint | 'max-width:600px' |
| `enablePersistence` | boolean | Save state to storage | false |
| `enableRtl` | boolean | Right-to-left layout | false |
| `showGridLines` | boolean | Visualize grid structure | false |

## Common Use Cases

1. **Analytics Dashboard** - Arrange chart panels with resize and drag capabilities
2. **Sales Dashboard** - Monitor KPIs with resizable metric panels
3. **Project Management** - Organize task boards with dynamic panel operations
4. **Business Intelligence** - Display reports with state persistence
5. **Admin Portal** - Customizable dashboard with user-defined layout

---

**Next Steps:** Start with the Getting Started reference to set up your Dashboard Layout project, then explore the specific features you need.
