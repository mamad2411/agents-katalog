---
name: alerting-on-slos
description: >-
  Turn SLOs into actionable multi-window multi-burn-rate alerts that page on significant error-budget consumption. Use when creating burn alerts, replacing threshold spam, or tuning pages-per-shift.
---

# Alerting On SLOS

**Domain:** `foundations`  
**Sources:** Workbook Ch5, SRE Book 1e Ch10

## When to use

- Converting SLOs into pages
- Alert fatigue from static thresholds
- Designing fast/slow burn alerts

## Principles

- Alert on significant budget burn, not every blip.
- Multi-window multi-burn-rate detects both fast outages and slow leaks.
- Good alerts: actionable, investigable, unique ownership.
- Ticket/queue for low urgency; page only for human-now work.

## Workflow

1. Confirm SLI event counts exist at alerting resolution.
2. Choose budget window (e.g. 28d / 30d).
3. Configure at least: fast burn (short window, high burn rate) + slow burn.
4. Simulate against past incidents: would it have paged? false positives?
5. Route: page vs ticket vs Slack; document runbook link in alert.
6. Measure pages/shift; iterate until sustainable (~2/shift aspirational classic guidance — adapt to team).

## Decision guide

- Low-traffic services: require min volume or longer windows to avoid noise.
- If alert never fires and outages happen → SLI wrong or thresholds too lax.

## Output template

```markdown
# Burn-alert design
- SLO + window:
- Fast burn: windows + rate + notify:
- Slow burn: windows + rate + notify:
- Exhaustion / projection (optional):
- Runbook URL:
- Validation against past incidents:
```

## Anti-patterns

- Threshold on raw QPS without budget context.
- Paging on every 5xx spike without burn math.

## Mental model

Burn rate 1 = spending budget exactly on pace for the window.
Burn rate 14 ≈ exhaust monthly budget in ~2 days — typically page-worthy with a short confirmation window.
Always pair long + short windows to cut flapping.


## Related skills

`sli-slo-design`, `alert-noise-reduction`, `on-call-excellence`

## Canonical references

- [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Practical Alerting](https://sre.google/sre-book/practical-alerting/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
