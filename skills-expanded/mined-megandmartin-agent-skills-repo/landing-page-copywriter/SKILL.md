---
name: landing-page-copywriter
description: Writes full landing-page copy under AIDA discipline — hero with 3 headline variants, problem, proof, offer, objection handling, and one CTA repeated down the page; conversion-focused, never clever-for-clever's-sake. Use when the user asks to "write landing page copy", "sales page", "homepage copy", "hero headline", or "copy for my offer page". Don't use for ranking-oriented blog articles — that's seo-blog-writer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Landing Pages, Copywriting, Conversion, AIDA]
    related_skills: [seo-blog-writer, email-nurture-sequence, brand-voice-guardian, case-study-builder]
---

# Landing Page Copywriter

Produces a complete page of copy where every section moves one visitor toward one action. AIDA runs the structure (Attention → Interest → Desire → Action), proof outweighs adjectives, objections get answered before they're asked, and the same single CTA repeats until it's the obvious next step. Clever that doesn't convert gets cut.

## When to Use

- The user needs copy for a landing page, sales page, waitlist page, or homepage with one primary action.
- Existing page copy converts poorly and needs a rewrite against AIDA.
- The user asks for "headline options", "hero copy", or "objection handling section".
- **Not for:** SEO blog articles (`seo-blog-writer`), email sequences that warm people up before the page (`email-nurture-sequence`), or sourcing the customer proof itself (`case-study-builder` produces it; this skill deploys it).

## Quick Reference

| Action | Rule |
|---|---|
| One page, one CTA | A single action, repeated 3–5× verbatim; secondary links only in footer |
| Hero headline | 3 variants: outcome-led, pain-led, proof-led — each ≤12 words |
| Proof | Real numbers, named customers, or quotes only; no proof available → say so, never invent |
| Objections | List top 3–5 real objections; each answered in copy, not dodged |
| Clever test | If a line needs a beat to "get it", replace with the clear version |
| Reading level | Hero and CTA readable in one pass; no jargon the visitor didn't bring |

## Procedure

1. **Gather** — confirm before writing: the offer (what, price/commitment), the one action (buy/book/join), the audience and their current alternative, 3–5 real objections (ask "why do interested people not buy?"), and available proof (numbers, quotes, logos, case studies). Proof missing → mark `[PROOF NEEDED]` slots; never fabricate testimonials or stats.
2. **Write the hero (Attention)** — 3 headline variants: (a) outcome-led ("Ship your product in 30 days"), (b) pain-led (names the frustration), (c) proof-led (leads with the number). Each ≤12 words, each paired with one subhead that adds the mechanism, plus the CTA button text (2–4 words, verb-first). Recommend one variant and say why.
3. **Problem section (Interest)** — describe the visitor's situation in their words (from step 1 inputs), sharp enough that they think "that's me". No product mention yet; agitate honestly, don't catastrophize.
4. **Proof + offer (Desire)** — introduce the offer as the turn: what it is, how it works in 3 steps, then stack proof — strongest first. Real quotes verbatim with names/roles; numbers with context. Every `[PROOF NEEDED]` slot lists exactly what asset would fill it.
5. **Objections** — one short block per objection from step 1 (FAQ format or inline). Answer directly; where the honest answer is "this isn't for you if X", write that — it strengthens everything else.
6. **Action** — closing CTA section: restate outcome, the CTA verbatim, and one risk-reversal line if it truly exists (guarantee, free tier, cancel-anytime). CTA text identical everywhere on the page — count occurrences.
7. **Clever audit + deliver** — reread every line: any pun, wordplay, or vague-but-pretty phrase that a distracted visitor wouldn't instantly parse gets replaced with the plain version. Assemble the Output Template.

## Output Template

```
# Landing Page Copy: [Offer]
**One action:** [CTA text, verbatim] | **Audience:** [who] | **Recommended headline:** [a/b/c + why]

## Hero
H1 variants: A) [outcome] B) [pain] C) [proof]
Subhead: ... | CTA button: [text]

## Problem
[2–4 short paragraphs in the visitor's words]

## How it works
1) ... 2) ... 3) ...

## Proof
[quotes verbatim + numbers with context, or [PROOF NEEDED: asset]]

## Objections
**"[objection]"** — [direct answer]  (×3–5)

## Final CTA
[outcome restated] → [CTA text] | Risk reversal: [line or omit]
```

## Pitfalls

- **Clever headline, unclear offer** — the hero wins applause and the visitor can't say what's sold. Recovery: apply the "stranger test" — could someone state the offer after reading only H1+subhead? No → outcome-led variant becomes the recommendation.
- **Invented social proof** — a plausible testimonial appears because the section felt empty. Recovery: strip anything the user didn't supply; ship `[PROOF NEEDED]` slots with a list of the exact assets to collect — an honest gap beats a fake quote.
- **CTA drift** — "Get started", "Try it free", and "Join now" all on one page. Recovery: pick one phrasing in step 1 and search-replace; every button reads identically.
- **Objections dodged** — the price objection gets a vibe ("incredible value") instead of an answer. Recovery: rewrite each objection block to pass "would a skeptic feel answered?"; anchor price against the alternative's cost or admit the fit boundary.
- **Feature-dump Desire section** — a spec list where the payoff should be. Recovery: rewrite each feature as "so you can [outcome]"; any feature without a "so you can" gets demoted or cut.

## Verification

- [ ] Exactly one CTA phrasing; appears 3–5×, verbatim (counted)
- [ ] 3 hero variants present (outcome / pain / proof), each ≤12 words, one recommended with rationale
- [ ] Every proof element is user-supplied or an explicit `[PROOF NEEDED]` slot — zero invented quotes/stats
- [ ] Each objection from step 1 has a direct answer in the copy
- [ ] AIDA order intact: attention → interest → desire → action, no section out of role
- [ ] Clever audit done: no line requires a second read to parse
