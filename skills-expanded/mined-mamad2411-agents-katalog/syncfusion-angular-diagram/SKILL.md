---
name: syncfusion-angular-diagram
description: "Build and configure Syncfusion EJ2 Angular Diagram for flowcharts, org charts, process diagrams, and data-visualization. Trigger when users ask to create nodes/connectors, apply layouts, swimlane, use BPMN/UML shapes, or add interactivity like drag-drop, zoom/pan, snapping, editing, and symbol palettes."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Diagrams

## When to Use This Skill

Use this skill when you need to:
- **Create visual diagrams** (flowcharts, org-charts, BPMN, UML)
- **Build interactive diagrams** with nodes and connectors
- **Apply layouts** (hierarchical, org-chart, mindmap, radial, flowchart)
- **Design BPMN or UML** diagrams for business processes
- **Add interaction** (drag, resize, selection, undo/redo)
- **Export or serialize** diagrams to JSON/images

## Important: API Verification Required
 
**API Verification Required**: Always verify API class names, properties, and signatures by reading reference files (`references/*.md`) BEFORE generating code examples. Do not assume or infer class names.
⚠️ Before writing ANY code, review the **Common Mistakes** section directly below to avoid known invalid APIs and properties.
 
## Component Overview

The **Syncfusion Angular Diagram component** provides a visual canvas for creating and editing diagrams:

### Core Concepts

1. **Nodes** - Rectangles, circles, flowchart shapes, custom shapes
2. **Connectors** - Lines linking nodes (Straight, Orthogonal, Bezier)
3. **Labels** - Text annotations on nodes and connectors
4. **Ports** - Connection points on node boundaries
5. **Swimlanes** - Horizontal/vertical lanes for process diagrams
6. **Layouts** - Automatic positioning (hierarchical, org-chart, mindmap, etc.)
7. **BPMN Shapes** - Business process diagram standardized shapes
8. **UML Diagrams** - Class and sequence diagram notation
9. **Symbol Palette** - Draggable symbol library
10. **Data Binding** - Render diagrams from JSON data

### Key Features

- **Interactive editing:** Drag, resize, rotate nodes and connectors
- **Auto-layout:** Hierarchical, org-chart, mindmap, radial, flowchart layouts
- **BPMN & UML:** Built-in shape libraries for standard diagrams
- **Serialization:** Save/load diagrams as JSON
- **Export:** PNG, SVG, PDF image export and print
- **Undo/Redo:** Full history support
- **Virtualization:** Render large diagrams efficiently
- **Accessibility:** WCAG 2.1 compliance with keyboard navigation

## Documentation and Navigation Guide

Start with **Getting Started**, then jump to the specific feature you need:

### Core Diagram Building
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and dependencies
- Theme setup (material, bootstrap, fabric)
- CSS/SCSS imports
- Basic DiagramComponent usage
- Module injection pattern
- Standalone component setup

📄 **Read:** [references/nodes.md](references/nodes.md)
- Creating and adding nodes to diagram
- Offsetting and positioning (offsetX, offsetY)
- Node dimensions (width, height)
- Built-in shapes (Flow, Basic, Path)
- Custom styling (fill, stroke, opacity)
- Node templates and appearance
- Expand/collapse node groups
- Node events (click, select, drag)
- getNodeDefaults pattern for style defaults

📄 **Read:** [references/connectors.md](references/connectors.md)
- Three connector types: Straight, Orthogonal, Bezier
- Segments configuration and pathfinding
- sourceID and targetID linking nodes
- Multiple segments in connectors
- Bezier control points and orientation
- Connector customization (stroke, fill, dashing)
- Connector events and interaction
- getConnectorDefaults pattern for style defaults

### Labels, Ports & Styling
📄 **Read:** [references/labels-and-annotations.md](references/labels-and-annotations.md)
- Adding annotations to nodes and connectors
- Label appearance (font, color, bold, italic, alignment)
- Positioning labels on connectors (start, end, center)
- Node labels vs connector labels
- Label interaction (edit mode, drag, resize)
- Label events (edit, focus, blur)
- Formatting with markdown or HTML

📄 **Read:** [references/ports.md](references/ports.md)
- Port types and positioning on nodes
- Appearance customization (shape, fill, size)
- Connecting connectors to specific ports
- Connection visibility and constraints
- Port interaction and visibility
- getPortDefaults pattern

📄 **Read:** [references/shapes-and-styles.md](references/shapes-and-styles.md)
- Built-in shape types: Flow, Basic, Path, Image, HTML, Native SVG
- Flow chart shapes (process, decision, start, end, etc.)
- Style properties (fill, stroke, strokeWidth, dashArray, shadow)
- CSS class and theme customization
- Gradient and pattern fills

### Advanced Diagrams
📄 **Read:** [references/bpmn-diagrams.md](references/bpmn-diagrams.md)
- BPMN module injection and setup
- BPMN shapes overview and standard notation
- Activities (task, subprocess, expanded subprocess, loop)
- Events (start, end, intermediate catch/throw)
- Gateways (exclusive, parallel, inclusive, complex)
- Flows (sequence flow, message flow, association)
- Data objects and data sources
- Groups and text annotations
- BPMN-specific styling and labels

📄 **Read:** [references/uml-diagrams.md](references/uml-diagrams.md)
- UML class diagram shapes
- Classifier shapes (class, interface, enumeration, package, component)
- Class attributes, methods, visibility modifiers
- UML relationships (association, generalization, aggregation, composition)
- UML sequence diagrams
- Lifelines, actors, messages (sync, async, return)
- Interaction frames and combined fragments

### Layout & Structure
📄 **Read:** [references/layouts.md](references/layouts.md)
- Hierarchical tree layout with top-down, bottom-up, left-right, right-left
- Organizational chart layout
- Mindmap layout (sub-trees, branches)
- Radial tree layout
- Flowchart layout with swimlanes
- Complex hierarchical tree with extended nodes
- Automatic layout configuration
- Layout customization (orientation, spacing, margin)
- Layout events and completion

📄 **Read:** [references/swimlanes.md](references/swimlanes.md)
- Swimlane structure overview (header, children, phases)
- Creating lanes and phases within swimlanes
- Swimlane children positioning and constraints
- Swimlane headers and labeling
- Swimlane palette integration
- Swimlane interaction (resize, move, add/remove children)

📄 **Read:** [references/groups-and-containers.md](references/groups-and-containers.md)
- Grouping nodes together
- Group operations (add/remove children, expand/collapse)
- Container nodes with padding and layout
- Child positioning within containers
- Container constraints

### Interaction & Tools
📄 **Read:** [references/symbol-palette.md](references/symbol-palette.md)
- SymbolPaletteComponent setup and integration
- Defining palette symbols and categories
- Drag and drop symbols to diagram
- Palette customization (icons, search, categories, size)
- Symbol palette events
- Creating custom symbol libraries

📄 **Read:** [references/data-binding.md](references/data-binding.md)
- DataManager and dataSourceSettings configuration
- Mapping data to nodes (id, parentId, nodeTemplate)
- Rendering organizational charts from JSON data
- PostgreSQL data source integration
- setNodeTemplate for data-driven node styling
- Dynamic data updates and refresh

📄 **Read:** [references/interaction-and-tools.md](references/interaction-and-tools.md)
- Node selection, drag, and resize interactions
- Tool modes (pointer, draw, pan, pan-select)
- Constraints (node constraints, connector constraints, diagram constraints)
- Commands (keyboard shortcuts, custom commands)
- Undo and Redo functionality
- Context menu (right-click menu)
- User handles (custom connection handles)

### Serialization & Export
📄 **Read:** [references/serialization-and-export.md](references/serialization-and-export.md)
- saveDiagram and loadDiagram (JSON serialization)
- Export to image formats (PNG, SVG, PDF)
- Print diagram functionality
- Visio file import (.vsdx)
- EJ1 API migration serialization
- Custom serialization handling

### Configuration & Settings
📄 **Read:** [references/diagram-settings.md](references/diagram-settings.md)
- Layers (add, lock, visibility, ordering)
- Virtualization (performance optimization for large diagrams)
- Grid lines (snapping, dots/lines, step size)
- Ruler (horizontal and vertical measurement rulers)
- Scroll settings (auto-scroll, pan)
- Page settings (size, orientation, margin, fit to page)
- Tooltip configuration
- Overview panel for navigation
- Localization and language support
- Accessibility (WCAG, ARIA labels, keyboard navigation)

---

## Quick Start Example

Here's a minimal diagram to get started:

```typescript
import { Component, Inject } from '@angular/core';
import { DiagramComponent, DiagramModule } from '@syncfusion/ej2-angular-diagrams';

@Component({
  selector: 'app-diagram',
  template: `
    <ejs-diagram #diagram 
      width="100%" 
      height="600px"
      [nodes]="nodes"
      [connectors]="connectors">
    </ejs-diagram>
  `,
  standalone: true,
  imports: [DiagramModule]
})
export class DiagramComponent {
  nodes = [
    {
      id: 'start',
      width: 80,
      height: 80,
      offsetX: 150,
      offsetY: 150,
      shape: { type: 'Flow', shape: 'Terminator' },
      annotations: [{ content: 'START' }]
    },
    {
      id: 'process',
      width: 100,
      height: 80,
      offsetX: 350,
      offsetY: 150,
      shape: { type: 'Flow', shape: 'Process' },
      annotations: [{ content: 'Process' }]
    },
    {
      id: 'end',
      width: 80,
      height: 80,
      offsetX: 550,
      offsetY: 150,
      shape: { type: 'Flow', shape: 'Terminator' },
      annotations: [{ content: 'END' }]
    }
  ];

  connectors = [
    { id: 'connector1', sourceID: 'start', targetID: 'process' },
    { id: 'connector2', sourceID: 'process', targetID: 'end' }
  ];
}
```

For detailed setup, **read [Getting Started](references/getting-started.md)**.

---

## Module Injection Pattern

Syncfusion Diagram uses **Inject directive** for feature registration:

```typescript
import { Component, Inject } from '@angular/core';
import { BpmnDiagrams, Swimlane, SymbolPalette } from '@syncfusion/ej2-angular-diagrams';
Diagram.Inject(BpmnDiagrams, SymbolPalette)
```

**Always inject the features you use.** This keeps bundle size small and makes dependencies explicit.

---

## Common Patterns

### 1. Get Node/Connector Defaults

```typescript
getNodeDefaults(node: NodeModel): NodeModel {
  return {
    shape: { type: 'Flow', shape: 'Process' },
    style: { fill: '#90EE90', stroke: '#228B22' }
  };
}
```

### 2. Bind Data to Nodes

```typescript
dataSourceSettings: {
  id: 'id',
  parentId: 'parentId',
  dataSource: yourDataArray
}
```

### 3. Handle Selection

```typescript
diagram.selectionChange((args) => {
  console.log('Selected:', args.newItems);
});
```

### 4. Export Diagram

```typescript
diagram.exportDiagram({format: 'PNG', fileName: 'diagram'});
```

### 5. Serialize Diagram

```typescript
const diagramData = diagram.saveDiagram();
localStorage.setItem('diagram', JSON.stringify(diagramData));
```

---

## Common Mistakes

### ❌ Shape Type Errors

**Mistake:**
```typescript
// ❌ WRONG - Shape type should be 'Flow', not 'FlowShape'
shape: { type: 'FlowShape', shape: 'Process' }
```

**Correct:**
```typescript
// ✅ CORRECT - Use 'Flow' for flowchart shapes
shape: { type: 'Flow', shape: 'Process' }

// ✅ CORRECT - Use 'Bpmn' for BPMN shapes
shape: { type: 'Bpmn', shape: 'Task' }

// ✅ CORRECT - Use 'Basic' for basic geometries
shape: { type: 'Basic', shape: 'Rectangle' }
```

**Reference:** [references/shapes-and-styles.md](references/shapes-and-styles.md)

### ❌ Invalid Module in Diagram.Inject()

**Wrong:**
```typescript
// ❌ Swimlane is NOT an injectable module
Diagram.Inject(BpmnDiagrams, Swimlane);
```
**Correct:**
```typescript
// ✅ Only inject verified documented modules
Diagram.Inject(BpmnDiagrams);
```
> 📄 Verify injectable modules in: `references/bpmn-diagrams.md`,
> `references/swimlanes.md`

---

### ❌ `whiteSpace` Does Not Exist in Annotation Style

**Wrong:**
```typescript
// ❌ whiteSpace is NOT a valid TextStyleModel property
annotations: [{
  content: 'Multi\nLine',
  style: { fontSize: 11, whiteSpace: 'pre-wrap' }  // ❌
}]
```
**Correct:**
```typescript
// ✅ Use \n in content — valid style props:
// fontSize, color, bold, italic, fontFamily,
// opacity, strokeColor, strokeWidth, fill
annotations: [{
  content: 'Multi\nLine',
  style: { fontSize: 11, color: '#000', bold: true }
}]
```
> 📄 Verify annotation style properties in:
> `references/labels-and-annotations.md`

---

### ❌ `updateNode()` Does Not Exist on DiagramComponent

**Wrong:**
```typescript
// ❌ updateNode() does not exist in EJ2 Diagram API
this.diagram.updateNode('nodeId', { style: { fill: '#ff0000' } });
```
**Correct:**
```typescript
// ✅ getObject() → mutate property → dataBind()
const node = this.diagram.getObject('nodeId') as NodeModel;
if (node) {
  node.style!.fill = '#ff0000';
  this.diagram.dataBind(); // ← always required after mutation
}
```
> 📄 Verify runtime APIs in: `references/nodes.md`

### ❌ Data Binding Configuration

**Mistake:**
```typescript
// ❌ WRONG - Missing proper data source setup
nodes = this.employeeData; // Direct array assignment
```

**Correct:**
```typescript
// ✅ CORRECT - Use dataSourceSettings with proper mapping
dataSourceSettings: {
  id: 'EmployeeID',
  parentId: 'ReportingManagerID',
  dataSource: this.employeeData
}

// Then configure setNodeTemplate for rendering:
setNodeTemplate(obj: NodeModel): void {
  // obj contains the data row
  obj.width = 100;
  obj.height = 60;
  obj.annotations = [{
    content: obj.data.EmployeeName
  }];
}
```

**Reference:** [references/data-binding.md](references/data-binding.md)

### ❌ Standalone Component Setup

**Mistake:**
```typescript
// ❌ WRONG - Using traditional decorator without standalone
@Component({
  selector: 'app-diagram',
  templateUrl: './component.html',
  imports: [DiagramModule]
  // Missing: standalone: true
})
```

**Correct:**
```typescript
// ✅ CORRECT - Mark as standalone component
@Component({
  selector: 'app-diagram',
  templateUrl: './component.html',
  standalone: true,     // ← Add this
  imports: [CommonModule, DiagramModule], 
})
```

**Reference:** [references/getting-started.md](references/getting-started.md)

### ⚠️ Performance Tips

- **Virtualization:** For diagrams with 1000+ nodes, enable virtualization in [references/diagram-settings.md](references/diagram-settings.md)
- **Layout Performance:** Pre-compute positions for complex hierarchies
- **Connector Updates:** Use `connectorChanges` instead of recreating connectors
- **Export Large Diagrams:** Use incremental approach for PDFs > 50MB

---

## Next Steps

- Choose your diagram type: flowchart, BPMN, UML, org-chart, etc.
- Read the relevant reference files above
- Check [Syncfusion Diagram Docs](https://ej2.syncfusion.com/angular/documentation/diagram/diagram-overview/) for API details
- Explore examples in [their sample repository](https://github.com/syncfusion/ej2-angular-samples)

