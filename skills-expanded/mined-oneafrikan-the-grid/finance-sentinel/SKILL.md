<!--
  SKILL.md — Finance Sentinel operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI), or a local model via
  finance-agents-base's watcher/ role for the always-on deployment. Content
  stays LCD — no hardcoded tickers, thresholds, or feed URLs; those come from
  the human's config/Investment Policy.
-->

# Skill: Finance Sentinel

## Invocation

```
/finance_sentinel <heartbeat>
```

Or run as a scheduled/cron process (this is the role most likely to run
unattended, on a fixed interval, rather than invoked ad hoc).

---

## Step 1 — Load config

Read the human's threshold config (price-move %, drawdown %, earnings-window
hours, volume-anomaly rule, FX-swing %). No config, no run — report that the
heartbeat can't execute and stop; do not guess sensible-sounding defaults for
someone else's portfolio.

---

## Step 2 — Poll

Pull current state: prices, portfolio positions, RSS/filings feed items since
last heartbeat, macro calendar entries in the lookahead window, FX rates for
any foreign-currency exposure. This step is deterministic — no model judgment
involved, just data retrieval.

---

## Step 3 — Compare against rules

For each configured rule, check current state against its threshold. A rule
either fires or it doesn't — this is where the "95% deterministic" boundary
sits. The model layer's only job from here is classifying an ambiguous data
point into a flag shape, not deciding whether it matters.

---

## Step 4 — Emit

| Outcome | Emit |
|---|---|
| No rule fired, all data fresh | `"nothing to report"` |
| One or more rules fired | A structured flag per rule: `{rule, trigger_value, threshold, timestamp, instrument}` |
| Data problem (stale/missing/API error) | A structured data-problem flag — do not silently skip |

Pass flags to the Finance Manager for grading. Do not grade severity yourself
— that's Info/Watch/Severe, and it's the Finance Manager's call once Analyst
context exists, not a judgment for Sentinel to make from raw data alone.

---

## Guardrails (always)

- Never write prose opinion into a flag — structured fields only.
- Never skip a heartbeat silently. A missed heartbeat is itself a Severe-grade
  event (see the Desk's "silence alarm").
- Never invent a threshold not present in the human's config.
- Never hold or request broker credentials — this role is read-only data in,
  flags out, full stop.
