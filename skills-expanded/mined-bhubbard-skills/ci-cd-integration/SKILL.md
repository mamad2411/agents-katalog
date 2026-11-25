---
name: ci-cd-integration
description: Integrate Unlighthouse into CI/CD pipelines (like GitHub Actions) for automated performance audits. Use this when the user wants to automate Lighthouse checks on pull requests or deployments.
---

# Unlighthouse CI/CD Integration

You can integrate Unlighthouse into your continuous integration (CI) pipeline to automatically audit your site and prevent performance regressions.

## GitHub Actions Integration

Unlighthouse offers a dedicated CI package `unlighthouse-ci` that fails the build if your Lighthouse scores drop below a specified threshold.

```yaml
name: Unlighthouse CI
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
          
      - name: Run Unlighthouse CI
        run: npx unlighthouse-ci --site https://your-production-site.com --build-static
```

## Budget Configuration
When running in CI, it is important to enforce budgets. You can specify a budget for performance, accessibility, best practices, and SEO in your config or directly via CLI:
```bash
npx unlighthouse-ci --site <url> --budget 90
```
This ensures all pages must score at least 90 in all categories.
