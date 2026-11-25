---
name: financial-modeling
description: Build business cases, ROI analyses, and financial models for consulting recommendations — cost-benefit analysis, NPV/IRR calculations, sensitivity analysis, scenario modeling, and investment justification. Use whenever business case, ROI, financial model, cost-benefit, NPV, IRR, payback period, scenario analysis, or investment justification come up. Use when user asks to "build a financial model", "revenue forecast", "DCF analysis", or mentions financial projections, valuation, scenario modeling, or sensitivity analysis.
---

# Financial Modeling for Consulting Engagements

Build traceable decision models, not guaranteed forecasts. Separate source facts, user inputs, assumptions, formulas, and scenarios; record units and as-of dates; reconcile outputs; and require qualified finance, accounting, tax, or investment review for consequential decisions.

A rigorous financial model is the foundation of credible recommendations. It forces clarity on assumptions, quantifies impact, enables trade-off analysis, and builds confidence that recommendations are justified. Poor financial models make consulting recommendations questionable and undermine implementation. This skill covers building business cases, financial analyses, and models that drive decisions.

## Business Case Structure

A complete business case has five components:

### 1. Problem Statement & Business Context

**What:**
- What problem are we solving?
- Why does it matter? (strategic, financial, operational impact)
- What's the status quo cost?
- What changes in the business environment make this urgent now?

**Example (insufficient):** "We need to implement a new ERP system."

**Example (strong):** "Current order processing takes 3 days and costs $200K annually in manual labor. We're constrained in handling growth: scaling current process would require +15 FTE. New market entrants can process orders in 4 hours. We need to reduce cycle time to <4 hours and automate exception handling to support 25% volume growth without proportional labor increase. This is a growth enabler and a cost reducer."

### 2. Options Analysis

Develop 2-3 realistic options. Avoid straw men.

**Option A: Status Quo (baseline)**
- Cost: $200K annually (current state labor + system maintenance)
- Impact: No improvement in cycle time or scalability
- Used as comparison baseline

**Option B: Improve Current Process**
- Redesign workflow; add staff; upgrade current system
- Cost: $150K implementation + $220K annual running cost (slight labor improvement)
- Impact: 10% efficiency gain; still limited scalability
- Risk: Incremental approach doesn't solve fundamental constraints

**Option C: Implement New Cloud System (Recommended)**
- New cloud-native order management platform
- Cost: $400K implementation + $180K annual running cost
- Impact: Reduces cycle time to <4 hours; automates 80% of exceptions; supports 2-3x volume growth
- Risk: System implementation, change management

Present options with equal weight (avoid leading language like "Option A (risky)" vs. "Option B (good)").

### 3. Financial Analysis for Recommended Option

Quantify costs and benefits over a defined period (3-5 years typical for IT investments).

**Costs (Year 1 vs. Ongoing):**
- Implementation/capital costs
- Training and change management
- Ongoing license/support/maintenance
- Operational ramp-up costs

**Benefits:**
- Hard savings: Direct cost reductions (labor, systems, materials)
- Revenue impact: Top-line improvement (volume, price, market share)
- Working capital: Improvements in days sales outstanding (DSO), inventory turns, etc.

**Net impact:** Benefits - Costs = Net Benefit

### 4. Risk Assessment

Identify key risks and mitigation strategies.

**Risks** (examples):
- Implementation delay (pushing benefit realization)
- Lower adoption than expected (reducing benefit)
- Cost overrun (increasing investment)
- Technology risk (system doesn't work as expected)
- Organizational change capacity (can't execute in parallel with other initiatives)

**Mitigations:**
- Governance and project management
- Executive sponsorship
- Change management investment
- Phased implementation
- Contingency budget

### 5. Implementation Plan & Timeline

High-level timeline showing:
- Key phases and milestones
- When costs are incurred vs. when benefits flow
- Dependencies and critical path
- Resource needs

---

## Cost-Benefit Analysis

### Identifying and Quantifying Costs

**Implementation Costs (Year 1):**
- Software/platform: $250K (software license + implementation partner)
- Hardware/infrastructure: $80K (servers, network, security)
- Data migration: $40K (extract/transform/load current data)
- Training development: $30K (curriculum design, instructor prep)
- Training delivery: $50K (salary + travel for 3 instructors, 5 days per 50 trainees)
- Change management: $70K (change lead salary, communications, coaching)
- **Total Year 1: $520K**

**Ongoing Costs (Year 2+):**
- Annual license/support: $120K
- Hosting/infrastructure: $40K
- Maintenance and enhancements: $30K
- Training (new employees): $15K
- **Total ongoing: $205K/year**

**Types of Costs to Include:**

| Cost Type | Examples | How to Estimate |
|-----------|----------|-----------------|
| **Direct Labor** | Consulting fees, internal PM time, training delivery | Hourly rates × hours needed |
| **Software/Licenses** | System cost, tools, infrastructure | Vendor quotes; industry benchmarks |
| **Hardware** | Servers, network, equipment | Vendor quotes; IT capital standards |
| **Travel** | Implementation team travel, training | Per diem rates × travel days |
| **Contingency** | Unforeseen costs | 10-15% of direct costs |
| **Indirect/Hidden** | IT support time, business interruption | Survey or estimate hours required |

**Avoid these mistakes:**
- Forgetting ongoing costs (licenses, support, training new hires)
- Underestimating implementation (add 20% contingency)
- Forgetting indirect costs (IT setup/support, business user time)
- Double-counting (don't count both "system cost" and "implementation labor" separately if vendor quotes are all-in)

### Identifying and Quantifying Benefits

**Hard Savings (directly reduce costs):**

| Benefit Type | Mechanism | Quantification | Example |
|--------------|-----------|---|---------|
| **Labor reduction** | Fewer people needed for task | Hours/people saved × loaded labor cost | Save 1 FTE = $80K (salary) + $20K (benefits) = $100K/year |
| **System consolidation** | Eliminate redundant systems | Old system cost - new system cost | Eliminate 2 legacy systems = $60K licenses + $30K maintenance |
| **Efficiency improvement** | Same output, less time | Hours saved × loaded labor cost | Reduce order processing from 3 days to 1 day = 2 days × headcount × loaded rate |
| **Defect/rework reduction** | Fewer errors, less rework | Error frequency × cost per error | Reduce order errors from 5% to 0.5% = 450 fewer errors/month × $40/error = $216K/year |

**Revenue Impact (increase sales/margin):**

| Benefit Type | Mechanism | Quantification | Example |
|---|---|---|---|
| **Volume growth** | Capability enables new business | Additional volume × margin per unit | Faster order processing enables 20% growth = 500 additional orders/month × $100 margin = $600K/year |
| **Price realization** | Better data/insight enables pricing power | Price increase × volume | Improved visibility enables 2% price increase = 2% × $10M revenue = $200K/year |
| **Customer retention** | Better service reduces churn | Churn reduction × customer lifetime value | Reduce churn 1% = 50 customers × $4K LTV = $200K/year |

**Soft Benefits (harder to quantify but real):**
- Improved customer satisfaction (could lead to volume/retention)
- Better decision-making (improved data visibility)
- Faster time to market
- Reduced risk (better controls, compliance)
- Employee satisfaction (less manual work)

**How to handle soft benefits:**
1. Don't include in base NPV calculation (overstates case)
2. Mention as upside: "If improved customer satisfaction drives 2% volume growth, NPV would be $1.2M instead of $800K"
3. Make explicit: "We assume no revenue impact in base case"

### Net Benefit Calculation

Simple formula:

**Net Benefit (Year X) = Benefits (Year X) - Costs (Year X)**

Multi-year example:

| Year | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | Total |
|---|---|---|---|---|---|---|
| **Implementation Costs** | ($520K) | — | — | — | — | ($520K) |
| **Ongoing Costs** | ($100K) | ($205K) | ($205K) | ($205K) | ($205K) | ($920K) |
| **Labor Savings** | $50K | $350K | $350K | $350K | $350K | $1,450K |
| **System Consolidation** | — | $90K | $90K | $90K | $90K | $360K |
| **Efficiency Gains** | — | $200K | $200K | $200K | $200K | $800K |
| **Revenue (volume growth)** | — | $300K | $600K | $600K | $600K | $2,100K |
| **Net Benefit** | ($570K) | $735K | $1,035K | $1,035K | $1,035K | $3,270K |

**Year 1 is negative (investment year); breaks even Year 2.**

---

## NPV, IRR, and Payback Period

### Net Present Value (NPV)

**Concept:** Value of future cash flows discounted to today's dollars.

**Why it matters:** $1 today is worth more than $1 in 3 years (because you could invest it and earn returns). NPV adjusts for time value of money.

**Formula:**

NPV = Σ [Cash Flow(t) / (1 + discount rate)^t] - Initial Investment

Where:
- t = year (0, 1, 2, 3...)
- discount rate = cost of capital (typically 8-12% for corporate projects)
- Cash Flow(t) = net benefit in year t

**Example with 10% discount rate:**

| Year | Net Cash Flow | Discount Factor (10%) | Present Value |
|---|---|---|---|
| 0 | ($520K) | 1.000 | ($520K) |
| 1 | ($100K) | 0.909 | ($91K) |
| 2 | $735K | 0.826 | $607K |
| 3 | $1,035K | 0.751 | $777K |
| 4 | $1,035K | 0.683 | $707K |
| 5 | $1,035K | 0.621 | $643K |
| **NPV** | | | **$2,123K** |

**Interpretation:**
- NPV > 0: Investment creates value; recommend proceeding
- NPV < 0: Investment destroys value; do not proceed
- Compare NPV across options: Higher NPV = better value creation

**Discount rate selection:**
- 8-10%: Low-risk projects (cost reduction, operational efficiency)
- 10-15%: Medium-risk projects (new capabilities, market entry)
- 15%+: High-risk projects (unproven technology, new markets)

### Internal Rate of Return (IRR)

**Concept:** The discount rate at which NPV = 0. Think of it as the "return on investment."

**Formula:** Solve for discount rate where: Σ [Cash Flow(t) / (1 + IRR)^t] = 0

**Easiest to calculate in Excel using =IRR() function.**

**Example continuing above:**

Using Excel IRR function on the cash flows:
**IRR = 68%**

**Interpretation:**
- IRR represents the annualized return on the investment
- Compare to cost of capital (discount rate)
- If IRR > cost of capital, investment is worth doing
- In this case, 68% IRR >> 10% cost of capital → strong investment

**When to use NPV vs. IRR:**
- Use NPV when: Comparing projects with different sizes or time horizons (NPV is more reliable)
- Use IRR when: Simple ROI view; communicating to executives ("This generates 68% returns")
- Use both: Present NPV + IRR together

**IRR limitations:**
- Assumes cash flows can be reinvested at the IRR rate (often unrealistic)
- Can have multiple IRRs in some cases (unusual but possible)
- Less reliable for comparing projects of very different sizes

### Payback Period

**Concept:** How long until the investment is recovered?

**Calculation:** Find the year when cumulative cash flow becomes positive.

Using the example above:
- Year 0: Cumulative = ($520K)
- Year 1: Cumulative = ($620K) [($520K) + ($100K)]
- Year 2: Cumulative = $115K [($620K) + $735K]

**Payback Period ≈ 1.8 years** (breaks even early in Year 2)

**More precise calculation:**
- Cumulative through Year 1: ($620K)
- Year 2 cash flow: $735K
- Payback = 1 + |($620K) / $735K| = 1 + 0.84 = 1.84 years

**When to use:**
- Useful for understanding cash flow timing
- Important for liquidity-constrained organizations
- Often required by management ("We need payback within 2 years")

**Limitations:**
- Doesn't account for time value of money
- Ignores cash flows after payback
- Can be misleading (favors short-term projects)

**Use payback as a secondary metric alongside NPV/IRR.**

---

---

## References

For detailed templates, frameworks, and field-level guidance, read:

- [`references/financial-modeling-reference.md`](references/financial-modeling-reference.md) — Complete framework details, templates, and examples

Read this file when the task requires:
- Sensitivity Analysis
- Common Financial Models for Consulting
- Model Quality Standards
- Presenting Financial Analysis
- Financial Modeling Deliverables
