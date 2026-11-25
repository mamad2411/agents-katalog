---
name: skillx-chinese-poem-generator-skill
description: skillx family-level skill for SkillLearnBench task family chinese-poem-generator.
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
  family: chinese-poem-generator
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `chinese-poem-generator`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and any prompt-listed files to identify the required output file, poem form, line count, perspective, theme, and rhyme requirement; this prevents inventing hidden constraints.
# step 2: Draft a concise title and eight poem lines that match the requested regulated-verse form and the stated viewpoint/theme; keep the content stylistically consistent and focused on the prompt.
# step 3: Check that each poem line has the required number of Chinese characters and that no lines are accidentally duplicated; fix these first because format errors are easy to verify and commonly fatal.
# step 4: Run the regulated-verse and modern-Mandarin rhyme checks with the provided poem tools; use the results to revise line endings or structure until the poem roughly satisfies the formal constraints.
# step 5: Write only the final text artifact in the required layout: title on the first line, then the poem lines in order; avoid adding commentary or extra files because the task expects a strict text output.
# step 6: Re-read the saved artifact and confirm the file exists at the requested path and matches the required shape exactly; finalize only after the visible checks pass and no prompt-visible constraint is unmet.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
