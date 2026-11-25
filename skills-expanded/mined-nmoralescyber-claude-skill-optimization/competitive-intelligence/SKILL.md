---
name: competitive-intelligence
description: Generates an interactive HTML battlecard artifact (clickable competitor cards, comparison matrix, talking points) optimized for live sales-call use. Make sure to use this skill whenever the user says give me a battlecard, build a battlecard for [competitor], how do we win against [competitor], what's new with [competitor], prep me for a deal where [competitor] is in play, or asks for competitive intel in a sales context. The output is a self-contained HTML file the user can keep open during calls. Do NOT use for: marketing positioning and messaging analysis (use marketing:competitor-positioning-brief), product feature parity matrix and roadmap analysis (use product-management:competitor-feature-analysis), one-prospect company research (use sales:account-research), or generic web research without the sales-battlecard output format (use raw web search).
---

# Competitive Intelligence

Builds an interactive HTML battlecard artifact for live sales-call use.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Sales needs a clickable battlecard for live calls | Marketing wants positioning analysis → `marketing:competitor-positioning-brief` |
| Output format needs to be a self-contained HTML artifact | PM wants feature parity matrix → `product-management:competitor-feature-analysis` |
| Includes talking points, objection handlers, win/loss patterns | Researching one prospect company → `sales:account-research` |
| Used in deals where the competitor is named | Just want a written brief, no interactive output |

## Battlecard structure (HTML output)

The artifact contains:

1. **Tab nav** — One tab per competitor (clickable to switch).

2. **Per-competitor card**
   - Logo + one-line positioning
   - Pricing model & approximate ranges
   - Strengths (be honest — sales loses credibility with weak strawman lists)
   - Weaknesses (verifiable, with sources)
   - Recent moves (last 90 days: launches, layoffs, funding, exec changes)
   - When they win against us (deal patterns, segments)
   - When we win against them (deal patterns, segments)
   - Common objections sales hears + recommended responses
   - Discovery questions to ask the prospect to identify which competitor they're seriously considering

3. **Comparison matrix** — Cross-competitor view, key dimensions only (5-8 rows max for readability).

4. **Recent intelligence feed** — Date-stamped items: "Acquired X on date", "Released Y feature on date", "Lost Z customer (per LinkedIn post on date)".

## Research depth

Sales battlecards are time-sensitive. Refresh every 90 days at minimum. Sources in priority:

1. Recent G2/Capterra reviews (last 6 months only)
2. LinkedIn posts from competitor's customers and ex-employees
3. Press releases and funding news (last 12 months)
4. Public job postings (current quarter)
5. Win/loss interviews from your own org (if connected)
6. Their pricing & docs pages

## Output

A single self-contained `.html` file that:
- Opens in any browser
- Works offline (all assets inlined)
- Has print-friendly CSS for one-pager backup
- Includes a "last updated" stamp
