---
name: testing-ui
description: "UI testing with Playwright and Puppeteer -- browser automation, visual regression, screenshots, and accessibility audits."
metadata: {"thinkfleetbot":{"emoji":"🎭","requires":{"bins":["npx","node"]}}}
---

# UI Testing

Browser-based UI testing with Playwright, Puppeteer, Cypress, and accessibility tools.

## Install Playwright

```bash
# Install Playwright and browsers
npm init playwright@latest
npx playwright install --with-deps

# Install specific browser only
npx playwright install chromium
```

## Run Playwright tests

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/login.spec.ts

# Run in headed mode (visible browser)
npx playwright test --headed

# Run in specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run with debug inspector
npx playwright test --debug
```

## Generate tests from URL

```bash
# Open codegen to record interactions
npx playwright codegen https://example.com

# Save generated test to a file
npx playwright codegen --output tests/generated.spec.ts https://example.com

# Codegen with specific viewport
npx playwright codegen --viewport-size=1280,720 https://example.com
```

## Screenshot page

```bash
# Take a screenshot of a URL
npx playwright screenshot --full-page https://example.com screenshot.png

# Screenshot with specific viewport
npx playwright screenshot --viewport-size=1280,720 https://example.com screenshot.png
```

## Visual regression

```bash
# Run Playwright tests with snapshot comparison
npx playwright test --update-snapshots

# Compare screenshots (expects toHaveScreenshot in tests)
npx playwright test tests/visual.spec.ts

# Show visual diff report
npx playwright show-report
```

## Run Cypress tests

```bash
# Open Cypress interactive runner
npx cypress open

# Run Cypress headless
npx cypress run

# Run specific spec
npx cypress run --spec cypress/e2e/login.cy.ts

# Run in specific browser
npx cypress run --browser chrome
```

## Accessibility audit with axe-core

```bash
# Install axe-core CLI
npm install -g @axe-core/cli

# Run accessibility audit on a URL
npx @axe-core/cli https://example.com

# Audit with specific rules
npx @axe-core/cli https://example.com --rules wcag2a,wcag2aa

# Playwright + axe-core (requires @axe-core/playwright)
npx playwright test tests/accessibility.spec.ts
```
