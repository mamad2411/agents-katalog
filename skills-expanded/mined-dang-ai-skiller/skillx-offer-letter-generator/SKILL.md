---
name: skillx-offer-letter-generator-skill
description: skillx family-level skill for SkillLearnBench task family offer-letter-generator.
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
  family: offer-letter-generator
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `offer-letter-generator`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and list the working files so you know the template location, data source, required output path, and any conditional rules before editing anything.
# step 2: Inspect the structured input data and extract the template placeholders so you can build an exact mapping from visible fields to template variables without inventing values.
# step 3: Handle any conditional block markers explicitly before or during filling: keep the enclosed content only when the controlling field says to include it, and always remove the marker tags from the final document.
# step 4: Fill the DOCX template with the mapped values using the document-specific tooling so the original formatting and structure are preserved.
# step 5: Save the completed document to the requested output path and preview its text or metadata to confirm the file was created successfully.
# step 6: Sanity-check the result for unresolved placeholders, leftover conditional markers, and mismatches with the visible data; repair the first concrete issue and re-preview if needed.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
