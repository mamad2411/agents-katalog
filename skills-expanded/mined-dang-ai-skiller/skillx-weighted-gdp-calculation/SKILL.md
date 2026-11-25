---
name: skillx-weighted-gdp-calculation-skill
description: skillx family-level skill for SkillLearnBench task family weighted-gdp-calculation.
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
  family: weighted-gdp-calculation
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `weighted-gdp-calculation`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inspect the workbook structure to identify the task sheet, source sheet, yellow input/output ranges, blue lookup keys, and any target summary cells; this establishes the exact cells to fill without changing sheet layout.
# step 2: Read the relevant source-data block from the data sheet and map how series codes and years are arranged; this lets you build two-condition retrieval formulas that match the workbook’s row and column labels.
# step 3: Write lookup formulas into each yellow data-population range using an allowed two-key pattern such as INDEX/MATCH or XLOOKUP with MATCH; this pulls the required source values into the task sheet while preserving formulas and styles.
# step 4: Write formulas for the requested country-level metric in the designated result range, using the task-specific numerator, denominator, and any required scaling by 100 so displayed percentages are in the expected form.
# step 5: Fill the summary statistic cells with spreadsheet formulas for minimum, maximum, median, mean, and quartiles over the computed metric range, and write the weighted-mean cell with a SUMPRODUCT-based formula using the appropriate weight range from the populated data.
# step 6: Recalculate the workbook and dump formulas or read back key ranges to confirm that lookup cells, metric cells, and weighted-mean cells contain formulas in the expected locations and that percentage scaling/rounding requirements are reflected.
# step 7: Run a style check on the modified workbook and finalize only if formatting is unchanged and the workbook contains the requested formulas within the existing sheets only.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
