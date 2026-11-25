---
name: skillx-video-object-counting-skill
description: skillx family-level skill for SkillLearnBench task family video-object-counting.
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
  family: video-object-counting
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `video-object-counting`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and list available files to determine the input video, required output table, requested object classes, and which template images exist for each class.
# step 2: Extract key frames from the input video into the required location and sort them in timeline order, because the output must report one row per extracted frame with the expected frame identifier pattern.
# step 3: Convert every extracted key frame to grayscale in place, because the counting method is expected to operate on normalized frame images.
# step 4: Group all provided template images by object class and, for any requested class with no template, set that class count to zero for every frame, because missing templates must not trigger ad hoc detection.
# step 5: For each frame and each class with templates, run template matching with every template for that class and combine the detections with box deduplication, because multiple templates may cover the same class and overlapping matches should not be double-counted.
# step 6: Build the result table with the instructed columns in the instructed order, using the normalized frame identifiers and one count per requested class for each frame.
# step 7: Write the CSV to the required path and sanity-check that the file exists, the row count matches the number of extracted frames, and the header/schema matches the instruction.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
