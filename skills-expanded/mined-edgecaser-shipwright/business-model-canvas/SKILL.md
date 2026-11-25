---
name: business-model-canvas
description: "Builds a full Business Model Canvas covering all 9 building blocks: Customer Segments, Value Propositions, Channels, Customer Relationships, Revenue Streams, Key Resources, Key Activities, Key Partnerships, and Cost Structure. More comprehensive than a Lean Canvas, better suited to established products or when you need to map the entire business system."
category: strategy
default_depth: standard
---

# Business Model Canvas

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Builds a full Business Model Canvas covering all 9 building blocks: Customer Segments, Value Propositions, Channels, Customer Relationships, Revenue Streams, Key Resources, Key Activities, Key Partnerships, and Cost Structure. More comprehensive than a Lean Canvas, better suited to established products or when you need to map the entire business system.

## When to Use

- Mapping a mature product's full business model for strategic review
- Comparing business models across product lines or business units
- Preparing for board presentations or investor due diligence
- Evaluating partnerships or platform plays where multiple sides need modeling
- When Lean Canvas is too startup-focused for your context

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick snapshot for a stakeholder conversation or internal alignment check | Customer Segments, Value Propositions, Revenue Streams only |
| **Standard** | Strategic review or partnership evaluation | All 9 building blocks + Key Dependencies + Stress Test |
| **Deep** | Board presentation, investor due diligence, or M&A evaluation | All sections + per-segment P&L breakdown, competitive model comparison, scenario modeling |

**Omit rules:** At Light depth, skip Channels, Customer Relationships, Key Resources, Key Activities, Key Partnerships, and Cost Structure. Produce only the three demand-side blocks with Key Dependencies noted inline.

## Framework

### The Nine Building Blocks

Work through them in this order, starting from the customer side:

```markdown
# Business Model Canvas: [Product / Business Unit]

**Date:** [date]
**Scope:** [what exactly is being modeled]

## 1. Customer Segments
Who are we creating value for? Which customers matter most?

| Segment | Size | Revenue Contribution | Growth Trend |
|---|---|---|---|
| [e.g., "Mid-market SaaS (100-500 employees)"] | [e.g., "~12,000 companies in US"] | [e.g., "65% of ARR"] | [Growing / Stable / Declining] |
| | | | |

**Segment type:** [Mass market / Niche / Segmented / Multi-sided platform / Diversified]

## 2. Value Propositions
What value do we deliver to each segment? What problem do we solve? What need do we satisfy?

| Segment | Value Proposition | Key Differentiator |
|---|---|---|
| [Segment 1] | [What they get from us] | [Why us over alternatives] |
| | | |

**Value drivers:** [Newness / Performance / Customization / Design / Brand / Price / Cost reduction / Risk reduction / Accessibility / Convenience]

## 3. Channels
How do we reach each customer segment? How do they want to be reached?

| Phase | Channel | Effectiveness |
|---|---|---|
| Awareness | [e.g., "Content marketing, SEO, conference talks"] | [High / Medium / Low] |
| Evaluation | [e.g., "Free trial, product demos, case studies"] | |
| Purchase | [e.g., "Self-serve checkout, inside sales"] | |
| Delivery | [e.g., "Cloud SaaS, API"] | |
| After-sales | [e.g., "In-app support, CSM for enterprise"] | |

## 4. Customer Relationships
What type of relationship does each segment expect? How do we establish and maintain them?

| Segment | Relationship Type | Key Touchpoints |
|---|---|---|
| [Segment 1] | [Self-service / Automated / Personal assistance / Dedicated / Co-creation / Community] | [e.g., "Onboarding call, quarterly review, support chat"] |
| | | |

## 5. Revenue Streams
What are customers willing to pay for? How do they currently pay? How would they prefer to pay?

| Revenue Stream | Model | Price Point | % of Total Revenue |
|---|---|---|---|
| [e.g., "Platform subscription"] | [Subscription / Usage / Licensing / Transaction fee] | [e.g., "$500/mo per seat"] | [e.g., "80%"] |
| [e.g., "Professional services"] | [One-time / Retainer] | [e.g., "$15K implementation"] | [e.g., "20%"] |

**Pricing mechanism:** [Fixed / Dynamic / Auction / Market-dependent / Volume-dependent / Negotiated]

## 6. Key Resources
What assets does our business model require?

| Resource | Type | Owned or Accessed | Critical? |
|---|---|---|---|
| [e.g., "ML models trained on proprietary data"] | [Physical / Intellectual / Human / Financial] | [Owned / Licensed / Partnered] | [Yes / No] |
| | | | |

## 7. Key Activities
What activities does our business model require us to do well?

| Activity | Category | Current Capability |
|---|---|---|
| [e.g., "Platform reliability (99.99% uptime)"] | [Production / Problem-solving / Platform management / Supply chain] | [Strong / Adequate / Needs investment] |
| | | |

## 8. Key Partnerships
Who are our key partners and suppliers? Which resources do we get from them? Which activities do they perform?

| Partner | What They Provide | What We Provide | Dependency Level |
|---|---|---|---|
| [e.g., "AWS"] | [e.g., "Infrastructure, global availability"] | [e.g., "Revenue (cloud spend)"] | [High / Medium / Low] |
| | | | |

**Partnership type:** [Strategic alliance / Coopetition / Joint venture / Buyer-supplier]

## 9. Cost Structure
What are the most important costs in our business model? Which key resources and activities are most expensive?

| Cost Category | Type | Monthly/Annual | % of Total |
|---|---|---|---|
| [e.g., "Engineering team"] | [Fixed / Variable] | [e.g., "$180K/mo"] | [e.g., "45%"] |
| [e.g., "Cloud infrastructure"] | [Variable] | [e.g., "$40K/mo"] | [e.g., "10%"] |

**Cost structure type:** [Cost-driven / Value-driven]
**Economies of scale:** [Where costs decrease with growth]
**Economies of scope:** [Where costs decrease with breadth]
```

## Minimum Evidence Bar

**Required inputs:** Product or business unit name, target customer description, and at least a directional revenue model.

**Acceptable evidence:** Internal revenue data, pricing pages, partnership agreements, customer interviews, published market sizing, team headcount or cost estimates.

**Insufficient evidence:** If no customer segment data or revenue model exists, produce a partial artifact with unanswered sections marked `[TBD, requires: customer segment validation or revenue model data]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Customer Segments (size, contribution), Revenue Streams (price points, model), Cost Structure (known fixed/variable costs) must be grounded in evidence.
- **Hypotheses:** Key Partnerships, Channel effectiveness ratings, and growth trends may be speculative, must be labeled as assumptions.

## Output Format

Produce:
1. **Full Business Model Canvas** with all 9 blocks completed
2. **Key Dependencies** - which blocks are most tightly coupled and what breaks if one changes
3. **Stress Test** - the 3 weakest links in the model and what would need to be true for them to hold

**Shipwright Signature (required closing):**
4. **Decision Frame**, Which business model elements to commit to vs. experiment on, key trade-offs, confidence level with evidence quality, owner, decision date, revisit trigger
5. **Unknowns & Evidence Gaps**, Unvalidated segment sizes, untested channel assumptions, unconfirmed partnership terms
6. **Pass/Fail Readiness**, PASS if all 9 blocks have evidence-backed entries and dependencies are mapped (at Light depth: PASS if Customer Segments, Value Propositions, and Revenue Streams have evidence-backed entries, remaining blocks are deferred); FAIL if any included block relies entirely on assumptions with no supporting data
7. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Confusing BMC with Lean Canvas** - BMC maps the full business system; Lean Canvas focuses on problem-solution fit for early-stage products. Use the right one for your stage.
- **Filling boxes with aspirations instead of reality** - Model what exists today, then note where you want to go. Mixing the two makes the canvas useless for decision-making.
- **Treating it as a one-time exercise** - The canvas should be revisited when your model changes (new segment, new pricing, new partnership).
- **Ignoring the connections between blocks** - A change in Customer Segments cascades through Value Propositions, Channels, Relationships, and Revenue Streams. Call out the dependencies.
- **Too generic** - "We provide value to customers" belongs nowhere on a useful canvas. Be specific enough that someone unfamiliar with your product could understand the business model.

## Weak vs. Strong Output

**Weak:**
> **Value Proposition:** We help companies be more efficient and save money.

No segment specificity, no measurable outcome, indistinguishable from any other B2B product.

**Strong:**
> **Value Proposition (Mid-market SaaS, 100-500 employees):** Reduces monthly financial close from 12 days to 3 by automating inter-entity reconciliation, saving ~$40K/quarter in controller time.

Tied to a named segment, quantified outcome, and a specific mechanism that can be verified.
