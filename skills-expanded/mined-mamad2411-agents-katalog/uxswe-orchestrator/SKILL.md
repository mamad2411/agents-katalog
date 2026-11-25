---
name: uxswe-orchestrator
description: Route UI work between building and reviewing, and run the build-evaluate-repair loop until the interface holds up. Use when a UI task needs both construction and review ("build this and make sure it's good", "ship-ready", "production quality"), when the right next step is unclear, or when repairing an interface against review findings. For a pure build use uxswe-build directly; for a pure review use uxswe-evaluate directly.
---

# uxswe-orchestrator

Routing and the repair loop. This skill holds no UX knowledge of its own — that
lives in `uxswe-build` and `uxswe-evaluate`. Its only job is deciding which runs
next and when to stop.

## Routing

| The request is | Route to |
|---|---|
| Create or restyle an interface, no existing artifact to judge | `uxswe-build`, then one evaluation pass |
| Review, audit, or critique something that already exists | `uxswe-evaluate` only |
| Fix the problems in an existing interface | `uxswe-evaluate` first, then repair what it found |
| Build something and make it hold up | the full loop below |

When the request is ambiguous, ask which the user wants rather than guessing —
running a full loop on a request for a quick prototype wastes their time, and
building when they wanted a review discards work they already have.

## The loop

```
build ──► evaluate ──► blocking defects? ──no──► report and stop
   ▲                          │
   └────── repair ◄───yes─────┘
```

1. **Build** — invoke `uxswe-build` for the initial construction.
2. **Evaluate** — invoke `uxswe-evaluate` against what was built. It returns
   located defects, each with a proposed repair and a severity.
3. **Repair** — apply the repairs for blocking defects. Apply non-blocking ones
   only if they are cheap and uncontested.
4. **Re-evaluate** — but only the areas that changed, plus anything the repair
   could plausibly have broken. A full re-evaluation every iteration is waste.
5. **Stop** when there are no blocking defects left.

## Termination

The loop must terminate. Enforce all three:

- **Cap at 3 repair iterations.** If blocking defects remain after the third,
  stop and report what is left with why it resisted repair. A loop that cannot
  converge in three passes has a problem that iteration will not fix.
- **Stop on no progress.** If an iteration produces the same defect count and
  the same defects, stop — the repairs are not landing.
- **Stop on oscillation.** If a repair reintroduces a defect that a previous
  repair fixed, stop and surface the conflict. Two findings are in tension and
  that is a design decision for the user, not something to resolve by looping.

A defect the user has explicitly accepted is not blocking. Record it and move
on; do not re-raise it on the next iteration.

## Reporting

Surface to the user once, at the end — not after every iteration. The report is:

- what was built or changed
- what the evaluation found, and what was repaired
- **what is still outstanding**, with severity and why it was not fixed
- any conflicts that need their decision

Do not report a clean result while blocking defects remain unfixed. If the loop
hit its cap, say so plainly and list what survived.
