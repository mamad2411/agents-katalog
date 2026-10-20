---
name: cook-a-burger
domain: daily
subdomain: food
locale: [generic]
interface: physical
difficulty: basic
est_time: 25min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Cook a juicy burger with a browned outside, safe interior temperature, and a patty that stays flat enough to fit the bun.

## Preconditions

- Ground beef, buns, salt, pepper, and desired toppings are ready.
- A skillet, grill, or griddle is clean and can be heated safely.
- An instant-read thermometer is available if exact doneness matters.

## Steps

1. **Portion the meat.** Divide cold ground beef into loose 115 g to 170 g portions without kneading or squeezing it smooth. → *Expect:* each portion holds together but still has a rough, craggy surface.
2. **Shape gently.** Pat each portion into a disk slightly wider than the bun and about 2 cm thick. → *Expect:* the patty looks even, with edges that are not cracked apart.
3. **Dimple the center.** Press a shallow thumbprint into the middle of each patty so it will not dome while cooking. → *Expect:* the center is lower than the rim by about 5 mm.
4. **Salt the outside only.** Season both faces with salt and pepper right before cooking, not while mixing the meat. → *Expect:* seasoning is visible on the surface and the meat has not been overworked.
5. **Heat the cooking surface.** [BRANCH: skillet or griddle | grill] heat to medium-high until a drop of water sizzles hard, or the grill grate is hot and brushed clean. → *Expect:* the surface is hot enough to brown within the first minute.
6. **Cook the first side.** Set the patty down and leave it alone for 3 to 5 minutes, depending on thickness. → *Expect:* the bottom develops a deep brown crust and releases with a thin spatula.
7. **Flip once.** Turn the patty one time and do not press it flat with the spatula. → *Expect:* juices stay in the burger and the browned side faces up intact.
8. **Cook to doneness.** Use temperature if possible: 63 C for medium with a rest, or 71 C for well done and food safety for ground beef. → *Expect:* the thermometer tip in the center reads the chosen target.
9. **Add cheese if using.** Place cheese on during the last minute and cover briefly with a lid or metal bowl. → *Expect:* cheese softens and droops without burning.
10. **Rest the burger.** Move the patty to a plate for 3 to 5 minutes before putting it on the bun. → *Expect:* juices settle and the bun does not immediately turn soggy.

## Decision points

- Patty is very lean → use lower heat and stop at well done rather than chasing a hard crust.
- Patty is thicker than 2.5 cm → reduce heat after browning and cook longer so the outside does not burn first.
- Cooking for children, pregnant people, older adults, or immunocompromised people → use 71 C as the target.

## Failure modes & recovery

- **F1 Puffy center:** detect a rounded patty that no longer fits the bun, recover by pressing a center dimple deeper next time, not by smashing mid-cook.
- **F2 Tough texture:** detect a dense, sausage-like bite, recover by handling the meat less and salting only the outside.
- **F3 Burned outside raw inside:** detect black crust with a cold center, recover by lowering heat and finishing covered until the center reaches target temperature.
- **F4 Sticking patty:** detect tearing when lifted, recover by waiting another minute for the crust to release.

## Verification

The burger has a browned crust, rests at least 3 minutes, and the center reaches the chosen doneness temperature.

## Variations

- `smash-burger`: use a smaller ball, smash once immediately on a ripping-hot griddle, and skip the center dimple.
- `turkey-or-chicken`: cook to 74 C and oil the surface well because lean poultry sticks easily.

## Safety & privacy

Medium risk from hot fat, smoke, and undercooked ground meat. Wash hands and utensils after touching raw meat, keep raw juices away from toppings, and ventilate if the pan smokes.
