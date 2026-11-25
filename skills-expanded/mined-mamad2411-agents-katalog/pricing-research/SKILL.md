---
name: pricing-research
description: >
  This skill should be used when the user says "research competitor pricing",
  "what are competitors charging", "pricing intelligence", "competitor scan",
  "market pricing analysis", "how should I price my SaaS", "what's the market
  rate for", "pricing benchmarks", "analyze competitor tiers", "scrape pricing
  pages", "willingness to pay research", "pricing survey design", or any request
  to gather competitive intelligence, benchmark pricing, or understand market
  positioning before setting prices. Also trigger when the user pastes a
  competitor URL and asks about their pricing, or when building a pricing
  strategy from scratch. This is the FIRST skill to use in any pricing
  workflow — research comes before modeling.
version: 0.1.0
---

# Pricing Research Engine

Deep competitive intelligence and market research for SaaS and API gateway pricing. This skill produces the raw research package that feeds into pricing-modeler.

## When to Use This Skill

Run this BEFORE pricing-modeler. Every pricing decision should start with evidence. This skill gathers that evidence from three source layers:

1. **Web intelligence** — competitor pricing pages, G2/Capterra reviews, public API docs
2. **Internal data** — your own analytics, customer segments, usage patterns (Supabase, GA4)
3. **Framework-guided analysis** — structured approaches to willingness-to-pay, value mapping

## Research Workflow

### Phase 1: Define the Pricing Research Scope

Before scraping anything, establish what you're pricing:

1. **Product type**: SaaS platform, API gateway, content delivery, hybrid
2. **Revenue model candidates**: per-seat, usage-based, flat-rate, freemium, outcome-based, hybrid
3. **Target market segment**: SMB, mid-market, enterprise, developer, compliance/GRC
4. **Geography**: US-only, global, specific regions with regulatory implications

For STIGViewer specifically, consider:
- The compliance/GRC SaaS vertical (niche but high-value)
- DoD/defense contractor buyer psychology (risk-averse, procurement-driven)
- API gateway for content automation (developer-facing, usage-sensitive)

### Phase 2: Competitor Intelligence Gathering

#### Direct Competitors (same category, same buyer)
Scrape and analyze pricing pages for direct competitors. For each competitor, capture:

- **Tier names and price points** (monthly/annual)
- **Feature gating** — what's in each tier vs. what's locked
- **Value metric** — what do they charge per? (seat, scan, asset, API call)
- **Free tier details** — limits, restrictions, upgrade triggers
- **Enterprise pricing** — "Contact us" vs. published, what triggers enterprise
- **Add-ons** — premium support, dedicated instances, compliance packages
- **Pricing page UX** — toggle design, comparison tables, FAQ, social proof

Use Apify actors or Claude in Chrome for automated scraping (Chrome handles JS-rendered pricing pages cleanly). Fall back to `WebFetch` for static pages, then manual URL analysis if both fail.

Read `references/competitor-matrix-template.md` for the structured capture format.

#### Adjacent Competitors (different category, overlapping buyer)
Map pricing from adjacent tools the buyer already pays for. This establishes the buyer's existing spend envelope and price anchors.

#### API/Developer Tool Benchmarks
For API gateway pricing specifically, research:
- Per-request pricing tiers (typical ranges by vertical)
- Rate limiting structures
- Authentication/key management pricing models
- Overage pricing mechanics
- Free tier API call limits across the industry

Read `references/api-pricing-patterns.md` for common API pricing models.

### Phase 3: Review Mining

Extract pricing-relevant intelligence from public reviews:
- **G2/Capterra reviews** mentioning "price", "expensive", "value", "ROI", "worth it"
- **Reddit threads** comparing tools in the category
- **Hacker News discussions** about pricing changes in the space
- **Twitter/X complaints** about competitor pricing changes

What to extract:
- Price sensitivity signals ("too expensive for small teams")
- Value perception ("worth every penny because...")
- Feature-price expectations ("at this price I'd expect...")
- Switching triggers ("switched from X because pricing...")

### Phase 4: Internal Data Analysis

When Supabase/analytics access is available, pull:
- **User segments by usage intensity** — what separates power users from casual
- **Feature adoption rates** — which features drive retention vs. which are ignored
- **Usage distribution** — API calls per account, content items per org
- **Churn correlation** — what plan size/type churns most
- **Expansion patterns** — what triggers upgrades

### Phase 5: Willingness-to-Pay Framework

Design a WTP research approach using one or more frameworks:

#### Van Westendorp Price Sensitivity Meter
Four questions to ask prospects/customers:
1. At what price would this be so expensive you wouldn't consider it? (too expensive)
2. At what price would this start to seem expensive but you'd still consider it? (expensive)
3. At what price would this seem like a bargain? (cheap)
4. At what price would this seem too cheap, making you question quality? (too cheap)

Plot the curves to find the acceptable price range and optimal price point.

#### Gabor-Granger Direct Pricing
Show a series of price points and ask "Would you buy at $X?" at each level. Build a demand curve.

#### Conjoint Analysis (Advanced)
If resources allow, design a conjoint study testing feature bundles at different price points to find the highest-value configuration.

For each framework, produce:
- The survey instrument (exact questions)
- Recommended sample size and distribution
- Analysis methodology
- How to interpret results

Read `references/wtp-frameworks.md` for detailed survey templates.

## Output: The Pricing Research Package

Compile everything into a structured deliverable:

```
# Pricing Research Package: [Product Name]
## Date: [date]

## 1. Market Overview
- Category definition and size
- Growth trajectory
- Key players and market share estimates

## 2. Competitor Pricing Matrix
[Structured table from Phase 2]

## 3. Value Metric Analysis
- What competitors charge per (and why)
- Recommended value metric candidates for your product
- Pros/cons of each metric

## 4. Price Range Intelligence
- Lowest price point in market
- Median price point
- Highest price point
- Your recommended positioning zone

## 5. Review & Sentiment Intelligence
- Key themes from review mining
- Price sensitivity signals
- Perceived value drivers

## 6. Internal Usage Patterns
[If data available]

## 7. WTP Research Design
- Recommended framework
- Survey instrument
- Target respondent profile

## 8. Strategic Recommendations
- Recommended pricing model
- Recommended value metric
- Preliminary price range
- Key risks and mitigations
```

Save the research package to `pricing-research-[product]-[date].md`.

## STIGViewer-Specific Context

When researching pricing for STIGViewer products, pay special attention to:
- **STIG/CMMC compliance tool pricing** — Tenable, Rapid7, SteelCloud, SCAP tools
- **GRC platform pricing** — Vanta, Drata, Secureframe, Tugboat Logic
- **Defense contractor procurement** — GSA schedule pricing, contract vehicle implications
- **FedRAMP-adjacent pricing premiums** — what compliance certifications add to price
- **API pricing for security content** — NVD API, MITRE ATT&CK integrations, OSCAL tooling

## Composio fallback — apps with no native MCP

If a step in this skill needs an app or service that has no native Cowork MCP connector — for example Notion, Linear, Jira, HubSpot, Salesforce, Stripe, Airtable, or Calendly — and the Composio connector is installed, reach the app through Composio's Tool Router rather than giving up or asking the user to do it by hand. Discover the tool with `COMPOSIO_SEARCH_TOOLS`, authenticate with `COMPOSIO_MANAGE_CONNECTIONS` if needed, then execute. See the `composio` plugin's `composio-tools` skill for the full pattern.

Native MCP connectors still come first — this is a fallback for reach, not a replacement for the native paths this skill already uses.
