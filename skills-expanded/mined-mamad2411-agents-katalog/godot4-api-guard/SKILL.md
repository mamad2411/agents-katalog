---
name: godot4-api-guard
description: Prevent Godot 3 API calls from leaking into Godot 4 code. Use this before writing, reviewing, or debugging any GDScript, and especially when code was copied from a tutorial, StackOverflow answer, blog post, or your own recall — Godot 3 material vastly outnumbers Godot 4 material online, so old-API hallucinations are the single most frequent source of broken generated GDScript. Also use when you see errors like "Invalid call. Nonexistent function", "Identifier not found", or "yield is not a valid keyword".
category: engineering
---

# Godot 4 API Guard

Godot 4 renamed or removed a large share of the Godot 3 API. Most GDScript in the world — tutorials, forum answers, training data — is Godot 3. When generating code from memory, the old names come out fluently and confidently, and the failure looks like a typo rather than a version mismatch.

Treat every one of the following as a red flag requiring a check, not a guess.

## Instant tells that code is Godot 3

If you see any of these, the snippet is Godot 3 and needs translating before use:

- `yield(` anywhere
- `export var` or `onready var` without a leading `@`
- `.instance()` on a PackedScene
- `connect("name", self, "_method")` — the three-argument string form
- `Pool*Array` types
- `KinematicBody2D`, `Spatial`, `Sprite` (unsuffixed), `Reference`
- `File.new()` or `Directory.new()`

## Core translations

| Godot 3 | Godot 4 |
|---|---|
| `yield(obj, "signal")` | `await obj.signal` |
| `export var hp := 10` | `@export var hp := 10` |
| `onready var s = $Sprite` | `@onready var s = $Sprite2D` |
| `tool` (first line) | `@tool` |
| `scene.instance()` | `scene.instantiate()` |
| `obj.connect("hit", self, "_on_hit")` | `obj.hit.connect(_on_hit)` |
| `emit_signal("died")` | `died.emit()` (string form still works) |
| `get_tree().change_scene(path)` | `get_tree().change_scene_to_file(path)` |
| `File` / `Directory` | `FileAccess` / `DirAccess` |
| `PoolByteArray`, `PoolVector2Array` | `PackedByteArray`, `PackedVector2Array` |
| `Reference` | `RefCounted` |
| `OS.get_ticks_msec()` | `Time.get_ticks_msec()` |
| `rand_range(a, b)` | `randf_range(a, b)` / `randi_range(a, b)` |
| `deg2rad` / `rad2deg` | `deg_to_rad` / `rad_to_deg` |
| `linear2db` / `db2linear` | `linear_to_db` / `db_to_linear` |
| `stepify(v, s)` | `snapped(v, s)` |
| `is_network_master()` | `is_multiplayer_authority()` |
| `remote` / `puppet` keywords | `@rpc(...)` annotation |
| `OS.window_size` | `DisplayServer.window_get_size()` |

## Node renames

| Godot 3 | Godot 4 |
|---|---|
| `Spatial` | `Node3D` |
| `KinematicBody2D` / `KinematicBody` | `CharacterBody2D` / `CharacterBody3D` |
| `Sprite` | `Sprite2D` |
| `AnimatedSprite` | `AnimatedSprite2D` |
| `Position2D` | `Marker2D` |
| `CollisionShape` | `CollisionShape3D` |
| `VisibilityNotifier2D` | `VisibleOnScreenNotifier2D` |
| `Viewport` (as render target) | `SubViewport` |
| `Tween` (as a node) | `create_tween()` — tweens are no longer nodes |

## The one that bites hardest: move_and_slide

Godot 3 took velocity as an argument and returned the resulting velocity:

```gdscript
# Godot 3 — WRONG in Godot 4
velocity = move_and_slide(velocity, Vector2.UP)
```

Godot 4 uses the built-in `velocity` property, takes no arguments, and returns a bool for whether a collision occurred:

```gdscript
# Godot 4
velocity.y += gravity * delta
velocity.x = direction * speed
move_and_slide()

if is_on_floor():
    velocity.y = jump_force
```

Floor direction is now the `up_direction` property on the node, configured in the editor or set in code, not a per-call argument.

## Version drift inside Godot 4 itself

Godot 4 is not one API. Check the minor version before answering, because these changed mid-4.x:

- **TileMap → TileMapLayer.** `TileMap` was deprecated in 4.3 in favor of one `TileMapLayer` node per layer. Code written for 4.0–4.2 TileMap will still run but is on a deprecation path.
- **`.uid` files for scripts** arrived in 4.4. A project generating `player.gd.uid` files is on 4.4+.
- Rendering, navigation, and physics defaults shifted across minor releases more than most engines.

If the version matters to the answer and you don't know it, read it rather than assuming:

```bash
godot --version
grep config/features project.godot
```

## When you are unsure

Say so and check. A wrong-but-plausible method name costs the user a debug cycle and erodes trust in everything else you wrote. `godot --headless --path . --check-only --script res://path/to/script.gd` will surface parse errors quickly, and the `godot-verify` skill runs the full loop.

For anything not in the tables above, the authoritative source is the class reference for the exact minor version the project targets — not recall.
