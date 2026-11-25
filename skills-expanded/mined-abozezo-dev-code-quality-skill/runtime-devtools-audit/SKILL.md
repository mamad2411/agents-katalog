---
name: runtime-devtools-audit
description: |
  Audits browser runtime behavior, rendering, console output, network traffic, and state transitions.
  Use when frontend, browser API, routing, hydration, interaction, or client-side data-fetching changes need evidence.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Browser
---

# Runtime & DevTools Audit

Use this skill to validate the exact browser-facing change in a running application.

## Workflow

1. Establish a working build first: run relevant formatting, linting, type checks, and tests.
2. Start the local application and open the affected route or component in browser tooling.
3. Check the rendered layout, responsive behavior, and each modified interaction.
4. Inspect `console.error`, `console.warn`, unhandled rejections, hydration warnings, runtime exceptions, and failed assets.
5. Inspect network requests for correct URLs, payloads, status codes, duplicate calls, and refetch loops.
6. Exercise loading, empty, error, success, navigation, and form states that the change can affect.
7. Re-test after fixes and report the route, evidence, errors found, and final browser result.

## Rules

- Do not infer browser correctness from static review.
- Treat unexpected console errors as failures until shown harmless.
- Verify the modified route or component rather than an unrelated screen.

## Reference

Read [the DevTools verification guide](reference/devtools-verification.md) for detailed failure modes and the audit checklist.
