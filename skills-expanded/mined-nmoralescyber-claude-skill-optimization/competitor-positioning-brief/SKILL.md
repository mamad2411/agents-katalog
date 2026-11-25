---
name: competitor-positioning-brief
description: Produces marketing-focused competitor positioning analysis — messaging pillars, value propositions, brand voice, content angles, and positioning gaps where the user can claim unowned territory. Renamed from marketing:competitive-brief on 2026-04-25 to resolve a name collision with product-management:competitive-brief (now product-management:competitor-feature-analysis). Make sure to use this skill whenever the user says position against [competitor], find positioning gaps, claim unowned messaging territory, audit a competitor's content/messaging, build a sales battlecard from a positioning angle, or asks how do we differentiate the message from [competitor]. Do NOT use for: feature-by-feature product comparison or roadmap analysis (use product-management:competitor-feature-analysis), interactive HTML battlecard generation for sales calls (use sales:competitive-intelligence), SEO keyword overlap analysis (use marketing:seo-audit), or one-prospect account research (use sales:account-research).
---

# Competitor Positioning Brief

Marketing-focused competitor analysis: messaging, voice, content angles, and positioning gaps.

## Rename note

This skill was previously named `marketing:competitive-brief`. Renamed on 2026-04-25 to resolve a name collision with `product-management:competitive-brief` (which is now `product-management:competitor-feature-analysis`). The old name still routes here for backward compatibility but new prompts should use the new name.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Analyzing a competitor's messaging, value prop, brand voice | Comparing product features or roadmaps → `product-management:competitor-feature-analysis` |
| Finding positioning angles competitors haven't claimed | Building an HTML battlecard for live sales calls → `sales:competitive-intelligence` |
| Auditing competitor content (blog, social, ads) for themes | Analyzing keyword/SEO overlap → `marketing:seo-audit` |
| Building messaging differentiation strategy | Researching one named prospect for outreach → `sales:account-research` |

## Output structure

Every positioning brief produced includes:

1. **Competitor snapshot** — Company, market position, target ICP, recent funding/leadership signals.

2. **Messaging pillars** — The 3-5 themes they consistently emphasize. With direct quotes from their site, ads, social.

3. **Brand voice analysis** — Tone, register, vocabulary patterns. ("Authoritative-friendly with technical proof points" vs. "Casual, founder-led, vulnerable").

4. **Content engine assessment** — What channels they invest in, posting cadence, top-performing post themes, content gaps in their library.

5. **Positioning territory map** — Visual or table showing claimed territories (their pillars), contested territories (you both claim), and unclaimed territories (positioning whitespace).

6. **Recommended positioning move** — The specific angle the user can take that competitor doesn't / can't credibly own. With supporting message variations.

7. **Battlecard insert** — 3-5 talking points sales can use when prospects mention this competitor (focused on positioning, not feature parity — that's `competitor-feature-analysis`).

## Research sources (in priority order)

1. Competitor's own site (homepage, About, Pricing, customer pages)
2. Recent press releases and funding announcements
3. Founder/exec social presence (LinkedIn especially)
4. G2/Capterra reviews — what customers say in their words
5. Earnings calls / 10-Ks (if public)
6. Job postings — what they're hiring for signals strategy
7. Conference talks and podcast appearances

## Output deliverables

- Markdown brief (the structured output above)
- One-page positioning canvas (visual, optional but recommended for deck use)
- Suggested next action (e.g., "Run `marketing:campaign-plan` to operationalize the unclaimed territory move")
