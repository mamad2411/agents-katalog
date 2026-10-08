---
name: code-style-review
description: Helps users code style review.
---

Review the following code for practical style issues.

If the target language is known, also read `lang/<language>.txt` when present and apply those language-specific review points in addition to this base guidance. If no such file exists, continue with the base guidance only.
If the deployment environment is known, also read `environment/<environment>.txt` when present and apply those environment-specific review points in addition to this base guidance. If no such file exists, continue with the base guidance only.

Focus only on issues that materially improve readability, consistency, maintainability, safety of change, or make failure handling / assumptions easier to notice.
Ignore personal preference, formatting trivia, cosmetic comments, and low-value suggestions.

Treat something as an "issue" only if it is likely in practice to:
- cause misunderstanding, misuse, or operational mistakes
- hide bugs, failure paths, side effects, or assumptions
- make future changes risky or unnecessarily difficult

Consider especially:
- readability: naming, structure, control flow, nesting, unclear intent
- consistency: conventions, similar logic written differently, uneven error handling or returns
- maintainability: duplication, hard-coded values, unclear responsibilities, weak abstraction boundaries
- safety of change: structure that makes safe modification difficult
- practical robustness signals: only when style obscures failures, edge cases, or operational behavior

Be selective. Report only issues that matter in practice.
Report at most 3 issues.

For each issue, explain:
- what is problematic
- why it matters in practice
- severity
- which code

If there are no important issues, write under "2. Issues" exactly: none
Do not overstate certainty. If something cannot be determined from the code alone, write "unknown".
Prefer minimal, practical improvements over large redesigns.

Output format:
1. Summary
2. Issues
3. Unknowns
