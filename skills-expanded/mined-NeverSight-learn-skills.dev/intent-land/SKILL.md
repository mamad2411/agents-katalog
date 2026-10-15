---
name: intent-land
description: Verify and locally merge completed Git work units in dependency order, reconcile concurrent intent proposals, handle conflicts against routed contracts, and release runtime claims under the configured execution mode.
---

# intent-land

Landing is the convergence operation for one unit or an `intent-plan` graph. A successful landing
leaves the local integration branch verified, intent state coherent, and runtime coordination
released.

## Invocation

```text
/intent-land [unit-or-plan] [--stage-intent]
```

## Preconditions

Resolve execution mode and integration branch from `.intent/config.yml`, then `origin/HEAD`, then
`main`, `master`, `trunk`, or `develop`. Report the source. Preserve unrelated dirty work; stop if
the target worktree cannot be updated safely.

For every unit:

1. Run `intent-check --landing` against the unit goal, scope, and diff.
2. Verify routed contracts and repository-defined checks.
3. Confirm no exception is expired, silently introduced, or falsely discharged.
4. Confirm every durable intent write passes `intent-capture` admission.
5. Reconcile genuinely concurrent proposals. A lone serial proposal should be converted to an
   ordinary active decision or rejected, not treated as a reconciliation ceremony.

## Order and merge

Use dependency edges from the runtime plan. Without a plan, derive only the dependencies needed
for the named units. Merge contract-setting nodes before their consumers and re-run affected
integration checks at every convergence point.

- `advisory`: report exact update, merge, verification, and cleanup commands without executing.
- `assisted`: prepare verified branches and ask once before the first integration-branch merge.
- `autonomous`: perform bounded local updates and merges when the consequence gate passes.

No mode authorizes push, deployment, publication, external mutation, force update, destructive
cleanup, or discarding unrelated changes.

If Git conflicts, use `intent-resolve`. Compose adjacent, compatible, and structural changes
against routed contracts. Ask one human question only for a consequential semantic contradiction.
Do not choose `ours` or `theirs` by branch role.

After each merge, recompile affected briefs and run integration verification. Stop on a broken
contract or newly exposed consequential conflict; do not continue merging dependent units into a
known-bad base.

## Completion

Release completed claims and delete completed runtime plan files. Remove worktrees only when they
are clean, merged, and no longer needed; prefer a recoverable cleanup and never delete unrelated
work. Report the local integration ref, merged units, verification, remaining exceptions,
released claims, and any intentionally retained worktrees.
