---
name: scorecard
description: Generate the weekly or monthly business performance scorecard — fixed KPI set with comparisons, status colours, and narrative explanations for every off-track metric. Usage - /scorecard weekly or /scorecard monthly.
---

# Scorecard — Periodic Performance Report

Owner: `performance-monitor`, with `insights-communicator` for the monthly narrative. Argument: `weekly` (default) or `monthly`.

## Procedure

1. **Determine the period.** Weekly = most recent complete week ({{WEEK_DEFINITION e.g. Mon–Sun}}); monthly = most recent complete calendar/fiscal month per `knowledge/business-context.md`. Never report a partial period without labelling it as such.

2. **Load the KPI set** from the scorecard section of `knowledge/metrics-catalog.md`. The set is fixed between periods; if it's empty, run `/define-kpis` first. Check `scorecards/` for prior editions — formats and metric set must stay comparable.

3. **Check data freshness first.** Verify every source table is loaded through the period end. A scorecard on stale data is worse than a late scorecard — if data is missing, say so per-metric rather than silently under-reporting.

4. **Compute each metric** using catalog formulas (or the pre-built marts) — take the SQL from `python scripts/run_metric.py "<name>"`, never from last period's scorecard or from memory: current value, vs prior period (Δ and %), vs same period last year where history allows, vs target where set, and status:
   - 🟢 on track (within {{GREEN_THRESHOLD e.g. ±5% of target/trend}})
   - 🟡 watch ({{YELLOW_THRESHOLD}})
   - 🔴 off track ({{RED_THRESHOLD}})
   Thresholds per metric live in the catalog; flag any metric without thresholds.

5. **Explain, don't just colour.** For every 🔴 and 🟡, run a quick localisation (which segment/channel drives it) and attach a one-line cause or "under investigation — see /investigate-metric". Also call out notable 🟢 overperformance — wins matter too.

6. **Anomaly sweep.** Beyond the fixed set, scan for trend breaks, paired-metric divergence, and segment-level moves hidden by stable toplines. Add an "Also noticed" section if anything qualifies.

7. **Write the scorecard** to `scorecards/YYYY/weekly-YYYY-WW.md` or `monthly-YYYY-MM.md`:
   - Headline (2–3 sentences: overall state + the one thing to pay attention to)
   - KPI table (metric, value, vs prior, vs LY, vs target, status, note)
   - Off-track detail (one short paragraph each)
   - Also noticed
   - Data caveats (freshness gaps, definition changes this period)
   - The provenance footer (`standards/reporting-standards.md`): source tier, data-through date, owner, review status
   - **Monthly only:** add a narrative section (what happened this month and why, ~half page) and a "watch next month" list.

8. **Check before it leaves.** Run `python scripts/scan_outputs.py scorecards/` — a segment breakdown is where a cell under the minimum group size appears. The **monthly** scorecard, and any scorecard going to executives, is reviewed by `analysis-reviewer` first; record the verdict in the footer.

9. **Distribute** per the standing cadence in `CLAUDE.md` §6. Producing the file is autonomous; *sending* it anywhere external requires the user's standing authorisation.

10. **Maintain.** If any metric was 🔴 two consecutive periods, recommend a full `/investigate-metric`. Log definition or threshold changes in `knowledge/decision-log.md`.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
