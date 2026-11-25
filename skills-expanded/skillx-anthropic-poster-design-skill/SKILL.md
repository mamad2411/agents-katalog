---
name: skillx-anthropic-poster-design-skill
description: skillx family-level skill for SkillLearnBench task family anthropic-poster-design.
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
  family: anthropic-poster-design
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `anthropic-poster-design`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and any visible task files to extract the required output paths, exact JSON schema, named text elements, composition type, and explicit visual constraints; this prevents guessing and keeps the deliverables aligned with the checker.
# step 2: Look up the needed brand tokens for the specified background, structural colors, accents, muted line color, and heading typography; record the applied HEX values and font name because they must be reused consistently in both the image and metadata file.
# step 3: Translate the brief into a simple deterministic layout recipe matched to the requested artifact type, such as a technical separated-module poster or a minimalist packaging/launch card; assign each required visual component to the mandated brand token so the composition is branded and auditable.
# step 4: Render the image with the family-specific drawing tool, using generous whitespace, clear hierarchy, restrained highlights, and simple geometric forms or modules; keep saturation low and avoid gradients, glow, neon, or other flashy effects because those are common failure modes.
# step 5: Write the companion JSON file using exactly the requested keys and only the applied values from the final design; include the heading font only when the schema asks for it.
# step 6: Inspect the rendered image metadata and visual summary to confirm the file exists at the required path, dimensions are valid, dominant colors match the intended palette, and any highlight-area or low-saturation constraints are still satisfied; repair the first concrete mismatch and recheck.
# step 7: Finalize only after both artifacts exist, the image content satisfies the visible brief, and the JSON shape exactly matches the specified schema; avoid using hidden local checks, prior answers, or solution files.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
