---
name: plugging-a-cable-end
description: Carries a cable's held free end into a terminal port after the
  last crossing — finds the port by vision as the terminal block furthest from
  the run's anchored end, takes the delivering hand and its working height from
  the support-hand planner, stages the carry three sides of a rectangle around
  the seated crossings at a hand's depth above the bench, drops into the mouth,
  opens the jaws and retreats along the bench. Use when a routed deformable
  linear object must terminate in a socket and the hand that anchored its free
  end is the one that can reach it.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: manipulation, tags: [deformable, cable, insertion, perception, bimanual, sim-only, cpu]}
gap:
  requires: {connector: [cable.plan_support, robot.grasp_frame, robot.set_grip, robot.wait_steps]}
  allowed_tools:
    - robot.get_observation
    - robot.get_ee_pose
    - robot.grasp_frame
    - robot.go_to_pose
    - sam3.segment_text
    - cable.plan_support
    - robot.set_grip
    - robot.wait_steps
  exit_conditions:
    plugged: The delivering hand reached the port mouth and opened; `detail` says whether it got there routed or on the diagonal.
    unplugged: No centreline or stations, no port in view, no support hand identified, the mouth unreachable at every height, or a tool raised on the carry; `detail` says which.
  required_inputs:
    scene: string
    prior: string
    arm_id: int
    grip_open_m: float
  produces_outputs:
    port: string
  canonical_scripts:
    - plug_port: scripts/plug_port.py
  streaming: false
---

# plugging-a-cable-end

Carry the run's free end into the port, after the last crossing.

## Why this is its own skill

A station is a place the cable passes; the port is where it stops. The crossing
template exists to get material onto the far side of a post and leave it there
under its own tension, and none of that applies to an end being put into a
box: there is no side to be on, nothing to reverse around, and the thing that
has to arrive is one specific end of the rod rather than whichever span happens
to be abreast.

**The support hand does it, because it is already holding the end.** Measured
with a reach sweep on the weave bench, the two arms cover complementary halves
and the run's free end lies in the support arm's half — 65 mm outside the work
arm's envelope. So the hand that anchored the end is the hand that plugs it: no
release, no re-grasp, no second hand crossing the weave. If the support hand
cannot be identified the skill refuses rather than guessing, because the only
fallback is the known-broken configuration.

## What it needs from the connector

This skill requires a connector that registers `cable.plan_support`, a
privileged support-hand planner that reads the true rod state — in simulation
the cable-routing suite's connector provides it. Here it is read for two
things only: which hand is the support hand (`arm_id`, `arm_name`) and the
working height its jaws need to straddle a rod on the bench (`grasp_m[2]`),
both arithmetic over the hand's own colliders. It also needs
`robot.grasp_frame` (the straight-down wrist composed from the live hand's
measured axes — a literal quaternion is a half turn out on a hand whose
approach axis is not tool-local +z), `robot.set_grip` and `robot.wait_steps`.
The generic connector registers none of the four, which is why the bundle is
`sim-only` today.

## Recommended subgraph state flow

```text
plug_port ──plugged──▶ verify
    └──unplugged──▶ verify (the weave layouts have no port; this is normal there)
```

1. Parse `scene` (stations) and `prior` (the rod's centreline as JSON, the
   `rod` output of the centreline-perceiving skill carried by the graph).
   Nothing to terminate → `unplugged` before any tool call.
2. Segment the terminal blocks from the `cable` camera
   (`sam3.segment_text`), keep those above the score and area floors, and
   take the one furthest from the rod's anchored end as the port.
3. `cable.plan_support` for the delivering hand and its working height;
   no `arm_id` → `unplugged`, "no support arm".
4. Read the hand's own pose (`robot.get_ee_pose`) and the wrist
   (`robot.grasp_frame`); stage `lift` → `across` (out past the stations) →
   `over` → `mouth` with `robot.go_to_pose`, each retried 20 and 40 mm lower
   before it is skipped. Only the mouth is fatal.
5. `robot.set_grip(width_m=grip_open_m, arm_id=<support>)`, settle, retreat
   back along the bench rather than up.

## Inputs and parameters

| Input | Shape |
|---|---|
| `scene` | JSON: `{"stations": [[x, y], ...]}` from the fixture survey |
| `prior` | JSON: `[[x, y, z], ...]` (or a `Centerline` object whose `points` are that list) — the rod's last fitted centreline; its last node is the free end |
| `arm_id` | the WORK arm; named in the refusal, never used to plug |
| `grip_open_m` | the width the delivering hand opens to at the mouth |

Parameters with the weave bench's measured defaults: `block_query`
(`"orange block"`), `block_score` (0.50), `block_min_px` (3400), `port_inset`
(0.004 m short of the port's centre), `carry_z` (0.070 m above the working
height — a spool flange stands 23 mm, and the 30 mm this once ran at dragged the
tail across the seats). `grip_close_m` is accepted for uniform binding and
unused. Output `port` is the chosen block's world centroid as a JSON list
(`"null"` when none was found).

## Router field

The script's exit is in its `exit` field (`plugged` / `unplugged`), not
`route`; `detail` carries the reason and whether the carry went routed or on
the diagonal.

## What a CPU test can and cannot exercise

The early gates (no prior, no support arm), the port choice, and the call
order (observe, segment, plan, pose, wrist, four waypoints, open on the support
hand, settle, retreat) run against canned tools. What a CPU test cannot
exercise is the planner behind `cable.plan_support`, the segmentation on a
real frame, or whether the rod's end actually came with the hand into the
channel — that is the task's port clause to say.

## Required end states

| End state | Meaning |
|---|---|
| `plugged` | The hand reached the mouth and opened; `port` bound. |
| `unplugged` | Refused, nothing in view, or the mouth unreachable; `detail` says which. |
