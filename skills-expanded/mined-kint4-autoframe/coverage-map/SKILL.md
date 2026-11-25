---
name: coverage-map
description: Map spec files against requirements or features to show what is covered, missing, and redundant. Use when the user runs /coverage-map or asks what is tested.
---

# /coverage-map — Map Test Coverage

**Type:** Functional
**Description:** Reads all spec files and maps them against requirements or features, showing what is covered, what is missing, and what is redundant.

---

## Input Format

Optional:
- A list of requirements / features (pasted or via connector)
- A feature name to scope the report

With no input, map all existing E2E specs by feature folder.

## Output Format

A coverage table grouped by feature:

| Feature | Covered | Missing | Redundant |
|---|---|---|---|

Plus a short prose summary and a prioritized list of gaps to close (with the suggested skill for each).

## Step-by-Step Instructions

1. Enumerate every spec under `tests/e2e/` (and the feature folders).
2. Parse each spec's `test.describe` and `test` names to build the list of covered behaviors.
3. If requirements were provided, align covered behaviors to each requirement; otherwise infer expected coverage from the feature and existing Page Objects.
4. Identify:
   - **Covered** — requirement has at least one passing-shaped test.
   - **Missing** — requirement with no matching test.
   - **Redundant** — multiple tests asserting the same behavior with no added value.
5. Render the coverage table grouped by feature.
6. Give a prioritized gap list, recommending `/tc-to-spec` or `/new-spec` to close each gap.
7. For stakeholder-facing summaries, point to `/report`.

## Rules

- Read specs, never execute them, to build the map.
- Be explicit about assumptions when requirements are not provided.
- Group everything by feature to match the folder structure.
