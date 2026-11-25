---
name: perf
description: Static performance hints (large images, missing img dimensions, no loading=lazy, sync script tags) plus optional Lighthouse JSON report ingestion that surfaces failing audits ranked by potential ms savings. Use when the user wants to audit web performance or process a Lighthouse report. Dragoon does NOT run Lighthouse itself - generate the report with `npx lighthouse <url> --output json --output-path lh.json` and pass --lighthouse. Run as `node ~/.claude/skills/dragoon/skills/perf/scripts/perf.js [--lighthouse path]`.
version: 1.0.0
---

# /perf

Two halves: static hints from your codebase, and parsing of Lighthouse JSON reports.

## When to use

- The user wants to audit web performance
- After running Lighthouse, to surface the most impactful audits
- Before launch, to catch image and script issues early

## Static rules

- `perf-001` large-image (>500KB) (medium)
- `perf-002` img-missing-dimensions causes CLS (low)
- `perf-003` img-without-loading-lazy below the fold (low)
- `perf-004` sync-script-tag blocks parsing (medium)

## Lighthouse ingestion

```
npx lighthouse https://example.com --output json --output-path lh.json
dragoon perf --lighthouse lh.json
```

Output: scores per category, core web vitals (LCP/CLS/TBT/INP/FCP/SI), and the top 6 failing audits ranked by ms savings.

## Run it

```
dragoon perf                                # static only
dragoon perf --lighthouse lh.json           # add lighthouse summary
dragoon perf --severity medium              # filter
dragoon perf --json                         # CI mode
```
