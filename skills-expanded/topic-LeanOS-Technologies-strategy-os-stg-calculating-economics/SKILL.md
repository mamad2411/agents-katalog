---
name: stg-calculating-economics
description: Calculates unit economics (LTV, CAC, payback, margins) with range-based estimates, cost structure, and scenario analysis. Use when constructing unit economics hypothesis during BUILD phase 2.
serves: strategist
domain: unit-economics
affects: unit-economics-hypothesis
depends-on: stg-designing-channels (channel mix, per-channel CAC, investment split)
produces: unit economics hypothesis in register format
---

# Economics Calculation

Calculate unit economics with range-based estimates, integrated cost structure, and scenario analysis. Every input carries tier label; output inherits highest (weakest) tier. Merged from old str-calculating-economics and str-structuring-costs.

## Procedure

### Step 1: Gather Inputs with Tier Labels [S]

Read: pricing inputs (from stg-designing-pricing), market sizing (from stg-sizing-markets), competitive data (from stg-analyzing-competition), solution design (growth architecture).

Assemble input table:

| Input | Source | Tier | Value |
|-------|--------|------|-------|
| ARPU | Pricing tiers | T2 (hypothesis) | {range} |
| Gross margin | Category benchmark, adjusted for COGS | T2 | {range} |
| Churn rate | Benchmark for category + ACV range | T2 (no customer data) | {range} |
| S&M spend | Channel strategy (stg-designing-channels) or cost structure estimate | T2 | {range} |
| Growth model | Solution design | T1 (a choice, not a prediction) | {model} |

Produce: input table with tier labels and source citations.

If channel strategy outputs are available (from stg-designing-channels), use per-channel CAC estimates and investment splits as the primary source for S&M spend and blended CAC inputs. This provides more rigorous CAC decomposition than freestanding S&M estimation.

**Gate:** `inputs_gathered: bool` -- all 5 inputs have values, tier labels, and sources.
- Pass: Step 2.
- Fail: For missing inputs, use category benchmarks with T2 label. If no benchmarks available, use SaaS median with T3 label and wide range.

### Step 2: Calculate Core Metrics as Ranges [S]

Calculate for optimistic, base, and pessimistic input sets:

**LTV** = ARPU x Gross Margin x (1 / Monthly Churn Rate)

**CAC** = (S&M Spend + Allocated Overhead) / New Customers Acquired

**LTV:CAC** = LTV / CAC

**Payback** = CAC / (ARPU x Gross Margin)

Output tier = max(input tiers). If any input is T3, output is T3. If all inputs are T2, output is T2.

Produce: metric ranges across three scenarios.

**Gate:** `metrics_calculated: bool` -- LTV, CAC, LTV:CAC, and payback calculated for all three scenarios with tier labels.
- Pass: Step 3.
- Fail: If a formula input is missing, use the widest reasonable range and note which input is driving uncertainty.

### Step 3: Calculate Cost Structure [S]

Read: solution design (features to build), growth architecture, constraints.

**Fixed costs:**
- Team: salaries, contractors (from role count x market rate)
- Infrastructure: servers, CI/CD, monitoring
- Software: SaaS tools, licenses
- Operations: legal, accounting, insurance

**Variable costs (COGS):**
- Hosting/compute per user (if AI inference, model per-interaction cost explicitly)
- Payment processing (2.9% + $0.30 typical)
- Support per ticket
- Onboarding per customer

**Derived metrics:**
- Gross margin = (revenue - COGS) / revenue
- Burn rate = fixed costs + variable costs at current scale
- Runway = available capital / monthly burn rate

Produce: cost structure with categories and monthly totals [T2].

**Gate:** `cost_structure_calculated: bool` -- fixed and variable costs categorized, gross margin calculated, burn rate and runway estimated.
- Pass: Step 4.
- Fail: If cost inputs are unknown, use industry benchmarks. AI inference costs are commonly missed -- always check if product has AI components.

### Step 4: Validate Against Benchmarks [R]

Compare metrics against benchmark thresholds:

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| LTV:CAC | >3:1 | 2-3:1 | <2:1 |
| Payback | <12 months | 12-18 months | >18 months |
| Gross margin | >70% | 50-70% | <50% |
| Monthly churn | <5% | 5-10% | >10% |

Flag any metric in warning or critical range with specific values.

Produce: benchmark validation with flags.

**Gate:** `benchmarks_validated: bool` -- all four metrics compared against thresholds.
- Pass: Step 5.
- Fail: Critical-range metrics are findings, not blockers. Report them.

### Step 5: Add Growth-Model-Specific Metrics [R]

Based on growth architecture from solution design:

| Growth Model | Key Metrics | Tier |
|-------------|------------|------|
| PLG | Signup->activation rate, free->paid conversion, PQL rate, expansion revenue % | T2-T3 |
| Network | Viral coefficient, invite rate, network density threshold | T2-T3 |
| Traditional | Sales cycle length, demo->close rate, AE productivity | T2-T3 |

All estimates are T2 (from benchmarks) or T3 (predictions). Label each.

Produce: growth-specific metrics with tier labels.

**Gate:** `growth_metrics_added: bool` -- at least 3 growth-model-specific metrics estimated with tier labels.
- Pass: Step 6.
- Fail: If no benchmarks for the specific growth model, use general SaaS benchmarks and note the reduced confidence.

### Step 6: Build Scenario Analysis [S]

Four scenarios:

- **Optimistic:** Favorable assumptions resolve (CAC at low end, LTV at high end, churn at low end).
- **Base:** Estimates as calculated.
- **Pessimistic:** CAC 3x estimate, segment 40% smaller, churn 2x benchmark.
- **Kill:** At what point do economics not work at all? State specific threshold values (e.g., "If CAC exceeds $X or churn exceeds Y%, LTV:CAC falls below 1:1").

Produce: four scenarios in register format.

**Gate:** `scenarios_built: bool` -- all four scenarios with specific numbers, pessimistic stress-tests assumptions.
- Pass: Step 7.
- Fail: If pessimistic is barely different from base, it is not a real stress test. Apply: 3x CAC, 40% smaller segment, 2x churn. If strategy only works in optimistic scenario, that is a finding.

### Step 7: Mode-Specific Validation [R]

| Mode | Check | Required |
|------|-------|----------|
| VENTURE | LTV:CAC in base scenario | > 3x |
| VENTURE | Payback in base scenario | < 18 months |
| BOOTSTRAP | LTV:CAC in base scenario | > 5x |
| BOOTSTRAP | Payback in base scenario | < 6 months |
| BOOTSTRAP | Path to profitability | Within runway |

If base scenario fails mode thresholds, flag as critical finding.

Produce: mode validation result.

**Gate:** `mode_validated: bool` -- all mode-relevant thresholds checked with pass/fail.
- Pass: Step 8.
- Fail: Threshold failure is a finding, not a blocker. Report which threshold failed, by how much, and what would need to change.

### Step 8: Write Hypothesis [S]

Write complete unit economics hypothesis in register format:

- **Claim:** One paragraph stating revenue model, LTV:CAC range, payback range, gross margin trajectory.
- **Evidence:** All calculations with sources and tier labels.
- **Mode Thresholds:** Table with required vs estimated for each metric.
- **Scenario Analysis:** Optimistic, base, pessimistic, kill -- with specific numbers.
- **Assumptions:** Every input that is T2 or T3 is an assumption (with tier, load-bearing flag, blast radius).
- **Kill Condition:** At what LTV:CAC ratio or payback period does this stop working? State specific numbers.
- **Possibility Space:** What alternative revenue models were considered and why eliminated.

Produce: complete unit economics hypothesis in register format.

**Gate:** `hypothesis_written: bool` -- all fields populated, no point estimates (all ranges), kill condition has specific thresholds.
- Pass: Done.
- Fail: Fix missing fields or convert point estimates to ranges.

## Quality Criteria

- All calculations shown, not just results
- Every input cites source and carries tier label
- Three scenarios presented (optimistic, base, pessimistic) plus kill scenario
- Gross margin accounts for AI inference costs if applicable
- Mode-specific thresholds explicitly checked (pass/fail with numbers)
- No point estimates -- ranges throughout
- Cost structure broken into fixed and variable with category detail

## Failure Modes

| Mode | Signal | Recovery |
|------|--------|----------|
| Premature precision | Specific CAC ($47.32) or LTV ($2,847) stated as if measured | These are pre-launch estimates. Present as ranges: CAC $30-$80. Cite the benchmark or assumption behind each bound |
| Optimistic-only scenario | Only base case presented, or pessimistic case is barely different from base | Pessimistic must stress-test: 3x CAC, 40% smaller segment, 2x churn. If the strategy works only in the optimistic scenario, that is a finding |
| Revenue without cost structure | LTV:CAC calculated but gross margin assumed at 80% without COGS analysis | Calculate actual COGS. AI inference costs can push margins below 60%. If COGS are genuinely low, document why |
| Disappearing uncertainty | T2 pricing estimate becomes T1 input to LTV calculation | Output tier = max(input tiers). If ARPU is T2 and churn is T2, LTV is T2. If any input is T3, LTV is T3 |

## Boundaries

**In scope:** LTV/CAC/payback calculation, cost structure (fixed + variable), gross margin analysis, benchmark validation, growth-model-specific metrics, scenario analysis, mode-specific threshold validation, tier propagation.

**Out of scope:** Pricing design (stg-designing-pricing), market sizing (stg-sizing-markets), competitive analysis (stg-analyzing-competition), solution design (stg-designing-solutions).
