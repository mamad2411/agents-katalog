---
name: chef-food-safety
description: >-
  Food-safety authority for cooking temperatures, cross-contamination, cooling,
  thawing, leftovers, raw or undercooked animal foods, vulnerable eaters and
  allergen handling. Use whenever safety is material, food sat out or storage
  history is uncertain, severe allergies are involved, or a recipe uses raw,
  low-temperature, preserved or otherwise high-risk food.
---

# Chef Food Safety

Safety controls are not texture preferences. Use current, applicable public-health guidance and state which jurisdiction/source governs when a number matters. Read `references/haccp-home.md` for the storage and decision tables.

## Cooking endpoints

For ordinary home cooking using the current FoodSafety.gov chart:

- Poultry, including ground poultry and stuffing inside poultry: **74°C internal**.
- Ground beef, pork, veal, lamb and comparable non-poultry ground meat: **71°C internal**.
- Whole cuts of beef, pork, veal and lamb: **63°C internal + 3 minute rest**.
- Fin fish: **63°C**, unless using another species-specific official endpoint.

Use a food thermometer where an objective endpoint governs safety. Color, clear juices, firmness, shrimp curl, or a timer can help with quality but do not replace the required check. Low-temperature/sous-vide cooking is a separate complete time-temperature-thickness process; never convert a bath setting into a pasteurization claim by itself.

## Cross-contamination

Keep raw animal foods and their tools away from ready-to-eat food. Do not wash raw poultry. Wash hands and contaminated surfaces at raw-to-ready transitions. A marinade that contacted raw meat must be treated as raw unless it is subsequently handled by an applicable safe process; reserving a clean portion before contact is the simplest sauce path.

For allergies, check the actual label and the guest's stated restriction. Shared fryers, boards, utensils, condiment jars and preparation surfaces can create cross-contact. Never infer that `plant-based`, `tamari`, `ghee`, `gluten-free style`, or another category word proves a product is safe for a specific allergy.

## Cooling, storage and reheating

Refrigerate perishable leftovers promptly in shallow portions; do not leave a large hot pot at room temperature to "cool first" for hours. General leftover windows and rice-specific rules differ; choose the product-specific rule rather than averaging them.

This library uses the Food Standards Agency's conservative rice rule when no other jurisdiction is specified: cool cooked rice quickly, refrigerate it, use within **24 hours**, and reheat no more than once until steaming hot throughout. Boiling or reheating food does **not** reset its previous storage history.

If time/temperature history is unknown and the missing fact changes the safety decision, ask that one fact or recommend discarding rather than inventing a safe history.

## Raw seafood and other special cases

Freezing can reduce parasite risk for appropriate fish but does not kill all harmful germs. `Sushi-grade` is not a complete safety process. For raw/undercooked seafood, use an applicable current method and supplier information; the safest default is thorough cooking.

For home canning, fermentation, curing and garlic/herbs in oil, route to `chef-fermentation-preservation` and use a validated product-specific method. Shelf stability cannot be inferred from flavor, smell, salt percentage or one pH statement alone.

## Vulnerable eaters and medical constraints

Pregnancy, young children, older adults and immunocompromised people can have stricter public-health guidance. Apply the user's known requirement or the applicable authority; do not invent a universal "extra strict" diet or storage window. Medical nutrition belongs to `diet-medical-adaptation` and must translate explicit restrictions rather than diagnose.

## Discard rule

Bulging/leaking shelf-stable containers, obvious spoilage, unsafe time-temperature history or a failed validated preservation process are not rescue projects. Do not taste food to prove it is safe.

Sources and project-level responsibility language: see `/SAFETY.md` and `/DISCLAIMER.md`.
