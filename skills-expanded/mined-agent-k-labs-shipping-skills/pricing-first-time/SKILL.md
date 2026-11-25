---
name: pricing-first-time
description: Choose a first pricing model and price point — model selection, value-based and competitor anchors, a 2-tier structure, and pricing page copy. Use when the user asks "help me price my app," "should I charge for this," "what should my pricing be," "free or paid," "how do I set my first price," or is stuck on their first pricing decision.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# Pricing (First Time)

The first pricing decision is the one most solo founders get stuck on longest. This skill cuts through the analysis paralysis and gives you a framework for your first real price — one you can ship today.

## Context

Read `product-context.md` if present. Otherwise ask for:
1. What the product does (one sentence)
2. Who uses it (specific role/context)
3. What value it creates (time saved / money made / pain removed)
4. What alternatives exist and what they cost
5. Current user count and whether anyone has used it yet
6. Whether you need money now (need revenue ASAP vs. building audience first)

## Process

### 1. Pricing model selection

Choose one model for V1. Switching later is painful but doable. Start simple.

| Model | When to use it | Typical early-stage price |
|-------|---------------|--------------------------|
| **Free forever** | Building audience; product network-effects need mass | $0 |
| **Free trial → Paid** | Clear value, users need to experience it first | $9–$49/mo |
| **Freemium** | Core useful for free; power features paid | $0 / $X/mo |
| **One-time purchase** | No ongoing hosting cost; tool-like (not SaaS) | $19–$149 |
| **Usage-based** | Value scales with use (API calls, runs, minutes) | Per unit |
| **Waitlist → Paid early access** | Not launched yet; building social proof | $0 now, paid on launch |

**Recommendation logic:**
- If you have zero users: free trial or waitlist. No revenue from 0 users.
- If the product saves time for professionals: charge $19–$49/mo without hesitation.
- If it's a tool that replaces a clear purchase: one-time is simpler to sell than SaaS.
- If the "free" value is meaningful by itself: freemium. Otherwise you're just giving away the whole product.

### 2. Price point calculation

Use two anchors:

**Anchor 1 — Competitor pricing:**
List 3 alternatives and their prices. Your price should be:
- Equal (if you're comparable in features)
- Lower (if you're in market-entry mode)
- Higher (if you have a clear differentiator worth paying for)

**Anchor 2 — Value-based floor:**
What does the product save or create per month for one user?
- If it saves 5 hours/month and user bills at $50/hr → value = $250/month. Charge 10–20% of that: **$25–$50/month**.
- If it makes users $500/month → charge 10%: **$50/month**.
- Charge at least 5% of the value you create. If you can't justify that, revisit the value proposition.

### 3. Tier structure

For V1, use **at most 2 tiers**. 3+ tiers cause decision paralysis.

**Recommended V1 structure:**

```
Free / Starter
- [Core value action] — limited (e.g., 5/month, 1 project, basic features)
- No card required
- Goal: get users to experience the core value

Pro — $[X]/month (or $[X*10]/year)
- Everything in Free
- [Expanded limit or full access]
- [One power feature only paid users get]
- No card required to try, card required to upgrade
```

Never gate trial on a credit card — it kills conversion. Card at upgrade only.

### 4. The "charge more" heuristic

If you've never charged for software before, you're almost certainly pricing too low. The sign:
- Someone offers to pay you → you say $5/month → they say "that's it?" → you've underpriced.
- Charge what makes you slightly uncomfortable. Then raise it 20% from there.

Common solo founder pricing mistakes:
- Pricing based on what *you* would pay, not what the *user* would pay
- Pricing based on cost to build, not value to the buyer
- Making the paid tier too similar to the free tier (no reason to upgrade)
- Monthly-only (always offer annual at 2 months free — some buyers prefer annual)

### 5. Pricing page copy

Generate the pricing page headline and tier descriptions:

**Headline formula:** "Get [outcome] for [$price]/month." Not "Pricing" as the heading.

For each tier, write:
- Tier name (avoid "Basic" and "Enterprise" — use outcome-based names)
- One-line description ("Best for founders shipping their first app")
- Feature list (5–7 bullets, written as outcomes not features)
- CTA text (not "Choose plan" — use "Start free" / "Get Pro" / "Try 14 days free")

## Output

1. **Model recommendation** — which pricing model to use and why
2. **Price point** — specific number(s) with the value-based and competitor anchors shown
3. **Tier structure** — 2 tiers with feature lists, ready to implement in Stripe
4. **Pricing page copy** — headline, tier names, descriptions, CTA text
5. **One thing to watch** — the leading indicator that tells you if this price is working (e.g., "If free-to-paid conversion is below 2% after 100 signups, drop the price 30%")

---

> **Pricing set? Announce it.** [SoloMax](https://solomax.app?ref=shipping-skills) turns your product URL into launch videos, hooks, and posting copy — ready for the channels where founders buy.
