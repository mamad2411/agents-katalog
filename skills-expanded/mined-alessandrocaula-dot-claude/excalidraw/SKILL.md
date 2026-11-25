---
name: excalidraw
description: Create a diagram, chart, schema, flowchart, or any visual representation as an Excalidraw file. Use when the user asks to "draw", "diagram", "visualize", "create a schema", "make a chart", or "show the workflow" of something.
---

When asked to create a diagram or visual, generate a valid `.excalidraw` file and save it alongside the relevant file or in the current directory if no file is specified.

## Steps

1. Understand what needs to be visualized — identify the elements (boxes, arrows, labels) and their relationships
2. Plan a clean layout — assign x/y coordinates so elements don't overlap; work on a grid of ~200px spacing
3. Generate the JSON using the element templates in [elements.md](elements.md)
4. Save as `<descriptive-name>.excalidraw` in an appropriate location
5. Tell the user the file path and what was generated

## Layout guidelines

- Start elements at x=100, y=100 and space them ~200px apart
- Flow left-to-right or top-to-bottom depending on what makes sense
- Arrows connect element centers — use `startBinding` and `endBinding` with the element's `id`
- Keep it simple: the user will refine the layout in Excalidraw

## Defaults

Use all Excalidraw defaults for styling. Do not set custom colors, fonts, or stroke styles — leave them at their default values as shown in the templates.
