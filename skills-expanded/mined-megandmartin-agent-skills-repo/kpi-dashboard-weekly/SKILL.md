---
name: kpi-dashboard-weekly
description: Compiles a Monday-morning KPI snapshot from a local metrics.csv — week-over-week deltas, traffic-light status against targets, and one concrete action per red metric. Use when the user says "KPI snapshot", "how are the numbers", "weekly metrics", "dashboard update", or on the scheduled Monday run. Don't use for revenue-only deep dives — use weekly-revenue-report — or for personal reflection — use weekly-review.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Metrics, KPI, Automation]
    related_skills: [weekly-revenue-report, pipeline-tracker, weekly-review]
    blueprint:
      schedule: "0 8 * * 1"
      prompt: "Compile my weekly KPI snapshot"
---

# KPI Dashboard Weekly

Every Monday at 08:00, reads the business's `metrics.csv` and answers three questions in one screen: what moved week-over-week, what's red against target, and what one action fixes each red. The standard: numbers computed by python3 from the actual file — never estimated — and every red metric leaves with exactly one owner-ready action, not a paragraph of concern.

## When to Use

- The scheduled Monday blueprint fires ("Compile my weekly KPI snapshot").
- User asks "how are the numbers", "KPI check", "are we on track".
- Adding a new metric or target to the tracked set.
- **Not for:** Stripe/revenue forensic detail — use `weekly-revenue-report`. Not for reconciling payments — use `payment-reconciliation`. Not for personal weekly reflection — use `weekly-review`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Find the file | `ls` the business folder for `metrics.csv` |
| Inspect columns | `head -3 metrics.csv` |
| Expected header | `date,metric,value,target` (one row per metric per week) |
| Compute deltas | `python3` stdlib script (Procedure step 3) — csv module, no pandas |
| Status rule | 🟢 ≥100% of target · 🟡 85–99% · 🔴 <85% (or missing data) |
| Archive snapshot | append output to `kpi-history.md` |

## Procedure

1. **Precheck** — confirm `metrics.csv` exists and `head -3` shows the `date,metric,value,target` header. If the file is missing or the header differs, report exactly what was found, propose the expected schema, and stop — never invent numbers to fill a dashboard.
2. **Freshness check** — the latest `date` in the file should be within the last 8 days. If the newest rows are stale, the snapshot still runs but opens with "⚠️ Data last updated {date} — this snapshot reflects that week."
3. **Compute** — run with python3 stdlib (adjust path):

   ```bash
   python3 - <<'EOF'
   import csv, collections
   rows = list(csv.DictReader(open('metrics.csv')))
   by_metric = collections.defaultdict(list)
   for r in rows:
       by_metric[r['metric']].append(r)
   for m, rs in sorted(by_metric.items()):
       rs.sort(key=lambda r: r['date'])
       cur, prev = rs[-1], (rs[-2] if len(rs) > 1 else None)
       v, t = float(cur['value']), float(cur['target'] or 0)
       delta = (v - float(prev['value'])) / float(prev['value']) * 100 if prev and float(prev['value']) else None
       pct = v / t * 100 if t else None
       status = 'GREEN' if pct and pct >= 100 else 'YELLOW' if pct and pct >= 85 else 'RED'
       print(f"{m}: {v:g} (target {t:g}, {pct:.0f}% -> {status})" + (f" WoW {delta:+.1f}%" if delta is not None else " WoW n/a"))
   EOF
   ```

   Success: one line per metric with value, %-to-target, status, and WoW delta. A `ValueError` means a non-numeric cell — find it with `grep -n` and report the bad row instead of skipping it silently.
4. **One action per red** — for each 🔴, write exactly one specific, this-week action tied to the lever that moves that metric (e.g., "Leads red at 60% → run the `cold-outreach-sequencer` batch Tuesday"). No red leaves the report actionless; no red gets three actions.
5. **Deliver + archive** — format per the template (greens get one line total — attention goes to reds), append the snapshot to `kpi-history.md`, and lead with the single most important sentence of the week.

## Output Template

```
# KPI Snapshot — Week of {Mon date}
**Headline:** {one sentence — the thing that matters most this week}

| Metric | This wk | WoW | Target | Status |
|---|---|---|---|---|
| {metric} | {value} | {+/-x%} | {target} ({pct}%) | 🔴/🟡/🟢 |

## 🔴 Reds → this week's actions
- **{Metric}** ({pct}% of target): {one action, one owner, one deadline}

## 🟡 Watch
- {metric}: {one line}

🟢 On track: {comma-separated list}.
Data through {latest date in csv}.
```

## Pitfalls

- **Missing week treated as zero** — a metric with no row this week shows as a catastrophic drop. Recovery: distinguish "no data" from 0; missing rows get status 🔴 with the action "log the number", and WoW shows "n/a", not −100%.
- **Numbers hallucinated when the CSV is malformed** — the dashboard must always come from the script's stdout. Recovery: if python3 errored, the report says so and shows the offending row; a partially computed dashboard is labeled partial.
- **Delta computed against the wrong week** — unsorted dates (or mixed formats like `7/14` vs `2026-07-14`) scramble prev/current. Recovery: the script sorts by date string — enforce ISO `YYYY-MM-DD` in the file; if mixed formats appear, normalize them first and tell the user.
- **Report balloons into analysis soup** — Monday morning gets 90 seconds. Recovery: greens are one line, the headline is one sentence, and each red gets exactly one action; cut everything else.

## Verification

- [ ] Every number in the table appears verbatim in the python3 output — nothing typed from memory
- [ ] Status colors match the 100/85 rule for every metric
- [ ] Each 🔴 has exactly one action with an owner and a deadline
- [ ] Data-freshness line present; stale data flagged at the top
- [ ] Snapshot appended to `kpi-history.md`
