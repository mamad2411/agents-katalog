---
name: defrost-frozen-food
domain: daily
subdomain: food
locale: [generic]
interface: physical
difficulty: basic
est_time: 30min
risk: medium
prerequisites: [daily/food/store-leftovers]
status: draft
last_verified: 2026-07-20
---

## Goal

Frozen food is thawed by one of the three safe methods and cooked on the right timeline, without ever taking a bath in the danger zone on the counter.

## Preconditions

- Frozen food and a plan for when it will be cooked, because the method is chosen by lead time: overnight (fridge), an hour (cold water), or now (microwave or cook-from-frozen).
- The one rule above all: **meat, fish, and poultry never thaw on the counter.** Room-temperature thawing warms the outside into the bacterial danger zone while the core is still frozen (`daily/food/store-leftovers`'s 2-hour logic applied in reverse).

## Steps

1. **Choose the method by lead time.** [BRANCH: cooking tomorrow → fridge | cooking within the hour or two → cold water bath | cooking right now → microwave defrost, or cook straight from frozen where the food allows] → *Expect:* a method matched to the clock, chosen before anything leaves the freezer.
2. **Fridge method: transfer to a plate or container on a low shelf.** The plate catches drips; the low shelf protects everything below (`embodied/kitchen/store-groceries`'s raw-meat-below rule). Allow roughly 12 to 24 hours for typical portions, a full day per couple of kilos for large items. → *Expect:* food thawing slowly at safe temperature; thawed items then keep a day or two in the fridge, which makes this the most forgiving method.
3. **Cold water method: submerge in a sealed bag in cold tap water, changing the water every 30 minutes.** Sealed matters (waterlogged food and contaminated water both ruin things); cold matters (warm water is the counter problem with extra steps). Small portions thaw in under an hour. → *Expect:* water refreshed on schedule; food pliable within the hour; **cook immediately after**.
4. **Microwave method: use the defrost setting with the weight entered, turning and separating as prompted.** Edges will start cooking slightly; that is the method's tradeoff. → *Expect:* thawed, possibly part-warm food; **cook immediately after**, because parts of it just visited warm temperatures.
5. **Cook-from-frozen where it works.** Vegetables, dumplings, thin fish fillets, burger patties, and most prepared foods cook honestly from frozen with a few extra minutes; packaging often says so. Large roasts and whole poultry do not. → *Expect:* the packet's from-frozen instructions followed, core cooked through (juices clear, or steaming-hot centers per `daily/food/use-a-microwave`'s standard).
6. **Verify the thaw before cooking normally.** Flexible, no ice crystals in the center, a knife meets no frozen core. → *Expect:* fully thawed texture, then straight into the planned cooking.

## Decision points

- Forgot to thaw and dinner is soon: the honest ranking is cook-from-frozen (if the food allows) > cold water > microwave; the counter is not on the list.
- Bread and baked goods: counter-thawing is fine for them; the danger-zone rule is about meat, fish, dairy, and cooked leftovers.
- Refreezing: raw food thawed in the fridge may be refrozen (with some quality loss); anything thawed by water or microwave gets cooked first and may be refrozen after cooking (`daily/food/portion-and-freeze-meals`).

## Failure modes & recovery

- **F1 Found meat that sat out on the counter for hours:** the asymmetric rule decides, and it decides discard. The freezer's money is cheaper than the week the alternative can cost.
- **F2 Bag leaked in the water bath:** rinse solid items and cook immediately; porous or ground items that took on water are compromised in quality but safe if cooked now.
- **F3 Microwave defrost cooked the edges gray:** normal at the margins; carve off if it offends and cook the rest promptly. Next time, lower power and more turning.
- **F4 Center still frozen at cooking time:** finish the thaw with the cold-water method for a few cycles, or switch the recipe to a from-frozen-friendly preparation (soups and stews forgive everything).

## Verification

The method matched the timeline, nothing proteinaceous ever sat at room temperature, water-bath and microwave thaws went straight into cooking, drips stayed on the catch plate, and the cooked result reached steaming-hot centers.

## Variations

- Vacuum-sealed portions (`daily/food/portion-and-freeze-meals` output) thaw dramatically faster in the water bath, which is the workflow's designed synergy.
- Planned households simply move tomorrow's dinner to the fridge each evening, converting this whole recipe into a ten-second habit.

## Safety & privacy

Medium risk entirely about the danger zone: the counter ban, the cook-immediately rules for the fast methods, and the drip-containment shelf discipline. The three methods exist so that impatience always has a safe option.
