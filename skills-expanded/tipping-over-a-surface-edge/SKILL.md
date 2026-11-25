---
name: tipping-over-a-surface-edge
description: Turn a body over on the surface it rests on instead of carrying
  it — pinch two opposite walls LOOSELY and off centre so the pads act as a pin
  joint, lift so the surface and gravity stand the body up on its own edge,
  then press it onto the surface and pull the pins toward you about whichever
  edge is grounded until it is just past balance, and let go. Use when a rigid
  grasp cannot transmit the torque a full roll needs (a parallel jaw rolling
  about its own closing axis), when the body is too big to turn over in hand,
  or when the arm's envelope cannot follow a held body through the roll.
compatibility: requires gap>=0.1
metadata: {category: manipulation, tags: [bimanual, tipping, flipping, pivot, loose-grasp, cpu, sim-only]}
gap:
  requires: {connector: [sim.get_object_pose, sim.query, robot.describe_arm, robot.describe_gripper, robot.grasp_frame, robot.set_grip, robot.stream_dual, robot.wait_steps, motion.plan_linear, motion.plan_joint]}
  allowed_tools:
    - sim.get_object_pose
    - sim.query
    - robot.describe_arm
    - robot.describe_gripper
    - robot.get_ee_pose
    - robot.get_gripper
    - robot.grasp_frame
    - robot.set_grip
    - robot.stream_dual
    - robot.wait_steps
    - motion.plan_linear
    - motion.plan_joint
  exit_conditions:
    inverted: The body came to rest turned over on the surface after the release.
    standing: The body stands on its edge or wall; it rocked back at the release. Re-grasp through the mouth and pull again, a few degrees further.
    other: The body is neither turned over nor standing — it slipped out of the pads during the lift, or the release threw it.
  hard_rules:
    - >
      The wrist NEVER turns against a body resting on the surface. A loose
      pinch is a pin joint only while the wrist holds still: a 30-degree wrist
      roll applied in place slid the wall 45 mm out of the pads and dropped the
      body, while a 50 mm lift with the roll fixed slid it under 1 mm. Hold the
      roll through the lift. During the pull, turn the wrist by what the body
      has ACTUALLY turned (read its pose) plus at most one step of lead.
      `motion.plan_linear(orientation="lock")` applies a new rotation as a
      step at its first waypoint — turn with `motion.plan_joint` or not at all.
    - >
      The pinch is off centre ON PURPOSE. A body hanging from two pins settles
      where its centre of mass is under them, atan(offset / drop); pinch too
      near the centre and the lift alone leaves it far short of vertical, and
      every remaining degree drags the pins toward you across the surface. Put
      the pinch where the asset declares it (a `grasp_box` such as
      `crate.pinch`), and read the edges it declares as `rod`s
      (`sim.query(atom="geometry", refs=["crate.near_edge"])`) for the pivot.
    - >
      Pull about the grounded edge, read live, and PRESS while pulling. A pin
      near the centre of mass carries the body's weight, which unloads the
      edge; unloaded, the edge slides instead of turning (measured: 0.8
      degrees per chord and 23 cm of slide against 2–3 degrees per chord and
      1.7 cm with an 8 mm downward bias and the wrist following). Rotate each
      hand about the edge from where the hand actually is, so the pinch offset
      and the arm's sag under load drop out.
    - >
      Release just past balance, and leave through the mouth FAST. Balance for
      a body standing on a wall is where its centre of mass passes over the
      edge (measured on the crate: 106–107 degrees of its deck axis from world
      up). Past it the fall grows exponentially — 2 degrees past becomes 10
      degrees past in 0.3 s — and the inner pad can only exit the way the body
      is falling. Crack the jaws (ramped, a few mm, both hands), back out along
      the mouth direction, then sweep outboard past the body's ends before
      anything else. A wide open near the rim rocks the body back; a hand that
      leaves slowly is hit by the falling top wall.
  canonical_scripts:
    - read_scene: scripts/read_scene.py
    - approach: scripts/approach.py
    - pinch: scripts/pinch.py
    - lift: scripts/lift.py
    - press_pull: scripts/press_pull.py
    - release: scripts/release.py
    - check: scripts/check.py
  streaming: false
---

# tipping-over-a-surface-edge

Turn a body over by letting the surface it rests on do the turning.

## Why this is its own skill

A parallel jaw transmits force well and torque about its own closing axis
badly: two pads on a 12.6 mm wall are a friction clutch a few millimetres
wide. A strategy that grasps rigidly and rolls asks the clutch to carry the
whole roll and stalls (63 degrees on the crate, measured, at every grip force
and arm gain tried). This strategy asks the pads for **force only** — a pin
joint — and gets the rotation from gravity and from the surface's edge.

## When to use

- The body is wide and flat, and the roll would be about the jaws' closing axis.
- The body's mass or size is beyond an in-hand roll, or the arm's envelope
  cannot follow the held body around.
- There is surface to tip onto: tipping over an edge carries the body one
  full width in the direction it falls.

## When NOT to use

- There is no room to land: the flip travels a body width across the surface.
- The body cannot stand on the edge it would pivot on (a round or very narrow
  section), or its centre of mass sits so far from that edge that the standing
  body is unstable the wrong way.

## Recommended subgraph state flow

```text
read_scene → approach → pinch → lift → press_pull → release → check → END
                                                      ↑              │ standing
                                                      └── re-grasp ──┘
```

1. **`read_scene`** — which hand is on which side, the body's pose, the
   declared features (`sim.query(atom="geometry", ...)` on the pinch box and
   the edges).
2. **`approach`** — both hands to a hover over their pinch points, wrist at the
   one roll the whole manoeuvre will hold, then straight down onto the wall
   with the wrist locked.
3. **`pinch`** — `robot.set_grip(object_width_m=<wall>, squeeze_m=0.0015,
   ramp_steps=40)`. Loose. 3 mm slid where 1.5 held.
4. **`lift`** — straight up, both hands together (`robot.stream_dual`), wrist
   still, until the near corner leaves the surface (read the edge's height).
5. **`press_pull`** — chords of 3 degrees about the grounded edge, read live
   each chord, hands commanded 8 mm below the rotated point, wrist following
   the measured attitude. Stop on the measured attitude a little past balance.
6. **`release`** — crack, out along the mouth, outboard past the ends, wait.
7. **`check`** — the body's attitude after settling routes the exit.

The numbers in `scripts/tipcommon.py` are the crate's (`crate_flip/flip` on
`yam_i2rt`) and each one carries its measurement; read a different body's from
its declared features and the packet's attitude facts rather than reusing them.

## Required end states

| End state | Meaning |
|---|---|
| `inverted` | Turned over and at rest on the surface. |
| `standing` | Rocked back onto its wall at the release. Re-grasp through the mouth and pull further. |
| `other` | Slipped out during the lift, or thrown by the release. Start over from `approach`. |
