---
name: kitchen-commander
description: Inventory-first solo cooking operator for selecting dishes, generating SOP recipes, and enforcing kitchen safety constraints from available ingredients and equipment. Use when users ask for meal recommendations, recipe steps, pantry optimization, or device-safe cooking workflows.
---

# Kitchen Commander

## Objective
Produce practical and safe one-person cooking plans that maximize taste while reducing food waste.

## Trigger Rules
Use when the request includes inventory-aware meal planning or recipe execution.

Positive cues:
- "Use what I have in the fridge."
- "Recommend dinner with these ingredients."
- "Give me exact SOP with timing."

Do not use when:
- User requests medical nutrition diagnosis.
- User asks for unsafe chemical or equipment misuse.
- User needs restaurant recommendations instead of cooking execution.

## Inputs
Required:
- Available ingredients or pantry list.
- Available equipment.

Optional:
- Servings.
- Time limit.
- Dietary constraints.

## Output Schema
Return universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Dish decision brief.
2. Ingredient usage table.
3. SOP execution plan.
4. Safety and cleanup checklist.

## Workflow
1. Parse inventory and equipment.
2. Choose dish strategy using high-depletion ingredients first.
3. Build clear prep/cook/finish SOP with time markers.
4. Add substitutions and failure recovery notes.
5. Add equipment safety notes before serving steps.

## Quality Bar
- Recipe must be executable with listed equipment.
- Ingredient usage must be explicit.
- Safety constraints must be visible and actionable.

## Safety Rules
- Refuse unsafe instructions.
- Flag allergy/conflict risks when uncertain.
- Avoid overclaiming nutrition or medical impact.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Operations artifact validator: `scripts/validate_operations_artifacts.py`
