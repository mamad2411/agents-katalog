---
name: type-fix
description: Fixes TypeScript type errors in a file or across the project
argument-hint: [file-path]
user-invocable: true
allowed-tools: Bash Read Edit Grep
effort: medium
---

## Fix TypeScript Errors

Target: **$1** (or entire project if not specified)

1. Get current errors:
```bash
npx tsc --noEmit 2>&1 | head -50
```

If a specific file was given, filter to that file.

2. Group errors by type:
   - `any` type leaks
   - Missing null checks
   - Incorrect return types
   - Property does not exist
   - Type mismatch

3. For each error:
   - Read the relevant code
   - Understand the actual type
   - Apply the minimal fix that maintains correctness:
     - Prefer proper types over `as any`
     - Use optional chaining `?.` for possible nulls
     - Narrow with type guards when needed

4. Show changes, ask for confirmation, apply.

5. Re-run `tsc --noEmit` to verify zero errors remain.
