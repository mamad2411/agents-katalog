---
name: checkout-ux
description: Use when reviewing a cart, checkout, or payment form — e.g. "review my checkout", "reduce checkout drop-off", "guest checkout or force an account", "too many form fields", "Apple Pay", "shipping or tax surprise at the end", "coupon field killing conversion", "payment form on mobile", "people abandon at payment".
---

# Checkout UX

Audit the cart, checkout, and payment step — not the product page. Let someone who already wants the item pay without being blocked, surprised, or sent away to hunt for a code.

## When to use

- A cart, checkout, or payment form (URL, screenshot, or walkthrough)
- Guest vs forced account, wallets, coupon field, shipping/tax total, payment errors
- "Review my checkout" or "reduce checkout drop-off"

## When not to use

- Product-page merchandising (social proof, sold-out on the PDP) → `product-page`
- How the list price is written → `pricing`; ticket *price* → `event-pricing`
- Cart-abandonment *email* timing → `post-purchase`
- Ranking store-wide conversion levers → `increase-conversion`

## Inputs

Collect, or state your assumption: the flow (steps vs one page; mobile vs desktop); whether an account is required before the form; the field list; when shipping, tax, and the total appear; coupon field; wallets (Apple Pay, Google Pay, Shop Pay, Link) and their placement; returning-customer path; error states (decline, inventory, 3-D Secure).

## Procedure

1. **Do not block payment behind account creation.** If checkout opens on Login / Register, replace Register with Continue as guest; account optional after payment. At one large retailer this raised the number of customers purchasing 45%. † Asking people to register at the *start of browsing* is a different experiment (long-run purchases up, short-run sales unhurt) and is not a reason to gate the pay form.
2. **Cut fields to what you must have to ship and take payment.** One name field; collapse Address line 2 and company; default billing = shipping; infer city/region from postal code where possible. Typical large-site checkouts ask for more. † Show format hints on restricted fields. Mark required fields more strongly than a tiny asterisk — a color cue beat asterisks, but pair it with text.
3. **Errors after the field or after submit, next to the field.** Not while they type, not only at the top. Immediate in-flow errors were ignored ("completion mode"); ISO-style instant feedback performed worst. After submit, messages beside the bad field beat a dump at the top or bottom.
4. **Steps vs one page: mixed. Field count matters more than page count.** A short labeled sequence is fine; twenty fields on one page is not a win. Do not claim one-page always converts better. †
5. **Show item, shipping, tax, and the total before the pay click.** Drip pricing (base now, fees later) makes people pick a lower base that is often a higher total, then stick with it dissatisfied. Posting tax-inclusive prices cut grocery demand 8%, which is why hiding tax until the register looks tempting; a last-second jump is still a surprise. One clear shipping line is fine; stacking many surcharges reverses the benefit. Depth: `pricing`.
6. **Hide the coupon box behind "Have a code?".** Prompting people who *don't* have a code lowered fairness, satisfaction, and purchase completion. Auto-apply known codes when you can. Depth: `promotions`, `discounts`.
7. **Express wallets above the form, especially on mobile.** Apple Pay, Google Pay, Shop Pay, and Link skip address and card fields. Not a vendor requirement. No peer-reviewed wallet lift on file. †
8. **Trust next to pay: guarantee copy and a cost breakdown beat a badge wall.** One third-party assurance seal raised conversion in a randomized field experiment (9,098 sessions). More than two seals lost effectiveness; they helped more for small retailers and new shoppers. Lock-icon clutter is not a finding. Depth: `store-audit`.
9. **Mobile: numeric keyboard on card/postcode/phone, large tap targets, wallets first.** †
10. **Returning customers: remembered shipping after they choose to identify**, not a login wall before the form. "Already have an account?" is a link, not a gate. †
11. **Recovery copy for decline, inventory, and 3-D Secure.** Don't clear the form. Say what failed and the next step. 3-D Secure is required in some regions — recover through it. If the item sold out during checkout, say so. †

Rank by distance from the rule and whether the miss sits on the pay path. Ship the top two or three, measure, then take the next.

## Output

| # | Issue | Change | Measured effect (study context) | Source |
|---|---|---|---|---|
| 1 | Login/Register before the form | Continue as guest | +45% customers purchasing (one large retailer) † | Spool |
| 2 | Always-on coupon box | "Have a code?" | Lower completion when prompted with no code | Oliver & Shor 2003 |

Close with what the flow already does right. Effects are from the cited contexts, not predictions.

## Common mistakes

- Treating this as a product-page audit — social proof and sold-out variants stay on `product-page`.
- Forcing an account "to capture the email" before payment — take the order first.
- A visible coupon field "because some people have codes" — the people without codes are the ones it hurts.
- Revealing shipping and tax only on the last click — drip pricing; people who stay are less satisfied.
- A wall of lock icons — one recognized seal can help an unknown store; more than two lost force.
- Declaring one-page checkout the winner — mixed; field count is the lever.

## Quick reference

| Check | Rule |
|---|---|
| Account | Guest continue; optional account after pay |
| Fields | Ship-and-pay only; collapse optional; format hints |
| Errors | After field/submit, beside the field |
| Pages vs steps | Mixed; fewer fields, not fewer pages |
| Total | Item + shipping + tax before pay |
| Coupon | Apply-on-demand, not an always-on box |
| Wallets | Above the form, especially mobile |
| Trust | Guarantee + breakdown; at most one or two seals |
| Returning | Opt-in identify, not a login wall |
| Failures | Keep the form; say what happened |

† No primary citation on file for this rule — a practitioner tip, not a measured finding.

Evidence and effect sizes: see [reference.md](reference.md).
