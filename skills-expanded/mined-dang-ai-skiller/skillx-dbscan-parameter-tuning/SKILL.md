---
name: skillx-dbscan-parameter-tuning-skill
description: skillx family-level skill for SkillLearnBench task family dbscan-parameter-tuning.
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
  family: dbscan-parameter-tuning
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `dbscan-parameter-tuning`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and file inventory to extract the input CSV locations, required output CSV path and columns, the hyperparameter grid, the image-key column, the instance-specific custom distance formula, and rounding/filtering rules; this prevents using hidden requirements or wrong metrics.
# step 2: Use the family-specific DBSCAN grid-search tool on the visible annotation and expert data, configuring it with the full stated parameter grid and the custom distance metric from the instruction; this efficiently evaluates all candidate settings in the allowed way.
# step 3: Ensure the evaluation follows the public scoring procedure over images keyed by the shared identifier: cluster citizen-science points per image, compute centroids, greedily match them to expert points with the stated distance cap using standard Euclidean distance, and compute per-image F1 and delta; this is the basis of the optimization target.
# step 4: Aggregate metrics exactly as instructed by iterating over all expert-image keys, counting missing or unmatched cases as zero F1 with undefined delta, including zero-F1 cases in the F1 mean, and excluding undefined deltas from the delta mean; this avoids biased averages.
# step 5: Filter candidate settings to those above the required F1 threshold, then compute the Pareto frontier by keeping only settings not dominated by another setting with higher-or-equal F1 and lower-or-equal delta; this produces the requested tradeoff set.
# step 6: Write the frontier rows to the required CSV with the exact header, field order, and rounding conventions, preserving integer fields as integers; this matches the expected artifact format.
# step 7: Perform a lightweight sanity check that the output file exists, has the required schema, and only contains filtered Pareto-optimal rows; fix the first concrete mismatch before finalizing.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
