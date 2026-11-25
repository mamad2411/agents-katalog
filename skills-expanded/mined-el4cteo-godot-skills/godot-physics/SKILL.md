---
name: godot-physics
description: Physics in Godot 4.7 (2D and 3D, Jolt default) - choosing body types, CharacterBody movement and floors/slopes/platforms, RigidBody forces and freezing, Area triggers, collision layers/masks, raycasts and shape queries, physics interpolation, ragdolls (PhysicalBoneSimulator3D), joints, Jolt differences and settings. Use for movement, collisions, triggers, projectiles, vehicles or ragdolls.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Physics (4.7)

Check the engine first: `project_inspect.py` → `physics_3d`. **New 4.6+ projects use Jolt.** Older ones may still run GodotPhysics3D (`DEFAULT`). 2D always uses Godot's 2D engine.
Code that touches physics goes in `_physics_process` (fixed tick, `physics/common/physics_ticks_per_second`, default 60).

## Choose the body
| Body | Use for | You control |
|---|---|---|
| `CharacterBody2D/3D` | players, NPCs, anything with scripted movement | `velocity`, then `move_and_slide()` |
| `RigidBody2D/3D` | crates, debris, balls, physics props | forces and impulses (`apply_central_impulse`) or `_integrate_forces(state)` |
| `AnimatableBody2D/3D` | moving platforms, doors, elevators | position via AnimationPlayer or a tween (`sync_to_physics`) |
| `StaticBody2D/3D` | level geometry (`constant_linear_velocity` for conveyors) | nothing |
| `Area2D/3D` | triggers, hitboxes, pickups, gravity and wind zones | signals and overlap queries |
Never move a RigidBody by setting `position` each frame. Use forces, `freeze`, or `PhysicsServer3D.body_set_state` for teleports.

## CharacterBody essentials
- Gravity: `velocity += get_gravity() * delta` reads Area overrides too. Then call `move_and_slide()`, which takes no arguments in 4.x.
- Floors: `up_direction`, `floor_max_angle`, `floor_snap_length` (raise it for stairs and ramps), `floor_stop_on_slope`, `floor_constant_speed`. Also `is_on_floor/wall/ceiling()` and `get_floor_normal()`.
- Moving platforms: `platform_on_leave` (keep or drop the platform's velocity). Riding works automatically on AnimatableBody and RigidBody.
- Collisions: loop `get_slide_collision_count()` → `get_slide_collision(i).get_collider()`, for example to push rigid bodies (see the reference).
- Stairs: Jolt and GodotPhysics have no automatic step-up. Use small ramps or a capsule plus snap, or a step-up raycast routine.
- Use a capsule collider for characters. Boxes snag on edges.

## Layers and masks
- **Layer** means "what I am". **Mask** means "what I scan for". Name the layers in Project Settings → Layer Names (`project_inspect.py` lists them).
- In code: `set_collision_layer_value(3, true)` and `set_collision_mask_value(2, false)` use 1-based layer numbers. Exports: `@export_flags_3d_physics var mask := 1`.
- A typical scheme: 1 world, 2 player, 3 enemies, 4 player hitbox, 5 enemy hurtbox, 6 pickups, 7 interactables. Projectiles only mask what they can hit.

## Queries
- Use `RayCast3D`/`ShapeCast3D` nodes for persistent checks (ground, line of sight, interaction). Call `force_raycast_update()` for an immediate result within the same frame.
- One-off checks: `get_world_3d().direct_space_state.intersect_ray(PhysicsRayQueryParameters3D.create(from, to, mask, [self_rid]))` returns a dictionary (`position`, `normal`, `collider`, `rid`, `face_index`), or empty on a miss. Run it only in `_physics_process`.
- Mouse picking in 3D: `camera.project_ray_origin(mouse)` and `project_ray_normal`, then the ray query above. Control nodes must not swallow the event first (`mouse_filter`).
- `intersect_shape`, `cast_motion` and `get_rest_info` work for area-of-effect and sweeps.

## Physics interpolation (smooth at any frame rate)
Turn on `physics/common/physics_interpolation`. Move and rotate physics-driven objects only in `_physics_process`. After a teleport, call `reset_physics_interpolation()`. Cameras that follow interpolated targets should follow in `_process`, or use `get_global_transform_interpolated()`.

## Ragdolls (3D)
Use Skeleton3D → `PhysicalBoneSimulator3D` (4.3+) → `PhysicalBone3D` children, created with the Skeleton3D menu "Create Physical Skeleton". Toggle with `physical_bones_start_simulation()`/`physical_bones_stop_simulation()`, and use `influence` to blend with animation. Active ragdolls should be driven by the simulator, not by moving the bones yourself.

## Jolt specifics (default in new projects)
- Better stacking, performance and determinism than GodotPhysics. `Area3D` reports overlaps with SoftBody3D (4.7) and static bodies.
- Unsupported joint parameters (bias, softness, relaxation and limit softness/restitution) print warnings. Single-body joints treat the body as `node_b` (setting `physics/jolt_physics_3d/joints/world_node`).
- `WorldBoundaryShape3D` has a limited effective size (`limits/world_boundary_shape_size`), and its `plane.d` sign flipped in 4.7. Prefer a big box for floors.
- Ray `face_index` needs `queries/enable_ray_cast_face_index`. Kinematic contacts need `simulation/generate_all_kinematic_contacts`, which costs performance.
- Tune limits for large worlds: `limits/max_bodies`, `max_body_pairs` and `max_contact_constraints`.

## Fast objects
Bullets and projectiles: use a raycast from the last to the current position each tick (hitscan), or `RigidBody3D.continuous_cd = true`. Thin walls plus fast bodies tunnel otherwise.

Controllers, interaction, pushing, queries and ragdoll code (compiled by the tests): [references/patterns.md](references/patterns.md)
