---
name: skillx-nlp-paper-reproduction-skill
description: skillx family-level skill for SkillLearnBench task family nlp-paper-reproduction.
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
  family: nlp-paper-reproduction
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `nlp-paper-reproduction`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Inspect the visible repository files and instructions to identify the target loss function, the required output artifacts, and any constraints such as forbidden file edits; do this first so you only use prompt-visible evidence.
# step 2: Read the project environment specification and the trainer-related source files to infer the expected dependencies, surrounding API, tensor shapes, and calling conventions; this lets you patch only the minimal loss path instead of changing unrelated code.
# step 3: Derive the SimPO objective from the paper and map it onto the existing trainer code, using the average sequence log-probability reward and the repo’s chosen-vs-rejected comparison structure; do this to implement the correct formula in the project’s style.
# step 4: Use the family-specific preparation tool to apply the minimal deterministic loss implementation and to generate the requested reproducibility artifacts, rather than attempting heavy training or broad refactors.
# step 5: Produce the evaluation output exactly at the required location and schema, ensuring the saved array key and output shape match the visible test expectations; also record interpreter and package metadata in the requested log file for reproducibility.
# step 6: Run lightweight sanity checks from visible files or tool summaries, fix the first concrete mismatch in loss computation or artifact format, and finalize only when all requested files exist and conform to the stated constraints.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
