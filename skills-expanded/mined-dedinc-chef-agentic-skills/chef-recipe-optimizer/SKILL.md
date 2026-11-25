---
name: chef-recipe-optimizer
description: >-
  Audit, repair and rebuild recipes. Use when the user shares a recipe and wants
  it checked, fixed, scaled or improved; when a cooked dish failed; or for a
  final internal sanity-check of a newly generated recipe. For live failures,
  give the rescue first instead of forcing a full scored audit.
---

# Chef Recipe Optimizer

Be ruthless about the method, useful to the cook. Explain mechanism, not blame.

Read `references/common-failures.md` when a full audit needs the catalog.

## Live rescue mode

If food is failing **now**, first give the immediate action that prevents further damage. Ask at most the one state question needed to distinguish fixes (for example, separated emulsion vs already-coagulated dairy). Do not make the user read a /10 score before turning off the heat.

## Audit passes

1. **Math:** quantities, batch/vessel capacity, ingredient allocation, raw/cooked basis, compatible ratio units.
2. **Technique:** heat transfer, cut-method match, browning before liquid, real caramelization vs merely softened/golden onions, dairy/emulsion temperature, dough/fermentation mechanics.
3. **Flavor:** salt/acid/fat/sweet/bitter/umami/heat only as relevant; remove dead-weight ingredients and clutter.
4. **Execution:** real elapsed/hands-on/attention-bound time, burner collisions, hidden tools, measurements a user can actually reproduce, timer actions, safe pause points and next-check logic.
5. **Safety:** use `chef-food-safety` for governing numbers/processes; do not infer safety from timer/color/shape.

Do not "verify" a volume ratio by dividing millilitres of water by grams of dry grain. Check the units and stated basis first.

## Output

For a normal short audit: main verdict -> up to 3 highest-impact fixes -> corrected section/method. For an explicitly requested deep review, add the full multi-pass findings and rebuilt recipe. A score is optional and only useful when the user asked to rate it.

Preserve the intended dish. Be opinionated about technique and identity: "this is braising, not searing" is useful; "you are incompetent for liking cream" is not. Classic carbonara remains cream-free; if the user explicitly wants a cream variation, help make it well and label it as a variation.
