---
name: blender-scene-preflight
description: Inspects a Blender scene before rendering and reports what it really contains - frame range, FPS, active camera, engine, resolution, samples, color management, compositor, motion blur, volumes, missing textures and linked files - and calls out any mismatch with what the user asked. Use before rendering any .blend you did not write, before sending a scene to a render farm, or when a render fails or looks wrong.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-render-director, blender-render-settings, blender-animation-delivery
---

# Blender Scene Preflight

Read the scene, report it, then decide. Most failed renders on another machine come from four things: missing files,
a different frame range than the user thinks, a camera that is not the active one, and add-ons or caches that only exist
on the author's machine.

## Run this first (read only)

Paste into a Blender MCP that runs Python, or run `blender -b scene.blend -P preflight.py`. It changes nothing.

```python
import bpy, os, json

s = bpy.context.scene
r = s.render
eng = r.engine
tree = getattr(s, "compositing_node_group", None) or (getattr(s, "node_tree", None) if getattr(s, "use_nodes", False) else None)

def missing(datablocks, kind):
    out = []
    for d in datablocks:
        path = getattr(d, "filepath", "")
        if not path or getattr(d, "packed_file", None):
            continue
        if kind == "image" and d.source not in {"FILE", "SEQUENCE", "MOVIE", "TILED"}:
            continue
        full = bpy.path.abspath(path, library=getattr(d, "library", None))
        if not os.path.exists(full.replace("<UDIM>", "1001")):
            out.append({"kind": kind, "name": d.name, "path": path})
    return out

world_volume = False
if s.world and s.world.node_tree:
    for n in s.world.node_tree.nodes:
        if n.type == "OUTPUT_WORLD" and n.inputs.get("Volume") and n.inputs["Volume"].is_linked:
            world_volume = True

report = {
    "file": bpy.data.filepath,
    "blender": bpy.app.version_string,
    "frames": [s.frame_start, s.frame_end], "frame_count": s.frame_end - s.frame_start + 1,
    "fps": round(r.fps / r.fps_base, 3),
    "camera": s.camera.name if s.camera else None,
    "cameras": [o.name for o in s.objects if o.type == "CAMERA"],
    "engine": eng,
    "resolution": [r.resolution_x * r.resolution_percentage // 100, r.resolution_y * r.resolution_percentage // 100],
    "samples": s.cycles.samples if eng == "CYCLES" else getattr(s.eevee, "taa_render_samples", None),
    "view_transform": s.view_settings.view_transform, "look": s.view_settings.look,
    "exposure": s.view_settings.exposure, "gamma": s.view_settings.gamma,
    "compositor_nodes": sorted({n.bl_idname for n in tree.nodes}) if tree else [],
    "motion_blur": r.use_motion_blur, "world_volume": world_volume,
    "film_transparent": r.film_transparent,
    "output": {"path": r.filepath, "format": r.image_settings.file_format},
    "libraries": [l.filepath for l in bpy.data.libraries],
    "missing": missing(bpy.data.images, "image") + missing(bpy.data.libraries, "library")
               + missing(bpy.data.cache_files, "cache") + missing(bpy.data.volumes, "volume")
               + missing(bpy.data.sounds, "sound") + missing(bpy.data.fonts, "font"),
    "objects": len(s.objects), "lights": sum(o.type == "LIGHT" for o in s.objects),
}
print(json.dumps(report, indent=2))
```

On JANCTION Render, `scene_info` returns the same kind of facts for an uploaded scene without rendering.

## Report it like this

```
Scene:      bedroom.blend (Blender 4.2)
Frames:     1-200 at 30 fps (6.67 s)    <- user asked for 240 frames: MISMATCH, ask
Camera:     CAM_Main (3 cameras in the scene)
Engine:     Cycles, 128 samples, 1504x846 at 100%
Color:      AgX, look None, exposure 0
Compositor: Glare, Lens Distortion   Motion blur: on   World volume: yes
Missing:    2 images (wood_diffuse.png, wall_normal.png)
```

Say the mismatch in one sentence and ask which wins: the user's number or the scene's range.

## Fix only what blocks the render

| Finding | Fix (on a copy) |
|---|---|
| Missing textures | Ask where they are; `bpy.ops.file.find_missing_files(directory=...)`, then `bpy.ops.file.pack_all()` |
| Absolute paths from another machine | `bpy.ops.file.make_paths_relative()` after the files sit next to the .blend |
| Wrong active camera | `s.camera = bpy.data.objects["CAM_Main"]` (ask if there are several) |
| Linked libraries | Send them with the scene, or `bpy.ops.wm.lib_relocate`; make local only if the user agrees |
| Simulation or Alembic caches | Bake and include the cache folder; a farm cannot re-simulate what it has not got |
| Add-on drivers or custom nodes | Check the add-on exists on the render machine; otherwise apply or bake its result |

Everything else (engine, samples, compositor, motion blur, volumes, color) is part of the look. Report it; do not change
it here.

## Save a copy, never the source

```python
import bpy, os
src = bpy.data.filepath
if not src:
    raise SystemExit("the scene has never been saved: ask the user where the source file is")
bpy.ops.wm.save_as_mainfile(filepath=os.path.splitext(src)[0] + "_render.blend", copy=True)
```
