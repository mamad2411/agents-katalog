---
name: syncfusion-aspnetcore-sankey
description: Build interactive Sankey Chart visualizations showing weighted flows and relationships between categories using nodes and links. Use this skill whenever the user mentions Sankey diagrams, flow visualization, process flows, value flows between categories, node and link styling, or wants to create diagrams that display the magnitude and direction of flows across stages or systems. The Sankey Chart is perfect for visualizing supply chains, energy flows, revenue streams, customer journeys, and data transformations.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Sankey Chart

The Syncfusion Sankey Chart is a powerful visualization component for displaying weighted flows and relationships between categories. It uses interactive nodes to represent entities and links to show connections with visual thickness proportional to flow values. Perfect for process flows, supply chains, energy distribution, and any scenario requiring flow magnitude visualization.

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API documentation for Sankey Chart component
- Constructor and property definitions
- Event properties and callbacks
- Configuration options and usage patterns
- Related settings classes and data structures

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic Sankey Chart initialization
- CSS imports and theme configuration
- Adding data with nodes and links
- First working example

### Node Customization and Styling
📄 **Read:** [references/nodes-customization.md](references/nodes-customization.md)
- Global node appearance configuration
- Individual node styling overrides
- Node width, padding, and opacity control
- Node positioning with offset property
- Interactive opacity during hovering
- Dynamic node rendering events
- Color application to nodes

### Link Styling and Configuration
📄 **Read:** [references/links-styling.md](references/links-styling.md)
- Link appearance and opacity properties
- Curvature control for link paths
- Link color types (Source, Target, Blend)
- Link value and thickness mapping
- Dynamic link customization with rendering events
- Opacity control during interactions
- Creating meaningful visual representations of flow magnitudes

### Labels and Legend Configuration
📄 **Read:** [references/labels-legend.md](references/labels-legend.md)
- Label visibility and font styling
- Global label settings (size, color, weight)
- Individual node label customization
- Dynamic label rendering and modifications
- Legend positioning and display options
- Legend customization (background, opacity, shapes)
- Interactive legend highlighting
- Dynamic legend item rendering

### Appearance and Theming
📄 **Read:** [references/appearance-theming.md](references/appearance-theming.md)
- Width and height configuration
- Responsive sizing with percentages
- Background and border customization
- Margin configuration
- Built-in theme selection
- Color schemes and visual styling
- Making charts responsive across devices

### Events and Interactions
📄 **Read:** [references/events-interactions.md](references/events-interactions.md)
- Lifecycle events (Load, Loaded)
- Node and link interaction events (click, enter, leave)
- Rendering events for customization
- Label and legend rendering events
- Size change event handling
- Export and print events
- Complete event handling patterns

### Orientation and RTL Support
📄 **Read:** [references/orientation-rtl.md](references/orientation-rtl.md)
- Horizontal and vertical orientation options
- Right-to-Left (RTL) layout support
- RTL with different orientations
- Layout mirroring for international applications
- Best practices for localization

### Print and Export
📄 **Read:** [references/print-export.md](references/print-export.md)
- Printing Sankey Charts to PDF or paper
- Exporting to PNG, JPEG, SVG, and PDF formats
- Custom filename and format selection
- Before and after export event handling
- Format selection based on use case
- File size and quality considerations

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- Screen reader support and ARIA attributes
- Keyboard navigation shortcuts
- Color contrast and mobile accessibility
- WAI-ARIA roles and attributes
- Ensuring inclusive visualizations

## Quick Start

```csharp
// ASP.NET Core - Basic Sankey Chart
@{
    var nodeData = new []
    {
        new { id = 0, label = "Source" },
        new { id = 1, label = "Process" },
        new { id = 2, label = "Target" }
    };

    var linkData = new []
    {
        new { sourceNodeID = 0, targetNodeID = 1, value = 100 },
        new { sourceNodeID = 1, targetNodeID = 2, value = 80 }
    };
}

<ejs-sankey id="container" width="100%" height="420px">
    <e-sankey-margin top="50" bottom="50"></e-sankey-margin>
    <e-sankey-nodes>
        @foreach (var node in nodeData)
        {
            <e-sankey-node id="@node.id"></e-sankey-node>
        }
    </e-sankey-nodes>
    <e-sankey-links>
        @foreach (var link in linkData)
        {
            <e-sankey-link sourceId="@link.sourceNodeID" targetId="@link.targetNodeID" value="@link.value"></e-sankey-link>
        }
    </e-sankey-links>
    <e-sankey-nodesettings padding=10
                           width="20">
    </e-sankey-nodesettings>
</ejs-sankey>
```

## Common Patterns

### Pattern 1: Colored Nodes with Flow Visualization
Create a Sankey Chart where each node has a distinct color and links show gradient blending:

```csharp
<ejs-sankey id="coloredSankey" width="100%" height="420px">
    <e-sankey-links>
        @foreach (var link in linkData)
        {
            <e-sankey-link sourceId="@link.sourceNodeID" targetId="@link.targetNodeID" value="@link.value"></e-sankey-link>
        }
    </e-sankey-links>
    <e-sankey-nodes>
        @foreach (var node in nodeData)
        {
            <e-sankey-node id="@node.id"></e-sankey-node>
        }
    </e-sankey-nodes>
    <e-sankey-nodesettings fill="#3DB6E6"></e-sankey-nodesettings>
    <e-sankey-linksettings opacity="0.4" colorType="Blend"></e-sankey-linksettings>
</ejs-sankey>
```

### Pattern 2: Interactive Responsive Layout
Build a responsive Sankey that adapts to container width:

```csharp
<ejs-sankey id="responsiveSankey" width="100%" height="100%">
    <e-sankey-nodes>
        @foreach (var node in nodeData)
        {
            <e-sankey-node id="@node.id"></e-sankey-node>
        }
    </e-sankey-nodes>
    <e-sankey-links>
        @foreach (var link in linkData)
        {
            <e-sankey-link sourceId="@link.sourceNodeID" targetId="@link.targetNodeID" value="@link.value"></e-sankey-link>
        }
    </e-sankey-links>
    <e-sankey-nodesettings width="20" padding="10"></e-sankey-nodesettings>
</ejs-sankey>

```

### Pattern 3: Vertical Process Flow
Display processes flowing from top to bottom:

```csharp
<ejs-sankey id="verticalFlow"
                 orientation="Vertical"
                 width="100%" height="600px">
    <e-sankey-nodes>
        @foreach (var node in nodeData)
        {
            <e-sankey-node id="@node.id"></e-sankey-node>
        }
    </e-sankey-nodes>
    <e-sankey-links>
        @foreach (var link in linkData)
        {
            <e-sankey-link sourceId="@link.sourceNodeID" targetId="@link.targetNodeID" value="@link.value"></e-sankey-link>
        }
    </e-sankey-links>
</ejs-sankey>
```

## Key Properties

- **Nodes**: Represent entities (sources, targets, intermediates) with customizable appearance
- **Links**: Connect nodes with value-based thickness representing flow magnitude
- **NodeStyle**: Global styling for all nodes (fill, stroke, width, padding, opacity)
- **LinkStyle**: Global styling for all links (opacity, curvature, colorType)
- **LabelSettings**: Configure label appearance, font, visibility, and positioning
- **LegendSettings**: Control legend display, position, and interactive behavior
- **Orientation**: Switch between Horizontal and Vertical flow directions
- **EnableRtl**: Enable right-to-left layout for international applications

## When to Use Sankey Charts

✅ **Best For:**
- Supply chain and logistics flows
- Energy distribution systems
- Revenue and profit streams
- Customer journey mapping
- Data pipeline visualization
- Process transformations
- Budget allocation flows
- Website traffic analysis

❌ **Not Ideal For:**
- Simple comparison of independent values
- Time-series trend analysis
- Hierarchical tree structures
- Network graphs without flow directionality
