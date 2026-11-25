---
name: negotiation
description: "Negotiate price and terms without caving — trade every concession for something of value, protect price by re-selling value, and defuse manufactured urgency. Use when a buyer asks for a discount, pushes back on price, or you're closing the terms. Triggers on: negotiate, discount, pricing pushback, close the terms, give a discount."
---

# Negotiation

## Purpose
Get a deal closed on terms you can defend without eroding price. Every concession
is traded for something that improves the deal — never given to "get to yes."

## Inputs
- The specific ask (discount %, terms, what the buyer wants)
- Deal value, products/SKUs in play, and your floor (walk-away price/terms)
- The value drivers and pains already established — your leverage to re-sell
- Open objections and what the buyer has already committed to

## Method
1. **Diagnose before you respond.** Don't react to the number. Find out *why*: is it
   budget, a competing quote, internal approval theater, or a test? The right
   response differs for each. Ask: "Help me understand — is this a budget ceiling,
   or are you comparing against another option?"
2. **Anchor first, anchor high.** Whoever frames the number first sets the range.
   Lead with full price tied to the value/ROI you established — never open with a
   discount. If they anchor low, re-anchor to value before discussing the gap; don't
   negotiate against their number.
3. **Trade, don't cave.** Never give a concession without getting something back.
   The rule is "If… then…": *"If you can do X, then I can do Y."* A unilateral
   discount trains the buyer that your price is fiction and that pushing harder pays.
4. **Re-sell value to protect price.** Before conceding a cent, return to the cost of
   the problem and the value of the outcome. Reframe price as a fraction of the value
   delivered: "The discount you're asking for is $Z; the problem we discussed is
   costing you $Z every month." Make price feel small against the stakes.
5. **Climb the concession ladder.** When you must move on price, extract value in
   return, working from cheapest-for-them to most valuable-for-you. Ask for these
   (roughly in order):
   - **Longer term length** — multi-year commitment for the discount
   - **Upfront / annual payment** — paid annually or in advance, not monthly
   - **Case study / logo rights** — public reference or quote
   - **References / intros** — referenceable calls, intro to other teams/divisions
   - **Expansion commitment** — committed path to more seats/products/usage
   Give the *smallest* price move that closes, and only in exchange for a rung.
6. **Recognize manufactured urgency.** "We need a decision by Friday" is often a
   tactic to pressure a discount. Test it: "What happens Friday?" If the deadline is
   real (board approval, fiscal year), it's leverage you can trade against. If it
   evaporates under one question, it's manufactured — don't pay for a fake clock.
7. **Plan give/gets before the call.** Map every concession to its return. Never
   improvise a discount live.

**Concession ladder (cheapest → most valuable to you):**
| Rung | What you give | What you ask in return |
|------|---------------|------------------------|
| 1 | Small % off | Longer term (2–3 yr) |
| 2 | Larger % off | Upfront / annual prepay |
| 3 | Discount or added scope | Case study + logo rights |
| 4 | Discount or premium support | Referenceable calls / intros |
| 5 | Best price | Committed expansion (seats/products) |

**Give/get planning table (fill before negotiating):**
```
Their likely ask:        <discount %, terms, scope>
My floor (walk-away):    <price/terms I will not cross>
Concession I'll offer:   <smallest move that closes>
Get in return:           <ladder rung — term, prepay, case study, ref, expansion>
Value to re-sell:        <cost of problem / ROI to anchor against>
Urgency test:            <"what happens on <date>?" — real or manufactured?>
```

**Trade-don't-cave rule:** every "yes" to a price move is conditional on a "yes" from
them. If they want something for nothing, the answer is a trade, not a discount.

## Tool binding
This skill works from the user's stated ask alone. It gets sharper when connected to
your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the deal directly instead of
asking the user to describe it:
- `ontology_resolve("deal", id, expand=["commitments","objections","value_drivers","products"])`
  — use the real `value_drivers` to re-sell value and protect price, the `products`
  and deal value to size the concession, open `objections` to understand *why* they're
  pushing, and `commitments` to know what the buyer has already agreed to (leverage
  for the give/get).
- `search_transcripts(...)` to quote the buyer's own words on the cost of the problem
  when you re-sell value.
Prefer Doris's extracted value drivers and objections over re-deriving them — they're
what the buyer actually said.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the deal value and products/line items to size
  the concession and know your floor.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → source the value drivers and
  objections from the call record.
- Email MCP → draft and send the trade ("If you can do X, then I can do Y").

### With nothing connected
Ask the user for the ask (discount %, terms requested), the deal value and products,
and their floor. Then output a negotiation plan: the anchored value re-sell, the
concession ladder with the specific get to request at each rung, a filled give/get
table, the urgency test, and the exact "If… then…" trade language to use live.

## Works without Doris
Fully functional from the user's stated ask — Doris only removes the description step
and supplies evidence-backed value drivers and objections to re-sell against.

## Common mistakes
- Giving a discount to "get to yes" without asking for anything in return.
- Discounting before re-selling value — conceding price you never needed to.
- Letting the buyer anchor the number and then negotiating against it.
- Paying for manufactured urgency you never tested with one question.
- Improvising concessions live instead of planning give/gets in advance.
