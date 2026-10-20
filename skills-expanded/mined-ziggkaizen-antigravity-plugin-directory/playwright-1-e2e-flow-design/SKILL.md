---
name: playwright-1-e2e-flow-design
description: Designs and reviews Playwright 1.x end-to-end user-flow coverage for critical journeys, route changes, authorization boundaries, and release risk. Use when planning E2E coverage, mapping product flows to tests, or deciding which Playwright tests should run after navigation or route changes.
license: MIT
compatibility: "Playwright 1.x Node.js projects using @playwright/test."
---

# Playwright 1 E2E Flow Design

Use this skill to decide what Playwright E2E tests should exist, which flows are critical, and how route or navigation changes should affect the test plan.

This skill intentionally stays application-neutral. The consuming repository owns app-specific names, roles, domains, products, and critical-flow inventory.

## Operating Principles

1. Start from user-visible business risk: trust, authorization, payments or payment-like actions, account state, data integrity, destructive actions, and high-traffic entry points.
2. Map each critical flow to a small number of reliable Playwright tests with clear preconditions and assertions.
3. Prefer deterministic setup through APIs, fixtures, or seeded state over long UI setup chains.
4. Keep tests independent enough to run alone, in parallel, and under retry.
5. For route, router, navigation, guard, or middleware changes, identify impacted flows before deciding that no E2E tests are needed.
6. Keep app-specific roles and product language in repository-owned docs, not in this plugin.

## Recommended Workflows

- Use `workflows/design-critical-flow-coverage-workflow.md` when building or revising the repository's critical-flow inventory and Playwright coverage map.
- Use `workflows/route-change-impact-workflow.md` when route, navigation, middleware, guard, redirect, or cross-origin behavior changes.

## Supporting Resources

- `resources/playwright-1-critical-flow-inventory-template.md`: application-neutral inventory template for mapping flows to tests.
- `resources/playwright-1-flow-risk-scoring.md`: lightweight scoring model for deciding which flows need E2E coverage first.
- `examples/playwright-1-critical-flow-test-plan.md`: example format for a repository-owned critical-flow test plan.

## Helper Script

Run the helper with `--help` before using it:

```bash
node .agents/plugins/playwright-1/skills/playwright-1-e2e-flow-design/scripts/playwright-1-route-impact-reminder.mjs --help
```

The script is read-only. It checks git-changed files for route-like changes and can be used by the optional disabled route-impact hook to remind agents to review critical-flow coverage.
