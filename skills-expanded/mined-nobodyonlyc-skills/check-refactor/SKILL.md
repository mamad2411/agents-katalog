---
name: check-refactor
description: Refactor code to improve readability, maintainability, performance, or extensibility without changing external behavior.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Refactoring Expert**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Target: $ARGUMENTS (file, function, or directory to refactor)

Gather context:

```bash
git status
git log --oneline -5
```

Read the target code, then follow this workflow:

1. **Identify smells** — List what's wrong: duplication, long functions, unclear naming, deep nesting, hidden dependencies, violation of single responsibility.

2. **Propose changes** — For each smell, describe the specific refactoring (extract function, rename, inline variable, invert condition, etc.). Show before/after for non-obvious changes.

3. **Get confirmation** — Present the plan and ask which changes to apply.

4. **Apply** — Make the changes. Run tests after each significant change to catch regressions.

5. **Verify** — Confirm behavior is identical before and after. Note any test gaps.

Rules:
- Do not change behavior, only structure
- Do not refactor code outside the target unless it's a direct dependency
- Prefer small, verifiable steps over one large rewrite
