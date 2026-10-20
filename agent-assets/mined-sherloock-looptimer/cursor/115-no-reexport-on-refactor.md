---
description: No re-exports when moving or renaming modules; update imports to canonical path.
globs: components/**/*.tsx, components/**/*.ts, hooks/**/*.ts, lib/**/*.ts
alwaysApply: false
---

## No re-exports when refactoring (mandatory)

When moving or renaming a file (e.g. a component, hook, or util), **do not** leave a re-export file at the old path.

- **Wrong**: Move `foo.tsx` to `feature/foo.tsx`, then add `old-path/foo.tsx` that only does `export { Foo } from "@/feature/foo"`.
- **Right**: Move the file to its final location and **update every import** to the new canonical path. Delete the old file; do not replace it with a re-export.

Re-exports after a refactor add indirection, duplicate “homes” for the same symbol, and confuse where the real implementation lives. Prefer a single canonical path and explicit imports.

### What to do on move/rename

1. Move or rename the file to its final path.
2. Find all imports of the old path (grep / “Find all references”).
3. Update each import to the new path.
4. Remove the old file entirely (no re-export stub).
