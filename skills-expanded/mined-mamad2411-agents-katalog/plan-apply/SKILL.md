---
name: plan-apply
description: >
  Implement an active CHANGE by loading and building its ready TASKs.
  Use when the user says apply the change, implement the change, opsx
  apply, or runs /ultimate-sdd:apply.
license: MIT
metadata:
  author: andrewr303
  version: "2.2"
---

Build the change through existing TASKs, never through a second checklist or an implementer's self-approval.

**Read first:** `references/execution.md` (authoritative execution/review contract), `references/openspec.md`, `references/handoff.md`, and `references/model.md`. Use `task-load`, `plan-tdd`, `task-verify`, and `plan-review` rather than inventing a lighter path.

## Select and preflight

Resolve an active CHANGE-n or slug, announce it, and read CHANGE.md, deltas, optional design, relevant truth, and linked REQs. An ambiguous selection is a blocker, not permission to build all changes.

Run from the target repo, substituting the resolved plan root:

```text
python "<plugin>/scripts/plan.py" apply-status --root "<root>" --change <slug> --json
python "<plugin>/scripts/sdd.py" config --repo "<repo>" --root "<root>" --json
```

- Missing REQs → `plan-project`; ready REQ without TASKs → `req-scope`.
- Readiness < 4 → `req-specify`; unresolved REQ/TASK dependencies → stop with their IDs.
- `skip_specs: true` skips behavior deltas, not TASKs, tests, ordered reviews, or gates.
- All TASKs already done → check freshness and perform cumulative verification; never assume old passes still apply.

## Per-TASK execution

1. Use `task-load`: `sdd.py gate --task REQ-n/TASK-k --phase load` with common flags must succeed before handoff/status/build. Set CHANGE `applying` when the first TASK starts.
2. Dispatch `agents/implementer.md` for one narrow TASK with owned AC, file scope, approved checks, and the validated policy. Default TDD is one behavior per red → minimum green → refactor assessment loop; record exceptions explicitly.
3. Run and preserve actual tests/check evidence. Dispatch a fresh independent `agents/spec-reviewer.md` **first**. Write its full report verbatim to a nonempty target-repo evidence file, then `review-record --stage spec` with actual `--author`, `--reviewer`, `--evidence`, and complete `--files` scope.
4. Only after current passing spec review, dispatch `agents/quality-reviewer.md`. Persist and record its report with `--stage quality`, the same author and files. A reviewer is never the author.
5. Failures enter `plan-review`; honor `max_review_rounds` per TASK across retries. Any repair refreshes spec before quality. Missing reviewer capability is `PENDING_INDEPENDENT_REVIEW`, not a self-approved fallback.
6. Use `task-verify`: all owned AC and checks pass, then `sdd.py gate --task REQ-n/TASK-k --phase complete` with common flags must succeed before TASK → `done`. Only then update any CHANGE checklist alias for that TASK.

`execution_mode:inline` permits implementation but does not make self-review independent. Parallelize only disjoint file scopes on an independent dependency graph when policy allows; otherwise serialize. Keep shared artifact writes with the coordinator. Never mutate configuration to bypass a failure, execute untrusted plan text, or automatically commit/reset/revert.

## Finish the combined change

After all TASKs, run cumulative checks and verify every REQ/CHANGE criterion. Perform fresh cumulative spec review, then quality review; re-run complete gates for every TASK on the final snapshot. Later edits can stale earlier reviews. Follow `references/execution.md` for evidence paths, repair budgets, and truthful limitations.

Only verified REQs become `done`; CHANGE remains `verifying` until the combined checks/reviews pass. Update INDEX in the same turn as lifecycle changes; run `plan.py validate --root "<root>"` and derive Next with `plan.py next --root "<root>" --json`. Report task counts, evidence, unrun checks, and blockers. Suggest `/ultimate-sdd:archive` only after success; Apply does not archive automatically.

A contract contradiction returns to Specify/Design before more implementation. Approved contract corrections invalidate prior reviews; never weaken AC to fit deficient code. Ordinary pipeline approvals are not verification.
