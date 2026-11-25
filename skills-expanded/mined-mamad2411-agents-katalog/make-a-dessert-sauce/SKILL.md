---
name: make-a-dessert-sauce
domain: daily
subdomain: food
locale: [generic]
interface: physical
difficulty: basic
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-22
---

## Goal

A simple dessert sauce, either chocolate ganache or berry coulis, with pourable consistency.

## Preconditions

- For ganache: chocolate and cream.
- For berry coulis: berries, sugar, lemon juice, and optional strainer.
- Small saucepan or microwave-safe bowl, spoon, and heat-safe jar.

## Steps

1. **Choose the sauce.** [BRANCH: ganache | coulis] use chocolate and cream for rich sauce, or berries and sugar for fruit sauce. → *Expect:* ingredients match one path.
2. **Set the ratio.** For ganache, use equal weights chocolate and cream; for coulis, use 2 cups berries to 2 to 4 tbsp sugar. → *Expect:* sauce base is measured before heating.
3. **Make ganache gently.** Heat cream until steaming, pour over chopped chocolate, wait 2 minutes, then stir from the center. → *Expect:* chocolate melts into a glossy sauce.
4. **Make coulis gently.** Simmer berries, sugar, and 1 tsp lemon juice for 5 to 8 minutes. → *Expect:* berries collapse and release syrup.
5. **Adjust consistency.** Thin ganache with warm cream, or reduce coulis by simmering; strain coulis if smoothness matters. → *Expect:* sauce coats a spoon but still pours.
6. **Taste warm.** Add a pinch of salt to ganache or more lemon to coulis if flavor tastes flat. → *Expect:* sweetness has contrast and does not taste dull.
7. **Serve at the right temperature.** Serve ganache warm or room temperature; serve coulis warm, room temperature, or cold. → *Expect:* texture flows over cake, ice cream, pancakes, or fruit.
8. **Store and rewarm.** Refrigerate covered and rewarm ganache gently. ⚠️ *Irreversible:* overheated chocolate can split or scorch, so use gentle heat and stop early. → *Expect:* leftover sauce is covered and labeled.

## Decision points

- Need a glaze → ganache should be warm and fluid, not hot.
- Need a plate drizzle → coulis should be strained and slightly reduced.
- Berries are very tart → start with more sugar, then correct with lemon only at the end.
- Chocolate is very dark → add a little extra cream or sugar if bitterness dominates.

## Failure modes & recovery

- **F1 Split ganache:** chocolate overheated or liquid added too fast; whisk in 1 tsp warm cream at a time from the center.
- **F2 Grainy ganache:** chocolate was not chopped fine enough; warm gently over a water bath and stir slowly.
- **F3 Watery coulis:** berries released lots of juice; simmer uncovered until it coats a spoon.
- **F4 Flat berry flavor:** lacks acid or salt; add lemon juice a few drops at a time.

## Verification

The dessert sauce is smooth enough for its use, tastes balanced, and pours or drizzles without running like water.

## Variations

- `white-chocolate`: use 2 parts white chocolate to 1 part cream for similar thickness.
- `raspberry`: strain seeds for a polished coulis.
- `mixed-berry`: combine berries and adjust sugar after simmering.

## Safety & privacy

Low risk. Avoid steam burns, heat chocolate gently, and refrigerate dairy or cooked fruit sauces promptly.
