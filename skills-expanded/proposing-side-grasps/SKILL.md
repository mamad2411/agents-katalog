---
name: proposing-side-grasps
description: Propose horizontal (side-entry) grasps swept around an object's
  oriented box — twelve azimuths ranked by jaw margin. Use when top-down access
  is blocked by an overhead shelf, a lid or a bin wall, or when the object's
  vertical dimension is the only one the hand can span. Declines when the
  object is wider than the jaws from every azimuth.
compatibility: requires gap>=0.1
metadata: {category: grasping, tags: [grasping, propose, geometric, cpu, sim-only]}
gap:
  requires: {connector: [sim.get_object_obb, robot.describe_gripper, robot.grasp_frame]}
  allowed_tools:
    - sim.get_object_obb
    - robot.describe_gripper
    - robot.grasp_frame
  exit_conditions:
    proposed: One or more horizontal approaches, widest jaw margin first.
    declined: No azimuth leaves a width the hand can span.
  required_inputs:
    target_obb: OrientedBoundingBox
  hard_rules:
    - >
      The candidates are ranked by jaw margin and by NOTHING else. Which side
      is actually open is a fact about the scene, not the object, and it is the
      selector's question — pair this with `selecting-reachable-grasp` and let
      the clearance gate reject the blocked azimuths.
    - >
      `robot.grasp_frame` takes BOTH the approach direction and the closing
      heading for a side grasp: `grasp_frame(approach=<candidate.approach>,
      close_heading_deg=<candidate.close_heading_deg>)`. Passing only the
      heading leaves the approach straight down, which is a top-down grasp
      wearing a side grasp's heading.
    - >
      `position` is the object's own centre height, NOT a pre-grasp standoff.
      Stage back along `-approach` yourself before descending in, or plan the
      entry with `motion.plan_linear(orientation="lock")`.
  canonical_scripts:
    - propose_side_grasps: scripts/propose_side_grasps.py
  streaming: false
---

# proposing-side-grasps

One strategy for the **propose** stage: horizontal entry, swept around the
object.

## Why this is its own skill

It is the alternative that exists so a top-down refusal has somewhere to go.
`proposing-short-axis-grasps` declines by measuring a width; it cannot offer a
side entry, because approaching horizontally is a *different strategy*, not a
different number. A policy with only one propose rung answers a structural
refusal by re-tuning parameters that cannot help.

## When to use

- Overhead access is blocked — a shelf plate, a lid, a bin rim above the target.
- The object is flat and wide on top but narrow in profile.
- The top-down rung declined.

## When NOT to use

- The object stands against a wall or in a corner and only one azimuth is open.
  This skill will happily rank a blocked side first; the clearance gate in
  `selecting-reachable-grasp` is what makes that safe, so do not use this rung
  without a selector.
- The graspable feature is a concave interior — a box's silhouette says nothing
  about concavity.

## Recommended subgraph state flow

```text
describe → get_obb → propose → select → END
```

1. **`describe`** — `tool: robot.describe_gripper`.
2. **`get_obb`** — `tool: sim.get_object_obb` (or `geometry.filter_and_compute_obb`
   on the vision body).
3. **`propose`** — `script: scripts/<sg>/propose_side_grasps.py`, inputs
   `target_obb`, `gripper`. Router on `route`.
4. **`select`** — build a pose per candidate with `robot.grasp_frame(approach=…,
   close_heading_deg=…)` and walk them with `selecting-reachable-grasp`. Its
   clearance gate is what turns "ranked by margin" into "reachable in this
   scene".

## Required end states

| End state | Meaning |
|---|---|
| `proposed` | Candidates, widest margin first. Continue to select. |
| `declined` | Wider than the jaws from every azimuth. The remaining option is a part of the object narrower than its whole box. |
