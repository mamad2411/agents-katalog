---
name: perceiving-routing-fixtures
description: Survey a cable-routing bench from one overhead RGB-D frame — find every station (spool, cleat) by colour, roundness and height off the work surface, fit the cable's ordered centreline through a text-prompted segmenter, derive the side each crossing owes from the instruction's alternation, and place the physical seat beside each post. Use when a routing plan needs the fixture layout and the starting shape of a deformable linear object, once, before the first move.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: perception, tags: [perception, cable, fixtures, routing, opencv, rgb-d, cpu]}
gap:
  allowed_tools:
    - robot.get_observation
    - sam3.segment_text
    - curve.fit_centerline
  produces_outputs: {scene: string, stations: int, rod: string, body: string}
  exit_conditions:
    found: At least one station and a cable-shaped centreline were measured; `scene` carries stations, sides, seats and the rod.
    not_found: No station passed the colour and height gates and the text fallback, or no rod mask fitted as a curve; `scene` is empty.
  canonical_scripts:
    - perceive_weave_vision: scripts/perceive_weave_vision.py
  streaming: false
---

# perceiving-routing-fixtures

One overhead frame, three numbers a routing plan needs: where the stations
are, which side of each the cable must finish on, and where it seats.

## Why this is its own skill

Routing a cable around fixtures is planned against a **layout**, and a layout
is a different kind of fact from an object pose. It has to be measured once,
from an unobstructed view, before anything moves — because every later frame
has a hand in it — and it has to be measured in a fixed order (along +y),
because the sides alternate and a permutation mirrors every crossing. This
skill owns that survey and the conventions in it, so the plan, the tracking
loop and the verify all build on the same stations.

Measured on a three-spool bench against the declared layout: stations to
0.0–0.2 mm, spool radius to ~0.3 mm, rod length +10 mm (mask dilation at the
tips, which is why the rod's line and radius are measured rather than its
extent). Sub-millimetre from 16×16-pixel blobs because a centroid over ~189
mask pixels is a sub-pixel estimate.

## When to use

- A deformable linear object has to be routed around rigid fixtures of one
  known colour that stand off the work surface (spools, cleats, posts).
- A fixed overhead RGB-D camera looks down the fixtures' own axes — a
  three-quarter view projects a flange disc to an ellipse whose centroid is
  not its centre.
- The routing loop (`perceiving-deformable-linear-objects`) needs a seed
  centreline born from the whole rod, unobstructed.

## When NOT to use

- The fixtures are not colour-separable from the bench and the text detector
  is the only handle — this skill's classical path finds nothing and falls
  back to the prompt, which is slower, noisier, and can return four stations
  on one frame and three on the next.
- The sides are decided by geometry rather than by the instruction (a threaded
  path with a declared order). `sides` here is language, not vision.

## State flow

```text
read frame ──► stations by colour + roundness + height (OpenCV)
                  │ none            │ some
                  ▼                 │
           sam3 text fallback       │
           (area floor, height gate)│
                  │                 │
                  ▼                 ▼
              none? ──► not_found   sort along +y
                                    │
                                    ▼
             rod: every prompt asked, candidates pooled, each fitted,
                  the LONGEST under the radius ceiling wins
                  (the longest over-thick one if nothing is under it)
                                    │ none ──► not_found
                                    ▼
             sides from the alternation + first_side; seats = post radius + rod radius
                                    │
                                    ▼
                                  found
```

1. **Stations, classical first.** A spool is rigid, one colour, one size and
   bolted down — everything a network is good at is already known about it.
   Colour threshold, a fill/aspect test for roundness, and the **height off
   the bench** (a spool flange stands 23 mm up, a cleat cap 43, a terminal
   plate 10; the gate is 15 mm) against a bench plane taken as the median
   world height of the depth image. Side by side on the same frames: SAM3
   2.8 mm from truth, OpenCV 2.9 mm, and 0.9 mm once the 2.8 mm
   surface-to-axis bias both share is removed. A blob 1.6× the median radius
   is two fixtures merged and is dropped.
2. **Stations, text fallback.** Only when the colour gate finds nothing: the
   `post_query` prompt, an area floor of 100 px (a terminal sliver is 27–44 px,
   a spool 172–200 from this camera), and the same height gate.
3. **Rod.** Every prompt in `rod_queries` is asked and the candidates pooled
   — one prompt is a calibration, and across four layouts neither
   `"thin white cable"` nor `"white rod"` found the rod on all of them (two
   each way, the loser under the 0.20 floor). Each candidate is fitted with
   `curve.fit_centerline`; among those under the 20 mm radius ceiling the
   **longest** wins (thinness ranked backwards: it chose a 148 mm fragment of
   a 700 mm rod). If nothing is under the ceiling the longest over-thick one
   is used and reported rather than the episode being thrown away.
4. **Sides and seats.** Sides alternate from `first_side` (−1) along +y — a
   convention the instruction does not state and no frame can show. The seat
   is the *physical* one, post radius plus rod radius (9.75 mm on this bench),
   not a scoring box's centre.

## Inputs

- `instruction` — the task text; read off the observation when empty. Only
  its alternation is used.
- `camera` (`"overhead"`), `post_query` (`"orange spool"`), `rod_queries`
  (`"thin white cable,white rod"`, comma-separated, all asked), `first_side`
  (−1), `curve_nodes` (42), `post_score` (0.30), `post_area_min` (100),
  `rod_score` (0.20).
- Colour-path knobs, forwarded to `scripts/fixtures_cv.py`: `spool_hsv_lo`
  (`"5,120,60"`), `spool_hsv_hi` (`"25,255,255"`, OpenCV's 0–180 hue),
  `spool_min_area` (60 px), `fixture_min_height_m` (0.015).

## Outputs

- `scene` — JSON text with `stations` (`[[x, y], …]` along +y), `sides`
  (±1 per station), `seats_x` (metres), `rod` (the centreline's points) and a
  `measured` block (post radii, rod radius, arclength, node count, ordered
  flag, whether the instruction said "alternating") kept for the trace.
- `rod` — the same centreline on its own, as **JSON text: the `points` of a
  `Centerline`**, an ordered list of `[x, y, z]` metres, byte-identical to what
  `perceiving-deformable-linear-objects` reads and writes so a graph can bind
  it straight into that loop's `prior`. `"null"` on `not_found`.
- `stations` — how many were found (also reported on `not_found`, so a run
  that saw its spools and lost the rod is diagnosable).
- `body` — `"vision"`.

The router field is `route`. Both `scripts/perceive_weave_vision.py` and its
helper `scripts/fixtures_cv.py` ship with the bundle; the helper is imported
by name from the script's own directory.

## Required end states

| End state | Meaning |
|---|---|
| `found` | `scene` and `rod` are bound; plan against them. |
| `not_found` | No stations, or no cable-shaped rod. Nothing downstream can run; abort or re-light the bench. |
