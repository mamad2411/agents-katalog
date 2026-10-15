---
name: syncfusion-javascript-diagram
description: Create and edit visual diagrams with Syncfusion JavaScript Diagram (flowcharts, BPMN, swimlanes, UML, org charts, network topologies). Trigger for diagram rendering, node/connector modeling, layouts, data binding, palettes, interactive tools, exporting, and workflow visualization tasks. 
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# ⚠️ STRICT USAGE RULES — MANDATORY FOR ALL CODE GENERATION

These rules are **non-negotiable** and must be followed for **every** code generation request.

## Rule A — Use Only Provided Reference Files

1. **Always read** `references/getting-started.md` for every request
2. Read **additional** reference files **only if they match the user's query** (see Navigation Guide below)
3. **No external knowledge** allowed:
   - ❌ Do NOT use internet documentation
   - ❌ Do NOT use training-data assumptions about Syncfusion APIs
   - ❌ Do NOT reference older EJ1 APIs or deprecated syntax
   - ✅ If a feature cannot be confirmed from reference files, apply Rule B

## Rule B — No Guessing, No Inference

If a feature, property, API, or behavior is **not explicitly documented** in the reference files:

**You must NOT:**
- Invent class properties, subclasses, or constructor overloads
- Infer JavaScript/TypeScript callback signatures or method names
- Assume module injections exist beyond those documented
- Generalize from other Syncfusion components
- Use deprecated or undocumented shape types

**Instead, respond with:**
```
⚠️ NOT DOCUMENTED: [feature name] is not covered in the reference files.
Skipping this feature to avoid generating incorrect code.
```

## Rule C — Enforce Required Module Injections

Before generating code for these features, **always include** the corresponding injection:

| Feature | Required Injection |
|---|---|
| BPMN diagrams | `Diagram.Inject(BpmnDiagrams)` |
| Export / Print | `Diagram.Inject(PrintAndExport)` |
| Mind Map layout | `Diagram.Inject(MindMap)` |
| Complex Hierarchical layout | `Diagram.Inject(ComplexHierarchicalTree)` |
| Hierarchical or Organizational layout | `Diagram.Inject(HierarchicalTree)` |
| Undo/Redo | `Diagram.Inject(UndoRedo)` |
| Line Distribution | `Diagram.Inject(LineDistribution)` |
| Line Routing | `Diagram.Inject(LineRouting)` |

Do **NOT** assume any other injections exist unless confirmed in reference files.

---

# Diagram Component Overview

The Diagram control is a feature-rich component for creating interactive, editable diagrams in TypeScript/JavaScript applications.

## Core Elements

| Element | Purpose | Common Properties |
|---|---|---|
| **Nodes** | Graphical shapes representing entities | `id`, `offsetX`, `offsetY`, `width`, `height`, `shape`, `style` |
| **Connectors** | Lines/arrows connecting nodes | `id`, `sourceID`, `targetID`, `type`, `style`, `targetDecorator` |
| **Labels** | Text annotations on nodes/connectors | `content`, `font`, `alignment`, `offset` |

## Key Features

✅ Automatic Layout (flowchart, hierarchical, organizational)  
✅ Data Binding (JSON, parent-child relationships)  
✅ Interactive Tools (drawing, selection, pan, zoom, drag-drop)  
✅ Styling (CSS customization, themes, conditional styles)  
✅ Serialization (save/load as JSON)  
✅ Export (PNG, JPG, SVG, PDF)  
✅ User Interactions (events, constraints, undo/redo)  

---

# Navigation Guide

**Always read `references/getting-started.md` first**, then read only files relevant to the request.

| Reference File | Read When the Query Involves |
|---|---|
| 📄 [getting-started.md](references/getting-started.md) | **Every request** — Package installation, imports, first diagram, initialization |
| 📄 [nodes-and-shapes.md](references/nodes-and-shapes.md) | Creating/styling nodes, shapes, positioning, BPMN/UML shapes, annotations |
| 📄 [connectors-and-connections.md](references/connectors-and-connections.md) | Lines (Straight/Orthogonal/Bezier), arrows, routing, sourceID/targetID, segments |
| 📄 [labels-and-annotations.md](references/labels-and-annotations.md) | Text labels, font, alignment, hyperlinks on nodes/connectors |
| 📄 [ports.md](references/ports.md) | Connection points, port positioning, port constraints |
| 📄 [shapes-and-styles.md](references/shapes-and-styles.md) | Flow/Basic/Path/Image/HTML/Native shapes, fill, stroke, gradient, opacity |
| 📄 [data-binding-and-loading.md](references/data-binding-and-loading.md) | DataSourceSettings, JSON loading, parent-child mapping, dynamic updates |
| 📄 [layout-and-automation.md](references/layout-and-automation.md) | Hierarchical, org chart, mind map, radial, symmetric layouts, orientation |
| 📄 [bpmn-diagrams.md](references/bpmn-diagrams.md) | BPMN module injection, events, gateways, activities, data objects |
| 📄 [uml-diagrams.md](references/uml-diagrams.md) | UML class/sequence/activity diagrams, classifiers, relationships |
| 📄 [swimlanes.md](references/swimlanes.md) | Swimlane structure, lanes, phases, header config, interaction |
| 📄 [groups-and-containers.md](references/groups-and-containers.md) | Grouping nodes, Canvas/Stack/Grid containers, nesting, boundaries |
| 📄 [symbol-palette.md](references/symbol-palette.md) | SymbolPaletteComponent, drag-drop, categories, custom symbols, search |
| 📄 [interaction-and-tools.md](references/interaction-and-tools.md) | Drawing tools, selection, constraints, pan/zoom, events, undo/redo |
| 📄 [styling-and-appearance.md](references/styling-and-appearance.md) | CSS theming, colors, fonts, accessibility, responsive design |
| 📄 [serialization-and-export.md](references/serialization-and-export.md) | Save/load diagrams as JSON, export to image/PDF, print, Visio support |
| 📄 [diagram-settings.md](references/diagram-settings.md) | Layers, virtualization, grid, ruler, scroll, page settings, tooltip, localization |
| 📄 [advanced-features.md](references/advanced-features.md) | Undo/redo, custom commands, toolbars, performance optimization |

---

# Quick Start

## 1. Install Package

```bash
npm install @syncfusion/ej2-diagrams
```

## 2. Import Required Modules

```ts
import { Diagram, NodeModel, ConnectorModel } from '@syncfusion/ej2-diagrams';
```

## 3. Create Diagram with Nodes & Connectors

```ts
// Define nodes
let nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 250,
    offsetY: 250,
    width: 100,
    height: 100,
    style: { fill: '#6BA5D7' },
    annotations: [{ content: 'Start' }]
  },
  {
    id: 'node2',
    offsetX: 400,
    offsetY: 250,
    width: 100,
    height: 100,
    style: { fill: '#FFD700' },
    annotations: [{ content: 'Process' }]
  }
];

// Define connector between nodes
let connectors: ConnectorModel[] = [
  {
    id: 'connector1',
    sourceID: 'node1',
    targetID: 'node2',
    style: { strokeColor: '#6BA5D7' },
    targetDecorator: { shape: 'Arrow' }
  }
];

// Create diagram
let diagram: Diagram = new Diagram({
  width: '100%',
  height: '500px',
  nodes: nodes,
  connectors: connectors
});

diagram.appendTo('#diagram-container');
```

**HTML:**
```html
<div id="diagram-container"></div>
```

---

# Common Patterns

## Flowchart Pattern
Creating a simple flowchart with decision points:
- Use rectangle shapes for processes
- Use diamond shapes for decisions
- Connect with arrows
- Apply Flowchart auto-layout

## Organizational Chart Pattern
Creating hierarchical structures:
- Use data binding with parent-child relationships
- Apply HierarchicalTree layout
- Define employee nodes with names/photos
- Show reporting relationships via connectors

## Network Diagram Pattern
Creating system architecture diagrams:
- Use predefined shapes (server, database, client)
- Connect with labeled lines showing data flow
- Organize using grid-based positioning
- Add icons and styling for clarity

## Interactive Diagram Pattern
Building user-editable diagrams:
- Enable drawing tools
- Allow node/connector creation and deletion
- Add context menus for operations
- Implement save/load with serialization
- Handle user events (selection, drag, resize)

---

## When to Use This Skill

✅ Creating any diagram type in TypeScript/JavaScript  
✅ Building flowcharts, process flows, or hierarchies  
✅ Implementing BPMN or UML diagrams  
✅ Configuring node/connector shapes, styles, annotations  
✅ Setting up automatic layouts  
✅ Adding symbol palettes for drag-and-drop  
✅ Binding diagram data from APIs or JSON  
✅ Exporting diagrams or printing  
✅ Enabling drawing tools, undo/redo, layers  

**Do NOT use for:** Simple static charts or graphs (use Chart component), data tables (use Grid component)

---

## Key TypeScript Interfaces

| Interface | Purpose | Key Properties |
|---|---|---|
| `NodeModel` | Node configuration | `id`, `offsetX`, `offsetY`, `width`, `height`, `shape`, `style`, `annotations` |
| `ConnectorModel` | Connector configuration | `id`, `sourceID`, `targetID`, `type`, `style`, `targetDecorator` |
| `ShapeModel` | Shape definition | `type` (Basic/BPMN/UML/Flow), `shape` name |
| `AnnotationModel` | Label on node/connector | `content`, `font`, `alignment`, `offset` |
| `PortModel` | Connection point | `id`, `offset`, `shape`, `visibility`, `constraints` |

---

## Common Shape Types

### Flow Shapes
`Terminator`, `Process`, `Decision`, `Document`, `DirectData`, `MultiDocument`, `PreDefinedProcess`, `Delay`, `Annotation`, `ManualOperation`, `ManualInput`, `Card`, `Or`, `SummingJunction`, `Extract`, `Merge`, `Sort`, `OffPageReference`

**Usage:**
```ts
shape: { type: 'Flow', shape: 'Process' }
```

### Basic Shapes
`Rectangle`, `Ellipse`, `Triangle`, `Pentagon`, `Hexagon`, `Heptagon`, `Octagon`, `Star`, `Cross`, `Diamond`, `CylindricalShape`, `Trapezoid`, `Parallelogram`, `Rhombus`

**Usage:**
```ts
shape: { type: 'Basic', shape: 'Rectangle' }
```