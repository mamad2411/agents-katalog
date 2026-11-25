---
name: core-feature
description: Initialize a new feature branch, prepare the development plan, and set up tracking.
---

Feature to implement: $ARGUMENTS

> This is the single-agent path. For a multi-agent, harness-tracked feature (parallel analysis, build/test/review loop, `./harness start`/`verify` lifecycle), use [workflow-feature](../workflow-feature/SKILL.md) instead.

Gather project context:

```bash
git log --oneline -5
git status
find . -name "*.md" -maxdepth 2 | head -5
```

Follow this workflow:

1. **Clarify** — If the requirement is ambiguous, ask at most 2 focused questions before continuing.
2. **Design** — Briefly describe the approach: what files change, what new code is needed, what stays the same. Get confirmation before writing code.
3. **Implement** — Write the code. Follow existing patterns in the codebase — don't introduce new abstractions unless necessary.
4. **Test** — Run existing tests. Add tests for the new behavior.
5. **Summary** — List files changed and what each does. Note any follow-up work.

Don't add features beyond what was asked. Don't refactor unrelated code.
