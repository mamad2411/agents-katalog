---
name: placing-held-feature
description: Move a held object so one of its declared features lands on a
  target point — a ring onto a hook, a tip into a hole, a plug at a bore.
  Composes the hand pose from the live object pose and the feature's centre in
  the object's own frame, recomputed each round so in-jaw slip cannot compound.
  Use for any goal written as "this object's feature at that place"; do NOT
  drive the hand to the target directly, which is wrong by the length of the
  held object.
compatibility: requires gap>=0.1
metadata: {category: manipulation, tags: [place, feature-mating, geometric, cpu, sim-only]}
gap:
  requires: {connector: [sim.get_object_pose]}
  allowed_tools:
    - sim.get_object_pose
    - robot.get_ee_pose
  exit_conditions:
    ready: A hand pose that puts the feature on the target, and the move it applies.
    unknown: A pose or a point could not be read; nothing was moved.
  required_inputs:
    target: Vec3
    object_name: str
    feature_local: Vec3
  hard_rules:
    - >
      Do NOT send the hand to the target. A goal like "`wrench_1.ring` encloses
      `wrench_hook_1.shank`" names where the RING must arrive; the hand must sit
      a whole tool-length away from it. `robot.solve_ik` refuses the hook pose
      on every arm of a task that is demonstrably solvable, and it is right to —
      that pose was never the target.
    - >
      `feature_local` is the feature's centre in the object's OWN frame, which
      the feedback packet's declared parts state (`wrench_1.ring — a loop at
      [0.17, 0, 0]`). It is an asset constant, identical on every episode and
      every layout. Reading it from the packet once is not fitting to a seed;
      measuring it per-episode from a pose is.
    - >
      Recompute every round rather than planning the whole place from the pick.
      The object shifts in the jaws during a carry, and a move planned from
      where the feature used to be arrives off by the slip. `distance_m` is the
      number to watch shrink.
    - >
      This TRANSLATES. It does not turn the object so a ring's hole lines up
      with a rod. What "aligned" means belongs to the goal's own predicate, so
      orient first (a locked `motion.plan_joint` in place), then mate.
  canonical_scripts:
    - mate_feature: scripts/mate_feature.py
  streaming: false
---

# placing-held-feature

The **place** stage's geometry: where must the hand be so that the thing it is
holding arrives where the goal wants it.

## Why this is its own skill

Grasping has a whole ladder of strategies and placing had none, which is
backwards for any goal phrased as a relation between a held object's feature
and a fixture. The composition is small and the mistake is not:

```
feature_now = object_position + R(object_rotation) · feature_local
move        = target − feature_now
hand_goal   = hand_now + move
```

Without it the obvious move is to drive the hand at the target, and that is
wrong by the length of the tool. It fails as a refusal rather than as a miss,
so it reads like an unreachable workspace rather than a mis-specified goal —
a diagnosis that costs iterations, because the fix it suggests (try the other
arm, give up on the target) is not the fix.

## When to use

- A goal written as *object.feature* at *fixture.feature* or in a region:
  a loop over a rod, a shaft into a hole, a plug at a bore.
- Any time the held object is large relative to the hand.

## When NOT to use

- To orient. This translates only; turn first, then mate.
- Before the object is held. It reads the object's live pose, which before a
  grasp is wherever it is lying.

## Recommended subgraph state flow

```text
locate → orient → mate → plan → execute → verify
```

1. **`locate`** — the target point. For a welded fixture with no body and no
   OBB, that is `sim.query` on the goal's own atom and refs; its `at` is the
   feature's world position.
2. **`orient`** — turn the held object so the mating axis lines up, as a locked
   `motion.plan_joint` at the current position. Transit first, then turn.
3. **`mate`** — `script: scripts/<sg>/mate_feature.py`. Route on `route`.
4. **`plan`/`execute`** — `motion.plan_linear(end=Ref("mate.hand_goal"),
   orientation="lock")` then `robot.execute_trajectory`. Locked, because the
   orientation you turned to is the one that must survive the move.
5. **`verify`** — re-run `mate` and read `distance_m`. Shrinking means the
   round worked; flat means the move is not being executed as planned.

Use `stop_short_axis`/`stop_short_m` when the fixture is mounted flush to a
board: close the two free axes fully and stop short on the board's normal, so
the approach does not drive the load into the mounting.

## Required end states

| End state | Meaning |
|---|---|
| `ready` | `hand_goal`, `move_m`, `feature_now`, `distance_m`. |
| `unknown` | A pose or point could not be read. Nothing moved; fix the inputs. |
