---
name: godot-2d
description: 2D games in Godot 4.7 - pixel-art and HD setup, TileMapLayer (cells, terrains, custom data, runtime tiles, physics chunking), Parallax2D, Camera2D (limits, smoothing, shake), y-sort and z-index, 2D lights and normal maps, AnimatedSprite2D, one-way platforms, custom drawing, many-sprite performance. Use for platformers, top-down, tile-based or any 2D scene.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# 2D in Godot 4.7

Movement physics lives in `godot-physics`, UI in `godot-ui`, shaders in `godot-shaders-vfx`. Look up any API with `../godot-core/scripts/api_lookup.py`.

## Project setup
| Style | Settings |
|---|---|
| Pixel art | `rendering/textures/canvas_textures/default_texture_filter = 0` (Nearest); `display/window/stretch/mode = "viewport"`, `scale_mode = "integer"`, aspect `keep`/`expand`; base size small (for example 320×180 or 640×360); optionally `rendering/2d/snap/snap_2d_transforms_to_pixel = true` |
| HD 2D / UI-heavy | stretch mode `canvas_items` (the 4.7 default for new projects), aspect `expand`, base size 1920×1080 or 1280×720, Linear filter |
Never mix texel sizes in pixel-art games. Scale sprites by whole numbers only.

## TileMapLayer (TileMap is deprecated)
- Use **one `TileMapLayer` node per layer** (ground, walls, decoration), all sharing one `TileSet` resource. Old `TileMap` nodes convert through the TileMap panel's toolbox: "Extract TileMap layers".
- Code: `set_cell(coords, source_id, atlas_coords, alternative)`, `erase_cell`, `get_cell_source_id` (−1 means empty), `get_cell_atlas_coords`, `get_used_cells()`, `get_used_cells_by_id()`, `local_to_map(to_local(global_pos))`, `map_to_local(cell)`.
- Per-tile metadata: add custom data layers to the TileSet (`is_hazard: bool`, `cost: float`), then read them with `get_cell_tile_data(cell).get_custom_data("is_hazard")`.
- Autotiling: set up terrain sets in the TileSet, then call `set_cells_terrain_connect(cells, terrain_set, terrain)` or `set_cells_terrain_path`.
- Collision, navigation and occlusion come from the TileSet's physics, navigation and occlusion layers. Physics shapes are merged into chunks (`physics_quadrant_size`, default 16). Set it to 1 only if you need `get_coords_for_body_rid` per cell.
- For changes at runtime, set the cells, then `update_internals()` if you need them immediately. Per-cell runtime variations use `_use_tile_data_runtime_update` and `_tile_data_runtime_update` with `notify_runtime_tile_data_update()`.
- Large worlds: use chunked layers per region and free distant chunks. Thousands of `set_cell` calls in one frame stall, so spread them over several frames.

## Camera2D
- `position_smoothing_enabled` and `position_smoothing_speed` smooth the follow. Limits are `limit_left/top/right/bottom` (toggle them all with `limit_enabled`). `drag_*_enabled` adds a dead zone.
- Screen shake: animate `offset` (not `position`) with decaying noise. See the reference.
- Use one active camera per viewport (`make_current()`). Zoom uses `zoom` (Vector2: >1 zooms in).

## Parallax2D (replaces ParallaxBackground/Layer)
Add `Parallax2D` nodes anywhere, with a Sprite2D or TextureRect as child. Set `scroll_scale` (0 = static, 1 = moves with the world), `repeat_size` = texture size for infinite tiling, `repeat_times` for zoomed-out cameras and `autoscroll` for clouds. It follows the active Camera2D automatically.

## Drawing order
- `y_sort_enabled` on the parent sorts its children by Y (top-down games). Each child's sort origin is its own origin, so put sprite feet at y=0.
- `z_index` (relative to the parent unless `z_as_relative = false`) works across siblings. `CanvasLayer` handles HUD and backgrounds independently of the camera.
- `CanvasGroup` renders a subtree as one unit, which lets outline shaders and transparency apply to a whole character.

## Lights and atmosphere
`PointLight2D` (textured) and `DirectionalLight2D`, plus `LightOccluder2D` for shadows (TileSets can carry occluders). `CanvasModulate` darkens the scene. Normal and specular maps go through a `CanvasTexture` used as the sprite texture. Light2D is per-pixel, so keep lights overlapping any given sprite in the single digits on mobile.

## Sprites and animation
- `AnimatedSprite2D` + `SpriteFrames` handles frame animation (`play(&"run")`, `animation_finished`). Since 4.7, per-animation loop mode uses `SpriteFrames.set_animation_loop_mode`.
- Use `AnimationPlayer` when frames must sync with hitboxes, sounds or method calls. Keyframe the `frame` property of a `Sprite2D` with `hframes`/`vframes`.
- Sprite sheets: `Sprite2D.region_enabled` + `region_rect`, or `AtlasTexture`.

## Platformer specifics
- One-way platforms: `CollisionShape2D.one_way_collision = true`. 4.7 adds `one_way_collision_direction` (default `Vector2(0, 1)`). Drop through by briefly disabling the player's mask bit or raising the position.
- `CharacterBody2D` defaults to `MOTION_MODE_GROUNDED` for platformers. Use `MOTION_MODE_FLOATING` for top-down.
- Coyote time, jump buffering and variable jump height are in the reference.

## Many objects
Thousands of bullets or particles: `MultiMeshInstance2D` or GPU particles, or skip nodes entirely with `RenderingServer` canvas items and `PhysicsServer2D`. `VisibleOnScreenEnabler2D` pauses off-screen enemies. See `godot-performance`.

Patterns (platformer feel, top-down movement, camera shake, tile queries, custom draw), compiled by the tests: [references/patterns.md](references/patterns.md)
