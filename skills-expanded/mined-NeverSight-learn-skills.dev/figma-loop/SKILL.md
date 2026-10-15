---
name: figma-loop
description: Teaches agents to iteratively build websites from Figma designs using an autonomous baton-passing loop pattern. Uses Figma MCP to extract design data and assets, and Playwriter MCP for visual verification. Use this skill whenever the user wants to convert Figma designs to code, build from a Figma file, iterate over Figma components, or implement a Figma-to-code pipeline — even if they don't explicitly say "figma-loop".
allowed-tools:
  - "figma-mcp*:*"
  - "playwriter*:*"
  - "Read"
  - "Write"
  - "Edit"
  - "Bash"
  - "Glob"
  - "Grep"
---

# Figma Build Loop

You are an **autonomous frontend builder** participating in an iterative component-building loop. Your goal is to extract a component from a Figma file, convert it to frontend code, download assets, verify visually with Playwriter, and prepare instructions for the next component.

## Overview

The Build Loop pattern enables continuous, autonomous design-to-code development through a "baton" system. Each iteration:
1. Reads the current task from a baton file (`.figma/next-prompt.md`)
2. Extracts design data from Figma using the Figma MCP
3. Downloads assets (SVGs, PNGs, GIFs) from Figma nodes
4. Converts the design to frontend code (HTML/CSS or framework-specific)
5. Verifies the rendered output visually using Playwriter
6. Writes the next task to the baton file for the next iteration

## Prerequisites

**Required:**
- Access to the Figma MCP Server
- Access to the Playwriter MCP Server
- A Figma file key (from a Figma URL such as `figma.com/design/<fileKey>/...` or `figma.com/file/<fileKey>/...`)
- A `.figma/PROJECT.md` file documenting the project vision and component roadmap
- A `.figma/DESIGN.md` file with extracted design tokens (from the first iteration)

**Optional:**
- A local dev server for visual verification (e.g., `npx serve site/public`)

## The Baton System

The `.figma/next-prompt.md` file acts as a relay baton between iterations:

```markdown
---
component: hero-section
nodeId: "12:345"
page: "Landing Page"
---
A bold, modern hero section with a gradient background and CTA button.

**DESIGN SYSTEM (REQUIRED):**
[Copy from .figma/DESIGN.md Section 6]

**Component Spec:**
1. Background image with gradient overlay
2. Headline text with accent color
3. Subheadline and CTA button
4. Responsive behavior for mobile
```

**Critical rules:**
- The `component` field in YAML frontmatter determines the component name
- The `nodeId` field is the Figma node ID (format: `digits:digits`) for extracting design data
- The `page` field is the human-readable page name in Figma (for context)
- The prompt content must include the design system block from `.figma/DESIGN.md`
- You MUST update this file before completing your work to continue the loop

## Execution Protocol

### Step 1: Read the Baton

Parse `.figma/next-prompt.md` to extract:
- **Component name** from the `component` frontmatter field
- **Node ID** from the `nodeId` frontmatter field (Figma format: `1234:5678`)
- **Page name** from the `page` frontmatter field
- **Prompt content** from the markdown body

### Step 2: Consult Context Files

Before extracting from Figma, read these files:

| File | Purpose |
|------|---------|
| `.figma/PROJECT.md` | Project vision, **Figma File Key**, existing components (component map), roadmap |
| `.figma/DESIGN.md` | Required visual style and design tokens for code generation |
| `.figma/metadata.json` | Figma file metadata, component statuses, asset tracking |

**Important checks:**
- Section 4 (Component Map) — Do NOT recreate components that already exist
- Section 5 (Roadmap) — Pick tasks from here if backlog exists
- Section 6 (Creative Freedom) — Ideas for new components if roadmap is empty

### Step 3: Extract Design Data from Figma

Use the Figma MCP tools to extract design data for the component:

1. **Get the file key**: Read `figma-file-key` from `.figma/PROJECT.md` frontmatter, or the Figma File Key field in Section 1
2. **Call `figma-mcp_get_figma_data`**:
   - `fileKey`: The Figma file key (from PROJECT.md)
   - `nodeId`: The node ID from the baton (e.g., `"12:345"`)
   - Do NOT use `depth` unless explicitly needed
3. **Parse the response** to extract:
   - **Layout**: Position, size, auto-layout (Flexbox/Grid), padding, spacing
   - **Typography**: Font family, size, weight, line-height, letter-spacing
   - **Colors**: Fill colors, stroke colors, gradients, opacity
   - **Spacing**: Margins, padding, gap between elements
   - **Content**: Text content, image references, icon references

> **Figma-to-CSS Mapping Reference:**
> - `layoutMode=HORIZONTAL` → CSS Flexbox (`display: flex; flex-direction: row`)
> - `layoutMode=VERTICAL` → CSS Flexbox (`display: flex; flex-direction: column`)
> - `layoutMode=GRID` → CSS Grid (`display: grid`)
> - `primaryAxisAlignItems=MIN` → `justify-content: flex-start`
> - `primaryAxisAlignItems=CENTER` → `justify-content: center`
> - `counterAxisAlignItems=MIN` → `align-items: flex-start`
> - `counterAxisAlignItems=CENTER` → `align-items: center`
> - `paddingLeft`, `paddingRight`, `paddingTop`, `paddingBottom` → `padding` shorthand
> - `itemSpacing` → `gap`

### Step 4: Download Assets

Identify all image/icon nodes in the component and download them:

1. **Scan the Figma data** for nodes with:
   - `imageRef` (for static images)
   - `gifRef` (for animated GIFs)
   - Vector nodes (for SVG export)
2. **Call `figma-mcp_download_figma_images`**:
   - `fileKey`: The Figma file key
   - `nodes`: Array of `{nodeId, fileName, imageRef?, gifRef?, needsCropping?, cropTransform?, requiresImageDimensions?}`
   - `localPath`: `.figma/assets/{component}/` (relative to project root)
   - `pngScale`: `2` (for PNGs, default is 2x resolution)
3. **Asset strategy**:
   - **SVG**: For vector graphics, icons, and logos
   - **PNG@2x**: For raster images, photos, and complex graphics
   - **GIF**: For animated content (use `gifRef` instead of `imageRef`)

**Example asset download call:**
```
figma-mcp_download_figma_images
  fileKey: "abc123def456"
  nodes:
    - nodeId: "12:345"
      fileName: "hero-bg.png"
      imageRef: "abc123..."
    - nodeId: "12:346"
      fileName: "logo.svg"
  localPath: ".figma/assets/hero-section"
  pngScale: 2
```

### Step 5: Convert Design to Code

Generate the component file based on the extracted Figma data:

1. **Create the component file** (e.g., `site/public/components/{component}.html` or framework equivalent)
2. **Map Figma properties to CSS**:
   - Use the Figma-to-CSS mapping from Step 3
   - Apply design tokens from `.figma/DESIGN.md`
   - Copy production assets from `.figma/assets/{component}/` to `site/public/assets/{component}/` when building static HTML, then reference them with relative public paths
3. **Wire into the site**:
   - Import the component into the appropriate page
   - Ensure consistent styling with existing components
   - Update navigation or parent components if needed

**Framework-agnostic approach:**
- Generate plain HTML/CSS by default
- If a specific framework is used (React, Vue, etc.), generate framework-specific code
- Keep component structure flat when possible (avoid deep nesting)

### Step 6: Visual Verification with Playwriter

Verify the rendered component matches the Figma design:

1. **Start a dev server** (if not already running):
   ```bash
   npx serve site/public
   ```
2. **Call `playwriter_execute`** to:
   - Navigate to the page containing the component
   - Take a screenshot of the rendered output
   - Capture the DOM snapshot for inspection
3. **Compare** the rendered output against the Figma design:
   - Check layout alignment, spacing, and proportions
   - Verify colors, typography, and asset placement
   - Note any visual drift or discrepancies
4. **Fix issues** if visual drift is detected, then re-verify

**Example Playwriter verification:**
```javascript
// Navigate to the page
await state.page.goto('http://localhost:3000/landing-page.html', { waitUntil: 'domcontentloaded' });

// Take a screenshot
await state.page.screenshot({ path: '/absolute/path/to/screenshot.png', scale: 'css' });

// Capture DOM snapshot
const snap = await snapshot({ page: state.page });
```

### Step 7: Update Project Documentation

Modify `.figma/PROJECT.md`:
- Add the new component to Section 4 (Component Map) with `[x]`
- Remove any idea you consumed from Section 6 (Creative Freedom)
- Update Section 5 (Roadmap) if you completed a backlog item

Update `.figma/metadata.json`:
- Mark the component as `status: "completed"`
- Record `outputFile` path
- Record `assets` array with downloaded asset paths

### Step 8: Prepare the Next Baton (Critical)

**You MUST update `.figma/next-prompt.md` before completing.** This keeps the loop alive.

1. **Decide the next component**:
   - Check `.figma/PROJECT.md` Section 5 (Roadmap) for pending items
   - If empty, pick from Section 6 (Creative Freedom)
   - Or invent something new that fits the project vision
2. **Get the next nodeId**:
   - Look up the component's nodeId in `.figma/metadata.json`
   - Or call `figma-mcp_get_figma_data` without `nodeId` to discover new components
3. **Write the baton** with proper YAML frontmatter:

```markdown
---
component: nav-bar
nodeId: "67:890"
page: "Landing Page"
---
A clean, minimal navigation bar with logo and menu items.

**DESIGN SYSTEM (REQUIRED):**
[Copy the entire design system block from .figma/DESIGN.md]

**Component Spec:**
1. Logo on the left
2. Navigation links centered
3. CTA button on the right
4. Responsive hamburger menu for mobile
```

## File Structure Reference

```
project/
├── .figma/
│   ├── metadata.json      # Figma file metadata & component tracking (persist this!)
│   ├── DESIGN.md          # Visual design system (from first iteration)
│   ├── PROJECT.md         # Project vision, component map, roadmap
│   ├── next-prompt.md     # The baton — current task
│   ├── assets/            # Downloaded assets from Figma
│   │   └── {component}/
│   │       ├── image.png
│   │       └── icon.svg
│   └── screenshots/       # Playwriter screenshots for verification
│       └── {component}.png
└── site/public/           # Production site
    ├── index.html
    ├── components/
    │   └── {component}.html
    └── ...
```

### `.figma/metadata.json` Schema

This file persists all Figma identifiers and component statuses so future iterations can reference them.

```json
{
  "fileKey": "abc123def456",
  "fileUrl": "https://www.figma.com/design/abc123def456/My-Design",
  "projectName": "My App",
  "lastSync": "2026-03-04T23:11:25.514932Z",
  "pages": {
    "Landing Page": {
      "components": {
        "hero-section": {
          "nodeId": "12:345",
          "type": "FRAME",
          "name": "Hero Section",
          "dimensions": { "width": 1440, "height": 600 },
          "status": "completed",
          "outputFile": "site/public/components/hero-section.html",
          "assets": [
            "site/public/assets/hero-section/hero-bg.png",
            "site/public/assets/hero-section/logo.svg"
          ]
        },
        "nav-bar": {
          "nodeId": "67:890",
          "type": "COMPONENT",
          "name": "Nav Bar",
          "dimensions": { "width": 1440, "height": 64 },
          "status": "pending",
          "outputFile": null,
          "assets": []
        }
      }
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `fileKey` | Figma file key (from the Figma URL) |
| `fileUrl` | Full Figma file URL |
| `projectName` | Human-readable project name |
| `lastSync` | ISO timestamp of last Figma data sync |
| `pages` | Map of page name → page object |
| `pages.{page}.components` | Map of component name → component object |
| `component.nodeId` | Figma node ID (format: `digits:digits`) |
| `component.type` | Figma node type (`FRAME`, `COMPONENT`, `INSTANCE`, etc.) |
| `component.name` | Human-readable component name from Figma |
| `component.dimensions` | Width and height in pixels |
| `component.status` | `pending`, `in-progress`, `completed`, or `failed` |
| `component.outputFile` | Path to the generated code file |
| `component.assets` | Array of paths to downloaded assets |

## Discovering Components in a Figma File

Before the first iteration, discover all components in the Figma file:

1. **Call `figma-mcp_get_figma_data`** without `nodeId`:
   - `fileKey`: The Figma file key
   - No `nodeId` — this returns the full file structure
2. **Parse the response** to find:
   - Top-level pages
   - Frames within each page (potential components)
   - Components and component sets
   - Node IDs for each frame/component
3. **Record in `metadata.json`**:
   - Map each component to its `nodeId`
   - Set initial status to `pending`
   - Note dimensions for reference
4. **Build the Component Map** in `.figma/PROJECT.md` Section 4

**Example discovery workflow:**
```
figma-mcp_get_figma_data
  fileKey: "abc123def456"
```

Response includes:
- `document` → `children` (pages)
- Each page → `children` (frames/components)
- Each frame → `id` (nodeId), `name`, `type`, `absoluteBoundingBox` (dimensions)

## Design System Extraction

The first iteration should extract the design system from Figma and save it to `.figma/DESIGN.md`:

1. **Call `figma-mcp_get_figma_data`** without `nodeId` to get the full file
2. **Extract design tokens**:
   - **Colors**: Document all fills, strokes, and gradients used
   - **Typography**: Font families, sizes, weights, line-heights
   - **Spacing**: Common padding, margin, and gap values
   - **Effects**: Shadows, blurs, and layer effects
   - **Components**: Reusable UI elements (buttons, cards, inputs)
3. **Save to `.figma/DESIGN.md`** in the format specified in the project template

## Orchestration Options

The loop can be driven by different orchestration layers:

| Method | How it works |
|--------|--------------|
| **CI/CD** | GitHub Actions triggers on `.figma/next-prompt.md` changes |
| **Human-in-loop** | Developer reviews each iteration before continuing |
| **Agent chains** | One agent dispatches to another (e.g., Jules API) |
| **Manual** | Developer runs the agent repeatedly with the same repo |

The skill is orchestration-agnostic — focus on the pattern, not the trigger mechanism.

## Common Pitfalls

- ❌ Forgetting to update `.figma/next-prompt.md` (breaks the loop)
- ❌ Recreating a component that already exists in the component map
- ❌ Not including the design system block from `.figma/DESIGN.md` in the prompt
- ❌ Using wrong `nodeId` format (must be `digits:digits`, e.g., `12:345`)
- ❌ Forgetting to download assets before generating code
- ❌ Missing `imageRef` or `gifRef` when calling `download_figma_images`
- ❌ Using absolute paths for assets instead of relative paths
- ❌ Not verifying the rendered output visually with Playwriter
- ❌ Forgetting to persist `.figma/metadata.json` after each iteration
- ❌ Not updating the component status in `metadata.json` after completion

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Figma data extraction fails | Check that `fileKey` is correct and the Figma file is accessible |
| Wrong component extracted | Verify `nodeId` matches the intended component in Figma |
| Asset download fails | Ensure `imageRef` or `gifRef` is provided for each node |
| Visual drift in rendered output | Compare Playwriter screenshot with Figma reference; check CSS mapping |
| Loop stalls | Verify `.figma/next-prompt.md` was updated with valid frontmatter |
| Navigation broken | Check all internal links use correct relative paths |
| Inconsistent styles | Ensure `.figma/DESIGN.md` is up-to-date and copied correctly |
| Component not found in metadata | Run discovery step to populate `metadata.json` with nodeIds |
