---
name: ecom-tax
description: Sales tax, VAT, GST, and marketplace-facilitator obligations. Auto-invoked when integrating tax engines, implementing nexus logic, handling cross-border orders, or reconciling tax filings.
---

# E-commerce Tax

Tax errors don't get caught by tests — they get caught by auditors years later,
with penalties and interest. Every tax figure on an invoice and every liability
number that gets filed has to be reproducible.

## When to reach for this

- Integrating a tax engine (Avalara AvaTax, TaxJar, Vertex, Stripe Tax)
- Implementing US economic-nexus tracking or EU OSS/IOSS flows
- Handling refunds, partial refunds, or chargebacks that reverse tax
- Building tax-exempt (resale certificate, B2B reverse-charge) checkout paths

## Principles

1. **Defer to the tax engine; own the integration.** Never hand-code rate
   tables. Send full validated address, product tax code, and order context;
   trust the engine's jurisdiction resolution. Cache responses only as the
   engine's terms explicitly permit.
2. **Track nexus continuously.** Most US states trigger at **$100K sales or 200
   transactions** per year (thresholds vary — South Dakota v. Wayfair baseline);
   EU distance selling consolidates at **€10K** under OSS. Build a daily rollup
   per jurisdiction that alerts ~30 days before crossing — registration has lead
   time.
3. **Taxability is configuration, not code.** Map every SKU to a product tax
   code (e.g., Avalara `PC040100` for general clothing). SaaS, digital goods,
   shipping, and gift cards each have distinct treatment per jurisdiction —
   never default to "tangible goods".
4. **Reversals mirror originals.** A refund posts its tax reversal to the same
   jurisdiction at the original rate, even if rates changed since. That means
   storing the full original tax detail (jurisdictions, rates, amounts) on the
   transaction, not recomputing at refund time.
5. **EU invoices are legal documents.** Sequential numbering, seller and buyer
   VAT numbers, itemized tax per rate, reverse-charge notation for B2B —
   missing fields invalidate the buyer's VAT reclaim.
6. **Reconcile three ways, monthly.** Tax-engine totals ↔ ledger tax liability
   ↔ filed returns. Drift is almost always a refund booked in a different
   period, currency rounding, or bundle allocation.

## Tax-engine call map

| Cart/order event | Engine call | Notes |
|---|---|---|
| Cart/checkout display | quote (uncommitted) | estimate; never file from quotes |
| Order capture | commit transaction | idempotency-keyed on order ID |
| Address change pre-ship | void + re-commit | jurisdiction may change |
| Refund (full/partial) | committed return tied to original doc | original rates and jurisdictions, per principle 4 |
| Exempt purchase | commit with exemption certificate ID | certificate stored with expiry; re-verify on lapse |
| Marketplace-facilitated sale | depends on platform role | facilitator collects → record but don't double-remit |

## Pitfalls

- Computing tax on the pre-discount subtotal (or post-, when the jurisdiction
  says otherwise) — discount treatment is a per-jurisdiction rule, not a default
- Filing from quote-mode calls that were never committed (totals won't tie out)
- Recalculating refund tax at today's rate instead of the original's
- Treating shipping as universally non-taxable (taxable in many US states when
  the goods are)
- Missing the marketplace-facilitator split — remitting tax the marketplace
  already remitted
- Exemption certificates accepted once and never expired or re-validated

---
*Related: `ecom-payments` (tax committed at capture, reversed with refunds),
`ecom-promotions` (discount-before-tax vs after-tax) · domain agent:
`ecom-architect` (checkout boundary, where tax calls live) · output/ADR
format: `playbook-conventions`*
