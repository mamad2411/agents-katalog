---
name: e2e-scenario
description: Turns a plain-language user journey into an end-to-end test written in the framework your project already uses.
disable-model-invocation: true
---

Write an end-to-end test for this journey: $ARGUMENTS

1. Detect the framework in use (Playwright, Cypress, Selenium, WebdriverIO, Detox, Maestro) from config and dependencies. Use it; do not introduce another. If none exists, recommend Playwright and ask first.
2. Read two existing e2e tests for structure, page objects, base URL handling and login helpers. Reuse them.
3. Break the journey into steps with a visible result at each one. Write assertions on what the user sees, not on internal state.
4. Choose selectors in this order: role and accessible name, label, test id. Avoid CSS chains and text that changes. If a needed element has no stable handle, list the data-testid to add and ask before editing the app.
5. Never use fixed sleeps; wait for a condition. Create test data through an API or seed script and clean it up afterward.
6. Run the test 3 times locally. Report any flake and fix its cause.

Show the file path, the steps covered, the run results and anything left manual.
