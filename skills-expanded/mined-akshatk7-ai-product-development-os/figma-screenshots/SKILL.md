---
name: figma-screenshots
description: Export screenshots from a Figma file into a project's screenshots/ folder. Use when the user asks to "take screenshots", "export Figma screens", "screenshot the designs", or wants design PNGs saved locally. Also handles creating figma-summary.md if one doesn't exist. Requires a Figma URL.
allowed-tools: mcp__figma__get_figma_data, mcp__figma__download_figma_images, Read, Write, Edit, Glob, Grep, Bash(mv:*), Bash(mkdir:*), Bash(ls:*), Bash(rm:*)
---

Export Figma design screens as PNG screenshots into a project folder.

This skill is mechanical — no complex reasoning needed. Cheaper models work fine.

**Before starting:** Read `gotchas.md` and `runs.log` in this skill folder.

## When to Use

- User asks to screenshot or export Figma designs for a project
- User wants to update screenshots after a design revision
- User needs design PNGs for reference during implementation

## Cost Optimization

The Figma MCP tools have very different cost profiles:

| Tool | Cost Impact | Why |
|------|-------------|-----|
| `get_figma_data` | **HIGH** — returns massive YAML with every style, layout, fill, stroke | Each call can return 10K+ lines of structured data |
| `download_figma_images` | **LOW** — just triggers Figma's render API and saves PNGs | Minimal token usage |

**The #1 cost driver is `get_figma_data` exploration calls.** Avoid them when possible — the `figma-summary.md` reference table makes future runs nearly free.

## Workflow

### Path A: figma-summary.md exists with node IDs → go straight to download (cheapest)

If the project already has a `figma-summary.md` with a "Figma Node ID Reference" table, skip to **Step 3**.

### Path B: No figma-summary.md → create it with node IDs, then download

Do Steps 1–2 to explore the Figma file and create the summary. **Capture node IDs during exploration** so the summary is immediately reusable.

## Instructions

### Step 1: Gather inputs

1. Check if the project has a `figma-summary.md` — if it has a node ID reference table, skip to Step 3.
2. Get the Figma URL from the user or from the project's `designs.md` / `CONTEXT.md`.
3. Extract the **file key** from the URL: `figma.com/design/<fileKey>/...`.
4. Extract any **node IDs** from URL params: `node-id=<nodeId>`.

### Step 2: Explore Figma and create figma-summary.md

This is the expensive step — do it once and capture everything needed.

1. Call `get_figma_data` with the top-level node and `depth: 2` to get the section structure.
2. If the response is too large, reduce to `depth: 1` and fetch each section separately.
3. From the response, identify:
   - **Sections** (SECTION type nodes) — top-level groupings
   - **Screen frames** (FRAME type, 1440px = desktop, 375px = mobile typical)
   - **Labels** (TEXT type with descriptive names)
4. Map labels to nearby frames to understand what each frame shows.
5. Write `figma-summary.md` with:
   - File key, canvas node ID, and source URL at the top
   - Narrative description of each section's design changes
   - **A "Figma Node ID Reference" section** with a table mapping every screen to its node ID and intended filename

The node ID reference table format:

```markdown
## Figma Node ID Reference

### Section A — Onboarding flow (node: `111:28828`)

| Screen | Node ID | File Name |
|--------|---------|-----------|
| A.1 Welcome state | `378:39243` | `A1-welcome.png` |
| A.2 Sign-up form | `111:31937` | `A2-signup.png` |
```

This table is the key deliverable — it makes all future screenshot exports near-free.

### Step 3: Download screenshots

1. Create the `screenshots/` directory inside the project folder if it doesn't exist.
2. Read the node ID reference table from `figma-summary.md`.
3. Call `download_figma_images` in batches of **4 nodes per call** (larger batches return 400 errors).
4. Use `pngScale: 2` for good quality without excessive file size.
5. Use the file names from the reference table.

### Step 4: Post-processing

1. The Figma tool saves files **without `.png` extension** — rename them:
   ```bash
   cd <project>/screenshots
   for f in *; do
     [ -f "$f" ] && [ "${f%.png}" = "$f" ] && mv "$f" "${f}.png"
   done
   ```
2. Clean up any `.json` data files created by `get_figma_data`:
   ```bash
   rm screenshots/figma-*.json 2>/dev/null
   ```
3. Verify the final file list with `ls screenshots/*.png | sort`.

## Naming Convention

Files follow the pattern `{Section}{Number}-{description}.png`:

- Section prefix matches your Figma file's section labels (e.g., `A1-`, `B2-`, `C3-`)
- Add `-mobile-` in the description for mobile (375px) screens
- Use kebab-case for descriptions
- Examples: `B2-confirmation-modal.png`, `A6-mobile-empty-state.png`

## Node Identification Cheat Sheet

When exploring Figma data, use this to distinguish actual screens from annotations:

| Node pattern | What it is | Screenshot? |
|---|---|---|
| FRAME, 1440px wide | Desktop screen | Yes |
| FRAME, 375px wide | Mobile screen | Yes |
| FRAME named `---` or `--` | Screen (generic Figma naming) | Yes |
| SECTION type | Group of related screens | No (screenshot children instead) |
| TEXT type with descriptive name | Label/annotation | No (use to identify nearby frames) |
| INSTANCE of `_Annotate / Note` | Designer annotation | No |
| INSTANCE of `Action` | Arrow/connector | No |
| IMAGE-SVG named `Line *` or `Vector *` | Connector line | No |
| INSTANCE of `Section Title` | Section header | No |
| COMPONENT_SET | Component definition | No |

## Troubleshooting

- **`get_figma_data` returns "Cannot create a string longer than..."**: Node tree too large. Add `depth: 1` or `depth: 2`, or target a more specific node ID.
- **`download_figma_images` returns 400 Bad Request**: Too many nodes in one batch. Reduce to 4 nodes per call.
- **Files saved without extension**: Expected behavior from the Figma MCP tool. Rename with `.png` in post-processing.
- **Frames all named `---` or `--`**: Common pattern. Use nearby TEXT nodes and frame dimensions to identify which is which.

## Post-Run

Append to `runs.log`. If new failure patterns discovered, add to `gotchas.md`.
