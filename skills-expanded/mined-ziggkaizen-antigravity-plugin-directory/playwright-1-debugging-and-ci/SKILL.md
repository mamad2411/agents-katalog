---
name: playwright-1-debugging-and-ci
description: Debugs Playwright 1.x failures, traces, reports, CI behavior, focused-test leaks, browser installation issues, and safe command execution. Use when a Playwright test fails locally or in CI, when reviewing CI readiness, or when validating Playwright artifacts and commands.
license: MIT
compatibility: "Playwright 1.x Node.js projects using @playwright/test."
---

# Playwright 1 Debugging and CI

Use this skill for failing tests, flaky behavior, CI configuration, artifact review, browser-install problems, focused-test prevention, and command safety.

## Operating Principles

1. Start with evidence: error output, trace, screenshot, video, HTML report, config, and exact command.
2. Reproduce the smallest failing case before broad changes.
3. Distinguish app defects from test defects.
4. Avoid hiding failures with blanket skips, excessive retries, focused tests, or large timeout increases.
5. Keep CI artifacts useful but do not expose secrets.
6. Ask before running destructive or production-impacting commands.
7. Treat MCP browser sessions as sensitive because they can expose the live browser state to the agent.

## Recommended Workflows

- Use `workflows/triage-failure-with-trace-workflow.md` when a failure has traces, screenshots, videos, or report artifacts.
- Use `workflows/ci-readiness-workflow.md` when adding or reviewing CI scripts, browser installation, reporters, retries, artifacts, focused-test gates, or route-impact gates.

## Supporting Resources

- `resources/playwright-1-flake-triage-checklist.md`: common flake categories and corrective actions.
- `examples/playwright-1-ci-package-json-scripts.md`: package script examples for local and CI runs.

## Helper Scripts

Run scripts with `--help` before using them:

```bash
.agents/plugins/playwright-1/skills/playwright-1-debugging-and-ci/scripts/playwright-1-ci-smoke.sh --help
node .agents/plugins/playwright-1/skills/playwright-1-debugging-and-ci/scripts/playwright-1-command-guard.mjs --help
node .agents/plugins/playwright-1/skills/playwright-1-debugging-and-ci/scripts/playwright-1-no-only-check.mjs --help
```

The command guard and focused-test checker are designed for Antigravity hooks and read hook JSON from stdin during normal operation.
