---
name: anchoring-a-free-end
description: Pins one end of a cable with the support hand before any crossing
  is attempted — asks the support-hand planner for the anchor grasp as
  joint-space legs, refuses it when its worst IK error is past the limit,
  streams the legs, closes the jaws to the plan's own width and dwells for the
  fingers' travel, and carries the solved chain and grasp orientation out on
  the exit so later pay-outs seed from them. Use when a deformable linear
  object must be held at one end so a sideways pull bends it instead of
  dragging the whole thing.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: manipulation, tags: [deformable, cable, bimanual, grasping, sim-only, cpu]}
gap:
  requires: {connector: [cable.plan_support, robot.set_grip, robot.wait_steps]}
  allowed_tools:
    - cable.plan_support
    - robot.execute_trajectory
    - robot.set_grip
    - robot.wait_steps
  exit_conditions:
    anchored: The support hand holds the far end; `segment`, `q_support` and `quat` are bound for the pay-outs that follow.
    unanchored: The planner returned no legs or a grasp past the IK error limit; nothing moved. Abort the weave rather than proceed one-handed.
  produces_outputs:
    segment: int
    worst_error_m: float
    q_support: string
    quat: string
  canonical_scripts:
    - anchor_far_end: scripts/anchor_far_end.py
  streaming: false
---

# anchoring-a-free-end

Take the cable's far end with the support hand, before any crossing.

## Why this is its own skill

Why it matters is a property of the material, not of the plan. A cable held at
one end and pulled sideways *bends*; a free cable **translates**. Without an
anchor the first crossing hauls the whole cable toward one station and the
next has nothing left to grasp — measured, 26 of 42 segments piled at a single
station. Every later crossing then works on a cable that has already moved out
from under the model that was measured.

Failure is fatal here in a way a missed look is not. A weave without an anchor
is not a degraded weave, it is a different and much worse task, so the skill
routes `unanchored` for a graph to abort on rather than carrying on and
reporting the result as a policy failure.

## What it needs from the connector

This skill requires a connector that registers `cable.plan_support`, a
privileged support-hand planner that reads the true rod state and returns the
anchor grasp as joint-space legs (`stages`), the hand that owns them
(`arm_id`, `arm_name`), the close width (`close`), the end joint state
(`q_end`), the grasp orientation (`quat`), the rod `segment` taken and the IK
error of the worst waypoint (`worst_grasp_error`) — in simulation the
cable-routing suite's connector provides it. It also needs `robot.set_grip`
(a ramped jaw command in metres, addressed by `arm_id`) and `robot.wait_steps`
(hold still while the scene runs on). The generic connector registers none of
the three, which is why the bundle is `sim-only` today.

## Recommended subgraph state flow

```text
anchor_far_end ──anchored──▶ (the first crossing)
       └──unanchored──▶ abort
```

1. Ask `cable.plan_support(approach=)` for the grasp.
2. Refuse when there are no legs or `worst_grasp_error` exceeds 50 mm — past
   that the chain is in a different basin and what streams is a whip with the
   cable near the jaws.
3. Stream each leg with `robot.execute_trajectory` on the plan's `arm_id`.
4. `robot.set_grip(width_m=plan.close, arm_id=plan.arm_id)`, then
   `robot.wait_steps` for the jaws' own travel: a finger command is a target,
   not a state, and the first crossing must not start while the pads are still
   moving.
5. Return the solved chain (`q_support`) and grasp orientation (`quat`) as
   JSON lists: every later pay-out seeds its IK from them, and re-deriving them
   per crossing would let the support chain drift into a different basin
   mid-weave.

## Inputs and outputs

The script takes one parameter, `approach` (m above the grasp the enter leg
starts from; 0.055). Outputs: `segment` (the rod segment held; -1 when
refused), `worst_error_m`, and `q_support` / `quat` as JSON strings
(`"null"` when refused).

## What a CPU test can and cannot exercise

The refusal gate and the call order (plan, stream each leg, close on the
plan's width and hand, dwell) run against a canned plan. What a CPU test cannot
exercise is the planner behind `cable.plan_support` — whether the legs it
returns reach the rod — nor whether the pinch actually holds under the first
crossing's pull.

## Required end states

| End state | Meaning |
|---|---|
| `anchored` | The far end is held; `segment`, `q_support`, `quat` bound. |
| `unanchored` | Refused before anything moved. Abort the weave. |
