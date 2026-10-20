---
name: build-a-balanced-plate
domain: daily
subdomain: food
locale: [generic]
interface: physical
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

A meal plate is assembled with satisfying portions of vegetables or fruit, protein, starch or grain, fat, and flavor.

## Preconditions

- Ready-to-eat foods or cooked components, plate or bowl, serving utensils, and knowledge of allergies or dietary needs.
- Perishable foods have been stored safely.

## Steps

1. **Start with produce.** Fill about half the plate with vegetables, fruit, or both. → *Expect:* plate has color, volume, and fiber-rich food.
2. **Add protein.** Fill about one-quarter with beans, tofu, eggs, dairy, fish, poultry, meat, or another protein. → *Expect:* portion is palm-size or otherwise adequate for the eater.
3. **Add starch or grain.** Fill about one-quarter with rice, bread, pasta, potatoes, corn, oats, or another staple. → *Expect:* meal has an energy source that fits appetite and activity.
4. **Add fat and sauce.** Include oil, nuts, avocado, cheese, dressing, or sauce in a moderate amount. → *Expect:* food tastes rounded and not dry.
5. **Check flavor contrast.** Add acid, herbs, spice, crunch, or salt if needed. → *Expect:* each bite tastes intentional rather than bland.
6. **Adjust for the eater.** [BRANCH: child | athlete | medical diet] Change portions according to hunger, activity, and professional guidance. → *Expect:* plate fits the person rather than a rigid diagram.
7. **Serve safely.** Keep hot foods hot and cold foods cold until eating. → *Expect:* meal is appetizing and perishable items have not sat out over 2 hours.

## Decision points

- Meal is a soup, stew, or bowl → judge balance by ingredients, not by physical plate sections.
- Appetite is low → prioritize protein and nutrient-dense foods in smaller portions.
- Medical nutrition advice applies → follow the clinician's plan over generic plate ratios.

## Failure modes & recovery

- **F1 All starch:** detect plate is mostly bread, rice, pasta, or potatoes → add produce and protein.
- **F2 Not filling:** detect hunger soon after eating → add protein, fat, or fiber next time.
- **F3 Too bland:** detect untouched vegetables or flat taste → add acid, seasoning, or sauce.
- **F4 Unsafe holding:** detect dairy, meat, rice, or cut produce left out over 2 hours → discard risky items.

## Verification

The plate includes produce, protein, starch or grain, some fat or sauce, and is portioned for the eater's needs while perishable food remains safely held.

## Variations

- `plant-based`: combine legumes, soy, nuts, seeds, or whole grains for protein.
- `breakfast`: use fruit or vegetables, eggs or yogurt, oats or toast, and nuts or butter.
- `packed-lunch`: choose foods that keep texture and remain safe with an ice pack if needed.

## Safety & privacy

Low risk. Respect allergies, religious diets, and medical nutrition privacy, and keep perishable cooked foods out of the danger zone as little as possible.
