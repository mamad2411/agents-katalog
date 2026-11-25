---
name: combine-skills
description: Merge several related skills into one skill with shared rules and a routing table, then check the merged skill against the originals. Use when the user asks to combine, merge, consolidate, or unify multiple skills.
disable-model-invocation: true
---

# Combine Skills (Advanced)

Merge related skills into one package **only if it scores better**. Output: a merged skill folder, a merge report, and a benchmark plan.

## Phase 1: Inventory
1. Get every source skill: pasted text, folders, or account skills (read their SKILL.md and all referenced files).
2. Run the inventory script on the folders:
   ```bash
   python scripts/inventory_skills.py <skill-dir-1> <skill-dir-2> [...]
   ```
   It reports each skill's triggers, sections, size, and **rule overlap** between skills.
3. Fill `templates/inventory-template.md`: triggers, inputs, steps, format, rules, scripts per skill.

## Phase 2: Decide (merge or not)
Score the set with `references/merge-decision.md` (6 criteria, 0–2 each).
- **≥ 8/12:** merge.
- **5–7:** merge only the closest subset, or merge shared rules into a small "house rules" skill instead.
- **≤ 4:** don't merge. Tell the user why, and suggest improving descriptions to stop overlap.

Show the score to the user before building.

## Phase 3: Resolve conflicts
Use `references/conflict-resolution.md`. For every conflict (severity scales, formats, tone, length, naming):
- Pick one winner using the priority order, **or**
- Keep it as a per-part override if both are truly needed.
- Record each decision in the merge report. Ask the user only about conflicts that change output meaningfully.

## Phase 4: Build
1. Structure (see `references/routing-patterns.md` to pick a routing pattern):
   ```
   merged-skill/
   ├── SKILL.md          triggers + routing + shared rules + multi-task order
   ├── references/<part>.md   one per original skill (task-specific only)
   ├── scripts/          merged, de-duplicated scripts
   └── evals/test-cases.md
   ```
2. Write the combined **description** covering every task's trigger phrases (≤ 1024 chars, aim ≤ 300).
3. Write the **routing table** mapping request type to reference file.
4. Define the **multi-task order** (which part runs first when several apply) and a **combined output** format.
5. Move duplicated rules into **Shared rules**; leave only task-specific rules in each reference.
6. Start from `templates/merged-SKILL-template.md`.
7. Validate: `python scripts/validate_skill.py <merged-skill-dir>`.

## Phase 5: Prove it
1. Build `evals/test-cases.md`: union of the originals' test cases + multi-task cases + cross-routing near-misses (request for part A must not load part B).
2. Benchmark **A = original separate skills** vs **B = merged** with the `benchmark-skill` workflow.
3. Switch only if B ≥ A on trigger accuracy **and** quality, with no regression on any single task.

## Phase 6: Migrate
- Save the merged skill; **disable the originals** so they don't compete.
- Built-in or plugin skills can't be edited; copy their content into the merged skill under a new name.
- Deliver the merge report (`templates/merge-report-template.md`).

## Rules
- Never merge without showing the decision score first.
- Never lose a trigger: every original trigger phrase must be in the merged description or covered by a broader phrase that the tests prove.
- Never lose a rule silently: each original rule is kept, merged into Shared rules, or listed as "dropped + reason".
- Shared rules win over part rules unless a part explicitly overrides them.
- SKILL.md stays short (≤ 200 lines ideal); task detail lives in `references/`.
- One routing entry per request type; no ambiguous rows.

## Self-check
- [ ] Merge score shown and ≥ 8 (or user approved a lower score)
- [ ] Every original trigger covered
- [ ] Every original rule accounted for in the merge report
- [ ] Validator passes
- [ ] Benchmark plan (or results) included
- [ ] Originals flagged for disabling
