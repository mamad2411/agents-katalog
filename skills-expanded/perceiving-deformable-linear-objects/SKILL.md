---
name: perceiving-deformable-linear-objects
description: Read a cable's ordered 3D centreline from one RGB-D frame and keep it current across a task — seed it from an unobstructed survey, re-fit it cold whenever the whole rod is in view, and fall back to tracking the carried prior only when the fresh fit comes back short. Use when a manipulation loop needs the current shape of a deformable linear object (a cable, rope, or hose) once per step rather than every frame, from a fixed third-person camera.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: perception, tags: [perception, cable, deformable, centreline, tracking, rgb-d, cpu]}
gap:
  allowed_tools:
    - robot.get_observation
    - sam3.segment_text
    - curve.fit_centerline
    - curve.track_centerline
  required_inputs: {prior: string, scene: string}
  produces_outputs: {rod: string, arclength_m: float, source: string, camera: string, visible: int}
  exit_conditions:
    found: A centreline is bound in `rod` — seeded, initialised, re-fitted, tracked, or the prior held because this frame could not improve on it.
    lost: No centreline could be born — no depth camera by the given name, no mask for the query, or no candidate fitted as a curve — and there was no prior to hand back.
  canonical_scripts:
    - perceive_rod: scripts/perceive_rod.py
  streaming: false
---

# perceiving-deformable-linear-objects

Read the cable's centreline once per step, and carry it through the loop as
text.

## Why this is its own skill

A rigid object is perceived once and then transformed; a cable has no pose,
only a shape, and the shape changes every time a crossing moves it. The thing
a routing loop needs is therefore an **ordered 3D centreline** — 42 nodes in
arc-length order, not a bounding box and not a principal axis — and a rule for
when to trust a fresh reading of it over the one it already has. That rule is
the skill: a cold fit has no history and is the better estimate whenever the
whole rod is in frame; a tracker is the better estimate only when it is not.
Which case a frame is in is measurable (length against the prior) and the
script routes on it.

Measured over eight arm poses from a bench camera pitched 55 degrees off the
vertical, scored against the rod's own bodies:

| estimate | median | p90 | max |
|---|---|---|---|
| cold fit per frame | 6.7 mm | 8.4 mm | 9.3 mm |
| tracked from the prior | 9.0 mm | 9.7 mm | 9.9 mm |

The tracker is the worse estimate when nothing is hidden, and monotonically so
across passes (7.6, 8.6, 9.2, 9.6, 9.6, 9.9 mm): each pass drags the prior
along instead of carrying a hidden stretch through. It is still the right
fallback, because the cold fit's own failure is sharp rather than gradual — a
skeleton broken by the arm merges to one fragment, measured at 338 mm of a
488 mm rod (0.69), while honest fits ran 0.99–1.06 of the truth. The
`whole_rod` gate (0.80) sits between those two populations.

## When to use

- A loop needs the current shape of a cable, rope, or hose once per station or
  per step, and the shape only changes when the robot moves it.
- A fixed third-person RGB-D camera can be placed where it sees the whole
  object. Measured: an eye-in-hand camera frames a fifth of the cable at best,
  and an A/B over three episodes came out identical (0.667 mean) — the move it
  costs buys nothing. Pitch the camera off the vertical: overhead, the hand
  covered the rod exactly when the rod was moving (28 of 42 nodes visible,
  60 mm RMS); at 55 degrees it sees 41 of 42 and fits at 6.7 mm.

## When NOT to use

- Every-frame tracking during a motion. This skill spends one detector call
  and one fit per read; call it between motions, not inside one.
- Rigid, linear parts (a shaft, a handle) — fit an axis with
  `geometry.fit_linear_feature` instead.

## State flow

```text
prior == "" or index == 0 ──► seed from scene.rod ──► found (seeded)
           │ no seed
           ▼
prior == "" ──► cold fit every mask candidate, take the THINNEST ──► found (initialised) | lost
           │ prior present
           ▼
for camera in (chosen, track_camera, init_camera):
    cold fit ──► length ≥ whole_rod × len(prior)? ──► found (refit)
    else track prior onto the frame ──► ≥ min_visible nodes seen? ──► found (tracked)
nothing improved ──► found (held; rod == prior)
```

1. **Seeded.** On the first pass (`index == 0`) — or whenever there is no
   prior — the survey's `rod` (the `scene` JSON's `rod` key, from
   `perceiving-routing-fixtures`) is returned as the model. The model must be
   born from an unobstructed view of the whole object, and that view exists
   exactly once per episode, before the first move; re-fitting after the hand
   has parked over the first station read 381 mm of a 500 mm rod.
2. **Initialised.** With no prior and no seed, the bench camera is read, up to
   `mask_candidates` masks are fitted, and the thinnest plausible one wins.
   The top-scoring mask is not always the cable: on a grey bench with white
   arms a prompt sometimes returns the rod merged with an arm, scored
   confidently — measured on a 700 mm rod as 963 and 983 mm seeds on two of
   six episodes, both of which failed. Radius (mask area over centreline
   length) separates them where score cannot; `max_rod_radius` (12 mm) is the
   ceiling.
3. **Refit.** The look's camera is tried first, then `track_camera`, then
   `init_camera`. A fresh fit whose arclength reaches `whole_rod` of the
   prior's is taken as is.
4. **Tracked.** A short fit hands the frame to `curve.track_centerline`, which
   moves the prior's nodes by what the frame says about each and carries the
   unanswered ones on the displacement field of their visible neighbours. The
   update is believed only when at least `min_visible` nodes (6, about 70 mm
   of a 500 mm rod) had real correspondence — a tracker that accepted every
   frame would walk the model onto whatever happened to be visible.
5. **Held.** Nothing improved on the prior; it is handed back unchanged.

## Inputs

- `prior` — the centreline the loop carries, as JSON text; empty on a cold
  start. The graph binds it to the latest `rod` written upstream (the
  survey's on the first pass, this skill's own afterwards).
- `scene` — the survey JSON from `perceiving-routing-fixtures`; only its
  `rod` is read here.
- `camera` — the camera the look chose for this pass (empty: the bench camera).
- `index` — the pass number; 0 is the pass before the first move.
- Bench constants as parameters with the measured defaults: `init_camera`
  and `track_camera` (`"cable"`), `rod_query` (`"thin white cable"`),
  `rod_score` (0.20), `whole_rod` (0.80), `min_visible` (6),
  `max_rod_radius` (0.012), `curve_nodes` (42), `mask_candidates` (4).

## Outputs

- `rod` — the centreline as **JSON text: the `points` of a `Centerline`**, an
  ordered list of `[x, y, z]` metres at 0.01 mm precision. It is passed as
  text so it round-trips through a loop unchanged (`json.loads` gives the
  list; a JSON `Centerline` object with a `points` key is also accepted on
  the way in). On `held` and `lost` it is the prior that was given (`"null"`
  when there was none), so a pass never binds a worse model than it had.
- `arclength_m`, `source` (`seeded` | `initialised` | `refit` | `tracked` |
  `held` | `no-camera` | `no-mask` | `no-fit`), `camera` (which view carried
  this update), `visible` (nodes with real correspondence; the node count for
  a fit).

The router field is `route`. A node that raises binds no outputs, so the next
reader of `rod` falls back to whatever was written before it.

## Required end states

| End state | Meaning |
|---|---|
| `found` | `rod` carries a centreline (see `source` for how it was earned). |
| `lost` | No model could be born and there was no prior to hold. |
