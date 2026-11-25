---
name: executing-held-object-motion
description: Executes an ordered, collision-aware pose sequence for an already-grasped rigid object without releasing it - the escape from support, clear-space rotation, fixture transit and orientation-locked local legs of a carry plan, or only the free-space approach waypoint of a placement plan. Use when a held object must be carried or reoriented before insertion, mating, packing, or sorting, and use executing-feature-mating afterwards for the engagement and release.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: motion, tags: [motion, held-object, execution, reorientation, insertion, packing]}
gap:
  requires: {connector: [motion.plan_to_pose, motion.plan_linear]}
  allowed_tools:
    - motion.plan_to_pose
    - motion.plan_linear
    - robot.execute_trajectory
    - robot.go_to_pose_cartesian
    - robot.get_ee_pose
  produces_outputs:
    final_pose: Se3Pose
    approach_pose: Se3Pose
    fallback_count: int
    registration_uncertainty_m: float
  exit_conditions:
    reoriented: The held-object waypoint sequence completed while the gripper remained closed.
    reached: Only the first (approach) waypoint of a placement plan was executed; the object is held at the approach pose.
    blocked: A planner refused a waypoint, or a waypoint motion failed before the requested pose was reached.
  required_inputs:
    reorientation_plan: PoseSequence
  canonical_scripts:
    - execute_reorientation: scripts/execute_reorientation.py
    - execute_approach_only: scripts/execute_approach_only.py
  streaming: false
---

Both scripts also return a per-waypoint report (`waypoint_reports`,
`waypoint_report`), stated here because the type registry names no bare list
or record. An `execution_profile` (one per object kind) adds `speed_scale`, a
Cartesian fallback when the planner refuses, and -- for the approach -- a local
Cartesian shortcut and a goal-contact retry; `robot.get_ee_pose` is read only
under a profile (`execute_approach_only`) or `measure_errors`
(`execute_reorientation`), because the read is a recorded tool call. `arm_id`
names the hand on a bimanual cell and is absent from every call when unset.

# executing-held-object-motion

Execute motion for a rigid object that is already held. The skill preserves the
grasp: it does not open or close the gripper. Its input is an ordered
`PoseSequence` containing clearance, transit, and orientation poses.

## When to use

- Stand an elongated object upright before putting it through an opening.
- Turn a tool from a table grasp into a hanging or fixture-mating orientation.
- Align a keyed object before insertion.
- Reorient an item before constrained packing or sorting.
- Reach only the approach pose of a placement plan so the held object can be
  re-observed (wrist re-registration) before a tight engagement.

Do not use it for an ordinary bin drop when `transporting-objects` can lift,
translate, descend, and release directly.

## Recommended subgraphs

```text
execute_reorientation -> reoriented
execute_approach_only -> reached
```

`execute_reorientation` runs the canonical script with
`reorientation_plan = Ref("in.reorientation_plan")`. Each waypoint is a
typed record `{pose, mode, use_attachment?, max_attempts?, allow_start_contact?,
allow_goal_contact?, contact_margin?}`. It forwards the plan's `world_config`
and `attached_object` to every planned leg and never replaces a rejected
collision-aware plan with an unchecked move. Use `contact_transition` only for
the initial support escape (a plain Cartesian move); use `planned_joint` for
clear-space rotation/transit and `planned_linear` for an orientation-locked
straight leg. A plan-level `time_scale > 1` slows execution by resampling the
joint path; every planned leg is executed with a 60-step-per-waypoint budget
so a stuck waypoint does not stall the graph. Output: `final_pose: Se3Pose`,
the last waypoint's end-effector pose.

`execute_approach_only` takes `placement_plan: PoseSequence` (the plan that
`executing-feature-mating` will finish) and executes only its first waypoint
as a collision-aware `motion.plan_to_pose` leg with the plan's world and
attachment, retrying the sampled planner up to three times and tracking the
trajectory to 2 mm. It raises when the planner refuses (route to `blocked`).
Output: `approach_pose: Se3Pose`, the waypoint it reached, so the graph can
re-register the held object there and recompute the engagement.

## Boundaries

- Upstream geometry or perception determines the desired object orientation
  and sufficient clearance. This skill executes that typed request.
- The sequence must describe end-effector poses, not object poses.
- The skill never releases the object and never queries cameras, simulation
  state, task goals, evaluators, or reward.
- Full 3-DOF orientation changes require a robot IK backend that honors wrist
  roll. A position/approach-axis-only backend cannot reliably stand a syringe
  or long tool upright.
