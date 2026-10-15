---
name: flow-debug
description: Investigate bugs before fixing. Write a RED test that confirms the issue, then stop. Invoke with /flow-debug.
disable-model-invocation: true
---

# Flow Debug

Find root cause. **Do not fix.** End with a failing test that proves the bug; then hand off to `/flow-patch`.

```
NO FIXES WITHOUT ROOT CAUSE FIRST
NO PRODUCTION FIXES IN THIS SKILL
```

## 1. Investigate

- Reproduce; read full errors/stacks
- Check recent changes (`git log`, diff)
- Trace to the real trigger — do not guess

## 2. Confirm with RED

Write the narrowest failing test (or substitute) that fails because of the bug. Follow `flow-shared/references/tdd-red-green.md` (RED only — stop before GREEN).

Resolve `flow-shared` via path resolver in `flow-shared/SKILL.md`.

## 3. Stop

Report: root cause, evidence, path to the RED test. Tell the user to invoke `/flow-patch` to fix (micro-spec should include making that test green).
