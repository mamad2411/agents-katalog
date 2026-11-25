---
name: failure-measure
description: Measure and publish OpenCrabs' honest, quantified tool-failure rates from the feedback_ledger — overall rate, 7-day trend, worst tools by failure %, and the single dominant failure cause. Stolen-discipline idea (OmegaClaw gap analysis 2026-07-28): OmegaClaw published its own premise-error rates; OC should do the same with its tool-call ledger.
---

# Failure Measure

Produce an honest, quantified self-failure report. **No vibes — numbers from the ledger.**

> Origin: OmegaClaw-Core's most transferable trait was that it *measured and published its own failure rates* (16.6% premise-swap, 15pp confidence overestimate) and built mitigations around them. OC already collects the data in `feedback_ledger`; this skill is the missing discipline of reading it and telling the truth.

## Data source

`~/.opencrabs/opencrabs.db`, table `feedback_ledger`. Columns: `event_type` (`tool_success`/`tool_failure`/`provider_error`/`user_correction`/`improvement_applied`/`phantom_tool_call`/…), `dimension` (tool/provider name), `value`, `metadata` (JSON w/ error text), `created_at`.

**Read-only. SELECTs only. Never write to this table from the skill.**

## Procedure

1. **Overall rate** — successes vs failures across `tool_success`+`tool_failure`:
   ```sql
   SELECT SUM(CASE WHEN event_type='tool_failure' THEN 1 ELSE 0 END) AS fails,
          SUM(CASE WHEN event_type='tool_success'  THEN 1 ELSE 0 END) AS ok
   FROM feedback_ledger WHERE event_type IN ('tool_success','tool_failure');
   ```
   `fail_pct = 100*fails/(fails+ok)`.

2. **7-day trend** — bucket `created_at >= <today-7d>` as `last7d`, else `prior`; fail_pct per bucket. **Flag any move > 5 percentage points** — that is a regression worth naming.

3. **Worst tools** — per-`dimension` fail_pct, `HAVING (ok+fail) >= 20`, `ORDER BY fail_pct DESC LIMIT 10`.

4. **Dominant cause** — for the worst tool, `GROUP BY substr(metadata,1,60) ORDER BY COUNT(*) DESC LIMIT 5`. One mechanical bug usually dominates. Name it and compute what % of *all* failures it explains.

5. **Provider errors** — `WHERE event_type='provider_error' GROUP BY dimension` to expose availability/billing drops separately (these are environmental, not tool bugs).

## Output format (tight)

- **Headline line:** overall fail % + the 7-day arrow (e.g. `22.2% all-time → 35.9% last7d ↑`).
- **Worst-5 table:** tool | calls | fail %.
- **One sentence** naming the single dominant cause and what fraction of failures it explains.
- **Verdict:** getting better or worse, and the suspected why.

## Hard rules

- Report the **ugly truth**. 35% gets reported as 35%, not hidden or rounded down.
- Never editorialize without a number behind it.
- If one cause explains >40% of failures, say so explicitly and name the fix.
- Keep it scannable — this is a measurement, not an essay.
