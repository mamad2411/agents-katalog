---
name: tam-scoring
description: >
  Build and run scoring models that tier raw company lists into campaign-ready segments, and point
  each scored data point at the ColdIQ endpoint that sources it. Use when building a scoring model,
  tiering a TAM, defining signal groups and point allocations, setting tier thresholds, cleaning a
  list before scoring, or running a Python scorer on an export. Triggers on "score companies",
  "tier the list", "scoring model", "TAM scoring", "ICP fit score", "tier thresholds", "100-point
  model", "qualify accounts". Do NOT use for enrichment/search to BUILD the list (see apollo-search
  / coldiq-search-enrich), signal sourcing (see signal-detection), or list dedup (see list-dedup).
---

# TAM Scoring

Assign every company a numeric score from observable signals, then bucket into tiers. ColdIQ
models run 80–100 points across 4–6 signal groups. The math is local; this skill notes which
ColdIQ endpoint provides each scored data point so the model runs on fresh data.

## ColdIQ Marketplace Endpoints (data sources for scored fields)

| Scored data point | Method | Path | Credits | Endpoint ID | Notes |
|-------------------|--------|------|---------|-------------|-------|
| Firmographics (size, revenue, industry, funding) | POST | `/v1/limadata/enrich/company` | 1 | `limadata.enrich.company` | One call for most groups |
| Large-scale company list | POST | `/v1/ai-ark/companies` | per result | `ai_ark.companies.search` | Build the list to score |
| Tech-stack signal | POST | `/v1/builtwith/domain` | flat | `builtwith.domain` | Complexity/specialization group |
| Funding / PE backing | GET | `/v1/signalbase/funding-signals` | unknown | `signalbase.funding_signals` | Ownership/bonus groups |

Score from enriched data — don't pay to enrich rows you'll DQ. Filter obvious DQs first, then:
→ **POST** `/v1/limadata/enrich/company` · 1 cr · `limadata.enrich.company`

## Standard tier thresholds

| Tier | Score | Action |
|------|-------|--------|
| Tier 1 | 65+ | Top priority, send first, best personalization |
| Tier 2 | 50–64 | Strong fit, second wave |
| Tier 3 | 35–49 | Marginal, volume plays only |
| DQ | <35 | Do not send |

## Common signal groups

1. **Scale (10–25):** 10k+ → 25, 5k–9,999 → 20, 2k–4,999 → 15, 500–1,999 → 10, 50–499 → 5, <50 → 0.
2. **Revenue (15–20):** $50M–$500M → 20 (sweet spot), $25–50M → 15, $500M–1B → 10, $10–25M → 8, $1B+ → 5.
3. **Industry (10–15):** core → 15, adjacent → 10, stretch → 5, unknown → 5, excluded → −100 (auto-DQ).
4. **Complexity / specialization (15–30):** the client-specific signal (multi-location count, market
   count, competitor/complementary tech, digital maturity).
5. **Ownership / PE (10–20):** PE-backed → 20, PE subsidiary → 15, VC/growth → 10, unknown → 5, founder/non-profit → 0.
6. **Bonus (5–10):** franchise HQ, cash-flow keywords, rapid growth, recent funding, relevant hiring.

## Data cleanup before scoring

```python
BOGUS_NAMES = {"local my business", "google ai plugin", "auto-entrepreneur"}
def is_bogus(name):
    l = name.strip().lower()
    return l in BOGUS_NAMES or any(s in l for s in ["follow us", "test account"])
# Remove slug franchises (keller-williams-realty-dpr), flag extreme values, dedup by name (keep top score).
```

## Python scorer pattern

```python
def score_company(row):
    total, breakdown = 0, []
    for label, fn, field in [("Scale", score_scale, "# Employees"),
                             ("Revenue", score_revenue, "Annual Revenue"),
                             ("Industry", score_industry, "Industry"),
                             ("Custom", score_custom, None)]:
        pts, reason = fn(row if field is None else parse_number(row.get(field, 0)))
        total += pts; breakdown.append(f"{label}: {pts} ({reason})")
    if any("EXCLUDED" in b for b in breakdown): return -1, "DQ", breakdown
    tier = "Tier 1" if total>=65 else "Tier 2" if total>=50 else "Tier 3" if total>=35 else "DQ"
    return total, tier, breakdown
# load → clean(is_bogus) → score → dedup by name(keep highest) → sort desc → export CSV with Score/Tier/Breakdown
```

## How to build a new model

1. Pick 4–6 signal groups summing to 80–100. 2. Set thresholds. 3. Write scoring rules per signal.
4. Clean data. 5. Run on the enriched export. 6. Generate per-tier CSVs. 7. Send a sample to the
client for approval. 8. Re-run when new enrichment data arrives. Dedup first
([list-dedup](../list-dedup/SKILL.md)) so you never score a company twice.
