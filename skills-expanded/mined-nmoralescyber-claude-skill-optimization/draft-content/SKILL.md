---
name: draft-content
description: Drafts marketing content across channels — blog posts, social media (LinkedIn, Twitter/X, Instagram, TikTok), email newsletters, landing page copy, press releases, and case studies. Make sure to use this skill whenever the user says draft, write, create copy for, compose, or put together any of these formats, even if they don't name "marketing." Includes channel-specific formatting (character limits, CTA placement, subject-line variants), SEO recommendations, headline options, and brand-voice adherence. Do NOT use for: customer-facing replies to support tickets or escalations (use customer-support:draft-response), personalized cold outreach to sales prospects (use sales:draft-outreach), internal stakeholder updates (use product-management:stakeholder-update), or contractual/legal correspondence (use legal:legal-response). Absorbs the deprecated marketing:content-creation skill as of 2026-04-25.
---

# Draft Content

Drafts marketing content across channels with channel-specific formatting, SEO awareness, and brand-voice consistency.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Writing a blog post, social post, newsletter, landing page, press release, or case study | Replying to a specific customer support ticket → `customer-support:draft-response` |
| The audience is broad (prospects, readers, subscribers) | The audience is one named prospect being researched and pursued → `sales:draft-outreach` |
| The goal is awareness, education, or top/mid-funnel conversion | The goal is internal alignment or a status update → `product-management:stakeholder-update` |
| Content goes through marketing review | Content involves contractual or regulatory language → `legal:legal-response` |

## Channel-specific defaults

**Blog posts** — 800-2000 words, H2/H3 hierarchy, target keyword in title + first paragraph + one H2, internal links suggested, meta description ≤160 chars.

**LinkedIn** — Hook in first line (preview cuts at ~210 chars), 3-line whitespace breaks, max 3 hashtags, no external links in body (kills reach — put in first comment).

**Twitter/X** — 280 chars per tweet; threads use numbered prefix (1/, 2/) and consistent formatting; one CTA at end.

**Instagram** — Caption hook in first line, paragraph breaks via blank lines (or invisible characters), 5-15 hashtags grouped at end or in comment.

**TikTok** — Caption ≤150 chars optimal, hook the algorithm with first 3 words.

**Email newsletter** — Subject line A/B variants (one curiosity-driven, one specific-value), preheader ≤90 chars, scannable subheads, single dominant CTA, no more than 3 links.

**Landing page** — Above-fold value prop in 1 sentence, social proof in row 2, single CTA repeated 2-3x, FAQ accordion below fold.

**Press release** — Inverted pyramid, dateline (CITY, Date), boilerplate paragraph at end, 2-3 quotes from named execs, contact info.

**Case study** — Customer logo permission confirmed, structure: Challenge / Solution / Results (with quantified outcome), pull quote from customer.

## Brand voice

If a brand voice guide exists in the workspace (CLAUDE.md, brand.md, or memory), match it. Otherwise extract voice cues from existing published content before drafting. Default voice: clear, direct, evidence-led, no hype words ("revolutionary", "game-changing", "next-gen" are banned unless the brand guide explicitly endorses them).

## Headline / subject line discipline

For every blog post and email, propose 3 headline variants:
1. **Specific + numerical** ("7 SOC 2 controls most startups skip")
2. **Curiosity + question** ("What auditors look for in your access logs (and why most companies miss it)")
3. **Direct value** ("How to pass your SOC 2 Type II in under 6 months")

Let the user pick or A/B test.

## SEO defaults (for blog and landing)

- Primary keyword in title, URL slug, first 100 words, one H2
- 2-3 secondary keywords sprinkled naturally
- Meta description: 150-160 chars, includes primary keyword + value prop + soft CTA
- Internal links: 2-4 to related content
- Suggest schema markup type (Article, FAQPage, HowTo) where relevant

## Compliance hygiene

Flag any draft for review if it contains:
- Performance claims without source ("90% of customers report...")
- Comparisons naming competitors
- Health, financial, or legal advice phrasings
- Customer names or logos without confirmed permission
- Unsubstantiated superlatives ("the best", "the only")

## Output format

Always include:
1. The full draft
2. 3 headline/subject variants
3. Suggested CTA(s) with placement
4. SEO checklist status (where applicable)
5. Compliance flags raised (or "none")
