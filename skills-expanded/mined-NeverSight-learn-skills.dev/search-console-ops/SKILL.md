---
name: search-console-ops
description: Uses Search Console and search operators to monitor performance and debug drops. Use when investigating traffic changes or validating indexing after deploys.
---

# Search Console Ops

## Overview

Operate GSC as the source of truth for Search performance and coverage.

## When to Use

- Traffic drops, coverage reports, post-deploy validation

**Not for:** Replacing GSC with invented metrics.

## Official sources

- https://developers.google.com/search/docs/monitor-debug/search-console-start
- https://developers.google.com/search/docs/monitor-debug/debugging-drops

## Process

1. Confirm property setup and date-range comparisons.
2. Separate: query CTR vs impression loss vs index coverage vs sitewide bugs.
3. Use URL Inspection on exemplars; request indexing only when fixes are live.
4. Use search operators carefully for spot checks (`site:`, etc.).
5. Document hypothesis → evidence → fix → re-measure.
6. Pair technical fixes with domain skills.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Analytics alone explains Search drops." | Use GSC coverage/performance slices for Search-specific diagnosis. |
| "Request indexing instead of fixing." | Indexing requests do not repair noindex/canonical bugs. |
| "site: operator is proof of indexation." | It is a rough check — URL Inspection is more reliable. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] GSC evidence cited (screenshot/export description)
- [ ] Hypothesis tied to a coverage or performance slice
- [ ] Follow-up date for re-check set
