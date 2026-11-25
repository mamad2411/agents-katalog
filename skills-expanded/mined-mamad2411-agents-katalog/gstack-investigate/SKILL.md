---
name: gstack-investigate
description: Systematic root-cause debugging for OPC work. Use when there is a bug, crash, regression, failing command, flaky behavior, provider issue, or unexplained output. Requires evidence before fixes.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
---

# gstack-investigate

Use this skill to diagnose before fixing.

## Workflow

1. State the observed symptom and the expected behavior.
2. Reproduce the issue with the smallest command, UI flow, fixture, or log slice available.
3. Trace the relevant path through the code before proposing a fix.
4. Form at least three plausible causes.
5. Test the causes with targeted checks, logs, assertions, or isolated commands.
6. Pick the cause with the strongest evidence.
7. Apply the smallest fix that addresses that cause.
8. Re-run the original reproduction and one nearby regression check.

## Rules

- Do not fix before reproduction or strong evidence.
- If one attempted fix fails, record why and try a different strategy.
- Prefer direct runtime evidence: command output, logs, API responses, persisted state, or failing tests.
- Keep unrelated refactors out of the fix.

## Output

Report:

- Symptom
- Root cause
- Fix
- Verification command or manual check
- Residual risk
