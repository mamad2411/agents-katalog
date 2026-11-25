---
name: skillx-organize-messy-files-skill
description: skillx family-level skill for SkillLearnBench task family organize-messy-files.
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
  family: organize-messy-files
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `organize-messy-files`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inventory the working directory to identify the source documents, the required destination folders, and any explicit constraints; this prevents acting on hidden artifacts or missing edge-case files.
# step 2: Inspect document contents in bulk with the available document-summary or text-extraction tools, and use keyword scoring if helpful, to infer each file’s subject from content rather than filename or extension alone.
# step 3: Build a deterministic one-file-to-one-folder classification for all documents across the requested subject taxonomy, applying the instruction’s fallback category for anything ambiguous so nothing remains unassigned.
# step 4: Create the required subject folders exactly as named in the instruction; this establishes the output structure without altering filenames or file contents.
# step 5: Move each source document into its assigned folder using the provided file-operation tools, preserving original files intact and ensuring every document is placed in exactly one destination.
# step 6: Sanity-check the result by listing the folders and comparing counts against the original inventory to confirm all documents were moved, no extra source documents were left behind, and the final directory shape matches the instruction.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
