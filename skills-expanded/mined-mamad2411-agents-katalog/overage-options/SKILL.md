---
name: overage-options
description: Price every way out of being over the baggage allowance — prepaid extra bag, airport excess, overweight bands, cabin-bag upsell, fare upgrade, shipping the difference, or leaving it — and recommend the cheapest that actually works for this itinerary. Use when the user is over their allowance, asks what excess baggage will cost, or asks whether to pay for another bag. Writes overage.md.
allowed-tools: Read, Write, Edit, Bash(python3 *), WebFetch, WebSearch, Grep, Glob
---

# Overage Options

Being over the allowance is a purchasing decision under time pressure, and it is routinely
made badly at the desk because nobody has the numbers. This skill produces the numbers before
the airport.

## The options, in the order they are usually worth checking

**1. Prepay online before departure.** Almost always the cheapest way to add a bag, frequently
half the airport price, and it is the option that disappears — most carriers close online bag
purchase somewhere between 24 hours and 1 hour before departure. Find the actual cutoff for
this carrier and state it as a deadline with a date and time, because it is the only option on
this list with an expiry.

**2. Redistribute instead of paying.** Before pricing anything: is the itinerary over in total,
or over on one bag? A 26 kg bag beside a 19 kg bag under a piece concept costs an overweight
fee for nothing. Run `/travel-packing-assistant:plan` first. Under a weight concept, redistribution buys
nothing at all and this step is skipped — which is why the piece-vs-weight determination in
`allowances.yaml` matters here.

**3. Overweight band vs an extra piece.** Two different fees. On many carriers a second checked
bag costs less than the overweight surcharge on the first, which means the cheapest fix for a
28 kg bag is to buy a bag and move 5 kg into it — and the traveller needs a spare bag to do it,
so this has to be decided at home. Compare explicitly, both directions.

**4. Cabin upsell.** On carriers whose cheap fares exclude a cabin bag, adding one is often the
cheapest kilogram available, and it moves weight the checked scale never sees.

**5. Fare or cabin upgrade.** Occasionally the fare-brand step up (which includes bags) costs
less than buying the bags separately, especially where two travellers are each paying. Check it
when the bag fees get into that range; do not check it reflexively.

**6. Ship it.** Post or courier the excess to the destination. Real comparison, not a throwaway
suggestion — it is frequently cheaper per kilogram than airline excess, especially for
non-urgent bulk. Price it properly: service, transit time against the trip dates, customs
exposure on the value being shipped, and whether anyone will be at the destination address to
receive it. A parcel that arrives after the traveller leaves is not a saving.

**7. Wear it.** Coats, boots, loaded jacket pockets. Free, immediate, socially normal, and
worth a few kilograms. Always mention it; never present it as the whole answer.

**8. Leave it.** `/travel-packing-assistant:leave-behind` ranks what to drop. This is the option that
gets chosen by default at the desk when none of the others were prepared.

## Getting the prices right

- Fees are **per segment or per journey** depending on the carrier and whether bags are
  through-checked. Getting this wrong is a factor-of-two error. State which applies and where
  you read it.
- Fees are quoted in the point-of-sale currency. Convert to the user's currency with an FX
  source (`mcp__gateway__fx__convert` where available), and show both — the amount they will
  be asked for is the local one.
- The same escalation ladder as policy research applies to fetching fee tables: plain page fetch
  first, then a residential-egress server-side fetch, then a browser, then ask the user to
  paste. Excess-fee pages are among the most aggressively geo-varied pages an airline serves.
- Record the source and date for every fee, exactly as in `allowances.yaml`. A fee schedule
  from a blog post is not a price.

## Output

Write `overage.md` in the workspace containing:

1. The shortfall, in kilograms, per bag and in total, stated first.
2. A costed table: option, what it takes, cost in local currency and the user's, deadline if
   any, and whether it requires anything the user does not already have (a spare bag, a scale,
   someone at the destination).
3. A recommendation — one option, named, with the reason in a sentence, and the runner-up.
   Make the call; do not hand back a menu.
4. The **decision deadline**, as an absolute date and time: the earliest cutoff among the
   options worth keeping open.

Then say the one thing that is easy to miss: if the excess is being paid anyway, the marginal
kilogram is usually free up to the next band, so there is no reason to leave things behind
once the fee is committed.
