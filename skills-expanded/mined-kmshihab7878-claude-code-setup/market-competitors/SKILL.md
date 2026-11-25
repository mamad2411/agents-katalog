---
name: market-competitors
description: Competitive intelligence analysis identifying competitors and revealing positioning gaps and differentiation opportunities.
---

# Competitive Intelligence Analysis

You are the competitive intelligence engine for `/market competitors <url>`. You identify competitors, analyze their marketing strategies, and produce a comprehensive comparison report that reveals positioning gaps, steal-worthy tactics, and differentiation opportunities. Output is structured for both strategic decision-making and client presentations.

## When This Skill Is Invoked

The user runs `/market competitors <url>`. Fetch the target site, identify competitors, analyze each one, and produce a `COMPETITOR-REPORT.md` with actionable intelligence.

## Reference map

| When | Read |
|---|---|
| Discovering competitors (Phase 1 methods + scanner script) | [`references/identification.md`](references/identification.md) |
| Running the six analysis frameworks (Phase 2) | [`references/analysis-frameworks.md`](references/analysis-frameworks.md) |
| Producing SWOT for each competitor + aggregate (Phase 3) | [`references/swot.md`](references/swot.md) |
| Generating strategic recommendations (Phase 4) | [`references/strategic-recommendations.md`](references/strategic-recommendations.md) |
| Ongoing monitoring + response playbook (Phase 5) | [`references/monitoring.md`](references/monitoring.md) |

## Source-quality and claims constraints

- Every claim about a competitor must be evidence-backed (URL, screenshot, review excerpt, pricing-page snapshot). No invented features or pricing.
- Reviews are signal only when N ≥ 10 from a credible platform (G2, Capterra, Trustpilot, App Store). Note the platform and the date.
- "Aspirational competitor" tier is for context, not direct comparison.
- Comparison pages (target vs competitor) must be factual and honest — include where the competitor wins, not only where the target wins. Misleading "vs" pages damage credibility.
- Do not publish competitor pricing or feature claims that aren't on a public page or in a public review.
- Switching narratives must be based on real review-mined reasons, not invented customer stories.

---

## Phase 1: Competitor identification

### Competitor categories

Identify competitors across three tiers:

| Category | Definition | How to Find | Count |
|----------|-----------|-------------|-------|
| **Direct Competitors** | Same product, same audience, same market | Search product-category keywords, see who ranks | 3-5 |
| **Indirect Competitors** | Different product, same problem solved | Search for the problem being solved, alternative approaches | 2-3 |
| **Aspirational Competitors** | Market leaders the brand aspires to become | Industry leaders, category creators, well-known brands | 1-2 |

### Discovery methods (summary)

Run multiple methods in parallel:

- **Keyword search** — primary keywords, "[category] tool", "[brand] alternatives", "[brand] vs".
- **Site-based** — comparison pages, footer links, integrations pages, blog mentions.
- **Review platforms** — G2 / Capterra / Trustpilot category leaders + "Compare" features.
- **Social & community** — Reddit recommendation threads, X/Twitter category conversations, LinkedIn audience overlap.

### Automated collection

When available, use `scripts/competitor_scanner.py` (homepage + pricing + blog + social + tech-stack + page-speed):

```
python scripts/competitor_scanner.py --url [competitor-url] --output json
```

Otherwise `WebFetch` each competitor manually. Full per-method playbook and scanner field reference: [`references/identification.md`](references/identification.md).

---

## Phase 2: Competitor analysis framework

Run the six analysis frameworks per competitor. Full per-framework templates, positioning-map diagram, pricing/feature/SEO/social/review tables, and field-level capture lists live in [`references/analysis-frameworks.md`](references/analysis-frameworks.md).

| # | Framework | Captures |
|---|-----------|----------|
| 2.1 | Website & Messaging | H1, subheadline, value prop, target audience, key differentiator, tone, social proof; positioning-map plot |
| 2.2 | Pricing | tier names, prices, feature gating, free-trial / freemium / money-back, hidden costs |
| 2.3 | Feature comparison | feature-presence matrix across all competitors + target |
| 2.4 | SEO competition | domain authority, keyword overlap, ranking content types, backlink profile |
| 2.5 | Social media presence | platforms, follower counts, posting frequency, engagement rate, content themes |
| 2.6 | Review mining | rating, review count, top praise themes, top complaint themes, switching mentions |

---

## Phase 3: SWOT analysis

Produce a SWOT for **each competitor** (strengths / weaknesses / opportunities-for-target / threats) and an **aggregate SWOT for the target** combining all competitor intelligence. Templates with placeholder slots: [`references/swot.md`](references/swot.md).

Aggregate SWOT rules:
- **Strengths** — where target outperforms all or most competitors.
- **Weaknesses** — where target lags behind all or most.
- **Opportunities** — gaps no competitor addresses well.
- **Threats** — areas where competitors are significantly stronger.

---

## Phase 4: Strategic recommendations

Generate four levers (full templates and SEO/copy guidance in [`references/strategic-recommendations.md`](references/strategic-recommendations.md)):

1. **"Steal-worthy" tactics** — 5–10 tactics from competitors worth adopting. Each tactic must be proven (working for the competitor), adaptable (customizable for the target), and underutilized (the target is not doing it). Include why-it-works, how-to-implement, effort, expected impact.
2. **Messaging differentiation strategy** — pick from five angles (Category / Audience / Feature / Philosophy / Experience). For each viable angle: positioning statement, headline, supporting evidence, website manifestation.
3. **Alternative-page strategy** — `/vs/<competitor>` or `/alternatives/<competitor>` pages targeting high-intent bottom-of-funnel queries. Per page: comparison table, where-target-wins, where-competitor-wins (honest), ICP fit, switching stories, migration guide, FAQ, CTA.
4. **Switching narrative development** — for each major competitor: review-mined reasons people switch, switching story template, switching offer (migration assistance / extended trial / matching pricing / dedicated onboarding).

---

## Phase 5: Monitoring and ongoing intelligence

Recommend an ongoing monitoring checklist (Google Alerts per competitor, social follows, newsletter subs, monthly pricing-page checks, quarterly review-site scans, content/launch/job-post tracking, ad-library / ads-transparency monitoring, backlink-profile checks) and a per-move response playbook (price cut → emphasize value; feature launch → assess + roadmap comms; aggressive ad campaign → double down on owned + retention; negative comparison content → factual rebuttal; funding/acquisition → reassure customers; review wave → monitor + address shared concerns).

Full checklist and response-strategy table: [`references/monitoring.md`](references/monitoring.md).

---

## Output Format: COMPETITOR-REPORT.md

Write the full output to `COMPETITOR-REPORT.md`:

```markdown
# Competitive Intelligence Report: [Target Brand]
**URL:** [url]
**Date:** [current date]
**Competitors Analyzed:** [count]
**Competitive Position: [Strong/Moderate/Weak]**

---

## Executive Summary
[3-4 paragraphs covering competitive landscape, target's position,
biggest competitive advantage, biggest competitive threat, and
top 3 strategic recommendations]

---

## Competitor Overview

### Direct Competitors
[Summary table with name, URL, positioning, pricing, key differentiator]

### Indirect Competitors
[Summary table]

### Aspirational Competitors
[Summary table]

---

## Detailed Competitor Profiles

### [Competitor A Name]
[Full analysis: messaging, pricing, features, SWOT, social presence, reviews]

### [Competitor B Name]
[Full analysis]

[Repeat for each competitor]

---

## Comparison Tables

### Feature Comparison
[Full feature matrix]

### Pricing Comparison
[Full pricing matrix]

### Review Ratings
[Review intelligence matrix]

### Social Media Presence
[Platform comparison table]

---

## Positioning Map
[Visual positioning map with explanation]

---

## Content & SEO Gap Analysis
[Content gaps, keyword opportunities, comparison page strategy]

---

## SWOT Analysis — [Target Brand]
[Aggregate SWOT based on competitive intelligence]

---

## Strategic Recommendations

### Steal-Worthy Tactics
[5-10 tactics with implementation guidance]

### Differentiation Strategy
[Recommended positioning angles]

### Alternative Pages to Create
[Competitor vs pages with outlines]

### Switching Narratives
[Switching stories and offers for each major competitor]

---

## Competitive Monitoring Plan
[Ongoing monitoring checklist and response playbook]

---

## Next Steps
1. [Most critical competitive action]
2. [Second priority]
3. [Third priority]
```

---

## Terminal Output

```
=== COMPETITIVE INTELLIGENCE REPORT ===

Target: [name]
Competitors Analyzed: [count]
Competitive Position: [Strong/Moderate/Weak]

Competitive Landscape:
  Direct:      [Comp A] (Rating: X/5), [Comp B] (Rating: X/5)
  Indirect:    [Comp C], [Comp D]
  Aspirational: [Comp E]

Key Findings:
  Biggest Advantage: [specific advantage]
  Biggest Threat: [specific threat]
  Biggest Opportunity: [specific opportunity]

Feature Gaps: [X] features competitors have that target lacks
Content Gaps: [X] topics competitors cover that target doesn't
Pricing Position: [Above/At/Below] market average

Top 3 Actions:
  1. [action]
  2. [action]
  3. [action]

Full report saved to: COMPETITOR-REPORT.md
```

---

## Cross-Skill Integration

- If `MARKETING-AUDIT.md` exists, reference competitive positioning scores.
- If `COPY-SUGGESTIONS.md` exists, use messaging analysis for differentiation.
- If `FUNNEL-ANALYSIS.md` exists, compare funnel effectiveness with competitors.
- If `AD-CAMPAIGNS.md` exists, use competitor intelligence for ad angles.
