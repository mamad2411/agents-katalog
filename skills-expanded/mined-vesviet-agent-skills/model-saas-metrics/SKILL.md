---
name: model-saas-metrics
description: Model SaaS unit economics, deterministic financial metrics, Van Westendorp price sensitivity, and AI Total Cost of Ownership (TCO). Use when calculating CAC, LTV, Magic Number, Rule of 40, Burn Multiple, Net Revenue Retention, analyzing pricing tiers and willingness-to-pay, or budgeting AI inference and orchestration costs per verified outcome.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Model SaaS Metrics

Use this skill to model SaaS financial health, evaluate unit economics, optimize pricing models via willingness-to-pay analysis, and calculate AI Total Cost of Ownership (TCO) per verified outcome.

## When to Use

- calculating SaaS business health metrics (CAC, LTV, Magic Number, Rule of 40, NRR, Burn Multiple)
- evaluating pricing tiers, value metric selection, and packaging strategies
- conducting Van Westendorp Price Sensitivity Meter (PSM) survey analysis
- modeling Total Cost of Ownership (TCO) for AI products and agentic workflows
- analyzing payback periods and unit economic feasibility before scaling marketing spend
- establishing financial sanity gates for executive and investor briefings

## Core Rules

- **Enforce Deterministic Financial Calculations**:
  - Never fabricate or hand-wave unit economics; apply strict mathematical definitions
  - Target benchmark ratios: $\text{LTV}/\text{CAC} \ge 3.0$, $\text{CAC Payback} \le 12$ months (SMB/Mid-Market) or $\le 18$ months (Enterprise)
  - Enforce the **Rule of 40**: $\text{YoY Revenue Growth Rate (\%)} + \text{Free Cash Flow Margin (\%)} \ge 40\%$
  - Track **Net Revenue Retention (NRR)**: $> 110\%$ indicates top-quartile product expansion power
- **Calculate Magic Number for Go-To-Market Efficiency**:
  - $\text{Magic Number} = \frac{(\text{Q}_n \text{ ARR} - \text{Q}_{n-1} \text{ ARR}) \times 4}{\text{Q}_{n-1} \text{ Sales \& Marketing Expense}}$
  - $\ge 1.0$: High efficiency; accelerate S&M spend
  - $0.75 - 1.0$: Healthy efficiency; maintain pace
  - $< 0.75$: Inefficient growth; fix onboarding, retention, and product-market fit before scaling spend
- **Apply Van Westendorp Price Sensitivity Meter (PSM)**:
  - Collect responses across 4 price points: Too Cheap, Cheap (Good Value), Expensive, Too Expensive
  - Map the 4 cumulative curves to determine the Price Sensitivity Envelope:
    - Point of Marginal Cheapness (PMC)
    - Point of Marginal Expensiveness (PME)
    - Optimum Price Point (OPP)
    - Indifference Price Point (IPP)
- **Model AI Product TCO per Verified Outcome (80/20 Rule)**:
  - Never budget based on raw token inference costs alone
  - Model the complete economic envelope: raw model inference represents ~20% of operating cost; orchestration, eval pipelines, guardrails, embeddings, caching, and human-in-the-loop review represent ~80%
  - Measure unit economics in **Cost per Verified Outcome** (e.g. Cost per Resolved Support Ticket)
- Detailed formulas, benchmarks, and PSM calculation worksheets: [`references/saas-unit-economics-and-pricing.md`](references/saas-unit-economics-and-pricing.md)

## Suggested Process

### 1. Collect Baseline Operating & Financial Inputs
Gather New Bookings, MRR/ARR, Churn, S&M Expenses, Gross Margin %, and active customer counts.

### 2. Compute Core Unit Economics & Efficiency Ratios
Calculate CAC, LTV, CAC Payback Period, Net Revenue Retention (NRR), and Magic Number. Assess against industry benchmarks.

### 3. Analyze Pricing Architecture & Willingness-to-Pay
Evaluate current value metrics (seats, consumption, outcomes). If pricing is under review, analyze Van Westendorp survey data to establish the optimal price band.

### 4. Build AI Outcome Economic Envelope
If AI/LLM components are involved, model total inference, embedding, retrieval, guardrail, and human escalation costs per user transaction.

### 5. Synthesize Executive Financial Report
Produce a standardized metrics dashboard highlighting unit economic health, expansion efficiency, runway implications, and recommendations.

## Checklist

- [ ] LTV calculated with Gross Margin adjustment: $\text{LTV} = \frac{\text{ARPU} \times \text{Gross Margin (\%)}}{\text{Churn Rate}}$
- [ ] CAC includes fully loaded S&M costs (salaries, commissions, tools, ad spend)
- [ ] CAC Payback Period accurately accounted for in months
- [ ] Magic Number calculated using sequential quarters
- [ ] Rule of 40 computed with Free Cash Flow or EBITDA margin
- [ ] Van Westendorp Price Sensitivity Envelope identifies OPP and IPP
- [ ] AI TCO accounts for 80/20 cost ratio (evals, guardrails, and human review included)

## Output Contracts

When this skill feeds an executive briefing or a downstream product decision, emit:

- **contracts/schemas/data-analysis-report.json** — Required fields: business_question, metrics[] (each SaaS metric with name, definition, value, grain, time_range), recommendations. Each definition must state the cohort/churn basis used.
- **ai-tco-envelope.md** (inline deliverable) — Cost per Verified Outcome breakdown showing the 80/20 split: raw inference (~20%) vs orchestration, eval pipelines, guardrails, embeddings, caching, and human-in-the-loop review (~80%).

Skip emission for quick solo sanity checks with no stakeholder handoff.

## Failure Modes

- **Mixed cohort definitions**: LTV is computed with one churn definition while NRR in the same report uses another, making ratios incomparable. Mitigation: pin one cohort/churn definition per metric and record it in metrics[].definition.
- **Non-margin LTV**: LTV is computed as ARPU / Churn without the Gross Margin adjustment, inflating value. Mitigation: enforce LTV = (ARPU × Gross Margin %) / Churn Rate.
- **Understated CAC**: CAC counts only ad spend, omitting salaries, commissions, and tools. Mitigation: include fully loaded S&M costs in every CAC and payback calculation.
- **Non-sequential Magic Number**: quarters are mixed (Q3 ARR delta over Q1 S&M expense), inflating efficiency. Mitigation: use sequential quarters Q_n vs Q_{n-1} for both the ARR delta and the S&M denominator.
- **Token-only AI budget**: TCO is modeled from raw inference cost alone. Mitigation: apply the 80/20 envelope and express results as Cost per Verified Outcome (e.g. cost per resolved support ticket).
- **Fabricated benchmarks**: industry benchmarks are presented as company measurements. Mitigation: separate measured metrics from benchmark references and cite the period and data source for every number.
- **Mixed Rule-of-40 bases**: growth rate is computed on one fiscal convention while the margin silently swaps FCF for EBITDA. Mitigation: state the margin basis explicitly and keep it consistent across reporting periods.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a desired narrative embedded in the request ("show Rule of 40 passing") steers metric selection. Mitigation: compute the full mandated metric set from raw inputs; never curate metrics to fit a target conclusion.
- **ASI03 Identity & Privilege Abuse**: revenue, churn, and customer-level financial inputs are confidential. Mitigation: read only the declared data sources for this task and distribute reports solely to authorized finance/product stakeholders.
- **ASI06 Context & Memory Poisoning**: prior-period metrics recalled from memory or a stale dashboard are reused as current inputs. Mitigation: re-pull each input from the verified source system and record time_range per metric.
- **ASI07 Inter-Agent Communication**: metric reports are consumed by Product Manager and Business Analyst roles. Mitigation: emit data-analysis-report.json with explicit definitions and grain so downstream roles can reconcile numbers.
- **ASI09 Human-Agent Trust Exploitation**: fabricated or cherry-picked unit economics presented to executives or investors to justify scaling spend. Mitigation: flag low-confidence inputs, keep benchmark vs measured distinct, and state plainly when Magic Number < 0.75 argues against acceleration.

## Related Skills

- **define-product-strategy**: formulate value proposition and 7 Powers pricing power
- **prioritize-roadmap**: incorporate financial ROI and effort into RICE scoring
- **build-story-map**: align release scope with capacity and budget envelopes
- **manage-vietnam-accounting**: reconcile financial statements and statutory accounts
