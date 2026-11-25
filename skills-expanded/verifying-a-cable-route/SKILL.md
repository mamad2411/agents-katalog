---
name: verifying-a-cable-route
description: Judge a finished cable route from a camera rather than from an evaluator — re-read the cable's centreline from the clear-view camera (tracking the carried prior when the support hand still hides one end), test that rod material lies on the owed side of every station within the seat's reach, and that the hand has left the rod. Use when a routing policy must decide for itself whether every crossing is seated and it is safe to stop, and report margins so a disagreement with a scorer is diagnosable.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: verification, tags: [verification, perception, cable, routing, rgb-d, cpu]}
gap:
  allowed_tools:
    - robot.get_observation
    - robot.get_ee_pose
    - sam3.segment_text
    - curve.fit_centerline
    - curve.track_centerline
  required_inputs: {scene: string, prior: string}
  produces_outputs: {success: bool, worst_margin_m: float, tcp_clear_m: float, detail: string}
  exit_conditions:
    woven: Every station has rod on its owed side within the seat's reach, and the hand is clear of the rod.
    short: At least one station is unseated (no rod abreast of it, on the wrong side, or outside the box), the hand is still on the rod, or no rod could be read at all; `detail` says which.
  canonical_scripts:
    - verify_weave_vision: scripts/verify_weave_vision.py
  streaming: false
---

# verifying-a-cable-route

Is every station seated, and am I off the rod — answered from a frame, with
margins.

## Why this is its own skill

A policy that can only know it is finished by asking a simulator's evaluator
is not a policy that could run in a cell. The route's success criteria are
visible — rod material in a box beside each post, a hand some distance from
the rod — and this skill measures exactly those, on the same stations the plan
was built on, with the same centreline tools the routing loop used. It is a
**judgement, not a score**: it does not reproduce a scorer's containment
arithmetic (agreeing with a number one cannot see is how a graph ends up
disagreeing with the thing the number was about) but it reports its own
margins so any disagreement is diagnosable.

Measured on a three-spool bench: one disagreement with the evaluator in twelve
episodes, and that one was the old pixel-counting test passing on a stray
fleck of mask — the reason the seat clause now counts a fraction of the
densified centreline (the goal's own 0.047) instead.

## When to use

- The last crossing has been released and the work hand has retreated; the
  cable camera has a clear view of the route.
- The plan's `scene` (stations along +y, the side each owes) is available —
  the stations are **not** re-detected, because a second independent
  detection is a second chance to mis-order the posts.

## When NOT to use

- Mid-route: with a hand on the rod the release clause cannot pass and a
  short fit is likely. Verify once, at the end.
- A route whose success is not "rod on a side of each post" (a wrap count, a
  plug in a port) — measure that instead.

## State flow

```text
scene ──► stations + sides (the plan's)
frame ──► rod mask ──► cold fit
              │ whole rod (≥ whole_rod × len(prior), or no prior) ──► use it
              │ short and a prior exists ──► track the prior onto the frame
              ▼
resample every sample_step ──► per station: rod abreast (|Δy| ≤ seat_band),
      offset onto the owed side in [seat_inner, seat_reach], ≥ seat_fraction of the rod?
hand: min distance from the rod > clear_m?
all seated and clear ──► woven, else short
```

The support hand is usually still holding the far end when this runs, and a
cold fit truncated there does not say it is truncated — it reports a station
with no rod. Measured: the station nearest the support grip came back
`no-rod` in every episode of one layout, including ones the evaluator scored
3 of 4. Tracking the carried `prior` onto the frame carries that end through.

Per station the outcome is one of `seated`, `wrong-side` (the best point is
on the far side of the post; the signed margin is negative), `outside-box`
(right side, beyond the seat's reach) or `no-rod` (nothing abreast; margin is
NaN). A previous revision read a wrong-side margin as a near-miss and a build
was spent pressing harder on a cable on the far side of its post.

## Inputs

- `scene` — the survey JSON from `perceiving-routing-fixtures`; `stations`
  and `sides` are read.
- `prior` — the centreline the loop carries (JSON text: a list of `[x, y, z]`
  points, or a `Centerline` object with `points`); empty when there is none,
  in which case the cold fit is used as is.
- `camera` (`"cable"`, 0.50 mm/px against the overhead's 1.75), `rod_query`
  (`"thin white cable"`), `rod_score` (0.20), `curve_nodes` (42), `whole_rod`
  (0.80), `sample_step` (0.002 m).
- Goal-clause constants, defaults from the goal this was written against:
  `seat_reach` (0.045, the box's outer edge), `seat_inner` (0.003, its inner
  edge — rod pressed against the post is not in the box), `seat_band` (0.035,
  the box's half-extent along the run), `seat_fraction` (0.047 of the rod),
  `clear_m` (0.05, the `tcp-distance` clause).

## Outputs

- `exit` — `woven` | `short`. **The router field is `exit`**, not `route`;
  wire the subgraph's exit on it.
- `success` — the same verdict as a bool.
- `seated` — one bool per station, in `scene` order (stated here rather than
  under `produces_outputs` because the type registry names no bare list of
  bools).
- `worst_margin_m` — the smallest finite signed margin across stations
  (negative: wrong side); 0.0 when none is finite.
- `tcp_clear_m` — the hand's distance from the nearest rod sample.
- `detail` — `"k/n seated (need of N nodes each): seated, wrong-side, …; hand
  D mm off the rod"`.

## Required end states

| End state | Meaning |
|---|---|
| `woven` | Every station seated on its owed side and the hand is clear. Stop. |
| `short` | Something is not: read `detail` and `seated` for which station and why. |
