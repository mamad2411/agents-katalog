---
name: godot-navigation-ai
description: Pathfinding and game AI in Godot 4.7 (2D and 3D) - NavigationRegion/NavigationAgent, navmesh baking at runtime, avoidance, links and obstacles, NavigationServer queries, AStarGrid2D/AStar3D for grids and graphs, enemy state machines, behavior trees, utility AI, perception (sight, hearing), LimboAI and Beehave. Use for enemies, NPCs, pathfinding or AI behavior.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Navigation and AI (4.7)

Navigation nodes and servers are marked **experimental** in 4.7: the API works, but check names with `api_lookup.py` (e.g. `NavigationAgent3D`), never from memory. 2D has its own server since 4.5 (`NavigationServer2D`).

## Pick the tool
| Need | Use |
|---|---|
| Characters walking on free-form 2D/3D levels | `NavigationRegion2D/3D` (navmesh) + `NavigationAgent2D/3D` per unit |
| Square/hex-like grids: tactics, roguelikes, tower defense | `AStarGrid2D` (no navmesh, no baking) |
| Waypoint graphs, road networks, flying nodes, room graphs | `AStar3D`/`AStar2D` with your own points |
| Tile levels | `TileMapLayer` with navigation polygons on tiles (`navigation_enabled`) or bake a `NavigationRegion2D` over it |
| Jumps, ladders, teleports, doors between regions | `NavigationLink2D/3D` (start/end, `bidirectional`, costs) |
| Moving things others must avoid | `NavigationObstacle2D/3D` (`avoidance_enabled`; `affect_navigation_mesh`/`carve_navigation_mesh` for baking) |

## Navmesh setup and baking
- 3D: add `NavigationRegion3D` → new `NavigationMesh` → set `agent_radius`, `agent_height`, `agent_max_climb`, `agent_max_slope` to match your character → Bake. `cell_size`/`cell_height` must match the map (`navigation/3d/default_cell_size`) or you get edge-merge warnings.
- Source geometry: `geometry_parsed_geometry_type` = meshes, static colliders or both; `geometry_source_geometry_mode` = children of the region, or a group (`geometry_source_group_name`). Colliders are cheaper to parse than visual meshes.
- 2D: `NavigationRegion2D` → `NavigationPolygon`; draw an outline or bake from colliders/meshes; `agent_radius` shrinks it.
- Runtime rebake (doors, destructible walls, procedural levels): `region.bake_navigation_mesh()` (threaded by default; listen to `bake_finished`). For many chunks use `NavigationServer3D.parse_source_geometry_data()` on the main thread, then `bake_from_source_geometry_data_async()`. Parsing must happen on the main thread; baking can be threaded.
- Several regions merge when their edges overlap or are within `edge_connection_margin`. Use `navigation_layers` (bitmask) for unit types: e.g. layer 1 ground units, layer 2 large units, layer 3 swimmers.
- `enter_cost`/`travel_cost` on regions and links make paths prefer or avoid areas (roads cheap, swamp expensive).

## Agent loop (the part people get wrong)
1. Set `agent.target_position` when the goal changes (not every frame; each set re-queries the path).
2. Every physics frame: `if agent.is_navigation_finished(): return`, then `next := agent.get_next_path_position()` and steer toward it.
3. Without avoidance: set `velocity` and `move_and_slide()`. With avoidance: assign the desired velocity to `agent.velocity`, then move in the `velocity_computed(safe_velocity)` handler.
4. **The map is empty on the first physics frame.** Await one frame (`await get_tree().physics_frame`) or check `NavigationServer3D.map_get_iteration_id(agent.get_navigation_map()) > 0` before the first query.
- `path_desired_distance`/`target_desired_distance`: raise them if agents orbit waypoints. `path_height_offset` (3D) fixes agents whose origin is far above the navmesh.
- Signals: `target_reached`, `navigation_finished`, `waypoint_reached`, `link_reached` (play a jump or climb animation, then continue).
- `is_target_reachable()` tells you when the final position isn't the target (blocked goal). `get_final_position()` is where the agent will stop.
- Avoidance (RVO) only steers velocities; it never changes the path. Tune `radius`, `neighbor_distance`, `max_neighbors`, `time_horizon_*`, `max_speed`, `avoidance_layers`/`avoidance_mask` and `avoidance_priority`. `use_3d_avoidance` only for flying units.
- Debug: Debug menu → Visible Navigation, and `agent.debug_enabled = true`.

## Direct queries (no agent)
- Paths: `NavigationServer3D.map_get_path(map, from, to, optimize, layers)`, or `query_path(NavigationPathQueryParameters3D, NavigationPathQueryResult3D)` for costs, region filters, `path_postprocessing` and simplification.
- Closest point: `map_get_closest_point(map, p)` snaps clicks and spawns to the navmesh. Random wander target: `map_get_random_point(map, layers, uniformly)`.
- Map RID: `get_world_3d().navigation_map` (3D), `get_world_2d().navigation_map` (2D).
- Thousands of units: skip agents, query paths for groups (flow-field or shared path to a leader) and use `AStarGrid2D` on a coarse grid. See `godot-performance`.

## AStarGrid2D essentials
`region = Rect2i(...)`, `cell_size`, `diagonal_mode`, `default_compute_heuristic`, then **`update()`** before use (after changing region, size or cell shape). Then `set_point_solid(cell)`, `set_point_weight_scale(cell, cost)`, `fill_solid_region(rect)`. Paths: `get_id_path(from, to, allow_partial_path)` (cells) or `get_point_path` (positions). `allow_partial_path = true` returns the closest reachable path when the goal is blocked. Not thread-safe: query from one thread.

## AI architecture
| Size of behavior | Use |
|---|---|
| 3–8 states (idle, patrol, chase, attack, flee) | enum state machine in the enemy script, or node states (see `godot-architecture`) |
| Reusable, designer-tweaked, many enemy types | behavior tree: LimboAI or Beehave, or the small tree in the reference |
| Many competing goals (needs, tactics, squad AI) | utility AI: score every action, pick the best, re-score on a timer |
- **Decide slowly, move every frame.** Run perception and decisions on a `Timer` (0.1–0.5 s, randomized per unit to spread load); keep steering in `_physics_process`.
- Perception: sight = distance check, then angle (`forward.dot(dir) > cos(half_fov)`), then one raycast for line of sight (cheapest first). Hearing = an autoload/global signal `noise_made(position, radius)` that nearby AIs check. Keep a `last_known_position` and search there after losing the target.
- Use groups (`get_tree().get_nodes_in_group(&"player")`) or an injected target. Don't hard-code node paths across scenes.
- Animation follows AI state; AI never waits on animation timing except through signals (`animation_finished`) or `AnimationTree` conditions.

## Addons (install with `godot-addons`)
- **LimboAI** (1.8.x for 4.6+/4.7): behavior trees + hierarchical state machines with an editor, debugger and blackboard. It ships as a GDExtension (GDScript/C# usable) or an engine module.
- **Beehave** (2.9.x supports 4.7): behavior trees as nodes in the scene, pure GDScript, with a debug view.
Prefer plain code for small games; use an addon when designers edit trees or you have 10+ behaviors.

Agents, avoidance, runtime baking, grid A*, state machine, perception, behavior tree and utility AI code (compiled by the tests): [references/patterns.md](references/patterns.md)
