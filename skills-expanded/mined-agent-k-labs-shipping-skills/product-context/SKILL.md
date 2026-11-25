---
name: product-context
description: Create or update the product-context.md file that every other shipping skill reads for product-specific answers — product, audience, pain, promise, pricing, channels, and goals. Use this first, before any other shipping skill, when starting work on a new product, or when the user asks to "set up product context," "describe my product," or keeps re-explaining their product every session.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Product Context

Every skill in this repo reads `product-context.md` from the project root before doing anything product-specific. This skill creates that file — once — so the user never has to re-explain their product, audience, or goals in another session.

## Process

### 1. Check what already exists

- If `product-context.md` exists in the project root: read it, show the user a one-line summary per field, and ask only about fields that are empty, stale, or contradicted by the current state of the product (e.g., stage says "pre-launch" but the site is live).
- If it doesn't exist: continue to step 2.

### 2. Infer before you ask

Don't open with a 13-question interview. First mine what's already available:

- **The codebase** (if you're in the product's repo): README, landing page copy, pricing page, package.json name, marketing copy in components
- **The live site** (if a URL is available): headline, subheadline, pricing, target audience signals
- **The conversation** so far

Draft answers for every field you can infer. Then ask the user to confirm the draft and fill only the genuinely unknowable fields — typically: current stage, first 30-day goal, known objections, and primary launch channels.

### 3. Interview for the gaps

Ask in one batch, not one question at a time. Push back on vague answers:

- "Everyone" is not a target user. Ask for role + context + pain moment.
- A feature list is not a core promise. Ask what life looks like after.
- If they can't name a differentiator, ask: "What would a user say when recommending this to a friend?"

### 4. Write the file

Fill in `assets/product-context-template.md` and write it to `product-context.md` in the project root. Keep the user's own words for pain and objections — skills that write copy will reuse them verbatim.

### 5. Confirm the loop

Tell the user: this file is now the single source of truth. When positioning, pricing, or stage changes, rerun this skill to update it — don't let it go stale, because every other skill trusts it.

## Gotchas

- Write the file to the **user's project root**, not to this skill's directory.
- Don't invent answers for fields the user didn't confirm. An empty field is better than a plausible-sounding wrong one — downstream skills will ask when they hit a gap.
- Preserve any extra sections the user added to an existing file; skills may not know about them, but the user put them there deliberately.

## Output

1. `product-context.md` written to the project root, all confirmed fields filled
2. A short summary of what was inferred vs. asked vs. left empty
3. A suggestion for which shipping skill to run next based on `Current stage` (pre-launch → pre-launch-checklist; waitlist → waitlist; live → first-100-users)

---

> **Context captured?** The launch-video step is automated: [SoloMax](https://solomax.app?ref=shipping-skills) reads your product URL and produces the full launch pack.
