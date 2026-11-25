---
name: skillx-financial-analysis-skill
description: skillx family-level skill for SkillLearnBench task family financial-analysis.
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
  family: financial-analysis
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `financial-analysis`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inspect the available quarter datasets and output schema so you know which funds, securities, periods, rankings, and JSON keys are required.
# step 2: For each question about a fund in a given quarter, fuzzy-search the filing index for the manager name, pick the best matching filing for the target quarter, and record its accession identifier so later queries hit the correct fund.
# step 3: Use the fund-details tool on that accession to extract summary fields such as AUM and holdings count, because these values are already reported at the filing level.
# step 4: For each quarter-over-quarter increase question, resolve the same manager separately in both quarters, compare the two holdings sets with the holdings-comparison tool, sort by positive dollar-value change, and keep the requested number of security identifiers.
# step 5: For each top-holders-by-security question, first resolve the target security identifier from the quarter data, then query the top holders for that identifier in the target quarter and return the requested number of manager names ranked by share value.
# step 6: Assemble only the requested answers into the exact JSON schema and write it to the specified path, preserving numeric fields as numbers and identifier/name lists in the requested order.
# step 7: Sanity-check that the file exists, the JSON keys and list lengths match the instruction, and every value came from visible filings or SEC-tool outputs rather than hidden artifacts.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
