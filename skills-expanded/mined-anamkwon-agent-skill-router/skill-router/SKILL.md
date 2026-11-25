---
name: skill-router
description: "Use to organize a large skill library into category routers, route new skills, and propose new categories when existing routers are insufficient."
---

# Skill Router

Use this router when organizing, reclassifying, or validating a growing skill library.
It keeps first-pass discovery small by routing from exposed category skills to hidden leaf skills.
For third-party installs, configure the target roots explicitly instead of assuming
the plugin is installed inside the same repository as the skills.

## Token Budget Rule

Do not read every leaf `SKILL.md` by default. Start from `routing/skill-inventory.json`,
`routing/routing-review.md`, `routing/routing-index.json`, and the exposed category router
SKILL files. Read a leaf body only when the inventory summary is ambiguous or when moving it
would change a category boundary.

The target skill roots come from `skill-router.config.json` or environment
variables. For user-global skills, use hidden leaf roots such as
`~/.claude/skill-leaves` and expose category routers in `~/.claude/skills`.
For project skills, use `.claude/skill-leaves` and `.claude/skills`.

## Workflow

1. Run `node plugins/skill-router/scripts/skill-router.mjs scan` to refresh compact metadata.
2. Read `plugins/skill-router/routing/routing-review.md` and existing category routers under `plugins/skill-router/skills/`.
3. Classify by workflow force and stop conditions, not by keyword alone.
4. Keep a skill in an existing category only when that category's `Use When` and `Avoid` rules stay clear.
5. If no existing category fits without vague wording, propose a new category in `plugins/skill-router/routing/routing-plan.json`.
6. Run `node plugins/skill-router/scripts/skill-router.mjs apply` only after the plan is coherent.
7. Run `node plugins/skill-router/scripts/skill-router.mjs scan` and `node plugins/skill-router/scripts/skill-router.mjs validate`.

## New Category Test

Create a new category only when at least one of these is true:

- A skill would need mismatched special cases in every existing category.
- Three or more unclassified or awkwardly classified skills share the same distinct workflow force.
- Expanding an existing category would make its `Avoid` rules vague.
- The new category can name clear `use_when`, `avoid_when`, and leaf routes.

## Routing Plan Shape

Write plans as JSON with `categories` and `routes`. `skill-router.mjs apply` is deterministic;
the agent owns judgment, and the script only applies the approved plan.

```json
{
  "categories": [
    {"id": "category-id", "display": "Category Name", "short": "Short focus", "description": "When to use first", "routing_prompt": "How to choose a leaf", "avoid": ["When not to use it"]}
  ],
  "routes": [
    {"category": "category-id", "skill": "leaf-skill", "reason": "Why this leaf belongs here"}
  ]
}
```

## Stop

- The skill description is too generic to classify from inventory metadata.
- Existing categories fit for unrelated reasons and no dominant force is clear.
- The plan creates a catch-all category such as misc, general, or other.
- Applying the plan would hide a useful distinction that the user needs for routing.
