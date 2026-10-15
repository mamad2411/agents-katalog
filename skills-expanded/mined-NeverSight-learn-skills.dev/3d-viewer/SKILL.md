---
name: 3d_viewer
description: >-
  View 3D model files directly locally without installing other large software. Supports 30+ formats including
  STL/3MF/STEP/STP/GLB/GLTF/OBJ/PLY/FBX/USDZ/SCAD. Can generate 3D models from natural language using OpenSCAD.
  Supports material editing, environment maps, animation playback, wireframe/topology overlay, measurement, etc.
  Trigger words: view this 3D model, open stl file, view step model, 3mf viewer, glb viewer, generate a gear, create a bolt,
  查看这个3D模型, 打开这个STL文件, 浏览STEP模型, 3D模型查看.
license: LGPL-2.0-only
compatibility:
  - opencode
  - claude
metadata:
  formats: "stl,3mf,step,stp,glb,gltf,obj,ply,fbx,usdz,scad,3ds,dae,drc,dxf,svg,hdr,exr"
  features: "url-auto-load,drag-and-drop,STEP-topology,wireframe,material-editor,environment-maps,measurement,ai-model-generation"
---

# 3D Model Viewer

A browser-based full-featured 3D model file viewer. Supports 30+ file formats with real-time 3D rendering.
The `?url=` parameter enables auto-loading models — users see the model directly when they open the browser, no manual drag-and-drop needed.
Can generate 3D models from OpenSCAD code — describe the shape in natural language and the AI compiles it to a visible model.

## Supported Formats

| Category | Formats |
|----------|---------|
| CAD | STEP/STP, 3MF, STL, OBJ, PLY, FBX, DAE, 3DS, IFC, 3DM |
| Programmatic | SCAD (OpenSCAD — AI can generate models from code) |
| 3D Graphics | GLB/GLTF, USDZ, DRC, BVH, VTK, XYZ, PDB |
| Other | NRRD, GCode, WRL, VOX, KMZ, AMF, LWO, MD2, PCD |
| 2D | SVG, DXF |
| Environment Maps | HDR, EXR |

## Workflow

When a user asks to view a 3D model file (by path or filename), follow these steps:

### Step 1: Verify the file exists
Confirm the model file path provided by the user exists, and record its absolute path.

### Step 2: Copy file to the service directory
```bash
cp "<model_file_path>" <skill_dir>/models/
```

### Step 3: Start local HTTP server (run in background, do NOT set timeout)

> Before starting, check if port 4273 is in use. If occupied and first run, kill the occupying process first.

**Windows:**
```powershell
Start-Process -WindowStyle Hidden -FilePath "node" -ArgumentList "<skill_dir>/scripts/serve.mjs"
```

**macOS / Linux:**
```bash
nohup node "<skill_dir>/scripts/serve.mjs" > /dev/null 2>&1 &
```

> After starting, verify port 4273 is listening (e.g. `netstat -ano | findstr :4273`).

The HTTP service is a long-running process and must be started in the background. **Do not** run it in the foreground, otherwise the bash timeout will kill the process.

Default port is **4273** (use `PORT=4174 node ...` to specify a different port).

This service also provides an **HTTP API** for AI to remotely control the viewer via `curl` (always include `id` so the server returns the synchronous result):
```bash
curl -X POST http://localhost:4273/api/command \
  -H "Content-Type: application/json" \
  -d '{"type":"3d-viewer","id":"req-001","command":"setTheme","params":{"value":"dark"}}'
```
The browser receives commands in real-time via SSE (`/api/events`). See Step 5 below for details.

> If `scripts/serve.mjs` is unavailable (non-Node.js environment), you can use `python -m http.server 4273` as a fallback — but this loses HTTP API remote control capability.

### Step 4: Open browser to auto-load the model
Open the following URL in the system default browser with the `?url=` parameter:

```
http://localhost:4273/#/workspace?url=./models/<filename>
```

The user will **see the model immediately** without needing to open the browser themselves, drag-and-drop files, or click upload.

Additional initial parameters can be appended:
```
http://localhost:4273/#/workspace?url=./models/<filename>&theme=dark&lang=zh
```

### Step 5: Further control (optional)

You can control the viewer at runtime through the following methods:

**Method A: MCP (Recommended — AI-native calling)**
MCP (Model Context Protocol) server exposes 30+ typed tools. AI calls them directly during conversation (e.g. "dim the theme" → automatically calls `set_theme`), no need to craft JSON:
```bash
# Point opencode/Claude Desktop config to this path
node "<skill_dir>/scripts/mcp-server.mjs"
```
The MCP server automatically connects to the running `serve.mjs`. See `docs/AI_CONTROL_API.md` for the full tool list.

**Method B: HTTP API**
Send commands to `serve.mjs` via `curl`, pushed to the browser through SSE (always include `id` for synchronous result):
```bash
curl -X POST http://localhost:4273/api/command \
  -H "Content-Type: application/json" \
  -d '{"type":"3d-viewer","id":"req-001","command":"setTheme","params":{"value":"dark"}}'
```

**Method C: postMessage (requires browser JS execution)**
```js
window.postMessage({ type: '3d-viewer', id: 'req-001', command: 'setTheme', params: { value: 'dark' } }, '*')
```

### Step 6: Cleanup
After viewing is complete, shut down the local HTTP service to release the port.


## AI Model Generation

When the user describes a 3D model in natural language (e.g. "a gear with 20 teeth", "a hex head bolt"), follow these steps:

1. First, describe your understanding of the user's modeling requirements — this way, if your understanding is off, the user can correct you right away. Assume the user does not know programming or OpenSCAD. Describe how you plan to model it in plain language.

2. Write OpenSCAD code based on the user's description, then save it to the `models/` directory with a `.scad` extension.

3. Then execute Step 3 (Start local HTTP server) and subsequent steps from the workflow above.

> **Note**: The first SCAD compilation needs to download `openscad.wasm` (~13MB), which may take several tens of seconds. Please be patient.
>
> **Note**: Compilation automatically generates the model mesh and loads it into the 3D viewer; it does not directly produce an STL file. If the user needs an STL file, use the export functionality.


## Skill Directory Structure

```
skills/3d_viewer/
├── SKILL.md              # Skill description (English)
├── SKILL_cn.md           # Skill description (Chinese)
├── index.html            # Viewer entry point
├── step-worker.js        # STEP conversion Web Worker
├── scripts/serve.mjs     # Node.js HTTP server + SSE bridge
├── scripts/mcp-server.mjs # MCP protocol server (AI-native call interface)
├── assets/               # JavaScript/CSS assets
├── wasm/                 # WebAssembly modules (OCCT/OpenSCAD/Draco/Basis/Rhino3DM)
├── env/                  # Environment maps
└── models/               # AI copies models to this directory
```


