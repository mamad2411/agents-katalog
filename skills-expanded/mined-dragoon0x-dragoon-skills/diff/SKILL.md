---
name: diff
description: Scaffold a playwright visual regression test suite that takes per-route full-page screenshots and compares against committed baselines. Pixel diffing is done by playwright's toHaveScreenshot, not by dragoon. Use when the user wants visual regression coverage. Pass --routes to set the routes to capture. Defaults to dry-run; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/diff/scripts/diff.js`.
version: 1.0.0
---

# /diff

Scaffolds visual regression with playwright snapshots.

## When to use

- The user wants visual regression coverage
- "Set up screenshot diffing", "snapshot tests", "pixel diff"
- Before any major UI refactor

## What it writes

- `playwright.visual.config.ts` snapshot-tuned config
- `tests/visual/routes.ts` list of routes to capture (default `/`)
- `tests/visual/snapshots.spec.ts` spec that loops routes and runs `toHaveScreenshot`

Pixel diffing is done by playwright's built-in toHaveScreenshot, not by dragoon. We just generate the harness.

## Run it

```
dragoon diff
dragoon diff --apply
dragoon diff --apply --routes "/,/about,/login"
```

## Then

```
npm i -D @playwright/test
npx playwright install --with-deps chromium
npx playwright test tests/visual --update-snapshots   # first time, baselines
npx playwright test tests/visual                      # after that, regression
```
