---
name: power-inversion
description: "Unified negotiation engine: BATNA mapping, Dignity Premium pricing, and commitment device protection. Absorbs: commitment-device."
argument-hint: "prepare deal | protect the deal | commitment | pricing pushback | negotiate"
allowed-tools:
  - Read
  - Write
auto-invoke: true
model: default
context_trigger: "negotiation, BATNA, leverage, dignity premium, they want info first, pricing pushback, protect this deal"
---

# Negotiation Engine (Power Inversion + Commitment)

> **Absorbs**: `commitment-device`

Unified pre-negotiation skill. Structures high-stakes deals by mapping BATNAs, asserting the Dignity Premium, and securing leverage BEFORE releasing valuable assets.

## Triggers

"negotiation", "prep for call", "pricing pushback", "should I share this first", "they want info before paying", "how do I protect this deal", "they said it's too expensive"

## Phase 1: Power Mapping

1. Evaluate subjective cost (identity compromise) vs objective payout.
2. Calculate the Minimum Acceptable Offer (Responder Floor).
3. Invert the Power Dynamic by threatening withdrawal ("The Walk").

## Phase 2: Commitment Devices

Never release the asset before securing commitment.

| Device | Mechanism | When to Use |
|--------|-----------|-------------|
| **Refundable Deposit** | $X upfront, refund if no deal | Filters extraction-only actors |
| **Partial Information** | "Deposit to see profiles" | Maintains leverage |
| **Penalty Clause** | Commission due regardless of channel | Closes bypass loophole |
| **Watermarking** | Unique identifiers proving pipeline | Creates audit trail |
| **Escrow** | Third party holds funds | Mutual protection |

**The $100 Filter**: A refundable deposit isn't about the money — it's a filter for intent. Serious buyer pays; extraction-only balks.

## Phase 3: Bias Detection (Pricing)

1. **Source Check**: Where did this number come from? (counterparty anchor, market rate, previous deal?)
2. **Structural Value**: `max(Cost of Production × 1.5, Value to Buyer × 0.3)`
3. **Position**: Under / Fair / Over relative to structural value

## Reference Protocols

- Protocol 64: Commitment Device Framework
- Protocol 120: Power Inversion
- Protocol 330: EEV (Expected Aggregate Value)
