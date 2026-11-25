---
name: ecommerce-operations
description: E-commerce and online retail operations — conversion funnel (traffic → product page → cart → checkout), average order value (AOV), bundle and upsell strategy, cart abandonment recovery, product listing/page optimization, pricing, promotion mechanics and promo calendars (tiered discounts), returns rate management, marketplace vs D2C trade-offs, fulfillment SLAs, inventory sync, reviews and ratings ops. Use for online store performance, listing optimization, promotions, or e-commerce metrics.
---

# E-commerce Operations (funnel, AOV, promos, returns, fulfillment)

## The funnel, measured at every gate

```
sessions → product page views → add-to-cart → checkout started → order
CVR (conversion rate)   = orders / sessions            (state the session definition and window)
PDP conversion          = add-to-cart / product page views
cart abandonment        = 1 − (checkout started / carts created)
checkout abandonment    = 1 − (orders / checkouts started)
AOV                     = gross order revenue / orders
revenue per session     = CVR × AOV      ← the number both levers roll up to
```

Diagnose by *which* gate leaks, segmented by device, traffic source, and new vs returning — a
blended CVR moves whenever the traffic mix moves and says nothing about the store. Mobile checkout
abandonment is routinely the largest single leak; check it before redesigning anything upstream.

## Product pages and listings

- One listing = one buyer question set: what is it, does it fit my need, why trust you, what does it
  cost all-in. Title and first image carry most of the click decision; specs, sizing, and photos
  from every angle carry the conversion.
- Search terms belong in titles and attributes (that's what search indexes match); keyword-stuffed
  titles that read as spam lower click-through and, on marketplaces, invite suppression.
- Reviews ops: ask post-delivery (timed after actual use), make it one click, respond to negatives
  publicly with a fix. Never incentivize positive-only reviews — platform bans aside, a spotless 5.0
  converts worse than a credible 4.6.
- Out-of-stock and inventory sync: oversells destroy marketplace account health; a buffer stock
  threshold per channel and a single source of truth for inventory beat manual reconciliation every
  time.

## Pricing and promotion mechanics

- Every promo needs pre-declared math: expected uplift in units × contribution margin after discount
  vs baseline margin forgone on units that would have sold anyway. A promo that "did great revenue"
  while paying full margin away on baseline demand lost money invisibly.
- Discount depth trains customers: predictable sitewide sales teach everyone to wait. Prefer
  targeted mechanics (first-order, bundle, threshold "spend X get Y" — which lifts AOV) over blanket
  percentages.
- Cart abandonment recovery: the sequence (reminder → objection-handling → incentive last, hours to
  days apart) recovers a meaningful fraction; leading with a discount in email #1 just reprices
  everyone who was coming back anyway.
- Price changes on marketplaces interact with buy-box/ranking algorithms — change one variable at a
  time and hold a measurement window, or you learn nothing.

## Returns

```
returns rate = returned units / units sold (by cohort of ship date, per SKU and category —
               a spike is a product or listing defect, not a customer mood)
true return cost = refund + outbound & return shipping + inspection/restock + resale value loss
```

Attack causes before policy: sizing and photo accuracy fix apparel returns; policy tightening fixes
the P&L line while quietly killing conversion (a generous returns policy is a conversion asset —
price it in, don't wish it away). Track return *reasons* as structured data, feed the top reason
back to the listing or the product.

## Marketplace vs D2C

- Marketplace buys you traffic and trust, and charges commission, ad-tax-to-be-visible, price
  pressure, and no customer relationship (the platform owns the buyer). D2C buys you margin, data,
  and CRM — and makes traffic entirely your acquisition cost.
- Run both deliberately: marketplaces for discovery and validation, D2C for repeat purchase and
  bundles. Keep channel P&Ls separate with all-in costs (commission, fulfillment fees, ads, returns)
  per channel; a SKU can be profitable on one channel and a loss on the other.

## Fulfillment SLAs

- Promise = handling time + carrier transit; measure ship-on-time and deliver-on-time separately
  (you own the first, you manage the second). Late shipment rates on marketplaces trigger account
  penalties before customers even complain.
- Fulfillment cost per order (pick/pack + packaging + shipping) belongs in contribution margin per
  order — free-shipping thresholds should be set just above current AOV, from that math, not from a
  competitor's banner.

## Failure modes

- Celebrating CVR gains that came from a traffic-mix shift (more branded/returning traffic), not from
  the store.
- AOV pushed up with bundles while contribution margin per order fell — revenue up, profit down.
- Promo calendar so dense the "baseline" week no longer exists, making every uplift claim unmeasurable.
- Returns rate managed as one number; the single defective SKU driving it ships for another quarter.
- Inventory synced hourly across channels, oversold in the gap during the one flash sale that mattered.

## Reviewer checklist

- [ ] Funnel metrics gate-by-gate, segmented by device and traffic source; session definition stated
- [ ] Any CVR/AOV claim traced to revenue per session and contribution margin, not either alone
- [ ] Promos have pre-declared baseline, uplift math, and margin-after-discount; measured vs it
- [ ] Returns analyzed per SKU/cohort with structured reasons; true return cost itemized
- [ ] Channel P&Ls separate and all-in (commission, ads, fulfillment, returns)
- [ ] Fulfillment: ship-on-time vs deliver-on-time split; free-shipping threshold derived from AOV math
- [ ] Review solicitation compliant and post-use; negative reviews answered with fixes

## Provenance

Standard e-commerce operations practice (funnel decomposition, revenue-per-session framing, promo
incrementality, returns causal analysis, channel P&L separation). No platform benchmark is cited;
any illustrative figure is **derived, unverified** — replace with the store's own analytics and fee
schedules before acting.
