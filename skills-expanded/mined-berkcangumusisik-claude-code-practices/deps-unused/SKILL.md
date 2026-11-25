---
name: deps-unused
description: Finds packages in package.json that are not actually used in the codebase
user-invocable: true
allowed-tools: Bash Read Edit
effort: low
---

## Find Unused Dependencies

1. Run automated analysis:
```bash
npx depcheck 2>/dev/null | head -40
npx unimported 2>/dev/null | head -40
```

2. For each flagged package, manually verify:
```bash
grep -r "require\|from\|import" src/ --include="*.ts" --include="*.js" | grep "package-name" | head -5
```

3. Watch for false positives:
   - Packages used in config files (`.eslintrc`, `jest.config`)
   - `@types/*` packages (used by TypeScript compiler)
   - Peer dependencies (required by other packages)
   - Dev tools used in scripts

4. Classify each:
   - **Safe to remove**: confirmed unused, no config reference
   - **Keep**: used in config or indirectly
   - **Investigate**: uncertain

5. For safe removals, show the `npm uninstall` commands. Ask for confirmation before running.

6. Estimate bundle size savings.
