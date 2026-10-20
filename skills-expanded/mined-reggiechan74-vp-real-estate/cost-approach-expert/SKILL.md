---
name: cost-approach-expert
description: Use when valuing transmission towers, telecom sites, substations, or specialized infrastructure where market comparables are unavailable or incomplete. Apply replacement cost new (RCN) less depreciation, or reconcile cost approach with limited market data. Key terms: RCN, physical/functional/external depreciation, indirect costs, age-life method, depreciated replacement cost.
---

## Overview — When to Use the Cost Approach

The cost approach is the appropriate primary method when market comparables are limited or non-comparable, which is typical for:

- Transmission towers (69kV, 138kV, 230kV+)
- Telecom sites (tower + ground station equipment)
- High-voltage substations
- Specialized equipment (HVDC converters, etc.)

Value is built up from the **Replacement Cost New (RCN)** of an equivalent modern asset, less three categories of depreciation, then reconciled with market data when comparables exist.

**Formula**

```
Depreciated Replacement Cost (DRC) = RCN
                                   – Physical Depreciation
                                   – Functional Obsolescence
                                   – External Obsolescence
```

---

## Implementation — Calculator Tool

**File**: `infrastructure_cost_calculator.py` (same folder as this SKILL.md)

**Capabilities**:

- RCN estimation from component materials, labor, and overhead
- All three depreciation categories (physical age/life and observed condition; functional; external)
- Asset-specific calculators for transmission towers, telecom sites, substations
- Depreciation schedule analysis by component and time period
- DRC calculation and reconciliation with market approach
- USPAP 2024 / CUSPAP 2024 compliant output

### Input Format

JSON structure (see `sample_transmission_tower.json`, `sample_telecom_site.json`, `sample_substation.json`, `sample_specialized_equipment.json` for complete examples):

```json
{
  "asset_type": "transmission_tower",
  "asset_description": "69kV lattice tower, H-frame, 120ft height",
  "location": { "jurisdiction": "Ontario", "transmission_class": "69kV" },
  "valuation_date": "2025-11-17",
  "replacement_cost_new": {
    "materials": { "steel_structure": 85000, "insulators_hardware": 15000, "foundation_concrete": 25000, "grounding_system": 8000, "access_ladder": 3000, "miscellaneous": 4000 },
    "labor": { "fabrication_assembly": 40000, "site_preparation": 12000, "installation_erection": 35000, "testing_commissioning": 8000 },
    "overhead_and_profit": { "general_overhead_percent": 15, "contractor_profit_percent": 12, "engineer_inspection_percent": 3 }
  },
  "physical_depreciation": { "method": "age_life", "effective_age_years": 15, "remaining_useful_life_years": 30 },
  "functional_obsolescence": { "design_efficiency": { "estimated_cost": 8000 } },
  "external_obsolescence": { "economic_factors": { "estimated_cost": -15000 } },
  "market_approach_reconciliation": { "comparable_sales": [], "cost_approach_value": 240000 }
}
```

### Usage

```bash
cd plugins/appraisal-valuation/skills/cost-approach-expert/
python infrastructure_cost_calculator.py input.json --output results.json --verbose
```

**When assisting users**:

1. Identify asset type (tower / telecom / substation / specialized)
2. Gather cost data (materials, labor, overhead, profit)
3. Analyze condition (effective age, observed deterioration)
4. Assess obsolescence (design, capacity, market changes)
5. Create JSON input from a sample template
6. Run calculator and analyze RCN, depreciation, DRC
7. Reconcile with market approach if comparables exist
8. Document findings: cost breakdown, depreciation justification, final value

### Output Highlights

- `replacement_cost_new`: materials, labor, overhead, profit subtotals → `total_rcn`
- `depreciation_analysis`: physical, functional, external components and totals
- `depreciated_replacement_cost`: RCN minus total depreciation
- `reconciliation`: market approach comparison, weighting, final value
- `compliance`: USPAP / CUSPAP / IVS flags

---

## Framework

### 1. Replacement Cost New (RCN)

The cost to construct an equivalent substitute asset at current market prices using modern methods. Three buckets:

- **Materials** — structure, insulators, foundation, grounding, equipment
- **Labor** — fabrication, site prep, erection, installation, testing (typically 30%–50% of materials for site assembly)
- **Indirect costs** — general overhead (12%–18% of direct costs) plus contractor profit (10%–15%)

For component-level cost ranges by asset type, see **[rcn-cost-tables.md](./rcn-cost-tables.md)**.

### 2. Three Depreciation Categories

| Category                  | What it Captures                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------- |
| **Physical**              | Loss in value from age, wear and tear, and observed deterioration                                  |
| **Functional Obsolescence** | Design inefficiencies, excess/inadequate capacity, operational deficiencies not curable by maintenance |
| **External Obsolescence** | Loss from factors external to the asset — market, regulatory, and economic conditions              |

**Physical depreciation** is computed with the age/life method, often refined by an observed-condition adjustment:

```
Physical Depreciation % = (Effective Age / Total Economic Life) × 100%
```

Where **Effective Age** is how old the asset appears based on condition (may differ from chronological age) and **Total Economic Life** is the total years the asset remains physically and functionally useful. Observed-condition adjustments come from rating structural integrity, corrosion, paint/coating, and hardware on an Excellent / Good / Fair / Poor scale and translating each into a percentage adjustment.

**Functional obsolescence** typically falls into three sub-categories:

- **Capacity issues** — excess capacity (oversized) or inadequate capacity (undersized, requiring future upgrade). Inadequate capacity is often quantified as the present value of the future upgrade cost.
- **Design efficiency** — outdated safety systems, missing climate control, poor maintenance accessibility.
- **Operational deficiencies** — environmental non-compliance (e.g., transformer-oil containment), single-point-of-failure controls, lack of remote monitoring (SCADA).

**External obsolescence** captures three external pressures:

- **Market conditions** — energy demand/supply, grid modernization, market saturation (especially in telecom)
- **Regulatory changes** — safety codes, SF6 phase-out, grid interconnection standards
- **Economic factors** — energy transition (coal retirement vs. renewable growth), interest-rate cycles, technological displacement (HVDC over AC, small-cell over macro-tower)

For asset-specific economic lives, the full condition rating tables, capacity present-value calculations, regulatory cost ranges, and full worked examples, see **[depreciation-examples.md](./depreciation-examples.md)**.

### 3. Canonical Example — Transmission Tower DRC

- **RCN**: $240,000
- **Physical depreciation**: 32.5% age/life + minor condition adjustment = **$85,200**
- **Functional obsolescence**: inadequate capacity + safety system deficiency = **$53,000**
- **External obsolescence**: grid modernization + energy transition = **$32,000**
- **Total depreciation**: $170,200
- **Depreciated Replacement Cost**: $240,000 – $170,200 = **$69,800**

The full step-by-step buildup, component-level depreciation schedule, and a second worked example for a telecom ground station are in **[depreciation-examples.md](./depreciation-examples.md)**.

---

## Reconciliation with Market Approach

When comparable sales exist, reconcile cost and market approaches:

1. **Identify comparable sales** — similar asset class, location, recent (within 2–3 years)
2. **Adjust comparables** — for asset type, height/capacity, location, condition
3. **Develop market value** — weighted range from adjusted comparables
4. **Compare and reconcile** — explain variance; weight approaches by data quality
5. **Conclude final value** — typically weighted average (e.g., 60% market / 40% cost when comps are strong)

**Example reconciliation**

```
Cost Approach Value:    $69,800
Market Approach Value:  $78,000
Weighted (40% / 60%):   $74,720  → rounded $75,000
```

When market comparables are limited or unavailable, the cost approach becomes primary. Strengthen it with multiple RCN sources, detailed condition inspection, expert input, and sensitivity analysis.

---

## Asset-Class Application

The cost approach buildup differs materially by asset class. For per-asset deep dives — RCN component buildups, typical depreciation profiles, and market validation considerations — see **[infrastructure-types.md](./infrastructure-types.md)**, which covers:

- Transmission towers (69kV / 138kV / 230kV+)
- Telecom sites (tower + ground equipment + shelter)
- High-voltage substations (multi-component, regulatory-driven)
- Integration with comparable sales and transmission-line technical analysis skills

---

## Slash Command

**Command**: `/cost-approach-infrastructure <input-json-path> [--output <report-path>]`

```bash
/cost-approach-infrastructure path/to/construction_data.json
/cost-approach-infrastructure path/to/construction_data.json --output $CLAUDE_PROJECT_DIR/Reports/2025-11-17_infrastructure_valuation.md
```

**Input schema**: `infrastructure_cost_input_schema.json`

**7-step workflow**:

1. Validate input JSON against schema
2. Calculate RCN (direct costs + overhead 12%–18% + profit 10%–15%)
3. Analyze physical depreciation (age/life and/or observed condition)
4. Assess functional obsolescence (design, capacity, operational)
5. Assess external obsolescence (market, regulatory, economic)
6. Calculate Depreciated Replacement Cost
7. Reconcile with market (if comparables provided) and emit timestamped markdown report

**Report naming**: `$CLAUDE_PROJECT_DIR/Reports/YYYY-MM-DD_HHMMSS_cost_approach_{asset_type}.md`

---

## Key Assumptions and Limitations

**Assumptions**

1. Replacement with similar (not necessarily identical) modern asset
2. Straight-line physical depreciation, refined by observed condition
3. Stable labor and material prices over 2–3 year horizon
4. Asset continues in same use (functional re-purposing triggers re-valuation)

**Limitations**

1. Incomplete market data increases reliance on assumption accuracy
2. Technological change (smart grid, renewables) creates external obsolescence uncertainty
3. Pending regulations create moving compliance-cost targets
4. Location-specific geological/weather factors hard to quantify
5. Substation and transmission asset value tied to broader system; isolated valuation may miss integration benefits

**Mitigation**: sensitivity analysis, expert interviews, scenario modeling, annual re-valuation.

---

## Professional Standards

**USPAP 2024** — Standards 7 (Development) and 8 (Reporting) of the cost approach require documented RCN basis, justified depreciation rates, explained comparable adjustments, stated limiting conditions, and proper reconciliation.

**CUSPAP 2024** — Canadian cost indices and economic-life assumptions; Tax Act compliance; reference CUSPAP Value Definitions and Approaches.

**IVS** — Document market conditions at valuation date, identify cost-data sources, support economic-life assumptions with objective evidence, and clearly distinguish curable vs. incurable obsolescence.

---

## Key Terms

- **RCN (Replacement Cost New)** — Cost to construct an equivalent modern substitute asset at current prices.
- **Depreciated Replacement Cost (DRC)** — RCN less physical, functional, and external depreciation.
- **Effective Age** — How old the asset appears based on condition (may differ from chronological age).
- **Economic Life** — Total years an asset remains physically and functionally useful.
- **Age/Life Method** — Physical depreciation = (Effective Age / Economic Life) × RCN.
- **Physical Depreciation** — Loss from age, wear, and observed deterioration.
- **Functional Obsolescence** — Loss from internal design deficiencies, excess/inadequate capacity, or operational shortcomings (curable or incurable).
- **External Obsolescence** — Loss from factors outside the asset: market, regulatory, economic.
- **Indirect Costs** — General overhead (12%–18%) plus contractor profit (10%–15%) layered on direct materials and labor.
- **Reconciliation** — Weighting the cost approach against market (and income) approaches to reach a final value conclusion.

---

## Summary

The cost approach is essential for specialized infrastructure where market comparables are thin. Build RCN from materials + labor + indirect costs, deduct physical / functional / external depreciation, and reconcile with market evidence when available.

**Reference files in this skill folder**:

- **[rcn-cost-tables.md](./rcn-cost-tables.md)** — Component-level RCN ranges, labor markups, overhead/profit percentages, and asset-specific economic lives.
- **[depreciation-examples.md](./depreciation-examples.md)** — Worked physical / functional / external depreciation examples, condition rating tables, and two full DRC + market reconciliation examples.
- **[infrastructure-types.md](./infrastructure-types.md)** — Transmission tower, telecom site, and substation deep dives with typical RCN buildup and depreciation profiles.
