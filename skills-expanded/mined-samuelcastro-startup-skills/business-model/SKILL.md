---
name: business-model
description: Help founders design pricing strategy, analyze unit economics, and create competitive positioning. Use when a founder asks "How should I price this?", "What's my unit economics?", "How do I position against competitors?", "Is this a good business model?", "Help me figure out my margins", "What's my LTV/CAC?", "Should I do subscription or usage-based?", or needs to articulate their business model for investors.
---

# Business Model Design

Guide founders from business model selection through pricing, unit economics, and competitive positioning to investor-ready articulation.

## Workflow

### 1. Diagnose Current State

Ask: "Where are you in business model development?"

| State | Signals | Next Step |
|-------|---------|-----------|
| **No model yet** | Has product idea, no monetization plan | → Step 2: Select Business Model Type |
| **Model chosen** | Knows type (SaaS, marketplace, etc.), needs pricing | → Step 3: Design Pricing |
| **Has pricing** | Needs to validate unit economics | → Step 4: Unit Economics Analysis |
| **Entering market** | Needs differentiation strategy | → Step 5: Competitive Positioning |
| **Pitch prep** | Needs to articulate model clearly | → Step 6: Create Deliverables |

### 2. Select Business Model Type

Match founder's product to the right model archetype. See `references/business-model-patterns.md` for the complete pattern library.

**Core Model Types (YC Framework):**

| Model | Description | Key Metrics | Best For |
|-------|-------------|-------------|----------|
| **SaaS** | Cloud subscription software | MRR/ARR, NRR, CAC | B2B software with recurring value |
| **Transactional** | Take cut of transactions | GTV, Net Revenue, Retention | Fintech, payments |
| **Marketplace** | Connect buyers + sellers | GMV, Take Rate, Liquidity | Platforms with network effects |
| **Subscription** | Recurring consumer service | MRR, Churn, LTV | Consumer products with habit |
| **Enterprise** | Large contracts to big companies | Bookings, ACV, Pipeline | Complex B2B, long sales cycles |
| **Usage-Based** | Pay per consumption | Monthly Revenue, Retention | APIs, infrastructure, cloud |
| **E-commerce** | Sell products online | Revenue, Gross Margin, CAC | D2C brands, physical goods |
| **Advertising** | Monetize free users via ads | DAU/MAU, Retention, CPM | High-scale consumer apps |

**Selection Questions:**
1. Who pays? (End user, business, advertiser, both sides?)
2. How often do they pay? (One-time, recurring, per-use?)
3. What's the natural buying pattern? (Impulse, considered, enterprise?)
4. Where's the value? (Product, platform, network?)

### 3. Design Pricing Strategy

Three foundational approaches — choose based on market position:

| Strategy | When to Use | Method |
|----------|-------------|--------|
| **Value-Based** | Differentiated product, clear ROI | Price based on customer value delivered |
| **Cost-Plus** | Commodity market, known costs | Cost + target margin (rarely optimal for SaaS) |
| **Competitive** | Established market, price-sensitive | Position relative to alternatives |

See `references/pricing-frameworks.md` for detailed implementation.

**Pricing Model Selection (for SaaS/subscription):**

| Model | Pros | Cons | Use When |
|-------|------|------|----------|
| **Per-seat** | Simple, predictable | Limits adoption | Value scales with users |
| **Per-feature (tiered)** | Natural upsell path | Complexity | Clear feature-value tiers exist |
| **Usage-based** | Scales with customer | Revenue volatility | Value directly tied to consumption |
| **Flat-rate** | Dead simple | Leaves money on table | Early stage, testing |
| **Freemium** | Low friction acquisition | Conversion challenge | Wide top-of-funnel, viral potential |
| **Hybrid** | Flexibility | Complexity | Enterprise + self-serve motions |

**Value Metric Selection (HOPE Framework):**
Find the metric that best captures value delivery:
- **H**igh value connection — Does it correlate to customer outcomes?
- **O**bvious to customer — Is it familiar and predictable?
- **P**redictable — Can customers forecast their usage?
- **E**asy to implement — Can you actually measure and bill it?

Common value metrics: seats, contacts, API calls, records, storage, revenue processed, messages sent.

**Pricing Sanity Checks:**
- Does price reflect value delivered?
- Can customers predict their bill?
- Is there a natural expansion path?
- Does pricing align with how customers budget?

### 4. Unit Economics Analysis

The health check for any business model. See `references/unit-economics.md` for formulas and benchmarks.

**Core Metrics:**

| Metric | Formula | Healthy Benchmark |
|--------|---------|-------------------|
| **CAC** | Total S&M Spend ÷ New Customers | Varies by model |
| **LTV** | (ARPU × Gross Margin) ÷ Churn Rate | 3× CAC minimum |
| **LTV:CAC Ratio** | LTV ÷ CAC | 3:1 to 5:1 optimal |
| **CAC Payback** | CAC ÷ Monthly Gross Profit | <12 months for SaaS |
| **Gross Margin** | (Revenue - COGS) ÷ Revenue | >70% for SaaS |

**Diagnostic Questions:**
1. What does it cost to acquire a customer? (CAC)
2. How much will that customer pay over their lifetime? (LTV)
3. How long until you recoup acquisition cost? (Payback)
4. Are you making money on each transaction? (Gross Margin)

**Red Flags:**
- LTV:CAC < 1:1 — Unsustainable, losing money on every customer
- LTV:CAC 1:1 to 2:1 — Dangerous, need optimization
- CAC Payback > 18 months — Cash flow risk, slow growth
- Gross Margin < 50% — Not a software business, harder to scale

**By Business Model Type:**

| Model | Key Economics | Target |
|-------|---------------|--------|
| **B2B SaaS** | LTV:CAC 3:1+, Payback <12mo | NRR >100% |
| **B2C SaaS** | LTV:CAC 3:1+, Payback <6mo | Viral coefficient >1 |
| **Marketplace** | Unit margin positive, GMV growth | Take rate 10-20% |
| **E-commerce** | Contribution margin >30%, CAC < first order | Repeat rate >40% |

### 5. Competitive Positioning

How to stand out in a crowded market. See `references/positioning-frameworks.md` for detailed frameworks.

**April Dunford's Positioning Flow:**

```
Competitive Alternatives → Unique Capabilities → Value → Target Customer → Market Category
```

**Step-by-step:**

1. **List Competitive Alternatives**
   - What would customers do if you didn't exist?
   - Include: direct competitors, indirect solutions, doing nothing, manual processes

2. **Identify Unique Capabilities**
   - What do you have that alternatives don't?
   - Features, technology, service, price, experience

3. **Map to Value**
   - So what? What does each capability enable?
   - Connect features → benefits → outcomes

4. **Define Best-Fit Customers**
   - Who cares most about your unique value?
   - What characteristics make someone care?

5. **Choose Market Category**
   - What context makes your value obvious?
   - Options: existing category, subcategory, new category

**Positioning Statement Template:**
> For [target customer] who [need/job], [product] is a [category] that [key benefit]. Unlike [competitors], we [key differentiator].

**Porter's Strategic Options:**
- **Cost Leadership** — Win on price (lowest cost structure)
- **Differentiation** — Win on value (unique capabilities worth premium)
- **Focus** — Win in a niche (cost or differentiation, narrow market)

**Positioning Strategies:**

| Strategy | When to Use | Risk |
|----------|-------------|------|
| **Head-to-Head** | You can genuinely beat the leader | Resource-intensive |
| **Big Fish, Small Pond** | Niche underserved by leaders | Market may be too small |
| **Create New Category** | Truly novel, no good comparison | Education cost is high |

### 6. Create Deliverables

**Output 1: Business Model One-Pager**

```markdown
## [Company Name] Business Model

**Model Type:** [SaaS/Marketplace/etc.]

**Value Proposition:** 
[One sentence: For whom, what problem, unique solution]

**Customer Segments:**
- Primary: [Description, size, characteristics]
- Secondary: [If applicable]

**Revenue Model:**
- Type: [Subscription/Usage/Transaction/etc.]
- Pricing: [Structure and price points]
- Value metric: [What you charge for]

**Key Metrics:**
| Metric | Current | Target |
|--------|---------|--------|
| MRR/ARR | $ | $ |
| Customers | # | # |
| LTV | $ | $ |
| CAC | $ | $ |
| LTV:CAC | X:1 | X:1 |

**Unit Economics:**
- Gross Margin: X%
- CAC Payback: X months
- Expansion potential: [How customers grow with you]

**Go-to-Market:**
- Primary channel: [How you acquire]
- Sales motion: [Self-serve/Sales-assisted/Enterprise]
```

**Output 2: Pricing Recommendation**

Document should include:
- Recommended pricing model with rationale
- Specific price points with justification
- Tier structure (if applicable)
- Comparison to alternatives
- Expected conversion/upgrade rates

**Output 3: Unit Economics Spreadsheet**

Create spreadsheet with:
- CAC calculation (itemized S&M spend)
- LTV calculation (ARPU, churn, margin)
- LTV:CAC ratio
- CAC payback period
- Sensitivity analysis (what if churn changes?)
- 12-month projection

See `references/unit-economics.md` for template structure.

**Output 4: Positioning Statement**

Format:
> For [target customer with specific characteristics] who [struggle with specific problem], [Product Name] is a [market category] that [delivers specific benefit/outcome]. Unlike [primary alternative], our product [key differentiator that matters to target customer].

Plus supporting elements:
- Competitive alternatives map
- Unique capabilities list
- Value proof points
- Best-fit customer profile

## Reference Files

- `references/business-model-patterns.md` — 55+ business model patterns with examples
- `references/pricing-frameworks.md` — Value-based, competitive, and hybrid pricing in detail
- `references/unit-economics.md` — LTV, CAC, formulas, benchmarks, and spreadsheet template
- `references/positioning-frameworks.md` — April Dunford method, Porter's strategies, positioning templates

---

*Adapted from [Linas Beliūnas's](https://linas.substack.com/p/onepersonunicorn) **The One-Person Unicorn** founder skill set.*
