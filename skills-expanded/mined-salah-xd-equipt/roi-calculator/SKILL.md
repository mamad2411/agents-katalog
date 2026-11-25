---
name: roi-calculator
description: "Builds ROI calculators for business decisions with cost inputs, benefit projections, and payback period analysis. Use when evaluating whether a business investment is worth it."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# ROI Calculator

## When to Use This Skill

Use this skill when you need to:
- Calculate the return on investment for a business decision
- Compare multiple investment options using the same framework
- Determine payback period for a new tool, hire, or initiative
- Build a business case with financial justification

**DO NOT** use this skill for stock market ROI, personal investment analysis, or general financial modeling. This is for operational business investment decisions.

---

## Core Principle

ROI IS A DECISION TOOL — THE GOAL IS NOT PRECISION BUT CLARITY ON WHETHER AN INVESTMENT IS WORTH MAKING AND HOW LONG UNTIL IT PAYS FOR ITSELF.

---

## Phase 1: Investment Context

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Investment description** | "What are you considering investing in? (tool, hire, campaign, equipment)" | No default — must be provided |
| **Total cost** | "What is the total cost? (upfront + ongoing monthly/annual)" | No default — must be provided |
| **Time horizon** | "Over what period should we measure ROI? (6 months, 1 year, 2 years)" | 12 months |
| **Expected benefits** | "What do you expect to gain? (revenue, time saved, cost reduction)" | No default — must be provided |
| **Current baseline** | "What is the current state without this investment?" | No default — describe current process/cost |

**GATE: Do not proceed without the investment cost and expected benefits.**

---

## Phase 2: Cost Analysis

```
## Investment Cost Breakdown

### Upfront Costs
| Item | Cost | Notes |
|------|------|-------|
| [Purchase/setup fee] | $[X] | One-time |
| [Implementation/training] | $[X] | One-time |
| [Migration/switching costs] | $[X] | One-time |
| **Total Upfront** | **$[X]** | |

### Ongoing Costs (Monthly)
| Item | Monthly Cost | Annual Cost |
|------|-------------|-------------|
| [Subscription/license] | $[X] | $[X] |
| [Maintenance/support] | $[X] | $[X] |
| [Additional labor] | $[X] | $[X] |
| **Total Monthly** | **$[X]** | **$[X]** |

### Total Cost of Ownership ([X]-Month Horizon)
| | Amount |
|--|--------|
| Upfront costs | $[X] |
| + Ongoing costs ([X] months) | $[X] |
| **= Total investment** | **$[X]** |
```

---

## Phase 3: Benefit Quantification

```
## Benefit Analysis

### Revenue Benefits
| Benefit | Monthly Value | Annual Value | Confidence |
|---------|-------------|-------------|------------|
| [New revenue enabled] | $[X] | $[X] | High/Med/Low |
| [Revenue increase from efficiency] | $[X] | $[X] | High/Med/Low |

### Cost Savings
| Benefit | Monthly Savings | Annual Savings | Confidence |
|---------|----------------|----------------|------------|
| [Tool/service replaced] | $[X] | $[X] | High |
| [Reduced labor costs] | $[X] | $[X] | Med |

### Time Savings
| Task | Hours Saved/Month | Value (hrs x rate) | Annual Value |
|------|------------------|-------------------|-------------|
| [Task 1] | [X] hrs | $[X] | $[X] |
| [Task 2] | [X] hrs | $[X] | $[X] |

### Total Benefits
| Category | Monthly | Annual |
|----------|---------|--------|
| Revenue benefits | $[X] | $[X] |
| Cost savings | $[X] | $[X] |
| Time savings value | $[X] | $[X] |
| **Total benefits** | **$[X]** | **$[X]** |
```

---

## Phase 4: ROI Calculation and Decision

```
## ROI Summary

### Core Metrics
| Metric | Value |
|--------|-------|
| Total investment ([X] months) | $[X] |
| Total benefits ([X] months) | $[X] |
| Net return | $[X] |
| **ROI percentage** | **[X]%** |
| Payback period | [X] months |
| Monthly net benefit (after payback) | $[X] |

### ROI Formula
ROI = (Total Benefits - Total Investment) / Total Investment x 100

### Payback Timeline
| Month | Cumulative Cost | Cumulative Benefit | Net Position |
|-------|----------------|-------------------|-------------|
| Month 1 | $[X] | $[X] | -$[X] |
| Month 3 | $[X] | $[X] | -$[X] |
| Month 6 | $[X] | $[X] | +/-$[X] |
| Month 12 | $[X] | $[X] | +$[X] |

### Decision Framework
| ROI Range | Recommendation |
|-----------|---------------|
| Over 200% | Strong yes — invest immediately |
| 100-200% | Yes — solid return, proceed |
| 50-100% | Likely yes — if strategic alignment exists |
| 0-50% | Maybe — consider alternatives |
| Negative | No — unless intangible benefits justify it |

### Recommendation
[Clear recommendation based on the numbers with key caveats]
```

---

## Example: Hiring a Virtual Assistant

**Investment:** $2,000/month ($24,000/year). **Benefits:** Saves founder 40 hours/month of admin work valued at $100/hr = $4,000/month in time recaptured. Plus $500/month in tasks done better (inbox management reducing missed opportunities).

**ROI:** ($54,000 - $24,000) / $24,000 = 125% annual ROI. Payback: Immediate — net positive from month 1.

---

## Anti-Patterns

- **Only counting hard dollar returns** — time savings and opportunity cost are real benefits. Quantify them.
- **Ignoring switching costs** — migration, training, and lost productivity during transition are real costs
- **Overconfident benefit projections** — use conservative estimates. If ROI works on conservative numbers, it definitely works in practice.
- **Comparing against doing nothing** — sometimes the alternative is not "do nothing" but "do something different." Compare against the best alternative.
- **Infinite time horizon** — always set a defined time period. An investment that takes 5 years to pay back on a tool you may replace in 2 years is a bad deal.

---

## Recovery

- **Benefits are hard to quantify:** Assign a conservative dollar value to intangible benefits. "Better client experience" = reduced churn = $X retained revenue.
- **Multiple options to compare:** Build a side-by-side comparison table with ROI for each option. Recommend the highest ROI with acceptable risk.
- **ROI is negative but feels necessary:** Identify the minimum benefit needed to break even and assess whether that is achievable. Some investments are strategic even with negative short-term ROI.
- **No baseline data:** Estimate the current cost of the problem being solved. Track for 2-4 weeks if possible before making the investment.
