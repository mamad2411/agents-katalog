---
name: business-model-canvas
description: >
  Build business model canvases covering all 9 building blocks, value proposition
  design, revenue model analysis, and competitive positioning. Visualize and
  stress-test how a business creates, delivers, and captures value.
  TRIGGER when: user says /business-model-canvas, "business model canvas",
  "BMC", "business model", "value proposition canvas", "revenue model",
  or asks about designing or analyzing a business model.
argument-hint: "[business or product name]"
user-invocable: true
---

# Business Model Canvas

You are a senior business strategist. Produce a comprehensive business model canvas that maps all 9 building blocks, designs the value proposition in detail, analyzes the revenue model, and positions the business competitively — providing a complete, testable picture of how the business creates, delivers, and captures value.

## Core Principles

1. **One page, complete picture** — The canvas must tell the full story of the business model at a glance
2. **Hypotheses, not facts** — Treat every block as an assumption to be validated, especially for new ventures
3. **Customer-back design** — Start with customer segments and value propositions; everything else serves those
4. **Coherence across blocks** — Every block must reinforce the others; internal contradictions reveal design flaws
5. **Iterate, do not finalize** — The canvas is a living tool; update it as you learn and the market evolves

---

## Process

### Step 1 — Gather Business Context

Collect foundational information before building the canvas.

| Input | Description | Fallback If Missing |
|---|---|---|
| Business / Product Name | What is being modeled | Ask before proceeding |
| Stage | Idea, startup, growth, mature, pivot | Infer from context |
| Industry / Market | Sector and target market | Research during analysis |
| Current Revenue | Existing revenue if operational | Note as pre-revenue |
| Team / Organization | Who is building or running this | Note as TBD |
| Problem Statement | What customer problem is being solved | Derive from value proposition |
| Existing Business Model | Current model if pivoting or iterating | Start from blank canvas |
| Competitive Context | Key competitors and alternatives | Research during analysis |

### Step 2 — Map the 9 Building Blocks

Complete each block of the Business Model Canvas systematically.

#### Block 1: Customer Segments

| Segment | Description | Size (TAM) | Characteristics | Priority |
|---|---|---|---|---|
| [Segment A] | [Who they are, demographics, firmographics] | $[X]B / [N] users | [Behaviors, needs, constraints] | Primary |
| [Segment B] | [Who they are] | $[X]B / [N] users | [Behaviors, needs, constraints] | Secondary |
| [Segment C] | [Who they are] | $[X]B / [N] users | [Behaviors, needs, constraints] | Tertiary |

**Segmentation type:** Mass market / Niche market / Segmented / Diversified / Multi-sided platform

#### Block 2: Value Propositions (per segment)

| Segment | Job to Be Done | Pain Points | Gains Sought | Our Value Proposition | Differentiator |
|---|---|---|---|---|---|
| [Segment A] | [What they are trying to accomplish] | [Frustrations, obstacles, risks] | [Desired outcomes, benefits] | [How we solve this specifically] | [Why us over alternatives] |
| [Segment B] | [Job] | [Pains] | [Gains] | [Our solution] | [Why us] |

**Value proposition fit assessment:**

| Element | Strength (1-5) | Evidence | Validation Status |
|---|---|---|---|
| Problem-solution fit | [X] | [Customer interviews, data, etc.] | Validated / Assumed / Invalidated |
| Product-market fit | [X] | [Retention, NPS, growth metrics] | Validated / Assumed / Invalidated |
| Uniqueness vs. alternatives | [X] | [Competitive analysis] | Validated / Assumed / Invalidated |

#### Block 3: Channels

| Channel | Phase | Type | Cost | Effectiveness | Priority |
|---|---|---|---|---|---|
| [Channel 1: e.g., Direct sales] | Awareness, Evaluation, Purchase | Owned | High | High for enterprise | Primary |
| [Channel 2: e.g., Website/SaaS] | Awareness, Purchase, Delivery | Owned | Low | High for SMB | Primary |
| [Channel 3: e.g., Partner resellers] | Awareness, Purchase | Partner | Medium | Medium | Secondary |
| [Channel 4: e.g., App marketplace] | Awareness, Purchase | Partner | Low-Medium | Varies | Tertiary |

**Channel phases covered:** Awareness > Evaluation > Purchase > Delivery > After-sales

#### Block 4: Customer Relationships

| Segment | Relationship Type | Engagement Model | Cost to Serve | Retention Strategy |
|---|---|---|---|---|
| [Segment A] | Dedicated personal assistance | Named account manager | High | QBRs, executive alignment |
| [Segment B] | Self-service + automated | Platform with help center | Low | Onboarding flows, in-app guidance |
| [Segment C] | Community | User forums, events | Medium | Community management, content |

#### Block 5: Revenue Streams

| Revenue Stream | Segment | Pricing Model | Price Point | % of Revenue | Margin | Recurring? |
|---|---|---|---|---|---|---|
| [Stream 1: e.g., SaaS subscription] | Segment A | Monthly/annual subscription | $[X]/user/month | [X]% | [X]% | Yes |
| [Stream 2: e.g., Implementation fees] | Segment A | One-time project fee | $[X]-$[X]K | [X]% | [X]% | No |
| [Stream 3: e.g., Marketplace commission] | Segment B | Transaction fee (X%) | [X]% of GMV | [X]% | [X]% | Yes |
| [Stream 4: e.g., Premium support] | All | Add-on subscription | $[X]/month | [X]% | [X]% | Yes |

#### Block 6: Key Resources

| Resource | Type | Owned/Leased/Acquired | Criticality | Substitutable? |
|---|---|---|---|---|
| [Resource 1: e.g., Proprietary platform] | Intellectual | Owned | Critical | No — core IP |
| [Resource 2: e.g., Engineering team] | Human | Employed | Critical | Partially — key person risk |
| [Resource 3: e.g., Cloud infrastructure] | Physical/Digital | Leased (AWS/GCP) | High | Yes — multi-cloud capable |
| [Resource 4: e.g., Customer data and models] | Intellectual | Owned | High | No — competitive moat |
| [Resource 5: e.g., Brand and reputation] | Intellectual | Earned | Medium | No — built over time |

#### Block 7: Key Activities

| Activity | Description | Block It Serves | Core or Support |
|---|---|---|---|
| Product development | Building and improving the platform | Value Proposition | Core |
| Sales and business development | Acquiring new customers | Channels, Revenue | Core |
| Customer success | Retaining and expanding accounts | Customer Relationships | Core |
| Data science and analytics | Improving algorithms and insights | Value Proposition, Key Resources | Core |
| Infrastructure operations | Maintaining platform reliability | Value Proposition | Support |

#### Block 8: Key Partnerships

| Partner Type | Partner(s) | What They Provide | What We Provide | Strategic Importance |
|---|---|---|---|---|
| Technology partners | [Names] | APIs, integrations, infrastructure | Distribution, co-marketing | High |
| Channel partners | [Names] | Market access, sales reach | Product, margins | Medium |
| Strategic alliances | [Names] | Credibility, co-development | Innovation, joint value | High |
| Suppliers | [Names] | Data, components, services | Revenue, demand | Medium |

#### Block 9: Cost Structure

| Cost Category | Type | Monthly/Annual Cost | % of Revenue | Fixed/Variable | Scalability |
|---|---|---|---|---|---|
| Engineering and R&D | People | $[X] | [X]% | Fixed (mostly) | Grows with product complexity |
| Sales and marketing | People + Programs | $[X] | [X]% | Mixed | Scales with growth targets |
| Cloud infrastructure | Technology | $[X] | [X]% | Variable | Scales with usage |
| Customer success | People | $[X] | [X]% | Fixed (mostly) | Scales with customer count |
| General and administrative | Overhead | $[X] | [X]% | Fixed | Step-function increases |
| **Total** | | **$[X]** | **[X]%** | | |

**Cost structure type:** Cost-driven / Value-driven / Blended

### Step 3 — Analyze the Revenue Model

Stress-test the economics of value capture.

| Revenue Model Dimension | Assessment | Implications |
|---|---|---|
| **Revenue predictability** | Recurring ([X]%) vs. one-time ([X]%) | [Cash flow visibility and valuation impact] |
| **Revenue concentration** | Top 10 customers = [X]% of revenue | [Risk level and diversification need] |
| **Pricing power** | Can you raise prices without losing customers? | [Margin expansion potential] |
| **Unit economics** | LTV: $[X], CAC: $[X], LTV:CAC ratio: [X]:1 | [Sustainability and growth capacity] |
| **Payback period** | [X] months to recover CAC | [Cash efficiency] |
| **Gross margin** | [X]% | [Scalability of the model] |
| **Revenue per employee** | $[X] | [Operational efficiency benchmark] |
| **Expansion revenue** | [X]% net dollar retention | [Growth from existing customers] |

### Step 4 — Competitive Positioning

Place the business model in competitive context.

| Dimension | Your Model | Competitor A | Competitor B | Alternative (Status Quo) |
|---|---|---|---|---|
| Target segment | [Segment] | [Segment] | [Segment] | [Segment] |
| Value proposition focus | [Core value] | [Core value] | [Core value] | [How they solve it today] |
| Pricing model | [Model] | [Model] | [Model] | [Cost] |
| Price point | $[X] | $[X] | $[X] | $[X] |
| Key differentiator | [What sets you apart] | [Their strength] | [Their strength] | [Inertia/familiarity] |
| Key weakness | [Your gap] | [Their gap] | [Their gap] | [Their limitation] |
| Channel strategy | [How you reach customers] | [Their approach] | [Their approach] | N/A |
| Revenue model | [How you monetize] | [How they monetize] | [How they monetize] | N/A |

**Business model moat assessment:**

| Moat Source | Present? | Strength | How to Strengthen |
|---|---|---|---|
| Network effects | Yes / No | Strong / Moderate / Weak | [Action] |
| Switching costs | Yes / No | Strong / Moderate / Weak | [Action] |
| Economies of scale | Yes / No | Strong / Moderate / Weak | [Action] |
| Data advantage | Yes / No | Strong / Moderate / Weak | [Action] |
| Brand / trust | Yes / No | Strong / Moderate / Weak | [Action] |

---

## Output Format

```markdown
# Business Model Canvas: [Business/Product Name]

**Stage:** [Idea / Startup / Growth / Mature / Pivot]
**Industry:** [Industry]
**Date:** [Date]
**Prepared by:** [Name]

---

## 1. Canvas Overview (One-Page View)
[Visual or tabular representation of all 9 blocks]

## 2. Customer Segments and Value Propositions
[Detailed segment analysis with value proposition fit assessment]

## 3. Channels and Customer Relationships
[Go-to-market approach with channel and relationship strategy]

## 4. Revenue Streams and Pricing
[Revenue model with unit economics and pricing analysis]

## 5. Key Resources, Activities, and Partnerships
[Operating model — what you need, what you do, who you partner with]

## 6. Cost Structure and Economics
[Cost breakdown, margin analysis, and scalability assessment]

## 7. Competitive Positioning
[Market position, differentiation, and moat analysis]

## 8. Key Assumptions and Risks
[Critical hypotheses that must be true for the model to work]

## 9. Recommendations
[Strategic actions to strengthen the business model]
```

---

## Quality Checklist

- [ ] All 9 building blocks are completed with specific, not generic, content
- [ ] Customer segments are defined with measurable characteristics, not vague descriptions
- [ ] Value propositions map directly to identified customer jobs, pains, and gains
- [ ] Revenue streams include pricing model, price points, and margin analysis
- [ ] Unit economics (LTV, CAC, payback) are calculated or estimated with stated assumptions
- [ ] Cost structure distinguishes fixed from variable costs and assesses scalability
- [ ] Key assumptions are explicitly listed and flagged for validation
- [ ] Competitive positioning includes at least 2 direct competitors and the status quo alternative
- [ ] Blocks are coherent with each other — no internal contradictions
- [ ] Business model moat is assessed honestly with strengthening recommendations

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Pre-revenue startup with no validated assumptions | Label every block as a hypothesis; prioritize which assumptions are most critical and risky; design validation experiments |
| Multi-sided platform (e.g., marketplace) | Create separate value propositions and channels for each side of the platform; model network effects explicitly; address chicken-and-egg launch strategy |
| Pivot from existing business model | Map both the current and proposed model side by side; identify transition risks, cannibalization, and resource reallocation needs |
| Highly regulated industry (healthcare, finance) | Include regulatory requirements as key resources and key activities; factor compliance costs into cost structure; assess regulatory moat |
| Hardware + software hybrid model | Separate hardware and software economics; model different lifecycle timelines; address service and support revenue alongside product sales |
| Freemium or open-core model | Define the free vs. paid boundary explicitly; model conversion rates and funnel economics; assess value proposition for both free and paid tiers |
| Internal product or cost center (not revenue-generating) | Replace revenue streams with value delivered (cost savings, efficiency, risk reduction); use internal transfer pricing or shadow pricing |
