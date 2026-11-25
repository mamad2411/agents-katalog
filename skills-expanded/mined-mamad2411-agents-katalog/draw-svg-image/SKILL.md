---
name: draw-svg-image
description: Create SVG images from a description or prompt using code
argument-hint: "[description]"
related:
  - convert
  - deep-review-codebase
  - visualize-in-web
  - open-files-in-web
  - gen-media
---
## Goal

Create a `.svg` file from the description or prompt the user provides

## Scope

- Build SVG with manual code for basic shapes
- Supports simple icons, diagrams, and easy illustrations
- If very complex, recommend `gen-ai-images` then convert to SVG with `convert-to-svg`

## Execute

### 1. Parse Description

> Goal: Understand what to build

1. Take the description or prompt from the user
2. Identify the shapes: `rectangle`, `circle`, `ellipse`, `line`, `polygon`, `path`, `text`
3. Identify colors, sizes, and positions if given
4. If unclear → ask for more

### 2. Choose Approach

> Goal: Pick the suitable SVG generation approach

1. Simple shapes → write SVG markup directly
2. The user wants heavy styling or a complex scene → use `gen-ai-images` then `/convert-svg`
3. Animation needed → use CSS animation or SMIL inside the SVG

### 3. Generate SVG

> Goal: Create a correct SVG file

1. Create the root `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 width height">`
2. Add `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<polygon>`, `<path>`, `<text>` per the description
3. Use `fill`, `stroke`, `stroke-width`, `opacity` per the style
4. Set `viewBox` for responsiveness

### 4. Save And Validate

> Goal: Save and verify

1. Save as `<name>.svg`
2. Check syntax by opening it in a browser or with `xmllint`
3. Report the file path

## Rules

### 1. Manual First

- Always try to build the SVG with code first
- Do not rely on AI generation for simple shapes

### 2. Clean SVG

- Use `viewBox` instead of fixed width/height
- Use group `<g>` for related elements
- Add `id` or `class` for styling when needed

### 3. Fallback

- If the description is complex or the user wants photorealistic output → recommend `gen-ai-images` + `convert-to-svg`
- For preview → use `/visualize-in-web` or `/open-web`

- Use /deep-review-codebase if needed
- Use /open-files-in-web if needed

- Use /gen-media if needed

## Expected Outcome

- A `.svg` file matching the description
- The SVG opens in a browser
- Reports the file path and the approach used
