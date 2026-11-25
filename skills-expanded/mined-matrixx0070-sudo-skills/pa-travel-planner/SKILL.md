---
name: pa-travel-planner
version: 1.0.0
description: Plan a trip end to end — itinerary, ranked options, and budget — with booking only on explicit approval.
author: matrixx0070
tags: [travel, itinerary, budget, planning, personal-assistant]
capabilities: []
---

## When to use

Use this when the owner wants a trip planned: flights, lodging, transport, activities, and a budget laid out as decision-ready options. Good for a weekend getaway, a family holiday, or a complex multi-city route the owner wants pre-digested.

**Not for:** booking without sign-off, expense reconciliation after a trip, or visa/legal advice (flag those to a professional). You plan and price; the owner books.

## Method

1. Collect constraints: dates (or flexibility), origin, destination(s), party size, total budget, and trip style (relax, adventure, culture, mix).
2. Decision point — are dates flexible? If yes, note cheaper adjacent dates; if fixed, plan around them.
3. Draft a day-by-day itinerary skeleton first (arrive, anchor activities, rest, depart) before pricing anything.
4. For each big-ticket item (flight, lodging), give 2-3 ranked options with the tradeoff named (cheapest / best-value / most convenient).
5. Build a budget table summing every category against the stated cap. Decision point — over budget? Flag it and propose specific cuts rather than hiding the overage.
6. Add logistics: transfers, check-in times, a packing note, and one backup for weather-dependent plans.
7. Present the full plan. Confirm before booking anything or contacting a hotel/host — booking spends money and is a hard stop.

## Example

Input: Lisbon, 4 days, 2 people, $1,800, culture + food.
Output: Day-by-day (Alfama walk, Belem, Sintra day trip, food tour). Flights: A $520 nonstop (best-value), B $410 one-stop (cheapest). Hotel: 3 nights central $360. Budget total $1,690 — under cap, $110 buffer. Next: pick a flight and I will prep the booking for your approval.

## Pitfalls

- Booking or "holding" anything before explicit approval — this spends the owner's money.
- One option only. Always give ranked alternatives so the owner actually decides.
- Ignoring transfer/buffer time between segments; a 45-min layover with a gate change fails.
- Quoting stale prices as guaranteed. Label prices as estimates to reconfirm at booking.

## Output format

```
TRIP PLAN — [destination] — [dates] — [party] — budget [cap]

ITINERARY
Day 1: [morning / afternoon / evening]
...
OPTIONS
Flight: A) [detail] $[x] (best-value)  B) [detail] $[x] (cheapest)
Stay:   A) [detail] $[x]  B) [detail] $[x]
BUDGET
Flights [x] | Stay [x] | Food [x] | Activities [x] | Transfers [x] = [total] vs [cap]
LOGISTICS: [transfers, check-in, packing, backup]

Next: pick options and reply APPROVE to prep bookings — nothing is booked yet.
```
