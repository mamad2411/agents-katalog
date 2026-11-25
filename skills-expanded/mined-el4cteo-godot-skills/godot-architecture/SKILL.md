---
name: godot-architecture
description: Structure Godot 4.7 projects that scale - feature-based folders, scene composition and components, when to use autoloads, event bus, custom Resources as data, state machines, scene switching and loading screens, save/load (safe formats), groups and dependency injection, mixed GDScript + C# projects. Use when starting a project, adding a system, or refactoring Godot code.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Godot architecture (4.7)

Inspect what already exists before adding anything: `python ../godot-core/scripts/project_inspect.py` (autoloads, input map, folders, C#). Reuse existing systems rather than adding parallel ones.

## Folder layout: by feature, not by file type
```
res://
  game/                 # cross-cutting: autoloads, event bus, save system, settings
  common/               # reusable components (health, hitbox, interactable) + shared UI widgets
  player/  player.tscn  player.gd|Player.cs  player_stats.tres  sprites/  sfx/
  enemies/  goblin/ ...  enemy_base.tscn (inherited by each enemy)
  levels/  level_01.tscn ...
  ui/  hud/ menus/ theme/main_theme.tres
  addons/               # third-party plugins only
```
Use snake_case for files and folders (they're case-sensitive in exports). C# files are named after their class (`Player.cs`). Keep each scene next to its script and assets.

## Composition rules
- **One scene per thing**, with a root node of the right type (`CharacterBody3D`, `Area2D`, `Control`). Instance scenes; don't build trees in code. Code only clones and drives them.
- Put reusable behavior in **component nodes** (`HealthComponent`, `Hitbox`, `Interactable`) with a `class_name`/`[GlobalClass]`, typed signals and `@export` configuration. The parent wires them together.
- **Call down, signal up.** A node calls methods on its children and listens to their signals. It never reaches up with `get_parent().get_parent()`.
- Siblings talk through the common parent (signal → parent → method) or the event bus. Avoid hard `../../X` paths.
- Inject dependencies with `@export var target: Node3D` or `@export var stats: EnemyStats` set in the inspector. Use `%UniqueName` inside a scene.
- Groups (`add_to_group("enemies")`, `get_tree().call_group(...)`, `get_nodes_in_group`) are good for broadcast and queries. Don't use them to fetch one specific node.
- Scene inheritance (`enemy_base.tscn` → `goblin.tscn`) for variants. Composition for behaviors. Keep inheritance chains shallow, at most 2 levels.

## Autoloads (singletons): few and boring
Good uses: an `Events` signal bus, `SaveSystem`, `Settings`, `SceneManager`, `Audio`. Each owns global state and never holds level nodes.
Bad uses: a "GameManager" that knows every node. Gameplay state that belongs to a level goes in the level scene.
Register autoloads in Project Settings → Globals (stored as `[autoload] Name="*res://game/events.gd"`), or in `project.godot`.
C# autoloads work the same way. Expose `public static Events Instance` and set it in `_EnterTree`.

## Data: custom Resources
- Write `class_name EnemyStats extends Resource` (or `[GlobalClass] partial class EnemyStats : Resource`) with `@export` fields, then create `.tres` files in the editor. Designers edit them in the inspector.
- Resources are **shared by default**. Every enemy using `goblin_stats.tres` sees the same object. Call `stats.duplicate()` per instance for mutable runtime state, or enable `resource_local_to_scene`.
- Use `duplicate_deep()` (4.5+) when nested sub-resources must be copied too.

## State machines
- A few states with simple logic: an `enum` plus `match` in `_physics_process` (see the reference).
- Many states, each with enter/exit/update: a node per state, or a `RefCounted` per state, driven by a small machine.
- Animation-only state: an `AnimationTree` StateMachine (`godot-animation`). Keep gameplay and animation state separate, and sync them through `travel()`.

## Scenes, loading, saving
- Switch scenes with `get_tree().change_scene_to_file(path)` / `change_scene_to_packed(ps)` / `change_scene_to_node(node)` (4.7). For large levels, load in the background with `ResourceLoader.load_threaded_request` behind a loading screen.
- Settings go in `ConfigFile` at `user://settings.cfg`. Saves go in JSON (`JSON.stringify`/`JSON.parse_string`) or `FileAccess.store_var(data, false)` at `user://save_1.json`.
- **Never `load()` `.tres`/`.res` files that users can edit or share as save files.** Resources can embed scripts, so this is arbitrary code execution. Use JSON or ConfigFile for anything that leaves the machine.
- Version every save file (`"version": 3`) and migrate on load.

## Mixed GDScript + C#
Both can live in one .NET project. Pick one main language for gameplay. Use the other at clear boundaries: C# for heavy systems, GDScript for quick tools and editor scripts. Talk across the boundary through signals, `Call`/`Get`, or shared Resources. Keep data in Resources so both sides can read it.

Patterns (event bus, state machine, save system, scene manager), compiled by the tests: [references/patterns.md](references/patterns.md)
