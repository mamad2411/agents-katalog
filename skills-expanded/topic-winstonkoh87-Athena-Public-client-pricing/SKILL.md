---
name: client-pricing
description: Commercial pricing engine for freelance deliverables. Encodes the pricing hierarchy, tiered anchor-floor tables, negotiation decision tree, and rate collapse prevention.
version: 1.0.0
created: 2026-03-06
cluster: 6 (Social Contract & Negotiation)
triggers:
  - quote
  - price
  - how much
  - charge
  - rate
  - negotiate price
  - client budget
context_trigger: "pricing, quote, proposal, how much should I charge, rate card, hourly rate, project fee, freelance pricing, scope creep, negotiation"
---

# Client Pricing Skill

> **Purpose**: Prevent rate collapse. Enforce anchor-first pricing. Automate the quoting decision tree.
> **Origin**: Empirical calibration from real client engagements — rate collapse incidents and floor-as-opening negotiation failures. Both were preventable.

## Core Principle

> "AI commoditizes labor. It cannot commoditize judgment."
>
> **Pricing Hierarchy** (defensibility axis):
> Time (❌) → Output (❌) → Deliverable (⚠️) → **Outcome (✅)** → **Access (✅✅)**

Never price at the Time or Output layer. Price at Deliverable (minimum) or Outcome (preferred).

## Tiered Pricing Table

| Deliverable Type | Anchor | Floor | Notes |
|---|---|---|---|
| **Essay** (1000–2000 words) | $250 | $150 | Counter at $200 if pushback | <!-- pds:allow -->
| **Problem Set** (SPSS, coding, math) | $350 | $250 | Scope-dependent; +$50/additional test family | <!-- pds:allow -->
| **Capstone/Report** (5000+ words) | $1,000 | $500 | Multi-round negotiation expected | <!-- pds:allow -->
| **Presentation** (slides + script) | $300 | $200 | +$100 if design assets required | <!-- pds:allow -->
| **Speed Premium** (< 48hr turnaround) | +30% | — | Non-negotiable surcharge |
| **Complexity Premium** (cross-domain) | +20% | — | E.g., engineering + writing + coding |

## The Negotiation Decision Tree

```
YOU: State anchor price
↓
CLIENT: "Too high"
↓
YOU: "What's your budget?" (NEVER counter against yourself)
↓
CLIENT names their number
↓
├─ (A) Within 20% of anchor → Counter midpoint, settle ±10%
├─ (B) 40-60% of anchor → Counter at floor + 20%, settle at floor + 10%
├─ (C) Below floor → "Sorry, [floor] is the lowest I can go"
│   ├─ Client accepts → Done
│   └─ Client walks → Let them (Dignity Premium)
└─ (D) Client ghosts → Follow up once at 24hr. No chase after.
```

**Three rounds maximum.** After round 3, you're haggling, not negotiating.

## Anti-Patterns (Reflexion Archive)

| Anti-Pattern | Case Study | Fix |
|---|---|---|
| **Opening at floor** | Quoted at floor instead of anchor — left $50+ on the table | Always open at anchor. Floor is your walk-away, not your opening |
| **Rate collapse via speed** | Delivered fast, effective rate dropped to $83/hr vs $310/hr benchmark | Price by deliverable complexity, not hours. Speed is your competitive advantage — don't let it compress price | <!-- pds:allow -->
| **Negotiating against yourself** | Generic pattern | After stating anchor, SHUT UP. Let the client name their number |
| **Scope creep without re-quote** | Client adds "just one more thing" | Any addition > 10% of original scope triggers re-quote |

## Activation Rules

1. **Auto-trigger**: When `academic-delivery` Step 2 (SCOPE) identifies commercial work
2. **Manual trigger**: "/quote", "how much should I charge", "client is asking about price"
3. **Exit**: Output a formatted quote with anchor + justification + scope boundary

## Quote Template

```
Hi [Client],

Based on the scope ([deliverable type], [word count/test count], [deadline]):

**Quote: $[ANCHOR]**

This covers: [explicit scope list]
Not included: [explicit exclusions]
Turnaround: [timeline]

Payment: [deposit]% upfront via PayNow, balance on delivery.

Let me know if you'd like to proceed.
```
