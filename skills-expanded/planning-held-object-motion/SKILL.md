---
name: planning-held-object-motion
description: "Plans the carry and engagement phases for an already-held rigid object: a clearance-first lift, the smallest feasible symmetry-equivalent reorientation, an orientation-locked transit above the fixture, or a direct plan to the approach pose; then a typed engagement or a straight linear insertion, optionally re-observing the held tip from the wrist first. Use when a held object must be brought to a fixture for insertion, hanging, packing, racking, or constrained sorting and an execution skill will run the resulting plans."
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: planning, tags: [motion-planning, held-object, clearance, insertion, hanging, packing, sorting]}
gap:
  requires: {connector: [motion.plan_joint]}
  allowed_tools:
    - robot.get_ee_pose
    - motion.plan_joint
    - sam3.segment_text
    - geometry.mask_to_world_points
  required_inputs:
    held_feature_in_tcp: Se3Pose
    fixture_feature: FunctionalFeature
    relation: string
    world_config: WorldConfig
    attached_object: AttachedObject
  produces_outputs:
    reorientation_plan: PoseSequence
    placement_plan: PoseSequence
  exit_conditions:
    planned: A carry plan or an engagement plan was produced.
    blocked: No feasible symmetry-equivalent held-object orientation was found, or the direct strategy was requested without an approach pose.
  canonical_scripts:
    - plan_clearance_motion: scripts/plan_clearance_motion.py
    - plan_feature_engagement: scripts/plan_feature_engagement.py
    - plan_linear_engagement: scripts/plan_linear_engagement.py
  streaming: false
---

# planning-held-object-motion

Turn a feature mate into safe phases for a held object:

```text
lift away from support
  -> rotate minimally in clear space
  -> translate above the fixture with orientation fixed
  -> approach and engage linearly
```

The skill plans; it does not move the robot or release the object. Follow it
with `executing-held-object-motion` to execute the carry plan and
`executing-feature-mating` to execute the engagement plan.

## Choosing the carry strategy

`plan_clearance_motion` takes `strategy`:

- `"clearance_first"` (default) derives a lift from the farthest attached
  sphere, selects the smallest reachable symmetry-equivalent rotation among
  eight roll candidates (each checked with `motion.plan_joint`), rotates while
  clear, and translates the aligned feature to a staging location on the free
  side of the fixture, `approach_clearance_m` along its axis. The staging
  location is derived from the fixture geometry and attached-object extent.
  `stage_outward_m` (default 0) shifts that location within the support
  plane away from the fixture toward the current hand — use it when a
  recessed opening is observed mostly at its far rim and the object should
  stage over the interior instead.
- `"direct"` escapes `escape_m` (default 6 cm) along the support normal as a
  `contact_transition` waypoint, then hands `approach_pose` to the executor as
  one `planned_joint` waypoint with `allow_start_contact` and three attempts.
  It calls no planner itself. Use it when the object is already clear of its
  support, the orientation change is small, and a single attached-object plan
  to the approach pose is appropriate; it requires `approach_pose`.

If uncertain, choose the clearance-first strategy for a large orientation
change or a long held object. Do not add arbitrary midpoint waypoints and do
not remove collision geometry to make direct planning succeed.

## Engagement

`plan_feature_engagement` converts the typed relation and the approach,
engaged, and mate poses into execution semantics. `loop_over_shaft` crosses the
shaft tip with a tracked `cartesian_cross` leg — stopping on first contact can
leave a loop balanced against the tip without enclosing the shaft — and then
seats with the bounded `contact_seat` servo; `feature_to_fixture` uses the
contact servo for both legs; aperture insertion uses `planned_linear`
waypoints that allow goal contact. The task graph therefore does not decide
ad hoc whether a contact servo is needed.

`plan_linear_engagement` plans a straight insertion from the fixture feature
alone: a `planned_joint` pre-contact pose `precontact_clearance_m` before the
opening and a `planned_linear` engaged pose `engagement_depth_m` past it, both
holding the current orientation. Give it `observation` (the current
`Observation`), `object_description` and `direction_marker_description` to
re-observe the held tip from the wrist first: when both the object and its
direction marker are visible, the endpoint of the object's principal axis
toward the marker replaces the carried feature position.

## Recommended skill sequence

1. Use `registering-held-objects` to obtain `held_feature_in_tcp` and
   `attached_object`.
2. Use `computing-feature-mating-poses` when explicit approach/engaged/mate
   poses are needed.
3. Select the carry strategy using the criteria above.
4. Execute the returned `reorientation_plan` with
   `executing-held-object-motion`.
5. Execute `placement_plan` with `executing-feature-mating`.

Waypoint modes are semantic: `contact_transition` leaves the initial support,
`planned_joint` is collision-aware free-space motion, `planned_linear` locks
orientation for a straight local leg, `cartesian_cross` is a tracked short
crossing, and `contact_seat` is the final intentional-contact servo.

## Boundaries

- Upstream perception supplies the held feature in TCP coordinates and the
  fixture pose/axis. Registration supplies attached-object collision geometry.
- Inputs describe functional geometry and a relation rather than an object
  class or task name; the graph chooses `strategy`, `stage_outward_m` and the
  re-observation descriptions.
- Free roll about the fixture axis is treated as symmetry. Candidates are
  checked for reachability and the smallest feasible TCP rotation is selected.
- `support_normal` may be supplied when the escape direction is known; it
  defaults to world up for a horizontal support surface.
- Relationship-specific clearances may be supplied by the graph when fixture
  depth is observable or specified. Conservative geometric defaults are used
  otherwise.
- The final crossing is linear and may allow goal contact. All earlier motion
  remains collision-aware free-space motion.
