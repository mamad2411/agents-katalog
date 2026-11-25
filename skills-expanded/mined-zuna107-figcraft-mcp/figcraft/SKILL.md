---
name: figcraft
description: Design, create, edit, inspect, and prototype UI screens, frames, components, and vector graphics live in FigCraft via the FigCraft-MCP server. Includes starter templates, native code export (Tailwind, Compose, SwiftUI, React, Flutter), canvas token extraction, automatic step-by-step multiplayer cursor streaming, 40+ Lucide vector icons, interactive prototype wiring, few-shot style learning, and token-optimized inspection tools.
---

# FigCraft Live MCP Skill Guide

`figcraft-mcp` connects any AI coding agent directly to the live **FigCraft Desktop** canvas (`--attach 7979`) with automatic live collaboration room detection, step-by-step multiplayer cursor streaming (`collab.cursor` + live selection highlight), official starter templates, native code generation (Tailwind, Jetpack Compose, SwiftUI, React, Flutter), canvas design token extraction, precomputed Lucide vector icons, multi-style design presets, and token-saving inspection tools (`list_screens`, `find_nodes`).

---

## 1. Optimized Workflow for Creating or Editing Screens

1. **Start from an Official Template (`create_from_template`)**:
   - If starting a new design and you don't have a rigid layout concept, instantiate an official starter template:
     - `mobile-app`: 4 trail app screens with components, auto-layout, and prototype flows (390 × 844).
     - `dashboard`: Analytics screen on a grid with vector charts and data tables (1440 × 960).
     - `landing-page`: Responsive marketing page with hero, features, figures, testimonials, and footer (1440 wide).
     - `design-system`: Color & text styles, Light & Dark mode variables, buttons, inputs, and cards.
     - `wireframe-kit`: Low-fidelity greyscale components and flow screens (390 & 1280 wide).
     - `social-posts`, `slides`, `icon-set`.
   - Generates complete, non-slop, production-grade screens in milliseconds.

2. **Inspect Canvas Fast (`list_screens`)**:
   - Call `list_screens` (`{"page": 1}`) to inspect screen names, IDs, positions, and bounds. Uses outline projection to save 90%+ tokens compared to standard `inspect_document`.

3. **Extract Existing Canvas Tokens (`extract_canvas_tokens`)**:
   - Call `extract_canvas_tokens` to pull exact color palettes, Light/Dark variables, spacing, radii, and font families from existing screens for 100% design consistency.
   - Alternatively, call `get_anti_slop_guidelines` (`"neutral_clean"`, `"ios_hig"`, `"material_m3"`, or `"dark_modern"`).

4. **Targeted Modifications (`find_nodes`)**:
   - When modifying an existing screen, call `find_nodes(parent=screen_id, query="Search Input")` to locate node IDs without dumping massive layer trees.

5. **Stream Elements Step-by-Step via `batch`**:
   - Group screen elements into a single `batch` call using `$ref` back-references.
   - `figcraft-mcp` automatically streams `batch` commands step-by-step (`~40ms` per element) with live multiplayer cursor movement, and returns a compact summary response to conserve LLM tokens.

6. **Use Vector Icons (`place_lucide_icon`)**:
   - Never use Unicode emojis. Call `place_lucide_icon` (or `icon_cmds` in Python scripts) to place crisp 24x24 Lucide vector icons (`search`, `wallet`, `home`, `barChart`, `plus`, `x`, `check`, `chevronDown`, `user`, etc.).

7. **Wire Interactive Prototype Flows (`create_prototype_link`)**:
   - Connect triggers (`sourceId`) to destination screens (`targetFrameId`) with `smartAnimate`, `dissolve`, `push`, `slideIn`, or `moveOut`.

8. **Export Frame Directly to Production Code (`inspect_code`)**:
   - Call `inspect_code(nodeId=screen_id, language="tailwind" | "compose" | "swiftui" | "react" | "flutter")` to get pixel-perfect production code generated natively by FigCraft's engine.

9. **Verify Visually & Save**:
   - Preview modified frames using `export` (`format: "png", scale: 2`) or `screenshot`, then call `save_file`.

---

## 2. High-Value MCP Tools

| Tool Name | Purpose & Token Optimization |
| :--- | :--- |
| `create_from_template` | **Anti-Slop Starter**: Instantiates official templates (`mobile-app`, `dashboard`, `landing-page`, `design-system`, etc.) with auto-layout in milliseconds. |
| `inspect_code` | **Native Code Export**: Compiles any frame directly into Tailwind CSS v4, Jetpack Compose, SwiftUI, React TSX, or Flutter without LLM translation. |
| `extract_canvas_tokens` | **Few-Shot Token Extractor**: Pulls color variables (Light/Dark), spacing, radii, and fonts directly from canvas in < 200 tokens. |
| `list_screens` | **Token Saver**: Lists top-level screen frames on the page (IDs, names, bounds) with outline projection (< 200 tokens). |
| `find_nodes` | **Token Saver**: Substring search for layers by name or text within a frame, preventing full tree dumps. |
| `batch` | Creates and styles multiple layers in 1 request. Returns compact summary to preserve token budget. |
| `place_lucide_icon` | Places a scaled 24x24 Lucide vector icon inside any frame in 1 step with live cursor movement. |
| `create_prototype_link` | Connects a clickable element (`sourceId`) to a destination screen (`targetFrameId`) with animations. |
| `get_anti_slop_guidelines` | Returns universal quality heuristics, multi-style presets (`neutral_clean`, `ios_hig`, `material_m3`, `dark_modern`), and component recipes. |
| `get_node` / `inspect_document` | Inspects node properties (supports `outline: True` for 90% token reduction). |
| `export` / `screenshot` | Renders crisp 2x PNG previews of any frame ID for visual verification. |
| `save_file` | Saves the active `.figcraft` document to disk. |

---

## 3. Python SDK (`figcraft_mcp.FigCraftLive`)

```python
from figcraft_mcp import FigCraftLive, icon_cmds

fc = FigCraftLive(step_delay=0.040)

# 1. Start from an official starter template
doc_info = fc.create_from_template("mobile-app", name="FinFlow App")

# 2. Extract canvas design tokens
screens = fc.list_screens(page_id=1)
print("Screen 1:", screens[0]["name"])

# 3. Export screen directly to Tailwind CSS or Jetpack Compose code
tailwind_code = fc.inspect_code(node_id=screens[0]["id"], language="tailwind")
compose_code = fc.inspect_code(node_id=screens[0]["id"], language="compose")

# 4. Modify and add Lucide vector icons
fc.batch([
    *icon_cmds(screens[0]["id"], "Search Icon", "search", 14, 12, 16, "#64748B", 1.8),
], label="Add Search Icon", stream=True)

fc.save()
fc.close()
```
