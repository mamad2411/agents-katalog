---
description: Run E2E and Visual Regression Guardrails Check
globs: ['**/*.e2e.ts', 'cypress/**/*.js', 'playwright/**/*.ts', '**/*.stories.tsx']
---

# Testing: E2E & Visual Regression Guardrails

<audit_rules>

- You MUST ensure critical user journeys (e.g., Checkout, Authentication) have complete E2E tests covering the happy path and major error states.
- You MUST run E2E tests against multiple viewports (e.g., desktop, tablet, mobile) to prevent responsive regressions.
- You MUST verify that critical CTA elements (e.g., "Buy Now" buttons) are asserted for visibility and clickability, not just presence in the DOM.
- You MUST check for the presence of component snapshot tests (e.g., Storybook) for reusable UI elements.
- You MUST flag the usage of `!important` in CSS, as it breaks component encapsulation and causes visual regressions.
  </audit_rules>

<example_good>

```typescript
import { test, expect } from '@playwright/test'

test('Mobile Checkout Flow', async ({ page }) => {
  // Set mobile viewport
  await page.setViewportSize({ width: 375, height: 667 })

  await page.goto('/pricing')
  const buyButton = page.locator('button:has-text("Subscribe")')

  // Verify visibility on mobile before clicking
  await expect(buyButton).toBeVisible()
  await buyButton.click()

  await expect(page).toHaveURL(/.*checkout/)
})
```

</example_good>

<example_bad>

```typescript
test('Checkout', async ({ page }) => {
  await page.goto('/pricing')
  // BAD: Force clicking a hidden element, failing to catch visual bugs
  await page.click('.buy-btn', { force: true })
})
```

</example_bad>
