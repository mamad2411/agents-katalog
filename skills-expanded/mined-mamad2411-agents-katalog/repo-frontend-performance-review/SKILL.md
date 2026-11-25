---
name: repo-frontend-performance-review
description: Reviews frontend performance risks including bundle growth, large dependencies, rendering hot paths, media, third-party scripts, network waterfalls, caching, hydration, and user-perceived latency. Use for frontend performance-sensitive changes.
---


# Repository Frontend Performance Review

Use this skill when a frontend change may affect page load, interaction latency, rendering cost, network behavior, or bundle size.

## Review Areas

- new dependencies and imports
- large images and media
- third-party scripts
- unnecessary client-side work
- expensive render paths
- polling or repeated requests
- blocking waterfalls
- caching semantics
- large lists or tables
- hydration and startup work

## Required Behavior

- Tie performance findings to user impact.
- Prefer measurement when available.
- Avoid speculative micro-optimization.
- Highlight large dependencies or third-party scripts.
- Identify validation not performed.

## Workflow

Use `workflows/frontend-performance-review-workflow.md`.

## Resource

Use `resources/performance-budget-checklist.md`.

## Scripts

This skill owns:

```text
scripts/frontend-performance-pattern-scan.py
```

Run with `--help` before manual use.

