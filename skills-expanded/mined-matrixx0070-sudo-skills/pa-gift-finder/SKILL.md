---
name: pa-gift-finder
version: 1.0.0
description: Find a thoughtful, well-matched gift given a person, an occasion, and a budget.
author: matrixx0070
tags: [gifts, shopping, occasions, recommendations, personal-assistant]
capabilities: []
---

## When to use

Use this when the owner needs a gift and wants ideas matched to a specific person, occasion, and budget — not generic bestseller lists. Good for birthdays, anniversaries, thank-yous, and "I have no idea what to get them."

**Not for:** bulk corporate gifting logistics, purchasing on your own, or gifts that require the recipient's private data you do not have. You recommend; the owner buys.

## Method

1. Build a recipient profile: relationship to owner, interests/hobbies, recent life events, things they already own or mentioned wanting, and any dislikes/allergies/values (e.g. vegan, minimalist).
2. Pin the occasion and its tone (romantic, celebratory, sympathy, casual) and the firm budget ceiling.
3. Decision point — is the profile thin? Ask 2-3 targeted questions (a hobby, a recent complaint they voiced, sizes) rather than guessing generically.
4. Generate 5-7 candidates spanning a range: one safe, one experiential (not an object), one personalized/handmade, one splurge-at-cap, one wildcard.
5. For each, give a one-line "why it fits this person" tied to the profile — the thoughtfulness lives here.
6. Decision point — any candidate risky (sizing, taste, duplicate)? Add a safer fallback or pair with a gift receipt note.
7. Note delivery timing vs the occasion date. Confirm before purchasing or messaging any vendor — buying spends money.

## Example

Input: sister, 30th birthday, loves hiking + started pottery, dislikes clutter, budget $80.
Ideas: (1) experience — local pottery studio class $65 (fits new hobby, no clutter); (2) merino hiking socks 2-pack $45 (used, not stored); (3) personalized trail map print of her favorite hike $70; (4) splurge — insulated trail flask $75; (5) wildcard — pottery tool kit $30. Pick one and I will prep the order for your approval.

## Pitfalls

- Generic bestsellers untied to the person; the whole value is the personal fit.
- Ignoring stated dislikes (clutter, allergies, values) — a mismatch reads as careless.
- Forgetting delivery lead time; a perfect gift arriving late fails the occasion.
- Buying or contacting a vendor on your own. Confirm before any purchase.

## Output format

```
GIFT IDEAS — for [recipient] — [occasion] — budget [cap]

Profile used: [interests, recent events, dislikes]

1. [idea] — $[x] — why it fits: [one line]
2. ...
(range: safe / experience / personalized / splurge / wildcard)

FALLBACK if unsure: [safer pick] (+ gift receipt)
TIMING: order by [date] to arrive for [occasion]

Next: pick one and reply APPROVE — I prep the order, you complete purchase.
```
