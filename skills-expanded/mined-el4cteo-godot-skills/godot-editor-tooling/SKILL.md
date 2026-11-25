---
name: godot-editor-tooling
description: Extend the Godot 4.7 editor - safe @tool/[Tool] scripts, configuration warnings, dynamic inspector properties, EditorScript, EditorPlugin with EditorDock (add_control_to_dock is deprecated), inspector plugins, gizmos, import/post-import/export plugins, undo/redo, addons, GDExtension. Use for editor plugins, custom docks, importers or level tools.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Editor tooling (4.7)

Check editor APIs with `../godot-core/scripts/api_lookup.py`. It flags deprecations, for example `EditorPlugin.add_control_to_dock` says "Use add_dock instead".

## @tool scripts (code that runs inside the editor)
- `@tool` (GDScript) / `[Tool]` (C#) at the top. The script runs in the editor **and** in the game. Guard game logic with `if Engine.is_editor_hint(): return`, and guard editor-only code with the opposite check.
- Every class the tool script calls on must also be `@tool`, or it runs as a placeholder. Errors in tool scripts can crash the editor, so keep them small and defensive.
- Nodes created by a tool must get `node.owner = get_tree().edited_scene_root` to be saved with the scene.
- Configuration warnings: override `_get_configuration_warnings() -> PackedStringArray` and call `update_configuration_warnings()` when inputs change. They show as a ⚠ icon in the Scene dock.
- Inspector buttons: `@export_tool_button("Bake", "Bake") var bake := _bake` (C#: `[ExportToolButton]`).
- Dynamic properties: `_get_property_list()`, `_get(name)`, `_set(name, v)`, `_validate_property(prop)` (hide or readonly per state), then `notify_property_list_changed()`.
- Changes made by tools should be undoable: `EditorInterface.get_editor_undo_redo()` → `create_action`, `add_do_property`/`add_undo_property`, `commit_action`.

## EditorScript (one-off automation)
`@tool extends EditorScript` with `func _run():`. Run it from the Script editor (File → Run, Ctrl+Shift+X) or from the command palette (4.5+). It's good for batch-renaming nodes, fixing resources and generating scenes. For headless automation outside the editor, use `../godot-core/scripts/run_godot.py script` or `scene_edit.py`.

## EditorPlugin (addons/<name>/)
- `plugin.cfg` (`name`, `description`, `author`, `version`, `script`) plus a `@tool extends EditorPlugin` script. Enable it in Project Settings → Plugins. Enabled plugins are listed in `project.godot [editor_plugins]`.
- Pair every `_enter_tree` add with an `_exit_tree` remove. Plugins get disabled and re-enabled during development.
- **Docks (4.6+):** create an `EditorDock` (experimental), set `title`, `default_slot` (`DOCK_SLOT_LEFT_UL` … `DOCK_SLOT_BOTTOM` for bottom panels) and `available_layouts`, add your UI as a child, then `add_dock(dock)` / `remove_dock(dock)`. **`add_control_to_dock` and `add_control_to_bottom_panel` are deprecated.**
- Other hooks: `add_tool_menu_item`, `add_inspector_plugin(EditorInspectorPlugin)`, `add_node_3d_gizmo_plugin`, `add_import_plugin`, `add_scene_post_import_plugin`, `add_export_plugin`, `add_autoload_singleton` (for addon runtime singletons), main screens (`_has_main_screen`, `_make_visible`), and viewport input (`_handles` + `_forward_3d_gui_input`/`_forward_canvas_gui_input`).
- Custom node types: prefer `class_name` + `@icon("res://addons/x/icon.svg")` over `add_custom_type`.
- `EditorInterface` (a singleton) gives you `get_edited_scene_root()`, `get_selection()`, `get_resource_filesystem().scan()`, `edit_node()`, `open_scene_from_path()`, `get_editor_settings()` and `get_base_control()` for theme colors.

## Import pipeline
- Per-asset scene tweaks: an `EditorScenePostImport` script (`_post_import(scene)`) set in the import dock's "Import Script". Use it to add collisions, set materials or rename nodes on every reimport.
- Project-wide scene tweaks: `EditorScenePostImportPlugin` (via `add_scene_post_import_plugin`).
- New file formats: `EditorImportPlugin` (`_get_recognized_extensions`, `_get_save_extension`, `_get_resource_type`, `_get_import_options`, `_import` → `ResourceSaver.save` to `save_path + "." + ext`).
- Export-time changes: `EditorExportPlugin` (`_export_begin`, `_export_file` → `skip()`/`add_file()`, `_get_export_features`).

## GDExtension (native code)
- Use it when you need C++ (or Rust/Swift bindings) speed, or native SDKs (Steam, platform services). Otherwise GDScript or C# is simpler.
- A `.gdextension` file defines the entry symbol, `compatibility_minimum = "4.7"` and per-platform libraries. Build against `godot-cpp` matching the engine (`--dump-extension-api` generates the API JSON).
- Loaded extensions are listed in a 4.7 Project Settings section. `GDExtensionManager.load_extension()` loads them at runtime. GDExtension classes behave like built-ins (inspector, `class_name`, docs through `--gdextension-docs`).

## Distribution
Put everything under `addons/<name>/` (LICENSE, README, `plugin.cfg`, icons) and avoid absolute paths outside it. Publish on the Godot Asset Store (4.7) or as a git submodule. Version it with semver in `plugin.cfg`.

Tool node with warnings and dynamic props, EditorScript batch fix, plugin with EditorDock, inspector plugin, post-import script, export plugin (compiled by the tests): [references/patterns.md](references/patterns.md)
