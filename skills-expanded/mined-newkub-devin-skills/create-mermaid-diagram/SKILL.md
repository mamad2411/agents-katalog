---
name: create-mermaid-diagram
description: Generate Mermaid source code from a description; save as .md or .mmd
argument-hint: "[prompt or topic]"
related:
  - draw-excalidraw
  - draw-tldraw
  - follow-tool-archify
  - report
  - report-flow
  - report-architecture-diagram
  - use-scripts
  - ship
  - open-files-in-web
  - report-workspace-graph

---
## Goal

Generate Mermaid source code from a prompt, a description, or a provided file, and save it as a `.md` or `.mmd` file that can be rendered with Mermaid Live Editor, the VS Code Mermaid extension, or markdown preview

## Scope

Use it to create common diagrams such as flowchart, sequence, class, state, er, gantt, gitgraph, pie, user-journey, quadrant, and mindmap for any project
Supports both a direct prompt and reading from files/images. To visualize from code, use `/report-architecture-diagram` or `/report-workspace-graph` instead

- Diagram must be interactive/shareable as a standalone HTML artifact → `/follow-tool-archify` (typed IR, validated, path-tracing viewer); Mermaid stays the default for inline docs

## Execute

### 1. Parse Request

> Goal: Understand what to draw

1. Take `prompt` or `topic` from the argument or context
2. If the user provides an image file or a text file → read its content
3. Determine the diagram type: `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, `gantt`, `gitGraph`, `pie`, `journey`, `quadrantChart`, `mindmap`
4. If unclear → use `/ask-me` to pick a type, or default to `flowchart`
5. Determine the output name: `<topic>-diagram.md` or `<topic>.mmd` if not specified

### 2. Generate Mermaid Source

> Goal: Generate correct code

1. Write the mermaid source according to the chosen type
2. Name node ids in `kebab-case` or `camelCase` with no special characters
3. Use quotes for labels that contain `/`, `<`, `>`, `&`, spaces, or Thai text, e.g. `"feature/<n>"`, `"release/deploy"`
4. Avoid nesting `()` `[]` `()` inside a label unless necessary
5. For flowcharts, use `direction` such as `direction TB`, `direction LR` to control the layout
6. Add `subgraph` when you need clear grouping

### 3. Save Source File

> Goal: Save the diagram file as code

1. Save as `.md` by wrapping the code with ` ```mermaid ` so it renders in markdown preview right away
2. Or save as `.mmd` if you want pure mermaid source
3. Add a heading/comment summarizing what the diagram shows
4. Check that the file is not over 250 lines; if it is, split it into multiple files

### 4. Validate Syntax (Optional)

> Goal: Confirm the Mermaid is valid without forcing an image render

1. Check the code structure by eye, or use `mmdc --version` if you want to verify
2. If `mmdc` is available, you may run `mmdc -i <input.md> -o <output.svg>`, but never force it as the primary output
3. Check for syntax errors such as duplicate node ids, malformed edges, or unmatched quotes
4. If validation fails → read the error, fix the source, and validate again (max 3 rounds)

### 5. Render Image Only On Request

> Goal: Render to an image only when the user asks

1. If the user does not ask for an image → skip this step
2. If the user asks for an image → check `mmdc`, then render to `.svg` or `.png` as requested
3. If `mmdc` is not available → suggest the user open the source in [Mermaid Live Editor](https://mermaid.live) or the VS Code Mermaid extension
4. If rendering fails after 3 rounds → report the status and stop

### 6. Report

> Goal: Summarize the results

1. Run `/report` to show the output file, diagram type, and render status
2. Suggest the next action, or how to fix things if syntax validation fails

## Rules

### 1. Output Format

- The default output must be source code only: `.md` or `.mmd`
- `.md` files must wrap the code with ` ```mermaid ` so it renders in markdown preview directly
- Rendering an image (`svg/png`) is an optional output; create it only when the user asks

### 2. Mermaid Safety

- Never hardcode secrets, personal paths, or API keys into the diagram
- Use quotes for labels that contain special characters
- Never use `%%{init}%%` directives that are too complex
- Avoid labels that are longer than necessary

### 3. Reusability

- Use `/use-scripts` when you need to create many diagram files or do complex processing
- If the prompt is redundant, run `/enhance-prompt` first
- Store diagrams in `.devin/diagrams/` when they are project-level docs

### 4. Fallback

- If `mmdc` is not available → hand the mermaid source to the user without doing anything extra
- If validation fails after 3 rounds → report the status and stop

- Use /draw-excalidraw if needed
- Use /draw-tldraw if needed
- Use /follow-tool-archify if needed
- Use /report-flow if needed
- Use /ship if needed
- Use /open-files-in-web if needed

## Expected Outcome

- A `.md` or `.mmd` file containing correct Mermaid source
- Source that renders immediately in Mermaid Live Editor / VS Code / markdown preview
- (optional) an `.svg` or `.png` file if the user asks to render an image
- Report the output file, diagram type, and validation status
- No TODO/MOCK/placeholder
