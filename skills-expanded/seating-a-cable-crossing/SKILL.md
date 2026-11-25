---
name: seating-a-cable-crossing
description: Streams one planned crossing leg of a cable onto a routing station,
  lets the rod settle, then LOOKS — segments the rod, fits its centreline and
  counts how much of the curve lies inside the station's seat box on the side
  the route requires — and reports the fraction honestly rather than assuming
  the crossing took. It measures and does not correct. Use when a
  deformable-linear-object route is laid one crossing at a time and each
  crossing must be verified by vision before the next is planned.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: manipulation, tags: [deformable, cable, routing, verification, perception, cpu]}
gap:
  requires: {connector: [robot.wait_steps]}
  allowed_tools:
    - robot.execute_trajectory
    - robot.get_observation
    - robot.wait_steps
    - sam3.segment_text
    - curve.fit_centerline
  exit_conditions:
    done: The place leg was streamed and the crossing measured; `seated` and `fraction` say whether it took.
    blocked: A tool raised during the place or the look (the subgraph's on_error).
  required_inputs:
    plan: string
    scene: string
    index: int
    arm_id: int
  produces_outputs:
    seated: bool
    fraction: float
    detail: string
  canonical_scripts:
    - seat_station: scripts/seat_station.py
  streaming: false
---

# seating-a-cable-crossing

Seat one crossing, then look, and hand on an honest number.

## Why this is its own skill

A weave that streams its legs and hopes never finds out which crossing failed.
The whole difference between a full solve and a third of one on the weave
bench was one crossing that did not take and was never looked at again. This
skill closes that loop for a single crossing: stream the planner's `place`
leg, wait for the rod to come to rest, then segment the rod, fit its
centreline and count the densified curve inside the station's seat box.

"Did not take" is a **fraction, not a touch**. The task scores containment as
the share of the rod inside a box a few centimetres wide beside the station,
on the side the route requires (`>= 0.047` on the weave bench). Measured on the
failures, a losing station is almost never on the wrong side: it is on the
right side with too little of it there.

## What it deliberately does not do

It **measures and does not correct**. The obvious correction — push the hand
further onto the required side when the box is short — was built and measured
and made the seat worse (0.016 to 0.000 after a 14 mm nudge): the cable is not
short of the box, it is crossing it at an angle, and driving the contact point
further in rotates it further. A correction wants a different move, arriving
along the seat rather than across it, and that belongs in the carry planner.

## Routing

The script always returns `route: done`; the verdict is in the outputs.
`seated` is `fraction >= seat_fraction`; `fraction` is `0.0` when the seat
could not be measured at all (no camera frame, no depth, no rod mask, a fit too
short to be a curve) and `detail` says so. A graph that wants to branch on the
verdict reads `seated`, not the exit. `blocked` is the exit a subgraph declares
as `on_error` for a tool that raises during the place or the look.

## Which station

The plan's `station` field names the station the planner actually worked, and
that — not the loop's pass index — selects the seat box. The planner does not
work stations in pass order (far-side crossings first, near-side seats last,
each from the anchored end outwards), so indexing the perceived list by the
pass number measured a different station's box from the one just worked on
every pass. `index` is the fallback only when the plan carries no `station`.

## Inputs and parameters

| Input | Shape |
|---|---|
| `plan` | JSON: `{"stages": [{"stage": "place", "trajectory": Trajectory, ...}], "station": int, "side": ±1}` from the crossing planner |
| `scene` | JSON: `{"stations": [[x, y], ...], "sides": [±1, ...]}` from the fixture survey |
| `index` | the pass number; used only when the plan names no station |
| `arm_id` | the work arm that streams the place leg |

Parameters with the weave bench's numbers as defaults: `seat_fraction` (0.047),
`seat_inner` / `seat_outer` (0.003 / 0.045 m out from the station on the
required side), `seat_half_y` (0.035 m along the station line), `camera`
(`"cable"`), `rod_query` (`"thin white cable"`), `curve_nodes` (42). Read a
different bench's off its own task document rather than reusing them.
`grip_open_m` / `grip_close_m` are accepted for uniform binding and unused.

## What a CPU test can and cannot exercise

The fraction arithmetic (densification, the side sign, the box bounds) and the
plan-station indexing run against canned observations and a canned centreline
fit. What a CPU test cannot exercise is the perception behind
`sam3.segment_text` and `curve.fit_centerline` on a real frame, and whether a
streamed `place` leg actually lays cable where the plan said.

## Required end states

| End state | Meaning |
|---|---|
| `done` | Streamed and measured; read `seated` / `fraction` / `detail`. |
| `blocked` | A tool raised; the subgraph's `on_error`. |
