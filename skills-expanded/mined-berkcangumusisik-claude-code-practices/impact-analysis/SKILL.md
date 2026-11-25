---
name: impact-analysis
description: Analyzes the impact of changing a file or function - what else would break
argument-hint: <file-path> [function-name]
user-invocable: true
allowed-tools: Grep Read Glob Bash
effort: medium
---

## Impact Analysis

Target: **$1** $2

1. Find all direct consumers:
```bash
grep -rn "from.*$1\|require.*$1\|import.*$1" src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
```

2. For each consumer, find their consumers (2 levels deep):
```bash
# For each file found above, repeat the grep
```

3. Check for indirect usage:
   - Dynamic imports: `import()`
   - Re-exports: files that `export * from`
   - Type-only imports that might break at runtime

4. Check test coverage of the target:
```bash
grep -rn "$2\|$(basename $1 .ts)" src/ --include="*.test.*" --include="*.spec.*"
```

5. Produce impact map:
```
src/auth/token.ts → changing this affects:
  DIRECT (3 files):
    src/middleware/auth.ts      ← critical path
    src/api/users.ts           ← medium risk
    src/utils/session.ts       ← low risk
  INDIRECT (7 files via middleware/auth.ts):
    src/api/*.ts               ← all protected routes
  TESTS (2 files):
    src/auth/token.test.ts
    src/middleware/auth.test.ts
```

6. Recommend: what tests to run, what to manually verify.
