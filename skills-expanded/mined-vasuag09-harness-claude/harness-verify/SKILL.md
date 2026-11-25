---
name: harness-verify
description: Orchestrate the entire VERIFY phase — code review, security review, tests, run-the-app verification, and ship-prep. Use after /harness-implement. Sequences the Verify skills, runs reviewers in parallel when sensible, halts on Critical/High findings, and stops at the git boundary.
---

# /harness-verify — run the Verify phase

Thin orchestrator over the Verify skills. Goal: prove the change is production-grade
before it can merge.

## Sequence

1. **Review** — run `/harness-claude:review` (delegate to `harness-claude:code-reviewer`); for any
   change touching auth/input/queries/files/external-calls/crypto/secrets, also
   `/harness-claude:security-review` (delegate to `harness-claude:security-reviewer`); and for any
   change that **touched a user-facing surface** (UI/page/screen/component/form/mobile/CLI-TUI),
   also `/harness-claude:design-review` (craft + a11y/UX gate). Run the applicable reviewers **in
   parallel**; skip the ones that don't apply and say so.
   → **HALT on any Critical/High (security/correctness) or Blocker (design) finding** — fix,
   then re-review the changed lines.

2. **`/harness-claude:test`** — run the full suite (in tmux if long) + coverage. Every acceptance
   criterion must have a test; coverage ≥ 80% on changed code. Add missing tests via
   `harness-claude:tdd-guide`.

3. **`/harness-claude:verify`** — launch the app/feature and **observe each acceptance criterion working**
   in reality (browser screenshot for web; exercise unhappy paths). Tests passing is
   necessary, not sufficient. Anything tests missed → add a regression test (back to step 2).

4. **`/harness-claude:ship`** — sync docs, draft the change summary from the full diff, confirm
   build/types/lint/tests green and no secrets/debug logs.
   → **HALT at the git boundary:** do NOT commit/push/PR. Report "ready — say the word."

## Rules
- Block, don't warn, on Critical/High security or correctness findings, or design Blockers.
- If a secret is exposed: stop, rotate, sweep for siblings.
- Never run git write operations unless the user explicitly asks.

## Output
Verify summary: review verdict, security verdict, design verdict (or "skipped — no UI surface"),
coverage %, observed-working evidence, docs synced, "ready to commit/PR." Then optionally
`/harness-claude:harness-maintain`.
