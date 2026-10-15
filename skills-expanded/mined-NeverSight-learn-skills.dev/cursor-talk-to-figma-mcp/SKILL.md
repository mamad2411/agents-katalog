---
name: cursor-talk-to-figma-mcp
description: MCP server enabling AI agents to read and modify Figma designs programmatically through WebSocket communication
triggers:
  - interact with figma designs
  - read figma document structure
  - modify figma components programmatically
  - automate figma design tasks
  - sync code with figma designs
  - extract design information from figma
  - create figma elements via ai
  - update figma text content in bulk
---

# Cursor Talk to Figma MCP

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill enables AI agents to communicate with Figma through the Model Context Protocol (MCP), allowing programmatic reading and modification of design files. The integration uses a WebSocket server to bridge AI agents (Cursor, Claude Code) with a Figma plugin.

## Installation

### Prerequisites

Install Bun runtime:

```bash
curl -fsSL https://bun.sh/install | bash
```

### Quick Setup

Run the automated setup which installs the MCP server in your Cursor configuration:

```bash
bun setup
```

### Manual MCP Configuration

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

For local development, use direct file path:

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

### Start WebSocket Server

```bash
bun socket
```

### Figma Plugin Installation

1. Install from [Figma Community](https://www.figma.com/community/plugin/1485687494525374295/cursor-talk-to-figma-mcp-plugin)
2. Or develop locally: Plugins > Development > New Plugin > Link existing plugin > Select `src/cursor_mcp_plugin/manifest.json`

## Core Workflow

### 1. Establish Connection

```javascript
// First, join a channel to communicate with Figma
await use_mcp_tool("TalkToFigma", "join_channel", {
  channelId: "my-design-session"
});
```

### 2. Read Design Information

```javascript
// Get document overview
const docInfo = await use_mcp_tool("TalkToFigma", "get_document_info", {});

// Get current selection
const selection = await use_mcp_tool("TalkToFigma", "get_selection", {});

// Get detailed node information
const nodeInfo = await use_mcp_tool("TalkToFigma", "get_node_info", {
  nodeId: "123:456"
});

// Read current selection details without parameters
const selectionDetails = await use_mcp_tool("TalkToFigma", "read_my_design", {});
```

### 3. Create Elements

```javascript
// Create a frame
const frame = await use_mcp_tool("TalkToFigma", "create_frame", {
  x: 0,
  y: 0,
  width: 375,
  height: 812,
  name: "iPhone Frame"
});

// Create a rectangle
const rect = await use_mcp_tool("TalkToFigma", "create_rectangle", {
  x: 20,
  y: 20,
  width: 335,
  height: 200,
  name: "Header Background"
});

// Create text
const text = await use_mcp_tool("TalkToFigma", "create_text", {
  x: 40,
  y: 100,
  characters: "Welcome to the App",
  fontSize: 24,
  fontName: { family: "Inter", style: "Bold" },
  name: "Header Title"
});
```

### 4. Modify Existing Elements

```javascript
// Set fill color (RGBA 0-1 range)
await use_mcp_tool("TalkToFigma", "set_fill_color", {
  nodeId: "123:456",
  r: 0.2,
  g: 0.4,
  b: 0.8,
  a: 1.0
});

// Set stroke
await use_mcp_tool("TalkToFigma", "set_stroke_color", {
  nodeId: "123:456",
  r: 0.1,
  g: 0.1,
  b: 0.1,
  a: 1.0,
  strokeWeight: 2
});

// Set corner radius
await use_mcp_tool("TalkToFigma", "set_corner_radius", {
  nodeId: "123:456",
  radius: 12
});

// Move node
await use_mcp_tool("TalkToFigma", "move_node", {
  nodeId: "123:456",
  x: 100,
  y: 200
});

// Resize node
await use_mcp_tool("TalkToFigma", "resize_node", {
  nodeId: "123:456",
  width: 300,
  height: 150
});
```

## Auto Layout Configuration

```javascript
// Set layout mode
await use_mcp_tool("TalkToFigma", "set_layout_mode", {
  nodeId: "123:456",
  layoutMode: "VERTICAL", // "NONE", "HORIZONTAL", "VERTICAL"
  layoutWrap: "NO_WRAP"   // "NO_WRAP", "WRAP"
});

// Set padding
await use_mcp_tool("TalkToFigma", "set_padding", {
  nodeId: "123:456",
  paddingTop: 24,
  paddingRight: 16,
  paddingBottom: 24,
  paddingLeft: 16
});

// Set alignment
await use_mcp_tool("TalkToFigma", "set_axis_align", {
  nodeId: "123:456",
  primaryAxisAlignItems: "CENTER",      // "MIN", "CENTER", "MAX", "SPACE_BETWEEN"
  counterAxisAlignItems: "CENTER"       // "MIN", "CENTER", "MAX", "BASELINE"
});

// Set sizing behavior
await use_mcp_tool("TalkToFigma", "set_layout_sizing", {
  nodeId: "123:456",
  layoutSizingHorizontal: "HUG",  // "FIXED", "HUG", "FILL"
  layoutSizingVertical: "FIXED"
});

// Set item spacing
await use_mcp_tool("TalkToFigma", "set_item_spacing", {
  nodeId: "123:456",
  itemSpacing: 12
});
```

## Bulk Text Operations

### Scan Text Nodes

```javascript
// Scan all text nodes with chunking for large designs
const textNodes = await use_mcp_tool("TalkToFigma", "scan_text_nodes", {
  chunkSize: 50,        // Process 50 nodes at a time
  startIndex: 0,        // Start from beginning
  parentNodeId: null    // Scan entire document (or specify parent)
});

// Response includes:
// - nodes: Array of text node info
// - hasMore: Boolean indicating more chunks available
// - nextIndex: Index for next chunk
// - total: Total number of text nodes
```

### Update Single Text

```javascript
await use_mcp_tool("TalkToFigma", "set_text_content", {
  nodeId: "123:456",
  characters: "Updated heading text"
});
```

### Batch Update Multiple Texts

```javascript
await use_mcp_tool("TalkToFigma", "set_multiple_text_contents", {
  updates: [
    { nodeId: "123:456", characters: "New Title" },
    { nodeId: "123:789", characters: "New Description" },
    { nodeId: "123:101", characters: "Updated Label" }
  ]
});
```

## Annotations

### Get Annotations

```javascript
// Get all annotations in document
const annotations = await use_mcp_tool("TalkToFigma", "get_annotations", {});

// Get annotations for specific node
const nodeAnnotations = await use_mcp_tool("TalkToFigma", "get_annotations", {
  nodeId: "123:456"
});
```

### Create/Update Annotation

```javascript
await use_mcp_tool("TalkToFigma", "set_annotation", {
  nodeId: "123:456",
  text: "This component needs **accessibility** improvements:\n- Add ARIA labels\n- Improve color contrast",
  category: "DESIGN" // "DESIGN", "ENGINEERING", "CONTENT", "OTHER"
});
```

### Batch Create Annotations

```javascript
await use_mcp_tool("TalkToFigma", "set_multiple_annotations", {
  annotations: [
    {
      nodeId: "123:456",
      text: "Update to new brand colors",
      category: "DESIGN"
    },
    {
      nodeId: "123:789",
      text: "Implement loading state",
      category: "ENGINEERING"
    }
  ]
});
```

## Components and Instances

### Get Components

```javascript
const components = await use_mcp_tool("TalkToFigma", "get_local_components", {});
```

### Create Component Instance

```javascript
const instance = await use_mcp_tool("TalkToFigma", "create_component_instance", {
  componentKey: "abc123def456",
  x: 100,
  y: 100
});
```

### Instance Override Management

```javascript
// Extract overrides from source instance
const overrides = await use_mcp_tool("TalkToFigma", "get_instance_overrides", {
  sourceInstanceId: "123:456"
});

// Apply overrides to target instances
await use_mcp_tool("TalkToFigma", "set_instance_overrides", {
  targetInstanceIds: ["123:789", "123:101"],
  overrides: overrides.overrides
});
```

## Prototyping and Connections

### Get Prototype Reactions

```javascript
// Get all prototype reactions with visual highlights
const reactions = await use_mcp_tool("TalkToFigma", "get_reactions", {});

// Response includes source/destination nodes and interaction details
```

### Create FigJam Connectors

```javascript
// First, copy a connector in FigJam and set it as default
await use_mcp_tool("TalkToFigma", "set_default_connector", {});

// Create connections based on prototype flow
await use_mcp_tool("TalkToFigma", "create_connections", {
  connections: [
    { from: "123:456", to: "123:789" },
    { from: "123:789", to: "123:101" }
  ]
});
```

## Selection and Focus

```javascript
// Focus on specific node (selects and scrolls viewport)
await use_mcp_tool("TalkToFigma", "set_focus", {
  nodeId: "123:456"
});

// Select multiple nodes
await use_mcp_tool("TalkToFigma", "set_selections", {
  nodeIds: ["123:456", "123:789", "123:101"]
});
```

## Node Management

### Clone Nodes

```javascript
const clone = await use_mcp_tool("TalkToFigma", "clone_node", {
  nodeId: "123:456",
  offsetX: 20,    // Optional X offset
  offsetY: 20     // Optional Y offset
});
```

### Delete Nodes

```javascript
// Delete single node
await use_mcp_tool("TalkToFigma", "delete_node", {
  nodeId: "123:456"
});

// Delete multiple nodes efficiently
await use_mcp_tool("TalkToFigma", "delete_multiple_nodes", {
  nodeIds: ["123:456", "123:789", "123:101"]
});
```

### Get Multiple Nodes Info

```javascript
const nodesInfo = await use_mcp_tool("TalkToFigma", "get_nodes_info", {
  nodeIds: ["123:456", "123:789", "123:101"]
});
```

## Export

```javascript
// Export node as image
const imageData = await use_mcp_tool("TalkToFigma", "export_node_as_image", {
  nodeId: "123:456",
  format: "PNG",      // "PNG", "JPG", "SVG", "PDF"
  scale: 2            // Optional: 1, 2, 3, 4
});

// Returns base64 encoded image data
```

## Scan Nodes by Type

```javascript
// Find all nodes of specific types (useful for finding annotation targets)
const frames = await use_mcp_tool("TalkToFigma", "scan_nodes_by_types", {
  types: ["FRAME", "COMPONENT", "INSTANCE"],
  parentNodeId: null  // Optional: limit to specific parent
});
```

## Common Patterns

### Pattern: Create a Card Component

```javascript
// 1. Create container frame
const card = await use_mcp_tool("TalkToFigma", "create_frame", {
  x: 0, y: 0, width: 300, height: 400, name: "Card"
});

// 2. Set auto layout
await use_mcp_tool("TalkToFigma", "set_layout_mode", {
  nodeId: card.id, layoutMode: "VERTICAL"
});

await use_mcp_tool("TalkToFigma", "set_padding", {
  nodeId: card.id,
  paddingTop: 20, paddingRight: 20,
  paddingBottom: 20, paddingLeft: 20
});

await use_mcp_tool("TalkToFigma", "set_item_spacing", {
  nodeId: card.id, itemSpacing: 16
});

// 3. Style the card
await use_mcp_tool("TalkToFigma", "set_fill_color", {
  nodeId: card.id, r: 1, g: 1, b: 1, a: 1
});

await use_mcp_tool("TalkToFigma", "set_corner_radius", {
  nodeId: card.id, radius: 8
});

// 4. Add shadow via stroke as workaround
await use_mcp_tool("TalkToFigma", "set_stroke_color", {
  nodeId: card.id, r: 0.9, g: 0.9, b: 0.9, a: 1, strokeWeight: 1
});
```

### Pattern: Bulk Content Replacement

```javascript
// 1. Scan all text nodes in chunks
let allTextNodes = [];
let hasMore = true;
let nextIndex = 0;

while (hasMore) {
  const result = await use_mcp_tool("TalkToFigma", "scan_text_nodes", {
    chunkSize: 50,
    startIndex: nextIndex
  });
  
  allTextNodes = allTextNodes.concat(result.nodes);
  hasMore = result.hasMore;
  nextIndex = result.nextIndex;
}

// 2. Filter and prepare updates
const updates = allTextNodes
  .filter(node => node.characters.includes("old-text"))
  .map(node => ({
    nodeId: node.id,
    characters: node.characters.replace("old-text", "new-text")
  }));

// 3. Batch update
await use_mcp_tool("TalkToFigma", "set_multiple_text_contents", {
  updates: updates
});
```

### Pattern: Convert Legacy Annotations

```javascript
// 1. Scan for text nodes with numbered markers
const textNodes = await use_mcp_tool("TalkToFigma", "scan_text_nodes", {});
const markers = textNodes.nodes.filter(n => /^\d+\./.test(n.characters));

// 2. Find potential annotation targets
const targets = await use_mcp_tool("TalkToFigma", "scan_nodes_by_types", {
  types: ["FRAME", "COMPONENT", "INSTANCE", "RECTANGLE"]
});

// 3. Match markers to targets (by proximity, naming, or path)
const annotations = markers.map(marker => {
  const targetNode = findClosestTarget(marker, targets.nodes);
  return {
    nodeId: targetNode.id,
    text: marker.characters.replace(/^\d+\.\s*/, ""),
    category: "DESIGN"
  };
});

// 4. Create native annotations
await use_mcp_tool("TalkToFigma", "set_multiple_annotations", {
  annotations: annotations
});

// 5. Delete old marker nodes
await use_mcp_tool("TalkToFigma", "delete_multiple_nodes", {
  nodeIds: markers.map(m => m.id)
});
```

### Pattern: Prototype to Connector Visualization

```javascript
// 1. Get prototype reactions
const reactions = await use_mcp_tool("TalkToFigma", "get_reactions", {});

// 2. Copy and set default connector style in FigJam
await use_mcp_tool("TalkToFigma", "set_default_connector", {});

// 3. Extract connections from reactions
const connections = reactions.reactions.map(r => ({
  from: r.node.id,
  to: r.action.destinationId
}));

// 4. Create connector lines
await use_mcp_tool("TalkToFigma", "create_connections", {
  connections: connections
});
```

## Windows + WSL Configuration

For Windows with WSL, uncomment the hostname in `src/socket.ts`:

```typescript
// Uncomment for Windows WSL
hostname: "0.0.0.0",
```

Install Bun via PowerShell:

```powershell
irm bun.sh/install.ps1|iex
```

## Troubleshooting

### WebSocket Connection Issues

- Ensure WebSocket server is running: `bun socket`
- Verify Figma plugin is active and connected
- Check that `join_channel` was called successfully
- For WSL, ensure hostname is set to `0.0.0.0`

### MCP Server Not Found

- Verify `~/.cursor/mcp.json` configuration is correct
- Restart Cursor after configuration changes
- Check that Bun is installed and in PATH
- For local development, use absolute paths

### Commands Fail Silently

- Always join a channel first with `join_channel`
- Verify node IDs exist using `get_document_info` or `get_selection`
- Check WebSocket server logs for errors
- Ensure Figma file is open and plugin is running

### Text Update Failures

- Verify node is actually a TEXT node type
- Check that text layer is not locked
- For batch updates, process in smaller chunks if needed
- Missing fonts may cause failures - ensure fonts are available

### Color Values

All color values use 0-1 range (not 0-255):
- Convert: `rgbValue / 255`
- Example: RGB(51, 102, 204) = r: 0.2, g: 0.4, b: 0.8

### Auto Layout Constraints

- `set_layout_mode` must be called before other auto-layout properties
- Cannot set padding on non-auto-layout frames
- Item spacing only works in auto-layout frames
- Some sizing modes require specific layout configurations

## Best Practices

1. **Always establish connection first** - Call `join_channel` before any other commands
2. **Get context before modifying** - Use `get_document_info` and `get_selection` to understand structure
3. **Use batch operations** - Prefer `set_multiple_text_contents` over multiple `set_text_content` calls
4. **Chunk large operations** - Use chunking parameters for designs with many nodes
5. **Verify changes** - Use `get_node_info` after modifications to confirm success
6. **Handle errors gracefully** - All commands can throw exceptions, implement proper error handling
7. **Use component instances** - Prefer instances over duplicating elements for consistency
8. **Organize with frames** - Use frames with auto-layout for structured, responsive designs
9. **Clean up legacy elements** - Delete old nodes after migrating to new patterns
10. **Test incrementally** - Verify each step when building complex automation workflows
