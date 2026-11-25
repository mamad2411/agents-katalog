---
name: react-performance
description: "Diagnose and fix React performance: render profiling, memoisation that pays, list virtualisation, bundle splitting and Core Web Vitals."
type: procedural
category: web
domain: web
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - react slow render
  - react profiler flamegraph
  - why does my component rerender
  - react bundle size
  - usememo usecallback worth it
aliases:
  - react-perf
keywords:
  - react
  - profiling
  - memo
  - usememo
  - virtualisation
  - web-vitals
  - bundle
mcp_servers:
  - playwright
  - chrome-devtools
  - context7
source: custom
enabled: true
---

# React Performance

## Purpose

Diagnose and fix React performance: render profiling, memoisation that pays, list virtualisation, bundle splitting and Core Web Vitals.

## When to Use

- A React screen is measurably slow and the cause is not yet known.
- A list, table or chart drops frames while scrolling or typing.
- Bundle size or LCP regressed after a release.

## When NOT to Use

- The bottleneck is server response time — profile the backend first.
- The app is not React.
- Nothing is slow; the goal is stylistic micro-optimisation.

## Capabilities

- Profile with the React DevTools profiler and read commit durations.
- Distinguish unnecessary re-renders from expensive renders.
- Virtualise long lists and defer non-critical work with transitions.
- Split bundles by route and lazy-load below-the-fold widgets.
- Measure the result with Core Web Vitals rather than impressions.

## Inputs

- A reproducible slow interaction and the hardware you will measure on.
- Profiler traces from a production build, not a dev build.
- The current LCP/INP/CLS baseline for the affected route.

## Workflow

1. Reproduce in a production build and record a profile of the exact interaction.
2. Find the commit that takes the most time, then the component responsible for it.
3. Fix the cause: unstable props, context churn, missing keys, or genuinely expensive work.
4. Move expensive computation out of render or behind `useMemo` only where the profile justifies it.
5. Virtualise lists over ~100 rows and paginate what cannot be virtualised.
6. Re-measure the same interaction and the Web Vitals, then keep the trace as evidence.

## Tools

- react-devtools
- playwright
- lighthouse
- webpack-bundle-analyzer

## Examples

- `A context providing a new object every render re-renders every consumer — memoising the value is the fix, not `memo()` on children.`
- `Wrapping 40 components in `memo` without a profile usually adds memory and changes nothing.`

## Safety

- Do not ship experimental React features to production to win a benchmark.
- Keep accessibility intact when deferring rendering; do not hide content from screen readers.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `playwright` | stdio | standard | medium | — |
| `chrome-devtools` | stdio | standard | medium | — |
| `context7` | stdio | standard | low | `CONTEXT7_API_KEY` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/web/react-performance`). First-party skill, maintained in this repository.

## Notes

- Dev builds are 2–10× slower and lie about relative cost; always profile a production build.
- `startTransition` helps input responsiveness, not total work.
- Pairs with: `nextjs-app-router`, `visual-regression-testing`.
