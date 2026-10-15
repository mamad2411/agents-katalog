---
name: intent-reconcile
description: Reconcile genuinely concurrent intent proposals into per-decision active state, compose product direction with architectural constraints, retire superseded decisions, and stop for consequential non-composable choices. Normally invoked by intent-land.
---

# intent-reconcile

This is the advanced concurrent-proposal integrator used by `intent-land`, not a serial task
closing ritual.

For a consequential conflict, follow
`../intent-check/references/intent-interview.md`. For unfamiliar repository orientation, read
`references/intent-orient.md` without loading proposal state.

## Invocation

```text
/intent-reconcile [proposal paths...] [--stage]
/intent-reconcile --obsolete <id> --source <inspectable-source>
```

With no paths, derive tracked `.intent/proposals/**/*.yml`. If there is only one proposal, no
concurrent property, and no cross-branch supersession, stop and use direct capture instead.

## Reconcile

1. Run `sh ci/check-intent.sh --landing` and validate affected exceptions.
2. Validate the active-decision admission test and provenance of every candidate.
3. Build the explicit `supersedes` graph over active ids and the batch. Topologically sort it;
   missing ids and cycles stop before writes.
4. Establish supersession observation through ancestry, a relevant `observed_ids`, or earlier
   same-batch order. `observed_ids` is not a read receipt.
5. Compare properties within their authority domain. Compose product outcomes with architectural
   constraints instead of applying a universal precedence ladder.
6. Use the consequence gate when properties cannot compose, architecture makes the outcome
   infeasible, or temporary underdelivery lacks acceptance.
7. Apply accepted proposals to `.intent/decisions/<scope-root>/<id>.yml` with `status: active`.
   Move replaced entries to `.intent/history/<scope-root>.yml`; discard rejected or advisory
   proposals from active state while Git retains their history.
8. Remove processed proposal files and empty proposal directories.
9. Recompile affected briefs and rerun landing checks.

Deleted anchors alone do not make a decision obsolete. Re-anchor a still-governing semantic
property. Retire it only when the property no longer applies.

Leave changes unstaged unless `--stage` is explicit, and then stage only files owned by this
operation. Integration writes are governed by `intent-land`, repository execution mode, and the
current task authorization. No mode authorizes a push or external side effect.
