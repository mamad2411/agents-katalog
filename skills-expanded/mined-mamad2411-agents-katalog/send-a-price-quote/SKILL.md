---
name: send-a-price-quote
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Send a clear price quote that tells a prospective customer what is included, what it costs, and how long the offer is valid.

## Preconditions

- The customer request, scope, quantities, delivery assumptions, and pricing are known.
- You know whether taxes, shipping, deposits, discounts, or expiration dates apply.
- The customer contact details are available.

## Steps

1. **Open a new quote or estimate.** Go to quotes, estimates, sales, or proposals and create a new record. → *Expect:* a blank quote form is visible.
2. **Select the customer.** Choose or add the customer and quote recipient. → *Expect:* the quote is addressed to the correct person or business.
3. **Define the scope.** Add concise descriptions of products, services, deliverables, exclusions, and assumptions. → *Expect:* the customer can see what is and is not included.
4. **Enter pricing.** Add quantities, rates, discounts, tax treatment, shipping, deposits, and payment terms. → *Expect:* the quoted total matches your intended offer.
5. **Set validity and next step.** Add expiration date, acceptance instructions, and whether approval converts to an invoice. → *Expect:* the customer knows how and when to accept.
6. **Preview the quote.** Review customer, scope, totals, dates, and terms. → *Expect:* no draft notes or internal-only fields are visible.
7. **Send the quote.** ⚠️ *Irreversible:* sending may create a commercial offer, so confirm pricing, scope, and recipient first. → *Expect:* the system records the quote as sent.

## Decision points

- Scope is uncertain → quote a discovery phase or include explicit assumptions.
- Price depends on volume or timing → add expiration and change-order terms.
- Customer needs approval workflow → include purchase-order or signature instructions.
- Quote should not be binding → label it estimate and include terms that explain variability.

## Failure modes & recovery

- **F1 Missing exclusion:** detect by customer assuming extra work is included → recover by revising and resending the quote before acceptance.
- **F2 Wrong tax or shipping:** detect by total differing from intended landed price → recover by editing before sending or issuing a revised quote.
- **F3 Sent to wrong recipient:** detect by activity log or bounce → recover by voiding or expiring the quote and sending a corrected version.
- **F4 Quote accepted after expiration:** detect by acceptance date after validity period → recover by reviewing pricing and issuing a new quote.

## Verification

The quote is marked sent with the correct customer, scope, exclusions, pricing, tax, expiration date, and acceptance instructions.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks uses Estimates; Xero uses Quotes; generic tools may use Proposal, Quote, or Estimate.
- `us`: sales-tax estimates should note that final tax may depend on delivery location and date.

## Safety & privacy

Medium risk because incorrect quotes can create pricing disputes. Avoid exposing internal margins, vendor costs, or unrelated customer information.
