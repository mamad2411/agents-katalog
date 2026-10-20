---
name: easement-valuation-methods
description: Use when valuing utility transmission easements, pipeline corridors, rail/transit corridors, access easements, telecom sites, or temporary construction easements. Apply percentage of fee method, income capitalization, before/after paired sales, or rate-of-return for TCEs. Key terms: percentage of fee, income capitalization, paired sales, discount rate, agricultural rent, TCE.
---

## Scope

This is the canonical easement-valuation skill in the marketplace. Other skills (notably `right-of-way-expert`) reference this skill rather than duplicate its methodology. Keep it self-contained and authoritative.

## Professional Standards Compliance

Methodology is compliant with **USPAP 2024** (USA), **CUSPAP 2024** (Canada), **Yellow Book / UASFLA** (US federal acquisitions), and **IVS 2022** (international, IVS 105).

**Core principles**:
- **Before-and-After Method** is the preferred approach for partial takings and easements.
- Develop scope of work appropriate to assignment complexity, intended use, and jurisdiction.
- Analyze **highest and best use** in both Before and After conditions.
- **Reconcile** approaches through reasoned weighting, never simple averaging.
- Extract easement percentages from paired sales empirically when data allows.

For the full standards treatment, reconciliation framework (Steps 1-5), adjustment hierarchy, and related-skill integration, see [`compliance-framework.md`](./compliance-framework.md).

## The Five Valuation Methods

| # | Method | When to Use | Core Formula |
|---|--------|-------------|--------------|
| 1 | **Before-and-After** | Preferred for partial takings, federal acquisitions (Yellow Book), Ontario expropriations, most USPAP/CUSPAP assignments | Value Before − Value After = Compensation |
| 2 | **Percentage of Fee** | Quick estimate; published ranges available for the corridor type; supplemental support for other methods | Easement Value = Fee Value × Easement % × Affected Area |
| 3 | **Income Capitalization** | Revenue-generating easements (telecom, agricultural rent loss measurable); perpetual duration; reliable cap rate | Easement Value = Annual Income Loss ÷ Cap Rate |
| 4 | **Before/After Paired Sales (market extraction)** | Excellent paired sales available; only difference is the easement; statistical validation possible | Easement % = (Comp w/o Easement − Comp w/ Easement) ÷ Comp w/o Easement |
| 5 | **Rate-of-Return (TCEs only)** | Temporary construction easements when rental market data unavailable | TCE Value = Fee Value × Annual Rate × (Days ÷ 365) + Damage + Business Losses |

### Method 1 — Before-and-After (Preferred for Partial Takings)

The federal method, preferred under USPAP/CUSPAP for partial takings:

```
Compensation = Value of entire property BEFORE easement
             − Value of entire property AFTER easement
```

Equivalent to the **Take-Plus-Damages** framework (direct land taken + severance damages to remainder), which is sometimes required by client/jurisdiction for itemized reporting. The two frameworks are mathematically equivalent when properly applied. See [`worked-examples.md`](./worked-examples.md) §2 for a side-by-side numerical comparison.

For severance damages to the remainder parcel (access loss, shape irregularity, farm operation disruption), use the **`severance-damages-quantification`** skill.

### Method 2 — Percentage of Fee

Historical market analysis shows a **5-35% range by easement type**. Quick reference:

| Easement Type | Typical % of Fee |
|---------------|------------------|
| Access easements | 5-15% |
| Utility transmission (legacy ranges) | 10-25% |
| Pipeline corridors (legacy ranges) | 15-30% |
| Modern IRWA-aligned calculator ranges | 25-40%+ |

Full base-percentage tables (by voltage, rail type, pipeline product, and corridor sub-type) plus all domain-specific adjustments live in [`compensation-tables.md`](./compensation-tables.md).

### Method 3 — Income Capitalization

Convert annual rental income (or productivity loss) to capital value using a cap rate adjusted for easement permanence and risk:

```
Easement Value = Annual Income Loss ÷ Capitalization Rate
```

**Discount rate selection** (full table in [`compensation-tables.md`](./compensation-tables.md) §5):
- Perpetual government/utility: 4-5%
- Perpetual private party: 5-6%
- Long-term: +1% above perpetual
- Medium-term: +2% above perpetual
- Temporary (1-5 yr): valued as lump-sum, not capitalized

**Adjustments**: +0.5-1% for uncertain renewal; +1-2% for risky operators; -0.5% for government guarantees; -0.5-1% for indexed escalations.

Agricultural-rent and telecom-site rental tables are in [`compensation-tables.md`](./compensation-tables.md) §5; worked example for agricultural land is in [`worked-examples.md`](./worked-examples.md) §1.

### Method 4 — Before/After Paired Sales (Market Extraction)

**Ideal paired sales criteria**:
- Same market area (within 5-10 km)
- Same highest and best use
- Same size class (±25% land area)
- Similar physical characteristics (topography, soil, access, services)
- Sale timing within 12-18 months
- Only difference: presence/absence of easement

**Extraction**:
```
Easement % of total property = (Adjusted no-easement value − Adjusted w-easement value) ÷ no-easement value
Easement % of affected acres   = Total-property % ÷ (Affected acres ÷ Total acres)
```

For 10+ paired sales, use hedonic regression:
```
Sale Price = β₀ + β₁(Acres) + β₂(Soil Class) + β₃(Frontage)
           + β₄(Easement Presence) + β₅(Easement Acres) + ε
```
Implied easement percentage = β₅ ÷ fee-simple per-acre value. Statistical thresholds: R² > 0.70, p < 0.05, VIF < 10.

Full adjustment grid, regression interpretation, and a worked extraction are in [`worked-examples.md`](./worked-examples.md) §3.

For rigorous comparable-sales adjustment methodology, use the **`comparable-sales-adjustment-methodology`** skill.

### Method 5 — Rate-of-Return (TCEs)

Temporary construction easements use **rental value for duration** plus restoration costs, not capitalized perpetual income.

**Preferred — Fair Market Rental**: research comparable land rents, apply to affected area, prorate for duration, add damage / restoration / business losses.

**Fallback — Rate-of-Return** (when rental market data unavailable):
```
TCE Value = (Affected Fee Simple Value × Annual Rate × Days ÷ 365)
          + Physical Damage Restoration Costs
          + Business / Operational Losses
```

**Annual rates** ([`compensation-tables.md`](./compensation-tables.md) §5):
- 6% — conservative, government agencies (Austin, TX precedent)
- 10% — industry standard for private utility projects (most common)
- 12%+ — high-disruption sites, premium locations, lengthy duration

**Duration adjustments**: short (<30 days) — daily rate may exceed prorated annual due to fixed setup costs; medium (3-12 months) — standard prorated calculation; long (1-3 years) — may approach permanent easement value; apply 2-4%/yr escalation.

Worked TCE examples (agricultural rental method and industrial rate-of-return method, plus 3-year escalation calculation) are in [`worked-examples.md`](./worked-examples.md) §4.

For construction-period noise / dust / vibration / traffic impacts, use the **`injurious-affection-assessment`** skill.

## Specialized Calculators

Three domain calculators wrap the shared core (`easement_calculator_base.py`) with corridor-specific base percentages, adjustments, and reconciliation weights.

| Calculator | Required Param | Default Reconciliation Weights |
|------------|----------------|--------------------------------|
| `hydro_easement_calculator.py` (transmission lines) | `voltage_kv` | 50% % of fee / 30% income / 20% before-after |
| `rail_easement_calculator.py` (rail / transit) | `rail_type` (+ optional `rail_alignment`) | 50% % of fee / 20% income / 30% before-after |
| `pipeline_easement_calculator.py` (pipelines / subsurface) | `pipeline_type` | 45% % of fee / 30% income / 25% before-after |

Full base percentages and adjustment factors per calculator are in [`compensation-tables.md`](./compensation-tables.md) §§1-3.

**Shared core capabilities** (`easement_calculator_base.py`): TCE rate-of-return, income capitalization, before/after comparison, dynamic reconciliation, sensitivity analysis.

## Canonical Example — 230 kV Transmission Easement Across Class 1 Farmland

Subject: 15-acre permanent easement on 100-acre Class 1 farm; fee simple value $12,000/acre.

| Approach | Calculation | Indicated Value |
|----------|-------------|-----------------|
| Percentage of fee | 15 ac × $12,000/ac × 15% | $27,000 |
| Income capitalization | 15 ac × $60/ac annual loss ÷ 4.5% cap | $20,000 |
| Before/after paired sales | One paired-sale analysis (adjusted) | $24,000 |

Weighting 40% / 30% / 30% → weighted average **$24,000**; range $20,000-$27,000; **final reconciled value $25,000** after sensitivity testing (cap rate ±1%, percentage ±5%).

Full reasoning, sensitivity check, and a parallel before-and-after vs. take-plus-damages comparison are in [`worked-examples.md`](./worked-examples.md) §§2 and 5.

## Key Terms

- **Before-and-After Method** — value of entire property before easement minus value after easement; preferred under USPAP/CUSPAP/Yellow Book for partial takings.
- **Take-Plus-Damages Method** — direct land taken plus severance damages to remainder; mathematically equivalent to Before-and-After when properly applied.
- **Percentage of Fee** — easement value expressed as a percentage of underlying fee simple land value.
- **Income Capitalization** — converts annual income loss to capital value using risk-adjusted cap rate.
- **Paired Sales (Market Extraction)** — empirical extraction of easement % impact from comparable sales differing only in easement presence.
- **Discount Rate / Capitalization Rate** — rate used to convert future income streams to present value; varies by easement permanence and operator risk.
- **Agricultural Rent** — annual rent per acre for comparable farmland; basis for productivity-loss income capitalization.
- **TCE (Temporary Construction Easement)** — short-duration easement valued by fair-market rental or rate-of-return method, not capitalized perpetual income.
- **Rate-of-Return Method** — TCE valuation applying annual rate (typically 10%) to affected fee simple value, prorated for duration.
- **Severance Damages** — damages to the remainder parcel from access loss, shape irregularity, or operational disruption. See `severance-damages-quantification`.
- **Injurious Affection** — construction or proximity impacts (noise, dust, vibration, traffic). See `injurious-affection-assessment`.
- **Reconciliation** — reasoned weighting of multiple approaches to a single value indication; not a simple average.

## Reference Files in This Directory

- [`compensation-tables.md`](./compensation-tables.md) — base percentages and adjustments for hydro, rail, pipeline calculators; agricultural rent and telecom rental tables; discount and TCE rate tables.
- [`worked-examples.md`](./worked-examples.md) — detailed walkthroughs per method (income cap, before-after vs. take-plus-damages, paired sales with adjustment grid and regression, TCE rental and rate-of-return, full reconciliation example, end-to-end transmission workflow).
- [`compliance-framework.md`](./compliance-framework.md) — USPAP/CUSPAP/Yellow Book/IVS deep dive; reconciliation framework (Steps 1-5); adjustment hierarchy; related-skill integration.
- `VERSION.md` — version history (do not edit unless updating versioning).
- Calculators: `hydro_easement_calculator.py`, `rail_easement_calculator.py`, `pipeline_easement_calculator.py`, `easement_calculator_base.py`, plus input schemas and tests.
