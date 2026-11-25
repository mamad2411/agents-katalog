---
name: paid-social-kpi-exporter
description: "When the user wants to export Meta Ads or paid social data into a spreadsheet, create daily or weekly KPI reports, calculate CPMr, cost per 1,000 accounts reached, CPM, CPC, CTR, CVR, CPA, ROAS, MER, spend pacing, blended CAC, or produce CSV-ready reporting tables. For strategic account diagnosis, use meta-performance-analyst."
metadata:
  version: 1.0.0
---

# Paid Social KPI Exporter

Turn paid social data into spreadsheet-ready tables, weekly control-room workbooks, and chart-ready reporting layers.

## Before Exporting

1. Read `.agents/vibemarketer-context.md` if it exists.
2. Identify source data: Meta Ads CLI, Meta MCP/API fallback, Triple Whale, Northbeam, CSV, spreadsheet, Shopify/backend export, or pasted table.
3. Confirm grain: daily, weekly, campaign, ad set, ad, product, or blended business level.
4. Confirm destination: CSV, Markdown table, Google Sheets-ready table, Excel-ready formulas, or a saved file.
5. Confirm comparison coverage before promising WoW/YoY charts. A latest-7-days pull can build a current-period workbook, but WoW cards need the previous 7 days / previous ISO week, YoY cards need the same ISO week last year, and Net New Reach cards need the account-level reach windows.
6. Before running the export, tell the user: "A latest-7-days pull is enough for a current-period workbook. For full WoW/YoY cards and charts, we need current week, previous 7 days / previous ISO week, same ISO week last year, and optional Net New Reach windows. Campaign-level daily rows are enough to validate top-line comparison charts; keep the history at one grain and do not mix campaign-level history with ad/ad-set rows in the same KPI history file. If those are missing, the workbook still renders but comparisons will show `n/a` or single-point charts."
7. If comparison coverage is missing, warn the user that the workbook will render but comparison cards/charts will show `n/a` or single-point visuals until they pull/import the missing windows.
8. If using spreadsheet tooling, prefer structured APIs/libraries over string manipulation.
9. If source files are CSV exports, use `scripts/normalize_kpis.py` when possible before writing a manual table.

## Reference

Read `references/kpi-schema.md` when mapping columns, formulas, or sheet structure.

Use `assets/daily-kpi-template.csv` as a paste-ready tab template.

Use `scripts/build_kpi_dashboard_pack.py` when the user wants a weekly control-room workbook, daily pulse, action slots, source-of-truth metric layer, native spreadsheet charts, or a spreadsheet workbook from daily data.

Use `scripts/run_daily_paid_social_export.py` when the user wants the full daily workflow: live Meta pull, normalization, history append/dedupe, operating workbook rebuild, and optional Google Sheets-safe XLSX output.

## Standard Outputs

Offer one of these:

- Daily KPI table for operators.
- Weekly performance rollup.
- Weekly control-room workbook with native spreadsheet charts.
- Chart-ready CSV pack for Google Sheets or Excel.
- Campaign/ad set/ad drilldown.
- Change log: what moved since yesterday or last week.
- Import-ready CSV.
- Normalized CSV saved to disk from source exports.

## Weekly Control Room Pack

When the user asks for graphs, a KPI dashboard, or a spreadsheet report, create a weekly control-room pack:

```bash
python3 skills/paid-social-kpi-exporter/scripts/build_kpi_dashboard_pack.py \
  data/daily_kpis.csv \
  --context .agents/vibemarketer-context.md \
  --net-new-reach data/meta-net-new-reach/windows.csv \
  --selected-week 18 \
  --xlsx \
  -o outputs/kpi-dashboard-pack
```

The pack writes:

- `daily_normalized.csv`: standardized daily source table.
- `weekly_summary.csv`: ISO-week rollup with CPMr, spend, reach, CTR, purchases, revenue, ROAS, and YoY deltas.
- `metric_cards.csv`: selected-week KPI cards with current value, WoW delta, YoY delta, status, and source.
- `action_slots.csv`: up to three high-level decision slots: Protect / Scale, Diagnose / Reduce, Rebalance / Test.
- `metric_source.csv`: source-of-truth state, missing-data notes, and reach caveats.
- `comparison_preflight.md` and `comparison_preflight.csv`: whether current, WoW, YoY, chart, and Net New Reach history is complete enough for comparison-heavy reporting.
- `chart_data.csv`: clean source ranges for native spreadsheet charts.
- `daily_pulse.csv`: yesterday vs trailing 7-day average and last 7 vs previous 7 movement.
- `campaign_rollup.csv`, `adset_rollup.csv`, `ad_rollup.csv`: selected-week entity reads with decision flags.
- `creative_handoff.csv`: ads to inspect with creative-angle-lab and why they matter.
- `kpi-dashboard.xlsx`: optional workbook that opens on `Weekly Control Room` with status-colored KPI cards, Data Freshness, What Changed This Week, decision cards, native spreadsheet charts, `Daily Pulse`, entity rollups, `Metric Source`, `Chart Data`, and `Raw Daily Data`.

Treat `kpi-dashboard.xlsx` as the primary artifact. For strategic narrative diagnosis, use `meta-performance-analyst`. For Google Sheets, the workbook includes native chart objects linked to `Chart Data`; if an importer strips chart objects, rebuild the same charts from those source ranges.

For a running daily history file, use append/dedupe mode:

```bash
python3 skills/paid-social-kpi-exporter/scripts/build_kpi_dashboard_pack.py \
  data/yesterday_paid_social.csv \
  --history data/kpi-history/daily_kpis.csv \
  --append-history \
  --xlsx \
  -o outputs/kpi-dashboard-pack
```

Append mode dedupes by date, platform, account, campaign, ad set, and ad identity before rebuilding the pack.

First-run caveat: if the input only contains the latest 7 days, treat the workbook as a current-period read. Before relying on WoW/YoY cards or multi-line charts, pull/import the previous 7 days and the same ISO week last year, then rebuild from the combined history.

For comparison-only validation, prefer campaign-level daily rows for the selected week, previous week, and same ISO week last year. Do not combine those historical campaign rows with current-week ad/ad-set rows in the same history file, because mixed grains can double-count spend and reach.

## Full Daily Export Runner

For installed live accounts, prefer the daily runner:

```bash
python3 skills/paid-social-kpi-exporter/scripts/run_daily_paid_social_export.py
```

The runner:

- Pulls active spending Meta campaigns/ad sets/ads through the slow resumable Meta puller.
- Pulls account-level Meta Net New Reach windows unless `--skip-net-new-reach` is passed.
- Normalizes hierarchy files.
- Appends/dedupes daily rows into `data/kpi-history/daily_kpis.csv`.
- Rebuilds the weekly control-room workbook under `outputs/daily-paid-social/kpi-dashboard`.
- Reads `.agents/vibemarketer-context.md` for attribution/source-of-truth preferences and targets when available.
- Labels complete/partial Meta source coverage from `manifest.json`.

After installation, users can schedule this command with their automation tool of choice, or ask Codex/Claude Code to create a daily automation in the workspace. Default recommendation: run once each morning after Meta has finalized the prior day's data.

## Source Of Truth

The workbook inherits attribution preference from `.agents/vibemarketer-context.md`:

- Triple Whale configured and Triple Whale data exists: use Triple Whale NCROAS/ROAS.
- Northbeam configured and Northbeam data exists: use Northbeam ROAS.
- Triple Whale or Northbeam configured but missing: show source-of-truth efficiency as unavailable.
- No context but Meta revenue/spend exists: use Meta ROAS only as `Meta-attributed fallback`.

## Net New Reach

Net New Reach is account-level only in V1:

```text
A = Reach(T-365 -> T-28)
B = Reach(T-365 -> T)
C = Reach(T-28 -> T)
D = Spend(T-28 -> T)
Net New Reach 28d = B - A
Net New Reach % = (B - A) / C
Spend per Net New Person = D / (B - A)
```

Use `skills/meta-performance-analyst/scripts/pull_meta_net_new_reach.py` to create the optional window CSV passed into the workbook builder. It defaults to `--source auto`: try the installed Meta Ads CLI first, then fall back to the Marketing API if that CLI does not support the required date-window flag. Use `--source api` to force the Marketing API path.

## Default Daily KPI Columns

Use this order unless the user asks otherwise:

```text
date, platform, account, campaign, ad_set, ad, spend, impressions, reach, frequency, cpmr, clicks, outbound_clicks, ctr, cpc, cpm, purchases, revenue, cpa, roas, aov, cvr, notes
```

For business-level reporting, add:

```text
total_revenue, total_orders, total_marketing_spend, mer, blended_cac, contribution_margin, contribution_profit
```

For attribution-aware reporting, add:

```text
meta_roas, tw_roas, tw_ncroas, northbeam_roas, northbeam_attributed_revenue, source_of_truth, goal_status
```

## Output Rules

- Use ISO dates: `YYYY-MM-DD`.
- Preserve currency and note it in the header.
- Return blank cells for unavailable fields, not invented zeros.
- Calculate formulas from raw fields when possible.
- Keep narrative light inside this skill. The workbook should answer the high-level metric questions; long-form interpretation belongs in `meta-performance-analyst`.

## CSV Output

When the user asks for CSV, output only valid CSV in a fenced `csv` block unless saving to a file.

## Formula Safety

Use safe divide formulas:

- Spreadsheet style: `=IFERROR(spend/purchases,"")`
- Plain calculation: return blank or `N/A` when denominator is zero.

## Quality Bar

- Make tables easy to paste into Google Sheets.
- For dashboard workbooks, open on `Weekly Control Room` and include source data, metric cards, chart data, native spreadsheet charts, and supporting entity tabs.
- Keep `Daily Pulse`, campaign rollups, ad set rollups, ad rollups, `Metric Source`, and creative handoff first-class supporting tabs.
- When source data comes from the Meta live hierarchy pull, check the accompanying `manifest.json` or coverage note before treating the workbook as complete. If the manifest is partial, label the workbook/read accordingly and rerun the Meta pull after cooldown before final reporting.
- When using `build_kpi_dashboard_pack.py` from live Meta hierarchy rows, pass `--source-manifest data/.../meta-active-hierarchy/manifest.json` so `Metric Source` and the dashboard header label complete/partial source coverage.
- Always review `comparison_preflight.md` before treating WoW/YoY charts as final. Missing comparison data should remain `n/a`, never invented zeros.
- Keep dashboard cards compact: selected week/year, primary metric, YoY delta, CPMr, spend, purchases/orders, and ROAS/NCROAS when available.
- Prefer ISO-week comparisons for multi-year views.
- Add decision flags such as `scale candidate`, `fatigue risk`, `CPMr watch`, `underfunded winner`, and `no conversion watch`.
- Keep raw metrics and calculated metrics separate when useful.
- Do not mix Meta-reported ROAS with blended MER without labeling.
- If the user asks for a daily overview, include a compact executive read, not just numbers.
