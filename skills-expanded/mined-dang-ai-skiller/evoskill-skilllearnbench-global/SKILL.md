---
name: evoskill-skilllearnbench-global-skill
description: Global one-shot evoskill skill library injection for skilllearnbench
  executor smoke and evaluation.
allowed-tools:
- list_dir
- read_file
- write_file
- python
- shell
metadata:
  benchmark: skilllearnbench
  source_method: evoskill
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-22T15:53:14Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: list_dir, read_file, write_file, python, shell

### Method Skill Library

#### Skill 1: build-dbscan-pareto-frontier

Description: Use this skill when a task asks you to tune DBSCAN over an instruction-defined parameter grid and produce a Pareto-frontier CSV that maximizes one public metric while minimizing another.

## When to use
- The task specifies DBSCAN hyperparameter search ranges in the prompt and requires a CSV artifact of Pareto-optimal settings.
- The prompt defines a custom DBSCAN distance formula, possibly with an extra control parameter such as `<shape parameter>`.
- Evaluation uses one metric to maximize and another to minimize, with explicit filtering thresholds, averaging rules, or matching rules.
- A family-specific `dbscan_grid_search` route is available and preferred over manual reimplementation.

## Procedure
1. Read the visible instruction and extract `<citizen dataset>`, `<expert dataset>`, `<join key>`, parameter grids for `<min_samples>`, `<epsilon>`, and any extra parameter, the custom DBSCAN distance, evaluation semantics, filter thresholds, output path, column order, and rounding rules.
2. Keep clustering distance separate from evaluation distance. Record any prompt-stated matching rule, per-group loop rule, and NaN/empty-case averaging behavior.
3. Run the dedicated `dbscan_grid_search` workflow with the extracted search space and task-specific metric definition instead of rebuilding the sweep ad hoc.
4. Collect candidate rows and discard any row that fails the visible threshold on the maximize metric or other prompt-stated filters.
5. Compute or verify Pareto optimality: keep row `<a>` only if no other row is at least as good on both objectives and strictly better on one, using the prompt’s maximize/minimize directions.
6. Format the surviving rows exactly as requested. Preserve integer fields as integers, round decimal fields to the required precision, order columns exactly, and write to `<output csv>` deterministically.
7. Sanity-check that the file exists, headers match exactly, all rows satisfy visible constraints, and no dominated row remains.

## Notes / caveats
- Do not assume a fixed distance family; the custom DBSCAN metric may vary across tasks.
- Do not substitute the clustering distance for the evaluation or matching distance if the prompt distinguishes them.
- Average only as instructed, especially for missing groups, unmatched cases, and NaN handling.
- Use only prompt-visible requirements and visible tool outputs, not prior solution artifacts or hidden checks.

#### Skill 2: compile-branded-poster-spec

Description: Use this skill when a task asks for a branded image plus a companion JSON file and the brief specifies output paths, exact schema keys, brand token roles, typography, composition constraints, or restrained visual-style requirements.

## When to use
- The task requires both an image artifact and a metadata or parameter JSON sidecar.
- The brief assigns named brand tokens to specific visual roles such as background, dominant forms, accents, or annotation lines.
- The prompt includes exact output paths, exact JSON keys, required headings, or composition constraints that must be preserved literally.
- The style must stay minimalist, low-saturation, or explicitly avoid gradients, glow, neon, or promotional treatment.

## Procedure
1. Read the visible brief and any visible inventory files for `<current task>` before drawing anything.
2. Extract a normalized spec with: `<image output path>`, `<json output path>`, exact JSON keys, required text labels, composition type, required structural elements, object-count constraints, and negative style constraints.
3. Resolve each named brand token into a concrete value only if the prompt or approved lookup provides it; otherwise leave a placeholder such as `<background token value>`.
4. Convert the brief into a minimal render recipe: define canvas intent, layout zones, heading placement, dominant forms, annotation treatment, and which element receives each token role.
5. Limit accent usage to the smallest amount that still satisfies the brief; keep neutrals and major structure dominant unless the prompt says otherwise.
6. Build a sidecar manifest mapping each exact JSON key to the value source that will populate it, including any required font field.
7. Create a pre-render checklist covering file paths, exact schema, required text presence, required modules or layers, role-to-color consistency, and restrained overall styling.
8. Save the structured spec or checklist to `<current file>` for downstream rendering and verification.

## Notes / caveats
- Preserve exact output paths and exact JSON key names; do not rename or reorder casually.
- Use only visible requirements; do not infer hidden grading rules or copy prior artifacts.
- Prefer a simple, compliant composition when the brief is underspecified.
- Separate required structural content from stylistic preferences so later validation is deterministic.

#### Skill 3: compute-earthquake-distance-to-plate-boundary

Description: Use this skill when a task asks you to identify an earthquake by nearest or farthest distance to tectonic plate boundaries, optionally after restricting events to one or more plate polygons or a derived plate-selection rule, and the inputs are visible geospatial point, polygon, and boundary layers.

## When to use
- The task asks for the earthquake closest to or furthest from a plate boundary.
- Earthquakes must first be limited to events inside a named plate or set of plates.
- The instruction derives the target plate indirectly, such as by event counts or another ranking rule.
- You must write one JSON object containing source attributes plus a computed `distance_km` field.

## Procedure
1. Read the instruction and extract the required output path, requested JSON keys, ranking rule, boundary scope, and any plate filter or derived selection rule.
2. Inspect the available geospatial files and identify the earthquake point layer, plate polygon layer, and boundary line layer. Prefer `geo_layer_summary` first.
3. If the task requires plate membership, isolate the relevant polygon set and filter earthquake points to those inside it with `geo_filter_points_in_polygon`, or use `run_python` if the rule is more complex.
4. Project the candidate points and relevant boundary lines into an appropriate metric CRS using `geo_project_layers` or a deterministic GeoPandas workflow. Do not measure in geographic coordinates.
5. Compute each candidate point's nearest distance to the correct boundary set with `geo_distance_to_boundary` or GeoPandas. Keep distances in meters until selection is complete.
6. Apply the task's selection rule on unrounded distances, then convert the winning distance to kilometers and round to exactly two decimals.
7. Build one JSON object with the requested earthquake attributes, normalize `time` to ISO 8601 if needed, add `distance_km`, write it to `<output path>`, and verify the file exists with exactly the requested keys.

## Notes / caveats
- Match the boundary set to the instruction: global boundaries may differ from boundaries relevant to a selected plate context.
- Round only at final output time; early rounding can change winners in near-ties.
- Preserve original attribute values unless the task explicitly requires normalization, especially for timestamps.
- Use family geospatial tools when they fit; fall back to `run_python` only for joins, custom filtering, or formatting the final object.

## Example
A task provides earthquake points, plate polygons, and plate-boundary lines, asks for the event inside a selected plate that is farthest from its boundary, and requires a single JSON result. Filter events to the chosen plate, project to a metric CRS, compute nearest boundary distances, rank on unrounded values, and write the winning event with `distance_km`.

#### Skill 4: constrained-model-calibration-with-exact-metrics

Description: Use this skill when a task asks you to calibrate a scientific model under explicit editable-parameter bounds and success depends on producing required run artifacts and computing the grader’s visible metrics exactly as specified.

## When to use
- The task permits edits to only a named subset of model parameters and gives numeric bounds for each.
- The task requires a successful simulation run plus output files at specific paths.
- The grader defines metrics with an exact merge, filtering, binning, or schema that must be matched precisely.
- Family-specific tools exist for reading configs, editing parameters, running the model, sweeping candidates, or computing public metrics.

## Procedure
1. Read the visible instructions and inspect the available files. Extract: editable parameters, forbidden fields, parameter bounds, required output paths, run window, metric names, merge rules, and output schema.
2. Read the current configuration from <config file>. Record baseline values for all editable and nearby non-editable fields.
3. Prefer domain-specific tools to inspect and edit the config, run the model, summarize outputs, and compute metrics. Fall back to lightweight scripting only if needed.
4. Generate bounded candidate settings for only the allowed parameters within <published ranges>. Use small sweeps or iterative trial runs rather than broad ad hoc changes.
5. After each candidate, run the model and confirm the expected artifact exists at <output path> and appears structurally valid.
6. Compute evaluation metrics using the exact visible protocol from <current task>: same join keys, rounding rules, filters, subsets, and JSON keys. Do not substitute alternative matching logic.
7. Select the best candidate that satisfies all visible thresholds. Write the final config, rerun once, and save the exact metrics report to <metrics file>.
8. Verify that only permitted parameters changed, all final values remain in range, required files exist, and the metric schema matches the specification exactly.

## Notes / caveats
- Do not edit convenience-adjacent fields unless they are explicitly allowed.
- Do not exceed bounds during sweeps; invalid intermediate settings can waste time or fail verification.
- Do not approximate the scorer with nearest-time joins, interpolation, or alternate binning when exact rules are given.
- Do not finalize on a promising run alone; confirm both artifact paths and metric-file keys before stopping.

#### Skill 5: count-video-objects-from-templates

Description: Use this skill when a task asks you to count requested object classes in each extracted video frame using visible template images, especially when the prompt specifies an exact CSV schema, wildcard template patterns, grayscale preprocessing, or zero-fill behavior for classes with no template.

## When to use
- The task requires per-frame object counts from a video and provides one or more template images for matching.
- The prompt specifies exact output columns, frame-id formatting, or a required output file/table path.
- Some classes may have multiple template files matched by a pattern and all must be used.
- A requested class may have no template, and the instruction defines that missing-template counts should be written as zero.

## Procedure
1. Read the visible instruction and extract: `<video path>`, `<output path>`, ordered columns, requested classes, `<frame id format>`, whether grayscale is required, and any rule for missing templates.
2. List available files in `<template directory>` and group template paths by requested class, expanding any visible wildcard pattern into all matching files.
3. Extract keyframes from `<video path>` into `<keyframe directory>` and sort them in timeline order.
4. If required, convert each extracted frame in place to grayscale before counting.
5. For each frame and each requested class, do one of the following:
   - If templates exist, run template matching with every template for that class.
   - Merge detections across templates and deduplicate overlapping hits so one object instance is counted once.
   - If no template exists and the prompt says absence maps to zero, emit `0` for that class.
6. Build rows using the exact `<frame id format>` and the exact requested column order.
7. Write the result to `<output path>` with `write_table` or `write_file`.
8. Sanity-check that the artifact exists, row order matches the timeline, and headers exactly match the prompt.

## Notes / caveats
- Preserve timeline order; do not reorder frames lexically if that breaks sequence.
- Use all templates for a class; do not stop after the first matching file.
- Do not invent unsupported classes or infer counts for classes without an explicit template rule.
- Deduplicate multi-template matches carefully or counts will be inflated.

## Example
A task asks for per-frame counts of several sprite types, provides multiple example images for some types, omits another type, and requires grayscale keyframes plus an exact CSV schema. Extract frames, grayscale them, count each class with all available templates, zero-fill the omitted class only if instructed, then write the table exactly as requested.

#### Skill 6: fill-docx-template-with-conditionals

Description: Fill a DOCX template from visible structured data while preserving formatting and resolving simple IF/END_IF conditional blocks when a task provides a Word template, a JSON-like data source, and an explicit output path.

## When to use
- The task provides a `.docx` template containing placeholder tokens and asks for a completed `.docx` output.
- The values come from a visible structured source such as JSON, TOML, or a clearly readable text file.
- The template includes simple control markers like `{{IF_<flag>}}...{{END_IF_<flag>}}` that must be kept or removed based on visible data.
- You need to preserve the original document structure and styling rather than recreating the file manually.

## Procedure
1. Read the instruction and visible files. Identify `<template file>`, `<data file>`, `<output path>`, and any explicit rules for placeholders, conditionals, or artifact type.
2. Inspect the template first. Use DOCX-specific placeholder extraction if available to list the actual tokens present, including any conditional markers.
3. Read `<data file>` and build a mapping only for placeholders that appear in `<template file>` and have visible values. Do not invent missing fields.
4. Resolve each conditional block `{{IF_<flag>}}...{{END_IF_<flag>}}` before or during fill: keep inner content and remove markers when the visible condition is true; otherwise remove the entire block.
5. Fill the remaining placeholders using a DOCX-aware tool that preserves formatting. Use Python or shell only for the narrow transformation needed if the built-in tool cannot handle the conditional logic.
6. Save the completed document to `<output path>`.
7. Verify the result with a lightweight pass: confirm the file exists, preview document text or inspect metadata, and check that unresolved placeholder or conditional markers are gone.
8. If verification finds a concrete mismatch, fix the first one and re-verify before finishing.

## Notes / caveats
- Use only prompt-visible facts and files.
- Avoid rewriting the document from scratch; preserve template styling and layout.
- Match condition checks deterministically against the visible source values.
- Verify the requested artifact type, not just the text content.

## Example
A task includes a template letter, a structured employee record, and a requested output file. Extract the template tokens, map only visible fields that are actually used, resolve a relocation-style conditional block, save the filled DOCX, then preview the text to ensure no markers remain.

#### Skill 7: fill-excel-lookups-and-weighted-summary

Description: Use this skill when a spreadsheet task requires filling designated cells from a source sheet with two-key lookup formulas, then computing row-wise percentage metrics, summary statistics, and a SUMPRODUCT-based weighted mean without changing workbook formatting or structure.

## When to use
- The workbook already contains task and source sheets, and instructions require editing only specified cells.
- The task asks for lookup formulas keyed by two conditions, such as a row identifier plus a header year.
- The filled lookup ranges feed downstream formulas for ratios, percentages, quartiles, or other descriptive statistics.
- The instructions explicitly forbid changing styles, adding sheets, macros, or structural elements.

## Procedure
1. Inspect `<workbook>` and read the visible instructions. Identify `<task sheet>`, `<source sheet>`, `<lookup ranges>`, `<derived ranges>`, and any rounding or percent-scaling requirements.
2. Locate the two lookup keys on the task sheet: `<row key cells>` and `<column key cells>`. Confirm the matching key columns and header row on the source sheet.
3. Build one reusable two-condition lookup formula for the first target cell using an allowed pattern such as `INDEX/MATCH`, `XLOOKUP` plus header match, or another permitted equivalent. Keep references anchored so the formula fills correctly across `<lookup ranges>`.
4. Write and propagate the lookup formula through each required fill block. Do not hardcode values from the source sheet.
5. Add formulas for each derived metric in `<derived ranges>` using the looked-up inputs. If the sheet expects displayed percent values, multiply by `<scale factor>` inside the formula.
6. Add summary formulas over the computed block for `<summary statistic list>` using the required ranges.
7. Add the weighted mean formula as `SUMPRODUCT(<value range>, <weight range>) / SUM(<weight range>)`, or the exact instructed denominator.
8. Recalculate the workbook if available, then verify formulas landed in the intended cells and styles remained unchanged.

## Notes / caveats
- Infer ranges and formula shape from the visible workbook; do not assume fixed dimensions.
- Preserve existing formatting by writing formulas only into the specified cells.
- Check absolute versus relative references before filling across rows and columns.
- Confirm whether rounding should come from formula design, existing cell formatting, or both.

#### Skill 8: fill-pdf-form-from-visible-case-facts

Description: Fill a structured PDF form from a visible case narrative when a task asks you to complete a legal or administrative form using only prompt-provided facts while leaving optional, court-filled, or unspecified fields blank.

## When to use
- The task provides a blank PDF form plus a narrative or intake note describing parties, dates, amounts, contact details, and claim facts.
- The instructions explicitly say to fill only necessary fields and keep unsupported, optional, or court-filled fields empty.
- The output must be a completed PDF at a specified path, often with date-format constraints.
- The form may vary in field names or layout, so you need to inspect the schema before mapping values.

## Procedure
1. Read the visible instructions and extract the blank form path, output path, required date format, and any verification requirements.
2. Parse only visible facts into a structured note: plaintiff(s), defendant(s), addresses, phones, emails, filing-history indicators, venue facts, claim amount, claim basis, communication history, dispute date range, and signing or filing date.
3. Inspect the PDF with `pdf_list_form_fields`; use `pdf_extract_text` or `pdf_render_pages` if labels or field placement are unclear.
4. Build a conservative field map from extracted facts to form fields. Normalize dates with `date_normalize` to `<required date format>`. Handle variants such as multiple plaintiffs or first-time versus repeat filing indicators.
5. Fill the PDF with `pdf_fill_form_fields`, writing only fields supported by visible evidence. Leave every unsupported field untouched.
6. Run `pdf_field_value_dump` on the filled output. Verify that all required visible facts landed in plausible fields and that no optional or unstated fields were populated.
7. If a mismatch appears, fix the mapping and refill. Then produce the requested output plus a concise populated-field summary.

## Notes / caveats
- Do not infer legal details, venue specifics, or checkbox states unless the prompt states them.
- Do not copy from hidden answer tables, prior outputs, or non-visible sources.
- Prefer dedicated PDF form tools over ad hoc scripting; use scripts only for small deterministic transformations.
- Watch for duplicated or similarly named fields and for one-party versus two-party sections.

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested artifact using the visible instruction and local files, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: list_dir, read_file, write_file, python, shell
