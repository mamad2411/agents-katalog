---
name: deps-update
description: Updates dependencies safely - patch/minor auto, major with analysis
user-invocable: true
allowed-tools: Bash Read Edit
effort: medium
---

## Update Dependencies

1. See what's outdated:
```bash
npm outdated 2>/dev/null || bun outdated 2>/dev/null
```

2. Categorize updates:
   - **Patch** (1.0.1 → 1.0.2): bug fixes, safe to update
   - **Minor** (1.0.0 → 1.1.0): new features, backward compatible, usually safe
   - **Major** (1.0.0 → 2.0.0): breaking changes, needs analysis

3. For major updates, check changelogs:
   - Read the package's CHANGELOG or GitHub releases
   - Identify breaking changes that affect this project
   - Check if there are codemods available

4. Apply updates in batches:
```bash
# Safe updates first
npm update 2>/dev/null || bun update

# Major updates individually after analysis
npm install package@latest
```

5. After each batch: run tests to catch regressions.
```bash
npm test 2>/dev/null || bun test
```

6. Report: N updated, N skipped (reason), N failed tests (which package caused it).
