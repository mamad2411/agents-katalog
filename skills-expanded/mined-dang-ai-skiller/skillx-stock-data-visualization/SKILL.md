---
name: skillx-stock-data-visualization-skill
description: skillx family-level skill for SkillLearnBench task family stock-data-visualization.
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
  family: stock-data-visualization
  tool_profile: qs_no_tests
  disclosure: family_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  functional_skill_count: 0
  generated_at: '2026-05-22T16:07:55Z'
---

## SkillLearnBench Family Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Task family: `stock-data-visualization`

Use this skill only for this task family. Read the current instruction and visible local files before acting.
Treat every rule below as a reusable procedure with placeholders tied to the current instance.

## Family Plan

# step 1: Read the visible instructions and inspect the available input files to identify the metadata file format, the per-stock history directory contents, the required output file tree, and any explicit DOM or interaction constraints.
# step 2: Prepare the app skeleton with the requested HTML, JavaScript, CSS, and vendored D3 files, and copy the provided datasets into the output data directory so the page can load everything locally.
# step 3: Normalize the visible stock metadata into one deterministic in-browser dataset, preserving all records and fields needed for ticker, company name, sector, and market-cap display regardless of whether the source metadata is tabular or JSON.
# step 4: Build a two-column layout with a force-directed bubble chart and a data table side by side; size bubbles by market cap with a uniform fallback for entries lacking it, color by sector, label each bubble with its ticker, and keep all text fully visible.
# step 5: Implement the force simulation using sector-based targets plus collision forces so same-sector bubbles cluster in compact centered groups without overlap, and render the legend as ordinary HTML div elements rather than SVG so only stock bubbles use SVG circle elements.
# step 6: Add interactions that show tooltips only for records with the required company fields and synchronize selection between bubbles and table rows, so clicking either view highlights the corresponding item in the other.
# step 7: Sanity-check relative asset paths, rendered DOM structure, SVG contents, copied data links, and browser output; fix the first concrete mismatch, then finalize only when all required files exist and the page satisfies the visible constraints.

## Extracted Functional Procedures

No functional SkillX procedure was recovered for this family. Follow the family plan and visible verifier contract directly.

## Completion Contract

Create the artifact requested by the current instance using the visible instruction and local files.
Do a lightweight local sanity check when useful. Finish with the exact completion marker required by the task.
