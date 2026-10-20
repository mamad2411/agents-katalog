---
name: operate-godot
description: Use when the user asks to build, inspect, import assets into, or export a Godot 4 project headlessly (realtime 3D delivery, game scenes, interactive world execution). Uses godot --headless --script CLI; no GUI. Free/MIT engine.
---

# Operate Godot (headless)

Drive **Godot 4** (MIT) from the CLI. Godot's own binary is the
operator; no bridge server needed. Use it for realtime delivery,
interactive scenes, physics, and game logic, where Blender's strength
is content authoring.

## Detection

```bash
godot --version            # PATH
where godot                # Windows search
```

If absent: `winget install GodotEngine.GodotEngine` (user step, free).
Use the standard build (not .NET) unless C# is required.

## Headless commands

```bash
godot --headless --editor --quit --path proj/   # import assets, build caches
godot --headless --path proj/ --script tool.gd  # run SceneTree script
godot --headless --path proj/ --export-release "Preset" out.exe
godot --headless --path proj/ --export-pack "Preset" out.pck
godot --headless --path proj/ --check-only --script tool.gd   # parse check
```

`--script` runs a GDScript extending `SceneTree` (or `MainLoop`); use
`quit()` to exit. Stdout captures print() output, so scripts can emit
JSON for agent consumption.

## Script template (query/edit a scene)

```gdscript
extends SceneTree
func _init():
    var scene = load("res://scenes/main.tscn").instantiate()
    print(JSON.stringify({"nodes": scene.get_child_count()}))
    quit()
```

Write `tool.gd` under the project (or a scratch dir passed with
`--path`), run headless, parse JSON from stdout.

## Blender -> Godot pipeline

- Export glTF from Blender (`bpy.ops.export_scene.gltf`), drop into
  Godot `res://`, run `godot --headless --editor --quit` to import.
- Godot's importer also reads `.blend` files directly (requires Blender
  installed on the same machine; it shells to `blender -b` internally).
- USDZ/usd import is supported via plugins; prefer glTF for reliability.

## Boundaries

- Godot not on PATH -> report install hint, don't silently download.
- `--script` runs GDScript; for pure scene queries, use `--check-only`
  or an export preset for validation.
- Game builds/signing are user-managed; the agent manipulates projects,
  not publishable artifacts, unless asked.
