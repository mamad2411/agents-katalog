---
title: Commercial Cost Estimation
description: Quantity take-off, unit rate application, and BOQ cost calculation for construction project cost estimation
version: 1.0
frequency_percent: 50.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-cost-estimation
gigabrain_tags: disciplines, 00250-commercial, commercial-cost-estimation, cost-estimation
openstinger_context: cost-estimation, budget-planning
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
related_skills:
  - commercial-pricing-analysis
  - commercial-milestone-billing
---

# Commercial Cost Estimation

## Overview

Perform comprehensive quantity take-off, unit rate application, and BOQ cost calculation to produce accurate project cost estimates for construction and infrastructure projects.

**Announce at start:** "I'm using the commercial-cost-estimation skill to develop project cost estimates."

## When to Use This Skill

**Trigger Conditions:**
- Preparing tender or bid pricing
- Developing project budgets or cost plans
- Estimating costs for variation orders
- Preparing cost forecasts during project execution
- Creating BOQ from design drawings and specifications

**Prerequisites:**
- Design drawings available (preferably issued for construction or at minimum IFT stage)
- Material take-offs (MTOs) or specification documents
- Unit rates available (from historical data or market rates)
- Understanding of construction methodology and sequence

## Step-by-Step Procedure

### Step 1: Measure Quantities from Drawings/MTOs

1. Review all relevant construction drawings and specifications
2. Perform quantity take-off using standard measurement methods (e.g., POMI, CESMM, NRM)
3. Record measurements by work category and item description
4. Cross-check quantities against MTO reports from engineering
5. Verify measurements with dimensional checks and spot calculations
6. Document all assumptions and measurement methods used

### Step 2: Apply Unit Rates

1. Match each measured item to appropriate unit rate from rate database
2. Apply rates consistently across similar items
3. Adjust rates for project-specific conditions (site access, complexity, scale)
4. Apply location factors if rates are from different geographic areas
5. Document rate source and date for each line item

### Step 3: Calculate Line Item Costs

1. Multiply measured quantities by applicable unit rates
2. Calculate sub-totals by work category or BOQ section
3. Include all direct costs (materials, labor, plant, subcontracts)
4. Calculate proportional direct costs for overhead items
5. Summarize total estimated cost for the scope

### Step 4: Apply Contingencies and Escalation

1. Identify risks and uncertainties in quantities, rates, or scope
2. Apply contingency allowance based on risk level and design maturity:
   - Design contingency: 5-15% depending on design stage
   - Construction contingency: 3-10% based on site conditions
3. Apply escalation for projects spanning multiple years
4. Document basis for all contingency and escalation percentages

### Step 5: Validate Against Budget

1. Compare total estimated cost against approved budget or cost plan
2. Calculate variance percentage and identify areas of over/under-budget
3. If estimate exceeds budget, identify cost reduction opportunities
4. If estimate is significantly under budget, verify completeness of scope
5. Prepare variance analysis report with explanations and recommendations
6. Obtain review and sign-off from project commercial manager

## Success Criteria

- [ ] All quantities measured from drawings/MTOs with documented methods
- [ ] Unit rates applied consistently from approved rate database
- [ ] All direct costs calculated with sub-totals by category
- [ ] Contingencies and escalation applied with clear justification
- [ ] Estimate validated against budget with variance analysis
- [ ] Cost estimate reviewed and approved by commercial manager

## Common Pitfalls

1. **Double-Counting Quantities** — Ensure each physical component is measured once and only once. Cross-reference MTOs with drawings to avoid duplication through overlapping work categories.
2. **Wrong Unit Rates** — Always verify rates match the correct specification, quality grade, and delivery conditions. Using a rate for the wrong material grade or thickness causes significant cost errors.
3. **Missing Scope Items** — Check against the complete scope of work and specifications. Items buried in general conditions, temporary works, or mobilization are commonly missed.
4. **Ignoring Buildability Issues** — Theoretical quantities don't always match construction reality. Apply waste factors, overlap allowances, and construction tolerances where appropriate.

## Cross-References

### Related Skills
- `commercial-pricing-analysis` — Historical rate analysis and benchmarking
- `commercial-milestone-billing` — Progress measurement and billing against estimates

### Related Agents
- `COM-006` Commercial Cost Controller Agent — Primary agent
- `COM-002` Commercial Quantity Surveyor Agent — Supporting agent
