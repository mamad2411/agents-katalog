---
name: issue-a-store-coupon-code
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a store coupon code with the intended discount, limits, and expiration.

## Preconditions

- You have approval for the discount amount, audience, and promotion dates.
- You have access to the store discount or promotions tool.
- You know margin, eligibility, and abuse-prevention requirements.

## Steps

1. **Open discount creation.** [BRANCH: Shopify | generic] choose Discounts > Create discount in Shopify, or open the platform's coupon tool. → *Expect:* a new discount form is open.
2. **Name the code.** Enter a clear, unique code that matches the campaign or customer case. → *Expect:* the code is easy to identify later.
3. **Set discount value.** Choose percentage, fixed amount, free shipping, or product-specific discount. → *Expect:* the discount matches the approved offer.
4. **Define eligibility.** Limit by products, collections, customer segment, minimum order, or one-time use as needed. → *Expect:* only intended orders qualify.
5. **Set dates and limits.** Add start date, end date, usage cap, and per-customer limits. → *Expect:* the code cannot run longer or wider than intended.
6. **Save the coupon.** Confirm the discount settings in the platform. → *Expect:* the code is active, scheduled, or saved.
7. **Test in cart.** Add eligible and ineligible items to a test cart and apply the code. → *Expect:* the discount applies only under intended conditions.
8. **Share the code.** Send the code through the approved channel with terms and expiration. → *Expect:* recipients know how and when to use it.

## Decision points

- If the code applies too broadly → narrow product, customer, or order rules before sharing.
- If the promotion is private → use single-use or customer-specific restrictions.
- If margin impact is uncertain → get finance or merchandising approval first.

## Failure modes & recovery

- **F1 Over-discount:** detect cart total is lower than approved → disable the code and correct settings.
- **F2 No expiration:** detect the code has no end date → add one before sharing.
- **F3 Code already used:** detect duplicate code conflict → create a new unique code and update campaign materials.

## Verification

The coupon exists with approved value, eligibility, limits, dates, and successful cart tests for eligible and ineligible cases.

## Variations

- Customer service credit: restrict to one customer and one use.
- Influencer code: add usage tracking and expiration by campaign.
- Free shipping: confirm shipping zones and minimum order rules.

## Safety & privacy

Low risk. Discounts affect revenue, so restrict private codes and avoid exposing customer-specific codes in public channels.
