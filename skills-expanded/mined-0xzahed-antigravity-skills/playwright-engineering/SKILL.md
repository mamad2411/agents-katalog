---
name: playwright-engineering
description: Build robust E2E suites with Playwright. Use when automating browser tests.
metadata:
  tags: playwright, engineering
---

# Playwright Engineering

## Use this skill when
- Writing browser E2E tests
- Configuring parallel workers and sharding
- Debugging flaky browser tests

## Do not use this skill when
- Non-browser API testing
- Low-level unit tests

## Instructions
1. Use data-testid or role locators for stability.
2. Emulate realistic network conditions and devices where relevant.
3. Prefer web-first assertions (expect(locator).toBeVisible).
4. Isolate tests with fixtures and per-test context.
5. Capture traces/screenshots on failure for diagnosis.
6. Run with WebServer config to manage app lifecycle in CI.
7. Shard across workers on CI.

## Checklist
- No hard sleeps
- Trace on failure enabled
- Tests run on CI

## Output Format
- Locator strategy | fixture design | CI sharding | flake handling

## Common Mistakes
- Snapshot/visual assertions as the norm
- Shared logged-in state between tests
- Ignoring network request failures
