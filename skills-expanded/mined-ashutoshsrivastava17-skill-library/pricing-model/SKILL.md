---
name: pricing-model
description: >
  Build and evaluate pricing models — unit economics, margin analysis,
  competitive benchmarking, willingness-to-pay, and scenario modeling.
  TRIGGER when: user says /pricing-model, "pricing strategy", "how to price",
  "pricing analysis", "unit economics", or "pricing model".
argument-hint: "[product or service to price]"
user-invocable: true
---

# Pricing Model

You are a pricing strategist building data-driven pricing models. Analyze unit economics, competitive positioning, and customer willingness-to-pay to recommend optimal pricing.

## Process

### Step 1: Define Pricing Context

| Parameter | Description |
|-----------|-------------|
| Product / service | What is being priced |
| Business model | SaaS, usage-based, marketplace, one-time, hybrid |
| Target segment | SMB, mid-market, enterprise, consumer |
| Current pricing | Existing price points (if any) |
| Competitive range | What competitors charge |
| Cost structure | Fixed costs, variable costs per unit |

### Step 2: Unit Economics

| Metric | Value | Calculation |
|--------|-------|-------------|
| COGS per unit | $X | Direct costs to serve one customer/unit |
| Gross margin | X% | (Revenue - COGS) / Revenue |
| CAC | $X | Total S&M spend / New customers |
| LTV | $X | ARPA × Gross Margin × (1 / Churn Rate) |
| LTV:CAC | X:1 | Target >3:1 |
| Payback period | X months | CAC / (ARPA × Gross Margin) |

### Step 3: Pricing Strategies

| Strategy | How It Works | Best For |
|----------|-------------|---------|
| **Cost-plus** | Cost + target margin | Commodities, known cost structure |
| **Value-based** | Price based on customer value delivered | Differentiated products, enterprise |
| **Competitive** | Match or beat market prices | Mature markets, clear alternatives |
| **Penetration** | Low initial price to gain share | New market entry, network effects |
| **Tiered** | Multiple packages at different price points | Serving multiple segments |
| **Usage-based** | Pay for what you use | Variable consumption, API/infra products |

### Step 4: Tier Design (if applicable)

| Tier | Target Buyer | Price | Key Features | Differentiator |
|------|-------------|-------|-------------|---------------|
| Free / Starter | [Persona] | $0 | [Features] | [Why they'd upgrade] |
| Pro | [Persona] | $X/mo | [Features] | [Value anchor] |
| Enterprise | [Persona] | Custom | [Features] | [White-glove, compliance, scale] |

### Step 5: Scenario Modeling

| Scenario | Price | Volume | Revenue | Margin | LTV:CAC |
|----------|-------|--------|---------|--------|---------|
| Current | $X | N | $Y | Z% | A:1 |
| 10% increase | $X+10% | N-? | $Y? | Z%? | A:1? |
| New tier | $X | N+? | $Y? | Z%? | A:1? |

## Output Format

```markdown
## Pricing Model: [Product]

### Unit Economics
[Metric table]

### Pricing Recommendation
[Recommended strategy with rationale]

### Tier Structure
[Tier table with features and prices]

### Competitive Positioning
[How our pricing compares]

### Scenario Analysis
[Revenue impact of different price points]

### Implementation Plan
[Rollout, grandfathering, communication]
```

## Quality Checklist

- [ ] Unit economics are calculated with real cost data
- [ ] Pricing supports target LTV:CAC ratio
- [ ] Competitive benchmarking is current
- [ ] Tiers have clear upgrade incentives
- [ ] Scenario analysis covers upside and downside

## Edge Cases

- **Freemium**: Define conversion targets; ensure free tier drives upgrades, not just freeloading
- **Usage-based pricing**: Provide cost predictability tools; set spending alerts
- **Enterprise custom pricing**: Define a price floor and discounting guidelines
- **Price increase on existing customers**: Plan grandfathering, communication, and churn modeling
