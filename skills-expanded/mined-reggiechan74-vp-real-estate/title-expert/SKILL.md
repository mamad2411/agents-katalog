---
name: title-expert
description: Use when reviewing title search reports, parsing registered easements/covenants/liens/environmental charges, assessing marketability defects, or quantifying encumbrance discounts during acquisition due diligence. Triggers on Ontario Land Titles searches, restrictive covenant analysis, registration defect detection, and cumulative encumbrance discount calculations.
---

## Overview

A title search is a systematic review of registered property interests that establishes:

- **Chain of ownership**: Who owns the property and for how long.
- **Encumbrances**: What restrictions and interests burden the property.
- **Priority order**: Which interests rank first, second, etc. (determines payment order on default).
- **Defects**: Registration errors, missing signatures, or procedural deficiencies.
- **Marketability**: Whether the property can be freely bought/sold or faces restrictions.

This skill focuses on the **Ontario Land Titles System (LTS)** — state-guaranteed title searched via Land Titles Act registers — which is the most common system for commercial acquisitions in Ontario. Quebec uses a civil-law registry with different methodology; other provinces use a mix of LTS, Torrens, and traditional registry.

### Key Documents to Review

From the title search itself:

1. **Ownership register**: Current registered owner, acquisition date, consideration.
2. **Charges register**: Mortgages, liens, judgment liens (priority determines payment order).
3. **Restrictions register**: Easements, covenants, restrictive covenants (affect use/value).
4. **Sketches/plans**: Property boundaries, easement corridors, affected areas.

Related documents pulled in support: easement schedules, mortgage documents, restrictive covenant agreements, environmental liens (contaminated-site remediation).

## Title Review Framework

The five-step framework below ties together parsing, defect detection, valuation impact, and remedial action. Each step links to a deeper reference file where applicable.

### Step 1 — Parse Registered Instruments

Identify every registered interest and classify it by type: easement, restrictive covenant, lien/mortgage, environmental charge, or notice/caveat. Capture parties, dates, scope (area affected), duration, priority/rank, and operational restrictions.

See **[Encumbrance Catalog](encumbrance-catalog.md)** for full parsing templates and sample registrations covering easements (appurtenant vs. in gross, perpetual vs. term), restrictive covenants (use, building/density, maintenance, special-use), mortgages and judgment/tax/municipal liens, and environmental liens registered under the Environmental Protection Act.

### Step 2 — Classify Each Encumbrance

Each encumbrance falls into one of three impact categories:

- **Physical** (occupies space): transmission/pipeline easements, underground utilities, rights of way.
- **Use** (restricts activities): restrictive covenants, conservation easements, zoning overlays.
- **Payment** (monetary obligation): mortgages, tax liens, environmental remediation liens.

### Step 3 — Detect Registration Defects

Look for procedural errors that could undermine validity or enforceability:

1. Improper property description (vague or inconsistent with reference plan).
2. Missing parties (covenantee no longer identifiable).
3. Signature/authorization defects (signed without authority, missing matrimonial consent).
4. Stale covenants (50+ years old, original purpose obsolete).
5. Priority/rank issues (registered out of chronological order).
6. Discharge/satisfaction not recorded (paid-off mortgage still on title).

See **[LTS Procedural Reference](lts-procedural-reference.md)** for the full defect catalog, the four-step defect assessment process (red flags → cross-reference → risk → remedial priority), and the title-cure playbook (discharge mortgages, modify covenants via Superior Court application, negotiate easement release, environmental remediation plans, priority certificates, subordination agreements).

### Step 4 — Quantify Value Impact

For each encumbrance:

1. **Identify** type and scope (area affected, perpetual vs. term).
2. **Assess** use impact (can owner continue primary use? what's prohibited?).
3. **Calculate** value impact (unencumbered vs. encumbered, percentage reduction).
4. **Assess** long-term relationship impact (regular access? maintenance obligations?).

When multiple encumbrances apply, discounts **compound** rather than sum:

```
Discounted Value = Original Value × (1 − D₁) × (1 − D₂) × (1 − D₃) ...
```

Four methodologies are available — Percentage of Fee, Income Capitalization, Market Extraction (Paired Sales), and Cumulative Discount Analysis. See **[Marketability and Encumbrance Discount Reference](marketability-defects.md)** for detailed worked examples of each methodology, plus buyer-pool, liquidity, and financing-impact analyses.

### Step 5 — Score Marketability and Recommend Remedies

Score the property using the rubric below, classify each encumbrance/defect by severity, and recommend remedial actions (discharge, court application, title insurance, environmental remediation, subordination agreement).

## Encumbrance Impact Summary

Indicative discount ranges by encumbrance type (see [marketability-defects.md](marketability-defects.md) for full derivations):

| Encumbrance Type | Typical Discount Range | Notes |
|------------------|------------------------|-------|
| Utility transmission easement (69kV) | 5-8% | Smaller corridor |
| Utility transmission easement (230kV) | 10-15% | Larger corridor, higher voltage |
| Low-pressure gas pipeline | 10-12% | |
| High-pressure pipeline | 15-20% | |
| Access/drainage easement | 2-8% | Depends on access frequency |
| Restrictive covenant (minor) | 0-3% | Already-restricted-by-zoning use |
| Restrictive covenant (moderate) | 10-20% | E.g., "residential only" in mixed-use zone |
| Restrictive covenant (severe) | 25-40% | E.g., conservation easement — no development |
| Environmental contamination (minor) | 15-25% | Limited scope |
| Environmental contamination (moderate) | 25-40% | 20,000-50,000 tonnes affected |
| Environmental contamination (severe) | 40-60% | 100,000+ tonnes, high remediation cost |

## Canonical Example: Transmission Easement on Farmland

A 100-hectare Class 1 farm is valued unencumbered at $1,000,000 ($10,000/ha). A 230kV transmission easement crosses the property: 10 towers × ~0.04 ha + 1 km access road (~0.6 ha) = ~1.0 ha permanently removed from production.

Direct land loss only: 99 ha × $10,000/ha = $990,000, a $10,000 (1%) reduction.

But operational impacts — field division, blocked center-pivot irrigation, twice-yearly utility access, no building/tree planting in the 60m corridor — compound the loss. Market-extracted paired sales for similar 230kV easements support a **12-14% discount** in practice. Applying 12%: encumbered value = $1,000,000 × (1 − 0.12) = **$880,000**.

If a second encumbrance applies — e.g., a 3% stormwater drainage easement — the cumulative discount is $1,000,000 × 0.88 × 0.97 = **$853,600** (14.6%), slightly less than the 15% sum of individual discounts because the discounts compound.

See [marketability-defects.md](marketability-defects.md) for the full multi-encumbrance commercial example with mortgage payoff and net-equity calculation.

## Marketability Scoring Rubric (0-100)

Assessed across 4 dimensions; score derived from weighted combination.

| Score Range | Rating | Description |
|-------------|--------|-------------|
| 90-100 | EXCELLENT | No material encumbrances; clear title; broad buyer pool; financing readily available |
| 75-89 | GOOD | Minor encumbrances only; easily discharged or insured; no restriction on primary use |
| 60-74 | FAIR | Moderate encumbrances; restricted buyer pool; some financing complexity |
| 40-59 | POOR | Significant encumbrances; development potential impaired; specialized buyer required |
| 0-39 | UNMARKETABLE | Severe encumbrances (environmental lien, unresolvable defect); transaction not feasible without remediation |

**Scoring dimensions**:

1. **Encumbrance Impact** (35%): Physical and use restrictions on primary highest and best use.
2. **Defect Risk** (25%): Registration completeness, party identification, authorization quality.
3. **Buyer Pool** (25%): Breadth of potential purchasers given encumbrances.
4. **Financing Impact** (15%): Lender willingness and LTV impact.

## Severity Matrix

Each encumbrance or defect is classified by severity before scoring:

| Severity | Definition | Examples | Recommended Action |
|----------|-----------|---------|-------------------|
| CRITICAL | Immediately prevents closing or renders title unmarketable | Missing discharge for paid mortgage; active environmental enforcement order; unresolved priority dispute | Must resolve before closing |
| HIGH | Significantly impairs use, value, or financing; requires action before or at closing | Environmental contamination lien; covenant blocking proposed development use; unregistered easement in operation | Should resolve before closing; obtain title insurance minimum |
| MEDIUM | Moderate impact on use or buyer pool; addressable with legal opinion or insurance | Stale restrictive covenant (enforceability uncertain); minor easement reducing development area by 5-10% | Address before closing or obtain covenant insurance |
| LOW | Minimal impact; unlikely to affect transaction or financing | Infrequent access easement; clerical/typographical registration error with clear intent | Monitor; obtain title insurance if lender requires |

## Calculator Tools

### Scripts

- `${CLAUDE_PLUGIN_ROOT}/skills/title-expert/title_analyzer.py` — Title search analysis: parses 14+ registered instrument types, detects registration defects, and generates encumbrance summary tables.
- `${CLAUDE_PLUGIN_ROOT}/skills/title-expert/encumbrance_discount_calculator.py` — Quantifies percentage discount ranges for encumbrances; produces before/after value analysis.

### Usage

```bash
/title-analysis path/to/title_search.json
/title-analysis path/to/title_search.json --output $CLAUDE_PROJECT_DIR/Reports/2025-11-17_title_analysis.md
```

**Report Naming**: `$CLAUDE_PROJECT_DIR/Reports/YYYY-MM-DD_HHMMSS_title_analysis_{pin}.md`

### JSON Input Schema (`title_input_schema.json`)

```json
{
  "property_identifier": "PIN 12345-6789",
  "property_address": "100 Industrial Road, Toronto, ON",
  "registered_instruments": [
    {
      "instrument_number": "AB123456",
      "instrument_type": "Easement",
      "parties": {
        "grantor": "John Smith",
        "grantee": "Hydro One Networks Inc."
      },
      "description": "Hydro transmission easement 20m wide",
      "registration_date": "1985-03-15",
      "area_affected": "2.5 acres"
    },
    {
      "instrument_number": "CD789012",
      "instrument_type": "Covenant",
      "parties": {
        "grantor": "Original Developer",
        "grantee": "Municipality"
      },
      "description": "Restriction to industrial use only",
      "registration_date": "1975-06-20"
    }
  ],
  "restrictions": [
    {
      "type": "Zoning",
      "description": "M2 - General Industrial",
      "impact": "Restricts to industrial uses"
    }
  ],
  "encumbrances": [],
  "defects": []
}
```

## Key Terms

- **Appurtenant easement**: Easement that benefits an adjacent "dominant" property and transfers with the land on sale.
- **Easement in gross**: Easement that benefits a person/entity rather than a property; may not transfer.
- **Covenantor / Covenantee**: Party obligated under a restrictive covenant / party benefiting from it.
- **Runs with the land**: Obligation that binds successive owners, not just the original signatory.
- **Priority / Rank**: Order in which registered charges are paid from sale or foreclosure proceeds.
- **Discharge**: Formal removal of a registered charge (mortgage, lien) once satisfied.
- **Subordination agreement**: Lender agreement to accept a lower-priority position behind another lender.
- **Phase II ESA**: Environmental Site Assessment with intrusive sampling, used to delineate contamination.
- **Closure letter**: Ministry of Environment letter confirming remediation complete and environmental liability cleared.
- **LTV**: Loan-to-value ratio; the proportion of a property's value a lender is willing to finance.
- **Cumulative discount**: Compounded value reduction when multiple encumbrances apply: V × (1 − D₁)(1 − D₂)(1 − D₃)...

## Reference Files

- **[encumbrance-catalog.md](encumbrance-catalog.md)** — Parsing templates and sample registrations for easements, restrictive covenants, liens/mortgages, and environmental charges; physical/use/payment classification.
- **[lts-procedural-reference.md](lts-procedural-reference.md)** — Six common registration defects, four-step defect assessment process, and full title-cure playbook (discharge, court application, insurance, remediation, priority adjustment).
- **[marketability-defects.md](marketability-defects.md)** — Single-encumbrance four-step analysis, multi-encumbrance cumulative impact worked example, buyer pool / liquidity / financing analyses, and four discount methodologies (percentage of fee, income capitalization, paired sales, cumulative).
