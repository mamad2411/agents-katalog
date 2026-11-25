---
name: working-capital-optimization
description: Optimizes working capital — improves DPO, accelerates collections, manages inventory, and negotiates payment terms to maximize cash efficiency. Use when the user mentions working capital, cash conversion cycle, DPO, DSO, or asks about improving payment terms, accelerating collections, or optimizing cash tied up in operations.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, cash, treasury, working-capital, cash-conversion-cycle]
related_skills:
  - cash-monitoring
  - cash-forecasting
  - accounts-receivable-management
  - accounts-payable-management
  - banking-relationship-management
inputs_required:
  - current-AP-and-AR-data-from-linked-skills
  - current-payment-terms-per-vendor-and-customer
  - cash-forecast-from-cash-forecasting
  - trailing-12-months-revenue-and-expense-data
deliverables:
  - working-capital-dashboard-DPO-DSO-CCC-trends
  - quick-win-priority-matrix-with-cash-impact
  - negotiation-templates-for-vendors-and-customers
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Working Capital Optimization

Optimize the cash conversion cycle — the time between spending cash and collecting it back. Improve DPO (days payable outstanding), accelerate collections, reduce cash tied up in operations, and negotiate better payment terms.

## Purpose

Working capital is the cash tied up in day-to-day operations — the gap between paying vendors and collecting from customers. Most startups bleed cash through inefficient payment cycles without realizing it. This skill systematically identifies and captures that hidden cash, improving liquidity without raising a single dollar.

## When to Use

- "Optimize our working capital"
- "Improve our cash conversion cycle"
- "Should we negotiate better payment terms?"
- "How can we extend DPO without damaging relationships?"
- "Analyze our working capital efficiency"

## Inputs Required

1. **Current AP and AR data** — from `accounts-payable-management` and `accounts-receivable-management`.
2. **Current payment terms** — per vendor and per customer.
3. **Cash forecast** — from `cash-forecasting` to see impact of changes.
4. **Revenue and expense data** — trailing 12 months.

## Quick Reference

| Metric | Formula | Target |
|--------|---------|--------|
| DSO (Days Sales Outstanding) | (AR / Revenue) × days | Lower is better — collect faster |
| DPO (Days Payable Outstanding) | (AP / COGS) × days | Higher is better — pay slower |
| DIO (Days Inventory Outstanding) | (Inventory / COGS) × days | Lower is better (often 0 for SaaS) |
| CCC (Cash Conversion Cycle) | DIO + DSO - DPO | Negative if possible |
| Every day of DPO gained | (Annual spend / 365) × 1 day | ~$1,370 per $500k spend per day |

## Procedure

### 1. Benchmark Current State

Calculate DPO, DSO, and CCC for the last 3 months. Show the trend.

### 2. Identify Quick Wins

Score each lever:

| Action | Cash Impact | Effort | Risk | Priority |
|---|---|---|---|---|
| Switch largest 3 SaaS subs to annual (negotiate discount) | $30k upfront outlay, $3.6k savings/year | Low | Low | 1 |
| Re-negotiate top 5 vendor terms from net-30 to net-45 | 15 days extra float on $50k/mo = $25k avg cash benefit | Medium | Low | 2 |
| Auto-charge SMB customers vs manual invoicing | Reduces DSO by 5-10 days | Medium | Medium (churn risk) | 3 |
| Offer 10% annual prepay to top 10 customers | $200k cash now vs spread over 12 months | Medium | Medium (dilution) | 4 |

### 3. Model the Impact

For each action, model the cash flow impact week-by-week in the 13-week forecast from `cash-forecasting`.

### 4. Negotiation Playbook

**Vendor payment term extension script:**
> "We're standardizing our payment terms to net-45 to align with our billing cycles. Can we update our agreement starting with the next invoice?"

**Customer prepayment offer:**
> "We're offering a 10% discount for customers who prepay annually. That's $X in savings — want me to switch you over?"

## Output Format

- Working capital dashboard: DPO trend, DSO trend, CCC trend
- Quick-win priority matrix with estimated cash impact
- Negotiation templates for top 10 vendors and customers
- 13-week cash flow impact of proposed changes (integrated with `cash-forecasting`)

## Done Criteria

The skill is complete when:
1. Current DPO, DSO, and CCC are calculated with 3-month trend
2. Quick-win opportunities are scored and ranked by cash impact, effort, and risk
3. Cash flow impact of proposed changes is modeled in the 13-week forecast
4. Negotiation scripts are drafted for top vendors and customers
5. Recommendations include trade-offs (e.g., relationship risk, churn impact)

## Pitfalls

- **Pushing DPO too aggressively on small vendors**: stretching a $2k/mo contractor from net-15 to net-45 may free up $2k in float but damages a relationship that is expensive to replace. Apply DPO optimization where the dollar amounts justify the relationship risk — typically vendors above $10k/month.
- **Optimizing DSO in isolation without considering churn**: auto-charging credit cards and enforcing strict net-30 terms accelerates cash but can trigger involuntary churn if customers experience payment friction. Always A/B test DSO changes on a subset of customers and measure churn impact before rolling out broadly.
- **Treating annual prepay discounts as "free cash"**: a 15% annual prepay discount is effectively a 15% price cut. If the cost of capital (venture debt rate, dilution cost of equity) is lower than the discount rate, prepay offers destroy value. Model the true cost of the discount against your actual cost of capital.
- **Ignoring the timing mismatch between DPO and DSO improvements**: extending DPO takes effect immediately (you simply pay later), while DSO improvements take 2–3 billing cycles to materialize. Planning as if both hit simultaneously overstates near-term working capital improvement.
- **Optimizing for CCC alone without running the cash forecast**: a lower CCC is directionally good, but working capital changes have specific week-by-week cash flow impacts. An action that improves CCC by 5 days could still cause a cash crunch in week 3 if large prepayments coincide with rent and payroll. Always run the 13-week forecast with the proposed changes.

## Verification

Can you answer "what is our current cash conversion cycle and how has it changed in the last 3 months?" Can you identify the top 3 quick wins with estimated dollar impact? Are the trade-offs (relationship risk, churn risk, discount cost) explicitly called out for each recommendation? If not, the optimization is incomplete.

## Example

**User prompt**: "Analyze our working capital efficiency and tell me where to focus."
**What should happen**: Calculate DPO, DSO, and CCC trends for the last 3–6 months, benchmark against SaaS industry norms, identify the biggest-leverage quick wins (ranked by cash impact vs. effort), and produce a priority matrix with estimated dollar impact and implementation timeline.

**User prompt**: "Negotiate better payment terms with our top 5 vendors."
**What should happen**: Pull the top 5 vendors by monthly spend from AP data, assess current terms vs. target DPO for each category, draft category-appropriate negotiation scripts, estimate the permanent cash float benefit of extending terms, and provide a 13-week cash flow impact of the proposed changes.

**User prompt**: "Should we offer annual prepay discounts to our customers?"
**What should happen**: Model the cash flow impact of converting monthly customers to annual prepay at various discount levels (5%, 10%, 15%), calculate the effective cost of capital for each discount rate, compare against the company's actual cost of capital (debt rate or equity dilution cost), and recommend the optimal discount level — or recommend against it if value-destructive.

## Linked Skills

- See current cash impact → `cash-monitoring`
- Model in forecast → `cash-forecasting`
- AR optimization tactics → `accounts-receivable-management`
- AP timing tactics → `accounts-payable-management`
- Banking options (credit lines, float) → `banking-relationship-management`
