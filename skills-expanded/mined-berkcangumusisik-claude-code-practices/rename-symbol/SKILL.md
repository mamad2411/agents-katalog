---
name: rename-symbol
description: Safely renames a function, variable, type, or class across the entire codebase
argument-hint: <old-name> <new-name>
user-invocable: true
allowed-tools: Bash Grep Read Edit
effort: low
---

## Rename Symbol

Old name: **$1**
New name: **$2**

1. Find all occurrences:
```bash
grep -rn "\b$1\b" . --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --exclude-dir=node_modules --exclude-dir=dist
```

2. Categorize occurrences:
   - Definition (function/class/type declaration)
   - Call sites
   - Type annotations
   - Imports/exports
   - Test files
   - Comments and documentation
   - String literals (flag separately - may be API contracts)

3. Show the full list. Flag any in string literals or external-facing API contracts as risky.

4. Ask for confirmation, then rename all (except flagged ones).

5. Run type check to verify:
```bash
npx tsc --noEmit
```

Report any errors introduced.
