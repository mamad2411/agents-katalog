---
name: repo-frontend-performance-debugging
description: Guides browser performance investigation using traces, network waterfalls, rendering evidence, and measurement hygiene. Use when debugging slow loads, interaction latency, layout shifts, asset bloat, or performance regressions.
---


# Frontend Performance Debugging

Use this skill when the task involves browser performance evidence.

## Focus Areas

- page load
- large assets
- network waterfalls
- render-blocking resources
- JavaScript execution
- long tasks
- interaction latency
- layout shifts
- memory leaks
- animation jank
- cache behavior
- service worker behavior

## Required Behavior

- Treat traces as potentially sensitive.
- Prefer local/staging.
- Record device, network, cache, browser, route, and auth state.
- Do not draw strong conclusions from one noisy run.
- Separate lab measurements from field data.
- Compare before/after under similar conditions when validating.

## Workflow

Use `workflows/performance-trace-review-workflow.md`.

