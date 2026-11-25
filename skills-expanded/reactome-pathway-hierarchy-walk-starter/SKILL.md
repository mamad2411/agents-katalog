# Reactome Pathway Hierarchy Walk Starter

Use this skill to traverse the official Reactome pathway hierarchy and summarize the ancestor chain, direct children, and descendant count for a target stable ID.

## What it does

- Fetches the official Reactome `eventsHierarchy` tree for a species.
- Locates a target pathway or reaction stable ID inside the nested hierarchy.
- Exports a compact JSON summary with the ancestor path and subtree shape.

## When to use it

- You need a verified starter for `pathway traversal and hierarchy walks`.
- You want a lightweight way to place a Reactome stable ID inside its broader biological context.
- You need deterministic JSON for tests, demos, or downstream routing logic.

## Example

```bash
python3 skills/systems-biology/reactome-pathway-hierarchy-walk-starter/scripts/run_reactome_hierarchy_walk.py \
  --species 9606 \
  --stable-id R-HSA-141409 \
  --out scratch/reactome-hierarchy/r_hsa_141409_hierarchy.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/systems-biology/reactome-pathway-hierarchy-walk-starter/tests -p 'test_*.py'`
- Expected summary: `top_level_pathway == "Cell Cycle"` and `ancestor_count == 5` for `R-HSA-141409`
