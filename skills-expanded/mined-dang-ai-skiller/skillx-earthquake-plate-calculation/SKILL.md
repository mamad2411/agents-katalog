---
name: skillx-earthquake-plate-calculation-skill
description: skillx family-level skill for SkillLearnBench task family earthquake-plate-calculation.
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
  family: earthquake-plate-calculation
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `earthquake-plate-calculation`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instruction and inspect the available earthquake, plate, and boundary files to identify the requested output fields, any target plate or boundary subset, and whether the task asks for a minimum, maximum, or conditional selection.
# step 2: Summarize the geospatial layers and determine how to link them: treat earthquakes as points, plates as polygons, and plate boundaries as lines so the later spatial filtering and distance calculations use the right geometry types.
# step 3: If the task restricts analysis to earthquakes inside one or more plates, isolate the relevant plate polygon(s) and filter the earthquake points to those contained within them; if the task depends on counts or magnitudes by plate, assign earthquakes to plate polygons first and derive the requested plate subset.
# step 4: Project the point and line layers to an appropriate metric CRS before measuring distance, because Euclidean distance in geographic coordinates is not reliable for kilometer outputs.
# step 5: Compute each candidate earthquake’s nearest distance to the relevant boundary set, using either all boundaries or the boundary subset implied by the instruction, and convert the result to kilometers rounded to the required precision.
# step 6: Select the earthquake that matches the requested extremum or rule after filtering and distance computation, then extract the required earthquake attributes and standardized timestamp format for the output schema.
# step 7: Write a single JSON object to the specified answer path and do a quick sanity check that the file exists, contains exactly the requested fields, and that the chosen record is consistent with the applied spatial filters and extremum rule.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
