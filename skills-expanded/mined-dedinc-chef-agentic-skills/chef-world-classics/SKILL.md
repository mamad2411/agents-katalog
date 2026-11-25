---
name: chef-world-classics
description: >-
  Iconic world dishes engineered for home conditions — pizza (any oven), sushi/rolls at home, ramen, pasta carbonara/bolognese, burgers, tacos, shawarma/gyros, pad thai, khinkali/dumpling family, and plov. Each with the authentic benchmark, the realistic home version, and condition-based adaptations (weak oven, no special gear, ingredient scarcity). Use whenever the user wants to make a famous dish "like the real one" or asks how to adapt one to their kitchen.
---

# Chef World Classics

Every iconic dish has a SOUL (the 2–3 things that make it *that dish*) and a COSTUME (traditional gear and ingredients). Home cooking succeeds by protecting the soul and re-tailoring the costume to your conditions. This skill defines both per dish — so adaptations stay honest instead of becoming a different dish with a famous name.

Read `references/dish-specs.md` for full per-dish specs (benchmark → home method → adaptations → failure points).

## The adaptation method (works for any dish not listed)

1. **Name the soul.** Pizza = charred chewy crust + restrained toppings. Carbonara = silky egg-cheese emulsion, NO cream. Sushi = seasoned rice at body temp + impeccable fish. Ramen = broth depth + alkaline noodles. If you can't name the soul, research before cooking (find 2–3 authoritative versions, extract what's constant — that's the soul; what varies is the costume).
2. **Map your constraint against the soul.** Weak home oven vs pizza's 400°C need → the crust mechanism must be replaced (steel/skillet tricks), not ignored. No verified raw-fish safety path → change the FILLING to a cooked option; never let a label substitute for the required process.
3. **Replace mechanisms, not just ingredients** (chain `chef-equipment-gastrophysics`): tandoor → screaming skillet + broiler; wok hei → smaller batches + max heat + finishing smoke note; charcoal → smoked paprika + proper crust honesty.
4. **Declare the trade.** Tell the user what the home version loses and what it gains (usually: 90% of the pleasure at 20% of the logistics). An honest "skillet pizza ≠ Naples, but it's GREAT" beats cosplay.

## Universal condition-adaptations

| Constraint | Strategy |
|---|---|
| Weak oven (max 220–250°C) | Preheated steel/cast-iron/upturned tray 45 min; broiler combo; skillet-start-oven-finish; thinner formats |
| No specialty ingredient | Substitute by ROLE via `chef-pantry-improviser`; if the soul-ingredient is missing (kimchi for kimchi-jjigae), postpone or pivot honestly |
| No special tool (wok/tandoor/steamer) | Mechanism replacement table in references; improvised steamer = plate on foil balls in a lidded pot |
| Raw-fish safety unavailable | Cooked/cured/vegetable versions of sushi (fully legitimate in Japan too); never "probably fine" fish — see `chef-food-safety` |
| Time poverty | Each spec includes the "weeknight cut": which corner cuts cost 10% and which cost the soul |
| One burner / hostel kitchen | Chain `chef-constraints-adaptation` — sequencing beats simultaneity |

## Quality benchmarks (how to know you nailed it)
Each dish spec ends with 2–3 objective checks, e.g.: pizza — underside leoparding, slice holds horizontal for one beat then droops; sushi rice — grains distinct, holds shape but collapses in the mouth, seasoned enough to eat alone; carbonara — sauce coats and flows like heavy cream, zero scrambled flecks; ramen — broth coats lips slightly (gelatin), noodles retain bite through the bowl. Cook to benchmarks, not vibes — this is the professional habit (`chef-training-progression`).
