---
name: dead-code
description: Finds unused functions, variables, exports, and dependencies across the codebase
user-invocable: true
allowed-tools: Bash Grep Glob Read
effort: medium
---

## Dead Code Analysis

1. Find unused exports (TypeScript/JS):
```bash
npx ts-prune 2>/dev/null || npx unimported 2>/dev/null || echo "Running manual search"
```

2. Manual search for likely dead code:
```bash
# Exported but never imported
grep -r "^export " src/ --include="*.ts" -l | head -20

# Functions defined but never called
grep -r "^function \|^const .* = (" src/ --include="*.ts" | head -30
```

3. For each candidate, verify by searching for all usages across the codebase.

4. Report categories:
   - **Safe to delete**: confirmed zero usages
   - **Probably dead**: only used in tests or commented-out code
   - **Keep**: used dynamically or via reflection

5. For safe-to-delete items: ask confirmation, then remove.

Never delete code you're not certain about - mark uncertain items with `// TODO: verify unused`.
