---
name: godot-core
description: Start here for any Godot 4.7 task (GDScript or C#/.NET). Exact API lookup from the installed engine, headless run/import/smoke tests, safe scene editing, project inspection, 4.5-4.7 changes and Godot 3 traps, and routing to the specialized godot-* skills. Use for any Godot, .gd, .cs, .tscn or project.godot request.
license: MIT
compatibility: Godot 4.7+ (standard or .NET build). Python 3.9+ for scripts. .NET 8+ SDK for C# projects.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Godot Core (4.7)

Script paths below are relative to this skill's folder. Sibling skills sit next to it (`../godot-csharp/...`).
All scripts print one compact JSON object. Run them; you don't need to read them. Set `GODOT_EXE` if the engine isn't found.

## Non-negotiables
1. **Never guess an API.** Your training data mixes Godot 3, early 4.x and 4.7. Check names, signatures, defaults and the matching C# name before you use them:
   `python scripts/api_lookup.py Class.member`, or `Class` / `--search word` / `@export_range` / `ProjectSettings.physics/3d/physics_engine`.
   It reads the engine you have installed, so the answer is always correct for that version.
2. **Don't hand-write `.tscn`/`.tres` structure.** Use `scripts/scene_edit.py`, which builds scenes through Godot itself. It never saves a half-applied edit. Changing a single property value in a text file is fine.
3. **Verify before you say it's done:** run `gd_check.py` and/or `cs_build.py`, then `run_godot.py smoke`, then `test_run.py` (see the loop below).
4. Read [references/godot3-traps.md](references/godot3-traps.md) before writing code from memory. Read [references/whats-new.md](references/whats-new.md) whenever a feature might be new (4.5–4.7).

## Route to the specialized skill
| Task | Skill |
|---|---|
| GDScript language, typing, signals, await, style | `godot-gdscript` |
| C#/.NET: csproj, partial classes, [Export]/[Signal], interop, marshaling | `godot-csharp` |
| Project structure, scenes vs scripts, autoloads, Resources, state machines, saves | `godot-architecture` |
| 2D: TileMapLayer, Parallax2D, Camera2D, 2D lights | `godot-2d` |
| 3D rendering: renderers, lights (AreaLight3D), GI, materials, HDR, import | `godot-3d-rendering` |
| Physics: Jolt, CharacterBody, raycasts, layers, ragdolls | `godot-physics` |
| UI: Controls, containers, themes, responsive layout, accessibility | `godot-ui` |
| Input: actions, rebinding, gamepads, gyro, touch, VirtualJoystick | `godot-input` |
| Animation: AnimationPlayer/Tree, Tween, IK, skeleton modifiers | `godot-animation` |
| Shaders, VFX, particles, compositor, stencil | `godot-shaders-vfx` |
| Audio: buses, interactive music, 3D audio | `godot-audio` |
| Multiplayer, RPC, replication, HTTP, sockets | `godot-networking` |
| Profiling, optimization, threading, servers | `godot-performance` |
| Export presets, templates, CLI/CI builds, platforms | `godot-export-ci` |
| `@tool`, EditorPlugin, docks, import/export plugins, GDExtension | `godot-editor-tooling` |
| Unit tests (GdUnit4, gdUnit4Net), debugging, logging | `godot-testing-debug` |
| VR/AR, OpenXR | `godot-xr` |
| Pathfinding, navmesh, enemy AI, behavior trees | `godot-navigation-ai` |
| 3D controllers, third-person cameras, GridMap/CSG levels | `godot-3d-gameplay` |
| Procedural levels, noise, dungeons, runtime meshes | `godot-procedural` |
| Upgrading from Godot 3 / older 4.x, porting from Unity | `godot-migration` |
| Phones, tablets, browsers: safe area, lifecycle, Web hosting | `godot-mobile-web` |
| Dialogue, quests, story flags, cutscenes | `godot-narrative` |
| Mods, DLC, PCK packs, patches | `godot-modding-dlc` |
| Screen shake, hit-stop, juice, trailers | `godot-game-feel` |
| Third-party addons and plugins | `godot-addons` |

## Tools
| Need | Command |
|---|---|
| Engine path, version, .NET or not | `python scripts/run_godot.py version` |
| Project summary: renderer, physics, autoloads, input map, C# setup | `python scripts/project_inspect.py [DIR]` |
| Scene tree of a `.tscn` without opening Godot | `python scripts/project_inspect.py --scene res://x.tscn [--props]` |
| One project setting / list files | `project_inspect.py --setting display/window/stretch/mode`, `--files --ext gd,cs` |
| Import assets, build the `class_name` cache | `python scripts/run_godot.py import` |
| Run the game headless for N frames and collect errors | `python scripts/run_godot.py smoke [res://scene.tscn] --frames 120` |
| Run an `extends SceneTree` / `MainLoop` script | `python scripts/run_godot.py script tool.gd -- args` |
| Create or edit scenes | `python scripts/scene_edit.py spec.json` (spec format: `--help`) |

## Verification loop
1. GDScript: `python ../godot-gdscript/scripts/gd_check.py` runs the real parser and analyzer on every `.gd` file.
2. C#: `python ../godot-csharp/scripts/cs_build.py` returns `dotnet build` errors as `file:line CSxxxx`. Build before smoke tests, because the engine loads the compiled assembly.
3. `run_godot.py smoke` runs the main scene headless. Any `errors` entry means a runtime problem, such as a null node path or a bad cast.
4. `python ../godot-testing-debug/scripts/test_run.py` runs the unit tests when the project has any.
For GPU-dependent visuals, ask the user to check the running game. Headless mode doesn't render.

## Working with a user's open editor
- The editor reloads files changed on disk. It asks before reloading a scene with unsaved edits, so tell the user to save before you edit a scene that's open.
- The `.godot/` folder is a cache. Never edit or commit it. Commit `*.uid` files (4.4+), because they keep references stable when files are renamed.
- Refer to resources by `uid://` or `res://` paths. Never use OS paths inside a project.
- Is a Godot MCP server connected? Use it for live editor state such as the open scene, selection or a running-game screenshot. These scripts are for files, the CLI and verification.

## Project facts to check first
Run `project_inspect.py` and respect what it finds:
- the renderer (`forward_plus`, `mobile` or `gl_compatibility`), which decides what you may use (see `godot-3d-rendering`)
- the 3D physics engine (new 4.6+ projects use Jolt)
- the stretch mode (new 4.7 projects use `canvas_items` + `expand`)
- whether the project has C#, from `csharp` in the output: mixed GDScript + C# projects are valid
- existing autoloads, input actions and folder layout, which you reuse instead of duplicating

## References
- [references/godot3-traps.md](references/godot3-traps.md): stale Godot 3 / early-4 APIs and their 4.7 replacements
- [references/whats-new.md](references/whats-new.md): 4.5, 4.6 and 4.7 features and breaking changes, from a diff of the real API
- [references/cli.md](references/cli.md): Godot command-line flags (from 4.7.2 `--help`)
