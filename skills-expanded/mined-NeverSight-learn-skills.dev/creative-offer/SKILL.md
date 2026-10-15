---
name: creative-offer
description: Build visuals that sell a specific offer and value proposition. Translates an offer (price, bundle, guarantee, bonus, deadline) into hero visuals that make the value legible at a glance. Use when the user says "visualize the offer", "promo creative", "make the deal look good", "value prop hero", or has a concrete offer to merchandise. Part of the Creative Production set.
---

# Creative — Offer Explorer

Make the OFFER the hero. Every visual decision serves one goal: a viewer understands the value and the reason to act *now* within two seconds. This is merchandising, not branding — clarity of value beats aesthetic flourish.

## When to use
- There's a concrete offer to push: discount, bundle, free trial, guarantee, limited drop.
- Promo/sale creative, pricing-page hero, launch banner, email header.
- The message is "here's the deal", not "here's who we are".

## When NOT to use
- Testing many message angles broadly → `creative-ads-explorer`.
- No offer yet, just brand look → `creative-explore`/`creative-moodboard`.
- Showing the product in use → `creative-scene`.

## Inputs (ask only what's missing — and never invent these)
- **The exact offer**: anchor price → deal price, what's included, bonus, guarantee terms, deadline.
- **Product + audience**.
- **Locked visual direction** if available.

If any number or term is unknown, ASK. Fabricating a price or guarantee is a hard fail.

## Workflow
1. **Decompose the offer into value units**: anchor vs deal price, bundle items (count matters — visible items = perceived stack), guarantee, bonus, urgency cue.
2. **Pick a merchandising layout** per concept: stacked-value, bundle-flatlay, before/after-value, guarantee-forward, countdown-urgency, price-anchor-strikethrough.
3. **Write 3-5 concepts**: headline (the offer in ≤8 words), visual prompt, the value cue it leans on, CTA.
4. **Generate** with your image tool. Keep any price/tagline text crisp and legible at thumbnail size; pass it verbatim. Save to `./creative/offer/<concept>.png`.
5. **Rank by clarity-of-value** and recommend the clearest.

## Worked example
Offer: course bundle, normally $400, now $149, +free templates, 30-day guarantee, ends Friday.
```
## Concept "Stacked Value"
headline: "$400 of training — yours for $149"
visual: vertical stack of 4 module cards + "BONUS: templates" tab, strikethrough $400 → $149
value cue: anchor contrast makes the discount feel large
CTA: Get the bundle
[ref: ./creative/offer/stacked-value.png]

## Concept "Guarantee-Forward"
headline: "Love it or your money back"
visual: bold 30-day badge center, course thumbnail behind, calm palette
value cue: removes risk → lowers purchase friction
CTA: Try risk-free
[ref: ./creative/offer/guarantee.png]
```
Recommendation: "Stacked Value" for cold traffic (value clarity); "Guarantee" for warm/hesitant. → winners to `creative-polish`.

## Quality bar
- A stranger grasps *what they get* and *why now* in under 2 seconds.
- Every price/term on screen is real and matches what the user provided.
- Text is legible at the size it'll actually be seen (thumbnail/feed).
- The value cue is deliberate (anchoring, risk-reversal, scarcity) — not decoration.

## Common pitfalls
- **Inventing numbers** — prices, discounts, guarantee terms come only from the user. Flag gaps.
- **Cluttered hero** — too many value units competing; lead with one, support with the rest.
- **Illegible price text** — the most important element rendered too small or low-contrast.
- **Urgency without basis** — don't add a fake deadline; only show one the user confirmed.

## Handoff
Winning concepts → `creative-polish` for production finish. Keep brand consistency via the `creative-explore` stub.

## Tooling
Needs a text-to-image tool. Without one, deliver concepts (headline + layout + visual prompt + value cue + CTA) for the user to render.
