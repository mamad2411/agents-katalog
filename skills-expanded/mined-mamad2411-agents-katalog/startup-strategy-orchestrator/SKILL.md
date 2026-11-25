---
name: startup-strategy-orchestrator
description: "Orchestrates the startup strategic and investment planning pipeline: from market sizing and opportunity assessment to headcount planning, financial modeling, and business case synthesis. Keywords: startup-strategy, market-sizing, financial-modeling, business-case, startup-metrics, headcount-planning."
version: 1
created: "2024-05-22"
updated: "2024-05-22"
---

# Startup Strategy Orchestrator - From Idea to Investment

This skill manages the comprehensive planning process for early-stage startups. It guides founders through the critical steps of validating a market, modeling the finances, and building a compelling business case for investors.

## When to Use
Use this skill when:
- Planning a new startup or product.
- Preparing for a seed or Series A fundraising round.
- Defining a 3-5 year roadmap and financial projection.
- Determining headcount needs and unit economics.

## The Orchestrated Workflow
This skill executes the following phases in sequence:

### Phase 1: Market Opportunity Analysis
1. **Market Sizing**: Invoke `startup-analyst` to calculate TAM, SAM, and SOM.
2. **Opportunity Assessment**: Invoke `startup-business-analyst-market-opportunity` to analyze the competitive landscape and identify differentiation.

### Phase 2: Financial Modeling
3. **Financial Projections**: Invoke `startup-financial-modeling` to build 3-5 year revenue, cost, and cash flow models.
4. **Metrics Framework**: Invoke `startup-metrics-framework` to define key performance indicators (CAC, LTV, Burn Rate).

### Phase 3: Operations & Synthesis
5. **Headcount Planning**: Invoke `team-composition-analysis` to determine hiring needs and org chart.
6. **Business Case Synthesis**: Invoke `startup-business-analyst-business-case` to compile all findings into an investor-ready business case document.

## Freedom Calibration & Constraints
- **Constraint Level: Medium**
  - **Rigidity**: The sequence of Market $\rightarrow$ Finance $\rightarrow$ Operations $\rightarrow$ Synthesis is mandatory.
  - **Freedom**: The specific assumptions for growth rates, conversion, and unit economics are left to the user's input.

## Critical Anti-Patterns (NEVER List)
| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** ignore burn rate | Failing to model runway leads to premature failure. | Always include a detailed cash flow and burn rate analysis. |
| **NEVER** use "Blue Ocean" without data | Claiming a monopoly without market sizing is a red flag for investors. | Use `startup-analyst` to back up every claim with TAM/SAM/SOM. |
| **NEVER** skip team planning | A great business plan fails without a plan for the people to execute it. | Always include `team-composition-analysis` in the final synthesis. |

## Verification
1. A TAM/SAM/SOM calculation is completed.
2. A 3-5 year financial model with revenue and costs is produced.
3. A headcount plan and org chart are defined.
4. A comprehensive investor-ready business case is synthesized.
