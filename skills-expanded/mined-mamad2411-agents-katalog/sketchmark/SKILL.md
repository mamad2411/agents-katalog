---
name: sketchmark
description: Create, edit, review, and explain Sketchmark diagrams written in the Sketchmark DSL. Use when an agent needs to turn ideas into plain-text diagrams, fix Sketchmark syntax, add or adjust nodes, edges, groups, tables, charts, markdown blocks, animation steps, or choose and use official Sketchmark plugins such as notation, geometry, anchors, annotations, wireframe, circuit, chem-molecule, and graph.
---

# Sketchmark

Author valid, copy-pasteable Sketchmark DSL that matches the current public API and examples.

## Workflow

1. Identify whether the task is core Sketchmark DSL or plugin-specific Sketchmark DSL.
2. Write DSL with every line starting at column 0. Do not indent diagram lines.
3. Start diagrams with `diagram` and end them with `end`.
4. Keep IDs unique and reuse exact IDs in edges, groups, and animation targets.
5. Prefer core primitives first. Use an official plugin only when it clearly makes the diagram easier to author or easier to read.
6. If the task includes animation, prefer `SketchmarkEmbed` and remember that any `step draw` target starts hidden until its draw step runs.
7. If the task includes framework examples, make them minimal and valid for the target framework.
8. If the user needs to see the result, provide a minimal `SketchmarkEmbed` path, not just raw DSL.
9. Before saying a visual element is unsupported, check the core shapes and rich block types in `references/dsl-authoring.md`, then check `references/plugins.md`.

## Authoring Rules

- Always call `.trim()` on multiline JS or TS template literals that contain Sketchmark DSL.
- Keep example DSL left-aligned inside template literals. Leading whitespace breaks parsing.
- Use quoted strings for labels with spaces and for table row cell values.
- Use `x` and `y` only when the root diagram or parent group uses `layout=absolute`.
- Treat group `items=[...]` order as visual order.
- Use `label-dx` and `label-dy` explicitly for overlapping-label issues before changing the overall layout.
- For `step bracket`, provide two targets. For `step narrate`, provide a quoted string.
- Remember that core Sketchmark supports more than `box`, including `circle`, `diamond`, `hexagon`, `triangle`, `cylinder`, `parallelogram`, `text`, `image`, `icon`, `line`, `path`, `note`, `table`, `markdown`, and charts.
- Remember that the animation system also includes annotation-style actions such as `circle`, `underline`, `crossout`, `bracket`, `tick`, and `strikeoff`, not just `draw` and `highlight`.
- Prefer direct, readable examples over exhaustive demos unless the user explicitly wants a full showcase.

## Integration Rules

- If the user needs a viewable result, prefer `SketchmarkEmbed` as the single default rendering path.
- For animated examples, use `SketchmarkEmbed`. Do not default to manual `instance.anim` wiring unless the user explicitly asks for low-level API control.
- For React and Next.js client components, render only on the client into a real DOM node.
- For Next.js App Router examples, include `'use client'`.
- If you mention an official plugin, show the corresponding package import.
- If the user is new to Sketchmark, show one clear path to view the diagram: `SketchmarkEmbed`.

## Read On Demand

- Read [references/dsl-authoring.md](references/dsl-authoring.md) for compact syntax patterns and validation checks.
- Read [references/rendering.md](references/rendering.md) when the user needs to run or view the diagram.
- Read [references/plugins.md](references/plugins.md) when the task may be better expressed with an official plugin.
- After choosing a plugin, read the matching per-plugin reference such as `references/plugin-circuit.md` or `references/plugin-geometry.md` before claiming the plugin lacks support.

## Quality Bar

- Produce examples that can be pasted directly into docs or code with minimal cleanup.
- Keep examples consistent with the package name `sketchmark` and the official plugin package names.
- Call out any likely gotcha if the user is mixing animation, absolute layout, or framework rendering.
- Do not assume the agent has access to the repo README. Include any essential syntax or rendering detail directly in the answer when a first-time user would need it.
