---
name: fix
description: Bug-fix fast lane — the entry point for fixing something already broken (a red test, a prod error, a reported defect), not building a new feature. Does the bug-specific part — reproduce as a failing test, find the root cause, write a minimal fix-plan — then hands off to the existing pipeline (/implement → /review → /security-review → /verify → /ship) so the fix rides the proven gates. The non-negotiable discipline: reproduce as a failing test FIRST, fix minimally. Opt-in; invoked explicitly. Use when something is broken and you want it fixed under the harness's gates without over-ceremonying it through /spec.
---

# /fix — reproduce first, fix minimally, ride the gates

Goal: take something that is **already broken** and fix it with discipline — capture the bug as a
failing test *before* touching the fix, scope the change to the cause, and let it flow through the
harness's existing review/verify/ship gates. The pipeline's front door (`/spec → … → /ship`) is
greenfield-shaped — it assumes you're *building*. `/harness-claude:fix` is the **parallel entry for bugs**: it
does the bug-specific work, then hands off rather than re-implementing the gates.

> **Opt-in.** Invoked explicitly; nothing auto-routes a bug here. **Git boundary:** `/harness-claude:fix` never
> commits or pushes — branch creation for non-trivial work is expected (`claude/fix-<slug>`, see
> `rules/git.md`); the fix is committed (if at all) only through `/harness-claude:ship`
> when you ask. **Reuse, don't rebuild:** the regression test goes through
> `harness-claude:tdd-guide`; review/verify/ship are the *existing* skills, not duplicated here.

## When `/harness-claude:fix`, when `/harness-claude:build-fix`
- **`/harness-claude:fix`** is for **behavioral / logic bugs** — wrong output, a crash on some input, a regression,
  a reported defect. It is reproduce-as-a-failing-test-first, then root-cause, then minimal fix.
- **`/harness-claude:build-fix`** is for **build / type / compile errors** — get the build green with a
  minimal diff. It is *not* a competitor: while fixing a behavioral bug you may call `/harness-claude:build-fix` to
  keep the build green mid-change. Use `/harness-claude:build-fix` alone when nothing is behaviorally wrong and you
  just need the compiler/types happy.

## How it works
```
reproduce (RED test)  →  root cause  →  minimal fix-plan  →  hand off to /implement  →  /verify → /ship
```

## Do this
1. **Branch, then reproduce — capture the bug RED.** Apply branch-at-first-write
   (`rules/git.md`) before the test file lands: not a git repo → skip silently; already on a
   non-default branch → stay there; on the default branch with non-trivial work → create
   `claude/fix-<slug>` first (never commit or push — that stays gated behind your explicit
   ask). Then, before writing any fix, produce a **failing test**
   that exercises the reported behavior and fails for the *right* reason. Run it; confirm it's RED.
   If a reliable automated repro genuinely isn't possible (e.g. needs real hardware, an external
   outage), say *why* and record concrete **manual repro steps** instead — never skip the repro
   step silently.
2. **Find the root cause, not the symptom.** State the actual defect and *why* it produces the
   reported behavior. A patch that makes the symptom disappear without naming the cause is not a
   fix — it's a guess. Use `mgrep` / the knowledge graph to trace the failing path to its origin.
3. **Write a minimal fix-plan.** The smallest change that turns the RED test GREEN, scoped to the
   cause. **No refactor-while-you're-in-there** — unrelated cleanup belongs to `/harness-claude:refactor-clean`,
   not here. If the only correct fix is a design change, stop and return to
   `/harness-claude:architect` or `/harness-claude:plan` rather than hacking around it.
4. **Add the repro as a durable regression test via `harness-claude:tdd-guide`.** The failing test
   from step 1 becomes a permanent test (RED → GREEN once the fix lands) so the bug can't silently
   return. This is the same TDD seam `/harness-claude:implement` opens each phase with.
5. **Hand off — do not rebuild the gates.** Pass the fix-plan + the RED regression test to
   `/harness-claude:implement` (it makes the test GREEN with the minimal change), then let the
   change ride the **existing** `/harness-claude:review` + `/harness-claude:security-review` →
   `/harness-claude:verify` → `/harness-claude:ship` gates. `/harness-claude:fix` does **not** duplicate review,
   verify, or ship.

## Security & trust
- A bug in security-sensitive code (auth, input handling, queries, file I/O, crypto, secrets) makes
  `/harness-claude:security-review` mandatory on the way out — flag it in the fix-plan so the gate
  isn't skipped. Validate the repro input at the trust boundary like any other input.
- **Git boundary holds:** `/harness-claude:fix` and every step it delegates to commit nothing unless you explicitly
  arm `/harness-claude:ship`.

## Notes
- Self-contained: a single skill that *leads* and reuses existing agents — `tdd-guide` (regression
  test), `code-reviewer` + `security-reviewer` (gates), `build-error-resolver` (build green). **No
  new agent, no new dependency, no new MCP server, no new runtime.**
- The skill *is* the lead — there is no separate fix agent (the lead logic lives here, the same way
  `/harness-claude:orchestrate` and `/harness-claude:operate` own theirs).

## Common rationalizations (don't accept these from yourself)

| Excuse | Reality |
|--------|---------|
| "The fix is obvious — a repro test is overhead" | An "obvious" fix without a RED repro is a guess with confidence. The test is what proves you fixed *this* bug. |
| "I can't easily reproduce it, so I'll just patch the likely cause" | Then say so and record manual repro steps — the fallback is explicit, never silent. |
| "While I'm in this file, I'll clean up..." | That's `/harness-claude:refactor-clean`'s job. Mixed fixes make the regression bisect-proof. |
| "The symptom is gone, ship it" | A disappeared symptom with an unnamed cause reappears wearing a different stack trace. |

## Red flags — stop and re-check
- You wrote fix code before the repro test existed.
- The repro test passes before the fix lands (it's not reproducing the bug).
- The fix-plan touches more files than the root-cause statement explains.
- The bug is in security-sensitive code and the fix-plan doesn't flag `/harness-claude:security-review`.

## Exit criterion
A failing test reproduced the bug (or manual repro steps were recorded with the reason automation
wasn't possible), the root cause was named, a minimal fix-plan was written, and the fix was handed
to `/harness-claude:implement` to ride the existing verify/ship gates — never a symptom-patch without
a repro, and never a duplicated gate.
