---
name: carbon-footprint
description: >
  Analyze organizational carbon footprint covering Scope 1/2/3 emissions inventory, calculation
  methodology, reduction targets, offset evaluation, and progress tracking.
  TRIGGER when: user says /carbon-footprint, "carbon footprint", "emissions inventory", "GHG inventory", "carbon analysis", "Scope 1 2 3 emissions".
argument-hint: "[reporting-period] [scope] [business-unit-or-facility]"
user-invocable: true
---

# Carbon Footprint Analysis

Quantify greenhouse gas emissions across Scopes 1, 2, and 3, establish reduction targets, evaluate offsetting strategies, and track decarbonization progress.

---

## Input Gathering

| Input                         | Description                                                    | Required |
|-------------------------------|----------------------------------------------------------------|----------|
| Organizational boundary       | Operational control, financial control, or equity share        | Yes      |
| Reporting period              | Calendar or fiscal year                                        | Yes      |
| Facility / site list          | All owned and operated locations                               | Yes      |
| Energy consumption data       | Electricity (kWh), natural gas (therms), fuel (gallons/liters) | Yes      |
| Fleet and travel data         | Vehicle mileage, fuel type, air travel records                 | Yes      |
| Emission factors              | EPA, DEFRA, IEA, or regional grid factors                     | Yes      |
| Supply chain / procurement    | Purchased goods spend, logistics data, waste volumes           | No       |
| Prior year inventory          | Previous GHG inventory for trend analysis                      | No       |

---

## Step-by-Step Process

### Step 1 — Boundary Setting and Scope Definition

Define what is in and out of scope:

| Scope     | Definition                                        | Examples                                      |
|-----------|---------------------------------------------------|-----------------------------------------------|
| Scope 1   | Direct emissions from owned/controlled sources    | Boilers, furnaces, fleet vehicles, refrigerants|
| Scope 2   | Indirect emissions from purchased energy          | Electricity, steam, heating, cooling           |
| Scope 3   | All other indirect emissions in the value chain   | 15 categories per GHG Protocol                 |

**Scope 3 Categories (prioritize by materiality)**:

| Category | Description                         | Typical Materiality           |
|----------|-------------------------------------|-------------------------------|
| 1        | Purchased goods and services        | High (manufacturing, retail)  |
| 2        | Capital goods                       | Medium                        |
| 3        | Fuel/energy-related activities      | Medium                        |
| 4        | Upstream transportation             | High (if significant logistics)|
| 5        | Waste generated in operations       | Low-Medium                    |
| 6        | Business travel                     | Medium (services companies)   |
| 7        | Employee commuting                  | Low-Medium                    |
| 8        | Upstream leased assets              | Varies                        |
| 9        | Downstream transportation           | Medium                        |
| 10       | Processing of sold products         | High (B2B components)         |
| 11       | Use of sold products                | High (energy-using products)  |
| 12       | End-of-life treatment               | Low-Medium                    |
| 13       | Downstream leased assets            | Varies                        |
| 14       | Franchises                          | Varies                        |
| 15       | Investments                         | High (financial sector)       |

Document inclusion/exclusion rationale for each category.

### Step 2 — Activity Data Collection

Gather activity data by emission source:

| Source                    | Data Required                              | Primary Collection Method        |
|---------------------------|--------------------------------------------|----------------------------------|
| Stationary combustion     | Fuel type, volume consumed                 | Utility invoices, meter readings |
| Mobile combustion         | Fuel type, gallons/liters or miles + MPG   | Fleet management system, fuel cards|
| Refrigerants              | Type, quantity charged/leaked              | Maintenance logs, HVAC records   |
| Purchased electricity     | kWh consumed per facility                  | Utility bills                    |
| Steam / heating / cooling | Energy content purchased                   | District energy invoices         |
| Purchased goods           | Spend data or physical quantities          | Procurement system, ERP          |
| Transportation            | Weight-distance (ton-miles/km) or spend    | TMS, freight invoices            |
| Business travel           | Miles by mode (air, rail, car)             | Travel booking system, expenses  |
| Waste                     | Tons by disposal method                    | Waste hauler reports             |

Apply data quality scoring (1-5) to each data source; flag anything below 3 for improvement.

### Step 3 — Emission Calculations

Apply the GHG Protocol calculation approach:

**Scope 1** (direct calculation):
- Emissions = Activity data x Emission factor x GWP
- Example: 10,000 therms natural gas x 5.3 kg CO2e/therm = 53 tCO2e

**Scope 2** (dual reporting):
- Location-based: Grid-average emission factors (e.g., EPA eGRID, IEA)
- Market-based: Supplier-specific factors, RECs, PPAs, residual mix
- Report both; market-based reflects procurement choices

**Scope 3** (tiered methodology):
| Tier     | Method              | Data Requirement   | Accuracy |
|----------|---------------------|--------------------|----------|
| Tier 1   | Spend-based         | $ spend x EEIO EF  | Low      |
| Tier 2   | Average-data        | Mass/units x avg EF| Medium   |
| Tier 3   | Supplier-specific   | Primary data from suppliers | High |

Progress from Tier 1 to Tier 3 over successive reporting years, starting with the highest-materiality categories.

### Step 4 — Reduction Target Setting

Establish targets aligned with climate science:

| Target Type              | Framework              | Requirement                                |
|--------------------------|------------------------|--------------------------------------------|
| Near-term SBT            | SBTi                   | 1.5C-aligned; 42% reduction by 2030 (from 2020) |
| Long-term SBT            | SBTi Net-Zero Standard | 90% reduction by 2050 at latest            |
| Absolute target          | Company-defined        | Total tCO2e reduction by a specific year   |
| Intensity target         | Company-defined        | tCO2e per revenue, per unit, per employee  |

Build an abatement cost curve (MAC curve) ranking reduction initiatives by $/tCO2e avoided:

| Initiative                        | Abatement Potential | Cost per tCO2e | Payback Period |
|-----------------------------------|--------------------:|---------------:|----------------|
| LED lighting retrofit             | X tCO2e             | -$50 (savings) | < 2 years      |
| Renewable electricity procurement | X tCO2e             | $0-20          | Immediate      |
| Fleet electrification             | X tCO2e             | $30-80         | 3-7 years      |
| Process efficiency improvements   | X tCO2e             | $10-50         | 1-5 years      |
| Supplier engagement (Scope 3)     | X tCO2e             | Variable       | 2-5 years      |

### Step 5 — Offset and Inset Evaluation

Evaluate carbon credits for residual emissions only (after maximum abatement):

| Criteria              | Standard                | Assessment Question                          |
|-----------------------|-------------------------|----------------------------------------------|
| Additionality         | Gold Standard, Verra VCS| Would the project happen without credit revenue? |
| Permanence            | All standards           | Is the carbon stored for 100+ years?          |
| Leakage               | All standards           | Does the project shift emissions elsewhere?   |
| Verification          | Third-party auditor     | Has an accredited body verified the claims?   |
| Co-benefits           | SDG alignment           | Does the project deliver social/environmental co-benefits? |
| Vintage               | Recent (< 3 years)      | Are credits from recent project activity?     |

Prefer removal-based credits (direct air capture, biochar, enhanced weathering) over avoidance credits. Budget $15-150/tCO2e depending on credit quality.

### Step 6 — Monitoring, Reporting, and Continuous Improvement

- Establish a quarterly emissions tracking cadence with automated data pipelines where possible.
- Compare actuals to the linear glide path toward the reduction target.
- Recalculate the base year if structural changes occur (M&A, divestiture, methodology change).
- Report externally via CDP, annual ESG report, and regulatory filings.
- Conduct annual third-party verification (limited or reasonable assurance).
- Update the MAC curve annually as technology costs and emission factors change.

---

## Output Format

```
## Carbon Footprint Report — [Organization] — [Period]

### Executive Summary
- Total GHG emissions: [X] tCO2e
- Scope 1: [X] tCO2e | Scope 2 (market): [X] tCO2e | Scope 3: [X] tCO2e
- YoY change: [+/-X%] absolute, [+/-X%] intensity
- Progress toward target: [X% of target achieved, Y% remaining by Z year]

### Emissions Inventory
| Scope / Category        | tCO2e   | % of Total | YoY Change | Data Quality |
|-------------------------|---------|------------|------------|--------------|
| Scope 1 — Stationary    | ...     | ...        | ...        | ...          |
| Scope 1 — Mobile        | ...     | ...        | ...        | ...          |
| Scope 1 — Fugitive      | ...     | ...        | ...        | ...          |
| Scope 2 — Location      | ...     | ...        | ...        | ...          |
| Scope 2 — Market        | ...     | ...        | ...        | ...          |
| Scope 3 — Cat 1         | ...     | ...        | ...        | ...          |
| ...                     | ...     | ...        | ...        | ...          |
| **Total**               | **...** | **100%**   | **...**    |              |

### Reduction Target Progress
- Base year: [year] — [X] tCO2e
- Target: [X% reduction by year]
- Current trajectory: [on track / behind / ahead]
- Gap to target: [X] tCO2e

### Abatement Initiatives
| Initiative              | Status     | Expected Abatement | Cost   | Timeline |
|-------------------------|------------|-------------------|--------|----------|
| ...                     | ...        | ...               | ...    | ...      |

### Methodology Notes
- Consolidation approach: [operational / financial control]
- Emission factors: [source and version]
- Scope 3 methodology tier by category: [table]

### Recommendations
1. [Prioritized next actions]
```

---

## Quality Checklist

- [ ] Organizational boundary clearly defined and consistently applied
- [ ] All material emission sources included (no cherry-picking)
- [ ] Activity data sourced from primary records (not estimates) where possible
- [ ] Emission factors current and from recognized sources (EPA, DEFRA, IEA)
- [ ] Scope 2 reported in both location-based and market-based methods
- [ ] Scope 3 screening completed; material categories quantified
- [ ] Data quality scored and improvement plan for low-quality sources
- [ ] Base year recalculation policy defined and applied
- [ ] Reduction targets aligned with SBTi or equivalent framework
- [ ] Third-party verification planned or completed

---

## Edge Cases

- **Company with operations in countries lacking reliable grid emission factors**: Use IEA country-level factors as default; document data gaps; apply conservative (higher) factors when uncertain.
- **Significant M&A activity during reporting period**: Apply the base year recalculation policy; restate historical emissions to include/exclude the acquired/divested entity.
- **Renewable energy procurement via unbundled RECs**: Market-based Scope 2 can use REC factors, but location-based must still use grid average; document REC vintage and geographic alignment.
- **Scope 3 Category 11 (use of sold products) dwarfs all other emissions**: This is common for fossil fuel, automotive, and electronics companies; report transparently, set absolute and intensity reduction targets, and invest in product redesign.
- **Joint ventures or non-controlling interests**: Apply the consolidation approach consistently; if equity share, include proportional emissions; if operational control, include only if the company operates the JV.
- **Carbon credit vintage and registry double-counting concerns**: Verify credits are retired on the registry, not just purchased; check for corresponding adjustments under Article 6 if applicable.
