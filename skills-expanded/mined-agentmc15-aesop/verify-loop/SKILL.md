---
name: verify-loop
description: Prove a change works before calling it done — build, test, lint, smoke-check, and report pass/fail. Use after any code change, before any commit/PR, and as the self-verify step inside an autonomous loop. Trigger whenever the agent is about to claim a task is complete.
---
# verify-loop

"Done" is a claim, not a proof. An open loop that writes code with no feedback is a machine for
generating confident mistakes. This skill is the feedback.

## Steps
1. Run the build (`AGENTS.md ## Project → Build`). If it fails, fix the cause and repeat.
2. Run the test suite (`→ Test`). For a bug fix, ensure a test reproduces the bug and now passes.
3. Run lint/format (`→ Lint`).
4. Smoke-check the changed behavior directly where feasible.
5. Where relevant, diff behavior between `main` and the change.
6. Report **PASS** or **FAIL**. On FAIL, show the minimal failing output (not the whole log) and the
   likely cause.

## Notes
- The maker shouldn't be the only checker — for risky changes, hand verification to a separate
  reviewer subagent (a stronger model). See `primitives/subagents/`.
- This is the `self_verify()` every loop in `harness/` and `loops/` depends on.
