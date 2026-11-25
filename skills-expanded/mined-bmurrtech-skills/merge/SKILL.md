---
name: merge
description: >
  Safely integrate a chosen GitHub PR under repository-enforced gates with
  expected-head guard and safe cleanup; hard-stop if required maintenance is
  missing on the reviewed head. Use when the user asks to merge a PR, land a
  branch, or submit to the merge queue.
disable-model-invocation: true
---

# merge

Integrate reviewed work the user actually intends. Owns PR selection, gate
evaluation, merge/queue submission, and safe cleanup — not committing new
product changes (use **`commit`**) and not cutting releases (use **`release`**).
Never mutates a reviewed head to fix missing maintenance.

## Workflow

### 1. Resolve the PR

Selection order:

1. Explicit PR number or URL
2. Explicit branch
3. Unambiguous task context
4. Current checkout only as a *hint* when it maps to exactly one open PR

If multiple candidates remain → ask. Do not guess. Never treat checkout alone
as selection.

**Done when:** one PR (base, head, head SHA) is identified.

### 2. Readiness + gates

Refresh PR metadata. Collect: draft state, mergeability, conflict status,
required checks/reviews, requested-changes, conversation-resolution rules,
merge queue, permitted strategies. See
[references/merge-policy.md](references/merge-policy.md).

Hard-stop on any **GitHub-enforced** blocking state. Surface material
**advisory** review findings (optional bots, unresolved non-required threads)
before proceeding — report them; do not invent gates.

**Maintenance check:** apply
[references/maintenance-check.md](references/maintenance-check.md). On miss →
**hard-stop**; route through **`commit`**. Do **not** edit the PR head; do
**not** auto-invoke upkeep inside merge. After maintenance lands, re-enter from
step 1.

If intended *local* (uncommitted) product changes still need committing → invoke
**`commit`** first; then re-enter from step 1.

**Done when:** required gates green (or blockers reported and stopped); advisory
findings listed; maintenance OK or hard-stopped.

### 3. Merge or queue

Capture current head SHA. Default **squash** unless policy requires otherwise.
If a merge queue is required → submit to queue (queued ≠ merged).

```bash
gh pr merge <PR> --squash --match-head-commit <EXPECTED_SHA>
```

(Adjust flags to match permitted method.) If head changed → stop; refresh;
reevaluate. Never carry authorization across a new head.

**Done when:** merged **or** queued state reported with resulting SHA when known.

### 4. Cleanup

Only after merge is confirmed. Delete review branch when safe per
[references/cleanup.md](references/cleanup.md). Sync local canonical without
destructive reset. Preserve unique local commits.

**Done when:** cleanup done or explicitly deferred with reason.

## Boundaries

- Do not run a second independent AI code review of the diff.
- Do not invent merge gates from optional bot comments.
- Do not mutate the reviewed head for missing maintenance — stop and route to
  **`commit`**.
- Do not auto-invoke **`upkeep`** / **`roadmap`** inside merge.
- Never admin-bypass, `--force`, `reset --hard`, or `clean -fd` as routine.
- Do not treat “merge” invocation alone as proof of success — verify GitHub state.
