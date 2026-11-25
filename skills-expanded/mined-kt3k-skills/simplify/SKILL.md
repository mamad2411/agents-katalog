---
name: simplify
description: |
  Read source code and find opportunities to simplify, deduplicate, and consolidate.
  Apply changes after user approval.
---

### Arguments (optional)

- `<scope>`: A file path, directory, or free-form description of the range to
  review (e.g. `src/foo.ts`, `the auth module`, `lines 100-200 of bar.py`).

### Steps

1. **Resolve the scope**:
   - If an argument is provided, use it as the review scope.
   - If no argument is provided:
     - Check the current git branch (`git rev-parse --abbrev-ref HEAD`).
     - If the current branch is not main (e.g. main, master), use **Current branch diff** as the review scope.
     - Otherwise, ask the user explicitly which scope to use,
       using `AskUserQuestion` with these options:
       - **Whole codebase** — review all source code in the repository
       - **Current branch diff** — review changes in the current branch vs the main branch
       - **Last commit** — review changes in the most recent commit (`git show HEAD`)
       - **Other** — let the user specify a custom scope (free-form input)
   - Do NOT proceed until the scope is determined.

2. **Review**: Read the source code in the resolved scope and identify areas
   that can be simplified, duplicated parts, and opportunities for refactoring
   or abstraction.

3. **Apply changes after user approval.**
