---
name: grasping-direct-ik
description: Direct IK align-then-descend grasping. The gripper pre-rotates to
  the grasp orientation at a safe height ABOVE the target before descending
  straight down, avoiding the twist-while-closing failure mode of a blended
  rotate+descend. The grasp rotation is rebuilt so the hand's declared closing
  axis (robot.describe_gripper, composed by robot.grasp_frame) closes across the
  target's short horizontal axis, and the hover clearance is the hand's own
  (robot.describe_workspace) unless the workflow pins it. Use when no
  trajectory planner (curobo) is deployed or the scene is uncluttered enough
  that a straight-line approach is safe.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: grasping, tags: [grasping, manipulation, direct-ik]}
gap:
  requires: {connector: [robot.describe_workspace, robot.describe_gripper, robot.grasp_frame]}
  allowed_tools:
    - geometry.top_down_grasp_candidates
    - robot.go_to_pose
    - robot.go_to_pose_cartesian
    - robot.get_ee_pose
    - robot.open_gripper
    - robot.close_gripper
    - robot.describe_workspace
    - robot.describe_gripper
    - robot.grasp_frame
    - curobo.plan_to_pose
  exit_conditions:
    grasped: Object held in the gripper after `close`.
    failed: Any failure during the grasp attempt — planning failure or trajectory execution error (a raise to `on_error`). Coordinator routes to abort.
  required_inputs:
    target_obb: OrientedBoundingBox
  hard_rules:
    - >
      Use `geometry.top_down_grasp_candidates` (returns
      `candidates: {poses: list[Se3Pose]}`), NOT
      `geometry.top_down_grasp_from_obb` (single bare pose). The downstream
      refine / align-pose construction assumes `compute_grasp.candidates.poses.0`
      exists.
    - >
      The `align_pose` descends straight down with the gripper pre-rotated.
      DO NOT skip the `compute_align` + `rotate_align` states — a direct
      go_to_pose to the grasp pose blends rotation and descent and twists the
      gripper against the object.
    - >
      `descend` targets the SAME pose `compute_align` was given
      (`refine_grasp.grasp_pose` when `refine_grasp` is present, else
      `compute_grasp.candidates.poses.0`). Feeding `compute_align` one pose and
      `descend` another re-introduces the twist the hover exists to avoid.
    - >
      Do NOT add a `verify_gripper_grasp` node — there is no such skill;
      postcondition verification is a `validate=True` checkpoint. Express "the gripper is holding the target after close" as a
      `validate=True` checkpoint (`target_held`). See `## Checkpoints` below.
  canonical_scripts:
    - compute_align_pose: scripts/compute_align_pose.py
    - refine_top_down_grasp: scripts/refine_top_down_grasp.py
    - execute_grasp_align: scripts/execute_grasp_align.py
    - plan_to_pose: scripts/plan_to_pose.py
  references:
    - title: Why pre-rotate-then-descend instead of blended rotate+descend?
      path: references/design_align_then_descend.md
  streaming: false
---

# grasping-direct-ik

Direct-IK grasp: rotate the gripper to grasp orientation at a safe height
above the target, then descend straight down, then close. No trajectory
planner — works on platforms where CuRobo is not deployed, or in
uncluttered scenes where planning is overkill.

Nothing here is written for one hand. The grasp rotation is composed by the
connector's `robot.grasp_frame` from the hand's measured approach and closing
axes, the fingertip floor and the hover clearance come from
`robot.describe_gripper` / `robot.describe_workspace`, so the same subgraph
grasps the same way on a hand that closes along tool-local x and on one that
closes along tool-local y.

## When to use

- The `curobo` tool bundle is not deployed (no collision-aware planner
  available).
- The scene is uncluttered enough that a straight-line approach is safe.

## When NOT to use

- Cluttered scenes where the arm must thread between obstacles. Prefer
  `grasping-with-planner` if available.

## Recommended subgraph state flow

The subgraph state machine the agent generates should look like (7 states):

```text
open → compute_grasp → refine_grasp → compute_align → rotate_align → descend → close → grasped
```

(`grasped` is the success-marker `noop` from `sg.add_exit("grasped")`,
with an edge to `END`.)

State details:

1. **`open`** — `type: tool`, `tool: "robot.open_gripper"`, `inputs: { settle_steps: 40 }`.
2. **`compute_grasp`** — `type: tool`, `tool: "geometry.top_down_grasp_candidates"`,
   `inputs: { obb: Ref("in.target_obb") }`.
3. **`refine_grasp`** — `type: script`, file
   `scripts/<sg>/refine_top_down_grasp.py` (from this bundle's
   `canonical_scripts`). Inputs:
   `grasp_pose = Ref("compute_grasp.candidates.poses.0")`,
   `target_obb = Ref("in.target_obb")`. Returns `grasp_pose`: the candidate
   with its rotation rebuilt so this hand's closing axis lies across the
   OBB's short horizontal axis (`robot.describe_gripper` +
   `robot.grasp_frame(approach=-z, close_heading_deg)`), and its Z raised to
   the fingertip floor (`support_z + finger.reach_m + finger.clearance_m`)
   when the hand states its finger envelope. Keep this state: the candidate
   fan is world-aligned and a thin object's centred grasp jams the jaws on
   the table without the floor.
4. **`compute_align`** — `type: script`, file
   `scripts/<sg>/compute_align_pose.py`. Inputs:
   `grasp_pose = Ref("refine_grasp.grasp_pose")`,
   `target_obb = Ref("in.target_obb")`, optionally `clearance` (a literal in
   metres). Returns `align_pose` at the grasp XY and rotation, with
   `z = max(obb_top, grasp_z) + clearance`. Omit `clearance` (or pass `0`)
   and the script asks `robot.describe_workspace` for `align_clearance_m` —
   the hand's own envelope above the fingertips. Pin it (e.g. `0.12`) when
   the *held* object is what needs the room, such as a long tool that will
   hang below the fingertips on the way up.
5. **`rotate_align`** — `type: tool`, `tool: "robot.go_to_pose"`,
   `inputs: { pose: Ref("compute_align.align_pose") }`.
6. **`descend`** — `type: tool`, `tool: "robot.go_to_pose"`,
   `inputs: { pose: Ref("refine_grasp.grasp_pose") }` — the same pose
   `compute_align` was given, so hover and grasp share one rotation.
7. **`close`** — `type: tool`, `tool: "robot.close_gripper"`, `inputs: { settle_steps: 60 }`.
   Edge directly from `close` to the `grasped` success marker; the
   subgraph's `on_error: "failed"` catches any raise from earlier steps.
   Whether the gripper actually closed on the object is checked by the
   `target_held` postcondition checkpoint (see `## Checkpoints`), NOT by
   a re-check-and-raise node (none such exists).

   ```json
   "edges": [ ..., ["close", "grasped"], ["grasped", "END"] ],
   "conditional_edges": {},
   "exit": { "router_field": null, "success_values": ["grasped"] },
   "on_error": "failed"
   ```

   The lift onto a safe carry height is handled by the next
   `transporting-objects` subgraph (its `waypoint_move` script lifts before
   lateral motion); do NOT add a lift step here.

`scripts/<sg>/plan_to_pose.py` is the optional planned variant of a single
leg: it calls `curobo.plan_to_pose` from the observation's joint state to a
target pose and returns the `trajectory` (raising `PlanningFailed` when the
planner refuses) for a platform that deploys CuRobo as a fast single-pose IK
fallback without the goalset grasp planner.

## Hard rules

1. Use `geometry.top_down_grasp_candidates` (returns
   `candidates: {poses: list[Se3Pose]}`), not
   `geometry.top_down_grasp_from_obb` (single bare pose). The refine and
   align-pose constructions assume `compute_grasp.candidates.poses.0` exists.
2. The `align_pose` descends straight down with the gripper pre-rotated.
   Do NOT skip the `compute_align` + `rotate_align` states — a direct
   `robot.go_to_pose` to the grasp pose blends rotation and descent and
   twists the gripper against the object.
3. `descend` uses the pose `compute_align` was given (`refine_grasp.grasp_pose`).
   Never descend to the raw candidate after hovering at the refined rotation.

## Required end states

| End state | Meaning |
|---|---|
| `grasped` | Gripper has closed on the object after the descend. Route to next subgraph (typically `transporting-objects`). |
| `failed` | Any grasp-attempt failure: planning failure or trajectory execution error (a raise to `on_error`). Coordinator routes to abort. Lives only in `on_error` — never declare a `failed` node. |


## See also

- `references/design_align_then_descend.md` — why pre-rotate-then-descend
  beats blended rotate+descend.
- `scripts/refine_top_down_grasp.py` — the close-axis rotation and fingertip
  floor, read off the live hand.
- `scripts/compute_align_pose.py` — the canonical align-pose construction.
- `scripts/plan_to_pose.py` — the optional CuRobo single-pose leg.
