---
name: operate-blender
description: Use when the user asks to create, build, manipulate, render, animate, or export 3D content (scenes, models, characters, environments, stylized/cartoon or hyper-real art, procedural geometry). Routes to extensions/blender-operator/wrapper.py, which drives headless Blender through a TCP exec loop with full bpy access; no GUI, no MCP addon, free/GPL tooling.
---

# Operate Blender

Drive **Blender** (free, GPL; output license-free) headless via
`extensions/blender-operator/wrapper.py`. It spawns
`blender -b --factory-startup --python blender_server.py -- --port N`; the
server keeps Blender alive and evaluates bpy code over JSONL TCP on
`127.0.0.1:19693`. The exec namespace is persistent and preloaded with
`bpy` across calls, so you can build a scene incrementally.

## Commands

```bash
W=extensions/blender-operator/wrapper.py

python $W --self-test            # blender discovery + version check
python $W launch [--blend f.blend] [--timeout 60]
python $W status                 # server up/down, blender version, pids
python $W exec --code "..."      # eval/exec bpy inline
python $W exec --file script.py  # run a script file (preferred)
python $W kill                   # graceful shutdown + pid cleanup
```

All output is JSON; exit 0 = ok. `launch` blocks until the server answers
`ping` (returns Blender version) or times out. Blender binary resolution:
`--exe` > `BLENDER_EXE` env > PATH > standard install dirs. If
`--self-test` reports `blender not installed`, ask the user to install it
(blender.org, winget `BlenderFoundation.Blender`) or pass `--exe`.

## Session protocol

1. `status` first; `launch` only if server down.
2. Reset scene at task start:
   `bpy.ops.wm.read_factory_settings(use_empty=True)`.
3. Build with `exec --file` scripts (atomic, reviewable). Inside a script,
   set `_result = {...}` to return structured JSON (`result_json` field).
   Expressions are eval()ed; statements are exec()ed; stdout/stderr are
   captured and returned (truncated at 64KB).
4. `kill` when done. Always.

## Verification loop (mandatory for visual work)

Never claim a scene/character/environment is done without a render:

```python
# inside exec code
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'        # or 'CYCLES' (5.x enum; 4.2 was 'BLENDER_EEVEE_NEXT')
sc.render.resolution_x = 960; sc.render.resolution_y = 540
sc.render.filepath = r'<abs path>\out.png'
bpy.ops.render.render(write_still=True)
```

Then `read` the PNG yourself and check it. Broken camera framing, black
frames, and z-fighting are detected by looking, not by exit code.

## Recipes by axis (bpy idioms)

**Scene setup.** `bpy.ops.mesh.primitive_*_add()` for primitives;
`bpy.ops.object.camera_add()` + point at target via `Quaternion`/`track`;
lights via `bpy.ops.object.light_add(type='AREA'|'SUN'|'POINT')`; world
background via `sc.world.node_tree.nodes['Background']`.

**Materials (hiper-realismo).** `mat.use_nodes=True`; Principled BSDF
inputs by name ('Base Color','Metallic','Roughness','IOR','Alpha');
image textures via `nodes.new('ShaderNodeTexImage')` + `bpy.data.images.load`;
use Cycles + `scene.cycles.samples` + denoise for final, EEVEE for iterate.

**Cartoon/NPR.** EEVEE only: `nodes.new('ShaderNodeShaderToRGB')` +
ValToRGB ramp for cel bands; outlines via inverted-hull duplicate
(Solidify modifier, negative offset, flip normals, black material) or
Line Art: `bpy.ops.object.gpencil_add(type='LINEART_*')` in 4.x, or
Freestyle (`sc.render.use_freestyle=True`). Grease Pencil 3 for 2D-in-3D.

**Procedural.** Direct mesh: `m = bpy.data.meshes.new('x');
m.from_pydata(verts, [], faces); m.update()`. Geometry Nodes in 4.x:
`ng = bpy.data.node_groups.new('g','GeometryNodeTree')`; declare sockets via
`ng.interface.new_socket(...)`; modifiers via `obj.modifiers.new(type='NODES')`.
Scatter: instance collections on points (`GeometryNodeInstanceOnPoints`).

**Animation.** `obj.keyframe_insert('location', frame=f)`; actions/
fcurves editable via `obj.animation_data.action.fcurves`; NLA for
nonlinear layering; Rigify ships bundled (`addon_enable('rigify')`) for
humanoid metarigs. Export: `bpy.ops.export_scene.fbx(filepath=...)` or
`.gltf` (glTF 2.0, default exchange format).

**Personagens.** Sculpt pipeline: remesh voxel (`obj.data.remesh_voxel_size`)
for freeform, multires modifier for detail, Quad Remesh via
`bpy.ops.object.quadriflow_remesh()` for retopo. Hair: curves-based
hair assets (4.x `curves` sculpt). Humanoid baseline: MPFB2 (free,
MakeHuman-for-Blender, CC0 output) if user installs it; otherwise build
from primitives + skin modifier (`bpy.ops.object.modifier_add(type='SKIN')`).

**Cenarios.** Terrain: ANT Landscape addon ships with Blender
(`bpy.ops.preferences.addon_enable(module='ant_landscape')`) or Grid mesh
+ Displace modifiers w/ procedural textures. Scatter: Geo Nodes
instance-on-points, or `bpy.ops.object.collection_instance_add`. Sky:
`ShaderNodeTexSky` in world nodes. Geo-referenced terrain: BlenderGIS
addon (optional, user installs).

**AI-3D generation (self-hosted, $0).** If ComfyUI is running
(`http://127.0.0.1:8188`), POST a workflow JSON to `/prompt`, poll
`/history`, then `bpy.ops.import_scene.gltf()` the GLB. Local model
alternatives callable from plain Python: TRELLIS (MIT), TripoSG (MIT),
InstantMesh (Apache), Hunyuan3D-2.1 (Tencent license: no EU/UK/KR).
Generated meshes import, then refine with the recipes above.

## Boundaries

- Never modify the Blender install dir or `bpy` internals; scene state
  only.
- Write renders/exports under the task workdir or `.devin/scratch/`,
  absolute Windows paths inside bpy strings (`r'C:\...'`).
- Long renders: raise `--timeout`; the socket blocks until exec returns.
- GPL note: Blender is GPL but its output (renders, exports) is the
  user's property; safe for any downstream use.
- `kill` at session end; do not leave orphaned `blender -b` processes.
