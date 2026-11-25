---
name: design-figma
description: >
  Create and edit designs in Figma. Create frames, shapes, text, components. Apply auto-layout,
  styles, effects. Export assets. Run plugins. Use when: "create in Figma", "add frame",
  "design component", "Figma", "add text in Figma", "auto-layout", "export from Figma",
  "run Figma plugin", "edit Figma design", "create prototype".
allowed-tools:
  - mcp__sh__platform_guide
  - mcp__sh__browser_tabs
  - mcp__sh__browser_open
  - mcp__sh__browser_navigate
  - mcp__sh__browser_js
  - mcp__sh__browser_click
  - mcp__sh__browser_dom
  - mcp__sh__browser_fill_form
  - mcp__sh__browser_wait
  - mcp__sh__browser_page_info
  - mcp__sh__screenshot_file
  - mcp__sh__key
  - mcp__sh__click_with_fallback
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_query_patterns
---

# Figma Design Automation

You are creating or editing designs in Figma using ScreenHand's browser automation. Figma runs in the browser and uses WebGL for the canvas — this affects how you interact with it.

## Intelligence Wrapper

Every tool call returns automatic hints. Watch for:
- **`[HINT]`** — Figma-specific selectors from the reference file, known working patterns
- **`[WARNING]`** — this tool has failed before in Figma, includes the fix
- **`[STRATEGY]`** — suggested next step based on past successful Figma workflows

The server auto-loads the `figma` reference when it detects navigation to `figma.com`.

## Setup

1. **Load platform knowledge**: `platform_guide(platform="figma")` — get selectors for panels, toolbar, menus.
2. **Recall**: `memory_recall(task="figma {task_description}")`.
3. **Verified patterns**: `memory_query_patterns(scope="figma")` — check verified selectors.
4. **Navigate**: `browser_navigate(url="https://www.figma.com/file/{fileId}")` — use the file URL from the user.
5. **Wait for load**: `browser_wait(condition="document.querySelector('[data-testid=\"canvas\"]') !== null")`.

## Two Interaction Modes

### Mode 1: Figma Plugin API (PRIMARY — for creating/modifying elements)

Use `browser_js` to call the Figma Plugin API. This is **far more reliable** than canvas clicks for programmatic operations.

**Create a frame:**
```javascript
const frame = figma.createFrame();
frame.name = "Header";
frame.resize(1440, 80);
frame.x = 0; frame.y = 0;
frame.fills = [{type: 'SOLID', color: {r: 1, g: 1, b: 1}}];
figma.currentPage.appendChild(frame);
```

**Create text:**
```javascript
const text = figma.createText();
await figma.loadFontAsync({family: "Inter", style: "Regular"});
text.characters = "Hello World";
text.fontSize = 24;
text.fills = [{type: 'SOLID', color: {r: 0, g: 0, b: 0}}];
```

**Create rectangle:**
```javascript
const rect = figma.createRectangle();
rect.resize(200, 50);
rect.cornerRadius = 8;
rect.fills = [{type: 'SOLID', color: {r: 0.2, g: 0.4, b: 1}}];
```

**Auto-layout:**
```javascript
frame.layoutMode = "HORIZONTAL"; // or "VERTICAL"
frame.primaryAxisSizingMode = "AUTO";
frame.counterAxisSizingMode = "AUTO";
frame.itemSpacing = 16;
frame.paddingLeft = frame.paddingRight = 24;
frame.paddingTop = frame.paddingBottom = 16;
```

**Note**: Plugin API access requires the Figma Plugin Console or running a plugin. If `figma` is not available in `browser_js`, fall back to Mode 2.

### Mode 2: UI Automation (for panel/toolbar interactions)

For UI chrome (panels, menus, buttons outside the canvas), use standard browser tools:

**Toolbar tools**: Use keyboard shortcuts (more reliable than clicking toolbar icons):
- `R` — Rectangle
- `T` — Text
- `F` — Frame
- `L` — Line
- `O` — Ellipse
- `P` — Pen
- `V` — Move tool

**Left panel (layers)**: `browser_dom(selector="[data-testid='objects-panel'] [role='treeitem']")` to list layers.

**Right panel (properties)**: `browser_dom(selector="[class*='properties']")` for design properties.

**Canvas interactions**: The canvas is WebGL — CSS selectors don't work on canvas elements. Use:
1. `browser_click(x, y)` with coordinates from the properties panel or Layer panel
2. Or use Plugin API (Mode 1) to select/modify elements programmatically

## Common Workflows

### Create a Component
1. Create elements via Plugin API or shortcuts
2. Select all: `key("cmd+a")` or click each
3. Create component: `key("cmd+opt+k")`
4. Name it in the layers panel

### Apply Styles
Via Plugin API:
```javascript
node.fills = [{type: 'SOLID', color: {r: 0.13, g: 0.13, b: 0.13}}];
node.effects = [{type: 'DROP_SHADOW', color: {r:0,g:0,b:0,a:0.15}, offset:{x:0,y:4}, radius:8, visible:true}];
node.strokes = [{type: 'SOLID', color: {r:0.8,g:0.8,b:0.8}}];
node.strokeWeight = 1;
```

### Export Assets
1. Select the element (Plugin API: `figma.currentPage.selection = [node]`)
2. Open export panel: `browser_click` on export section in right panel
3. Set format: PNG, SVG, PDF via dropdown
4. Set scale: 1x, 2x, 3x
5. Click "Export" button

### Run a Plugin
1. `key("cmd+/")` — open quick actions
2. Type the plugin name
3. Select from results
4. Plugin UI appears as a modal — interact via `browser_dom` and `browser_click`

## Figma Keyboard Shortcuts Reference

| Action | Shortcut |
|--------|----------|
| Select all | `cmd+a` |
| Group | `cmd+g` |
| Ungroup | `cmd+shift+g` |
| Component | `cmd+opt+k` |
| Duplicate | `cmd+d` |
| Copy/Paste | `cmd+c` / `cmd+v` |
| Undo/Redo | `cmd+z` / `cmd+shift+z` |
| Zoom to fit | `shift+1` |
| Zoom to selection | `shift+2` |
| Frame | `F` |
| Rectangle | `R` |
| Text | `T` |
| Auto-layout | `shift+a` |
| Quick actions | `cmd+/` |

## Verification

After each operation, take `screenshot_file` to visually confirm the design change.

## Save

- Figma auto-saves. No explicit save needed.
- `memory_save(task="figma: {description}")` to persist the workflow.

$ARGUMENTS
