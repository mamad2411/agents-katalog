---
name: executing-feature-mating
description: Executes a supplied feature-mating plan for an already-held rigid object - collision-aware planner legs tracked to millimetre precision, Cartesian servo for short corrections and fixture crossings, contact-controlled seating - then releases and retreats along the fixture axis or straight up. Use when the goal is a constrained mate such as a loop over a shaft, a shaft into an aperture, or a handle seated on a support; use transporting-objects for ordinary container drops.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: motion, tags: [motion, placement, insertion, fixtures, release]}
gap:
  requires: {connector: [motion.plan_to_pose, motion.plan_linear, robot.move_cartesian_until_contact, robot.wait_steps, robot.describe_arm]}
  allowed_tools:
    - robot.get_ee_pose
    - robot.execute_trajectory
    - robot.go_to_pose_cartesian
    - robot.move_cartesian_until_contact
    - robot.open_gripper
    - robot.wait_steps
    - motion.plan_to_pose
    - motion.plan_linear
  produces_outputs:
    final_pose: Se3Pose
    waypoint_count: int
    fallback_count: int
    registration_uncertainty_m: float
    released: bool
    retreat_pose: Se3Pose
  exit_conditions:
    seated: The feature-mating waypoint sequence completed; the object is engaged with the fixture and still held.
    released: The gripper opened at the mate and retreated clear of the released object.
    blocked: A planner refused an engagement waypoint, or a waypoint or release motion failed before completion.
  required_inputs:
    placement_plan: PoseSequence
  canonical_scripts:
    - execute_placement_plan: scripts/execute_placement_plan.py
    - release_and_retract: scripts/release_and_retract.py
  streaming: false
---

Both scripts also return a report -- `waypoint_reports` (one record per
waypoint) from `execute_placement_plan`, `release_report` from
`release_and_retract` -- stated here rather than under `produces_outputs`
because the type registry names no bare list or record. A `contact_profile`
(one per object kind) overrides the executor's tolerances one key at a time;
`arm_id` names the hand on a bimanual cell; `verify_cartesian` and
`measure_errors` turn on the TCP re-reads that fill the reports (they are
recorded tool calls and are off unless asked). `robot.describe_arm` is called
only under `verify_cartesian`, to learn whether the solver honours roll.

# executing-feature-mating

Execute a previously computed feature-mating plan for an already-grasped rigid
object, then release it. The upstream localization/planning node supplies
ordered poses; this skill does not locate a fixture or compute mating poses and
does not depend on object names, task names, simulator state, or evaluator
predicates.

Use this instead of `transporting-objects` when the goal is a constrained mate,
not a drop into a volume or onto a broad surface. Examples are putting a loop
over a rod, inserting a rod through a loop, or lowering a handle gap onto a
support point.

## Recommended subgraphs

```text
execute_placement_plan -> seated
release_and_retract    -> released
```

The two scripts are usually two subgraphs so the graph can settle, verify, or
re-observe between engagement and release; a single subgraph running both in
order is also valid.

### `execute_placement_plan`

Runs `scripts/execute_placement_plan.py` with
`placement_plan = Ref("in.placement_plan")`. The plan carries its collision
world and attached-object spheres, and every waypoint is a typed record
`{pose, mode, allow_start_contact?, allow_goal_contact?, contact_margin?}`:

- `planned_joint` — collision-aware transit via `motion.plan_to_pose`.
- `planned_linear` — orientation-locked straight leg via `motion.plan_linear`.
- `cartesian_cross` — a short local segment across a fixture mouth, driven by
  the robot's Cartesian servo so an incidental touch does not stop it.
- `contact_seat` — the final intended-contact leg via
  `robot.move_cartesian_until_contact`, which stops when the target is reached
  or measured TCP progress stalls.

Before each planned leg the script reads `robot.get_ee_pose`: a waypoint within
1.5 mm and 2 degrees is skipped (the planner would otherwise be asked for a
zero-motion problem its start-contact check can reject), and a `planned_joint`
correction of at most 3 cm with matching orientation is served through
`robot.go_to_pose_cartesian` rather than a fresh joint-space trajectory that
can make a loosely held object slip. Larger legs are planned with up to three
attempts (the sampled planner can miss a narrow corridor on one seed) and
executed with a 2 mm tracking tolerance and a 60-step-per-waypoint budget. A
planner refusal raises; route it through `on_error: blocked`. Output:
`final_pose: Se3Pose`, the last waypoint pose.

### `release_and_retract`

Runs `scripts/release_and_retract.py` with `final_pose` (the mate pose the
object was released at) and, for a fixture mate, `retreat_axis: Vec3` (the
fixture axis), `attached_object: AttachedObject` and `relation: string`. It
opens the gripper (`open_settle_steps`, default 80), retreats and then waits
`settle_steps` (default 120) so a freshly released object stops swinging before
the graph reports success.

- With `retreat_axis`: the retreat runs along the axis (reversed for
  `shaft_into_aperture`, `tip_through_aperture` and `insert_through`, where the
  feature went into the fixture) by `max(retract_m or 0.08, farthest attached
  sphere + 1 cm)` and lifts by half that distance so the open fingers clear the
  released object.
- Without `retreat_axis`: a plain vertical retreat of `retract_m` (or 0.08 m
  when unset), still never less than the attached extent plus 1 cm.

## Boundaries

- This skill does not infer fixture geometry or choose feature landmarks.
- Do not query `sim.*`, cameras, rewards, or goal predicates inside this skill.
- Preserve the waypoint order. Insertion plans encode clearance first, mating
  second, seating third; shortcutting between them can cross solid geometry.
- Never fall back to unchecked robot motion after a collision-aware planner
  rejects a waypoint.
- Use `transporting-objects` for bins, baskets, and unconstrained surface drops.
