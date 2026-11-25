---
name: skillx-travel-planning-skill
description: skillx family-level skill for SkillLearnBench task family travel-planning.
allowed-tools:
- list_dir
- read_file
- write_file
- python
- shell
metadata:
  benchmark: skilllearnbench
  source_method: skillx
  source_dir: <SOURCE_DIR>
  family: travel-planning
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `travel-planning`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inspect the available data files to extract the required output path, JSON schema, trip constraints, and allowed data sources. This prevents schema or rule violations.
# step 2: Query the travel tables for candidate cities, attractions, restaurants, accommodations, and ground-travel distances that satisfy the prompt constraints such as destination region, no flights, cuisine preferences, and any accommodation requirements. Use only provided database data.
# step 3: Build a day-by-day itinerary covering the required number of days and cities, placing driving legs between cities, selecting meals and attractions per day, and using `"-"` for any intentionally skipped field required by the instruction. This ensures every day object is complete and constraint-aware.
# step 4: Estimate total trip cost with the provided budget tools, including lodging, meals, and ground transportation assumptions, and adjust choices if the plan exceeds the budget. This keeps the itinerary feasible.
# step 5: Write the final JSON artifact to the requested path with exactly the required top-level keys, a correctly sized `plan` array, and a `data_sources` list naming the datasets actually used. This satisfies the output contract.
# step 6: Run a lightweight validation on the written file for JSON validity, field presence, formatting conventions, prohibited transport modes, and any special per-day constraints, then fix the first concrete mismatch before finalizing. This catches common public-check failures.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
