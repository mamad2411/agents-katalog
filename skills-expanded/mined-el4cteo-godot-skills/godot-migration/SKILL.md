---
name: godot-migration
description: Upgrade or port a project to Godot 4.7 - Godot 3 to 4 (converter, GDScript 2.0, C# partial classes, shaders, TileMap, physics), 4.0-4.6 to 4.7 breaking changes, C# csproj and SDK bumps, and Unity or Unreal concept mapping to Godot nodes, scenes, signals and Resources. Includes a scanner that lists every stale API in a project. Use when upgrading, porting or converting a project.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#). Python 3.9+ for scripts/migrate_scan.py.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Migration and Porting (to 4.7)

**Run it first:** `python scripts/migrate_scan.py [DIR]` reports the project's Godot version (`config_version=4` means Godot 3, `5` means Godot 4; `config/features` gives the 4.x minor) and every stale API with file, line and fix. `--rule NAME` filters by rule, `--limit N` caps the output. It's static and fast; it never edits files.

## Always
1. **Commit or copy the project first.** The converter and the editor rewrite files with no backup.
2. Upgrade one step at a time where it's cheap: the latest 3.x (3.6) before 4.x; for 4.x projects, open them directly in 4.7.
3. Let the editor import once (`run_godot.py import`), then loop: `migrate_scan.py` → fix → `gd_check.py`/`cs_build.py` → `run_godot.py smoke` until all are clean (`godot-core` verification loop).
4. Re-save resources so the diffs stop: **Project → Tools → Upgrade Project Files** (rewrites `.tscn`/`.tres` in the 4.7 format; 4.6+ scenes carry `unique_id=`). Commit the `*.uid` files.
5. Delete `.godot/` if the editor shows ghost errors after the upgrade (it's a cache, and it rebuilds).

## Godot 3 → 4.7
1. Dry run: `python scripts/migrate_scan.py DIR --convert` (wraps `--validate-conversion-3to4`) lists what the converter would change. Then `--convert --apply` (wraps `--convert-3to4`). Raise `--max-kb`/`--max-lines` for huge files (defaults 4000 KB, 100000 lines).
2. The converter renames classes, properties, `export`/`onready`/`yield`, many methods, shader built-ins and `.shader` → `.gdshader`. It also renames **node names in paths** (`$Camera` → `$Camera3D`) while the scene nodes keep their old names, so check every `$`/`get_node` path.
3. Then fix by hand what it can't do (the scanner finds most of these):
| Area | What to do |
|---|---|
| `setget`, `connect("sig", obj, "m", binds)`, `funcref`, RPC keywords | property `set/get` blocks, `sig.connect(m.bind(...))`, Callables, `@rpc(...)` |
| `move_and_slide(vel, up, ...)` | the converter emits `set_velocity(); move_and_slide(); velocity = velocity`: clean it up to `velocity` + `move_and_slide()`, and retune `floor_snap_length` and `floor_max_angle` |
| `Tween` node, `interpolate_property` | `create_tween().tween_property(...)` |
| `TileMap` | TileSets need re-setup (terrains replace autotile), then extract layers to `TileMapLayer` nodes (TileMap bottom panel) |
| Physics feel | gravity, friction, snapping and the engine changed. New 4.6+ projects use Jolt; a converted project keeps GodotPhysics3D until you switch `physics/3d/physics_engine` |
| Lighting/look | GLES3 → Compatibility, GLES2 doesn't exist. GIProbe → VoxelGI/SDFGI, tonemapping and glow differ, so retune the Environment (`godot-3d-rendering`) |
| Shaders | `SCREEN_TEXTURE`/`DEPTH_TEXTURE` → `uniform sampler2D x : hint_screen_texture`/`hint_depth_texture`; `hint_color` → `source_color`; see the scanner's `shader3-*` rules |
| Particles | `Particles` → `GPUParticles3D`. Process materials convert, but retune emission and sub-emitters |
| `OS.*` window and time APIs | `DisplayServer`, `get_window()`, `Time` |
| Files | `File.new()`/`Directory` → static `FileAccess.open()`/`DirAccess.open()` (they return null on error: check `FileAccess.get_open_error()`) |
| Plugins and addons | most Godot 3 addons don't work: get the 4.x version (`godot-addons`). GDNative → GDExtension (a rebuild against godot-cpp) |
| C# | regenerate the project: **Project → Tools → C# → Create C# solution** (`Sdk="Godot.NET.Sdk/4.7.2"`, `net8.0`). Then `partial` classes, `[Signal] delegate void XEventHandler()`, `+=` signal events, `double delta`, `GodotObject`, `Instantiate<T>()`, `Godot.Collections` types (`godot-csharp`) |
| Networking | the high-level multiplayer API was rewritten. Port to `MultiplayerSpawner`/`Synchronizer` and `@rpc` (`godot-networking`) |
Stale-name tables for writing new code: `../godot-core/references/godot3-traps.md`.

## 4.0–4.6 → 4.7
- Open the project in 4.7; it upgrades `project.godot` and `config/features`. Breaking changes per version are in `../godot-core/references/whats-new.md`. The scanner flags the code-level ones (`get_rpc_config`, `get_as_text(bool)`, BlendSpace `sync`, `device == 0`, C# `Animation.Length` as `double`, `StringName` animation names).
- C#: bump `Sdk="Godot.NET.Sdk/4.7.2"` in the `.csproj` (the scanner flags older SDKs), rebuild, and fix the binary breaks. Android needs `net9.0` (the generated csproj adds the condition).
- `TileMap` → `TileMapLayer`, `ParallaxBackground` → `Parallax2D`, `SkeletonIK3D` → the IK modifiers: deprecated, not removed, so migrate when you touch that code.
- Behavior to retest: `Resource.duplicate(true)` (4.5), async navigation map updates (4.5), TileMapLayer physics chunking (4.5), the glow defaults (4.6), thinner antialiased lines (4.7), `AudioStreamPlayer2D/3D.area_mask` default 0 (4.7).
- Existing projects keep their renderer, physics engine and stretch settings. New defaults apply only to new projects.
- Re-export with matching export templates (`godot-export-ci`).

## Porting from Unity or Unreal
Think in **scenes of nodes**, not GameObjects with components. A scene is a prefab, a level and a component at once.
| Unity | Godot 4.7 |
|---|---|
| GameObject + components | node tree; one script per node; compose with child nodes (`godot-architecture`) |
| Prefab / prefab variant | `PackedScene` (`.tscn`) / inherited scene |
| ScriptableObject | `Resource` (`.tres`) with `@export` fields |
| `Awake`/`Start`/`Update`/`FixedUpdate` | `_init`/`_ready`/`_process(delta)`/`_physics_process(delta)` |
| Coroutines, `async` | `await` on signals and timers (C# `await ToSignal(...)`) |
| UnityEvent, C# events | signals |
| Tags, layers | groups (`add_to_group`), collision layers/masks, visual `layers` |
| `DontDestroyOnLoad`, singletons | autoloads |
| `Resources.Load`, Addressables | `preload`/`load`, `ResourceLoader.load_threaded_request` |
| PlayerPrefs | `ConfigFile` in `user://` |
| Rigidbody / CharacterController | `RigidBody3D` / `CharacterBody3D` |
| Animator + state machine | `AnimationTree` with a state machine |
| UGUI / UI Toolkit | `Control` nodes + containers + `Theme` |
| Input System actions | Input Map actions (`godot-input`) |
| `transform.forward` (+Z) | `-global_basis.z` (**−Z is forward**; Godot is right-handed, Y-up, 1 unit = 1 m) |
| `Debug.Log` | `print()` / `GD.Print()`; `push_warning`/`push_error` |
Unreal: Actor → Node3D scene; Blueprint → GDScript or C# script on the node; GameMode/GameInstance → autoloads; Components → child nodes; DataAsset → Resource; Level streaming → `load_threaded_request` + `add_child`.

Godot 3 → 4 C# and GDScript before/after, Unity-style component patterns in Godot, and a migration checklist (compiled by the tests): [references/porting.md](references/porting.md)
