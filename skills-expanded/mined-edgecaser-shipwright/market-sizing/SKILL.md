---
name: market-sizing
description: "Walks through both top-down and bottom-up market sizing methodologies with explicit assumption tracking. Produces investor-ready estimates with transparent reasoning."
category: discovery
default_depth: standard
---

# Market Sizing (TAM / SAM / SOM)

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Walks through both top-down and bottom-up market sizing methodologies with explicit assumption tracking. Produces investor-ready estimates with transparent reasoning.

## When to Use

- Evaluating a new market opportunity
- Preparing investor decks or business cases
- Prioritizing between multiple market segments
- Sanity-checking revenue projections

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick sanity check on whether a market is worth exploring | Top-Down Sizing only, single-source TAM/SAM/SOM |
| **Standard** | Business case or investor deck preparation | All sections |
| **Deep** | Board-level investment decision or new market entry | All sections + scenario modeling (bull/base/bear), sensitivity analysis on top 3 assumptions, comparable company benchmarks |

**Omit rules:** At Light depth, skip Bottom-Up Sizing, Triangulation, and the full Assumption Register. Retain citations, calculation steps and inline assumptions for each TAM/SAM/SOM estimate.

## Key Definitions

- **TAM (Total Addressable Market):** The total revenue opportunity if you captured 100% of the market
- **SAM (Serviceable Addressable Market):** The portion of TAM your product can realistically reach given current product scope, geography, and go-to-market
- **SOM (Serviceable Obtainable Market):** The realistic share of SAM you can capture in a defined timeframe given competition, resources, and brand awareness

## Framework

### Method 1: Top-Down Sizing

Start from a known market size and narrow down.

```markdown
## Top-Down Estimate

### TAM
Source: [Industry report / analyst estimate]
Total market value: $[X]B
Basis: [What's included, e.g., "global project management software spending"]
Year: [year of estimate]

### SAM
Narrowing factors:
- Geography: [e.g., North America only → 40% of TAM]
- Segment: [e.g., SMB only → 25% of remaining]
- Product scope: [e.g., only collaboration features → 60% of remaining]
SAM = TAM × [factor1] × [factor2] × [factor3] = $[Y]B

### SOM
Capture assumptions:
- Year 1 market share target: [X]%
- Basis: [comparable company benchmarks or bottoms-up capacity]
SOM = SAM × [capture rate] = $[Z]M
```

### Method 2: Bottom-Up Sizing

Build from unit economics upward.

```markdown
## Bottom-Up Estimate

### Unit Economics
- Target customer: [persona / company profile]
- Average annual contract value (ACV): $[X]
- Basis for ACV: [pricing model × expected usage]

### Addressable Customer Count
- Total companies in target segment: [N]
- Source: [Census data / LinkedIn / industry report]
- Filter 1: [e.g., 10-500 employees → N1]
- Filter 2: [e.g., uses [category] tools → N2]
- Filter 3: [e.g., in target verticals → N3]
- Addressable customers: [N3]

### Market Size
- TAM = [Total potential customers] × ACV = $[X]
- SAM = [Reachable customers] × ACV = $[Y]
- SOM = [Capturable in timeframe] × ACV = $[Z]
```

### Step 3: Triangulate & Validate

Always produce both top-down and bottom-up estimates and compare:

```markdown
## Triangulation
| Method | TAM | SAM | SOM |
|---|---|---|---|
| Top-Down | $[X]B | $[Y]B | $[Z]M |
| Bottom-Up | $[X]B | $[Y]B | $[Z]M |
| Delta | [%] | [%] | [%] |

## Reconciliation
[Explain why the estimates differ and which you trust more for each tier]
```

### Step 4: Assumption Register

Every market sizing exercise must include an explicit assumption log:

```markdown
## Assumption Register
| # | Assumption | Value Used | Sensitivity | Source |
|---|---|---|---|---|
| A1 | ACV | $[X] | HIGH, ±20% changes SOM by $[Y]M | [source] |
| A2 | Segment penetration | [X]% | MEDIUM | [source] |
| A3 | Market growth rate | [X]% CAGR | LOW | [analyst report] |
```

**Sensitivity:** HIGH = changes the conclusion, MEDIUM = shifts magnitude, LOW = minor impact.

## Minimum Evidence Bar

**Required inputs:** Target market definition (industry, geography, or customer segment) and at least one of: pricing model, comparable company data, or industry report reference.

**Acceptable evidence:** Analyst reports (Gartner, IDC, CB Insights), government/census data, public company filings, industry association statistics, comparable company revenue disclosures, or primary research with documented sample sizes.

**Insufficient evidence:** If no credible source exists for the TAM base figure, state "Insufficient evidence for TAM estimate" and stop and recommend sourcing an industry report (Gartner, IDC, CB Insights) or running a bottom-up count from public data (e.g., LinkedIn, Census Bureau) before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** TAM base figures and customer counts must cite a specific source with publication year.
- **Hypotheses:** Narrowing factors (segment penetration, capture rate) and ACV assumptions may be estimated, label each as "assumed" with sensitivity rating in the Assumption Register.

## Output Format

Produce a market sizing document with:
1. **Executive Summary**, TAM/SAM/SOM headline numbers with confidence ranges
2. **Top-Down Analysis**, with sources and narrowing factors
3. **Bottom-Up Analysis**, with unit economics and customer counts
4. **Triangulation**, comparison and reconciliation
5. **Assumption Register**, all assumptions with sensitivity ratings
6. **Visualization**, nested TAM > SAM > SOM summary

**Shipwright Signature (required closing):**
7. **Decision Frame**, Whether the market justifies investment given SOM range, trade-off between market size confidence vs. speed to decision, confidence in estimates with evidence quality, owner, decision date, revisit trigger
8. **Unknowns & Evidence Gaps**, Assumptions with HIGH sensitivity that lack primary sources, segments with no bottom-up validation
9. **Pass/Fail Readiness**, PASS if both top-down and bottom-up estimates are present with cited sources and deltas are reconciled (at Light depth: PASS if top-down TAM/SAM/SOM is present with at least one cited source; bottom-up and triangulation not required); FAIL if only one method used or TAM source is undocumented (at Light depth: FAIL if TAM source is undocumented)
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Conflating TAM with opportunity**, TAM is theoretical; SOM is what matters for planning
- **Cherry-picking favorable estimates**, Show both methods and reconcile honestly
- **Hidden assumptions**, Every number should have a source or a labeled assumption
- **Ignoring growth rates**, Static sizing misses trajectory; include CAGR estimates
- **Precision theater**, A range ($800M-$1.2B) is more honest than a false-precision point estimate ($943M)

## Weak vs. Strong Output

**Weak:**
> "TAM is $50B based on the global SaaS market."

Unsourced, uses an overbroad category, no narrowing logic, makes any SOM look artificially large.

**Strong:**
> "TAM is $8.2B (Gartner 2025, global spend on employee onboarding software). SAM = $2.5B after filtering to North America (40%) and mid-market 100-1000 employees (76% of segment). Source: LinkedIn company count cross-referenced with BLS data."

Cited, narrowed with explicit factors, uses two independent sources for triangulation.
