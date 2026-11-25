---
name: geometry
description: >-
  Use when analysing or preparing USD assets in an Omniverse or Isaac Sim stage: face and vertex counts, where the
  geometry budget goes, comparing two prims or two variants, finding a scene's variant sets and switching them for a
  check, building variant sets (a full and a simplified shell), flattening references, exporting a prim as its own
  file, or fixing material paths after a copy.
allowed-tools: >-
  mcp__plugin_omniverse-mcp_omniverse__get_sim_state mcp__plugin_omniverse-mcp_omniverse__get_mesh_stats
  mcp__plugin_omniverse-mcp_omniverse__get_prim_bounds mcp__plugin_omniverse-mcp_omniverse__get_prim_properties
  mcp__plugin_omniverse-mcp_omniverse__get_scene_tree mcp__plugin_omniverse-mcp_omniverse__capture_viewport
---

# Analyse and prepare geometry

Counting is read-only; variants, flattening and exports change the stage or write files, so say what they will do
before calling them.

## Steps

1. **Where the faces are.** `get_mesh_stats` gives a prim's totals, then the tree under it to `max_depth` (2 unless
   given): each mesh's faces, vertices and triangles, and each prim's `subtree_faces`, which show the subtrees that
   cost most. Call it again on a heavy subtree, or with a larger `max_depth`, to break it down to its meshes. Implicit
   shapes (`Cube`, `Sphere`) count 0: only `UsdGeom.Mesh` has faces.
2. **Compare.** `compare_prims` with two paths compares geometry, bounds and materials; with one path, a variant set
   and two variant names, it compares the variants, switching in Kit's session layer and putting it back itself.
3. **Find the switches.** `get_scene_tree(property_filter=["variant_sets"])` writes every prim's `variant_sets` line
   to a file: grep it for lines that aren't `[]`. `get_prim_properties` gives one prim's: each set, its selection, its
   options and the layer holding the selection (`session`, `root` or a file's name).
4. **Switch for a check.** `set_variant_selection` writes in Kit's session layer by default, which no save writes,
   so every file stays as it was; `variant_name=""` clears that selection and the files' own shows again. Capture or
   measure each state, then clear what you switched. A switch on an instance prim gives it a prototype of its own
   (the answer's `Note:`); a prim inside an instance is refused, naming the instance to switch.
5. **Variants to keep.** `create_variant_structure` makes a set with named variants; fill each, then
   `set_variant_selection(..., layer="edit_target")` writes the selection where edits go: the root layer, which
   `save_scene` keeps, unless Kit's Layer window made a sublayer the edit target, which `save_scene` doesn't write
   (the answer says so).
   Always switch with the tool: it detects Fabric Scene Delegate and refreshes the viewport where Kit needs it
   (before Kit 110, Isaac Sim 5.x), where a switch from `execute_script` can leave stale geometry on screen.
6. **Asset preparation.**
   - `flatten_usd` resolves every reference into one file; `export_prim_as_file` writes a subtree as a self-contained
     file. Both overwrite the output path: confirm it with the user. Both refuse a file the open stage has loaded, its
     own included: write elsewhere, or `save_scene` to save the open stage itself.
   - After copying assets to a new folder, `update_material_paths(old_prefix, new_prefix)` rebinds materials.
7. **Check** with `capture_viewport` at one camera position for each state you compare: capture both variants
   before moving the camera, never all of one and then all of the other.

## Traps

| Trap | What to do |
|---|---|
| Stale bounds after a variant switch | the tools measure with a fresh bounds cache each call; a script that keeps a `BBoxCache` must `Clear()` it |
| A switch meant to stay is gone after `save_scene` | the session layer, the default, is never saved: `save_scene` names what it left out. Clear it (`variant_name=""`), then switch again with `layer="edit_target"` |
| `layer="edit_target"` refused | the session layer holds a selection for that set, which would hide it: clear it with `variant_name=""` first |
| Edits inside a variant land on the root layer | Usd-level APIs ignore the variant edit context: a script uses the `Sdf` layer API |
| A layer Kit already holds for a path | never `Clear()` it: if the open stage uses it, the scene empties. A script writes a file from an in-memory layer with `Export`, and calls `Reload(force=True)` on a held layer only when `stage.GetUsedLayers()` lacks it and `layer.dirty` is false (without `force`, a file written in the second it was loaded looks unchanged); the tools refuse to write a file the open stage has loaded |
| `prim.SetActive()` in a script moves the camera | Kit may frame the prim again: avoid it in scripts |
| `stage.Flush()` | does not exist in OpenUSD |
