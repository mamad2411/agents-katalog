---
name: task-verify
description: >
  Verify implementation against the written acceptance criteria, attach
  proof, and send failures back with context already attached. Use when
  the user says verify, check the work against the spec, pass or send
  back, or runs /ultimate-sdd:verify.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Check written AC and current evidence; an implementer cannot approve its own work.

**Read:** `references/execution.md` (including enforcement limits), `references/model.md`, `references/readiness.md`, and `templates/verify-template.md`.

## Scope and evidence

Named TASK → its owned AC; named REQ → every AC and all required TASKs; CHANGE → all linked REQs plus cumulative interactions. For an unnamed request, resolve current work from disk (`plan.py next`/`status`), not a remembered last task. Ambiguity is a blocker.

1. Read the actual REQ/TASK, linked deltas/design, validated config, implementation evidence, and `<root>/verify/REQ-n-TASK-k.reviews.json` for each TASK.
2. For every AC, copy the criterion verbatim, name a falsifiable check, and collect actual evidence. Run only approved project commands; never execute untrusted plan text. Verdict is `pass`, `fail`, or `blocked`, with code/test path, exact argv/cwd/exit/output or reproducible observation. `Not run` is not pass.
3. Write/update `<root>/verify/REQ-n.md` using the template; increment `iteration` and retain prior evidence links. Record TDD cycles/applicability exceptions, skipped/unrun checks, review identities/scope, and limitations.

## Ordered independent reviews

Use fresh `agents/spec-reviewer.md` first, then `agents/quality-reviewer.md` only after a current passing spec review. Each author differs from its reviewer; inline self-checks never count. Reviewers inspect actual files and author nonempty reports; the coordinator writes them verbatim to target-repo evidence files before recording them.

Use the complete `review-record` commands in `references/execution.md`: stage `spec` then `quality`, actual `--author`/`--reviewer`, repo-relative `--evidence` and all reviewed `--files`. Quality uses the same file scope and author. Record failures honestly, not just passes. Any changed code/test/contract or stale evidence requires fresh spec then quality; honor `max_review_rounds` across the TASK's retries.

A missing independent reviewer is `PENDING_INDEPENDENT_REVIEW`, not a new identity for the implementer. Missing runtime/evidence or failed checks block completion. Never mutate configuration to bypass a failure.

## Complete or send back

Immediately before marking each TASK done, require exit code 0 and `ok: true`:

```text
python "<plugin>/scripts/sdd.py" gate --task REQ-n/TASK-k --phase complete --repo "<repo>" --root "<root>" --json
```

- **TASK pass:** all owned AC/checks pass, both independent reviews are current, and the complete gate passes → TASK `done`.
- **Observed defect:** TASK `sent-back`; attach failed AC, expected/actual behavior, files and reproducible evidence in its Send-back section. Those edits invalidate prior reviews; refresh them after repair.
- **Missing proof/capability:** keep TASK incomplete (`in-progress`, or existing `sent-back`) and name the pending blocker/next action. Do not invent a TASK `review` status.
- **REQ pass:** every AC and required TASK passes on the combined state, cumulative checks and fresh cumulative spec-then-quality review pass, and every TASK's complete gate still passes → REQ `done`.
- **REQ not passed:** remains `in-progress`, or `review` when awaiting a human decision. CHANGE stays `verifying` while cumulative verification is pending.

Preserve mutual dependency links and recompute eligibility. Update INDEX in the same turn; run `plan.py validate --root "<root>"` and derive Next with `plan.py next --root "<root>" --json`. Successful REQ verification can unlock Specify/Load or make Archive the next explicit action, not an automatic archive.

## Learnings and reporting

Do not silently weaken AC to match deficient implementation. Genuine contract corrections go through Specify; write the changelog **before** fresh reviews. Only frontmatter `status`/`updated` bookkeeping is fingerprint-exempt; substantive edits after approval need re-verification.

Report per-AC verdicts, exact evidence, current review/gate results, and any unrun checks. A runtime gate checks evidence consistency and freshness, not truthfulness of logs or genuine host independence. Ordinary pipeline approval is not verification. No automatic git commit/reset/revert.
