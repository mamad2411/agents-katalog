---
name: proposing-short-axis-grasps
description: Propose top-down grasps whose jaws close ACROSS an elongated
  object's short axis, derived from its oriented box. Use when the object is
  longer than it is wide, as the first grasp-proposal rung — a handle, a
  spanner, a screwdriver, a bar, a laid-down bottle — where closing along the
  length would put the fingers down the object and meet them on each other.
  Declines when the short axis is wider than the hand opens, which is the
  signal to try `proposing-side-grasps` rather than to re-tune this one.
compatibility: requires gap>=0.1
metadata: {category: grasping, tags: [grasping, propose, geometric, cpu, sim-only]}
gap:
  requires: {connector: [sim.get_object_obb, robot.describe_gripper, robot.grasp_frame]}
  allowed_tools:
    - sim.get_object_obb
    - robot.describe_gripper
    - robot.grasp_frame
  exit_conditions:
    proposed: A closing heading and one or more stations along the long axis.
    declined: The short axis exceeds the jaw span. Route to another propose rung.
  required_inputs:
    target_obb: OrientedBoundingBox
  hard_rules:
    - >
      Do NOT pass `sim.get_object_obb`'s `grasp_yaw` to
      `robot.grasp_frame(close_heading_deg=…)`. `grasp_yaw` is the heading of
      the object's LONG axis; `close_heading_deg` is the direction the jaws
      close ALONG. They are ninety degrees apart and the mistake is silent —
      it validates, plans, executes, and closes the fingers down the length of
      the handle. Use this skill's `close_heading_deg` output, which is derived
      square to the long axis.
    - >
      The heading is inert under `robot.go_to_pose`, which reaches a position
      and an approach direction and leaves the wrist roll FREE. To make the
      closing direction real, plan with
      `motion.plan_linear(orientation="lock")` and run it through
      `robot.execute_trajectory`.
    - >
      Offer the stations to a selector; do not take `positions.0` on faith.
      The centre station is the best guess for a symmetric body and routinely
      wrong for an asymmetric one. See `selecting-reachable-grasp`.
  canonical_scripts:
    - propose_short_axis: scripts/propose_short_axis.py
  streaming: false
---

# proposing-short-axis-grasps

One strategy for the **propose** stage of a pick: a top-down grasp across the
narrow dimension of an elongated body.

## Why this is its own skill

A pick has stages — propose, select, approach, close — and each has more than
one strategy. Treating "grasping" as one indivisible thing is what leaves a
policy with a single approach and nowhere to go when it does not fit: it can
only jitter the numbers of a strategy that structurally cannot work. Proposing
is separated from selecting so that a refusal here (*"the short axis is wider
than the hand"*) is a **routable exit** to a different rung, not a failed
episode.

## When to use

- The target is longer than it is wide: a handle, spanner, screwdriver, bar.
- Top-down access is available.
- Any privilege tier. The box may come from `sim.get_object_obb` **or** from
  `geometry.compute_obb` over a segmented cloud — this skill cannot tell which,
  which is what makes it portable to the vision body.

## When NOT to use

- The top is blocked (a shelf, a lid) — use `proposing-side-grasps`.
- The body is roughly cubic; there is no meaningful short axis to close across.
- The graspable part is a concave interior (the inside of a ring, a pivot
  between two plates). A box has no opinion about concavity, and neither has
  this skill.

## Recommended subgraph state flow

```text
describe → get_obb → propose → frame → select → END
```

1. **`describe`** — `tool: robot.describe_gripper` (for the jaw span).
2. **`get_obb`** — `tool: sim.get_object_obb`, `inputs: {object_name: …}`.
   At `camera_only`/`none`, substitute `geometry.filter_and_compute_obb`.
3. **`propose`** — `script: scripts/<sg>/propose_short_axis.py`, inputs
   `target_obb = Ref("get_obb.obb")`, `gripper = Ref("describe")`.
   Router on `route`: `proposed` → `frame`, `declined` → the subgraph's
   `declined` exit.
4. **`frame`** — `tool: robot.grasp_frame`, `inputs:
   {close_heading_deg: Ref("propose.close_heading_deg")}`.
5. **`select`** — hand `propose.positions` and `frame.rotation` to
   `selecting-reachable-grasp`, which walks them.

## Required end states

| End state | Meaning |
|---|---|
| `proposed` | A heading and stations. Continue to select. |
| `declined` | The hand cannot span this object's short axis. Route to another propose rung — do not retry this one with different numbers. |
