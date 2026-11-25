---
name: market-competitors
description: Competitor intelligence scan covering positioning, pricing, messaging, social proof, and historical evolution via Wayback Machine. Invoke whenever the user says "competitors", "competitive analysis", "how do we stack up", "alternatives to", or runs `/market competitors <url>`. Produces COMPETITOR-ANALYSIS.md with a side-by-side matrix and specific differentiation plays.
---

# Market Competitors — Competitive Intelligence

Identify 3–5 relevant competitors, analyze their public-facing marketing, and tell the client where to attack and where to defend.

## Step 1 — Identify competitors

Sources in order:
1. Ask the user if they already have a list.
2. Run `scripts/analyze_page.py` on the client's homepage for vocabulary.
3. Use `WebSearch` for: `"<brand> vs"`, `"<brand> alternatives"`, `"best <category>"`, `"<primary keyword> tools"`.
4. Pick the top 3–5 competitors that are **actually competing for the same user**, not just in the same category.

State your selection and why before running the analysis.

## Step 2 — Scan each competitor

Run `python3 scripts/competitor_scanner.py <url>` on each (or use `analyze_page.py` if the scanner errors). For each competitor capture:

| Field | Source |
|---|---|
| Hero headline | H1 or first large text |
| Subhead / value prop | Paragraph under H1 |
| Primary CTA text | Most prominent button |
| Pricing (if visible) | Pricing page |
| Social proof | Logos, counts, reviews, testimonials |
| Positioning archetype | See below |
| Content cadence (if blog) | Last 3 post dates |
| Tech/tracking stack | Scripts detected |

## Step 3 — Historical evolution (Wayback Machine)

For the client and each competitor, fetch:
```
https://web.archive.org/web/2023*/<competitor-url>
https://web.archive.org/web/2024*/<competitor-url>
```

Compare the 2023 hero to the 2025 hero. Has their positioning shifted? Did they pivot? This is often where you spot pricing changes, audience pivots, or abandoned features. (Skip gracefully if the Wayback Machine fails.)

## Step 4 — Positioning matrix

Plot every competitor plus the client on a 2×2 (pick the two most relevant axes for the category):

- SaaS: Simplicity ↔ Power × Price
- E-com: Premium ↔ Value × Niche ↔ Mass
- Agency: Specialist ↔ Generalist × Boutique ↔ Enterprise
- Creator: Entertainment ↔ Education × Broad ↔ Niche

## Step 5 — Comparison matrix

| | **Client** | Comp A | Comp B | Comp C |
|---|---|---|---|---|
| One-liner | | | | |
| Target audience | | | | |
| Price anchor | | | | |
| Primary CTA | | | | |
| Social proof | | | | |
| Key differentiator | | | | |
| Weakness | | | | |

## Step 6 — White space analysis

Answer these explicitly:
1. **What does every competitor claim?** (table stakes — the client must match these)
2. **What does no competitor own?** (white space — the client should claim this)
3. **Where is the client's current position ambiguous or overlapping?** (risk)
4. **Which competitor is most vulnerable, and why?** (attack opportunity)

## Step 7 — Differentiation plays

Give 3–5 concrete plays. Each play has: the claim, the evidence needed to back it, and the channel to land it in.

**Example:**
> **Claim:** "Set up in 90 seconds — the fastest onboarding in category."
> **Evidence needed:** Timed onboarding video, signed testimonials, comparison table.
> **Channel:** Hero H1, G2 category page, paid search ads targeting competitor brand terms.

## Output: COMPETITOR-ANALYSIS.md

```markdown
# Competitive Analysis — [Client]
**Date:** [YYYY-MM-DD]
**Competitors analyzed:** [A, B, C, ...]

## Market Snapshot
[2-3 sentences: category health, dominant positioning, where the client sits.]

## Positioning Matrix
[ASCII or described 2x2 with competitor placement]

## Comparison Matrix
[Full table]

## Competitor Deep Dives
### [Competitor A]
- URL, positioning, pricing, audience
- Strengths
- Weaknesses
- Historical shift (Wayback): [brief note or "no significant change"]

... repeat for each ...

## White Space
1. **Unclaimed:** [opportunity]
2. **Overclaimed:** [where everyone sounds the same]
3. **Vulnerable competitor:** [who and why]

## Differentiation Plays
1. **[Play]** — evidence needed, channel, expected outcome
...

## Recommendations
### This week
### This quarter
```

## Quality Bar

- Never invent competitor pricing, headcount, or revenue. If you can't verify it, don't cite it.
- Quote actual headlines and CTAs so the client can audit your work.
- Avoid the "they're strong in X, weak in Y" generic framing — name the specific page, page element, or campaign.
- If the client is clearly stronger than all competitors, say so and focus on how to widen the lead.
