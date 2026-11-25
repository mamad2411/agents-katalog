---
name: debug-root-cause
description: Use for bugs, flaky behavior, crashes, broken UI, incorrect state, or inconsistent platform behavior. Investigate evidence first and fix the actual cause across Swift, Kotlin, Flutter, Tauri, Rust, and frontend code.
---

# Debug Root Cause

## Use when
- behavior is wrong, flaky, crashing, visually broken, or inconsistent
- the task is to explain and fix a failure chain rather than add new product behavior
- the user needs root-cause analysis, not symptom masking

## Do not use when
- the main task is greenfield feature implementation
- there is no concrete failure to investigate

## Working rules
- Do not patch before you can explain the broken invariant.
- Separate symptom, trigger, and root cause.
- Prefer deterministic reproduction or the strongest evidence available in the repo.
- Check state ownership, lifecycle, async ordering, serialization, configuration, and environment mismatches before editing.
- Remove temporary debug instrumentation unless the user explicitly wants it kept.

## Workflow
1. Define observed behavior, expected behavior, and reproduction conditions.
2. Gather evidence from code, logs, traces, recent changes, and platform constraints.
3. Rank the smallest set of plausible hypotheses.
4. Disprove the top hypotheses with the minimum checks needed.
5. Fix the root cause at the narrowest correct layer.
6. Add regression protection with a test or explicit validation step.

## Quality bar
- The final explanation names the broken invariant.
- The fix restores the invariant instead of hiding the symptom.
- Adjacent flows likely to regress from the same cause are checked before closeout.

## Reference routing
- Read `references/debug-checklist.md` for the investigation checklist.
- Read `references/release-quality-gates.md` when the bug affects a user-critical or release-critical flow.
- Read `references/official-docs.md` only when platform semantics or API guarantees matter to the diagnosis.

## Output contract
Provide:
- reproduction summary
- top hypotheses considered
- confirmed root cause
- implemented fix
- validation or regression protection added
- real remaining risk
