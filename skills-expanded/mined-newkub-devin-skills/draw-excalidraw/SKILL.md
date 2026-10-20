---
name: draw-excalidraw
description: Create .excalidraw files from shape descriptions
argument-hint: "[description]"
related:
  - draw-svg-image
  - draw-tldraw

---

## Goal

Create a `.excalidraw` file from a diagram or drawing description

## Scope

- Generate JSON per the Excalidraw schema
- Supports shapes: rectangle, diamond, ellipse, arrow, line, text, freedraw
- Creates files openable in Excalidraw or the VS Code extension

## Execute

### 1. Parse Description

> Goal: Understand the diagram

1. Take the description from the user
2. Identify the elements to create: shapes, text, arrows, positions
3. Set the canvas size and background color
4. If complex → create a simple layout first

### 2. Generate Schema

> Goal: Build the JSON per Excalidraw

1. Use the schema:
   ```json
   {
     "type": "excalidraw",
     "version": 2,
     "source": "https://excalidraw.com",
     "elements": [],
     "appState": { "viewBackgroundColor": "#ffffff" },
     "files": {}
   }
   ```
2. Create element objects for each shape:
   - `rectangle`: `type: "rectangle"`
   - `diamond`: `type: "diamond"`
   - `ellipse`: `type: "ellipse"`
   - `arrow`: `type: "arrow"`
   - `line`: `type: "line"`
   - `text`: `type: "text"`
   - `freedraw`: `type: "freedraw"`
3. Set properties: `id`, `x`, `y`, `width`, `height`, `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `roughness`

### 3. Save File

> Goal: Save the file

1. Save as `<name>.excalidraw`
2. Validate the JSON
3. Report the path

## Rules

### 1. Schema

- Must have `type`, `version`, `source`, `elements`, `appState`
- Use `version: 2`
- `id` values must be unique

### 2. Layout

- Space elements far enough apart to read
- Use a simple grid or coordinates
- Text should sit near the related shape

### 3. Simple First

- Create a simple diagram first; refine if the user wants more
- No need to generate every style option

- Use /draw-svg-image if needed
- Use /draw-tldraw if needed

## Expected Outcome

- A `.excalidraw` file openable in Excalidraw
- Contains the elements from the description
- JSON valid and schema-correct
