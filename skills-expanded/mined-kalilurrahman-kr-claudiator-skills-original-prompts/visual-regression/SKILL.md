---
name: visual-regression
description: Implement visual regression testing with screenshot comparison to catch unintended UI changes. Outputs Playwright/Percy test setup, baseline management, diff thresholds, and CI integration.
argument-hint: [frontend framework, component library, browser targets, CI environment]
allowed-tools: Read, Write, Bash
---

# Visual Regression Testing

Visual regression testing catches unintended UI changes — layout shifts, color changes, font differences, broken components — that functional tests miss because they don't look at pixels. A single screenshot comparison can catch what thousands of assertion lines would miss.

## Process

1. **Choose tooling** — Playwright built-in snapshots (free, self-hosted) or Percy/Chromatic (managed, better diffing).
2. **Identify what to capture** — critical pages, all component states, responsive breakpoints.
3. **Establish baselines** — run tests, approve initial screenshots, commit to repo.
4. **Configure thresholds** — acceptable pixel difference percentage (0.1-1% is typical).
5. **Integrate with CI** — run on PR, fail on unexpected changes, require approval to update.
6. **Manage baseline updates** — deliberate UI changes must go through an update workflow.

## Output Format

### Playwright Visual Regression

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/visual',
  snapshotDir: './tests/visual/__snapshots__',
  updateSnapshots: process.env.UPDATE_SNAPSHOTS === 'true' ? 'all' : 'none',
  
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01,      // 1% pixel difference allowed
      threshold: 0.2,                // Color channel threshold (0-1)
      animations: 'disabled',        // Disable CSS animations for stable screenshots
    },
  },
  
  projects: [
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 },
      },
    },
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 13'],
      },
    },
    {
      name: 'tablet',
      use: {
        ...devices['iPad (gen 7)'],
      },
    },
  ],
  
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    screenshot: 'only-on-failure',
  },
});
```

```typescript
// tests/visual/pages.spec.ts — page-level screenshots
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    // Mask dynamic content before screenshotting
    await page.addStyleTag({
      content: `
        /* Hide dynamic timestamps */
        [data-testid="timestamp"] { visibility: hidden; }
        /* Freeze animations */
        *, *::before, *::after { animation: none !important; transition: none !important; }
      `
    });
  });
  
  test('hero section matches baseline', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Mask dynamic ad/banner areas
    await expect(page).toHaveScreenshot('homepage-hero.png', {
      mask: [
        page.locator('[data-testid="dynamic-banner"]'),
        page.locator('.advertisement'),
      ],
      fullPage: false,   // Viewport only for above-fold
    });
  });
  
  test('full page matches baseline', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Scroll to load lazy images
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    await page.evaluate(() => window.scrollTo(0, 0));
    
    await expect(page).toHaveScreenshot('homepage-full.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });
});

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name=email]', 'test@example.com');
    await page.fill('[name=password]', 'test-password');
    await page.click('[type=submit]');
    await page.waitForURL('/dashboard');
  });
  
  test('dashboard overview', async ({ page }) => {
    await expect(page).toHaveScreenshot('dashboard-overview.png', {
      mask: [
        page.locator('[data-testid="live-metric"]'),   // Mask live numbers
        page.locator('[data-testid="current-time"]'),
      ],
    });
  });
  
  test('dashboard dark mode', async ({ page }) => {
    await page.click('[data-testid="dark-mode-toggle"]');
    await page.waitForTimeout(300);  // Wait for theme transition
    
    await expect(page).toHaveScreenshot('dashboard-dark.png');
  });
});
```

```typescript
// tests/visual/components.spec.ts — component-level screenshots
import { test, expect } from '@playwright/test';

const BUTTON_STATES = ['default', 'hover', 'active', 'disabled', 'loading'];
const ALERT_VARIANTS = ['success', 'error', 'warning', 'info'];

test.describe('Button Component', () => {
  for (const state of BUTTON_STATES) {
    test(`button-${state}`, async ({ page }) => {
      await page.goto(`/storybook?story=button--${state}`);
      await page.waitForSelector('[data-storybook-ready]');
      
      if (state === 'hover') {
        await page.locator('button').hover();
      }
      
      const component = page.locator('#storybook-root');
      await expect(component).toHaveScreenshot(`button-${state}.png`);
    });
  }
});

test.describe('Alert Component', () => {
  for (const variant of ALERT_VARIANTS) {
    test(`alert-${variant}`, async ({ page }) => {
      await page.goto(`/storybook?story=alert--${variant}`);
      await page.waitForSelector('[data-storybook-ready]');
      
      const component = page.locator('#storybook-root');
      await expect(component).toHaveScreenshot(`alert-${variant}.png`);
    });
  }
});

// Form states
test.describe('Form Validation States', () => {
  test('form with errors', async ({ page }) => {
    await page.goto('/signup');
    await page.click('[type=submit]');  // Submit empty form to trigger errors
    await page.waitForSelector('[data-testid="field-error"]');
    
    await expect(page.locator('form')).toHaveScreenshot('form-validation-errors.png');
  });
  
  test('form success state', async ({ page }) => {
    await page.goto('/signup');
    await page.fill('[name=email]', 'valid@example.com');
    await page.fill('[name=password]', 'SecurePass123!');
    
    // Mock API to return success
    await page.route('**/api/signup', route => {
      route.fulfill({ status: 200, body: JSON.stringify({ success: true }) });
    });
    
    await page.click('[type=submit]');
    await page.waitForSelector('[data-testid="success-message"]');
    
    await expect(page).toHaveScreenshot('signup-success.png');
  });
});
```

### Percy Integration (Managed Service)

```typescript
// tests/visual/percy.spec.ts — Percy for richer diff reporting
import { test } from '@playwright/test';
import percySnapshot from '@percy/playwright';

test('product listing page', async ({ page }) => {
  await page.goto('/products');
  await page.waitForLoadState('networkidle');
  
  // Percy handles multi-browser, responsive snapshots automatically
  await percySnapshot(page, 'Product Listing', {
    widths: [375, 768, 1280],   // Mobile, tablet, desktop
    minHeight: 1024,
  });
});

test('checkout flow', async ({ page }) => {
  await page.goto('/cart');
  await percySnapshot(page, 'Cart Page');
  
  await page.click('[data-testid="checkout-button"]');
  await page.waitForURL('/checkout');
  await percySnapshot(page, 'Checkout Step 1 - Shipping');
  
  await fillShippingForm(page);
  await page.click('[data-testid="continue"]');
  await percySnapshot(page, 'Checkout Step 2 - Payment');
});
```

### CI Pipeline

```yaml
# .github/workflows/visual-regression.yml
name: Visual Regression Tests

on:
  pull_request:
    paths:
      - 'src/**'
      - 'public/**'
      - 'tests/visual/**'

jobs:
  visual-regression:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium
      
      - name: Build application
        run: npm run build
      
      - name: Start application
        run: npm start &
        env:
          NODE_ENV: test
      
      - name: Wait for app
        run: npx wait-on http://localhost:3000 --timeout 30000
      
      - name: Run visual regression tests
        run: npx playwright test tests/visual/
        env:
          BASE_URL: http://localhost:3000
      
      - name: Upload diff screenshots on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diffs-${{ github.run_id }}
          path: |
            tests/visual/__snapshots__/**/*.png-diff
            test-results/**/*.png
          retention-days: 7
      
      - name: Comment PR with diff summary
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const diffFiles = fs.readdirSync('tests/visual/__snapshots__')
              .filter(f => f.endsWith('-diff.png'));
            
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Visual Regression Failures\n\n${diffFiles.length} visual differences detected.\nDownload the artifacts to review diffs.\n\nTo update baselines: \`npm run update-snapshots\``
            });

  update-snapshots:
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'
    
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - run: npm ci && npx playwright install --with-deps chromium
      
      - name: Update snapshots
        run: npx playwright test tests/visual/ --update-snapshots
        env:
          UPDATE_SNAPSHOTS: 'true'
          BASE_URL: ${{ secrets.STAGING_URL }}
      
      - name: Commit updated snapshots
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'test: update visual regression baselines [skip ci]'
          file_pattern: 'tests/visual/__snapshots__/**'
```

### Snapshot Management Script

```bash
#!/bin/bash
# scripts/update-snapshots.sh — Update baselines with review workflow

set -e

echo "📸 Updating visual regression snapshots..."
echo ""
echo "⚠️  This will update ALL visual baselines."
echo "   Only run this when UI changes are intentional."
echo ""
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Run tests with update flag
UPDATE_SNAPSHOTS=true npx playwright test tests/visual/ --update-snapshots

# Show what changed
echo ""
echo "Changed snapshots:"
git diff --stat tests/visual/__snapshots__/

echo ""
echo "Review the diffs: git diff tests/visual/__snapshots__/"
echo "Commit when satisfied: git add tests/visual/__snapshots__ && git commit -m 'test: update visual baselines'"
```

## Rules

- **Disable animations** in CSS before taking screenshots — animated elements produce flaky tests.
- **Mask dynamic content** — dates, user names, live metrics, ads must be masked before comparison.
- **Never commit failing baselines** — baselines represent approved, correct UI state.
- **Separate update workflow** — updating baselines requires explicit intent, not an accidental flag.
- **Test at multiple viewports** — mobile, tablet, desktop — responsive bugs are real.
- **Component-level tests are more stable** — full page tests fail on any change anywhere.
- **Wait for network idle** — screenshot before all assets load produces flaky diffs.
- **Per-browser baselines** — Chrome and Firefox render fonts slightly differently; track separately.
- **Review diffs as a team** — visual regression failures are often legitimate UI changes, not bugs.
- **Include visual tests in PR checklist** — "screenshot approved" should be an explicit step.
