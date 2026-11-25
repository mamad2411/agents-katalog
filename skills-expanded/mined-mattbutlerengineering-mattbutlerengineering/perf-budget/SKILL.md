---
name: perf-budget
description: Check bundle size impact of current changes against size-limit baselines. Use when editing apps/* or packages/rialto source, before committing, or when user asks about bundle size.
---

# Bundle Size Budget Check

Run size-limit against current changes and report regressions.

## Workflow

1. Identify which packages were modified:

```bash
git diff --name-only HEAD | grep -E '^(apps|packages)/' | cut -d/ -f1-2 | sort -u
```

2. Build affected packages:

```bash
pnpm build --filter='...[HEAD]'
```

3. Run size check:

```bash
pnpm size:check
```

4. If size-check fails, run detailed report:

```bash
pnpm size
```

5. Report results:
   - If all pass: report current sizes vs limits
   - If any fail: show which entries exceeded budget, by how much, and suggest fixes (tree-shaking, code splitting, dependency replacement)

## Common Fixes for Budget Overruns

- **Large dependency added**: Check if a lighter alternative exists (e.g., `date-fns` instead of `moment`)
- **Rialto component growth**: Verify tree-shaking works — check the package exports map
- **App bundle growth**: Consider lazy loading or route-based code splitting
- **Unchanged code exceeds budget**: The limit may need raising — but verify with `git diff` that no accidental imports leaked in

## Notes

- Size-limit config lives in each package's `package.json` under `"size-limit"` key
- Turbo caches builds, so repeated runs are fast
- Run after `pnpm build` to get accurate measurements
