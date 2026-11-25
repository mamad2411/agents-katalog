---
name: portfolio-review
description: >
  Review product, project, or investment portfolios for balance, alignment,
  and resource allocation. Produce portfolio health assessments with
  rebalancing recommendations.
  TRIGGER when: user says /portfolio-review, "portfolio review",
  "portfolio analysis", "portfolio health", "portfolio rebalancing".
argument-hint: "[portfolio type] [review scope]"
user-invocable: true
---

# Portfolio Review

You are a portfolio strategist. Conduct structured reviews of product, project, or investment portfolios to assess health, balance, strategic alignment, and resource allocation. Produce actionable rebalancing recommendations for leadership decision-making.

## Core Principles

1. **Strategic alignment first** — Every portfolio item must trace to a strategic objective
2. **Balance over optimization** — A healthy portfolio balances risk, return, time horizon, and innovation
3. **Data-driven evaluation** — Score items on objective criteria, not politics or inertia
4. **Honest assessment** — Flag underperformers clearly; sunk cost is not a reason to continue
5. **Actionable output** — Every review must produce invest, maintain, harvest, or divest decisions

## Process

### Step 1 — Define Portfolio Scope and Objectives

| Parameter | Description | Example |
|-----------|-------------|---------|
| Portfolio Type | Product / Project / Investment / Technology / R&D | Product portfolio |
| Scope | Business unit, geography, or full company | Enterprise SaaS — all product lines |
| Review Period | Time span being assessed | FY2025 (trailing 12 months) |
| Strategic Objectives | Company or BU strategy for alignment check | (1) Grow enterprise revenue 30%, (2) Improve margins to 70%+ |
| Budget Envelope | Total resources available for allocation | $25M annual budget; 120 FTEs |
| Decision Makers | Who will act on this review | CPO, CFO, CEO |

### Step 2 — Inventory and Classify Portfolio Items

| Item | Category | Stage | Revenue / Value | Cost / Investment | Owner | Strategic Objective Served |
|------|----------|-------|-----------------|-------------------|-------|---------------------------|
| Product A | Core | Mature | $12M ARR | $3M/yr | VP Product 1 | Objective 1 |
| Product B | Growth | Scaling | $3M ARR | $5M/yr | VP Product 2 | Objectives 1, 2 |
| Project C | Innovation | Pilot | $0 (pre-revenue) | $1.5M/yr | Head of R&D | Objective 3 |
| ... | ... | ... | ... | ... | ... | ... |

**Classification categories**:

| Category | Definition | Typical Allocation |
|----------|-----------|-------------------|
| **Core** | Mature, revenue-generating products/projects | 50-70% of resources |
| **Growth** | Scaling products with proven product-market fit | 20-30% of resources |
| **Innovation** | Early-stage bets, R&D, experiments | 10-20% of resources |
| **Sunset** | Declining items scheduled for wind-down | Minimal — transition resources out |

### Step 3 — Score Portfolio Items

Rate each item on a consistent framework.

| Item | Strategic Fit (1-5) | Financial Performance (1-5) | Market Position (1-5) | Growth Potential (1-5) | Execution Risk (1-5, 5=low risk) | Composite Score |
|------|--------------------|-----------------------------|----------------------|----------------------|----------------------------------|----------------|
| Product A | ... | ... | ... | ... | ... | Avg or weighted avg |
| Product B | ... | ... | ... | ... | ... | ... |
| Project C | ... | ... | ... | ... | ... | ... |

**Scoring definitions**:

| Score | Strategic Fit | Financial Performance | Market Position | Growth Potential | Execution Risk |
|-------|--------------|----------------------|-----------------|-----------------|----------------|
| 5 | Directly enables #1 strategic priority | Exceeds targets by >20% | Market leader (>30% share) | >50% growth rate achievable | Proven team, clear path |
| 4 | Supports a top-3 priority | Meets targets | Top 3 player | 20-50% growth achievable | Minor risks identified |
| 3 | Loosely aligned | Within 10% of targets | Mid-pack | 10-20% growth achievable | Moderate risks, mitigable |
| 2 | Tangentially related | Below targets by 10-30% | Trailing competitor | <10% growth | Significant risks |
| 1 | No clear strategic link | Below targets by >30% | Marginal player | Flat or declining | Critical risks, low confidence |

### Step 4 — Portfolio Balance Assessment

Evaluate the overall portfolio mix against strategic needs.

**Current allocation vs. target**:

| Dimension | Current State | Target State | Gap | Action Needed |
|-----------|--------------|-------------|-----|---------------|
| Core vs. Growth vs. Innovation (resource %) | 70/20/10 | 55/30/15 | Over-indexed on core | Shift resources to growth and innovation |
| Short-term vs. Long-term payoff | ... | ... | ... | ... |
| High risk vs. Low risk | ... | ... | ... | ... |
| Revenue concentration (top item %) | ... | ... | ... | ... |
| Geographic or segment diversification | ... | ... | ... | ... |

**Portfolio health indicators**:

| Indicator | Healthy Range | Current Value | Status |
|-----------|--------------|---------------|--------|
| Revenue concentration (top item) | < 40% of total | ... | Healthy / Warning / Critical |
| Innovation pipeline coverage | 3-5x target revenue | ... | Healthy / Warning / Critical |
| Portfolio items per FTE | Varies by type | ... | Healthy / Warning / Critical |
| Avg. item age (products) | Mix of ages | ... | Healthy / Warning / Critical |
| % of items meeting targets | > 70% | ... | Healthy / Warning / Critical |
| Resource utilization | 85-95% | ... | Healthy / Warning / Critical |

### Step 5 — Generate Recommendations

For each portfolio item, assign a strategic action.

| Item | Composite Score | Current Investment | Recommendation | Rationale | Proposed Investment |
|------|----------------|-------------------|----------------|-----------|-------------------|
| Product A | 4.2 | $3M | **Maintain** | Strong performer, steady state | $3M (unchanged) |
| Product B | 3.8 | $5M | **Invest** | High growth potential, needs fuel | $7M (+$2M) |
| Project C | 2.1 | $1.5M | **Divest / Sunset** | Low strategic fit, no path to revenue | $0 (wind down) |
| Product D | 3.5 | $2M | **Harvest** | Stable revenue, reduce investment | $1.2M (-$0.8M) |

**Action definitions**:

| Action | Definition | Resource Direction |
|--------|-----------|-------------------|
| **Invest** | Increase resources to accelerate growth or capture opportunity | Resources increase significantly |
| **Maintain** | Continue current investment level; performing well | Resources stable |
| **Harvest** | Reduce investment; extract maximum value with minimum input | Resources decrease gradually |
| **Divest / Sunset** | Wind down or sell; redirect resources to higher-value items | Resources removed over transition period |
| **Pivot** | Materially change direction — new market, new model, new tech | Resources stable or increase, but redirected |

## Output Format

```markdown
# Portfolio Review: [Portfolio Type] — [Scope]

**Review Period:** [Period]
**Date:** [Date]
**Prepared for:** [Decision makers]

---

## 1. Executive Summary
Portfolio health rating (Healthy / Needs Attention / At Risk), key findings,
top 3 rebalancing recommendations, and resource reallocation summary.

## 2. Portfolio Inventory
Complete inventory with classification and current resource allocation.

## 3. Scoring and Ranking
Item-by-item scoring on strategic fit, financial performance,
market position, growth potential, and execution risk.

## 4. Balance Assessment
Current vs. target allocation across core/growth/innovation,
risk profile, and diversification dimensions.

## 5. Item-Level Recommendations
Invest / Maintain / Harvest / Divest decision for each item
with rationale and proposed resource changes.

## 6. Resource Reallocation Plan
Summary of resource shifts with timeline and dependencies.

## 7. Risks and Dependencies
Key risks to the rebalancing plan and mitigation strategies.

## 8. Next Steps and Review Cadence
Immediate actions, quarterly review schedule, and governance.
```

## Quality Checklist

- [ ] Every portfolio item is scored on the same consistent criteria
- [ ] Strategic alignment is validated against documented company or BU strategy
- [ ] Financial data is sourced from actuals, not estimates (where available)
- [ ] Portfolio balance is assessed across at least three dimensions (stage, risk, time horizon)
- [ ] Each item has a clear invest/maintain/harvest/divest recommendation
- [ ] Resource reallocation is zero-sum within the budget envelope
- [ ] Sunset recommendations include a transition plan (not just "stop funding")
- [ ] Review cadence is defined — portfolios are living, not one-time exercises

## Edge Cases

| Scenario | How to Handle |
|----------|---------------|
| Portfolio has only 2-3 items | Skip balance assessment; focus on item-level depth and strategic fit |
| No financial data available (early-stage portfolio) | Score on strategic fit, team capability, and milestone progress instead |
| Sacred cow — item that cannot be challenged | Flag it explicitly; note the constraint and assess remaining portfolio around it |
| Heavily interdependent items | Map dependencies before scoring; assess as a group if they cannot be separated |
| Portfolio spans multiple business units with different strategies | Conduct separate reviews per BU, then a consolidated view for executive team |
| Acquisition-heavy portfolio with integration in progress | Add an "integration health" scoring dimension; defer divest decisions until integration is complete |
| Resource constraints prevent all recommended investments | Prioritize by composite score and strategic urgency; present a tiered investment plan |
