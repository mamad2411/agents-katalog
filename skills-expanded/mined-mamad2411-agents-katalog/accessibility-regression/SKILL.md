---
name: accessibility-regression
description: Detect accessibility regressions automatically in CI using axe-core + Playwright/Cypress, Storybook a11y addon, Lighthouse budgets, and a baseline of known/waived violations. Use to keep WCAG conformance once you've achieved it.
source: self
date_added: 2026-04-30
---

# Accessibility Regression Testing

Manually achieving conformance is hard; keeping it without automation is impossible. Automate to catch regressions on every PR; manual + AT remain irreplaceable for new behavior.

## Stack Baseline (2026)

| Layer | Tool |
| --- | --- |
| Component | jest-axe / vitest-axe; Storybook `@storybook/addon-a11y` |
| Page (E2E) | `@axe-core/playwright` or `cypress-axe` |
| Crawl | Pa11y CI; Lighthouse CI |
| Lint | `eslint-plugin-jsx-a11y`, `stylelint-a11y`, `axe-linter` |
| Trend | axe Dev Hub, Accessibility Cloud |

## CI Gating Pattern

1. **Per PR** — component tests + page tests on changed routes; **fail on new violations**.
2. **Per merge** — full crawl of staging; trend report uploaded.
3. **Nightly** — Lighthouse CI a11y score per route; alert on drop.
4. **Per release** — manual + AT regression checklist for tier-1 flows.

## Baseline & Waivers

- Maintain a **violations baseline** (`axe-result-snapshot.json`) of known issues.
- New PRs cannot increase counts above baseline; PRs that fix issues update the baseline downward.
- Each waiver requires: rule ID, selector, justification, expiry, owner. Re-evaluated at expiry.

## Playwright + axe Example

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('home page has no critical a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .disableRules([/* documented exceptions only */])
    .analyze();
  expect(results.violations.filter(v => ['critical','serious'].includes(v.impact!))).toEqual([]);
});
```

## Storybook a11y Addon (component)

For every story: addon panel must show "No violations" before merge. CI runs `@storybook/test-runner` with axe.

## Lighthouse CI Budget

```json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.95 }]
      }
    }
  }
}
```

Lighthouse a11y score is a coarse signal — use as a budget, not a substitute for axe.

## What Automation Won't Catch

- Meaningful alt text quality.
- Logical heading/reading order vs visual order.
- Focus management in dialogs.
- Live region appropriateness.
- Cognitive load, content clarity, error message helpfulness.
- Real screen reader announcements.

Keep a manual + AT regression checklist for these per release.

## Common Pitfalls

- Snapshot diff over content text — noisy false positives.
- Failing the build on every minor finding — teams disable the gate. Tier severity instead.
- One-shot scan, never trended — misses creep.
- Waivers without expiry — they pile up.
- No component-level coverage — design system regressions reach all consumers.

## Output

- CI gates on PRs and merges.
- Trend dashboard: violations by rule, by route, over time.
- Waiver register with expiries.
- Per-release manual checklist sign-off.

## References

- axe-core docs — https://www.deque.com/axe/
- @axe-core/playwright — https://github.com/dequelabs/axe-core-npm
- Storybook a11y addon — https://storybook.js.org/addons/@storybook/addon-a11y
- Lighthouse CI — https://github.com/GoogleChrome/lighthouse-ci
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
