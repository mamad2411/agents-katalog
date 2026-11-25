---
name: investment-analysis
description: >
  Evaluate investments or business cases using NPV, IRR, payback period, sensitivity analysis,
  and a structured recommendation framework.
  TRIGGER when: user says /investment-analysis, "evaluate investment", "business case", "NPV analysis", "IRR calculation", "capital allocation", "ROI analysis", "build a business case".
argument-hint: "[investment or project name] [total investment amount] [time horizon]"
user-invocable: true
---

# Investment Analysis

Evaluate proposed investments, capital projects, or strategic business cases using rigorous financial analysis. This skill produces a structured evaluation with quantitative metrics, risk assessment, and a clear recommendation.

---

## Step 1 — Define the Investment Opportunity

Capture the full scope of the proposed investment.

| Parameter              | Description                                          | Example                          |
|------------------------|------------------------------------------------------|----------------------------------|
| Investment Name        | Descriptive title                                     | New AI-Powered Analytics Module  |
| Sponsor                | Who is proposing the investment                       | VP of Product                    |
| Investment Type        | CapEx, OpEx, acquisition, R&D, market entry           | R&D (OpEx)                       |
| Total Investment       | Upfront and ongoing cost commitment                   | $1.2M over 18 months             |
| Time Horizon           | Evaluation period                                     | 5 years                          |
| Strategic Alignment    | Which company objectives this supports                | "Expand platform capabilities"   |
| Alternatives           | Options considered (including "do nothing")           | Build vs. Buy vs. Partner        |
| Decision Deadline      | When a go/no-go decision is needed                    | End of Q2 2026                   |

### Checklist
- [ ] Problem statement or opportunity clearly articulated
- [ ] Alternatives identified (minimum: invest, delay, do nothing)
- [ ] Sponsor has committed to providing input assumptions
- [ ] Finance team has confirmed discount rate / hurdle rate
- [ ] Timeline and resource requirements are scoped

---

## Step 2 — Estimate Costs

Build a comprehensive cost model including all direct and indirect expenses.

### Cost Breakdown Template

| Cost Category            | Year 0 (Upfront) | Year 1    | Year 2    | Year 3    | Year 4    | Year 5    | Total     |
|--------------------------|-------------------|-----------|-----------|-----------|-----------|-----------|-----------|
| Personnel (FTE)          |                   |           |           |           |           |           |           |
| Contractors / Consultants|                   |           |           |           |           |           |           |
| Technology / Infrastructure|                 |           |           |           |           |           |           |
| Software Licenses        |                   |           |           |           |           |           |           |
| Hardware / Equipment     |                   |           |           |           |           |           |           |
| Training & Change Mgmt   |                   |           |           |           |           |           |           |
| Marketing / GTM          |                   |           |           |           |           |           |           |
| Opportunity Cost         |                   |           |           |           |           |           |           |
| Contingency (10–15%)     |                   |           |           |           |           |           |           |
| **Total Costs**          |                   |           |           |           |           |           |           |

### Cost Estimation Guidelines
- Include fully-loaded costs (salary + benefits + overhead) for personnel.
- Capture opportunity costs: what else could this capital fund?
- Add contingency buffer of 10–15% for estimation uncertainty.
- Distinguish between sunk costs (already spent, do not include in forward analysis) and incremental costs.

---

## Step 3 — Estimate Benefits

Quantify the financial returns the investment will generate.

### Benefits Classification

| Benefit Type        | Description                                    | Quantification Method            |
|---------------------|------------------------------------------------|----------------------------------|
| Revenue — Direct    | New revenue stream directly from investment    | Bottom-up demand model           |
| Revenue — Indirect  | Revenue uplift from improved capabilities      | Attach rate x base revenue       |
| Cost Avoidance      | Costs that would be incurred without investment| Current spend trajectory avoided |
| Cost Reduction      | Actual reduction in existing spend             | Current cost - future cost       |
| Efficiency Gain     | Time saved, converted to dollar value          | Hours saved x fully-loaded rate  |
| Risk Mitigation     | Avoided losses or penalties                    | Probability x impact             |
| Strategic Value     | Market positioning, competitive advantage      | Qualitative + proxy metrics      |

### Benefits Schedule Template

| Benefit                    | Year 1    | Year 2    | Year 3    | Year 4    | Year 5    | Total     | Confidence |
|----------------------------|-----------|-----------|-----------|-----------|-----------|-----------|------------|
| New product revenue        |           |           |           |           |           |           | Medium     |
| Customer retention uplift  |           |           |           |           |           |           | High       |
| Operational cost savings   |           |           |           |           |           |           | High       |
| Compliance risk avoidance  |           |           |           |           |           |           | Low        |
| **Total Benefits**         |           |           |           |           |           |           |            |

---

## Step 4 — Financial Metrics Calculation

Compute the standard investment evaluation metrics.

### Net Present Value (NPV)

NPV = Sum of [ (Benefits_t - Costs_t) / (1 + r)^t ] for t = 0 to T

| Year | Net Cash Flow | Discount Factor (at r%) | Present Value |
|------|---------------|-------------------------|---------------|
| 0    |               | 1.000                   |               |
| 1    |               |                         |               |
| 2    |               |                         |               |
| 3    |               |                         |               |
| 4    |               |                         |               |
| 5    |               |                         |               |
| **NPV** |           |                         |               |

- **Discount Rate**: Use the company's weighted average cost of capital (WACC) or hurdle rate. Typical range: 8–15%.
- **Decision Rule**: Invest if NPV > 0.

### Internal Rate of Return (IRR)

- IRR is the discount rate that makes NPV = 0.
- **Decision Rule**: Invest if IRR > hurdle rate.
- **Caution**: IRR can be misleading for non-conventional cash flows (multiple sign changes). In those cases, use Modified IRR (MIRR).

### Payback Period

| Month/Quarter | Cumulative Net Cash Flow | Payback Reached? |
|---------------|--------------------------|------------------|
| Q1            |                          | No               |
| Q2            |                          | No               |
| ...           |                          |                  |
| QN            |                          | Yes              |

- **Simple Payback**: Time to recover initial investment (undiscounted).
- **Discounted Payback**: Time to recover initial investment using discounted cash flows.
- **Decision Rule**: Shorter payback is better; typically acceptable if < 3 years for OpEx, < 5 years for CapEx.

### Return on Investment (ROI)

ROI = (Total Benefits - Total Costs) / Total Costs x 100%

### Metrics Summary

| Metric                | Value      | Threshold  | Pass / Fail |
|-----------------------|------------|------------|-------------|
| NPV                   |            | > $0       |             |
| IRR                   |            | > WACC     |             |
| Simple Payback        |            | < 3 years  |             |
| Discounted Payback    |            | < 4 years  |             |
| ROI                   |            | > 100%     |             |

---

## Step 5 — Sensitivity Analysis

Test how the investment outcome changes under different assumptions.

### One-Variable Sensitivity Table

| Variable Changed            | -20%     | -10%     | Base Case | +10%     | +20%     |
|-----------------------------|----------|----------|-----------|----------|----------|
| Revenue growth rate         |          |          |           |          |          |
| Customer adoption rate      |          |          |           |          |          |
| Implementation cost         |          |          |           |          |          |
| Discount rate               |          |          |           |          |          |
| Time to market (delay)      |          |          |           |          |          |

*Values in the table represent the resulting NPV for each sensitivity.*

### Scenario Matrix (Two-Variable)

|                         | Low Adoption (20%) | Base Adoption (35%) | High Adoption (50%) |
|-------------------------|--------------------|---------------------|---------------------|
| Low Price ($X)          | NPV = ...          | NPV = ...           | NPV = ...           |
| Base Price ($Y)         | NPV = ...          | NPV = ...           | NPV = ...           |
| High Price ($Z)         | NPV = ...          | NPV = ...           | NPV = ...           |

### Break-Even Analysis
- What is the minimum revenue needed to break even (NPV = 0)?
- What is the minimum adoption rate needed?
- What is the maximum cost the project can incur before NPV turns negative?

---

## Step 6 — Risk Assessment and Recommendation

Evaluate non-financial risks and deliver a clear recommendation.

### Risk Register

| Risk                           | Probability | Impact   | Severity  | Mitigation Strategy                       |
|--------------------------------|-------------|----------|-----------|-------------------------------------------|
| Technology risk (build failure)|             |          |           | Phased delivery; proof of concept first    |
| Market risk (low demand)       |             |          |           | Customer validation before full commitment |
| Execution risk (delays)        |             |          |           | Agile methodology; milestone checkpoints   |
| Competitive risk               |             |          |           | Speed to market; differentiation focus     |
| Regulatory risk                |             |          |           | Legal review; compliance-by-design         |
| Key person dependency          |             |          |           | Cross-training; documentation              |

*Probability: Low / Medium / High. Impact: Low / Medium / High. Severity: Low / Medium / High / Critical.*

### Recommendation Framework

| Criterion                | Weight | Score (1–5) | Weighted Score |
|--------------------------|--------|-------------|----------------|
| Financial return (NPV)   | 30%    |             |                |
| Strategic alignment      | 25%    |             |                |
| Risk profile             | 20%    |             |                |
| Feasibility / complexity | 15%    |             |                |
| Time to value            | 10%    |             |                |
| **Total**                | 100%   |             |                |

### Recommendation Levels
- **Strong Invest** (score > 4.0): Clear financial and strategic case; manageable risk.
- **Invest with Conditions** (3.0–4.0): Positive case but requires specific mitigations or phased approach.
- **Defer** (2.0–3.0): Uncertain return; revisit when conditions change.
- **Do Not Invest** (< 2.0): Negative NPV or unacceptable risk; pursue alternatives.

---

## Output Format

```
## Investment Analysis — [Project Name]

### 1. Executive Summary
- Investment amount: $X over Y years
- NPV: $X | IRR: X% | Payback: X years
- Recommendation: [Strong Invest / Invest with Conditions / Defer / Do Not Invest]
- Key rationale (3 bullets)

### 2. Investment Overview
[Problem statement, strategic context, alternatives considered]

### 3. Cost Analysis
[Detailed cost breakdown by year]

### 4. Benefits Analysis
[Quantified benefits with confidence ratings]

### 5. Financial Metrics
[NPV, IRR, payback, ROI summary table]

### 6. Sensitivity Analysis
[Sensitivity tables and break-even points]

### 7. Risk Assessment
[Risk register with mitigations]

### 8. Recommendation
[Weighted scoring; clear go/no-go with conditions]

### 9. Appendix
- Detailed cash flow model
- Assumption log
- Comparable investments / benchmarks
```

---

## Quality Checklist

- [ ] All costs are incremental (sunk costs excluded)
- [ ] Benefits are conservatively estimated with confidence ratings
- [ ] Discount rate is documented and approved by Finance
- [ ] NPV, IRR, and payback are consistent with each other
- [ ] Sensitivity analysis covers the 3–5 most impactful variables
- [ ] Risks have specific mitigation strategies, not generic statements
- [ ] "Do nothing" alternative is explicitly evaluated
- [ ] Recommendation is supported by both quantitative and qualitative analysis

---

## Edge Cases

| Scenario                                  | Handling Approach                                                              |
|-------------------------------------------|--------------------------------------------------------------------------------|
| Mutually exclusive projects               | Compare NPVs directly; use incremental IRR for differing scales               |
| Capital rationing (limited budget)        | Rank by profitability index (NPV / Investment); optimize the portfolio         |
| Non-financial strategic investment        | Use weighted scoring framework; document strategic value qualitatively         |
| Very long payback (> 7 years)             | Increase scrutiny; require higher NPV margin; consider stage-gating           |
| Negative NPV but regulatory mandate       | Present as compliance cost; optimize for minimum cost of compliance            |
| Highly uncertain benefits                  | Use Monte Carlo simulation or expected value (probability-weighted outcomes)   |
