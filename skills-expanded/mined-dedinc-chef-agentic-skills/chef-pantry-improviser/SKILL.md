---
name: chef-pantry-improviser
description: >-
  Cook from what's actually available — building dishes from a list of on-hand ingredients, substituting missing ingredients in any recipe, and adapting recipes to a real pantry. Use whenever the user lists what's in their fridge ("у меня есть курица, рис и морковка, что сделать?"), says they're missing an ingredient, wants to avoid a store run, or needs to use up leftovers before they spoil.
---

# Chef Pantry Improviser

Improvisation is not "throw it all in a pan" — it is slotting available ingredients into proven dish templates. Every successful improvised dish is a known structure wearing different clothes.

Read `references/substitutions.md` for the ingredient substitution matrix.

## Step 1 — Inventory triage

Sort what the user has into roles:
- **Protein** (meat, fish, eggs, legumes, cheese, tofu)
- **Starch/base** (grains, pasta, potatoes, bread)
- **Vegetables** (fresh, frozen, canned, pickled)
- **Flavor makers** (onion, garlic, spices, sauces, stock cubes, tomato paste, dairy, citrus, herbs)
- **Perishability**: what dies first cooks first. Ask what's oldest if leftovers are involved.

Assume the invisible pantry (salt, oil, pepper) unless told otherwise; confirm anything critical.

## Step 2 — Match to a template

A dish needs: protein + starch (optional) + vegetable + flavor system + fat + acid. Pick the template that the available flavor makers can support:

| Template | Skeleton | Minimum viable |
|---|---|---|
| Fried rice / grain fry | Day-old grain + hard heat + protein bits + veg + soy/egg | Rice, eggs, any allium |
| Frittata / omelet bake | Eggs + anything sautable + cheese optional | 4+ eggs, one vegetable |
| Pasta of what-there-is | Pasta + fat/emulsion + 1–2 accents + pasta water | Pasta, garlic, oil or butter |
| One-pot rice (plov-adjacent) | Sautéed protein/veg + rice + measured liquid | Rice, onion, any protein |
| Soup from bones/cube | Aromatic sweat + liquid + starch + protein | Stock cube, onion, potato |
| Stir-fry | Hot pan + protein + staged veg + soy-based sauce | Any protein, any crisp veg |
| Traybake | Everything cut even + oil + 210°C | Any protein + root veg |
| Curry/stew direction | Onion base + spices + tomato/coconut/cream + protein | Onion, canned tomato, any spice spine |
| Grain/legume bowl | Warm base + roasted veg + dressing + crunch | Any grain + any veg + vinaigrette |
| Savory pancakes/fritters | Grated veg + egg + flour + pan-fry | 1 vegetable, 1 egg, flour |

The user's flavor makers determine the direction (see regional pantry spines in `chef-spice-guide`): soy+ginger → stir-fry; sour cream+dill → Eastern European; canned tomato+oregano → Mediterranean; curry powder+coconut/cream → curry.

## Step 3 — Substitute like a chef

Substitute by ROLE, not by name. Ask: what does this ingredient do here — acid? fat? body? aroma? crunch? Then swap within the role (matrix in references). Rules:
- Aromatics are flexible (onion↔leek↔shallot); structural ingredients are not (see baking guide for baking limits).
- Never substitute more than 2 core items in an unfamiliar recipe — beyond that, switch to a template dish instead of pretending it's the same recipe.
- State the flavor cost honestly: "dried herbs work here, you lose the fresh finish — compensate with lemon zest."

## Step 4 — Sanity-check and format

Run the resulting dish through the standard engineering rules (salt %, acid, texture contrast, browning — see `chef-recipe-developer`) and present it in the standard recipe format, flagging which parts were improvised and what to buy next time to unlock better versions.

## Leftover safety
- Reheat once, fully hot (not warm). Rice: fridge within 1 h of cooking, use within 24 h, reheat thoroughly.
- Cooked meat: 3–4 days fridge. Cooked fish: 1–2 days, best repurposed cold or in fish cakes.
- When in doubt about smell/slime — out. No dish is worth it.
