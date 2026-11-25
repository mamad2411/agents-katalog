---
name: computing-feature-mating-poses
description: Computes approach, engaged, and mate TCP poses from a held feature in the hand and a fixture feature, resolving free mate symmetries from the current robot pose without executing motion. Use when a held loop must go over a shaft or hook, or a held shaft or tip must enter an aperture, and explicit approach, engaged, and mate poses are needed for planning.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: planning, tags: [fixture, insertion, hanging, geometry]}
gap:
  allowed_tools: [robot.get_ee_pose, geometry.compute_feature_mate]
  required_inputs: {held_feature_in_tcp: Se3Pose, fixture_feature: FunctionalFeature, relation: string, attached_object: AttachedObject}
  produces_outputs: {mate_pose: Se3Pose, approach_pose: Se3Pose, engaged_pose: Se3Pose, approach_axis: Vec3, seating_distance: float, minimum_clearance: float}
  exit_conditions:
    computed: A valid mate was computed.
    infeasible: The fixture feature has no directed axis or the feature dimensions cannot satisfy the relation.
  canonical_scripts:
    - compute_mate: scripts/compute_mate.py
  streaming: false
---

# computing-feature-mating-poses

This skill computes geometry only. When a relation has a free rotational
degree of freedom, it selects the equivalent mate closest to the current TCP
orientation to avoid arbitrary or unreachable reorientation. Its pre-contact
standoff encloses the complete attached-object sphere projection along the
fixture axis, preventing long held bodies from sweeping into the fixture.

## When to use

- A held loop or ring must be placed over a shaft, peg, or hook.
- A held shaft or tip must enter an aperture.
- The mating pose has rotational symmetry that should be resolved from the
  current robot pose.

Use `loop_over_shaft` for a loop or ring placed over a peg or hook. Use
`shaft_into_aperture` for a shaft entering an opening;
`tip_through_aperture` and `insert_through` are accepted aliases. The skill
checks that the relevant inner and outer dimensions have sufficient clearance:
for `loop_over_shaft` the held `radius_inner` against the fixture
`radius_outer`, for apertures the held `radius_outer` against the fixture
`radius_inner`.

For `loop_over_shaft`, describe the fixture at its distal tip with an axis
pointing outward from the mounting surface, `radius_outer`, and the observed
`usable_length` from tip toward the mount. The skill uses these dimensions to
center the shaft inside the loop during crossing, travel to a stable interior
shaft position, and then seat the loop without requiring an object-specific
target point. `crossing_lift_m` (default 0) raises the approach and engaged
poses vertically by that amount after centering, so a long held body that
settles in the hand between observation and crossing still clears the tip;
the mate pose is unaffected. It applies when `usable_length` is declared.

For apertures, the fixture axis points into the opening. The approach is
mirrored onto the free side of the mate, and `insertion_depth` (when the
fixture declares it) moves the engaged and mate poses that far into the
opening.

## Outputs

- `approach_pose` is a collision-free standoff before fixture engagement.
- `engaged_pose` crosses the distal tip far enough for the loop to surround the
  shaft, or enters the aperture.
- `mate_pose` places the loop farther along the usable shaft and seats it, or
  seats the shaft at the requested depth.
- `seating_distance` and `minimum_clearance` describe the computed mate.

## Boundaries

- This skill computes poses but does not plan or execute robot motion.
- Inputs describe functional geometry and a typed relation, not object names.
  Object-specific corrections (a settling offset measured for one tool) enter
  through `crossing_lift_m`, supplied by the graph.
- Execute the result with `planning-held-object-motion` and the corresponding
  motion-execution skills.
