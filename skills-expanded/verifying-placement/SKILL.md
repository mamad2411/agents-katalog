---
name: verifying-placement
description: Confirms from one RGB-D view that a released object went through an aperture, accepting either that it vanished into the container or that its visible centre lies below the rim within the opening's footprint, and routing not_placed when it is still visible above or beside the aperture. Use when an insertion-and-release must be checked without simulator state, after the release has completed.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: verification, tags: [placement, verification, aperture, rgb-d]}
gap:
  allowed_tools:
    - sam3.segment_text
    - geometry.mask_to_world_points
  required_inputs:
    observation: Observation
    object_description: string
    aperture_center: Vec3
    rim_z: float
  produces_outputs:
    verified: bool
    evidence: string
  exit_conditions:
    verified: The object is no longer visible, or its visible centre is below the rim within the aperture footprint.
    not_placed: The object is still visible above the rim or outside the aperture footprint, or too little depth was valid to confirm.
  canonical_scripts:
    - verify_placement: scripts/verify_placement.py
  streaming: false
---

# verifying-placement

Use once, after `executing-feature-mating` has released the object. Take a
fresh observation and call `verify_placement` with the aperture the fixture
perception measured (`aperture_center`, `rim_z`).

The script segments `object_description` in `camera_name`. Below
`score_min` the object is taken to have disappeared into the container,
which is `verified`. Otherwise its mask is back-projected and the median
must lie more than `depth_margin_m` below `rim_z` and within
`xy_tolerance_m` of the aperture centre in XY; anything else, including a
mask with fewer than `min_points` valid depth points, routes `not_placed`
with the evidence spelled out. The script never raises on a verdict.

## Boundaries

- Only meaningful for an opaque container after a completed release; an
  object still in the gripper would also "disappear" from an overhead view.
- No simulator query or object pose is read.
