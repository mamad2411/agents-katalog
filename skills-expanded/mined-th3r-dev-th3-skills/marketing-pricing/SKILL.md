---
name: marketing-pricing
description: Price a service's packages from real costs and the real market. Measure the marketplace category first (fastwork_market.py), collect the user's own numbers (income target, living costs, equipment, tools, learning, platform fee), use published averages labelled as assumptions for anything unknown, then compute break-even and target hourly rates, gross them up for the platform fee, and check every package with offer.py price so none loses money. Use WHENEVER the user asks "ตั้งราคายังไง", "คิดราคางาน", "ราคาต่อชั่วโมง", "แพ็กเกจราคาเท่าไหร่", "ขาดทุนไหม", "ค่าน้ำค่าไฟหารต่อวัน", "how much to charge", "pricing packages", "rate", "break-even".
---

# Pricing

Two numbers decide a price: what the work costs you per hour, and what the market pays. Theory,
models and the evidence behind each: [references/pricing.md](references/pricing.md).

## Workflow

1. **Measure the market.** `uv run scripts/fastwork_market.py <category URL> --limit 40`. Keep the
   printed numbers (cheapest-package median and quartiles, three-tier medians, delivery days,
   revisions) in the offer's `market` table with the date.
2. **Collect costs, asking first.** Ask the user for: monthly income target (current salary is a fair
   floor), working days and hours, monthly living costs, equipment, software, learning and security
   training, and the platform fee they actually pay. Ask once, in one list.
3. **Fill gaps with averages.** Anything the user doesn't know and can't be confirmed gets a published
   average, written into the offer with its source and the word "assumption" (for example a standard
   8-hour, 22-day month; a laptop spread over its 3 to 5 year life). Never a made-up number.
4. **Write the offer TOON** (shape in the [example](../examples/th3r-web-service/offer.toon)): fee,
   hours, `costs` rows tagged `living` or `business`, target income, packages with estimated hours.
5. **Price.** `python3 scripts/offer.py price <offer.toon>`:

   ```
   break-even per hour = all monthly costs / working hours
   target per hour     = (target income + business costs) / working hours
   listed per hour     = rate / (1 - platform fee)
   ```

   Each package is LOSS (its hours exceed what the price covers at break-even), UNDER TARGET, or ok.
   Fix every LOSS by cutting scope or raising the price, then rerun.
6. **Place it in the market.** Compare with the sample: a starter near or above the cheapest-package
   median is fine when the scope is clearly bigger than template work; say why in the listing.
7. **Add the ongoing package** (maintenance per month, Session as the unit if the platform has no
   Month) and an extra-hour rate at the listed target rate, rounded up.

## Done when

- `offer.py price` shows no LOSS, and every assumption in the offer has a source.
- The prices sit inside the measured market, or the listing explains why not.
