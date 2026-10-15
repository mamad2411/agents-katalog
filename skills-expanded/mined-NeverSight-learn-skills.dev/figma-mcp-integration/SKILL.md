---
name: figma-mcp-integration
description: Enable AI agents to read and modify Figma designs programmatically through Model Context Protocol integration
triggers:
  - "connect to Figma"
  - "read Figma design"
  - "modify Figma elements"
  - "create Figma components"
  - "update text in Figma"
  - "export Figma nodes"
  - "set up Figma MCP"
  - "automate Figma design"
---

# Figma MCP Integration

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill enables AI agents to communicate with Figma through the Model Context Protocol (MCP), allowing programmatic reading and modification of Figma designs. The integration supports creating elements, modifying layouts, batch text updates, annotations, and prototype flow visualization.

## Installation

### 1. Install Bun Runtime

```bash
curl -fsSL https://bun.sh/install | bash
```

### 2. Quick Setup

```bash
# Clone and setup
git clone https://github.com/grab/cursor-talk-to-figma-mcp.git
cd cursor-talk-to-figma-mcp
bun setup
```

### 3. Start WebSocket Server

```bash
bun socket
```

### 4. Configure MCP in Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "TalkToFigma": {
      "command": "bunx",
      "args": ["cursor-talk-to-figma-mcp@latest"]
    }
  }
}
```

For local development:

```json
{
  "mcpServers": {
    "TalkToFigma": {
      "command": "bun",
      "args": ["/absolute/path/to/src/talk_to_figma_mcp/server.ts"]
    }
  }
}
```

### 5. Install Figma Plugin

- Visit [Figma Community Plugin](https://www.figma.com/community/plugin/1485687494525374295/cursor-talk-to-figma-mcp-plugin)
- Or in Figma: Plugins > Development > New Plugin > Link existing plugin > Select `src/cursor_mcp_plugin/manifest.json`

### Windows + WSL Configuration

```bash
# Install via PowerShell
powershell -c "irm bun.sh/install.ps1|iex"
```

Edit `src/socket.ts` to allow WSL connections:

```typescript
// Uncomment for Windows WSL
hostname: "0.0.0.0",
```

## Core Workflow

### 1. Establish Connection

```javascript
// First, join a channel to connect MCP server with Figma plugin
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "join_channel",
  arguments: {
    channelId: "design-session-1"
  }
});
```

### 2. Read Document Structure

```javascript
// Get document overview
const docInfo = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_document_info",
  arguments: {}
});

// Get current selection
const selection = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_selection",
  arguments: {}
});

// Read detailed design info from selection
const designDetails = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "read_my_design",
  arguments: {}
});
```

### 3. Query Specific Nodes

```javascript
// Get single node info
const nodeInfo = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_node_info",
  arguments: {
    nodeId: "123:456"
  }
});

// Get multiple nodes
const nodesInfo = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_nodes_info",
  arguments: {
    nodeIds: ["123:456", "789:012", "345:678"]
  }
});
```

## Creating Elements

### Create Frames and Shapes

```javascript
// Create frame container
const frame = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_frame",
  arguments: {
    x: 100,
    y: 100,
    width: 400,
    height: 300,
    name: "Hero Section"
  }
});

// Create rectangle
const rect = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_rectangle",
  arguments: {
    x: 120,
    y: 120,
    width: 200,
    height: 100,
    name: "Card Background"
  }
});

// Create text node
const text = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_text",
  arguments: {
    x: 140,
    y: 140,
    characters: "Welcome to our app",
    name: "Heading",
    fontSize: 24,
    fontFamily: "Inter",
    fontWeight: "Bold"
  }
});
```

### Create Component Instances

```javascript
// Get available components
const components = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_local_components",
  arguments: {}
});

// Create instance
const instance = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_component_instance",
  arguments: {
    componentKey: "abc123def456",
    x: 200,
    y: 200
  }
});
```

## Styling Elements

### Colors and Fills

```javascript
// Set fill color
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_fill_color",
  arguments: {
    nodeId: "123:456",
    r: 0.2,
    g: 0.5,
    b: 0.9,
    a: 1.0
  }
});

// Set stroke
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_stroke_color",
  arguments: {
    nodeId: "123:456",
    r: 0.1,
    g: 0.1,
    b: 0.1,
    a: 1.0,
    strokeWeight: 2
  }
});

// Set corner radius
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_corner_radius",
  arguments: {
    nodeId: "123:456",
    radius: 8
  }
});

// Set individual corners
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_corner_radius",
  arguments: {
    nodeId: "123:456",
    topLeft: 16,
    topRight: 16,
    bottomLeft: 4,
    bottomRight: 4
  }
});
```

## Auto Layout Configuration

### Enable Auto Layout

```javascript
// Set horizontal auto layout
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_layout_mode",
  arguments: {
    nodeId: "123:456",
    layoutMode: "HORIZONTAL",
    layoutWrap: "NO_WRAP"
  }
});

// Set vertical with wrapping
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_layout_mode",
  arguments: {
    nodeId: "123:456",
    layoutMode: "VERTICAL",
    layoutWrap: "WRAP"
  }
});
```

### Configure Spacing and Padding

```javascript
// Set padding
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_padding",
  arguments: {
    nodeId: "123:456",
    top: 24,
    right: 16,
    bottom: 24,
    left: 16
  }
});

// Set item spacing
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_item_spacing",
  arguments: {
    nodeId: "123:456",
    spacing: 12
  }
});
```

### Alignment and Sizing

```javascript
// Set alignment
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_axis_align",
  arguments: {
    nodeId: "123:456",
    primaryAxisAlign: "SPACE_BETWEEN",
    counterAxisAlign: "CENTER"
  }
});

// Set sizing behavior
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_layout_sizing",
  arguments: {
    nodeId: "123:456",
    horizontal: "FILL",
    vertical: "HUG"
  }
});
```

## Text Operations

### Scan and Update Text

```javascript
// Scan text nodes with chunking for large designs
const textNodes = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "scan_text_nodes",
  arguments: {
    startIndex: 0,
    chunkSize: 100,
    nodeId: "page-node-id" // Optional: scope to specific node
  }
});

// Update single text node
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_text_content",
  arguments: {
    nodeId: "123:456",
    characters: "Updated heading text"
  }
});

// Batch update multiple text nodes
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_multiple_text_contents",
  arguments: {
    updates: [
      { nodeId: "123:456", characters: "New title" },
      { nodeId: "789:012", characters: "New description" },
      { nodeId: "345:678", characters: "Updated label" }
    ]
  }
});
```

### Bulk Text Replacement Pattern

```javascript
// 1. Scan all text nodes
const allTextNodes = [];
let startIndex = 0;
const chunkSize = 100;
let hasMore = true;

while (hasMore) {
  const chunk = await use_mcp_tool({
    server_name: "TalkToFigma",
    tool_name: "scan_text_nodes",
    arguments: { startIndex, chunkSize }
  });
  
  allTextNodes.push(...chunk.nodes);
  hasMore = chunk.hasMore;
  startIndex += chunkSize;
}

// 2. Filter and prepare updates
const updates = allTextNodes
  .filter(node => node.characters.includes("placeholder"))
  .map(node => ({
    nodeId: node.id,
    characters: node.characters.replace("placeholder", "actual content")
  }));

// 3. Batch update
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_multiple_text_contents",
  arguments: { updates }
});
```

## Layout Manipulation

### Move and Resize

```javascript
// Move node
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "move_node",
  arguments: {
    nodeId: "123:456",
    x: 300,
    y: 200
  }
});

// Resize node
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "resize_node",
  arguments: {
    nodeId: "123:456",
    width: 500,
    height: 400
  }
});

// Clone node
const cloned = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "clone_node",
  arguments: {
    nodeId: "123:456",
    offsetX: 50,
    offsetY: 50
  }
});
```

### Focus and Selection

```javascript
// Focus on specific node
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_focus",
  arguments: {
    nodeId: "123:456"
  }
});

// Set multiple selections
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_selections",
  arguments: {
    nodeIds: ["123:456", "789:012", "345:678"]
  }
});
```

### Delete Nodes

```javascript
// Delete single node
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "delete_node",
  arguments: {
    nodeId: "123:456"
  }
});

// Delete multiple nodes
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "delete_multiple_nodes",
  arguments: {
    nodeIds: ["123:456", "789:012", "345:678"]
  }
});
```

## Annotations

### Create and Manage Annotations

```javascript
// Get existing annotations
const annotations = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_annotations",
  arguments: {
    nodeId: "page-id" // Optional: scope to specific node
  }
});

// Create single annotation
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_annotation",
  arguments: {
    nodeId: "123:456",
    label: "Design Note",
    text: "This button should be **bold** and use primary color",
    category: "NOTE"
  }
});

// Batch create annotations
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_multiple_annotations",
  arguments: {
    annotations: [
      {
        nodeId: "123:456",
        label: "Fix spacing",
        text: "Increase padding to 24px",
        category: "ISSUE"
      },
      {
        nodeId: "789:012",
        label: "Accessibility",
        text: "Add alt text for screen readers",
        category: "REVIEW"
      }
    ]
  }
});
```

### Scan Nodes for Annotation Targets

```javascript
// Find specific node types
const buttons = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "scan_nodes_by_types",
  arguments: {
    nodeTypes: ["COMPONENT", "INSTANCE"],
    namePattern: "button" // Optional filter
  }
});
```

### Convert Legacy Annotations Pattern

```javascript
// 1. Scan for legacy annotation text nodes
const textNodes = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "scan_text_nodes",
  arguments: { startIndex: 0, chunkSize: 200 }
});

// 2. Identify annotation markers (e.g., "1. Fix this", "2. Update color")
const legacyAnnotations = textNodes.nodes
  .filter(node => /^\d+\./.test(node.characters))
  .map(node => ({
    nodeId: node.id,
    number: node.characters.match(/^(\d+)\./)[1],
    text: node.characters.replace(/^\d+\.\s*/, ""),
    position: { x: node.x, y: node.y }
  }));

// 3. Find UI elements near each annotation
const targetElements = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "scan_nodes_by_types",
  arguments: {
    nodeTypes: ["FRAME", "COMPONENT", "INSTANCE", "TEXT"]
  }
});

// 4. Match annotations to targets and create native annotations
const newAnnotations = legacyAnnotations.map(legacy => {
  const target = findClosestElement(targetElements, legacy.position);
  return {
    nodeId: target.id,
    label: `Note ${legacy.number}`,
    text: legacy.text,
    category: "NOTE"
  };
});

await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_multiple_annotations",
  arguments: { annotations: newAnnotations }
});

// 5. Delete legacy annotation nodes
const legacyIds = legacyAnnotations.map(a => a.nodeId);
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "delete_multiple_nodes",
  arguments: { nodeIds: legacyIds }
});
```

## Component Instance Overrides

### Extract and Apply Overrides

```javascript
// 1. Get overrides from source instance
const overrides = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_instance_overrides",
  arguments: {
    instanceId: "source-instance-id"
  }
});

// 2. Apply overrides to target instances
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_instance_overrides",
  arguments: {
    targetInstanceIds: [
      "target-instance-1",
      "target-instance-2",
      "target-instance-3"
    ],
    overrides: overrides
  }
});
```

### Bulk Override Propagation Pattern

```javascript
// 1. Select source instance with desired overrides
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_focus",
  arguments: { nodeId: "source-instance" }
});

// 2. Extract overrides
const sourceOverrides = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_instance_overrides",
  arguments: { instanceId: "source-instance" }
});

// 3. Find all instances of same component
const components = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_local_components",
  arguments: {}
});

const targetInstances = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "scan_nodes_by_types",
  arguments: {
    nodeTypes: ["INSTANCE"],
    namePattern: "ComponentName"
  }
});

// 4. Apply to all matching instances
const targetIds = targetInstances
  .filter(node => node.mainComponent?.key === "component-key")
  .map(node => node.id);

await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_instance_overrides",
  arguments: {
    targetInstanceIds: targetIds,
    overrides: sourceOverrides
  }
});
```

## Prototype Reactions and Connectors

### Visualize Prototype Flows

```javascript
// 1. Get prototype reactions with visual highlights
const reactions = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_reactions",
  arguments: {
    nodeId: "page-id" // Optional: scope to specific node
  }
});

// 2. Copy a FigJam connector and set as default style
// (Manually copy a styled connector in Figma first)
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_default_connector",
  arguments: {}
});

// 3. Create connector lines from reactions
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_connections",
  arguments: {
    connections: reactions.map(r => ({
      sourceNodeId: r.sourceNodeId,
      targetNodeId: r.destinationId
    }))
  }
});

// Or create custom connections
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_connections",
  arguments: {
    connections: [
      { sourceNodeId: "start-node", targetNodeId: "step-1" },
      { sourceNodeId: "step-1", targetNodeId: "step-2" },
      { sourceNodeId: "step-2", targetNodeId: "end-node" }
    ]
  }
});
```

## Export Operations

### Export Nodes as Images

```javascript
// Export as PNG
const pngExport = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "export_node_as_image",
  arguments: {
    nodeId: "123:456",
    format: "PNG",
    scale: 2
  }
});

// Export as SVG
const svgExport = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "export_node_as_image",
  arguments: {
    nodeId: "123:456",
    format: "SVG"
  }
});

// Export as JPG
const jpgExport = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "export_node_as_image",
  arguments: {
    nodeId: "123:456",
    format: "JPG",
    scale: 1
  }
});

// Note: Currently returns base64 text
```

## Component and Style Management

### Query Components and Styles

```javascript
// Get all local components
const components = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_local_components",
  arguments: {}
});

// Get all styles
const styles = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_styles",
  arguments: {}
});
```

## Common Workflows

### Design System Component Creation

```javascript
// 1. Create base button component frame
const buttonFrame = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_frame",
  arguments: {
    x: 100, y: 100, width: 120, height: 44,
    name: "Button/Primary"
  }
});

// 2. Configure auto layout
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_layout_mode",
  arguments: {
    nodeId: buttonFrame.id,
    layoutMode: "HORIZONTAL"
  }
});

await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_padding",
  arguments: {
    nodeId: buttonFrame.id,
    top: 12, right: 24, bottom: 12, left: 24
  }
});

await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_axis_align",
  arguments: {
    nodeId: buttonFrame.id,
    primaryAxisAlign: "CENTER",
    counterAxisAlign: "CENTER"
  }
});

// 3. Add button text
const buttonText = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_text",
  arguments: {
    x: 0, y: 0,
    characters: "Button",
    fontSize: 16,
    fontFamily: "Inter",
    fontWeight: "Semi Bold"
  }
});

// 4. Style the button
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_fill_color",
  arguments: {
    nodeId: buttonFrame.id,
    r: 0.2, g: 0.5, b: 1.0, a: 1.0
  }
});

await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_corner_radius",
  arguments: {
    nodeId: buttonFrame.id,
    radius: 8
  }
});
```

### Responsive Card Grid

```javascript
// 1. Create container
const grid = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "create_frame",
  arguments: {
    x: 0, y: 0, width: 1200, height: 800,
    name: "Card Grid"
  }
});

// 2. Configure as horizontal wrapping grid
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_layout_mode",
  arguments: {
    nodeId: grid.id,
    layoutMode: "HORIZONTAL",
    layoutWrap: "WRAP"
  }
});

await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_item_spacing",
  arguments: { nodeId: grid.id, spacing: 16 }
});

// 3. Create card instances
const cardData = [
  { title: "Card 1", desc: "Description 1" },
  { title: "Card 2", desc: "Description 2" },
  { title: "Card 3", desc: "Description 3" }
];

for (const data of cardData) {
  const card = await use_mcp_tool({
    server_name: "TalkToFigma",
    tool_name: "create_component_instance",
    arguments: {
      componentKey: "card-component-key",
      x: 0, y: 0
    }
  });
  
  // Update card text (if card has text nodes)
  await use_mcp_tool({
    server_name: "TalkToFigma",
    tool_name: "set_multiple_text_contents",
    arguments: {
      updates: [
        { nodeId: `${card.id}:title`, characters: data.title },
        { nodeId: `${card.id}:desc`, characters: data.desc }
      ]
    }
  });
}
```

### Content Localization

```javascript
// 1. Scan all text in design
const allText = [];
let index = 0;
let hasMore = true;

while (hasMore) {
  const result = await use_mcp_tool({
    server_name: "TalkToFigma",
    tool_name: "scan_text_nodes",
    arguments: { startIndex: index, chunkSize: 100 }
  });
  allText.push(...result.nodes);
  hasMore = result.hasMore;
  index += 100;
}

// 2. Prepare translations
const translations = {
  "Welcome": "Bienvenido",
  "Sign Up": "Registrarse",
  "Learn More": "Aprende Más"
};

// 3. Map and update
const updates = allText
  .filter(node => translations[node.characters])
  .map(node => ({
    nodeId: node.id,
    characters: translations[node.characters]
  }));

await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "set_multiple_text_contents",
  arguments: { updates }
});
```

## Troubleshooting

### Connection Issues

**WebSocket not connecting:**
```bash
# Ensure WebSocket server is running
bun socket

# For WSL, check hostname is set to 0.0.0.0 in src/socket.ts
# Check firewall settings
```

**MCP not available in Cursor:**
```bash
# Verify mcp.json configuration
cat ~/.cursor/mcp.json

# Restart Cursor after configuration changes

# For local development, use absolute paths
# "args": ["/full/path/to/src/talk_to_figma_mcp/server.ts"]
```

### Channel Connection

**Commands not reaching Figma:**
```javascript
// Always join channel first
await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "join_channel",
  arguments: { channelId: "unique-session-id" }
});

// Verify Figma plugin is running and connected to same channel
```

### Node Operations

**Node not found errors:**
```javascript
// Always verify node exists before operations
const nodeInfo = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_node_info",
  arguments: { nodeId: "123:456" }
});

// Use get_selection to get current selection IDs
const selection = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_selection",
  arguments: {}
});
```

**Text update failures:**
```javascript
// Ensure text nodes have proper fonts loaded
// Check font availability in Figma before setting

// Use set_text_content for simple updates
// Use set_multiple_text_contents for batch operations

// Verify node is actually a TEXT type
const nodeInfo = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_node_info",
  arguments: { nodeId: "text-node-id" }
});

if (nodeInfo.type !== "TEXT") {
  throw new Error("Node is not a text node");
}
```

### Performance

**Large design handling:**
```javascript
// Use chunking for text scans
const CHUNK_SIZE = 50; // Adjust based on design complexity

// Process in batches
const batchSize = 20;
for (let i = 0; i < updates.length; i += batchSize) {
  const batch = updates.slice(i, i + batchSize);
  await use_mcp_tool({
    server_name: "TalkToFigma",
    tool_name: "set_multiple_text_contents",
    arguments: { updates: batch }
  });
}
```

**Memory issues with exports:**
```javascript
// Export specific nodes instead of entire pages
// Use appropriate scale factors (1x, 2x)
// Consider SVG for scalable exports vs raster formats
```

### Auto Layout Issues

**Elements not respecting layout:**
```javascript
// Verify parent has auto layout enabled
const parentInfo = await use_mcp_tool({
  server_name: "TalkToFigma",
  tool_name: "get_node_info",
  arguments: { nodeId: "parent-id" }
});

// Set layout mode first
await use_mcp_tool
