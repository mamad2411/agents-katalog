# TLDraw Canvas Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/canvas/`
> - **Canvas script**: `scripts/canvas/generate_canvas.py`
> - **Run with**: `.venv\Scripts\python.exe scripts/canvas/generate_canvas.py`
> - **Prerequisites**: Node.js 18+ installed
> - **Canvas types**: Mind map, content plan, pipeline diagram, brainstorm board
> - **First use**: Run `npm install` in `tldraw-canvas/` directory

## Purpose
Create interactive visual canvases using TLDraw React SDK.
Generates mind maps, content plans, pipeline visualizations, and brainstorming boards.

## Trigger Phrases
- "create a canvas", "visual mind map", "draw a content plan"
- "pipeline diagram", "brainstorm board", "visualize this"
- `/content canvas`

## Prerequisites
- Node.js 18+ installed
- First use runs `npm install` in `tldraw-canvas/`

## 3-Mode Workflow

### PLAN Mode
1. Check Node.js: `node --version`
2. If tldraw-canvas/node_modules missing → run `npm install` in `tldraw-canvas/`
3. Determine visualization type: mind map, content plan, pipeline, freeform

### CLARIFY Mode
- Ask: What to visualize? (topic, plan, pipeline, etc.)
- Ask: Canvas type?
  - `mind-map` — Central topic with branches
  - `content-plan` — Timeline or grid of content pieces
  - `pipeline` — Flow diagram with stages
  - `freeform` — Empty canvas, user draws
- Ask: Include content from analysis? (if references/analysis exists)

### IMPLEMENT Mode
1. Generate canvas data JSON:
   ```bash
   python scripts/canvas/generate_canvas.py --type mind-map --topic "Content Strategy" --output tldraw-canvas/public/canvas-data.json
   ```
2. Start dev server:
   ```bash
   cd tldraw-canvas && npm run dev
   ```
3. Open browser to http://localhost:5173

## Canvas Data Format
The Python script generates a JSON file with tldraw-compatible shapes:
- Rectangles with text for nodes
- Arrows for connections
- Color coding by category
- Auto-layout for readability

## Output
- Interactive canvas at http://localhost:5173
- Canvas data saved to: `tldraw-canvas/public/canvas-data.json`
- Exported snapshots saved to: `output/canvas/`

## Notes
- Dev server runs until manually stopped (Ctrl+C)
- Canvas is interactive — user can drag, resize, add shapes
- Data persists in canvas-data.json between sessions
