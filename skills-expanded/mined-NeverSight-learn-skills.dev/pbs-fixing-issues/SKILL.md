---
name: pbs-fixing-issues
description: "Use when phase validation or code review found blockers that must be fixed with minimal, surgical changes"
---

# Fixing Issues

## Overview

Fix a specific blocker with the absolute minimum change. This is a surgical patch — not an opportunity to improve, refactor, or clean up.

**Core principle:** Fix the issue. Only the issue. Nothing else.

**Announce at start:** "I'm using the pbs-fixing-issues skill to fix: [issue description]."

## The Iron Law

```
THIS IS A PATCH — MINIMUM CHANGE ONLY.
NO REFACTORING. NO IMPROVING. JUST FIX THE ISSUE.
```

## Input

- Phase spec: `.pbs-framework/phases/phase-XX/spec.md` (for context)
- Issue description: from the validation report or code review findings
- Relevant code files: identified from the issue description

## The Process

1. Read the phase spec: `.pbs-framework/phases/phase-XX/spec.md` (for context)
2. Read the issue description provided by the human
3. Identify the **root cause** — not the symptom
4. If no test covers this case:
   - **REQUIRED:** Use superpowers:test-driven-development — write the failing test first
5. Implement the minimum fix to resolve the root cause
6. **REQUIRED:** Use superpowers:verification-before-completion — run ALL validation commands, not just the ones related to the fix
7. Report:
   - **Root cause:** what was actually wrong
   - **What changed:** files modified with one-line descriptions
   - **Validations:** all commands pass (with actual output)

<HARD-GATE>
Do NOT commit the fix. The human reviews the diff and the report first.
Present the fix report, then WAIT for the human to approve before any commit.
This applies regardless of how obvious the fix appears.
</HARD-GATE>

## Common Mistakes

- **Fixing the symptom, not the root cause** — a symptom fix will resurface. Trace to the root cause.
- **Expanding the fix scope** — "while I'm here" is the enemy. Fix ONLY the reported issue.
- **Not writing a regression test** — if no test covers the bug, write one first (TDD). Otherwise the bug will return.

## Red Flags

- "While I'm here, let me also..." → NO. Only the fix.
- "Let me refactor this for clarity" → NO. Patch only.
- "This other file needs the same fix" → Only if strictly necessary for THIS issue.
- "I should add error handling here too" → Is it the reported issue? If not, report it separately.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This refactor prevents the bug from recurring" | Report it as a suggestion. Don't do it now. |
| "It's just one extra line" | One extra line is still scope creep. |
| "The code around the fix is messy" | Messy code that works is not your problem right now. |

## Integration

**Called by:**
- pbs-phase-validation — for each blocker found
- Requesting code review — for blockers found in review

**Required skills:**
- **REQUIRED:** superpowers:test-driven-development — test first if no test exists
- **REQUIRED:** superpowers:verification-before-completion — verify all validations pass

**After fix:**
- Re-run pbs-phase-validation to verify the fix didn't break anything else
