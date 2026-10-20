---
name: buy-groceries
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: basic
est_time: 1h
risk: low
prerequisites: [have-payment-method]
status: draft
last_verified: 2026-07-20
---

## Goal

A grocery run that returns home with what the week actually needs — within budget, cold chain respected, nothing crushed, nothing forgotten.

## Preconditions

- A list, built from planned meals plus staples running low (the list is the difference between this recipe and an expensive wander).
- Payment method, reusable bags where customary/required.
- A rough budget and knowledge of what's already in the fridge/pantry (30 seconds of checking prevents the third jar of the same sauce).

## Steps

1. **Build the list by category, and eat something first.** Group list items the way stores are laid out: produce / meat-dairy / pantry / frozen / household. Shopping hungry measurably worsens every decision ahead. → *Expect:* a categorized list; you, not starving.
2. **Route the store perimeter-first, frozen-last.** Classic layout: produce → bakery → meat/dairy along the walls, pantry aisles as needed, frozen at the very end so it travels warm-side the least. → *Expect:* cart filling in list order; frozen still in the store's freezer, not your cart, until the end.
3. **Pick produce and dates deliberately.** Produce: firmness/smell over cosmetic perfection; ripeness matched to *when you'll eat it* (bananas for Friday can be green today). Dated goods: reach for dates that outlive your meal plan — and know "best before" is quality, "use by" is safety. → *Expect:* items that survive until their planned meal.
4. **Compare by unit price, not sticker price.** The shelf tag's per-kg/per-100g figure is the honest number; bigger packs win only if you'll finish them. → *Expect:* choices justified by unit price or genuine need, not package theater.
5. **Load the cart with physics in mind.** Heavy/rigid below (cans, bottles), crushables on top (bread, eggs, chips, berries). Same rule again at bagging. → *Expect:* nothing fragile under anything heavy at any stage.
6. **Sweep the list before the checkout line.** One scan of unchecked items — the missing ingredient discovered *now* costs one aisle walk; at home it costs the meal. → *Expect:* every list line checked or consciously dropped.
7. **Check out and bag by destination.** (`daily/pay-at-a-cashier` or `daily/use-a-self-checkout`.) Bag cold-with-cold (they insulate each other), heavy-below again, and chemicals/soaps away from food. → *Expect:* paid, bagged in a scheme that unpacks logically.
8. **Go home reasonably directly and put cold things away first.** Perishables have been out of refrigeration since step 7; frozen and chilled unpack before anything else. → *Expect:* fridge/freezer loaded within the safe window; pantry at leisure; bags stored for next time.

## Decision points

- Deal on something not on the list → the test is "would this have made the list if I'd known?" — stock-up on used-weekly staples: yes; novelty at 20% off: it's still spending, not saving.
- Substitution needed (item out of stock) → substitute within the *meal's role* (any firm white fish for the recipe's cod), not by shelf adjacency.
- Long checkout lines everywhere → the produce-and-dairy in your cart doesn't mind 10 minutes; it minds the hot car later — a line is not a reason to skip step 8's directness.

## Failure modes & recovery

- **F1 Forgot a key ingredient anyway:** check the corner shop before re-driving to the supermarket; adapt the meal before either.
- **F2 Eggs/bread crushed:** the physics rule (5/7) lapsed — this trip, salvage (french toast forgives); next trip, the rule.
- **F3 Fridge item left on the counter for hours (discovered later):** apply `daily/store-leftovers`'s asymmetric rule — meat/dairy/seafood past ~2 h warm: discard; unopened shelf-stable-ish items (hard cheese, many condiments): judgment.
- **F4 Budget blown at the register:** ask to remove items — normal and unembarrassing ("actually, take the X off, please"); the alternative of paying-and-regretting teaches nothing.

## Verification

Home with every list item or a conscious substitute, cold chain unbroken (cold items in the fridge/freezer promptly), nothing crushed, spend within budget, and the next trip's list already collecting what ran out.

## Variations

- Market/multi-shop cultures (`eu`, `jp` daily-shopping patterns): smaller more frequent trips — the list shrinks, the freshness step dominates, the cold-chain window matters less.
- Online grocery + pickup/delivery: steps 2–5 become substitution-preference settings; verification shifts to checking the delivered order against the receipt at the door.

## Safety & privacy

Low risk. The cold chain (frozen-last, home-directly, cold-away-first) is the one food-safety thread; lifting and cart physics protect only your eggs and your lower back.
