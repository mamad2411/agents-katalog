---
name: multi-category-scan-pattern
description: >-
  Scan across multiple opportunity categories (MES, AI/ML, DevOps, MedTech, GovCon)
  in parallel and detect when market activity shifts between them. Covers extended
  quiet period detection, cross-category pivot triggers, and scan orchestration.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [c2c, research, scanning, market-intelligence, quiet-period, opportunity-hunting]
    triggers: [multi-category scan, cross-category, c2c hunter, opportunity scan, quiet period, market shift]
    related_skills: [gpt-researcher, recurring-status-checks]
---

# Multi-Category Scan Pattern

When running recurring C2C opportunity scans across multiple categories (MES, AI/ML,
DevOps, MedTech, GovCon), market activity does not stay evenly distributed. One
category may dominate for weeks while others remain silent, then activity shifts.

This skill covers the scan orchestration pattern, quiet period detection, and
cross-category pivot triggers that the generic `gpt-researcher` skill does not
specialize in.

## Scan Architecture

### Category Template

Each category uses the same scan pattern:

1. **DDG Lite broad query** — 1-2 bare-keyword queries via r.jina.ai
2. **`site:dice.com` targeted query** — specific role keywords, $/hr filters
3. **`site:linkedin.com` recruiter post query** — activity post discovery
4. **LinkedIn post extraction** — try the post URL through jina.ai

### 5-Category Sweep

Run one DDG Lite query per category in parallel (or sequentially). The standard
categories are:

| # | Category | Example Query | Expected Sources |
|---|----------|--------------|-----------------|
| 1 | MES Solumina | `Solumina+MES+C2C+contract+remote+2026` | Dice, LinkedIn, SmartRecruiters |
| 2 | AI/ML Agentic | `site:dice.com+Agentic+AI+engineer+remote+contract+C2C` | Dice, agentic-engineering-jobs.com |
| 3 | DevOps | `C2C+DevOps+contractor+remote+Docker+Kubernetes+2026` | consultant.dev, aggregators |
| 4 | MedTech | `C2C+MedTech+healthtech+data+engineering+remote+contract+2026` | join-this.com, aggregators |
| 5 | GovCon | `C2C+GovCon+cleared+remote+contract+2026` | clearedcareers.com, SAM.gov |

### Resource-Constrained Scan (6 queries in ~35s)

When running in cron context with sequential terminal() calls, execute 5 queries
(one per category) plus one cross-category sweep. Each query ≈ 6-30s. Combined
with processing time, a full sweep completes in ~35-60s. Reserve `site:dice.com`
queries for categories that have shown the most recent activity.

## Quiet Period Detection

### Per-Category Quiet Period Tracking

```python
# Track consecutive [SILENT] runs per category
# Format stored in cron job context or reference file
category_quiet_days = {
    "MES": 14,      # Last actionable lead: Jul 14
    "AI/ML": 0,     # Lead found this cycle
    "DevOps": 14,   # Never had actionable leads
    "MedTech": 14,  # Last stale lead: April 2026
    "GovCon": 14,   # Never had actionable leads
}
```

### Cross-Category Shift Trigger

When a category reaches **14+ consecutive days** without actionable leads:

1. **Do NOT** keep hammering the same queries — the market in that niche may have
   genuinely paused (new funding rounds, program starts, end-client budget cycles)
2. **Shift focus** to the next most-promising category — run broader queries there
   with lower rate thresholds
3. **Break-glass technique:** Use `site:dice.com` in DDG Lite for each remaining
   category in sequence — Dice's cache frequently surfaces leads that generic
   keyword queries miss during quiet periods
4. **If all categories are quiet** (7-21 day extended quiet), the market itself
   has paused. Respond [SILENT] and wait for the next cycle.

### Confirmed Pattern (Jul 2026)

MES Solumina went quiet for 14+ days (last real report Jul 14). The next actionable
lead came from the AI/ML Agentic category (ConglomerateIT, $90/hr C2C Azure AI
Foundry role) — not from the Solumina niche. This validated the cross-category
shift model.

## Lead Quality Thresholds

Different categories have different rate floors:

| Category | Rate Floor | Actionable At | Notes |
|----------|-----------|---------------|-------|
| MES Solumina L2 Support | $50-65/hr | Below floor | Market rate, not premium |
| MES Solumina Migration SME | $80-120/hr | At floor | Rare — premium niche |
| AI/ML Agentic Engineer | $80-90/hr | At floor | Emerging C2C market |
| AI/ML GenAI Harness | Unconfirmed | — | Too new to establish floor |
| DevOps/Platform | $50-100/hr | Variable | Wide range, depends on stack |
| MedTech Data Engineering | $50-80/hr | Below floor | Stale postings dominate |
| GovCon Cleared | $80-150/hr | At floor | Requires clearance |

When a category consistently produces leads below floor for 3+ consecutive scans,
document the "market rate shift" but don't break silence for below-floor leads alone.
Exception: if the below-floor lead has outstanding contact signals (direct recruiter
email, phone, same-day posting), report it as intelligence even if rate is below
target.

## Pitfalls

- **Do NOT assume the dominant category will remain dominant.** After 14+ days quiet,
  the next active category may be completely different.
- **Do NOT use the same query patterns across all categories.** MES benefits from
  product-name keywords (Solumina, ExampleVendor); AI/ML benefits from framework keywords
  (MCP, LangChain, CrewAI); DevOps benefits from tool keywords (K8s, Docker).
- **Do NOT surface a lead from a previously-quiet category without running the
  recruiter-name dedup check** against prior cron outputs.
- **Do NOT treat one category's success as permission to report on all categories.**
  Report only the category(ies) with genuinely new findings.
