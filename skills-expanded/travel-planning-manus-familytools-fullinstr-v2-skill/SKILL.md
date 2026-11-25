---
name: travel-planning-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for travel-planning using latest full-instruction v2 family injection.
allowed-tools:
  - budget_calculator
  - data_catalog
  - distance_matrix_lookup
  - list_dir
  - make_dir
  - read_file
  - read_table
  - run_python
  - run_shell
  - search_text
  - travel_db_query
  - write_file
  - write_json
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Travel Planning

## When to use this skill
Use this skill for the `travel-planning` family of tasks in SkillLearnBench. It is required when building a multi-day travel itinerary that must satisfy specific constraints (budget, transportation, dietary, accommodation) using real-world data from provided datasets.

## Visible input and artifact inventory
The environment provides datasets in directories like `background/`, `accommodations/`, `restaurants/`, `attractions/`, and `googleDistanceMatrix/`. The primary input is `instruction.md`, detailing the itinerary requirements. The expected output is a single JSON file, typically at `/app/output/itinerary.json`.

## Execution procedure for the current task
1. **Information Extraction**: Read `instruction.md` to extract constraints: days, cities, dates, budget, dietary, accommodation, and transportation rules.
2. **Data Discovery**: Use `data_catalog` and `list_dir` to explore available datasets.
3. **Itinerary Construction**: Build the itinerary day by day. Select transportation, meals, attractions, and lodging that align with constraints.
4. **Constraint Verification**: Check costs against the budget using `budget_calculator`. Verify distances using `distance_matrix_lookup`.
5. **Artifact Generation**: Format the data into the required JSON structure, including a `plan` array and a `data_sources` array.
6. **Final Output**: Write the JSON to the output path using `write_json`.

## Family tool routing and useful placeholder snippets
- **Data Exploration**: Use `data_catalog` to understand CSV schemas. Use `read_table` to extract specific rows.
- **Querying**: Use `travel_db_query` for complex searches across tables.
- **Calculations**: Use `distance_matrix_lookup` for driving distances. Use `budget_calculator` for expenses.
- **File Operations**: Use `write_json` to serialize the final itinerary.

## Validation checks before final submission
- **Schema Compliance**: Ensure the output JSON matches the required structure exactly.
- **Constraint Adherence**: Verify budget, cuisines, accommodation needs, and transportation rules.
- **Data Authenticity**: Confirm all selected entities exist in the provided datasets.

## Common failure modes and repair actions
- **Budget Exceeded**: Replace high-cost items with affordable alternatives from the datasets.
- **Missing Cuisines**: Use `travel_db_query` to search the restaurant dataset for required cuisines.
- **Invalid JSON Format**: Ensure strings are properly escaped and the structure matches the example.

## Finalizer capsule
If nearing the maximum step limit, prioritize generating a structurally valid JSON file with whatever partial plan exists. Ensure the `plan` array has the correct number of days, using placeholders or `"-"` for missing fields. The goal is a valid artifact adhering to the schema.
