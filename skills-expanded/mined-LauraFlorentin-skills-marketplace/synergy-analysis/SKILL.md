---
name: synergy-analysis
description: >
  Synergy identification, quantification, and validation for M&A transactions.
  Maps overlapping headcount, vendor relationships, and infrastructure across
  buyer and target organizations. Generates cost-takeout plans with
  costs-to-achieve estimates for lender validation and integration planning.
  Use when user asks to "analyze synergies", "cost synergy model", "synergy targets", or mentions revenue synergies, cost savings, or synergy bridge.
---

# Synergy Analysis

Use authorized, minimized employee and vendor data. Aggregate personal data where possible, avoid protected-trait or individual-performance inference, and require HR, employment-law, finance, functional-owner, and works-council review as applicable before workforce actions.

Synergy underwriting provides the mathematical and strategic justification for paying an acquisition premium. Cost synergies — headcount rationalization, facility closures, vendor consolidation — are the most reliable forms of value creation, but identifying them requires mapping two complex organizations.

## The /synergy-map Protocol

### How It Works

1. **Ingest** the target's employee census, benefits data, and third-party spend
2. **Compare** against the acquirer's operating model and vendor lists
3. **Identify** overlapping functions:
   - Duplicate back-office roles (dual ERP teams, redundant HR, overlapping finance)
   - Redundant regional sales coverage
   - Duplicated vendor relationships (same cloud provider, same audit firm)
4. **Quantify** savings with confidence ratings
5. **Estimate** costs to achieve (severance, lease breaks, migration costs)

Record the source, owner, timing, dependency, cost to achieve, and confidence for every synergy. Do not promise a fixed productivity gain.

### Output Format

```
## Synergy Map — [Target] + [Acquirer]

### Summary
| Category | Identified Run-Rate Savings | Costs to Achieve | Net Year 1 Impact |
|----------|---------------------------|-------------------|-------------------|
| Headcount | $[X]M | $[X]M | $[X]M |
| Third-Party Spend | $[X]M | $[X]M | $[X]M |
| Facilities | $[X]M | $[X]M | $[X]M |
| Technology | $[X]M | $[X]M | $[X]M |
| **Total** | **$[X]M** | **$[X]M** | **$[X]M** |

### Headcount Overlap
| Function | Target FTEs | Acquirer FTEs | Redundant | Savings | Confidence |
|----------|-------------|---------------|-----------|---------|------------|
| Finance & Accounting | [N] | [N] | [N] | $[X]K | High |
| IT Operations | [N] | [N] | [N] | $[X]K | Medium |
| Sales (Regional) | [N] | [N] | [N] | $[X]K | Low |

### Vendor Consolidation
| Vendor/Category | Target Spend | Acquirer Spend | Estimated Saving | Mechanism |
|----------------|-------------|----------------|-----------------|-----------|
| Cloud hosting | $[X]K | $[X]K | $[X]K | Volume renegotiation |
| Audit/Tax | $[X]K | $[X]K | $[X]K | Consolidate to single firm |

### Costs to Achieve
| Item | Estimate | Timing |
|------|----------|--------|
| Severance (redundant FTEs) | $[X]M | Months 1-6 |
| Lease termination penalties | $[X]K | Months 3-9 |
| IT migration costs | $[X]K | Months 1-12 |
| Retention bonuses (key talent) | $[X]K | Months 1-24 |
```

## Synergy and Cost Savings Report

The formal deliverable that moves beyond the mapping to a validated, defended analysis:

| Section | Focus |
|---------|-------|
| Synergy Thesis & Strategy | Strategic rationale and integration philosophy |
| Headcount & Organizational Overlap | Quantified role-level redundancies |
| Third-Party Spend Rationalization | Vendor pricing leverage and consolidation |
| Technology & Infrastructure | ERP migration, license elimination, real estate |
| Costs to Achieve | One-time expenditures: severance, lease breaks, IT migration |

## Operating Guidelines

- Synergies are notoriously overestimated — apply conservative assumptions
- Distinguish between **run-rate savings** (annual) and **one-time gains**
- Always include costs to achieve — synergies without execution costs are misleading
- Confidence ratings: **High** (contractual/observable), **Medium** (benchmarked), **Low** (estimated)
- Lenders demand third-party validation — ensure the analysis is independently defensible
- Revenue synergies are speculative and should be separated from cost synergies
- Flag any synergy that depends on retaining key personnel who may have flight risk


## Examples

**Input**: "Estimate synergies from acquiring a 200-person SaaS company."

**Quick synergy model output**:
| Category | Run-Rate Savings | Costs to Achieve | Net Year-1 |
|---|---|---|---|
| Headcount (G&A overlap) | $8.4M | $3.2M | $5.2M |
| Software/vendor consolidation | $1.8M | $0.3M | $1.5M |
| Facilities (office consolidation) | $0.9M | $0.4M | $0.5M |
| **Total** | **$11.1M** | **$3.9M** | **$7.2M** |

**Confidence**: Medium (benchmarked against 12 comparable SaaS acquisitions).


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Synergy estimates rejected by lenders | No third-party validation | Reference comparable transaction benchmarks; show methodology |
| Revenue synergies overstated | Optimism bias | Separate cost and revenue synergies; apply 50% haircut to revenue synergies |
| Costs to achieve underestimated | Missing one-time items | Use M&A database benchmarks for severance ($X per redundant FTE) |
| Model doesn't account for dis-synergies | One-sided analysis | Explicitly model customer churn risk and key-man retention cost |
