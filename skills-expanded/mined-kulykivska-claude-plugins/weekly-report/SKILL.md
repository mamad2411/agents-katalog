---
name: weekly-report
description: >-
  Generate the weekly business report across projects: what shipped, metric
  movement, incidents, next week's plan. Trigger on "weekly report",
  "how did the week go", or on a Friday/Sunday recap request.
---

# Weekly report

## Steps

1. **Window**: the last 7 days (or since the previous report if one exists
   in the project's docs).
2. **Shipped**: git log across all active repos for the window, grouped by
   project; include deploys that reached prod.
3. **Metrics**: pull what is reachable: conversion/funnel numbers from the
   app's admin endpoints, usage counts, model scorecard deltas (only from
   real evaluation runs). Compare against the previous week; compute deltas.
4. **Incidents**: anything that broke in prod and what fixed it (from memory
   notes, logs, and the week's sessions).
5. **Delegate assembly** to the `report-builder` subagent with the collected
   data; ask for the weekly format with 2-3 charts max.
6. Save the result under the project's docs (dated) so next week has a
   baseline, and give the executive summary inline.
