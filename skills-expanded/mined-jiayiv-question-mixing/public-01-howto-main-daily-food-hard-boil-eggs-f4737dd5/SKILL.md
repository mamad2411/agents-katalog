---
name: hard-boil-eggs
domain: daily
subdomain: food
locale: [generic]
interface: physical
difficulty: basic
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Cook eggs in the shell until the whites are fully set and the yolks reach the texture you want, then cool them so they peel cleanly.

## Preconditions

- Eggs, a saucepan, water, a timer, a bowl, and ice or very cold water.
- A stove or other heat source that can bring water to a boil.
- Tongs, a slotted spoon, or another safe way to move hot eggs.

## Steps

1. **Choose the start method.** [BRANCH: cold start | boiling-water drop] Use cold start for fewer cracked shells and boiling-water drop for slightly easier peeling. → *Expect:* one method chosen before heat is turned on.
2. **Load the eggs in one layer.** Put eggs in a saucepan without stacking them. → *Expect:* each egg touches the pan bottom or sits in a single layer.
3. **Add or heat the water.** Cold start: cover eggs with 2 to 3 cm of cold water. Boiling-water drop: bring enough water to a gentle boil first. → *Expect:* water depth can cover the eggs fully.
4. **Start the timer at the right moment.** Cold start: when water reaches a full boil, turn off heat, cover, and time covered rest. Boiling-water drop: lower eggs into boiling water, reduce to a steady simmer, and time immediately. → *Expect:* timer is running only after the chosen trigger.
5. **Use the texture chart.** Time 6 min for jammy yolks, 8 min for mostly set, 10 min for firm yellow yolks, or 12 min for extra firm yolks. → *Expect:* timer length matches the yolk texture you want.
6. **Prepare an ice bath while eggs cook.** Fill a bowl with ice water deep enough to cover the eggs. → *Expect:* the cooling bowl is ready before the timer ends.
7. **Chill the eggs immediately.** Move eggs into the ice bath for at least 5 min, or 10 min for easy handling. → *Expect:* shells feel cool enough to hold.
8. **Peel under water if serving now.** Crack the wide end first, roll gently, then peel under running water or in the bowl. → *Expect:* the membrane loosens and the shell lifts off in larger pieces.
9. **Store unpeeled eggs if saving.** Dry the shells and refrigerate in a covered container. → *Expect:* eggs are cold, labeled if needed, and not left at room temperature.

## Decision points

- Very fresh eggs → prefer boiling-water drop or steam, because older eggs usually peel more cleanly.
- Eggs keep cracking → use cold start, lower the heat to a simmer, and avoid crowding.
- Cooking many eggs → use a wider pot so eggs stay in one layer and water returns to temperature quickly.
- Serving sliced eggs → chill longer before cutting so yolks stay clean and whites do not tear.

## Failure modes & recovery

- **F1 Green ring around yolk:** detect gray-green color and sulfur smell, recover by using shorter timing and immediate ice bath next time.
- **F2 Runny center:** detect yolk too loose after cutting, recover by simmering peeled halves briefly only if texture matters, otherwise use as soft-boiled.
- **F3 Rubber whites:** detect bouncy whites, recover by reducing cook time and avoiding a hard boil after eggs are in the pan.
- **F4 Shell sticks badly:** detect tiny shell flakes and torn white, recover by peeling under water from the wide end and using older eggs next time.

## Verification

One cooled test egg peels without large white tears, and when cut open the white is fully opaque and the yolk matches the selected timing.

## Variations

- Steaming: steam eggs over boiling water for 10 to 12 min, then ice bath; this often peels well.
- No ice: use the coldest tap water and refresh it until the bowl stays cold.
- High altitude: add 1 to 2 min if eggs are consistently underdone.

## Safety & privacy

Low risk from hot water and steam. Keep pot handles turned inward, move eggs with a spoon or tongs, and refrigerate cooked eggs promptly.
