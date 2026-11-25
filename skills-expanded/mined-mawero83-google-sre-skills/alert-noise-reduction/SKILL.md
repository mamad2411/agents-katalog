---
name: alert-noise-reduction
description: >-
  Diagnose and reduce paging noise using SRE practices: symptom vs cause, actionability, dependency fan-in, flapping, and SLO-based alerting. Use when on-call is drowning, auditing alert health, or cutting false positives.
---

# Alert Noise Reduction

**Domain:** `foundations`  
**Sources:** Workbook Ch5, SRE Book 1e Ch6/10/11, SRE Book 2e Ch10

## When to use

- High pages/day with low real incidents
- Auto-resolve-heavy alert streams
- Pre-ownership noise audits

## Principles

- Noise destroys response quality and retention.
- Every page must demand human action now; else demote.
- Never silence capacity/safety signals by deleting them — retune, dampen, or convert to burn-rate.
- Separate auto-cleared flakes from human-acked work in metrics.

## Workflow

1. Pull ≥28 days of pages: volume, ack/resolve times, auto-resolve rate, top titles.
2. Classify: true positive / flake / duplicate / non-actionable / wrong owner.
3. For top offenders: fix SLI, add hysteresis, dependency suppression, or ticket route.
4. Introduce SLO burn alerts for user impact; demote cause alerts.
5. Re-measure pages/shift and MTTA after 2 weeks.

## Decision guide

- Duplicate storms → group/dedup or suppress children when parent fires.
- Night flakes → confirm window / burn rate, not delete.

## Output template

```markdown
# Noise reduction plan
- Baseline pages/day + auto-resolve %:
- Top 10 noisy alerts + class:
- Fixes (owner, change, ETA):
- Target pages/shift:
- Re-measure date:
```

## Anti-patterns

- Deleting disk/capacity alarms to 'reduce noise'.
- Wide suppressions without expiry.

## Related skills

`alerting-on-slos`, `on-call-excellence`, `pager-hygiene`

## Canonical references

- [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Being On-Call](https://sre.google/sre-book/being-on-call/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
