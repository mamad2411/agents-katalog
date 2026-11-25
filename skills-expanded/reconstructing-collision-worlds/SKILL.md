---
name: reconstructing-collision-worlds
description: Reconstructs a planner collision world from calibrated RGB-D views alone, excluding the grasp target, the robot, and a perceived fixture mask, dropping depth-edge slivers and invalid-depth sheets, and carving the free space an intentional-contact goal needs as an approach tube along a fixture axis or a corridor through a lid aperture. Use when a held-object motion must be planned against obstacles no simulator or CAD scene supplies, before registering the object and planning the carry.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: perception, tags: [collision-world, rgb-d, motion-planning, reconstruction]}
gap:
  requires: {connector: [motion.get_robot_collision_spheres]}
  allowed_tools:
    - sam3.segment_text
    - motion.get_robot_collision_spheres
    - geometry.build_world_config
  required_inputs:
    observation: Observation
    target_mask: Mask
  produces_outputs:
    world_config: WorldConfig
    strategy: string
  exit_conditions:
    built: A scene mesh set with the goal's free space carved was produced.
    failed: No camera was selected or the reconstruction produced no scene mesh (raised).
  canonical_scripts:
    - build_collision_world: scripts/build_collision_world.py
    - filter_mesh_components: scripts/filter_mesh_components.py
  streaming: false
---

# reconstructing-collision-worlds

Run once after perception and before grasping, with the same observation
the perception skills used. `build_collision_world` merges depth from the
selected views (`camera_names`, comma-separated; empty = all) into
alpha-shape meshes through `geometry.build_world_config` and returns a
`WorldConfig` plus the mesh names.

## What is excluded

- The grasp target by its perceived `target_mask` in `mask_camera_name`
  (default `overhead`), and by segmenting `target_description` in every
  other selected view so the object does not become a static obstacle where
  it later rotates in the hand.
- The robot, by text segmentation per view and by
  `motion.get_robot_collision_spheres` when the connector provides it (a
  connector without it falls back to the visual masks).
- A perceived `fixture_mask` from the mask camera, unless it is a full-frame
  placeholder that would erase the world.

## What is carved

- An approach tube of 55 mm radius along `outward_sign * fixture_axis`
  ending 12 mm behind `fixture_tip`, when both are given. Use
  `outward_sign: -1` for an axis that points into the fixture (an aperture's
  inward axis) and `1` for one that points toward its free side (a shaft).
- A vertical corridor of `corridor_radius` through `corridor_center` between
  `corridor_rim_z - 35 mm` and `+180 mm`, when the centre and a positive
  radius are given. The radius is the caller's measurement (for example a
  fraction of the perceived aperture radius); the script adds no margin.

## Cleaning and packing

Sparse, nearly zero-thickness sheets under 15 cm are dropped; components
lying entirely below `sheet_floor_z` or spanning more than
`sheet_max_extent_m` are invalid-depth returns and are dropped too (0
disables either gate). `voxel_size` trades surface ripple for detail.
`pack_meshes: true` folds every component into one `perceived_scene` mesh
for planners whose scene cache admits few named obstacles.

## Boundaries

- No simulator state, CAD model, or fixed world coordinate is read.
- The script raises when no mesh survives; the graph routes that to
  `failed`.
