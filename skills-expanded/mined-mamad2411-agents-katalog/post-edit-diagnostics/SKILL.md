---
name: post-edit-diagnostics
description: Run diagnostics and formatter after editing code files.
---

# Post-edit diagnostics

After each code edit, run file-scoped diagnostics for edited files.

**Why:** Type errors and unformatted code committed silently fail CI later, forcing a context-switch back to code you have already moved on from. Catching them at edit time is far cheaper. This is best enforced by a PostToolUse hook or pre-commit lint; the rule explains why it matters when no hook is configured.

- Run the project formatter on edited files (e.g. `prettier --write`).
- Treat diagnostics findings from edited files as required follow-up before unrelated work.
- Preserve file scope by default; do not broaden to whole-project scans unless asked.
- If multiple files were edited, check each edited file explicitly.

## Examples

```text
// BAD — edit three files, move on without running diagnostics
edit src/api/users.ts
edit src/api/orders.ts
edit src/utils/auth.ts
→ unformatted code committed; type error introduced silently

// GOOD — run formatter and diagnostics on each edited file before continuing
edit src/api/users.ts
edit src/api/orders.ts
edit src/utils/auth.ts
$ prettier --write src/api/users.ts src/api/orders.ts src/utils/auth.ts
$ tsc --noEmit
→ type error in auth.ts caught and fixed before commit
```
