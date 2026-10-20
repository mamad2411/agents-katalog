---
name: competitive-product
description: "When to activate: competitive analysis, competitive product, feature comparison, positioning, differentiation, competitive moat, battle cards, win loss analysis"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: product
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Competitive Product Analysis

## Analysis Framework

### Three Questions to Answer
1. **Who** are the competitors? (direct, indirect, substitute)
2. **What** do they offer? (features, pricing, positioning)
3. **Why** do customers choose them over us (or us over them)?

### Competitor Categories
| Type | Definition | Example |
|------|-----------|---------|
| **Direct** | Same product category, same customer | Notion vs Confluence |
| **Indirect** | Different approach, same job-to-be-done | Notion vs email threads |
| **Substitute** | Customer does the job without software | Spreadsheet instead of project tool |
| **Potential** | Not competing yet, could enter | Large platform with adjacent features |

## Feature Comparison Matrix

### Matrix Template
| Feature area | Us | Competitor A | Competitor B | Competitor C |
|-------------|-----|-------------|-------------|-------------|
| Core feature 1 | ✓ | ✓ | ✓ | — |
| Core feature 2 | ✓ | ✓ | — | ✓ |
| Differentiator 1 | ✓ | — | — | — |
| Differentiator 2 | ✓ | Partial | — | ✓ |
| Weakness area | Partial | ✓ | ✓ | ✓ |
| **Pricing** | $X/mo | $Y/mo | $Z/mo | $W/mo |
| **Free tier** | Yes | No | Yes | No |
| **API** | ✓ | ✓ | — | — |
| **Enterprise** | ✓ | ✓ | — | ✓ |

### Scoring Convention
- ✓ Full capability
- Partial = exists but limited / inferior
- — = not available
- ? = unknown / unverified

### Data Sources
- Product's own marketing site and docs
- G2, Capterra, Trustradius reviews
- YouTube demos and walkthroughs
- Reddit discussions in relevant subreddits
- Win/loss interview data from sales
- Competitor job postings (signals investment areas)

## Positioning Map

Plot competitors on two axes that matter to your buyers.

```
         ↑ Enterprise-grade
         |
  [Comp B]  [Comp A]
         |
Ease ←---+--→ Power
of use   |
         |         [Us]
    [Comp C]
         |
         ↓ SMB / self-serve
```

### Choosing Your Axes
- Must reflect what buyers actually care about (validated by interviews)
- Should not be arbitrary — use job-to-be-done or buyer research
- Common axes: price vs features, ease vs power, speed vs reliability, SMB vs enterprise

### Positioning Statement
```
For [target customer] who [need/problem],
[Product] is the [category] that [key benefit]
unlike [alternatives] which [limitation].
```

## Differentiation Strategy Types

| Strategy | Description | Requires |
|----------|------------|---------|
| **Low cost** | Undercut on price | Scale or lower COGS |
| **Differentiation** | Uniquely better at something that matters | Deep product investment |
| **Niche focus** | Best for a specific segment | Vertical expertise |
| **Speed** | Faster to value / deploy | Simplicity focus |
| **Integration** | Plays best in an ecosystem | Platform relationships |
| **Experience** | Design and UX as differentiator | Design investment |

### Differentiation Validation
Your differentiation is real when:
- Customers mention it unprompted in interviews
- Win/loss data shows it as a reason for choosing you
- Competitors cannot easily replicate it (moat exists)
- It connects to a real customer job-to-be-done

## Competitive Moat Assessment

| Moat type | Description | Examples | Durability |
|-----------|------------|---------|-----------|
| **Network effects** | Product more valuable as more users join | Slack, Figma | High |
| **Switching costs** | Painful to leave (data, integrations, habits) | Salesforce, Jira | High |
| **Scale economics** | Lower cost per unit at scale | AWS, Stripe | Medium-High |
| **IP / technology** | Patent, proprietary algorithm, data advantage | Palantir, OpenAI | Medium |
| **Brand** | Trust and recognition | Atlassian, HubSpot | Medium |
| **Ecosystem** | Marketplace, integrations, partners | Shopify, Salesforce | High |

### Moat Assessment Questions
- How long would it take a well-funded competitor to replicate our core value?
- What would a customer lose if they switched tomorrow?
- Does our product get better as we add more customers?
- Do our integrations create lock-in?

## Ongoing Competitive Monitoring

### Alert Setup
- Google Alerts: "[competitor name]", "[competitor] raises", "[competitor] launches"
- G2/Capterra: Monitor review scores and new reviews monthly
- LinkedIn: Follow competitor pages; track job postings
- Crunchbase: Funding alerts for direct and indirect competitors
- Product Hunt: Launches in your category

### Monthly Review Cadence
1. Pull new G2/Capterra reviews for top 3 competitors
2. Check competitor changelog / release notes
3. Review win/loss data from CRM
4. Update feature matrix for any changes
5. Flag to product and sales any material changes

## Battle Card Template

```
## [Competitor Name] Battle Card

**One-line summary**: [What they do and who they serve]

**Their strengths**:
- [Strength 1]
- [Strength 2]

**Their weaknesses**:
- [Weakness 1]
- [Weakness 2]

**When they win**: [Scenario where they beat us]
**When we win**: [Scenario where we beat them]

**Our key differentiators vs them**:
- [Differentiator 1] → Proof point: [customer quote or data]
- [Differentiator 2] → Proof point: [customer quote or data]

**Common objections and responses**:
Q: "Competitor X has feature Y, you don't"
A: [Response]

Q: "Competitor X is cheaper"
A: [Response]

**Pricing comparison**:
| Plan | Us | Them |
|------|----|------|
| Starter | $X | $Y |

**Last updated**: [Date] | **Owner**: [Name]
```

## Win/Loss Analysis Process

### Data Collection
- Sales team tags every closed deal: Won / Lost / No Decision
- Lost deals: sales notes reason (price / feature gap / competitor / timing)
- Win interviews: 15-min call with new customer in first 30 days
- Loss interviews: outreach to lost deals at 90 days post-decision

### Win Interview Questions
1. What alternatives did you evaluate?
2. Why did you ultimately choose us?
3. Was there anything that almost made you choose someone else?
4. What would cause you to switch to a competitor in the future?

### Loss Interview Questions
1. What made you go with [competitor] instead?
2. What did they offer that we didn't?
3. Was there anything we could have done differently?
4. Would you reconsider us in the future? Under what conditions?

### Win/Loss Dashboard
| Metric | Target | Frequency |
|--------|--------|-----------|
| Win rate vs each competitor | Track trend | Monthly |
| Top loss reasons | Rank by frequency | Monthly |
| Competitive deal cycle length | vs non-competitive | Quarterly |
| Feature gaps cited in losses | Rank, inform roadmap | Quarterly |
