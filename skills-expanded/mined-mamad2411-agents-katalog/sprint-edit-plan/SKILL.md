---
name: sprint-edit-plan
description: Reviews an imported plan and proposes patches to make it ai-scrum-ready. Detects vague AC, oversized tasks, missing test approach, weak DoR fields, missing PRD/design refs. Used by /sprint:edit-plan.
---

# sprint-edit-plan

## Validation checks

For each task in plan.tasks:

1. **AC quality** (use `ai-scrum:ac-validator` skill)
   - Must have at least one AC.
   - Each AC must have non-empty `given`, `when`, `then`.
   - `then` should describe an observable outcome (not "system works correctly").

2. **Test approach**
   - `test_approach.unit` non-empty for tasks with logic.
   - `test_approach.integration` non-empty for tasks crossing module boundary.

3. **Sizing**
   - If `size` ∈ {L, XL} → suggest split.
   - If size missing — infer from AC count + dependencies.

4. **DoR** (use `ai-scrum:dor-validator` skill)
   - `title_clear`, `ac_verifiable`, `test_approach_known`, `dependencies_listed` все true.

5. **Cross-references**
   - `source.kind == "prd"` → `source.ref` resolvable.
   - `dependencies` точки на ID существующих в плане.

## Patch operations

| Op | When | What |
|----|------|------|
| `tighten_ac` | AC vague | Re-write Then to be measurable |
| `split_task` | size L/XL with ≥3 AC | Create N sub-tasks по AC clusters |
| `add_test_approach` | empty test_approach | Suggest based on file types in `expected_artifacts` |
| `add_dor_field` | missing field | Set boolean + rationale comment |
| `link_prd` | source.kind=prd, ref empty | Search `docs/specs/` for matching feature slug |

## Output

JSON list of patch operations + human-readable summary. User approves all/some/none. Approved patches applied via skill output to plan file.

Schema: see `schemas/plan.schema.json` and `schemas/sprint-task.schema.json`.
