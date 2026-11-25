---
name: figma-console-mcp-design-system-api
description: Connect AI to Figma for design system extraction, component creation, token sync, and visual debugging via MCP
triggers:
  - connect to figma design system
  - extract figma components and variables
  - create figma frames and components
  - sync design tokens with figma
  - debug figma designs with screenshots
  - manage figma variables and styles
  - export figma design tokens to code
  - build ui components in figma
---

# Figma Console MCP Design System API

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## What is Figma Console MCP?

Figma Console MCP is a Model Context Protocol server that bridges AI assistants with Figma, providing **103 tools** for design system extraction, component creation, bidirectional token synchronization, and visual debugging. It enables AI to read, create, and modify Figma designs programmatically.

**Key capabilities:**
- **Design extraction** - Pull variables, components, styles, and full design trees
- **Bidirectional token sync** - Export variables to DTCG JSON + CSS, push edits back to Figma
- **Component creation** - Create frames, shapes, text, and instantiate components
- **Variable management** - Create, update, rename, delete design tokens
- **Visual debugging** - Screenshot nodes, scan accessibility, diff versions
- **FigJam & Slides** - Create stickies, flowcharts, presentations
- **Real-time monitoring** - Watch console logs and selection changes (Desktop Bridge)

## Installation

### NPX Setup (Recommended)

**Prerequisites:**
- Node.js 18+
- Figma Desktop app
- Figma personal access token ([create one](https://help.figma.com/hc/en-us/articles/8085703771159))

**Configuration for Claude Code:**
```bash
claude mcp add figma-console -s user \
  -e FIGMA_ACCESS_TOKEN=$FIGMA_ACCESS_TOKEN \
  -e ENABLE_MCP_APPS=true \
  -- npx -y figma-console-mcp@latest
```

**Configuration for other MCP clients** (Cursor, Windsurf, Claude Desktop):

Add to your MCP config file:

```json
{
  "mcpServers": {
    "figma-console": {
      "command": "npx",
      "args": ["-y", "figma-console-mcp@latest"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your-token-here",
        "ENABLE_MCP_APPS": "true"
      }
    }
  }
}
```

**Config file locations:**
- **Claude Desktop (macOS):** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Desktop (Windows):** `%APPDATA%\Claude\claude_desktop_config.json`
- **Cursor:** `~/.cursor/mcp.json`
- **Windsurf:** `~/.codeium/windsurf/mcp_config.json`

### Desktop Bridge Plugin Setup

The Desktop Bridge plugin enables write operations (component creation, variable management):

1. Open Figma Desktop
2. Go to **Plugins → Development → Import plugin from manifest**
3. Select `~/.figma-console-mcp/plugin/manifest.json`
4. Run the plugin in your Figma file

The plugin auto-connects to the MCP server on ports 9223-9232.

### Environment Variables

```bash
# Required
FIGMA_ACCESS_TOKEN=figd_xxx  # Personal access token

# Optional
ENABLE_MCP_APPS=true         # Enable Desktop Bridge plugin
LOG_LEVEL=info               # debug | info | warn | error
```

## Core Tool Categories

### 1. Design System Extraction

**Get file metadata:**
```typescript
// Tool: figma_get_file
{
  "file_key": "abc123xyz"
}
// Returns: Full design tree with components, variables, styles
```

**Extract design tokens:**
```typescript
// Tool: figma_export_tokens
{
  "file_key": "abc123xyz",
  "output_format": "dtcg-json"  // or "css-custom-properties"
}
// Returns: DTCG JSON with all variables across collections/modes
```

**List local variables:**
```typescript
// Tool: figma_get_local_variables
{
  "file_key": "abc123xyz"
}
// Returns: All color, number, string, boolean variables
```

### 2. Component & Frame Creation

**Create a basic frame:**
```typescript
// Tool: figma_create_frame
{
  "name": "Hero Section",
  "width": 1200,
  "height": 600,
  "background_color": "#0066FF"
}
// Returns: Created frame node with ID
```

**Create text node:**
```typescript
// Tool: figma_create_text
{
  "parent_id": "frame-node-id",
  "content": "Welcome to Design System",
  "font_size": 48,
  "font_weight": 700,
  "color": "#FFFFFF"
}
```

**Create rectangle with gradient:**
```typescript
// Tool: figma_create_rectangle
{
  "parent_id": "frame-id",
  "width": 300,
  "height": 200,
  "fill": {
    "type": "GRADIENT_LINEAR",
    "gradientStops": [
      {"position": 0, "color": "#FF0080"},
      {"position": 1, "color": "#7928CA"}
    ]
  },
  "corner_radius": 16
}
```

**Instantiate component:**
```typescript
// Tool: figma_create_instance
{
  "component_key": "component-key-from-library",
  "parent_id": "frame-id",
  "x": 100,
  "y": 100
}
```

### 3. Variable & Token Management

**Create color variable:**
```typescript
// Tool: figma_create_variable
{
  "file_key": "abc123xyz",
  "collection_name": "Brand Colors",
  "name": "primary/500",
  "type": "COLOR",
  "value": "#0066FF"
}
```

**Update variable value:**
```typescript
// Tool: figma_update_variable
{
  "file_key": "abc123xyz",
  "variable_id": "var-id",
  "value": "#0055DD"
}
```

**Bidirectional token sync workflow:**
```typescript
// 1. Export tokens to DTCG JSON
// Tool: figma_export_tokens
{
  "file_key": "abc123xyz",
  "output_format": "dtcg-json"
}
// Save response to tokens.json

// 2. Edit tokens.json locally (change hex values, etc.)

// 3. Import changes back to Figma
// Tool: figma_import_tokens
{
  "file_key": "abc123xyz",
  "tokens": {
    "color": {
      "primary": {
        "$type": "color",
        "$value": "#0055DD"
      }
    }
  }
}
// Only changed values trigger API calls (diff-aware merge)
```

### 4. Visual Debugging & Screenshots

**Screenshot a node:**
```typescript
// Tool: figma_get_image
{
  "file_key": "abc123xyz",
  "node_ids": ["node-id-1"],
  "format": "png",
  "scale": 2
}
// Returns: Base64-encoded PNG or image URL
```

**Screenshot with selection context:**
```typescript
// Tool: figma_screenshot_selection
{} // Screenshots currently selected node in Figma Desktop
```

### 5. Accessibility Scanning

**Run design accessibility audit:**
```typescript
// Tool: figma_accessibility_scan
{
  "file_key": "abc123xyz",
  "node_id": "frame-id"
}
// Returns: 14 WCAG checks (contrast, touch targets, etc.)
```

**Component accessibility scorecard:**
```typescript
// Tool: figma_accessibility_component_scorecard
{
  "file_key": "abc123xyz"
}
// Returns: Per-component breakdown of accessibility issues
```

### 6. Version History & Diffing

**List file versions:**
```typescript
// Tool: figma_get_versions
{
  "file_key": "abc123xyz"
}
```

**Diff two versions:**
```typescript
// Tool: figma_diff_versions
{
  "file_key": "abc123xyz",
  "version_a": "v1.0",
  "version_b": "v2.0"
}
// Returns: Added/removed/changed nodes
```

**Binary-search blame (find when property was introduced):**
```typescript
// Tool: figma_blame
{
  "file_key": "abc123xyz",
  "node_path": "Frame → Button",
  "property": "cornerRadius"
}
// Returns: Version where property first appeared
```

## Common Patterns

### Extract Design System to CSS Variables

```typescript
// 1. Export all tokens
const tokens = await figma_export_tokens({
  file_key: "abc123xyz",
  output_format: "css-custom-properties"
});

// 2. Write to CSS file
// tokens.css_output contains:
// :root {
//   --color-primary-500: #0066FF;
//   --spacing-md: 16px;
// }
```

### Create Button Component from Scratch

```typescript
// 1. Create frame
const frame = await figma_create_frame({
  name: "Button/Primary",
  width: 120,
  height: 44,
  background_color: "#0066FF"
});

// 2. Add text
await figma_create_text({
  parent_id: frame.id,
  content: "Click me",
  font_size: 16,
  color: "#FFFFFF",
  text_align: "CENTER"
});

// 3. Add auto-layout
await figma_set_properties({
  node_id: frame.id,
  properties: {
    layoutMode: "HORIZONTAL",
    primaryAxisAlignItems: "CENTER",
    counterAxisAlignItems: "CENTER",
    paddingLeft: 24,
    paddingRight: 24
  }
});
```

### Sync Design Tokens with Code

```typescript
// Pull tokens from Figma
const figmaTokens = await figma_export_tokens({
  file_key: "abc123xyz",
  output_format: "dtcg-json"
});

// Merge with local modifications
const localTokens = JSON.parse(fs.readFileSync('tokens.json'));
const merged = { ...figmaTokens, ...localTokens };

// Push changes back
await figma_import_tokens({
  file_key: "abc123xyz",
  tokens: merged
});
```

### Monitor Design Changes in Real-Time

```typescript
// Requires Desktop Bridge plugin running

// Watch console logs
await figma_watch_console({
  duration_seconds: 300  // 5 minutes
});

// Watch selection changes
await figma_watch_selection({
  duration_seconds: 60
});

// Watch document changes
await figma_watch_document({
  duration_seconds: 120
});
```

### Create FigJam Board Elements

```typescript
// Create sticky note
await figma_create_sticky({
  file_key: "figjam-key",
  text: "User feedback",
  color: "YELLOW",
  x: 100,
  y: 100
});

// Create flowchart connector
await figma_create_connector({
  file_key: "figjam-key",
  start_node_id: "sticky-1",
  end_node_id: "sticky-2",
  connector_type: "ARROW"
});

// Create table
await figma_create_table({
  file_key: "figjam-key",
  rows: 3,
  columns: 4,
  x: 500,
  y: 200
});
```

## Configuration Best Practices

### Token Scopes Required

Your Figma personal access token needs:
- **File content** (Read) - Required for all read operations
- **File versions** (Read) - For version history tools
- **Variables** (Read/Write) - For token management
- **Comments** (Read/Write) - For collaboration tools

### Desktop Bridge Plugin Updates

**When to re-import the plugin:**
- Release notes explicitly mention plugin changes (v1.22.4, v1.10.0)
- New transport methods added (WebSocket → MessageChannel)
- Plugin shows "connection failed" despite server running

**How to re-import:**
1. Plugins → Manage plugins
2. Re-import `~/.figma-console-mcp/plugin/manifest.json`
3. Restart the plugin

The stable path never changes, so it's a one-click update.

## Troubleshooting

### "Connection failed" in Desktop Bridge

**Symptoms:** Plugin shows red "Failed to connect"

**Solutions:**
1. Verify `ENABLE_MCP_APPS=true` in your MCP config
2. Restart Figma Desktop completely
3. Check server is running: `ps aux | grep figma-console-mcp`
4. Verify plugin scans ports 9223-9232: check plugin console logs
5. Re-import plugin manifest if after major version update

### "Unauthorized" errors

**Symptoms:** All API calls return 401/403

**Solutions:**
1. Verify `FIGMA_ACCESS_TOKEN` is set correctly
2. Check token hasn't expired (tokens don't expire but can be revoked)
3. Verify token has required scopes (File content, Variables)
4. Try creating a new token with all scopes enabled

### Write operations fail (create_frame, create_variable)

**Symptoms:** Tools return "Desktop Bridge required" or "Read-only mode"

**Solutions:**
1. Install and run Desktop Bridge plugin
2. Verify `ENABLE_MCP_APPS=true` is set
3. Check plugin shows green "Connected" status
4. Switch from Remote SSE to NPX/Local Git setup (SSE is read-only)

### Token import shows "no changes detected"

**Symptoms:** `figma_import_tokens` returns "0 changes applied"

**Solutions:**
1. Verify DTCG JSON format is correct (`$type`, `$value` keys)
2. Check variable names match exactly (case-sensitive)
3. Use `figma_export_tokens` first to see canonical structure
4. Ensure collection/mode names match existing Figma structure

### Screenshots return blank images

**Symptoms:** `figma_get_image` returns white/transparent image

**Solutions:**
1. Verify node IDs are correct (use `figma_get_file` to list nodes)
2. Check node isn't hidden or has zero dimensions
3. Try different scale values (0.5, 1, 2)
4. For selection screenshots, ensure node is selected in Figma Desktop

## Tool Count by Category

- **File operations:** 12 tools (get_file, get_versions, diff_versions, etc.)
- **Node creation:** 18 tools (create_frame, create_text, create_rectangle, etc.)
- **Variable management:** 14 tools (create, update, rename, delete variables)
- **Token sync:** 2 tools (export_tokens, import_tokens)
- **Visual debugging:** 8 tools (screenshots, accessibility scans)
- **FigJam:** 11 tools (stickies, connectors, tables, code blocks)
- **Slides:** 9 tools (create decks, add slides, manage content)
- **Real-time monitoring:** 6 tools (watch console, selection, document)
- **Component operations:** 15 tools (instantiate, detach, swap)
- **Dev mode:** 8 tools (inspect, measure, export code)

**Total:** 103 tools

## Resources

- **Documentation:** https://docs.figma-console-mcp.southleft.com
- **GitHub:** https://github.com/southleft/figma-console-mcp
- **npm:** https://www.npmjs.com/package/figma-console-mcp
- **Changelog:** [CHANGELOG.md](https://github.com/southleft/figma-console-mcp/blob/main/CHANGELOG.md)
- **Figma API Docs:** https://www.figma.com/developers/api
