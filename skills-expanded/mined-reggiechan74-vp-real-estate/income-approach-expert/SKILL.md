---
name: income-approach-expert
description: Use when valuing telecom ground leases, agricultural rental land, fee interests under ground leases, or perpetual easement income streams. Capitalize land rent to derive value via market rent analysis and cap rate selection (extraction, band of investment, build-up). Key terms: NOI, cap rate, market rent, ground lease, reversion value, sensitivity analysis.
---

## Overview: Income Approach to Land Valuation

The income approach estimates land value by capitalizing the net operating income (NOI) that the land generates as a rental-producing asset. It is particularly applicable to:

- **Telecom sites** (tower ground leases, carrier rental income)
- **Agricultural land** (pasture / row crop rental income)
- **Ground leases** (fee simple land under long-term commercial lease)
- **Easement lands** (perpetual income from utility transmission rights)
- **Parking lots** (surface parking income)
- **Land lease communities** (mobile home parks, RV parks)

**Fundamental formula**:
```
Land Value = Net Operating Income ÷ Capitalization Rate
```

### When to use direct capitalization vs. DCF

- **Direct cap (NOI ÷ Cap Rate)**: Stabilized, near-perpetual income (telecom, agricultural, parking). Default for this skill.
- **DCF**: When the income stream is non-stabilized, term-limited, or has a material reversion (e.g., 25-year ground lease where fee holder regains possession). See the shopping-center walkthrough in `worked-examples.md`.
- **Sales comparison**: Use as a reconciliation check when 3+ comparable income-producing sales exist.

---

## Market Rent Analysis

The foundation of income approach valuation is determining **defensible market rent** for the land use.

### Workflow
1. Identify 3-5 comparable rents in the same market and use class.
2. Adjust for material differences (term, escalation, renewal, maintenance responsibility).
3. Reconcile to a single market rent conclusion.
4. Document reasoning and supporting evidence.

**Ideal comparable criteria**: same use, same market (5-15 km), same lease type, within 12-18 months of valuation date, arm's length.

**Common adjustment directions**:
- Shorter terms → higher rent (non-renewal risk)
- Fixed escalations (2-3%) → 2-5% premium vs. flat
- Commodity / CPI indexation → reduce base rate 5-10% (tenant absorbs less risk)
- Favorable renewals → 3-7% lower base; uncertain renewals → 5-10% higher
- Landlord-maintained → higher rent (landlord bears cost risk)

**For detailed evidence sources, full comparable catalogs (telecom, agricultural), and worked adjustment examples, see [comparable-rent-catalog.md](comparable-rent-catalog.md).**

---

## Capitalization Rate Selection

The **cap rate** converts annual NOI to present value. Selection is the highest-leverage assumption in the analysis: a ±0.5% change typically moves value ±8-10%.

### Three derivation methods

**Method 1 — Market extraction** (preferred when data exists)
```
Cap Rate = NOI ÷ Sale Price
```
Extract from 3+ recent arm's-length sales of comparable income-producing land. Reconcile to a single rate or tight range.

**Method 2 — Band of investment** (weighted cost of capital)
```
Cap Rate = (LTV% × Debt Yield) + (Equity% × Equity Yield)
```
Typical inputs: LTV 50-75%, debt yield 4-6%, equity yield 8-12%.

**Method 3 — Build-up** (risk-free rate plus premiums)
```
Cap Rate = Risk-Free Rate + Liquidity Premium + Inflation Premium + Business Risk
```
Each component must be justified by market evidence.

### Documentation requirements

1. **Extraction**: Show extraction calculation for each of 3+ comps; reconcile to single rate.
2. **Band of investment**: Document LTV / debt yield / equity yield sources; show weighted calculation.
3. **Build-up**: Justify each premium with market evidence; compare result to extracted rates if available.
4. **Sensitivity**: Always show how ±0.5% cap rate variation affects value.

**For comprehensive cap rate ranges by property type, agricultural rent levels by soil class, full band-of-investment and build-up worked components, see [cap-rate-tables.md](cap-rate-tables.md).**

---

## NOI Determination

```
Gross Rental Income     = Market rent × applicable unit
Less:  Vacancy / collection loss
Plus:  Other income (parking, utilities, equipment)
= Effective Gross Income
Less:  Operating expenses
        - Property taxes
        - Insurance
        - Maintenance and repairs
        - Management fees (typically 3-5% of GRI)
        - Utilities (if landlord-paid)
= Net Operating Income
```

---

## Canonical Example: Telecom Ground Lease (Short Form)

**Subject**: Cellular tower ground lease, urban-fringe site, stabilized national-carrier tenant.

| Item | Value |
|------|-------|
| Market rent | $32,000/year |
| Vacancy | 0% |
| Property tax | $2,000 |
| Insurance | $800 |
| Maintenance | $1,200 |
| Management fee (5% × $32,000) | $1,600 |
| **Total OpEx** | **$5,600** |
| **NOI** | **$26,400** |
| Cap rate (extracted, 3 comps) | 6.0% |
| **Land value** = $26,400 ÷ 0.060 | **$440,000** |

Sensitivity at ±0.5% cap rate: $480,000 (5.5%) to $406,154 (6.5%). Conclude $440,000 with range $406K-$480K.

**For full walkthroughs (telecom $35K-rent build, 80-acre Class 2 agricultural with sales reconciliation, 25-year shopping-center ground lease with reversion, perpetual easement, multi-variable scenarios), see [worked-examples.md](worked-examples.md).**

---

## Application by Land Use Type

### Telecom sites
Multi-decade leases with creditworthy carriers; stable income, limited tenant pool, carrier-built improvements, location specificity. Typical cap rates 5.5-7.0% (ground), 6.0-7.5% (rooftop), 7.0-8.5% (co-location).

### Agricultural land
Commodity-exposed rent; annual / short-term leases; deep buyer pool; capital appreciation typically priced in (sales extraction yields 2-4% cap rates that under-state NOI yield). Use 4.0-6.0% cap rate for income approach on partially indexed rent; reconcile against sales.

### Ground leases (fee under long-term lease)
Value the fee in two layers:
```
Fee Value = (Interim Rent ÷ Cap Rate) + (Reversion Value ÷ (1 + Cap Rate)^n)
```
Use a lower cap rate for the contractual interim stream and a higher discount rate for the long-dated reversion.

### Easement lands
Capitalize the income-loss equivalent (or direct easement payment) at a low cap rate (4-5%) given perpetual nature and low risk.

**For per-use cap rate ranges and rent benchmarks, see [cap-rate-tables.md](cap-rate-tables.md). For full per-use valuation walkthroughs, see [worked-examples.md](worked-examples.md).**

---

## Reconciliation with Sales Comparison

Always cross-check the income approach against sales comparison when 3+ comps exist.

- **Income < Sales**: Buyers expect capital appreciation beyond NOI (common for agricultural land); favor sales if well-supported.
- **Income > Sales**: Market may under-price income potential, or sales reflect distressed / non-income attributes; investigate before concluding.

A blended conclusion (e.g., weighted average) is appropriate when both approaches yield credible but divergent results. See the agricultural reconciliation example in `worked-examples.md`.

---

## Integration with Related Appraisal Skills

- **Easement valuation methods**: Income approach is the primary method for valuing perpetual easement income (telecom carrier payments, capitalized agricultural rent loss in transmission corridors).
- **Comparable sales adjustment methodology**: Provides the extraction data set used in cap rate Method 1, and the reconciliation check at the end of the workflow.

---

## Land Capitalization Calculator

**Tool**: `land_capitalization_calculator.py` (located in same folder as this SKILL.md)

**Capabilities**:
- Market rent analysis and reconciliation
- Multiple cap rate derivation methods (extraction, band of investment, build-up)
- NOI calculation with customizable operating expenses
- Land value calculation with sensitivity analysis
- Comparison to comparable sales approach
- PDF report generation

**Input format** (JSON):

```json
{
  "subject_property": {
    "property_type": "telecom_ground_lease",
    "location": "Chicago, IL",
    "size_acres": 0.5,
    "valuation_date": "2024-11-17"
  },
  "market_rent_analysis": {
    "comparable_rents": [
      {
        "rent_annual": 32000,
        "adjustments": {"term_adjustment": 0},
        "source": "Similar tower site, same carrier"
      }
    ],
    "concluded_market_rent": 32000
  },
  "operating_expenses": {
    "property_tax": 2000,
    "insurance": 800,
    "maintenance": 1200,
    "management_fee_percent": 5
  },
  "cap_rate_analysis": {
    "method": "market_extraction",
    "cap_rate_range": {"low": 0.06, "high": 0.09},
    "concluded_cap_rate": 0.060
  }
}
```

**Usage**:

```bash
/income-approach-land path/to/rental_data.json

/income-approach-land path/to/rental_data.json --output $CLAUDE_PROJECT_DIR/Reports/2025-11-17_land_valuation.md
```

**Input Schema**: `land_rental_input_schema.json`

**7-Step Workflow**:

1. **Validate Input**: Validates JSON against `land_rental_input_schema.json`
2. **Analyze Market Rent**: Reconciles comparable rents to market rent conclusion
3. **Select Capitalization Rate** via:
   - Market extraction: Cap Rate = NOI ÷ Sale Price
   - Band of investment: (LTV% × Debt Yield) + (Equity% × Equity Yield)
   - Buildup method: Risk-free + Liquidity + Inflation + Business Risk
4. **Calculate NOI**: Market Rent − Operating Expenses
5. **Calculate Land Value**: NOI ÷ Cap Rate
6. **Reconcile with Sales**: Compare with sales comparison approach (if available)
7. **Sensitivity Analysis**: Test ±0.5% cap rate impact on value; generate timestamped markdown report

**Report Naming**: `$CLAUDE_PROJECT_DIR/Reports/YYYY-MM-DD_HHMMSS_income_approach_{site_type}.md`

**Direct calculator invocation**:
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/income-approach-expert/
python land_capitalization_calculator.py input.json --output results.json --verbose
```

**Output**: NOI breakdown, cap rate justification, land value conclusion, sensitivity tables (±0.5% cap rate, ±5% rent), reconciliation with sales (if provided), PDF appraisal-grade report.

---

## Key Assumptions and Documentation

For defensible appraisal work, document:

1. **Market rent conclusion**: 3+ comparable rents, adjustments shown, sources and timing.
2. **Operating expenses**: Category breakdown, methodology (% GRI, per-unit, market survey), landlord-vs-tenant responsibility.
3. **Capitalization rate**: Primary method, supporting data, ±0.5% sensitivity, comparison to published surveys when available.
4. **Highest and best use**: Why income approach is most appropriate; why other approaches are insufficient.
5. **Limitations**: Lease renewal uncertainty, commodity / weather risk (agricultural), operator credit risk (telecom), thin comparable transaction data.

---

## Key Terms

- **NOI (Net Operating Income)**: Effective gross income less operating expenses.
- **Cap Rate**: NOI ÷ Sale Price (extraction view); the all-in yield that capitalizes stabilized NOI to value.
- **Market Rent**: The rent a property would command in an arm's-length transaction, supported by comparable evidence.
- **Ground Lease**: A long-term lease of land where the tenant typically owns improvements during the lease term; reversion of improvements at lease end depends on the lease.
- **Reversion Value**: The estimated value of the property at the end of the lease term, discounted back to present value.
- **Sensitivity Analysis**: Test of how value changes when key assumptions (cap rate, rent, OpEx) vary by defined increments.
- **Band of Investment**: Cap rate derivation that blends debt and equity yields weighted by capital structure.
- **Build-Up Method**: Cap rate derivation from risk-free rate plus liquidity, inflation, and business risk premiums.

---

## Reference Files

- [cap-rate-tables.md](cap-rate-tables.md) — Cap rate ranges by property type, agricultural rent benchmarks, band-of-investment and build-up component tables, extraction reference set.
- [comparable-rent-catalog.md](comparable-rent-catalog.md) — Telecom and agricultural rent comparable catalogs, full adjustment methodology, evidence sources by use type.
- [worked-examples.md](worked-examples.md) — Full walkthroughs: telecom cellular tower, 80-acre Class 2 agricultural with sales reconciliation, 25-year shopping-center ground lease with reversion, perpetual easement, single- and multi-variable sensitivity scenarios.
