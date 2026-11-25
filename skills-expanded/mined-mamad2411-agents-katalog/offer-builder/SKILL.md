---
name: offer-builder
description: Builds or rebuilds the offer — the outcome promised, a value stack where every element kills a named pain, price logic, risk reversal designed against the buyer's worst fear, and urgency only if it is real — ending in an offer one-pager saved to the brief. Use when conversion is soft, discounting is creeping in, or the product is fine but the deal is forgettable.
argument-hint: "[current offer + price, or 'work from the brief']"
---

# Offer Builder — make the deal the best part of the pitch

Traffic problems are often offer problems wearing a disguise. When the offer is genuinely strong — a clear outcome, value stacked against named pains, a price that reads as obvious, risk carried by the seller — the ads get easier to write and the calls get easier to close. This skill builds that offer from the customer evidence in the brief, not from what the team hopes sounds premium.

## Inputs
- The current offer and price if one exists, plus what is actually delivered: $ARGUMENTS
- From `marketing-brief.md` if present: top pains and desired outcomes (the stack is built against them), objections (the risk reversal is built against them), competitor offers, and the position.

## Do this
1. Name the outcome being bought. The after-state, specific and honest — "a booked sales calendar", not "access to our platform". If the outcome cannot be stated without listing deliverables, the offer is not ready and this step is the work.
2. Build the value stack. Every element must kill a named pain or remove a named obstacle from the customer research. Cut anything decorative — padding inflates nothing but doubt.
3. Set the price logic. Anchor against the cost of the problem, the value of the outcome, and the nearest alternative, then write the one-line logic a buyer would repeat internally to justify it ("costs less than the hire it replaces").
4. Design the risk reversal against the buyer's worst fear — wasted budget, looking foolish in front of the boss, months lost to a failed switch. Name the fear first, then build the guarantee that reverses it. A guarantee that does not touch the fear is furniture.
5. Add urgency only if it is real — capacity limits, a cohort date, a genuine price change, a seasonal window. If nothing real exists, ship without urgency; a fake deadline costs more trust than it gains conversions.
6. Read the offer as the buyer and answer the five silent questions. Every unanswered one is a hole in the offer:
   - Is the outcome worth the price to me?
   - Do I believe you can deliver it?
   - Will it work for someone in my situation?
   - How long until I see it?
   - How much of my own effort will it take?
7. Write the offer one-pager and update **The offer** section of `marketing-brief.md`. Inside Claude Code, the offer-strategist agent can run the deep version of this whole pass.

## Output
The offer one-pager — outcome, stack with the pain each element kills, price with its one-line logic, risk reversal, urgency or its honest absence — saved into `marketing-brief.md` under **The offer**. Flag every stack claim that currently lacks proof.

## Rules
- Value is perceived by the buyer, not calculated by the seller. A stack element is worth what the evidence says the pain costs, not what it costs to deliver.
- No invented scarcity, ever. One fake deadline poisons every real one after it.
- Every stack element kills a named pain from the brief. An element that cannot name its pain does not ship.
- The guarantee reverses the buyer's worst fear, not the seller's smallest risk.
- Price with a straight face. If the one-line logic cannot be said aloud to a real buyer, the price or the logic is wrong.
