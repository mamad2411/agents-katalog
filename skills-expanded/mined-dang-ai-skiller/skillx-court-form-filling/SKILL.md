---
name: skillx-court-form-filling-skill
description: skillx family-level skill for SkillLearnBench task family court-form-filling.
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
  family: court-form-filling
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `court-form-filling`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inspect the workspace to identify the blank PDF, required output path, date-format rule, and any limits on which fields may be filled; this anchors the task to prompt-visible evidence only.
# step 2: Inspect the PDF structure with form-field listing and, if needed, extracted text or rendered pages; this reveals the field names, checkbox options, and layout needed for accurate mapping.
# step 3: Extract the case facts from the prompt into a structured mapping for parties, contact details, addresses, filing-history status, claim amount, claim narrative, venue basis, and signing/filing dates; normalize all provided dates to the required format before filling.
# step 4: Map only explicitly stated facts into the corresponding PDF fields, including alternate plaintiff fields or filing-history checkboxes when the prompt supports them; leave court-completed, optional, and unspecified fields blank to avoid overfilling.
# step 5: Fill the form with the prepared field-value mapping and save it to the requested output path; use the dedicated PDF form-filling tool so the result preserves the original document structure.
# step 6: Dump the filled field values and compare them against the extracted facts and blank-field rule; fix the first concrete mismatch such as a wrong checkbox, misplaced party data, unnormalized date, or accidentally populated extra field.
# step 7: Finalize only after the filled PDF exists at the required path and the sanity check shows the output matches the visible instructions.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
