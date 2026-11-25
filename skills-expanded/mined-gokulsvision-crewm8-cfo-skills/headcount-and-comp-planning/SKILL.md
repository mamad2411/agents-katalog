---
name: headcount-and-comp-planning
description: Guide headcount planning and compensation strategy — hiring prioritization, compensation benchmarking, burn impact modeling, equity grant frameworks, and hiring ROI analysis for strategic talent investment.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, headcount, compensation, hiring, equity, salary-benchmarking, talent]
related_skills: [budget-creation-management, cash-forecasting, business-case-modeling, profitability-analysis, scenario-planning]
inputs_required: [current-headcount-by-department-level-location, hiring-plan-roles-priority-start-dates, revenue-forecast-and-runway, option-pool-status-and-cap-table, compensation-benchmarks-market-data]
deliverables: [headcount-plan-monthly-by-department-12-24-months, compensation-framework-salary-and-equity-bands, people-cost-model-integrated-with-budget, hiring-capacity-assessment, option-pool-analysis, arr-per-employee-trajectory]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Headcount & Compensation Planning

Guide the company's most important investment decision: who to hire and how to pay them. Model headcount growth, benchmark compensation, design equity frameworks, and ensure hiring plans are affordable and aligned with strategy. Goal: the company has the right people at the right cost at the right time.

## Purpose

Headcount is the single largest cost for almost every startup — typically 65-80% of total OpEx — and the most important driver of growth. Hiring the right people at the right time (and not hiring the wrong ones) determines whether the company achieves its goals or burns through its runway. This skill provides the frameworks to plan headcount growth strategically, benchmark compensation competitively, design equity packages that attract talent without excessive dilution, and ensure every hire is a capital allocation decision with a clear ROI.

## When to Use

- "Plan our headcount for next year"
- "How many people should we hire?"
- "Benchmark our compensation against the market"
- "Design our equity grant framework"
- "What's the ROI of hiring this team?"
- "Can we afford this hiring plan?"
- "Model the financial impact of our headcount growth"

## Inputs Required

1. **Current headcount** — by department, level, location, salary, equity.
2. **Hiring plan** — roles to fill, priority order, target start dates.
3. **Revenue and runway** — from `revenue-forecasting` and cash forecasting.
4. **Option pool status** — from cap table management.
5. **Compensation benchmarks** — market data, recruiter feedback, offer accept/decline data.

## Quick Reference

| Benchmark | Seed | Series A | Series B+ |
|-----------|------|----------|-----------|
| ARR / Employee | $50-100k | $100-200k | $200-400k |
| People cost as % of OpEx | 60-70% | 65-75% | 70-80% |
| Monthly hiring capacity | 1-2 hires | 2-4 hires | 4-8+ hires |
| Annual voluntary attrition | 10-20% | 10-20% | 10-20% |

| Role Level | Engineering Salary (SF/NYC, Series A) | Equity Grant |
|------------|--------------------------------------|--------------|
| Entry / Junior | $100-130k | 0.1-0.3% |
| Mid-Level | $140-180k | 0.2-0.5% |
| Senior | $180-220k | 0.3-1.0% |
| Staff / Lead | $210-260k | 0.5-1.5% |
| Director | $240-300k | 0.75-2.0% |
| VP / Head of | $280-350k | 1.0-3.0% |

| Total Cost of Employee | Rule of Thumb |
|------------------------|---------------|
| Fully loaded cost | 1.25-1.35× base salary |
| Benefits (health, dental, vision, life, disability) | ~10-15% of salary |
| Payroll taxes (FICA, FUTA, SUTA) | ~8-10% of salary |
| Equipment (one-time) | ~$3-5k |
| Tools/software per seat | ~$200-500/mo |

## Procedure

### 1. Audit Current State

- Headcount by department, level, location, tenure.
- Compensation by role (salary + equity).
- Option pool: grants outstanding, available, burn rate.
- ARR per employee (trailing and forward-looking).

### 2. Build the Hiring Plan

For each role to fill:
- Priority (P0: business-critical, P1: important, P2: nice-to-have).
- Target start date.
- Salary band and equity band.
- Hiring source (inbound, outbound, referral, agency).
- Expected time-to-fill (typically 30-60 days for individual contributors, 60-90 days for leaders).

### 3. Model the Financial Impact

Add hiring costs to the monthly budget:

| Month | Starting HC | New Hires | Departures | Ending HC | Salary Cost | Total People Cost | Cumulative Incremental Burn |
|---|---|---|---|---|---|---|---|
| Jan | 42 | +3 | −1 | 44 | $520k | $676k | — |
| Feb | 44 | +2 | 0 | 46 | $545k | $708k | +$32k |
| ... | | | | | | | |
| Dec | ... | ... | ... | 65 | $790k | $1,027k | +$351k/mo vs Jan |

### 4. Stress Test

- What if hiring takes 2x as long? (happens to almost everyone)
- What if compensation is 15% higher than planned? (competitive market)
- What if attrition is 20% instead of 10%?
- Can we still hit our revenue targets with fewer people?

### Compensation Framework

#### Salary Benchmarks (2026, US-Based Startups)

Ranges vary by stage and funding. For well-funded Series A (SF/NYC):

| Role Level | Engineering | Product / Design | Sales (Base) | Sales (OTE) | Marketing | G&A / Finance |
|---|---|---|---|---|---|---|
| Entry / Junior | $100-130k | $90-120k | $70-90k | $100-130k | $80-110k | $70-90k |
| Mid-Level | $140-180k | $130-170k | $90-120k | $160-220k | $120-160k | $110-140k |
| Senior | $180-220k | $170-210k | $120-150k | $240-300k | $160-200k | $140-180k |
| Staff / Lead | $210-260k | $200-250k | — | — | $190-230k | $170-210k |
| Director | $240-300k | $230-280k | $140-180k | $280-360k | $210-260k | $190-240k |
| VP / Head of | $280-350k | $260-320k | $160-200k | $320-400k | $240-300k | $220-280k |
| C-Level | $300-400k | $280-360k | — | — | — | $280-380k |

Adjust by:
- **Funding stage**: Seed: −15-25%. Series B+: +10-20%.
- **Location**: Tier 2 cities: −10-20%. Non-US developed markets: −20-40%. Emerging markets: −40-60%.
- **Remote**: most companies pay national rate (some geo-adjust, some don't — know your policy).

#### Equity Grant Framework

The standard 4-year vest with a 1-year cliff:

| Role Level | Engineering | Non-Engineering |
|---|---|---|
| Entry / Junior | 0.1-0.3% | 0.05-0.15% |
| Mid-Level | 0.2-0.5% | 0.1-0.3% |
| Senior | 0.3-1.0% | 0.2-0.5% |
| Staff / Lead | 0.5-1.5% | 0.3-0.75% |
| Director | 0.75-2.0% | 0.5-1.0% |
| VP / Head of | 1.0-3.0% | 0.75-2.0% |
| C-Level (non-founder) | 2.0-8.0% | — |
| First 5 engineers (seed) | 1.0-3.0% | — |
| First 10 employees | 0.5-1.5% | 0.3-1.0% |
| Advisor (standard) | 0.1-0.5% | — |

**Refresh grants**: typically at the 2-3 year mark, 50-100% of initial grant. Promotions also trigger refreshes.

**Option pool burn rate**: annually, the company consumes 2-4% of fully diluted shares in new grants. Track this.

#### Total Cost of an Employee

```
Total cost = Salary + Benefits + Payroll Taxes + Equipment + Tools + Office Space

Rule of thumb: total cost ≈ 1.25-1.35× base salary
  - Benefits (health, dental, vision, life, disability): ~10-15% of salary
  - Payroll taxes (employer FICA, FUTA, SUTA): ~8-10% of salary
  - Equipment (laptop, monitor, desk, chair): ~$3-5k one-time
  - Tools/software per seat: ~$200-500/mo
  - Office space (if applicable): ~$500-1,500/mo per person
```

### Headcount Planning Model

#### The Envelope Calculation

```
Step 1: Target end-of-year headcount based on:
  - Revenue headcount ratio: ARR / employee count
    - Seed target: $50-100k ARR/employee
    - Series A target: $100-200k ARR/employee
    - Series B target: $200-400k ARR/employee

Step 2: Calculate total people cost:
  Total people cost = Average fully loaded cost × Target headcount

Step 3: Check against budget and runway:
  - People cost should be 60-80% of total OpEx
  - Runway after hiring plan must remain > 12 months

Step 4: If the plan doesn't fit:
  - Scale back headcount growth
  - Find efficiency (higher ARR/employee)
  - Raise more money
```

#### Hiring Ramp Model

A realistic hiring model (how many can you actually hire per month?):

| Stage | Monthly Hiring Capacity | Why? |
|---|---|---|
| < 20 employees | 1-2/month | Founders doing recruiting, no dedicated recruiter |
| 20-50 employees | 2-4/month | 1 internal recruiter, some process |
| 50-100 employees | 4-8/month | Recruiting team, structured process |
| 100+ employees | 8-15/month | Full recruiting org |

Also model **attrition**: startups typically see 10-20% annual voluntary turnover.

#### Department Headcount Allocation

Typical SaaS startup distribution:

| Department | Pre-PMF | Series A | Series B+ |
|---|---|---|---|
| Engineering / R&D | 50-70% | 35-50% | 30-40% |
| Product / Design | 10-15% | 10-15% | 10-15% |
| Sales | 5-10% | 15-25% | 25-35% |
| Marketing | 3-5% | 5-10% | 8-12% |
| Customer Success / Support | 3-10% | 5-10% | 8-12% |
| G&A / Finance / Ops / HR | 5-10% | 5-10% | 5-10% |

## Output Format

- Headcount plan (monthly, by department, 12-24 months)
- Compensation framework (salary bands + equity bands by level)
- People cost model integrated with the budget
- Hiring capacity assessment (realistic vs aspirational)
- Option pool analysis: months until depletion at current burn rate
- ARR per employee trajectory

## Done Criteria

The skill is complete when:
1. Current headcount is audited and compared against revenue benchmarks (ARR/employee).
2. Hiring plan is built with priorities, target start dates, and realistic hiring capacity.
3. Financial impact is modeled (monthly people cost, cumulative burn, runway impact).
4. Compensation framework (salary bands + equity bands) is defined by role level.
5. Hiring plan is stress-tested against slower hiring, higher comp, and higher attrition scenarios.
6. Runway after hiring plan is confirmed > 12 months.

## Pitfalls

1. **Hiring faster than the company can absorb** — a startup that doubles headcount in 6 months often sees productivity drop as culture dilutes, management spans widen, and processes break. Hire at a pace the organization can integrate.
2. **Overpaying for talent without benchmarking** — paying above-market for the first 5-10 hires creates a compensation anchor that makes every future hire more expensive. Use benchmarks; don't just match whatever the candidate asks for.
3. **Underestimating the fully-loaded cost of hiring** — salary is just the beginning. Benefits (10-15%), payroll taxes (8-10%), equipment ($3-5k one-time), tools ($200-500/mo per seat), and management overhead mean the total cost is 1.25-1.35× salary. A $150k hire actually costs $190-200k.
4. **Planning headcount growth without realistic hiring capacity** — budgeting for 8 hires per month when the company has no recruiter and can only close 2-3 per month creates a phantom budget (underspend that looks like a win but actually means the plan is wrong).
5. **Not modeling attrition** — if you plan to grow from 40 to 60 (net +20) but don't account for 10% annual attrition (4 departures/year, about 1 per quarter), you actually need to hire 24, not 20. Net headcount plans without gross hiring numbers are incomplete.

### Heuristics

- **Hiring is the #1 startup cost**: ~70% of OpEx. Treat every hire as a capital allocation decision.
- **Every hire must pay for themselves**: a sales rep should generate > 3x their OTE in ARR. An engineer should build something worth > 3x their cost.
- **Hiring always takes longer than planned**: the most common budget miss is "we planned to hire 5 people this quarter and hired 2." Build it into the model.
- **Comp is emotional, not rational**: a candidate's comp expectations are anchored to their last job, not your framework. Be flexible within bands.
- **Equity is the startup's superpower**: use it. Cash comp can't compete with FAANG. Equity can.

### Edge Cases

- **Remote / distributed teams**: location-based pay bands, async culture costs (offsites, home office stipends), multi-state compliance.
- **International hiring**: EOR (Employer of Record) costs ~$500-1,000/mo per employee vs setting up a local entity. For < 5 people in a country, EOR is cheaper.
- **Contractor conversions**: converting a long-term contractor to FTE. Factor in benefits, equity, and severance costs. Typically 20-40% more than their contractor cost.
- **Reduction in force (layoffs)**: severance (typically 2-4 weeks per year of service + COBRA), acceleration decisions, communications planning, legal review.

## Verification

Can you answer "How many people do we need to hire this year, and can we afford it?" and "What's our ARR per employee today vs where we need to be?" and "If hiring takes twice as long, what's the impact on revenue and runway?" If not, the headcount plan isn't robust enough.

## Example

> **User**: "Build our headcount plan for next year — we're at 42 people, want to get to 65, with $4.1M ARR."
> **Expected behavior**: You audit current headcount (42 people, $4.1M ARR = $98k ARR/employee — below Series A benchmark of $100-200k), build a hiring plan (20 net new hires, accounting for 10% attrition = need to hire 25 gross), model monthly cost impact ($676k people cost in Jan growing to $1,027k by Dec, +$351k/mo incremental burn), check runway (20 months remaining, plan keeps it above 14 months), define salary bands for each new role, recommend equity grants, and stress-test (if hiring is 30% slower, impact is lower costs but also lower revenue growth — accept the tradeoff).

> **User**: "We're about to make offers to 3 senior engineers. How should we structure equity?"
> **Expected behavior**: You review the option pool status (15% of fully diluted remaining, 2.5% burn rate), benchmark equity for senior engineers at Series A stage (0.3-1.0%), recommend 0.5% per engineer with 4-year vest and 1-year cliff, calculate total pool consumption (1.5% for 3 hires = 60% of annual burn rate in one month — recommend requesting board approval to increase the pool), and advise on refresh grant timing (50% of initial at year 3 if performance meets expectations).

## Linked Skills

- Budget integration → `budget-creation-management`
- Cash flow impact → `cash-forecasting`
- ROI case for a team hire → `business-case-modeling`
- Profitability per employee → `profitability-analysis`
- Headcount in scenario models → `scenario-planning`
