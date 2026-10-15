---
name: blender-asset
description: "Generate `.glb` 3D assets headlessly via Blender Python (`blender --background --python`). Use when a Godot/Unity/Unreal project needs a procedural mesh / prop / room piece. Skill provides only thin helpers (`prelude.py`, `export.py`); project-specific generation scripts live in `assets/modeling/`. Do not use for live Blender editing or hero-character sculpting."
---

Headless Blender asset generation. The skill is a thin Python helper layer imported via `PYTHONPATH`; project-specific generation scripts live outside the skill in `<project>/assets/modeling/`.

## When to use

Trigger when:
- A 3D asset is needed for the project (mesh, prop, architectural piece, low-poly anything)
- The asset is parameterizable / procedural / good enough at PS1-era detail
- A `.glb` output is acceptable (Godot, Unity, Unreal, three.js — all consume glTF)

Skip when:
- Hero character with detailed sculpting is needed (Python alone is insufficient — needs an artist)
- A 2D texture is what's needed (use `image-asset` instead)
- Live Blender scene editing is required (this skill is one-shot)

## Conventions

- **Skill helpers**: `.agents/skills/blender-asset/scripts/{prelude,export,...}.py`. Imported by project scripts via `PYTHONPATH`.
- **Project asset scripts**: `<project>/assets/modeling/<name>.py`.
- **Output GLBs**: `<project>/assets/models/<name>.glb`.
- **Driver**: `.agents/skills/blender-asset/build.sh <script-path>` — bundled with the skill. Run from project root. Injects the skill's `scripts/` into `sys.path`, runs `blender --background --python … -- --out <abs>`, writes the GLB to `<project>/assets/models/<name>.glb`, logs to `<project>/logs/build_asset_<name>.log`.
- **GLB load check** (Godot): `.agents/skills/blender-asset/godot/check_glb.gd` is a `SceneTree` script that loads a GLB via `GLTFDocument` and prints node/mesh counts. Useful for headless verification:

  ```bash
  godot --headless --path . --script res://.agents/skills/blender-asset/godot/check_glb.gd -- res://assets/models/<name>.glb
  ```

## Required idioms in project scripts

1. Wrap entry with `from prelude import run; run(main)`. `run()` calls `setup()` (empties default scene) and forces `sys.exit(1)` on uncaught exceptions.
2. Output path: `args = parse_args(); save_glb(args.out)` — never hard-code paths.
3. **Prefer `bpy.data.*` / `bmesh` over `bpy.ops.*`.** Most operators require a UI context that does not exist in `--background` and fail with `Operator … poll() failed, context is incorrect`. The few primitive ops that do work are still better replaced with `bmesh.ops.*` for predictability.
4. Apply modifiers in geometry, not at export time, when you want to reason about the final mesh in script (`obj.modifiers.new(...)` then `bpy.context.view_layer.update()` and read back).

## Common pitfalls

- **Default-cube leakage**: skipping `setup()` ships Blender's startup cube/light/camera in your GLB.
- **Operator context errors**: see idiom #3.
- **Y-up confusion**: glTF is Y-up, Blender is Z-up. `save_glb` passes `export_yup=True` — do not pre-rotate the scene unless you turn this off.
- **Modifier loss in GLB**: `save_glb` uses `export_apply=True`. If you turn it off, Subdivide/Decimate/Bevel results vanish.
- **Silent exit 0 on error**: Blender returns 0 even when Python raised. `run()` is the fix — always use it.

## Verifying setup

Run `.agents/skills/blender-asset/build.sh assets/modeling/test_cube.py`. Confirm `assets/models/test_cube.glb` appears (~1 KB). If yes, pipeline is wired up.
