---
name: github-actions
description: Creates or improves GitHub Actions CI/CD workflows
argument-hint: [workflow-type: ci|deploy|release|lint]
user-invocable: true
allowed-tools: Read Glob Edit Bash
effort: medium
---

## GitHub Actions Workflow

Type: **$1** (ci | deploy | release | lint - or auto-detect)

1. Check existing workflows:
```bash
ls .github/workflows/ 2>/dev/null
cat package.json | grep '"scripts"' -A 20
```

2. Generate the appropriate workflow:

**CI (test + lint on PR):**
```yaml
name: CI
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run typecheck
```

3. Add optimizations:
   - Dependency caching (`actions/cache`)
   - Matrix testing for multiple Node/Python versions if needed
   - Fail-fast vs complete runs
   - Concurrency groups (cancel in-progress on new push)

4. For deploy workflows: ask for target platform (Vercel, Railway, AWS, Fly.io, etc.)

5. Save to `.github/workflows/<type>.yml`
