---
name: syncfusion-winforms-diagram
description: "Implement Syncfusion Windows Forms Diagram control for creating interactive diagramming applications. Use this when creating flowcharts, organizational charts, network diagrams, or node-based visualizations. The control provides drag-and-drop editing, symbol palettes, connector management, and diagram serialization for building Visio-like applications in Windows Forms."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms Diagram

Essential Diagram is an extensible and high-performance .NET diagramming framework for Windows Forms applications. It enables you to develop Microsoft Visio-like interactive graphics and diagramming applications with support for both vector and raster graphics.

## When to Use This Skill

Use this skill when you need to:

- **Create interactive diagrams** - Build flowcharts, organizational charts, network diagrams, or any node-based visualizations
- **Implement diagram editors** - Develop Visio-like applications with drag-and-drop, symbol palettes, and drawing tools
- **Connect shapes visually** - Link nodes with various connector types (orthogonal, bezier, directed lines)
- **Design custom diagramming tools** - Create domain-specific diagram applications with custom shapes and symbols
- **Build visual modeling software** - Implement UML diagrams, ER diagrams, mind maps, or workflow designers
- **Add diagramming capabilities** - Integrate diagram controls into existing Windows Forms applications
- **Manage complex layouts** - Use automatic layout algorithms for hierarchical, radial, or organizational layouts

## Component Overview

Essential Diagram provides a comprehensive Model-View-Controller architecture with the following components:

**Core Controls:**
- **Diagram** - Main canvas for rendering and manipulating 2D shapes, text, images, and controls
- **Overview** - Perspective view with dynamic pan/zoom viewport
- **PaletteGroupBar/PaletteGroupView** - Symbol palette management for drag-and-drop
- **PropertyEditor** - Property inspection and editing for diagram objects
- **DocumentExplorer** - Tree view of diagram objects and layers

**Key Features:**
- 15+ interactive drawing tools (Rectangle, Line, Bezier, Polygon, Text, etc.)
- 7+ connector types with automatic routing and line bridging
- Matrix transformations (translate, rotate, scale)
- Layers, grouping, and Z-order management
- Undo/redo, rulers, gridlines, snap-to-grid
- Event handling, data binding, context menus
- Serialization, printing, and export capabilities
- Symbol Designer and Diagram Builder utilities

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

When you need to:
- Install and configure the Diagram control
- Understand the Model-View-Controller architecture
- Create your first diagram (designer or code)
- Add basic nodes and connect them
- Set up a complete working diagram

### Nodes and Shapes

📄 **Read:** [references/nodes-and-shapes.md](references/nodes-and-shapes.md)

When working with:
- Creating rectangles, ellipses, polygons, and other shapes
- Positioning and styling nodes (fill, border, shadow)
- Custom shapes and Symbol Designer
- Node properties and manipulation
- Bitmap nodes and composite shapes

### Connectors and Links

📄 **Read:** [references/connectors.md](references/connectors.md)

When implementing:
- Line, Orthogonal, DirectedLine, PolyLine connectors
- Bezier, Spline, Curve, and Arc connectors
- Head and tail decorators (arrows, diamonds, circles)
- Automatic line routing and line bridging
- Connection points and port management
- Connector styling and customization

### Drawing Tools

📄 **Read:** [references/drawing-tools.md](references/drawing-tools.md)

When enabling:
- Interactive drawing tools (SelectTool, RectangleTool, LineTool, etc.)
- Shape tools (Ellipse, Polygon, RoundRect, Arc)
- Line drawing tools (PolyLine, Curve, Bezier, Spline, Pencil)
- Text and RichText tools
- Connection tools (LineLinkTool, OrthogonalLinkTool, etc.)
- Tool activation and configuration

### Diagram Controls

📄 **Read:** [references/diagram-controls.md](references/diagram-controls.md)

When adding:
- Overview control for pan/zoom viewport
- PaletteGroupBar for symbol palette management
- PaletteGroupView for palette display
- PropertyEditor for property inspection
- DocumentExplorer for object tree visualization
- Creating controls through designer and code

### Layout and Organization

📄 **Read:** [references/layout-organization.md](references/layout-organization.md)

When organizing:
- Layers (creating, managing, visibility)
- Grouping and ungrouping nodes
- Alignment tools (left, center, right, top, middle, bottom)
- Z-order operations (bring forward, send backward)
- Spacing and sizing tools
- Nudge operations

### Labels and Ports

📄 **Read:** [references/labels-ports.md](references/labels-ports.md)

When configuring:
- Adding and formatting labels on nodes
- Text styling (font, color, alignment, rotation)
- Connection ports on nodes
- Port constraints and connection rules
- Custom port positioning
- Label and port visibility

### Diagram Features

📄 **Read:** [references/features.md](references/features.md)

When implementing:
- Dynamic properties at runtime
- Event handlers (node, connection, model events)
- Data binding to diagram objects
- Context menu customization
- Touch support for touch-enabled devices
- Measurement units (pixels, inches, millimeters)

### User Interaction

📄 **Read:** [references/user-interaction.md](references/user-interaction.md)

When handling:
- Undo/redo functionality
- Pan and zoom tools
- Magnification control
- Selection modes and multi-select
- Copy, cut, paste operations
- Rotation and flip tools

### View Controls

📄 **Read:** [references/view-controls.md](references/view-controls.md)

When configuring:
- Rulers (horizontal and vertical)
- Gridlines and snap-to-grid
- Guides for alignment
- Scrolling behavior
- Zoom and pan settings
- Page borders and backgrounds

### Layout Management

📄 **Read:** [references/layout-management.md](references/layout-management.md)

When applying:
- Automatic layout algorithms
- Hierarchical layouts
- Organizational chart layouts
- Radial and tree layouts
- Custom layout managers
- Layout configuration and optimization

### Advanced Features

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

When working with:
- Diagram serialization (save/load)
- Printing (page setup, print preview, headers/footers)
- Export to image formats
- Symbol Designer utility for custom symbols
- Diagram Builder utility for creating diagrams
- Custom tool development
- Performance optimization

### Troubleshooting

📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)

When encountering:
- Common issues and solutions
- Assembly dependencies and versioning
- Performance optimization tips
- Best practices and FAQ

## Quick Start Example

### Basic Diagram with Connected Nodes

```csharp
using Syncfusion.Windows.Forms.Diagram;
using Syncfusion.Windows.Forms.Diagram.Controls;

// Create diagram control
Diagram diagram = new Diagram();
diagram.Size = new Size(800, 600);
diagram.HScroll = true;
diagram.VScroll = true;
diagram.ShowRulers = true;

// Create and attach model
Model model = new Model();
diagram.Model = model;

// Create a start node (ellipse)
Ellipse startNode = new Ellipse(100, 100, 120, 80);
startNode.FillStyle.Color = Color.LightGreen;
startNode.FillStyle.ForeColor = Color.Green;
startNode.LineStyle.LineColor = Color.DarkGreen;
startNode.LineStyle.LineWidth = 2;

Label startLabel = new Label();
startLabel.Text = "Start";
startLabel.FontColorStyle.Color = Color.Black;
startNode.Labels.Add(startLabel);

model.AppendChild(startNode);

// Create a process node (rectangle)
Syncfusion.Windows.Forms.Diagram.Rectangle processNode = 
    new Syncfusion.Windows.Forms.Diagram.Rectangle(300, 100, 120, 80);
processNode.FillStyle.Color = Color.LightBlue;
processNode.LineStyle.LineColor = Color.DarkBlue;
processNode.LineStyle.LineWidth = 2;

Label processLabel = new Label();
processLabel.Text = "Process";
processLabel.FontColorStyle.Color = Color.Black;
processNode.Labels.Add(processLabel);

model.AppendChild(processNode);

// Connect nodes with an orthogonal connector
OrthogonalConnector connector = 
    new OrthogonalConnector(startNode.PinPoint, processNode.PinPoint);
connector.LineStyle.LineColor = Color.Gray;
connector.LineStyle.LineWidth = 2;
connector.HeadDecorator.DecoratorShape = DecoratorShape.Filled45Arrow;

startNode.CentralPort.TryConnect(connector.TailEndPoint);
processNode.CentralPort.TryConnect(connector.HeadEndPoint);

model.AppendChild(connector);

// Add diagram to form
this.Controls.Add(diagram);
```

## Common Patterns

### Creating a Complete Diagram Editor

```csharp
// Setup diagram with all helper controls
Diagram diagram = new Diagram();
diagram.Dock = DockStyle.Fill;
Model model = new Model();
diagram.Model = model;

// Add Overview control
OverviewControl overview = new OverviewControl();
overview.Dock = DockStyle.Left;
overview.Diagram = diagram;

// Add PaletteGroupBar for symbols
PaletteGroupBar paletteBar = new PaletteGroupBar();
paletteBar.Dock = DockStyle.Left;
paletteBar.LoadPalette("BasicShapes.edp");
paletteBar.LoadPalette("FlowchartSymbols.edp");

// Add PropertyEditor
PropertyEditor propertyEditor = new PropertyEditor();
propertyEditor.Dock = DockStyle.Right;
propertyEditor.Diagram = diagram;

// Add DocumentExplorer
DocumentExplorer docExplorer = new DocumentExplorer();
docExplorer.Dock = DockStyle.Right;
docExplorer.AttachModel(model);

// Add all to form
this.Controls.Add(diagram);
this.Controls.Add(overview);
this.Controls.Add(paletteBar);
this.Controls.Add(propertyEditor);
this.Controls.Add(docExplorer);
```

### Activating Drawing Tools

```csharp
// Activate rectangle tool for drawing rectangles
diagram.Controller.ActivateTool("RectangleTool");

// Activate line connector tool
diagram.Controller.ActivateTool("LineLinkTool");

// Activate selection tool (default)
diagram.Controller.ActivateTool("SelectTool");

// Configure tool settings
Tool tool = diagram.Controller.ActiveTool;
if (tool is LineConnectorTool lineConnector)
{
    lineConnector.HeadDecorator.DecoratorShape = DecoratorShape.Filled45Arrow;
    lineConnector.TailDecorator.DecoratorShape = DecoratorShape.Circle;
}
```

### Working with Layers

```csharp
// Create a new layer
Layer backgroundLayer = new Layer();
backgroundLayer.Name = "Background";
backgroundLayer.Visible = true;
backgroundLayer.Enabled = true;
model.Layers.Add(backgroundLayer);

// Add nodes to specific layer
Rectangle node = new Rectangle(50, 50, 100, 60);
backgroundLayer.AppendChild(node);

// Set active layer
model.ActiveLayer = backgroundLayer;

// Toggle layer visibility
backgroundLayer.Visible = false;
diagram.Refresh();
```

### Applying Automatic Layout

```csharp
// Create nodes
List<Node> nodes = new List<Node>();
for (int i = 0; i < 10; i++)
{
    Rectangle node = new Rectangle(0, 0, 80, 50);
    node.Name = "Node" + i;
    model.AppendChild(node);
    nodes.Add(node);
}

// Apply hierarchical layout
HierarchicalLayout layout = new HierarchicalLayout(model, model.Bounds);
layout.HorizontalSpacing = 50;
layout.VerticalSpacing = 50;
layout.Orientation = LayoutOrientation.TopToBottom;
layout.Layout();

diagram.UpdateView();
```

### Saving and Loading Diagrams

```csharp
// Save diagram to file
diagram.SaveBinary("MyDiagram.edd");

// Load diagram from file
diagram.LoadBinary("MyDiagram.edd");
diagram.Refresh();

// Save model only
model.Save("MyModel.xml");

// Load model
Model loadedModel = Model.Load("MyModel.xml");
diagram.Model = loadedModel;
```

## Key Classes and Methods

### Core Classes

- **`Diagram`** - Main diagram control inheriting from `ScrollControl`
- **`Model`** - Contains diagram nodes, connectors, and layers
- **`View`** - Renders the model and manages display properties
- **`Controller`** - Handles user input and tool activation

### Node Classes

- **`Node`** - Base class for all diagram nodes
- **`Rectangle`, `Ellipse`, `Polygon`, `RoundRect`** - Basic shape nodes
- **`Line`, `PolyLine`, `Curve`, `Bezier`, `Spline`** - Line-based nodes
- **`TextNode`, `RichTextNode`** - Text nodes
- **`BitmapNode`** - Image nodes
- **`Group`** - Container for grouped nodes

### Connector Classes

- **`OrthogonalConnector`** - 90-degree angle connectors
- **`DirectedLinesConnector`** - Smart routed connectors
- **`LineConnector`** - Straight line connectors

### Common Methods

- **`Model.AppendChild(node)`** - Add node to model
- **`Controller.ActivateTool(toolName)`** - Activate drawing tool
- **`Diagram.UpdateView()`** - Refresh diagram display
- **`Node.Labels.Add(label)`** - Add label to node
- **`Port.TryConnect(endpoint)`** - Connect nodes via ports
- **`Controller.Group()`** - Group selected nodes
- **`Model.HistoryManager.Undo()`** - Undo last action

## Common Use Cases

1. **Flowchart Designer** - Create process flows with decision nodes, start/end symbols, and directional connectors
2. **Organizational Chart** - Build hierarchical structures with automatic layout and employee nodes
3. **Network Diagram** - Visualize network topology with servers, routers, and connection lines
4. **UML Editor** - Design class diagrams, sequence diagrams, and use case diagrams
5. **Mind Map** - Create radial mind maps with central ideas and branching concepts
6. **Workflow Designer** - Design business process workflows with BPMN notation
7. **ER Diagram** - Model database schemas with entities, attributes, and relationships
8. **Circuit Designer** - Design electrical circuits with components and wire connections

## Related Skills

- [Implementing Syncfusion Windows Forms Components](../../) - Main library navigation
- Component categories available in the main library skill

---

**Need Help?** Check the troubleshooting reference for common issues and solutions.
