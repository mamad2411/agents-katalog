---
name: review
description: Review changed code for quality, correctness, and maintainability before merge. Use immediately after implementing or modifying code. Delegates to the harness-claude:code-reviewer agent. First gate of the Verify phase.
---

# /review — code quality & correctness

Goal: catch bugs and quality issues before they merge.

## Do this
1. **Delegate to `harness-claude:code-reviewer`** with the diff in scope (`git diff`, `git diff
   --staged`, or the files named).
2. The reviewer checks correctness, edge cases, error handling, naming, complexity,
   duplication, adherence to harness rules, and test coverage — reporting `file:line`
   with severity.
3. Triage findings:
   - **Critical** → block, fix now.
   - **High** → fix before merge.
   - **Medium/Low** → fix when reasonable / note.
4. Apply fixes, then re-review the changed lines if Critical/High were found.

## Common rationalizations (don't accept these from yourself)

| Excuse | Reality |
|--------|---------|
| "The diff is tiny — review would be ceremony" | Small diffs cause outsized breakage precisely because nobody looks. The reviewer is cheap; the regression isn't. |
| "I just wrote it, so I know it's correct" | The author is the worst-placed reviewer. That's the whole reason this gate delegates to a fresh-context agent. |
| "It's only a High, and the user is waiting" | High means fix **before** merge. Speed pressure is when gates earn their keep. |
| "I'll batch the findings with the next change" | Deferred findings become permanent. Fix now while the context is loaded. |

## Red flags — stop and re-check
- You summarized the diff to the reviewer instead of giving it the actual diff.
- The review returned zero findings on a non-trivial change (suspicious, not reassuring).
- Critical/High fixes landed but the changed lines were never re-reviewed.

## Exit criterion
No Critical or High findings outstanding. Then `/harness-claude:security-review` (or run both in
parallel if the change is security-sensitive).
