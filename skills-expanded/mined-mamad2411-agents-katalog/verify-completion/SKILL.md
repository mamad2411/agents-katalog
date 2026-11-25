---
name: verify-completion
description: Decide whether a task actually met its Goal and Acceptance Criteria with real evidence at the required Evidence Level, not whether the note merely looks finished
---

# Verify Completion

Decide whether the work for a task **actually** met its Goal and Acceptance Criteria — with real evidence — not whether the note looks finished. This is **Layer 8: Evidence / Reality Check** of `docs/specs/kurosawa-thin-harness-architecture.md` (§16); the repo-specific Evidence Level mapping is in `docs/specs/evidence-policy.md`.

## When to use
- After `execute-task` / `reconcile-task`, before moving a task to `done/`. Also to audit a task already marked done.

## Evidence Level (the bar for "done")

| Level | Name | What counts | Use for done? |
|---:|---|---|---|
| 0 | Claim Only | the agent's description | never sufficient |
| 1 | Static | diff / actual file / type check | docs-only / trivial |
| 2 | Test | test command + output, failing-before/passing-after | **standard minimum** |
| 3 | Runtime | local run / API response / log / DB outcome | integration & behavior |
| 4 | Production | production log / monitoring / canary / rollback ready | production impact — owner approval required |

Rule: **Done requires Evidence Level ≥2 unless the task is docs-only.** Production-impacting changes require Level 4 + owner approval. Claim Only is never proof (§16.3, §22.6).

## Steps

1. Read the task's Goal, Scope, and Acceptance Criteria. If criteria are missing or not observable, stop — you cannot certify done; bounce to `review-task` / `scan-decisions` to define them.
2. Turn each acceptance criterion into a concrete check (command, test, query, or file inspection).
3. Gather evidence for each and record the Evidence Level reached. Prefer durable outcome over process success: a command/workflow exiting 0 is **not** proof — verify the durable result (DB outcome / coverage, file state, projection) per `docs/06_error_policy.md` and the invariant "workflow success is not sufficient; DB outcome coverage is required."
4. Apply `check-claims` discipline: cite `file:line` or command output for every PASS. Mark anything unproven as UNVERIFIED, not PASS.
5. Check scope: nothing out-of-scope was silently changed; nothing in-scope was skipped.
6. Give a verdict per criterion (PASS / FAIL / UNVERIFIED), the Evidence Level reached, and an overall verdict. If the level is below the bar for the task, it is NOT DONE.

## Durable outcomes to check (news-app — Evidence Level 2–3 examples)

A command/log saying "OK" is not enough. Prefer at least one of these, matched to the work:

- collection: target rows actually increased; no duplicates introduced.
- notification: `notification_sent_at` / log row set; no duplicate sends.
- signal/AI: result row persisted with model / prompt version / status.
- cleanup: rows removed match the prior dry-run count.
- projection: public-read rows synced and within retention.
- docs: source-of-truth doc updated in the same change.

## Verdict
- **DONE** — all criteria PASS with cited evidence.
- **NOT DONE** — any FAIL; list what is missing.
- **UNVERIFIABLE** — criteria absent/unobservable, or proof needs access you lack; state what is needed.

## Rules
- Do not certify DONE without observable evidence. "It should work" / "build passed" is not done.
- Workflow / command success ≠ goal reached. Check the durable outcome.
- Do not move a task to `done/` on a NOT DONE / UNVERIFIABLE verdict.
- No guessing — unproven means UNVERIFIED.

## Output
- Per-criterion table: criterion | check | evidence | verdict
- Overall verdict (DONE / NOT DONE / UNVERIFIABLE)
- Remaining gaps / Next Proof Needed
- Recommendation: move to `done/` or keep active
