---
name: ecom-promotions
description: Coupons, discounts, gift cards, loyalty, and promotion-stacking rules. Auto-invoked when designing promo logic, debugging unexpected discount totals, or integrating loyalty / store-credit systems.
---

# E-commerce Promotions

Promotions are the most error-prone code in e-commerce — a single stacking bug
can discount the whole catalog to zero during peak, and gift cards are bearer
instruments that fraud rings actively probe.

## When to reach for this

- Designing a promo rule model (percent, fixed, BOGO, tiered, bundle) or its targeting/eligibility
- Debugging an unexpected discount total or a stacking conflict
- Implementing gift cards, store credit, or loyalty accrual/redemption
- Adding abandoned-cart or win-back incentive codes

## Principles

1. **Promos are pure functions.** `(cart, customer, context) → discount_lines`,
   no hidden mutation — identical inputs always reproduce identical outputs,
   which is the only way to audit a disputed total.
2. **Precedence is written down and versioned.** Fix the application order
   (line-item → cart-level → shipping; tax computed on the discounted base) and
   snapshot the rule-set version onto every order so any historical total can be
   replayed exactly.
3. **Cap every knob.** Max discount per line, per cart, per customer per period;
   max loyalty-point redemption; max gift cards per order. Missing caps are how
   $0 orders ship in production.
4. **Gift cards are money.** Activation cool-off on newly sold cards, velocity
   limits on redemption, geo/BIN checks at purchase, and rapid-drain monitoring.
   Refunds-to-card must track remaining balance correctly.
5. **Instrument every application.** Each promo applied writes a structured
   event (`promo_id`, `rule_version`, `discount_amount`, cart context) — without
   it, attribution, abuse detection, and finance reconciliation are guesswork.
6. **Stress-test stacking with generated carts.** Property-based tests: random
   carts × random active promo sets, asserting the invariants below. Humans do
   not find combinatorial stacking bugs by inspection.

## Invariants every generated-cart test asserts

- [ ] Cart total never negative; no line discounted below zero
- [ ] No item priced below its floor (cost or configured minimum margin)
- [ ] Exclusive promos never co-applied; stacking matrix respected
- [ ] All caps respected (per-line, per-cart, per-customer, loyalty, gift-card split)
- [ ] Rounding policy applied once, at the documented step — totals re-derive exactly
- [ ] Removing a cart item never *increases* the total (discount re-evaluation is monotonic)
- [ ] Same cart + same rule-set version → identical discount lines (determinism)

Also worth a regression suite: replay historical orders against the current
engine pinned to their stored rule-set version — totals must match to the cent.

## Pitfalls

- Percentage discounts applied after fixed discounts when the spec says the
  reverse (order-of-operations changes the total)
- Single-use codes enforced only client-side or checked outside the redemption
  transaction (race → multi-redemption)
- Gift-card balance updated without an idempotency key — a retried redemption
  drains it twice
- Loyalty points accrued on the pre-discount total but reversed on the
  post-discount refund (slow point inflation)
- Stacked free-shipping + cart-percent promos pushing orders below cost with no
  margin floor
- A/B promo tests without a holdout — you can't see cannibalization of
  full-price demand

---
*Related: `ecom-tax` (discount-before-tax vs after-tax treatment),
`ecom-payments` (gift card as tender, refund-to-card), `ecom-inventory`
(reserving BOGO/bundle components) · domain agent: `ecom-architect`
(promotions-engine boundary) · output/ADR format: `playbook-conventions`*
