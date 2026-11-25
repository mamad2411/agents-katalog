---
name: packing-inventory
description: Build or update the inventory of what is being carried — items, quantities, weights, carriage restrictions, and how replaceable each thing is at the destination. Use when the user is listing what they have packed or intend to pack, dictating the contents of a bag, or asking what is in their luggage. Writes inventory.yaml, which the solver and the leave-behind ranking both read.
allowed-tools: Read, Write, Edit, Bash(python3 *), Bash(ls *), Grep, Glob
---

# Packing Inventory

`$TPA` below is this plugin's `new-workspace` skill directory — the folder holding its `SKILL.md`,
`scripts/`, `schema/`, `typst/` and `template/`. Find it by name in your tool's skills folder (some
tools prefix it, e.g. `travel-packing-assistant__new-workspace`) and set `TPA` once per session.

The inventory is the input everything else depends on. A plan built on a half-inventory is a
plan for a bag that does not exist.

It does not have to be complete to be useful — `/travel-packing-assistant:weigh` reconciles the itemised
total against the actual scale reading and reports the gap, so a partial inventory is honest
rather than wrong. What it must not be is *silently* partial.

## Capture modes

Offer whichever fits what the user is doing right now. Do not force a mode.

**Dictation.** The user talks through a bag; you write items as they go. Fastest for a bag
already packed. Batch back a confirmation every ten items or so rather than after each one.

**Photograph.** The user lays the contents out and photographs them. Open the image, list
what you can identify, and ask about anything ambiguous. Good for clothing, poor for weights —
everything from a photo is `weight_source: estimated`.

**Category sweep.** For packing not yet done: walk the categories in
`data/packing-categories.md` and ask what is going in each. Slower, but it is the only mode
that catches the thing they have not thought of yet.

**Import.** A previous trip's `inventory.yaml` is the best starting point a repeat traveller
has. If the user names an earlier trip workspace, read its inventory, carry over the items and
their measured weights, and ask only what changed.

## Weights

Ask how much of the inventory can be weighed. In descending order of usefulness:

1. **Measured** — a kitchen scale, in grams. Ten minutes of weighing the heavy end of the list
   (shoes, chargers, books, toiletries, outerwear) removes most of the uncertainty, because
   weight distribution in luggage is strongly top-heavy: a small number of items usually
   account for the majority of the mass.
2. **Vendor / catalogue** — a published spec weight for electronics and hardware. Usually
   accurate, usually excludes the cable and the case, so weigh those separately.
3. **Estimated** — from `data/typical-weights.md`. Fine for socks, not for a laptop.

Record which, per item, in `weight_source`. That field is what lets `reconcile.py` tell the
difference between "the inventory is missing items" and "the estimates are drifting".

Weigh **containers separately**: a bag's `tare_kg` and each packing cube's `tare_kg` belong in
`bags.yaml`, not as inventory items. Double-counting an empty suitcase is the classic way to
produce a plan that is 4 kg pessimistic.

## The fields people skip and later need

- **`carriage`** — anything that cannot travel in an arbitrary bag. Power banks and spare
  lithium batteries are cabin-only in essentially every jurisdiction; liquids over 100 ml
  cannot go through the cabin security check; sharps, tools and some aerosols are
  checked-only or barred. See `data/carriage-rules.md`. Set `carriage_reason` every time; the
  solver treats these as hard constraints and the reason is what the traveller reads when they
  wonder why the plan put a heavy thing in the small bag.
- **`tier`** — essential / useful / nice-to-have / expendable. Assign it as you capture, not
  later. Ranking forty items under time pressure at a check-in desk does not work; ranking
  them at home does.
- **`replaceable_at_destination`** — can it be bought at the other end, and roughly for how
  much. This is the field that makes the leave-behind list sensible: a 900 g bottle of shampoo
  that costs $4 to replace is the correct thing to abandon, and no weight-only ranking can
  know that.
- **`value`** — replacement cost. Used with weight to rank; also the honest answer to whether
  something belongs in a checked bag at all.

## Procedure

1. Read `inventory.yaml` and `bags.yaml`. If bags are not defined yet, define them first —
   an item cannot be assigned to a bag that does not exist.
2. Capture in the mode the user chose. Assign stable ids (`I001`…) and never renumber; the
   plan, the PDFs and the conversation all reference them.
3. Fill `carriage`, `tier` and `replaceable_at_destination` as you go.
4. Validate: `python3 $TPA/scripts/validate.py . --json`.
5. Report: item count, itemised total in kg, the split by `weight_source`, and the ten heaviest
   items. The heavy-ten list is the single most useful thing to show a traveller — it is where
   every kilogram of headroom is going to come from.

## Pinning

If the user says something must stay in a particular bag — documents in the cabin bag,
a gift that must not be crushed — set `assigned_bag` and `pinned: true`. The solver will
place it first and refuse to move it, and will report an error rather than quietly relocating
it if the pin makes the pack infeasible.
