---
name: excalidraw-lite
description: Use for simple diagrams with 3-10 nodes — flowcharts, quick flows, basic relationships. Fast, low-token. Use excalidraw-diagram instead for complex architecture, nested containers, or multi-zone systems.
---

## Rules
- No clarifying questions. Interpret and generate immediately.
- No planning commentary. Output JSON + one-line summary.
- Standard node size: w=200, h=60. Arrow spacing: 80px between nodes.
- Max 3 colors. Left-to-right OR top-to-bottom. Never both.

---

## Color Palette (pick what fits, use sparingly)

| Role | strokeColor | backgroundColor |
|------|-------------|-----------------|
| Input / start | `#1971c2` | `#e7f5ff` |
| Process / middle | `#f59f00` | `#fff9db` |
| Output / end | `#2f9e44` | `#d3f9d8` |
| Neutral | `#495057` | `#f8f9fa` |

All text inside shapes: `#1e1e1e`. Arrow labels: match arrow's strokeColor.

---

## Layout Grid

**Left-to-right flow:**
- Node 1: x=30, y=100 → Node 2: x=310 → Node 3: x=590 (step = node_width + 80px gap)
- Arrow: x = prev_right, y = node_center_y, points = [[0,0],[80,0]]

**Top-to-bottom flow:**
- Node 1: x=300, y=30 → Node 2: y=170 → Node 3: y=310 (step = node_height + 50px gap)
- Arrow: x = node_center_x, y = prev_bottom, points = [[0,0],[0,50]]

**Branch (1 → 2 outputs):**
- Parent center → child left and child right using diagonal points

---

## Element Schema (minimal — include ALL fields)

### Rectangle node
```json
{
  "id": "node-1",
  "type": "rectangle",
  "x": 30, "y": 100,
  "width": 200, "height": 60,
  "angle": 0,
  "strokeColor": "#1971c2",
  "backgroundColor": "#e7f5ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": {"type": 3},
  "boundElements": [],
  "updated": 1,
  "link": null,
  "locked": false
}
```

### Text label (always paired with its node)
```json
{
  "id": "label-1",
  "type": "text",
  "x": 30, "y": 121,
  "width": 200, "height": 20,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "boundElements": [],
  "updated": 1,
  "link": null,
  "locked": false,
  "text": "Node Label",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "Node Label",
  "lineHeight": 1.25
}
```
> Text y = node_y + 21 (centers text vertically in a 60px tall node)

### Arrow
```json
{
  "id": "arrow-1-2",
  "type": "arrow",
  "x": 230, "y": 130,
  "width": 80, "height": 0,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": {"type": 2},
  "boundElements": [],
  "updated": 1,
  "link": null,
  "locked": false,
  "points": [[0, 0], [80, 0]],
  "lastCommittedPoint": null,
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

---

## JSON Wrapper
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ... ],
  "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

---

## Deliver

1. Save to `diagrams/[slug].excalidraw` (always use the `diagrams/` subfolder to keep the project root clean)
2. Output the JSON in a code block
3. One sentence describing what the diagram shows

> **To open:** Go to excalidraw.com → menu → Open → select the `.excalidraw` file. Or paste the JSON directly with Cmd+V.
