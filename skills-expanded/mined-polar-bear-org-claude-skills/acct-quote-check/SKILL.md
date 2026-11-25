---
name: acct-quote-check
description: Checks a sales quote before it leaves, with every line compared to your price book, discounts only where approved and by whom, the arithmetic recomputed with each difference shown, the assumption behind each quantity and the terms to verify. Use for "run acct-quote-check", "sales quote", "check this quote", "quote review before sending", "is my quote right", "pricing proposal check", "verify the discount on this quote", "quotation check", part of the Claude for Account Executives Pack by 90n.
---

# Sales Quote Check

## When To Use
A quote went out with an error in it and the customer found it first. Run this on every quote before it leaves, whether you built it by hand or it came out of a pricing tool. It answers two questions: does every amount come from your price book, and are the totals right?

## When Not To Use
To argue for your answer, use Sales Proposal. To decide which discount to give and against what, use Concession Plan: here a discount passes only if it is already approved. This skill checks a quote; it does not set a price.

## Inputs
- The draft quote, as a file, an export or pasted lines.
- Your price book or the prices your leadership gave you, with its version, and the approved discounts with the name of the approver.
- The quantities and what they rest on, and the tax rate that applies, supplied by you or your finance team.
If you have only the draft, I check the arithmetic, mark every price "[to confirm against the price book]" and mark the output as a first draft. With the desktop Output picker and Google Drive connected the check can go to Google Sheets; any spreadsheet works too.

## Approach
A pre-send check against the seller's own price book and approved discounts: common practice, described generically. I compare and recompute; I never set a price. Validity, payment and tax terms differ by country and by contract, so they are listed as points to verify. The failure it prevents: the goodwill discount added from memory, or a total that no longer matches the sum of its lines.

## Workflow
1. I ask at most three questions: where the prices come from (price book, version, date), which discounts are approved and by whom, and which tax rate applies.
2. Lines: for each, description, quantity, unit price and the price book reference it should match. A price not found in the book is flagged "not in the price book" and goes to the open questions; I do not supply one.
3. Discounts: each must carry the approver's name and stay within what was approved. One with no approver is flagged, never removed quietly and never accepted.
4. Arithmetic: I recompute every line, the subtotal, the tax at the rate you gave and the total, and show each difference with both values. I correct nothing in silence.
5. Quantities: I write what each one rests on (days, seats, sites, units), so the customer can see what would change the price.
6. Terms to verify: the two parties named correctly, validity period, payment terms, currency, tax treatment, and any reference to your standard terms. These are a list to check, not advice: check with a qualified adviser.
7. Open questions for you or your leadership: missing prices, unconfirmed quantities, a discount the customer asked for that nobody approved.

## Output Format
```markdown
# Sales Quote Check
**Quote:** [reference] · **Customer:** [name] · **Price book:** [version, date] · **Status:** not cleared to send
## Lines against the price book
| Line | Quantity | Unit price on the quote | Price book reference and price | Discount (approved by) | Result |
|---|---|---|---|---|---|
| [item] | [quantity] | [price] | [reference, price] | [none / discount, name] | [matches / differs / not in the price book] |
## Arithmetic
| Element | On the quote | Recomputed | Difference |
|---|---|---|---|
| Subtotal | [amount] | [amount] | [difference or none] |
| Tax ([rate you supplied]) | [amount] | [amount] | [difference] |
| Total | [amount] | [amount] | [difference] |
## What each quantity rests on
- [line]: [days, seats, sites, units, as agreed on date]
## Terms to verify
- [ ] Parties, validity, payment terms, currency, tax treatment: check with a qualified adviser
## Open questions
- [missing price / quantity to confirm / discount with no approver]
## Decision
[Approver name] clears prices and discounts; [you] send the quote on [date] once every difference is resolved.
```

## Done When
- Every unit price is matched to a price book reference or listed in the open questions.
- Every line and total is recomputed, and every difference is shown.
- Every discount names its approver or is flagged, and the terms list ends with the adviser line.

## Quality Bar
- I choose no tax rate and give no tax or legal advice.
- The status stays "not cleared to send" until you clear it.
- The check runs the same way on a hand-built quote and on one from a pricing tool.
- Claude never invents a price or a discount: every amount comes from your price book and every calculation is shown.

## Next
Run acct-customer-proof-story (Customer Proof Story) to give the quote a true story from a similar customer.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
