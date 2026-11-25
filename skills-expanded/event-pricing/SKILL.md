---
name: event-pricing
description: Use when pricing or promoting tickets, classes, workshops, bookings, or any event with dates and limited seats — e.g. "how should I price the workshop", "early-bird discount or something else", "should I show sold-out dates", "only 12 seats left banner", "what goes on the ticket page", "how do I sell out this cohort".
---

# Event pricing

Events are experiences: buyers decide on feelings, sold-out dates signal quality, and the wrong kind of scarcity turns the people who miss out against you. This skill is the delta versus `pricing`, `promotions`, `discounts`, and `product-page`. Ticket *price digits* still follow `pricing`; the payment form follows `checkout-ux`.

## When to use

- Setting a ticket, class, or booking price
- Designing pre-sales, early-bird offers, and how dates or seats are shown

## When not to use

- Shared digit, gift, deadline, and depth rules in isolation → `pricing`, `promotions`, `discounts`
- Product-page media and price position in isolation → `product-page`, `product-visuals`
- Finding the price level people will pay → `price-research`
- Checkout/payment fields for the ticket sale → `checkout-ux`

## Inputs

Collect, or state your assumption: the event, ticket price, and date(s); how far away the first date is; how many dates or slots and how many are sold out; any complementary item you can give; whether it is bought for enjoyment or for a functional outcome.

Most events — workshops, concerts, retreats, cooking classes — are hedonic. Training bought for a functional result (exam prep, compliance) is the utilitarian exception.

## Procedure

Only the rules that change for dated, capacity-limited events.

1. **Rounded ticket price.** Experiences are bought on feelings, so $150 beats $149. Just-below only for a promotion price. Depth: `pricing`.
2. **Show sold-out dates — up to 30% of them.** Mark them instead of hiding them; beyond ~30% people abandon. This is the event form of the sold-out-variant rule. Depth: `product-page`.
3. **Deadline, not a seat-count, as the promotional lever.** "Early pricing ends 30 Sept, 23:59 CET" is fine. "Only 12 seats left!" as a marketing hook is not: people who miss a quantity-capped *offer* get angry and switch. Showing *accurate* remaining capacity as inventory (a seat picker, "2 dates left" in a list) is fine. Depth: `discounts`.
4. **Pre-sales: gift, not early-bird discount, when the event is 3+ weeks out.** A bonus session, materials, or the recording at no cost. Within about a week, either works. Hedonic events tolerate long windows; functional ones should keep them short. Depth: `promotions`.
5. **Human-labeled recommendations** for experiences ("others also booked"). Depth: `store-audit`.

Shared, unchanged: discount ≤ 40% and amount-vs-% by the 100 threshold; invented relevant special days; video and gaze-away on the ticket page; price below the image. Depth: `discounts`, `promotions`, `product-visuals`, `product-page`.

## Worked example

Pottery studio, 8-week wheel class, plan: $149, 25% early-bird, "Only 12 seats left", sold-out Saturday hidden, algorithm "recommended" row.

- **$150**, rounded.
- Early-bird 8 weeks out → **glazing-masterclass recording at no cost**, dated deadline, no seat-count banner.
- Show the sold-out Saturday, marked, if sold-out dates stay in the 10–30% band.
- **"Others also booked"** instead of the algorithm label.

## Output

| Item | Value |
|---|---|
| Ticket price | $150 (rounded; hedonic) |
| Dates shown | All 8; 2 marked sold out (25%) |
| Pre-sale (8 weeks out) | Recording at no cost by a dated deadline |
| Urgency copy | Deadline + reason + timezone; no seat-count promo |
| Rejected | 25% early-bird, "Only 12 seats left", hidden sold-out dates |
| Why | one line per choice |

## Common mistakes

- Keeping the early-bird discount because it "gives a real reason to book now" — 3+ weeks out, a gift converts better.
- Dropping "12 seats left" only because it might be inaccurate — accurate or not, unit caps as a promo anger the people who miss out. Use a deadline. Accurate inventory in a picker is a different thing.
- Hiding sold-out dates — they are the strongest quality signal on the page; show them, up to 30%.
- Pricing at $149 to look cheaper — it signals a bargain, not an experience.

## Quick reference

| Situation | Do | Depth |
|---|---|---|
| Ticket price | Rounded | `pricing` |
| Sold-out dates | Show, marked; 10–30% | `product-page` |
| Promo urgency | Deadline, never a seat-count hook | `discounts` |
| Pre-sale, 3+ weeks out | Gift, not early-bird | `promotions` |
| Recommendations | Human label | `store-audit` |

Evidence and effect sizes: see [reference.md](reference.md).
