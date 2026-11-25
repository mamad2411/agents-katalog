---
name: dep-graph
description: Maps module dependencies and finds circular imports and coupling issues
argument-hint: [entry-file]
user-invocable: true
allowed-tools: Bash Grep Read Glob
effort: medium
---

## Dependency Graph Analysis

Entry: **$1** (or `src/index.ts` if not specified)

1. Try dependency analysis tools:
```bash
npx madge --circular src/ 2>/dev/null | head -30
npx depcruise --include-only "^src" --output-type text src/ 2>/dev/null | head -50
```

2. Manual circular dependency search:
```bash
# Files that import each other
grep -rn "^import.*from" src/ --include="*.ts" | awk '{print $NF}' | sort | uniq -c | sort -rn | head -20
```

3. Identify:
   - **Circular imports**: A → B → C → A (breaks tree-shaking, causes runtime issues)
   - **High fan-in**: modules imported by many others (change = high risk)
   - **High fan-out**: modules that import many things (likely doing too much)
   - **Layer violations**: UI importing from DB layer directly

4. For each circular import: propose how to break the cycle (extract shared types, invert dependency, use dependency injection).

5. Draw a simplified text dependency graph for the top-level modules.
