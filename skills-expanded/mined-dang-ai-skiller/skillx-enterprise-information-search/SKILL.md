---
name: skillx-enterprise-information-search-skill
description: skillx family-level skill for SkillLearnBench task family enterprise-information-search.
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
  family: enterprise-information-search
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `enterprise-information-search`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the question file and inventory the available data directories and files so you know the answer schema, the question keys, and which enterprise datasets can support each lookup.
# step 2: Inspect the catalog or sample records from metadata and product files to map the main entities, fields, and relationships so you can route each question to the right source records.
# step 3: For each question, identify the target entity, filters, and requested output type, then use the structured data tools first to search, query, fuzzy-match, and aggregate the relevant records with minimal ad hoc code.
# step 4: Join information across files when needed, such as linking organization, employee, team, customer, product, or period fields, so each answer is grounded in the visible enterprise data rather than a single incomplete source.
# step 5: Build the result object in the required JSON shape, ensuring every question key maps to an object with `answer` as a list and `tokens` as a positive numeric value.
# step 6: Run a lightweight validation pass on completeness and format, confirm the output file exists at the requested path, and repair any first concrete mismatch before finalizing.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
