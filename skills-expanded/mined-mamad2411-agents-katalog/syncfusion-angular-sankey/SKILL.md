---
name: syncfusion-angular-sankey
description: Create and configure Syncfusion Angular Sankey diagrams for flow visualization. Use this when visualizing weighted flows, processes, and hierarchical relationships. Supports node and link styling, legends, tooltips, events, accessibility features, and comprehensive data binding for complex flow diagrams.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Sankey

The Sankey component visualizes directional flow and relationships between entities using nodes and links. Perfect for displaying process flows, energy distribution, resource allocation, and hierarchical relationships with proportional link widths representing quantities.

## When to Use This Skill

Use the Sankey component when you need to:
- **Visualize Flow Data:** Display directional flow with proportional link widths representing quantities
- **Show Process Steps:** Represent multi-stage processes or workflows
- **Analyze Resource Allocation:** Visualize how resources move through systems
- **Compare Categories:** Show relationships and distributions between categories
- **Display Hierarchies:** Render organizational or hierarchical structures with weighted connections

## Component Overview

The Sankey diagram consists of:
- **Nodes:** Represent sources, sinks, and intermediate entities (customizable width, color, labels)
- **Links:** Represent flow between nodes (width proportional to value, customizable curvature and color)
- **Labels:** Display node and link information with configurable positioning and styling
- **Legend:** Optional legend for categorizing nodes
- **Tooltips:** Contextual information on hover or click

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation of `@syncfusion/ej2-angular-charts` package
- Angular 19+ standalone component setup
- Basic Sankey initialization and first render
- Module injection (Tooltip, Legend services)
- Initial data binding
- **When to use:** Start here for setup and first working example

### Nodes and Links
📄 **Read:** [references/nodes-and-links.md](references/nodes-and-links.md)
- Define node structure (id, label, value)
- Customize node appearance (width, padding, colors, opacity)
- Individual node styling and overrides
- Define link relationships between nodes
- Configure link styling (curvature, opacity, color)
- Node offset and positioning
- **When to use:** Need to configure diagram structure, customize nodes/links, or control positioning

### Appearance and Sizing
📄 **Read:** [references/appearance-and-sizing.md](references/appearance-and-sizing.md)
- Set component dimensions (width, height, responsive sizing)
- Background color and border customization
- Margin control
- Theme application (Material, Bootstrap, Tailwind, etc.)
- Global node and link styles
- **When to use:** Styling the overall diagram, responsive layouts, or theme integration

### Labels, Legends, and Tooltips
📄 **Read:** [references/labels-legends-tooltips.md](references/labels-legends-tooltips.md)
- Label positioning and styling for nodes and links
- Legend configuration and positioning (top, bottom, left, right)
- Legend highlighting behavior
- Tooltip templates and content customization
- Interactive element behaviors
- **When to use:** Adding labels, legends, or tooltips for better context

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- Element-level customization (per-node, per-link styling)
- Predefined color palettes and mapping
- Data-driven conditional styling
- Custom theme creation
- Category-based styling strategies
- Performance optimization for large diagrams
- **When to use:** Advanced styling, color mapping, or dynamic appearance changes

### Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Lifecycle events (load, loaded)
- Interaction events (nodeClick, nodeEnter, nodeLeave, linkClick)
- Rendering events for dynamic styling (nodeRendering, linkRendering)
- Export and print events
- Event handling patterns
- **When to use:** Handle user interactions, trigger custom logic, or respond to diagram lifecycle

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Horizontal and vertical orientation
- Right-to-left (RTL) layout support
- Print and export functionality (PNG, JPEG, SVG, PDF)
- Accessibility features (WCAG compliance, screen readers)
- Performance optimization for many nodes/links
- Edge cases and troubleshooting
- **When to use:** Multi-language support, export requirements, accessibility needs, or performance tuning

## Quick Start Example

```typescript
import { Component, ViewEncapsulation } from '@angular/core';
import { SankeyAllModule } from '@syncfusion/ej2-angular-charts';

@Component({
  imports: [SankeyAllModule],
  standalone: true,
  selector: 'app-sankey-demo',
  template: `<ejs-sankey [dataSource]="data" [nodeSettings]="nodeSettings"></ejs-sankey>`,
  encapsulation: ViewEncapsulation.None
})
export class SankeyDemoComponent {
  data: any[] = [
    { sourceID: 'S1', targetID: 'T1', value: 5 },
    { sourceID: 'S1', targetID: 'T2', value: 3 },
    { sourceID: 'S2', targetID: 'T1', value: 2 }
  ];

  nodeSettings: any = {
    width: 20,
    padding: 10
  };
}
```

## Common Patterns

### Pattern 1: Flow Visualization with Categories
```typescript
// Define nodes with categories for legend grouping
const nodes = [
  { id: 'Power', label: { text: 'Power Plant' }, category: 'Source' },
  { id: 'Grid', label: { text: 'Grid' }, category: 'Intermediary' },
  { id: 'Home', label: { text: 'Households' }, category: 'Sink' }
];

// Links represent flow quantities
const links = [
  { sourceID: 'Power', targetID: 'Grid', value: 100 },
  { sourceID: 'Grid', targetID: 'Home', value: 80 }
];
```

### Pattern 2: Dynamic Styling Based on Values
```typescript
// Render event handler for value-based coloring
onNodeRendering = (args: INodeRenderingEventArgs) => {
  const value = args.node.value || 0;
  args.node.color = value > 100 ? '#00A651' : value > 50 ? '#FFB81C' : '#E81B23';
};
```

### Pattern 3: Interactive Highlighting
```typescript
// Use opacity to emphasize relationships
onNodeEnter = (args: INodeEnterEventArgs) => {
  args.node.highlightOpacity = 1;
};

onNodeLeave = (args: INodeLeaveEventArgs) => {
  args.node.highlightOpacity = 0.3;
};
```

## Key Configuration Properties

| Property | Type | Purpose |
|----------|------|---------|
| `width` | string | Component width ('700px', '100%', or '90%') |
| `height` | string | Component height ('420px', '450px', or '100%') |
| `title` | string | Main title for the diagram |
| `subTitle` | string | Subtitle with descriptive text |
| `orientation` | string | Flow direction ('Horizontal' or 'Vertical') |
| `enableRtl` | boolean | Enable right-to-left layout |
| `theme` | string | Built-in theme (Material, Bootstrap, Tailwind, HighContrast, etc.) |
| `nodeStyle` | Object | Global node styling (width, padding, opacity, colors) |
| `linkStyle` | Object | Global link styling (curvature, opacity, colorType) |
| `labelSettings` | Object | Label positioning and visibility |
| `legendSettings` | Object | Legend configuration and positioning |
| `tooltip` | Object | Tooltip template and visibility settings |
| `nodes` | Array | Node definitions (manual property binding) |
| `links` | Array | Link definitions (manual property binding) |

## Common Use Cases

1. **Energy Distribution:** Show power flow from generation (Solar, Nuclear, Natural Gas) to consumption (Residential, Commercial, Industrial)
2. **Supply Chain:** Visualize product movement through manufacturing → warehouses → distribution centers → retail stores
3. **Financial Flow:** Display money transfers between sources (revenue, investment) → operations → expenses
4. **Process Workflows:** Represent multi-stage processes with branching paths and bottleneck analysis
5. **User Journeys:** Track user movement through application sections (landing → signup → onboarding → features)
6. **Resource Allocation:** Show how budget or resources are distributed across departments or projects
7. **Hierarchical Structures:** Visualize organizational or system hierarchies with weighted relationships

--- 
**Related Documentation:** See [implementing-syncfusion-angular-components](../) for other data visualization components.
