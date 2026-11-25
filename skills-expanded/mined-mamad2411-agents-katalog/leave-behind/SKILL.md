---
name: leave-behind
description: Produce a ranked emergency leave-behind list — what to abandon, in what order, to get under the allowance, ranked by cost per kilogram saved and by whether the item can be re-bought at the destination. Use when the user is overweight and willing to leave things, asks what to drop, or wants a contingency list for the check-in desk. Writes leave-behind.md.
allowed-tools: Read, Write, Edit, Bash(python3 *), Grep, Glob
---

# Leave Behind

The list you want to have already made when a scale reads 26.4 kg and there is a queue behind
you. Deciding what to abandon takes ten calm minutes at home and goes badly in ninety seconds
at a counter.

Only run this when the user has said they are willing to leave things. It is not the first
answer to being overweight — `/travel-packing-assistant:overage` prices the alternatives, and paying a
fee is frequently the better deal.

## The ranking

Not "heaviest first". The right ordering is **cost per kilogram saved**, where cost accounts
for what it takes to undo the decision:

```
cost_per_kg = effective_cost / kilograms_saved

effective_cost = replacement cost at the destination, if it can be bought there
               = full value, if it cannot
               = ∞, for anything essential or irreplaceable
```

Which is why `replaceable_at_destination` in the inventory earns its place. A 900 g bottle of
shampoo replaceable for $4 ranks far above a 200 g charger that costs $60 and a trip to a shop
in a city the traveller does not know — even though the charger is lighter.

`scripts/pack_solver.py --overflow` computes this ranking and writes it to `plan.yaml` under
`overflow_ranking`. Read it rather than re-deriving it by eye.

## Categories that reliably top the list

Check these before anything else — they are where most travellers are carrying dead weight:

- **Liquids and toiletries.** Dense, cheap, available everywhere. Full-size shampoo,
  conditioner and shower gel are frequently 1.5–2 kg between them, and are the single most
  common thing worth abandoning.
- **Water.** Empty every bottle before weighing. A litre is a kilogram.
- **Paper.** Books, printouts, magazines. Heavy, and mostly duplicable on a phone.
- **Duplicates.** The third pair of jeans, the second charger of the same type, spare cables.
- **Shoes.** A pair of shoes is often 0.8–1.2 kg. Wear the heaviest pair; drop the third pair.
- **Packaging.** Boxes, blister packs, original cartons for things bought on the trip. Often
  hundreds of grams per item and no function past the shop door.

And the categories that must **never** enter the ranking regardless of weight: medication and
its documentation, passports and travel documents, prescription glasses, medical devices, keys,
and anything with a value that is not financial. Mark these `tier: essential` in the inventory
so the ranking cannot reach them.

## Where the abandoned things go

Say this explicitly, per item, because "leave behind" at an airport usually means a bin:

- **Given to whoever is at the airport** — the best outcome, available only if someone drove.
- **Posted from the airport** — many terminals have a post office or a shipping desk landside.
  Only useful for compact, valuable items, and only before security.
- **Left at home** — for the outbound leg, this is really "removed from the bag now", which is
  the whole point of doing this at home.
- **Binned.** The default, and the reason to have ranked properly.

## Output

Write `leave-behind.md` with:

1. The shortfall in kilograms, stated first, and which bag it is in.
2. The ranked table: item, weight, where it currently is (bag and cube — the traveller has to
   physically find it), cost per kg saved, replaceable at destination, and the **running
   cumulative saving**. The cumulative column is the operative one: it says where to stop.
3. A marked **stop line** — the point at which the bag comes under the limit, with the margin
   at that point.
4. A short physical procedure: which bag to open, which cube the first three items are in, and
   what to do with them. The cube assignment is what makes this executable at a counter in
   under a minute.

Keep the list to what is actually needed plus roughly 30% margin. A ranking of forty items is
a document nobody reads under pressure; ten is a list someone can act on.
