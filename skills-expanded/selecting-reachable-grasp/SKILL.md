---
name: selecting-reachable-grasp
description: Walk a ranked list of candidate grasp poses and take the first the
  arm can actually reach — IK solves it, the solution lands where it was asked,
  and (where `sim.clearance` is available) the arm is clear of the scene there.
  Use after any propose rung. This is the fix for taking candidate 0 on faith
  and closing the jaws on nothing.
compatibility: requires gap>=0.1
metadata: {category: grasping, tags: [grasping, select, ik, cpu, sim-only]}
gap:
  requires: {connector: [motion.plan_joint, robot.describe_arm, sim.clearance]}
  allowed_tools:
    - robot.solve_ik
    - robot.describe_arm
    - motion.plan_joint
    - sim.clearance
  exit_conditions:
    selected: A pose the arm reaches, with the joint configuration that reaches it.
    none_reachable: No candidate solved. Route to another propose rung.
  hard_rules:
    - >
      A returned IK solution is NOT a solved pose. Backends return their best
      effort; check the position error before trusting it. This skill rejects a
      solve that lands more than 20 mm from the request, which is the
      difference between a grasp and a gesture near one.
    - >
      `robot.solve_ik` reaches a position and an approach direction and leaves
      the wrist ROLL free on any robot that does not declare `honour_roll`. For
      a grasp the roll IS the grasp, so an IK solve alone does not mean the arm
      can adopt the closing direction there. This skill checks it with
      `motion.plan_joint(orientation="lock")` and reads `rotation_error_rad`;
      do not switch `check_roll` off for a grasp.
    - >
      Pass `object_name` so the target is excluded from the clearance test.
      The whole point of a grasp is to approach the object, so counting it as
      an obstacle refuses every candidate.
    - >
      `corridor_checked: false` means the clearance gate did not run (it needs
      `sim.clearance`, which only the `full` tier has) — it does NOT mean the
      path is clear. Do not read a `selected` at `camera_only` as
      collision-checked.
    - >
      On `none_reachable`, route to a DIFFERENT propose rung. Re-running the
      same proposer with adjusted constants is the failure mode this stage
      split exists to prevent: the list did not fit the arm, and a nearby list
      will not either.
  canonical_scripts:
    - select_reachable: scripts/select_reachable.py
  streaming: false
---

# selecting-reachable-grasp

`poses` is a list of `Se3Pose`, best first -- a propose skill's `poses`
output, or the `poses` field of a `GraspCandidates`. It is declared here in
prose rather than under `required_inputs` because the registry has no name for
a bare list of poses, and a `GraspCandidates` is a dict the script does not take.

One strategy for the **select** stage: reachability, then clearance, first
match wins.

## Why this is its own skill

A proposer ranks by the object's geometry, which is the only thing it knows.
Whether the *arm* can hold a pose is a different question, and entry 0 is
routinely the one it cannot. Nothing downstream notices — IK returns something,
the servo drives to it, and the jaws close on air. A study packet put it
exactly: *"gripper closed on nothing while grasping ring_spanner_19"*.

Taking the **first** that passes rather than the best: the list arrives ranked
by a proposer that knows things about the object this skill does not, and
re-ranking here would silently overrule it.

## When to use

- After every propose rung. There is no case where taking candidate 0 unchecked
  is better than walking the list.

## When NOT to use

- As a substitute for a collision-aware planner on the *carry*. This gates the
  grasp configuration, not the path to it. The two are different halves: a
  corridor test refuses a grasp whose descent goes through a shelf; a planner
  routes the carry around a beam. Neither substitutes for the other.

## Recommended subgraph state flow

```text
select → (selected | none_reachable)
```

A single script node. Inputs: `poses` (built from the proposer's stations and
`robot.grasp_frame`'s rotation), `arm_id`, `object_name`, `check_clearance`.
Router on `route`.

Downstream, execute the selection with
`motion.plan_linear(orientation="lock")` → `robot.execute_trajectory` so the
closing heading is actually held — `robot.go_to_pose` leaves the wrist roll
free and discards it.

## Required end states

| End state | Meaning |
|---|---|
| `selected` | `pose` and `joint_config`. Read `index` to see how far down the list it had to go, and `corridor_checked` to see whether clearance ran. |
| `none_reachable` | Nothing in the list solved. Route to another propose rung, not back to this one. |
