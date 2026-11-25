---
description: Print a TokenWise session report — tokens per model, $ saved vs all-Opus baseline, reclassifications, quality flags. Reads from .tokenwise/log.ndjson filtered to the current session. Use when the user asks "how much did I save", "show me tokenwise stats", or runs /tokenwise:report.
---

# /tokenwise:report — Session routing report

Print a routing report for the current Claude Code session.

## Steps

1. **Locate the log file:**
   - Default: `./.tokenwise/log.ndjson` (current project)
   - If user provides a path via `$ARGUMENTS` (e.g. `/tokenwise:report /path/to/log.ndjson`), use that

2. **If the file doesn't exist:**
   ```
   No TokenWise log found at <path>.

   Possible reasons:
   1. TokenWise hasn't logged any routed tasks yet — run a few tasks first
   2. You're in a different project than the one with the log
   3. TokenWise install didn't write the routing rules — check ~/.claude/CLAUDE.md for the "BEGIN TokenWise" marker

   See: /tokenwise:install
   ```

3. **Determine current session:**
   - Look at the most recent contiguous block of log entries with the same `session_id`
   - If `$ARGUMENTS` contains `--session <id>`, use that session_id instead

4. **Aggregate per model:**
   - Group entries by `model_used`
   - Sum `input_tokens`, `output_tokens`, `cost_actual_usd`, `cost_baseline_usd`, `savings_usd`
   - Count tasks per model

5. **Print the report:**

```
TokenWise Session Report
========================

Session ID:       <id>
Started:          <ts of first entry>
Duration:         <wall time>

Tasks routed:     <total count>

Per model:
  Haiku    <count> tasks   <input_sum> input  /  <output_sum> output   →  $<cost_sum>
  Sonnet   <count> tasks   <input_sum> input  /  <output_sum> output   →  $<cost_sum>
  Opus     <count> tasks   <input_sum> input  /  <output_sum> output   →  $<cost_sum>
  Fable    <count> tasks   <input_sum> input  /  <output_sum> output   →  $<cost_sum>

Total spent:                                                              $<total>
Baseline (all-Opus):                                                      $<baseline>
Savings:                                                                  $<savings>  (<pct>%)

Quality flags:
  Reclassifications: <count> (<top reason>)
  User overrides:    <count>
  Regressions:       <count if logged, else "—">

Pricing snapshot:
  Fable 5     $10 / $50 per 1M tokens
  Opus 4.7    $5 / $25
  Sonnet 4.6  $3 / $15
  Haiku 4.5   $1 / $5
```

**Per-model row note:** omit any model row entirely if `<count>` is 0 — Fable's row will legitimately be absent in most sessions. When a Fable row does appear, its `cost_sum` counts toward "Total spent" as normal, but since `cost_baseline_usd` for a Planning task is still priced at Opus, that task's individual `savings_usd` is negative. Don't clamp negative savings to zero; let the total "Savings" line reflect the real (possibly reduced) net.

6. **Format numbers cleanly:**
   - Token counts: `1.2M`, `480K`, `28.4k`
   - Costs: `$1.62`, `$0.017` (keep 2-3 sig figs, no trailing zeros)
   - Percentages: `79.5%` (one decimal)

7. **If $ARGUMENTS contains `--json`**, output the aggregated data as JSON instead of the text report.

## Tools

Read, Bash (for `jq` or simple awk if needed).
