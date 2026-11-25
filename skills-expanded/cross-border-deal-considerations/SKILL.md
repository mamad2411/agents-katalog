---
name: cross-border-deal-considerations
description: Produces a cross-border deal assessment covering price currency and hedging, withholding structure, repatriation, and the approval sequence when you need to run a transaction across jurisdictions.
---

# Cross-Border Deal Considerations Agent

## When to use
Use this when buyer, target, or financing sit in more than one jurisdiction and the domestic playbook stops being sufficient. Typical triggers: a bid priced in a currency the acquirer does not fund in, a target whose cash sits behind a withholding regime, or a closing that must clear several regulators. Reach for it when the question is what the deal really costs once borders are in it.

## What it does
It produces a cross-border assessment: a map of where value and cash sit, an FX exposure and hedging recommendation on the price, a structure tested for withholding and treaty access, a repatriation plan, a restatement onto the acquirer's accounting standard, and a sequenced approval calendar.

## Method
1. Map the footprint. Know where value and risk sit.
   - List entities with tax residence, functional currency, and share of EBITDA and cash, plus any permanent-establishment wrinkle.

2. Fix the currency of the price. Decide who bears FX.
   - Set the currency of the offer, of funding, and of target cash flows; a price fixed in the target's currency puts the entire signing-to-closing move on the buyer.

3. Hedge the exposure. Match the instrument to the contingency.
   - A deal-contingent forward costs a premium but falls away if the deal does; a plain forward is cheaper and leaves a naked position on a break. Price both rather than taking the cheaper quote.

4. Structure for withholding. Test the holding chain.
   - Route through a jurisdiction with a treaty to the target's, then test it against limitation-on-benefits and beneficial-ownership rules. A structure that survives only if nobody looks at it is not a structure.

5. Plan repatriation before signing. Cash at the parent is what counts.
   - Model dividends, interest, and royalties net of withholding, check interest-deductibility limits, and flag trapped cash and reserve constraints.

6. Restate onto the acquirer's standard. Compare like with like.
   - Convert IFRS to US GAAP or the reverse for leases, development-cost capitalisation, revenue timing, and provisions, then recompute the multiple on the restated figure. It usually moves.

7. Sequence the approvals. Work backwards from the long-stop date.
   - Merger control, investment screening, sector regulators, and works-council consultation, marking which are suspensory and which cannot start until another has filed. Time-zone overlap decides how many move in one day.

8. Set closing mechanics. Fund across two banking calendars.
   - Build the funds flow around non-coincident holidays and value dates, and name which side is exposed overnight.

## Inputs
- Entity and jurisdiction map for buyer, target, and financing vehicles
- Currency of the offer, of funding, and of target cash flows
- Target financials with the reporting standard identified
- Treaty positions, prior rulings, and the approval list per jurisdiction
- Signing date, long-stop date, and the financing availability period

## Output format
- A jurisdictional map with EBITDA, cash, and functional currency by entity
- An FX exposure statement with a hedging recommendation and its cost
- A structure section on withholding, treaty access, and substance
- A repatriation plan showing cash reaching the parent, net of withholding
- A restatement bridge from reported figures to the acquirer's standard
- A sequenced approval calendar and the closing funds flow
- Present all schedules in prose, never as markdown tables

## Example
For a US acquirer of Halden Instrumente (fictional, illustrative), the price is fixed at EUR 400 million. At 1.10 that is USD 440 million; at 1.18 it is USD 472 million, so the exposure is USD 32 million, and a deal-contingent forward at 2 percent of notional costs EUR 8 million, or USD 8.8 million, to remove it. The target reports EUR 50 million of IFRS EBITDA; expensing EUR 4 million of capitalised development and returning EUR 2 million of lease rent to operating costs gives EUR 44 million on the acquirer's standard, so the 8.0x headline is 9.1x like for like. EUR 30 million of dividends bear 25 percent withholding statutorily and 5 percent under treaty, a EUR 6 million annual difference that survives only if the holding company clears substance. Merger control at 25 working days runs alongside the investment screen, so a nine-month long-stop is comfortable and six months is not.
