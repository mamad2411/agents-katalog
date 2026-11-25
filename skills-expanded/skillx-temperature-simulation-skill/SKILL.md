---
name: skillx-temperature-simulation-skill
description: skillx family-level skill for SkillLearnBench task family temperature-simulation.
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
  family: temperature-simulation
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `temperature-simulation`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction, list the available files, and inspect the current namelist parameters and observation schema so you know the required outputs, allowed edits, and evaluation rules before changing anything.
# step 2: Record the baseline values of all constrained namelist fields, then limit any planned calibration to only the explicitly allowed parameters and their stated bounds so the final configuration remains valid and compliant.
# step 3: Run the lake model with the current or lightly edited namelist to produce the required NetCDF output, and use a file summary check to confirm the run succeeded and wrote the expected output file.
# step 4: Compute the public evaluation metrics from the model output and observations using the exact visible matching method and required metric subsets, because the final report must match the checker’s merge logic rather than an approximate custom calculation.
# step 5: If any metric misses its threshold, perform a bounded parameter sweep or a small sequence of targeted namelist edits over the allowed calibration fields, rerunning the model and recomputing metrics after each candidate to improve fit while preserving all unchanged settings.
# step 6: Leave the best compliant parameter set in the namelist, rerun once to confirm the final output file is produced, and verify that only allowed parameters differ from baseline and all final values remain within bounds.
# step 7: Write the final metrics JSON with exactly the requested keys and values from the exact public metric computation, then finalize only after both required output artifacts exist at the specified visible paths.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
