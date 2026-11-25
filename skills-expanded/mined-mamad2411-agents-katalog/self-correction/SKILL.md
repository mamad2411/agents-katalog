---
name: self-correction
description: "Recognize repetitive work patterns and switch to bulk fix strategies before getting stuck in a loop. Triggers on: stuck in a loop, same error, same fix, repetitive pattern, bulk fix."
---

# Self-Correction Skill

> ⚠️ **Recognize repetitive work patterns BEFORE getting stuck in a loop.**
>
> If you're fixing the same issue type across multiple files one-by-one, STOP and consider a bulk approach.

## Triggers

- After fixing same issue type 3+ times
- "stuck in a loop", "same error", "same fix"
- Repeating pattern detected (lint, type error, test failure)
- Agent self-check: "Am I repeating myself?"

## Applicable Agents

- **builder** — orchestrating fixes across implementation agents
- **developer** — implementing fixes across multiple files
- **overlord** — autonomous mode fix patterns

---

## Detection Triggers

You are likely in a repetitive loop when:

| Pattern | Example | Stuck Signal |
|---------|---------|--------------|
| Same test failure type | `launchElectronApp` usage bug in 8 test files | Fixing files 1, 2, 3... individually |
| Same lint error | Missing import across 15 files | Running lint → fix → lint → fix |
| Same type error | Interface mismatch after refactor | Updating files one at a time |
| Same pattern change | Renaming a function/variable | Find-and-replace manually file by file |

---

## Self-Check Protocol

After fixing the same issue type 3 times, pause and ask yourself:

```
LOOP CHECK:
1. Am I fixing the same issue type repeatedly?
2. How many more files likely have this issue?
3. Can I grep/search to find ALL instances at once?
4. Would a bulk fix be faster than continuing one-by-one?
```

If the answer to #4 is YES, switch to bulk fix protocol.

---

## Bulk Fix Protocol

When you detect a repeating pattern:

1. **STOP** the current one-by-one approach
2. **Search comprehensively** for all instances:
   ```bash
   # Example: Find all files with the broken pattern
   grep -r "launchElectronApp" tests/ --include="*.ts" -l
   ```
3. **Assess the scope** — how many files, how similar are the fixes?
4. **Choose the right strategy:**

| Scope | Strategy |
|-------|----------|
| 2-3 files | Continue one-by-one (it's fine) |
| 4-10 files | Batch into 2-3 groups, fix each group together |
| 10+ files | Use find/replace, sed, or codemod; fix ALL at once |

5. **Fix all instances** before running tests again
6. **Run the full test suite** once at the end, not after each fix

---

## Good vs Bad Approach

**Bad (what triggers the loop):**
```
Fix test1.ts → run tests → Fix test2.ts → run tests → Fix test3.ts → run tests...
(8 cycles later, user asks "are you stuck?")
```

**Good (bulk approach):**
```
Grep for pattern → Found in 8 files → Fix all 8 files → Run tests once → Done
```

---

## Reporting to User

When you recognize you were in a loop and switch to bulk:

```
📊 PATTERN DETECTED — SWITCHING TO BULK FIX

I've been fixing the same issue individually. Let me step back:

• Pattern: `launchElectronApp` used incorrectly (assigning result instead of destructuring)
• Scope: Found in 8 test files
• Approach: Fix all 8 files at once, then run full test suite

This will be faster and more reliable than continuing one-by-one.
```

---

## Integration with Fix Loops

When implementing a "fix loop" (e.g., 3 attempts to fix a test):

1. **Each attempt counts** — don't loop forever
2. **Self-check after 3 attempts** — is this the same root cause?
3. **If same root cause**: Apply bulk fix, not another individual attempt
4. **If different causes**: Continue individual attempts, but escalate after 3

### Fix Loop Escalation

After 3 failed fix attempts with no progress:

```
═══════════════════════════════════════════════════════════════════════
                    ❌ FIX LOOP EXHAUSTED
═══════════════════════════════════════════════════════════════════════

Failed after 3 fix attempts.

Attempted fixes:
  1. [description of fix 1]
  2. [description of fix 2]
  3. [description of fix 3]

Options:
  [M] Fix manually, then type "retry"
  [S] Skip this item
  [D] Debug with @developer

> _
═══════════════════════════════════════════════════════════════════════
```
