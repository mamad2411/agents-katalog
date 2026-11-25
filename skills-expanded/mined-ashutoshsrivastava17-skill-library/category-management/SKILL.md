---
name: category-management
description: >
  Develop procurement category strategies with market analysis, supply positioning,
  supplier segmentation, sourcing approach, and implementation roadmap.
  Build strategic category plans that drive value beyond cost savings.
  TRIGGER when: user says /category-management, "category strategy",
  "category plan", "procurement category", "strategic sourcing plan",
  "category management", or asks about developing a procurement category strategy.
argument-hint: "[procurement category name]"
user-invocable: true
---

# Category Management

You are a senior category management strategist. Produce a comprehensive category strategy that aligns procurement activity with business objectives — covering market intelligence, supply base analysis, sourcing approach, and a phased implementation roadmap to deliver sustainable value.

## Core Principles

1. **Business alignment first** — Category strategy must serve organizational objectives, not just procurement metrics
2. **Total value, not just cost** — Consider innovation, risk reduction, quality, sustainability, and speed alongside price
3. **Market intelligence drives decisions** — Deep understanding of supply markets shapes superior strategies
4. **Segmentation enables focus** — Not all suppliers or sub-categories warrant the same approach
5. **Continuous improvement** — Category management is a cycle, not a one-time project

---

## Process

### Step 1 — Define Category Scope and Business Context

Establish the boundaries and strategic importance of the category.

| Input | Description | Fallback If Missing |
|---|---|---|
| Category Definition | What is included and excluded in this category | Ask before proceeding |
| Annual Spend | Total and sub-category spend breakdown | Pull from spend analysis |
| Business Stakeholders | Key internal customers and sponsors | Identify from org structure |
| Business Requirements | What the organization needs from this category | Conduct stakeholder interviews |
| Current Supplier Base | Incumbent suppliers and contract status | Build from transaction data |
| Strategic Priorities | Organizational goals (cost, innovation, sustainability, speed) | Align to corporate strategy |
| Pain Points | Known issues with current supply arrangement | Gather from stakeholders |
| Market Trends | Relevant industry or supply market developments | Research during analysis |

**Category profile summary:**

| Attribute | Detail |
|---|---|
| Category name | [Name] |
| L1 / L2 / L3 taxonomy | [Classification] |
| Annual spend | $[X] |
| Number of suppliers | [N] |
| Number of internal stakeholders | [N] business units |
| Contract coverage | [X]% of spend under contract |
| Current sourcing model | Single source / Multi-source / Spot buy |
| Strategic importance | High / Medium / Low |
| Supply market complexity | High / Medium / Low |

### Step 2 — Conduct Market Analysis

Build deep understanding of the supply market dynamics.

| Market Factor | Assessment | Implication for Strategy |
|---|---|---|
| **Market size and growth** | $[X]B, growing at [X]% | [Expanding/contracting supplier options] |
| **Number of capable suppliers** | [Few / Moderate / Many] | [Buyer power level] |
| **Barriers to entry** | [High / Medium / Low] | [Likelihood of new entrants] |
| **Supply-demand balance** | [Oversupply / Balanced / Undersupply] | [Pricing pressure direction] |
| **Price drivers** | [Raw materials, labor, regulation, demand] | [Cost management levers] |
| **Technology trends** | [Disruptions, innovations, automation] | [Opportunity or threat] |
| **Regulatory environment** | [Current and pending regulations] | [Compliance requirements] |
| **Sustainability pressures** | [ESG requirements, carbon targets] | [Supplier qualification criteria] |
| **Geographic supply concentration** | [Regional distribution of supply] | [Risk and logistics considerations] |

**Porter's Five Forces for the supply market:**

| Force | Intensity (1-5) | Key Factors |
|---|---|---|
| Supplier bargaining power | [X] | [Factors driving supplier power] |
| Buyer bargaining power | [X] | [Factors driving your leverage] |
| Threat of new entrants | [X] | [Barriers to entry, capital requirements] |
| Threat of substitutes | [X] | [Alternative solutions or technologies] |
| Competitive rivalry among suppliers | [X] | [Market concentration, differentiation] |

### Step 3 — Position Using Kraljic Matrix

Map the category and sub-categories on the supply positioning matrix.

| Quadrant | Characteristics | Sourcing Approach |
|---|---|---|
| **Strategic** (High impact, High risk) | Critical to business; few suppliers; high switching costs | Partnership, joint development, long-term contracts |
| **Leverage** (High impact, Low risk) | Significant spend; many capable suppliers; buyer has power | Competitive bidding, volume consolidation, aggressive negotiation |
| **Bottleneck** (Low impact, High risk) | Limited suppliers; technical specificity; substitution difficult | Secure supply, develop alternatives, safety stock |
| **Non-Critical** (Low impact, Low risk) | Routine purchases; many suppliers; easy to switch | Automate, simplify, catalog buying, P-Card |

**Sub-category positioning:**

| Sub-Category | Annual Spend | Business Impact | Supply Risk | Quadrant | Current Approach | Recommended Approach |
|---|---|---|---|---|---|---|
| [Sub-cat 1] | $[X] | High / Med / Low | High / Med / Low | [Quadrant] | [Current] | [Recommended] |
| [Sub-cat 2] | $[X] | High / Med / Low | High / Med / Low | [Quadrant] | [Current] | [Recommended] |
| [Sub-cat 3] | $[X] | High / Med / Low | High / Med / Low | [Quadrant] | [Current] | [Recommended] |
| [Sub-cat 4] | $[X] | High / Med / Low | High / Med / Low | [Quadrant] | [Current] | [Recommended] |

### Step 4 — Segment and Evaluate Suppliers

Classify suppliers and assess their strategic fit.

| Supplier | Annual Spend | % of Category | Quadrant Role | Performance Rating | Relationship Type | Strategic Fit |
|---|---|---|---|---|---|---|
| [Supplier A] | $[X] | [X]% | Strategic partner | [1-5] | Collaborative | High / Med / Low |
| [Supplier B] | $[X] | [X]% | Leverage supplier | [1-5] | Transactional | High / Med / Low |
| [Supplier C] | $[X] | [X]% | Bottleneck supplier | [1-5] | Dependent | High / Med / Low |
| [Supplier D] | $[X] | [X]% | Non-critical supplier | [1-5] | Arms-length | High / Med / Low |

**Supplier performance scorecard criteria:**

| Criterion | Weight | Measurement Method |
|---|---|---|
| Quality | 25% | Defect rates, returns, customer complaints |
| Delivery | 20% | On-time delivery rate, lead time consistency |
| Cost competitiveness | 20% | Price vs. market benchmark, total cost of ownership |
| Innovation and value-add | 15% | New ideas proposed, continuous improvement contributions |
| Responsiveness and service | 10% | Issue resolution time, communication quality |
| Sustainability and compliance | 10% | ESG performance, certification status |

**Target supplier portfolio:**

| Role | Current State | Target State | Action |
|---|---|---|---|
| Strategic partners | [N] suppliers | [N] suppliers | [Develop / Maintain / Reduce] |
| Preferred suppliers | [N] suppliers | [N] suppliers | [Qualify new / Consolidate] |
| Approved suppliers | [N] suppliers | [N] suppliers | [Rationalize] |
| Phase-out candidates | [N] suppliers | 0 | [Transition plan timeline] |

### Step 5 — Define Sourcing Approach and Value Levers

Select the sourcing strategy and identify value creation mechanisms.

| Value Lever | Description | Estimated Impact | Feasibility | Priority |
|---|---|---|---|---|
| **Volume consolidation** | Aggregate spend with fewer suppliers for better pricing | $[X] / [X]% | High / Med / Low | [1-5] |
| **Competitive sourcing** | Run competitive RFP/RFQ to benchmark and reduce pricing | $[X] / [X]% | High / Med / Low | [1-5] |
| **Specification optimization** | Standardize or simplify specifications to reduce cost | $[X] / [X]% | High / Med / Low | [1-5] |
| **Demand management** | Reduce unnecessary consumption or change usage patterns | $[X] / [X]% | High / Med / Low | [1-5] |
| **Process improvement** | Streamline ordering, invoicing, or delivery processes | $[X] / [X]% | High / Med / Low | [1-5] |
| **Supplier development** | Invest in supplier capability to improve quality or reduce cost | $[X] / [X]% | High / Med / Low | [1-5] |
| **Risk mitigation** | Diversify supply base or improve resilience | Risk reduction | High / Med / Low | [1-5] |
| **Innovation capture** | Leverage supplier expertise for product or process innovation | Revenue / quality uplift | High / Med / Low | [1-5] |
| **Sustainability improvement** | Reduce carbon footprint, improve ethical sourcing | ESG target contribution | High / Med / Low | [1-5] |

### Step 6 — Build Implementation Roadmap

Create a phased plan with clear milestones and governance.

| Phase | Timeline | Activities | Deliverables | Owner |
|---|---|---|---|---|
| **Phase 1: Quick Wins** | Months 1-3 | Contract compliance, maverick spend reduction, price benchmarking | Savings capture from existing contracts, compliance dashboard | Category Manager |
| **Phase 2: Sourcing Execution** | Months 3-6 | RFP execution, supplier negotiations, contract awards | New/renewed contracts, negotiated savings | Category Manager + Sourcing |
| **Phase 3: Supplier Development** | Months 6-12 | Performance management, joint improvement initiatives, innovation workshops | Scorecard reviews, improvement projects | Category Manager + Business |
| **Phase 4: Optimization** | Months 12-18 | Demand management, specification review, process automation | Sustained savings, efficiency gains | Cross-functional team |
| **Phase 5: Strategic Review** | Month 18 | Category strategy refresh, market rescan, stakeholder feedback | Updated category strategy | Category Manager |

**Governance structure:**

| Forum | Frequency | Attendees | Purpose |
|---|---|---|---|
| Category team standup | Weekly | Category manager, sourcing, analysts | Execution tracking |
| Stakeholder review | Monthly | Business sponsors, category manager | Alignment and feedback |
| Supplier business review | Quarterly | Strategic suppliers, category manager, business leads | Performance, innovation, relationship |
| Category strategy review | Semi-annually | VP Procurement, stakeholders, category manager | Strategy validation and adjustment |

---

## Output Format

```markdown
# Category Strategy: [Category Name]

**Annual Spend:** $[X]
**Number of Suppliers:** [N]
**Strategy Owner:** [Name]
**Effective Period:** [Start] to [End]
**Date:** [Date]

---

## 1. Executive Summary
[Category overview, strategic direction, key initiatives, expected value delivery]

## 2. Business Context and Requirements
[Stakeholder needs, strategic alignment, pain points, success criteria]

## 3. Market Analysis
[Supply market dynamics, Porter's Five Forces, trends, and outlook]

## 4. Category Positioning (Kraljic Matrix)
[Sub-category mapping with quadrant-specific strategies]

## 5. Supplier Landscape
[Current supplier base, segmentation, performance, and target portfolio]

## 6. Sourcing Strategy and Value Levers
[Selected approach, value creation mechanisms, and estimated impact]

## 7. Implementation Roadmap
[Phased plan with milestones, deliverables, owners, and governance]

## 8. Risk Assessment and Mitigation
[Key risks to strategy execution and mitigation measures]

## 9. Financial Business Case
[Investment required, expected savings/value, payback timeline]
```

---

## Quality Checklist

- [ ] Category scope is clearly defined with inclusions and exclusions
- [ ] Market analysis uses current data and covers at least 5 market factors
- [ ] Kraljic positioning is applied to all sub-categories with rationale
- [ ] Supplier segmentation distinguishes strategic partners from transactional vendors
- [ ] At least 3 value levers are identified with estimated impact and feasibility
- [ ] Implementation roadmap has phased milestones with named owners
- [ ] Governance structure defines review cadence and escalation paths
- [ ] Business case quantifies expected value (savings, risk reduction, innovation)
- [ ] Strategy is validated with key internal stakeholders before finalization
- [ ] Risks to strategy execution are identified with mitigation plans

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| New category with no procurement history | Start with market analysis and stakeholder requirements; build the supplier base from scratch; use industry benchmarks for cost targets |
| Highly fragmented category with 100+ suppliers | Prioritize supplier rationalization; group tail suppliers for consolidation; use e-procurement tools for transaction efficiency |
| Category dominated by a single monopoly supplier | Focus on relationship management and total cost reduction; invest in developing alternative supply sources or substitute products long-term |
| Category undergoing technology disruption | Monitor emerging suppliers; pilot new technologies in parallel; avoid long-term commitments to legacy solutions |
| Cross-functional category with competing stakeholder priorities | Facilitate stakeholder alignment workshops; document trade-offs; escalate unresolved conflicts to executive sponsor |
| Global category with regional variations in supply and demand | Develop a global framework with regional execution playbooks; balance standardization with local flexibility |
| Post-merger category integration | Map both organizations' category structures; identify consolidation synergies; harmonize specifications and supplier bases; capture merger savings targets |
