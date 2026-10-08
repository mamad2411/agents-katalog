---
name: pricing
description: Decides value metric, packaging, and price from evidence and willingness-to-pay signals. Use when guessing price, free tier is too generous, developers use it but nobody pays, or buyers ask how to pay.
license: MIT
disable-model-invocation: true
---

# Pricing

Value metric first. Packaging second. Number last. Price the value, not your fear.

Framework: [references/pricing.md](references/pricing.md).

## Process

From repo root: `node scripts/run-state-check.js pricing`.

Requires **ICP hypothesis**. If week-2 retention is unknown and no buyer asked to pay, say prove retention first (`activation`, `analytics`).

1. Name value metric (what scales with customer success).
2. Draw free / paid / enterprise line. Upgrade at moment of earned value.
3. Find number: deflected WTP emails > value anchor > competitor anchor > range question from interviews.
4. Run `review` on the pricing recommendation before presenting.

Does not update run-state unless founder asks; may add line to **Last observation**.

## Output

- Value metric (one sentence)
- Packaging (free vs paid vs enterprise triggers)
- Recommended tiers (max three self-serve)
- Number rationale (evidence pointers)
- What to test next (one pricing conversation or email)

## Done

Three decisions addressed in order. Assumptions flagged. review passed or REVISE named.

## Refuse

Cost-plus from AWS bill. Four tiers. Usage with no cap. Competing on "cheaper." Paywall before retention proof unless buyer already asked to pay.
