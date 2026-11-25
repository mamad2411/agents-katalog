---
name: godot-3d-gameplay
description: Building 3D games in Godot 4.7 - third-person and orbit cameras (SpringArm3D), camera-relative movement, lock-on, top-down/RTS/isometric cameras, GridMap + MeshLibrary levels, CSG blockout and baking, modular kit import hints, Path3D rails, interactables, spawners, world-space UI, large worlds and LOD. Use for 3D player controllers, cameras or level building.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# 3D Gameplay (4.7)

This skill covers how a 3D game *plays*: controllers, cameras, levels. Rendering is `godot-3d-rendering`, bodies and raycasts are `godot-physics` (it has the first-person controller), animation blending is `godot-animation`.

## Scene layout that scales
```
Player (CharacterBody3D)            # movement, script
├─ CollisionShape3D (capsule)
├─ Model (Node3D)                   # rotate this to face movement, not the body
│  └─ character.glb (AnimationTree lives here)
└─ CameraRig (Node3D, top_level)    # follows the player in _process, owns the yaw
   └─ Pitch (Node3D)
      └─ SpringArm3D                # camera collision
         └─ Camera3D
```
- `top_level = true` on the rig keeps the camera from inheriting the body's rotation and physics jitter. Follow `player.get_global_transform_interpolated()` when physics interpolation is on.
- Turn the **Model**, not the body, so the collider and camera stay stable. Rotate with `lerp_angle` or `Basis.slerp`.
- Keep gameplay in the root script and expose `@export` tuning (speed, acceleration, jump, sensitivity).

## Camera-relative movement (third person)
`input := Input.get_vector("move_left", "move_right", "move_forward", "move_back")` then `dir := (camera_yaw_basis * Vector3(input.x, 0, input.y)).normalized()`. Use the rig's **yaw** basis only (no pitch) so looking down doesn't slow you. Accelerate with `move_toward` for grip, lerp toward zero for slide.

## Cameras
| Style | Recipe |
|---|---|
| Third-person orbit | yaw on the rig, pitch on a child (clamp −70°..60°), `SpringArm3D` (`spring_length`, `margin`, sphere `shape` radius 0.2–0.3) |
| Over-the-shoulder aim | tween the spring length and `Camera3D.h_offset`, lower `fov` |
| Lock-on | the rig looks at the midpoint of the player and target; the player strafes facing the target |
| Top-down / ARPG | fixed pitch −50..−60°, smooth follow, mouse picking for aiming (see `godot-physics`) |
| Isometric / tactics | `projection = PROJECTION_ORTHOGONAL`, `size` = zoom, rotate 45° yaw, ~−35° pitch |
| RTS | the rig moves on XZ (WASD, edge pan), the wheel changes height or `size`, clamp to map bounds |
| Rail / cinematic | `PathFollow3D` on a `Path3D` with `progress` driven by a tween or AnimationPlayer |
- `SpringArm3D` must not hit the player: exclude it with `add_excluded_object(player.get_rid())` or leave the player layer out of `collision_mask`.
- Mouse look in `_unhandled_input` (`InputEventMouseMotion.relative`), stick look in `_process` (multiply by `delta`). Don't mix them in one place.
- Several cameras: call `make_current()` on the one you want. Blending between cameras needs a tween of one camera's transform (or the Phantom Camera addon).
- Screen shake and FOV kicks: `godot-game-feel`.

## Levels
**GridMap** (modular 3D tiles):
1. Build a scene with one `MeshInstance3D` per tile, each with a `StaticBody3D` + `CollisionShape3D` child (and an optional `NavigationRegion3D`). Then use **Scene → Export As → MeshLibrary**. The 4.7 MeshLibrary editor (bottom panel) edits items, previews and undo.
2. `GridMap.mesh_library`, `cell_size` = tile size, and the `cell_center_*` flags to match pivots.
3. Code: `set_cell_item(Vector3i, item, orientation)` with `orientation = get_orthogonal_index_from_basis(basis)`, `get_cell_item`, `get_used_cells_by_item`, `local_to_map`/`map_to_local`.
4. Navigation: `bake_navigation = true` uses the item navmeshes, or bake a `NavigationRegion3D` over the GridMap (`godot-navigation-ai`).
**CSG** (`CSGBox3D`, `CSGCombiner3D`, `CSGPolygon3D`, `operation = union/subtraction/intersection`) is for blockout and prototypes. It's slow to rebuild at runtime. For shipping, call `bake_static_mesh()` + `bake_collision_shape()` (or the editor's CSG → Bake Mesh / Collision). `use_collision` on the root only. 4.7 adds `autosmooth`/`smoothing_angle`.
**Modular kits from Blender (.glb)**: name suffixes create nodes on import: `-col` (mesh + static collision), `-colonly` (collision only), `-convcolonly` (convex), `-navmesh`, `-rigid`, `-noimp` (skip). Prefer `-colonly` boxes over trimesh colliders for performance.

## Gameplay objects
- **Interactables**: an `interact(actor)` method plus group `interactable`. Find them with a `ShapeCast3D` or `RayCast3D` from the camera (`godot-physics` has the prompt code). Show a `Label3D` or a screen-space prompt.
- **Pickups/triggers**: `Area3D` (`body_entered`), with masks set so only the player layer triggers them.
- **Doors, lifts, moving platforms**: `AnimatableBody3D` moved by AnimationPlayer/tween or `PathFollow3D` so riders get carried.
- **Spawners**: `Marker3D` points, `PackedScene.instantiate()`, then `add_child` to a level container **before** setting `global_position`, or set `position` relative to the container. Pool bullets and debris (`godot-performance`).
- **Checkpoints/respawn**: store a `Transform3D`, teleport with `reset_physics_interpolation()`.
- **World-space UI**: `Label3D`/`Sprite3D` with `billboard`, or 2D UI positioned with `camera.unproject_position(p)` (hide when `camera.is_position_behind(p)`).
- **Vehicles**: `VehicleBody3D` + `VehicleWheel3D` (arcade cars), or a RigidBody3D with raycast suspension for more control.

## Big worlds
- Visibility ranges (`GeometryInstance3D.visibility_range_begin/end` + fade) for HLOD; `OccluderInstance3D` for indoor culling; automatic mesh LOD is on by default for imported meshes.
- Precision: past ~10 km from the origin, jitter appears. Either shift the world origin (move everything back when the player passes a threshold) or use a double-precision engine build.
- Stream areas with `ResourceLoader.load_threaded_request()` (`godot-performance`). Terrain: the Terrain3D addon (1.1, Godot 4.5+) or a heightmap mesh with `HeightMapShape3D` (`godot-procedural`).

Third-person controller and camera rig, lock-on, top-down aiming, RTS camera, GridMap painting, CSG baking, rail camera and health bars (compiled by the tests): [references/patterns.md](references/patterns.md)
