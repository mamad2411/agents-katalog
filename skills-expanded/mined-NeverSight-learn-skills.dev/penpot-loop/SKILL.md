---
name: penpot-loop
description: Teaches agents to iteratively build websites from Penpot designs using an autonomous baton-passing loop pattern. Uses the official @penpot/mcp server (focused-page execute_code, UUIDs, base64 assets) and Playwriter for visual verification. Use this skill whenever the user wants to convert Penpot designs to code, build from a Penpot file, iterate over Penpot components, or implement a Penpot-to-code pipeline — even if they don't explicitly say "penpot-loop".
allowed-tools:
  - "Bash"
  - "Read"
  - "Write"
  - "Edit"
  - "Glob"
  - "Grep"
---

# Penpot Build Loop

You are an **autonomous frontend builder** participating in an iterative component-building loop. Extract a component from a Penpot file, convert it to frontend code, save assets, verify visually with Playwriter, prepare the next component.

## Overview

The Build Loop uses a "baton" file (`.penpot/next-prompt.md`) to relay work between iterations. Each iteration: reads the baton, pulls design data via `penpotUtils` inside `execute_code`, exports assets with `export_shape`, generates frontend code, verifies with Playwriter, and writes the next task to the baton.

## Prerequisites

**Required:** Penpot MCP Server (`@penpot/mcp`, default `http://localhost:4401/mcp`), the Penpot MCP Plugin loaded in Penpot and connected (WebSocket on port `4402`), a Penpot file open in a focused browser tab, Playwriter MCP for verification, and `.penpot/PROJECT.md` + `.penpot/DESIGN.md` files. **Optional:** a local dev server (e.g., `npx serve site/public`).

### Quick start: bringing up the environment

```bash
npx -y @penpot/mcp@latest
```

In Penpot: open your file → **Plugins menu → Load plugin** with URL `http://localhost:4400/manifest.json` → open the plugin UI → click **"Connect to MCP server"**.

> ⚠️ **Do not close the plugin UI** while iterating — it owns the WebSocket. Chromium 142+ shows a PNA permission popup the first time; **approve it** or the connection silently fails.

## What the User Provides (First-Run UX)

The minimum surface the user must hand the agent to start the loop. Three input modes, in priority order:

| # | Mode | What user provides | When to use |
|---|------|--------------------|-------------|
| 1 | **URL with deep params** | `https://design.penpot.app/#/workspace?file-id=<UUID>&page-id=<UUID>&shape-id=<UUID>` | One specific component is the target. Fastest, most explicit. |
| 2 | **URL + scope** | URL + one-line scope (e.g. "build the navbar and hero") | Multiple components, user knows which ones. |
| 3 | **Bare description** | Text description only, with a file focused in the browser tab | User opened the file but did not copy a URL. Agent picks the first reasonable shape. |

On first run, the agent seeds `.penpot/PROJECT.md` with `penpot-file-id` (and `currentTargetShapeId` when mode 1) parsed from the URL, then jumps to Step 1b (Baton priming). After that, the baton (`/.penpot/next-prompt.md`) takes over.

**Tip:** copy the URL straight from Penpot's "Share" dialog. It already includes the four query params in the right order.

**Agent discovers autonomously.** The user does not need to provide these: page structure (`penpotUtils.shapeStructure`), shape trees, color/typography tokens (`tokenOverview`), image fills, flex layouts, fonts, or component names. The agent pulls everything else from the focused file via `execute_code`.

### First prompt (copy-paste)

```
Build the hero section from this Penpot file:
https://design.penpot.app/#/workspace?file-id=0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345&page-id=0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345&shape-id=0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345
```

Modes 2 and 3 also work. Mode 1 is safest because all four UUIDs are explicit and the agent never has to guess which shape you meant. If the URL has no `shape-id` (mode 2), the agent reads `.penpot/PROJECT.md` first to find `currentTargetShapeId`.

## MCP Tool Surface (5 tools, learn once)

| Tool | Args | Purpose |
|------|------|---------|
| `high_level_overview` | (none) | Returns the official Penpot usage guide. **Read once per session.** |
| `penpot_api_info` | `type: string`, `member?: string` | Look up API docs (caps at ~2000 chars; use `member` to drill). |
| `execute_code` | `code: string` | Run JS in the Penpot plugin context. Return value is JSON-stringified back. |
| `export_shape` | `shapeId` (UUID / `'selection'` / `'page'`), `format: 'svg'\|'png'`, `mode: 'shape'\|'fill'`, `filePath?` | Export a shape (or its image fill) as PNG bytes or SVG text. |
| `import_image` | `filePath` (absolute), `x?, y?, width?, height?` | Import a local image. **Mutates the document — see "Must NOT".** |

### Plugin context globals (inside `execute_code`)

Three objects are available in every call:

- **`penpot`** — the `Penpot` API. Use for `penpot.selection`, `penpot.root`, fonts, library, tokens.
- **`penpotUtils`** — helpers for searching, structuring, exporting, importing. **Always prefer these over hand-rolled shape walking.**
- **`storage`** — arbitrary persistent object that survives across `execute_code` calls. Use for intermediate results and your own utility functions.

> 💡 `penpot.selection` can change between calls. **Copy it into `storage` immediately** if you intend to use it later.

## Must NOT (Guardrails)

Violating any of these is a **hard failure** for an iteration. These guardrails exist because the corresponding actions either mutate the user's design, bypass the design-to-code discipline, or are the wrong tool for this skill's scope.

- ❌ **Do NOT use `penpot.generateStyle()` or `penpot.generateMarkup()`** — they generate CSS/HTML/SVG from shapes and bypass the design-to-code discipline. Write the code yourself from extracted design tokens.
- ❌ **Do NOT mutate the document** via `execute_code`. This skill is **read-only by design**. Forbidden (non-exhaustive):
  - `shape.resize(...)`, `shape.fills = ...`, `shape.strokes = ...`, `shape.name = ...`
  - `penpot.createRectangle()`, `penpot.createText()`, `penpot.createBoard()`, `penpot.createPath()`
  - `parent.appendChild(...)`, `parent.insertChild(...)` (reparenting design content)
  - `shape.remove()`
  - `penpot.library.local.createColor()`, `penpot.library.local.createTypography()`, `penpot.library.local.createComponent(...)`
  - `set.addToken(...)`
  - Any tool that creates, modifies, or deletes shapes, pages, components, colors, typographies, or tokens
- ❌ **Do NOT use the `import_image` tool** — it mutates the document. (This skill does design → code, not code → design.)
- ❌ **Do NOT use Figma's `digits:digits` ID format** anywhere. Penpot uses **UUIDs** (e.g. `0c4b6e9c-8e3a-4d4f-9b21-...`). If you see `12:345` anywhere, that's a Figma ID — wrong tool.
- ❌ **Do NOT export a token library as a separate workflow** — token export is loop-internal and lives in `.penpot/DESIGN.md`.
- ❌ **Do NOT do code-to-design flows.** This skill is **design → code only**.

## The Baton System

The `.penpot/next-prompt.md` file acts as a relay baton between iterations:

```markdown
---
component: hero-section
shapeId: "0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345"
page: "Landing Page"
---
A bold, modern hero section with a gradient background and CTA button.

**DESIGN SYSTEM (REQUIRED):**
[Copy from .penpot/DESIGN.md Section 6]

**Component Spec:**
1. Background image with gradient overlay
2. Headline text with accent color
3. Subheadline and CTA button
4. Responsive behavior for mobile
```

**Critical rules:** `component` (kebab-case) names the component; `shapeId` is the **Penpot UUID** (not Figma's `digits:digits`); `page` is the human-readable page name; the body must include the design system block from `.penpot/DESIGN.md`. **You MUST update this file before completing your work to continue the loop.** See `resources/baton-schema.md` for the full spec.

## Execution Protocol

### Step 1: Read the Baton

Parse `.penpot/next-prompt.md` to extract: **component name** (`component` field), **shapeId** (Penpot UUID), **page name** (`page` field), and **prompt body**. If `.penpot/next-prompt.md` does not exist yet, this is the **first iteration** — proceed to Step 1b.

### Step 1b: First-iteration setup (only if no `.penpot/` directory exists)

Create `.penpot/` with `PROJECT.md` (see `resources/project-template.md`) populated from the user's intent. **Do not** create components yet — that's Step 3.

### Step 2: Consult Context Files

Read these (if they exist): `.penpot/PROJECT.md` (vision, **Penpot File UUID**, component map, roadmap), `.penpot/DESIGN.md` (tokens for code generation), `.penpot/metadata.json` (statuses, asset tracking). **Check:** Section 4 (don't recreate existing components), Section 5 (pick from roadmap), Section 6 (creative freedom if roadmap is empty).

### Step 3: Discover / Locate the Component

The baton gives a `shapeId` (UUID) and a `page`. Confirm the shape exists in the focused file:

```javascript
const page = penpotUtils.getPageByName("Landing Page");
if (!page) return { error: "Page not found", pages: penpotUtils.getPages() };
const shape = penpotUtils.findShapeById("0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345");
if (!shape) return { error: "Shape not found in file" };
storage.targetShape = shape; storage.targetPage = page;
return { shapeFound: true, shapeId: shape.id, shapeName: shape.name, shapeType: shape.type,
         pageId: page.id, pageName: page.name,
         position: { x: shape.x, y: shape.y, width: shape.width, height: shape.height } };
```

If not found, **stop and ask the user** — the UUID may be stale. Do not invent a different shape. For first iteration (or empty roadmap), run `penpotUtils.shapeStructure(penpot.root, 3)` to populate `.penpot/metadata.json`. For multi-page files, iterate `penpotUtils.getPages()` and walk each `page.root`.

### Step 4: Extract Design Data

Walk the target shape's subtree with `penpotUtils` helpers:

```javascript
const target = storage.targetShape;
const structure = penpotUtils.shapeStructure(target, 5);
const designData = penpotUtils.analyzeDescendants(target, (root, shape) => ({
  id: shape.id, name: shape.name, type: shape.type,
  x: shape.parentX, y: shape.parentY, width: shape.width, height: shape.height,
  fills: shape.fills, strokes: shape.strokes, borderRadius: shape.borderRadius,
  opacity: shape.opacity, rotation: shape.rotation,
  visible: shape.visible, hidden: shape.hidden,
  constraints: { horizontal: shape.constraintsHorizontal, vertical: shape.constraintsVertical }
}), 10);
return { structure, designData };
```

**Penpot-to-CSS Mapping Reference:**
- `board.flex` → CSS Flexbox: `flex.dir: "row"|"column"` → `flex-direction`; `flex.rowGap`/`flex.columnGap` → `row-gap`/`column-gap`; `flex.alignItems` → `align-items`; `flex.justifyContent` → `justify-content`; `flex.topPadding`/`flex.rightPadding`/`flex.bottomPadding`/`flex.leftPadding` → `padding` shorthand
- `board.grid` → CSS Grid: `grid.rows`/`grid.columns` → `grid-template-rows`/`grid-template-columns`; `grid.rowGap`/`grid.columnGap` → `gap` (or `row-gap`/`column-gap`)
- `text.characters` → text content; `text.fontSize` → `font-size`; `text.fontWeight`/`text.fontFamily`/`text.lineHeight`/`text.letterSpacing` → matching CSS; `text.align` → `text-align`; `text.verticalAlign` → `vertical-align`
- `shape.fills: [{ fillColor: "#FF0000", fillOpacity: 1 }]` → `background-color: #FF0000;` (with `opacity`)
- `shape.strokes: [{ strokeColor: "#000", strokeOpacity: 1, strokeWidth: 1, strokeStyle: "solid" }]` → `border: 1px solid #000;`
- `shape.borderRadius` (uniform) → `border-radius`; `shape.rotation` (degrees) → `transform: rotate(Ndeg);`

### Step 5: Save Assets

Identify image-bearing shapes and export them. **Use `export_shape` — never `import_image`** (mutates the document).

**Pattern A — direct write to disk (when file system access is enabled):**
```text
export_shape(shapeId: "0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345", format: "png", mode: "shape", filePath: ".penpot/assets/hero-section/hero-bg.png")
```
Repeat per image shape. Use `format: "svg"` for vectors, `format: "png"` for raster.

**Pattern B — base64 inline (multi-user / remote mode, no file system access):** the tool returns base64; decode with `node .penpot/scripts/save_base64_asset.js "<base64>" .penpot/assets/hero-section/hero-bg.png`.

**Pattern C — programmatic image-fill discovery:** `penpotUtils.findShapes(s => s.fills?.some(f => f.fillImage), storage.targetShape)` returns image fills; call `export_shape` per shape's `id` with `mode: "fill"` for raw image bytes.

**Asset strategy:** **SVG** for vectors/icons/logos; **PNG** (default 1x; sharp upsamples to 2x) for raster/photos; use `mode: "fill"` when you want just the raw image, not the full shape.

### Step 6: Convert Design to Code

1. Create the component file (e.g., `site/public/components/{component}.html` or framework equivalent)
2. Map Penpot properties to CSS using Step 4's reference
3. Apply design tokens from `.penpot/DESIGN.md` — don't hardcode colors, fonts, or spacing that the design system already defines
4. Wire into the site: import the component, ensure consistent styling, update navigation/parents as needed
5. Use relative paths for downloaded assets

**Framework-agnostic approach:** plain HTML/CSS by default; framework-specific code if a framework is in use; keep component structure flat.

### Step 7: Visual Verification with Playwriter

1. Start a dev server if not running: `npx serve site/public`
2. Use `playwriter_execute` to navigate, take a screenshot, capture the DOM snapshot
3. Compare rendered output against the Penpot design — check layout, spacing, proportions, colors, typography, asset placement
4. Fix visual drift, then re-verify

```javascript
await state.page.goto('http://localhost:3000/landing-page.html', { waitUntil: 'domcontentloaded' });
await state.page.screenshot({ path: '/absolute/path/to/screenshot.png', scale: 'css' });
const snap = await snapshot({ page: state.page });
```

**Optional sanity check:** also export the same component from Penpot with `export_shape` (`mode: "shape"`) and compare to the Playwriter screenshot.

### Step 8: Update Project Documentation

Modify `.penpot/PROJECT.md`: add the new component to Section 4 (Component Map) with `[x]`, remove any idea you consumed from Section 6, update Section 5 if you completed a backlog item. Update `.penpot/metadata.json`: mark `status: "completed"`, record `outputFile`, record `assets` array.

### Step 9: Prepare the Next Baton (Critical)

**You MUST update `.penpot/next-prompt.md` before completing.** 1) Pick the next component from Section 5 (Roadmap), Section 6 (Creative Freedom), or invent one. 2) Get the next `shapeId` from `metadata.json` or by discovery: `penpotUtils.findShapes(s => s.type === 'board' || s.type === 'component', penpot.root)`. 3) Write the baton with proper YAML frontmatter (UUID in `shapeId`):

```markdown
---
component: nav-bar
shapeId: "a1b2c3d4-5678-90ab-cdef-1234567890ab"
page: "Landing Page"
---
A clean, minimal navigation bar with logo and menu items.

**DESIGN SYSTEM (REQUIRED):**
[Copy the entire design system block from .penpot/DESIGN.md]

**Component Spec:**
1. Logo on the left
2. Navigation links centered
3. CTA button on the right
4. Responsive hamburger menu for mobile
```

## File Structure & `.penpot/metadata.json` Schema

```
project/
├── .penpot/
│   ├── metadata.json      # Persist this — Penpot file metadata & component tracking
│   ├── DESIGN.md          # Visual design system (from first iteration)
│   ├── PROJECT.md         # Project vision, component map, roadmap
│   ├── next-prompt.md     # The baton — current task
│   ├── assets/{component}/  # Exported assets
│   ├── screenshots/{component}.png  # Playwriter verification
│   └── scripts/save_base64_asset.js  # base64 → file decoder
└── site/public/           # Production site
    ├── index.html, components/{component}.html, ...
```

```json
{
  "fileId": "0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345",
  "fileUrl": "https://design.penpot.app/#/workspace?file-id=0c4b6e9c-...",
  "projectName": "My App",
  "lastSync": "2026-06-01T18:55:41.740Z",
  "pages": {
    "Landing Page": {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "components": {
        "hero-section": {
          "shapeId": "0c4b6e9c-8e3a-4d4f-9b21-aa7bc12de345", "type": "board", "name": "Hero Section",
          "dimensions": { "width": 1440, "height": 600 }, "status": "completed",
          "outputFile": "site/public/components/hero-section.html",
          "assets": [".penpot/assets/hero-section/hero-bg.png", ".penpot/assets/hero-section/logo.svg"]
        },
        "nav-bar": {
          "shapeId": "a1b2c3d4-5678-90ab-cdef-1234567890ab", "type": "board", "name": "Nav Bar",
          "dimensions": { "width": 1440, "height": 64 }, "status": "pending",
          "outputFile": null, "assets": []
        }
      }
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `fileId` | Penpot file UUID |
| `fileUrl` | Full Penpot file URL |
| `projectName` | Human-readable project name |
| `lastSync` | ISO timestamp of last Penpot data sync |
| `pages.{page}.id` | Penpot page UUID |
| `component.shapeId` | Penpot shape UUID (NOT Figma's `digits:digits`) |
| `component.type` | `board`, `component`, `rectangle`, `text`, `group`, etc. |
| `component.name` | Human-readable component name from Penpot |
| `component.dimensions` | Width and height in pixels |
| `component.status` | `pending`, `in-progress`, `completed`, or `failed` |
| `component.outputFile` | Path to the generated code file |
| `component.assets` | Array of paths to downloaded assets |

## Discovering Components in a Penpot File

Before the first iteration, discover all components: 1) `penpotUtils.shapeStructure(penpot.root, 3)` to get the tree. 2) Parse for top-level boards (potential components), groups/frames within each, text/image/shape elements, and each frame's UUID `shapeId`. 3) Record in `metadata.json` — map each component to its `shapeId`, set initial `status: "pending"`, note dimensions. 4) Build the Component Map in `.penpot/PROJECT.md` Section 4.

## Design System Extraction

The first iteration should extract the design system and save it to `.penpot/DESIGN.md`: 1) `penpotUtils.shapeStructure(penpot.root, 3)` for file structure. 2) Walk the tree to collect **Colors** (all unique `fillColor`/`strokeColor` via `findShapes` predicates), **Typography** (`fontFamily`/`fontSize`/`fontWeight`), **Spacing** (common `rowGap`/`columnGap`/padding), **Effects** (`shadows`/`blurs`), **Components** (reusable UI elements). 3) Check design tokens with `penpotUtils.tokenOverview()` (returns `setName → { tokenType → [tokenName, ...] }`). 4) Save to `.penpot/DESIGN.md` in the format from the project template.

## Orchestration Options

| Method | How it works |
|--------|--------------|
| **CI/CD** | GitHub Actions triggers on `.penpot/next-prompt.md` changes |
| **Human-in-loop** | Developer reviews each iteration before continuing |
| **Agent chains** | One agent dispatches to another |
| **Manual** | Developer runs the agent repeatedly with the same repo |

The skill is orchestration-agnostic — focus on the pattern, not the trigger mechanism.

## Common Pitfalls

- ❌ Forgetting to update `.penpot/next-prompt.md` (breaks the loop)
- ❌ Recreating a component that already exists in the component map
- ❌ Not including the design system block from `.penpot/DESIGN.md` in the prompt
- ❌ Using Figma's `digits:digits` format instead of Penpot UUIDs
- ❌ Calling `penpot.generateStyle()` or `penpot.generateMarkup()` as a shortcut
- ❌ Mutating the document via `execute_code` (skill is read-only)
- ❌ Forgetting to copy `penpot.selection` into `storage` (selection can change)
- ❌ Forgetting to export assets before generating code
- ❌ Using `import_image` (this skill does design → code only)
- ❌ Not verifying the rendered output visually with Playwriter
- ❌ Forgetting to persist `.penpot/metadata.json` after each iteration
- ❌ Not updating the component status in `metadata.json` after completion

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `execute_code` fails with "Plugin not connected" | Open Penpot in browser, ensure the MCP plugin UI is open and showing "Connected to MCP server". WebSocket on port 4402 must be live. |
| `penpotUtils.findShapeById` returns null | The shape's UUID may be stale or from a different file. Re-run discovery on the current page and update the baton. |
| Multiple pages and the wrong one is focused | The MCP plugin operates on the **currently focused page**. Click into the correct page in Penpot's UI, then retry. |
| Library components in the file | `penpot.library.local.components` and `penpot.library.connected` give access. Use `findShapeById` for the main instance, then `instance()` to create new instances on the current page. **This is read-only — just inspect, do not instantiate.** |
| Unnamed shapes (`shape.name === ""` or null) | Skip them when building the component map. Only persist components you can name meaningfully. |
| Plugin not installed in Penpot | **Plugins menu → Load plugin** with `http://localhost:4400/manifest.json` (development URL while MCP server is running). |
| Chromium blocks localhost from https://design.penpot.app (PNA) | Approve the permission popup the first time the plugin tries to reach localhost. In Brave, disable Shields for the Penpot site. In Firefox, no action needed. |
| `export_shape` returns image but you need a file | Either pass `filePath` (when file system access is enabled) or use `scripts/save_base64_asset.js` to decode the base64 payload. |
| File system access disabled (multi-user/remote mode) | `import_image` and `filePath` on `export_shape` won't work. Operate on inline base64 payloads and use `save_base64_asset.js`. |
| `penpotUtils.shapeStructure` returns too much data | Lower `maxDepth` (e.g. `2` instead of `5`) or query sub-trees individually. |
| Rendered output doesn't match design | Compare Playwriter screenshot with `export_shape` PNG of the source shape. Re-check Penpot-to-CSS mapping for layout, fills, strokes, typography. |
| Loop stalls | Verify `.penpot/next-prompt.md` was updated with valid frontmatter (UUID in `shapeId`, existing `component`). |
| `penpot.generateStyle` is tempting | **Don't.** It bypasses design-to-code discipline and produces CSS you cannot easily audit against the design system. |
| Tokens exist but `tokenOverview` returns empty | Confirm the file actually uses design tokens (not just hardcoded values). Some files have both. |

## Skill Boundaries

This skill handles **design → code** only. It explicitly does NOT:

- ❌ Code → design (modifying Penpot files based on code)
- ❌ Generating new designs in Penpot via LLM
- ❌ Token library export as a separate deliverable
- ❌ Cross-file design system sync
- ❌ Asset upload to Figma / design handoff to other tools

If you find yourself needing any of these, you are out of scope — stop and confirm with the user.
