---
name: godot-scene-surgery
description: Safely read, edit, and repair Godot .tscn and .tres files by hand. Use this whenever you are about to open, diff, patch, merge, or generate a scene file, resource file, or .godot project file — including adding or removing nodes, rewiring signals, fixing a "resource not found" or broken uid:// error, or resolving a git merge conflict in a scene. Godot scene files look like plain INI and are extremely easy to corrupt, so consult this before any direct edit rather than after something breaks.
category: engineering
---

# Scene Surgery

Godot's `.tscn` and `.tres` files are human-readable text, which makes them tempting to edit directly. They are also full of cross-references that must stay consistent, and a file that is one id off will fail to load with an error that points at the wrong place. Editing them blind is the single most common way an agent breaks a Godot project.

## The default answer is: don't hand-edit

Prefer, in this order:

1. **Change it in the editor** — tell the user what to click. Slower for you, zero risk.
2. **Change it from GDScript at runtime or in a `@tool` script** — `add_child`, `set_script`, `ResourceSaver.save()`. The engine writes valid files by construction.
3. **Hand-edit the text** — only for small, well-understood changes, and only after reading this file.

If the user asked for something a script can do, write the script. "Add a `Timer` child to every enemy scene" is a `@tool` script or an `EditorScript`, not fifteen text patches.

## Anatomy of a .tscn (format 3 = Godot 4)

```
[gd_scene load_steps=3 format=3 uid="uid://bx8n2k4mqvr1t"]

[ext_resource type="Script" path="res://scripts/player.gd" id="1_qw3rt"]
[ext_resource type="Texture2D" path="res://art/player.png" id="2_hj8kl"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_a1b2c"]
size = Vector2(16, 24)

[node name="Player" type="CharacterBody2D"]
script = ExtResource("1_qw3rt")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture = ExtResource("2_hj8kl")

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_a1b2c")

[connection signal="body_entered" from="Hurtbox" to="." method="_on_hurtbox_body_entered"]
```

Things that must stay in sync, and that break silently when they don't:

- **`id` strings** — every `ExtResource("x")` and `SubResource("y")` reference must match a declared block. Ids are strings in format 3, not integers as in Godot 3.
- **`load_steps`** — the engine uses it to size its loading. If you add or remove a resource block, this number is now wrong. Don't guess at the arithmetic; open and resave the scene in the editor, which regenerates it correctly.
- **`uid="uid://..."`** — the stable identity of the file. **Never invent, copy, or edit a uid.** Two files sharing a uid corrupts the project's uid cache in `.godot/`. If a uid looks wrong, delete the line entirely and let the editor regenerate it; do not make one up.
- **`parent="..."`** — a NodePath relative to the scene root. `parent="."` is the root, `parent="Sprite2D/Trail"` is nested. Rename a node and every child's `parent` path, every `[connection]`, and every `NodePath(...)` property pointing at it must change too.
- **Node declaration order** — a child must appear after its parent in the file.

## Safe edits vs unsafe edits

Reasonably safe to do by hand:

- Changing a scalar property value on an existing node (`position = Vector2(10, 20)`).
- Renaming a node **plus** every reference to it, done in one pass.
- Adding a `[connection]` line for a signal that exists on a node that exists.
- Deleting a leaf node with no references pointing at it.

Do not do by hand:

- Adding a new `ext_resource` or `sub_resource` (touches `load_steps`).
- Reordering or renumbering ids.
- Anything involving `uid://`.
- Merging a git conflict in a `.tscn` by picking hunks. Take one side whole, then redo the other side's change in the editor. Interleaved scene hunks almost never produce a loadable file.
- `.tres` files for built-in resource types with binary-ish payloads (baked navigation, lightmaps, imported meshes).

## Before you edit

Confirm the format version. `format=3` is Godot 4.x; `format=2` is Godot 3.x and means the project is on the old engine, which changes almost every API answer you would otherwise give. If you see `format=2`, stop and check with the user which engine version they are on.

## After you edit

Verify the file still loads instead of assuming it does:

```bash
godot --headless --path . --quit
```

This imports and opens the project without a window. A broken scene surfaces as a load error on stderr. Read the output; do not report success on a non-zero exit code. If the `godot-verify` skill is available, use its runner instead so test results come back in the same pass.

## Common errors and what they actually mean

| Error | Real cause |
|---|---|
| `Cannot open file 'res://...'` in a scene | An `ext_resource` path points at a moved or deleted file |
| `Resource file not found: uid://...` | A uid was hand-edited, or `.godot/` cache is stale — try deleting `.godot/` and reimporting |
| `Node not found: "X"` at runtime | A `parent=` path or `NodePath()` property survived a node rename |
| Scene opens but a node lost its script | `script = ExtResource("id")` references an id that no longer exists |
| Every node is a child of the root after a merge | Interleaved merge hunks scrambled `parent=` paths — revert and redo |
