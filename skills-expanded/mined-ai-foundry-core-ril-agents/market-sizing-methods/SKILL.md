---
name: market-sizing-methods
description: TAM/SAM/SOM estimation, ICP definition, and customer segment sizing. Use when estimating market opportunity, defining ideal customer profiles, or sizing addressable segments.
---

# Market Sizing Methods

Market sizing is frequently done wrong — either too optimistically (top-down from industry reports) or too vaguely (hand-waving about "a large and growing market"). This skill covers rigorous methods for estimating opportunity size and defining who to target.

## When to Use This Skill

- Sizing the opportunity before committing to a product direction
- Defining the ideal customer profile (ICP) for a new product or segment
- Estimating TAM/SAM/SOM for business planning or investor materials
- Validating whether a niche is large enough to build a business on
- Segmenting an existing user base by value and growth potential

## Core Concepts

### TAM / SAM / SOM

| Term | Definition | Question It Answers |
|------|-----------|-------------------|
| **TAM** — Total Addressable Market | Everyone who could theoretically buy this | How big is the universe? |
| **SAM** — Serviceable Addressable Market | The portion you can realistically reach with your current model | How much of TAM can you access? |
| **SOM** — Serviceable Obtainable Market | What you can realistically capture given competition and constraints | What can you actually win? |

TAM is for context. SAM is for planning. SOM is for forecasting.

### Top-Down vs. Bottom-Up

**Top-down:** Start from industry size data, apply percentages down to your segment.
- Fast but often inaccurate — percentages compound errors
- Use as a sanity check, not a primary estimate

**Bottom-up:** Start from individual customer unit economics, build up.
- More work but far more defensible
- Forces explicit assumptions about pricing and adoption

Always do both and compare. When they diverge significantly, investigate why.

## Bottom-Up TAM Estimation

### Steps

1. **Define the unit:** What's one customer? (one business, one user, one seat)
2. **Define the universe:** How many units exist that match your target definition?
3. **Apply revenue per unit:** What would each unit pay per year?
4. **Multiply:** Universe × ARPU = TAM

### Example

```
Product: B2B expense management tool
Target: SMBs with 10-200 employees in the US

Step 1 — Universe:
  US businesses with 10-200 employees: ~1.5M (Census Bureau data)
  Subset with travel/expense activity: ~60% = 900K businesses

Step 2 — ARPU:
  Base price: $15/seat/month × avg 25 seats = $375/month = $4,500/year

Step 3 — TAM:
  900K businesses × $4,500/year = $4.05B TAM

SAM (reachable via digital/PLG model):
  Businesses with >5 employees that use SaaS tools: ~40% = 360K
  360K × $4,500 = $1.62B SAM

SOM (Year 3 target):
  0.5% market share = 1,800 customers × $4,500 = $8.1M ARR
```

### Transparency Requirements

For every market size estimate, document:
- The data source for the universe size
- The assumptions behind any percentages applied
- The revenue per unit assumption and how it was derived
- Confidence level: High (primary research), Medium (secondary data), Low (estimation)

## ICP Definition

The Ideal Customer Profile describes the type of customer most likely to buy, retain, and expand. It's not a persona (who they are) — it's a firmographic and behavioral profile (what kind of organization they are and what they're doing when they buy).

### ICP Template

```
# Ideal Customer Profile: [Segment Name]

## Firmographics (B2B) / Demographics (B2C)
- Company size: [employees / revenue range]
- Industry: [specific verticals]
- Geography: [regions / markets]
- Tech maturity: [description]

## Behavioral Signals
- What triggers them to look for a solution like ours:
- What they're currently using (or doing) instead:
- How they evaluate and buy:

## Jobs to Be Done
- Primary job: [what they're trying to accomplish]
- Constraints: [what limits their current approach]

## Value Realization
- Time to first value: [how quickly they see benefit]
- Expansion pattern: [how usage grows after initial purchase]
- Retention risk: [what causes churn]

## Negative ICP (who to avoid)
- [Characteristics of customers who churn, are unprofitable, or require excessive support]
```

### ICP Validation Signals

An ICP definition is a hypothesis until validated by:
- **Win rate:** Deals matching the ICP close at a higher rate
- **Time to value:** ICP customers reach activation faster
- **Retention:** ICP customers churn less
- **NPS / satisfaction:** ICP customers are more satisfied
- **Expansion:** ICP customers expand their usage

If your best customers don't match your stated ICP, update the ICP.

## Segment Sizing and Prioritization

When multiple segments exist, score each on:

| Dimension | Question | Score |
|-----------|---------|-------|
| **Size** | How many potential customers? | 1-5 |
| **Willingness to pay** | How much would they pay? | 1-5 |
| **Accessibility** | How easy to reach and sell? | 1-5 |
| **Strategic fit** | How well does this segment align with our strengths? | 1-5 |
| **Growth trajectory** | Is this segment growing? | 1-5 |

Rank segments by total score. Focus initial go-to-market on the top 1-2 segments.

## Common Sizing Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| "1% of a $10B market" | Doesn't explain HOW you get that 1% | Build a bottom-up model instead |
| Using industry reports uncritically | Reports define markets differently than your product | Redefine from first principles |
| Conflating TAM with SAM | Not all of TAM is reachable with your GTM model | Apply accessibility filters |
| No negative ICP | Targeting everyone means optimizing for no one | Define explicitly who you're NOT targeting |
| Static sizing | Markets change; a 3-year-old estimate may be wrong | Date estimates and refresh annually |

## Best Practices

1. **Show your work** — every number needs a source or a stated assumption
2. **Use ranges, not point estimates** — $400M–$700M is more honest than $550M
3. **Start with SAM, not TAM** — TAM impresses; SAM is what you can actually build a business on
4. **Test the ICP against real customers** — your best customers define the ICP, not the other way around
5. **Update annually** — market structure changes; stale sizing leads to wrong decisions
