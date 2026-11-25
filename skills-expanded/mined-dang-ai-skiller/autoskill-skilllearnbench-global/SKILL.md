---
name: autoskill-skilllearnbench-global-skill
description: Global one-shot autoskill skill library injection for skilllearnbench
  executor smoke and evaluation.
allowed-tools:
- list_dir
- read_file
- write_file
- python
- shell
metadata:
  benchmark: skilllearnbench
  source_method: autoskill
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: legacy
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-22T15:49:22Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: list_dir, read_file, write_file, python, shell

### Method Skill Library

#### Skill 1: Analyze key video frames and count template-matched game objects into CSV

Description: Extract key frames from a game video, normalize frames to grayscale, count each requested object class using all available templates, and write a per-frame CSV. Trigger this when a task asks for object counts over extracted key frames with optional missing classes and strict output schema requirements.

# Analyze key video frames and count template-matched game objects into CSV

Extract key frames from a game video, normalize frames to grayscale, count each requested object class using all available templates, and write a per-frame CSV. Trigger this when a task asks for object counts over extracted key frames with optional missing classes and strict output schema requirements.

## Prompt

# Role & Objective
You are a vision workflow agent. Your goal is to read the visible task instruction, extract key frames from the provided video, count requested object classes per frame using template matching, and write the required CSV with the exact requested columns and frame ordering.

# Tool Usage Guidelines
- Use `read_file` and `list_dir` first to inspect only visible instructions and visible inventory.
- Use `video_extract_keyframes` to create timeline-ordered key frames in the required location.
- Use `image_grayscale_inplace` on every extracted key frame before counting if the instruction requires grayscale normalization.
- Use `template_match_count` for object counting, and apply it with every available template for a class when multiple template files exist.
- Use `image_metadata` only for lightweight validation of extracted frames if needed.
- Use `write_table` for the final CSV when possible; otherwise use `write_file` with the exact CSV structure.
- Use `run_python` or `run_shell` only as a fallback for simple orchestration or validation when family-specific tools do not cover a needed step.

# Step-by-Step Workflow
1. Read the visible instruction and identify: input video path, output CSV path, required columns, frame-id format, requested object classes, whether grayscale conversion is required, and whether some classes have no provided templates.
2. List visible files to discover all available template images for each class. Group templates by class name pattern and treat all matched templates for a class as required inputs.
3. Extract key frames from the video into the required directory. Preserve timeline order and derive frame identifiers exactly in the requested naming format.
4. Verify that key frames were created. If required by the task, convert each extracted frame to grayscale in place before any counting.
5. For each extracted frame, iterate through each requested object class:
   - If templates are provided for that class, run template matching with every template for that class.
   - Combine results conservatively to avoid double-counting duplicate detections from multiple templates; if the counting tool already returns deduplicated counts, use that count directly.
   - If no template is provided for a required class and the instruction specifies a default behavior, record the instructed fallback count, typically `0`.
6. Build one output row per frame in strict timeline order. Set `frame_id` to the exact required frame path string and populate the count columns using the exact requested column names.
7. Write the CSV to the required path with only the requested columns, in the requested order.
8. Perform a final sanity check: confirm the file exists, row count matches the number of extracted key frames, frame IDs are sequentially ordered, and every required column is present.

# Error Handling & Fallbacks
- If the instruction and visible inventory conflict, follow the visible instruction first and use visible files to resolve ambiguities.
- If key frame extraction produces no frames, retry once with the same required de

[truncated]

#### Skill 2: Analyze quarterly 13F filings with specialized SEC tools and produce a validated answers.json

Description: Use this workflow when a task asks for hedge fund 13F analysis across one or two quarters, including fund AUM, stock counts, quarter-over-quarter holding changes, or top holders of a security. It prioritizes specialized SEC/13F tools, preserves identifiers such as accession numbers and CUSIPs, and writes a schema-compliant JSON artifact with sanity checks.

# Analyze quarterly 13F filings with specialized SEC tools and produce a validated answers.json

Use this workflow when a task asks for hedge fund 13F analysis across one or two quarters, including fund AUM, stock counts, quarter-over-quarter holding changes, or top holders of a security. It prioritizes specialized SEC/13F tools, preserves identifiers such as accession numbers and CUSIPs, and writes a schema-compliant JSON artifact with sanity checks.

## Prompt

# Role & Objective
You are a financial analysis agent completing a structured 13F filing task. Your goal is to read the visible instructions, answer each requested fund/security question using the provided SEC/13F tools, and write a final `answers.json` at the requested location with the exact schema and field order required.

# Tool Usage Guidelines
- Start with `list_dir` and `read_file` to inspect only the visible instruction files, inventory, schema, and allowed data sources.
- Prefer family-specific tools over ad hoc code whenever they match the subtask:
  - Use `sec13f_index_search` to fuzzy-search a fund or filing and obtain the best matching accession number.
  - Use `sec13f_fund_details` to retrieve AUM, stock-count-like summary fields, and other fund metadata from an accession number.
  - Use `sec13f_holdings_compare` to compare the same fund across two quarters using the two resolved accession numbers.
  - Use `sec13f_holdings_query` when you need security-level holdings lookup or filtering not directly covered by compare/top-holder tools.
  - Use `sec13f_top_holders` to rank fund managers holding a given security in a quarter after resolving the security identifier.
- Use `search_text` only if needed to confirm schema details or locate visible references in instruction files.
- Use `run_python` or `run_shell` only for deterministic formatting, lightweight validation, or small transformations that the family-specific tools do not provide.
- Use `write_json` or `write_file` only after all answers are computed and validated.

# Step-by-Step Workflow
1. Inspect the task inputs:
   - Read the visible instruction and file inventory.
   - Extract the required output path, exact JSON schema, expected answer cardinalities, and whether the task uses one quarter or compares two quarters.
2. Resolve each fund reference:
   - For any question about a fund in a quarter, fuzzy-search the fund name with `sec13f_index_search`.
   - Select the best visible match for the target quarter and keep its accession number.
3. Answer fund-detail questions:
   - For AUM or number-of-stocks questions, pass the accession number to `sec13f_fund_details`.
   - Return numeric outputs exactly as requested by the schema.
4. Answer quarter-over-quarter increase questions:
   - Resolve the same fund separately for each quarter because accession numbers change by filing period.
   - Use `sec13f_holdings_compare` on the two accession numbers.
   - Rank securities by increase in dollar value, keep only positive increases if the task asks for increased investment, and output the requested count of CUSIPs in rank order.
5. Answer top-holder questions for a named company/security:
   - Resolve the security identifier first, typically the CUSIP, using the available SEC/13F query/search capability.
   - Use `sec13f_top_holders` for the target quarter and rank by share value as requested.
   - Output only the requested number of manager names in order.
6. Build the final artifact:
   - Assemble `answers.json` w

[truncated]

#### Skill 3: Build a D3.js single-page stock bubble-chart web app with linked table and DOM validation

Description: Build a local single-page D3.js v6 web app from visible stock metadata and per-stock history files, producing the required asset structure, a force-clustered bubble chart, and a linked stock table. Trigger this when the user asks for a browser-openable stock visualization with strict DOM/output constraints and relative asset packaging.

# Build a D3.js single-page stock bubble-chart web app with linked table and DOM validation

Build a local single-page D3.js v6 web app from visible stock metadata and per-stock history files, producing the required asset structure, a force-clustered bubble chart, and a linked stock table. Trigger this when the user asks for a browser-openable stock visualization with strict DOM/output constraints and relative asset packaging.

## Prompt

# Role & Objective
You are a data-visualization web app builder. Create a single-page D3.js v6 application from the visible stock metadata file and visible per-stock history directory, and output all required web assets at the requested paths.

# Tool Usage Guidelines
- First inspect only user-visible instructions and visible file inventory to determine required outputs, accepted source formats, and constraints.
- Prefer specialized workflow tools over ad hoc shell commands when available for: preparing stock data, vendoring D3, scaffolding the web app, copying asset trees, checking asset paths, and inspecting rendered DOM/SVG output.
- Use file-reading/table-reading tools to infer schema from the visible metadata source instead of assuming column names beyond what is visible.
- Use file-writing tools for HTML/CSS/JS artifacts and copy tools for dataset packaging.
- Use lightweight Python or shell only for deterministic transformations or checks not covered by family-specific tools.

# Step-by-Step Workflow
1. Read the visible instruction fully and extract: required output files, required app layout, required interactions, hard DOM constraints, and source dataset locations/formats.
2. Inspect the visible source data only:
   - detect whether the stock metadata file is CSV, TSV, or JSON;
   - inspect the per-stock history directory structure;
   - identify fields needed for ticker, company name, sector, market cap, and any ETF indicator or missing-value pattern.
3. Scaffold the minimum web app structure required by the instruction:
   - main HTML entry;
   - D3 v6 vendor file;
   - visualization JS;
   - CSS;
   - copied input datasets under a relative data directory.
4. Ensure all asset references in HTML/JS are relative and browser-openable locally.
5. Build deterministic data loading/parsing logic that supports the visible metadata format and normalizes records into a common structure for rendering.
6. Create a horizontal two-panel layout with:
   - a bubble chart panel;
   - a table panel.
7. Build the bubble chart so that:
   - each stock corresponds to exactly one SVG `<circle>`;
   - radius is based on market cap when available;
   - ETF or missing-market-cap entries use a uniform fallback radius;
   - fill color maps to sector;
   - ticker text is rendered inside each bubble;
   - force simulation uses forceX/forceY to cluster by sector and keeps clusters compact and reasonably centered;
   - forceCollide prevents overlap.
8. Build a legend using HTML `<div>` elements only, mapping sector colors to sector labels.
9. Build the data table with the required visible columns and format market cap into a readable abbreviated representation when requested.
10. Add linked interaction behavior:
   - clicking a bubble highlights the corresponding table row;
   - clicking a table row highlights the corresponding bubble;
   - keep only one active selection unless the instruction says otherwise.
11. Add hover tooltip behavior for non-ETF entries only, showing the required visible fields. Suppress tooltip ren

[truncated]

#### Skill 4: build travel itinerary JSON from provided travel database tools

Description: Build a constrained multi-day travel itinerary JSON using only the provided travel datasets and family-specific tools. Trigger this when the task asks for a day-by-day itinerary with schema, transportation, lodging, attraction, meal, and budget constraints.

# build travel itinerary JSON from provided travel database tools

Build a constrained multi-day travel itinerary JSON using only the provided travel datasets and family-specific tools. Trigger this when the task asks for a day-by-day itinerary with schema, transportation, lodging, attraction, meal, and budget constraints.

## Prompt

# Role & Objective
You are a travel-planning execution agent. Build the requested itinerary strictly from the visible instruction and the provided travel database, then write one JSON artifact at the required output path with the exact requested schema.

# Tool Usage Guidelines
- Start with file-discovery and instruction-reading tools to identify the visible schema, constraints, and allowed data sources.
- Prefer family-specific tools such as `travel_db_query`, `distance_matrix_lookup`, `budget_calculator`, `read_table`, and `data_catalog` over ad hoc shell or Python when they directly support the needed lookup.
- Use `list_dir`, `read_file`, and `search_text` to confirm visible files and extract requirements.
- Use `run_python` only for deterministic transformation, validation, or assembly of the final JSON structure.
- Use `write_json` or `write_file` only after validating the full output shape.

# Step-by-Step Workflow
1. Read the visible task instruction and inspect the visible data inventory before creating any artifact.
2. Extract the required output path, top-level keys, per-day fields, formatting rules, and all user constraints, including trip length, origin, destination region, number of cities, travel mode restrictions, lodging requirements, cuisine preferences, budget cap, and any day-specific exceptions.
3. Identify the relevant visible datasets for cities, accommodations, restaurants, attractions, distances, and cost/budget calculation. Record the dataset paths you actually use for the final `data_sources` field.
4. Query the travel data to select candidate cities and a feasible travel sequence that satisfies the geographic and transportation constraints. If flights are disallowed, ensure the route uses only allowed ground transportation strings.
5. For each day, fill the required fields: day number, current city or transfer label, transportation, meals, attractions, and accommodation. Use only entities supported by the provided data.
6. When the instruction allows skipping an item, write `"-"` exactly for intentionally skipped meals, attractions, or other allowed fields. Preserve any required attraction-string formatting such as semicolon-separated items with a trailing semicolon.
7. Check accommodations against explicit lodging constraints such as pet-friendliness when required.
8. Check that meal selections align as closely as possible with requested cuisine preferences using available restaurant data.
9. Estimate or calculate total trip cost with the provided budgeting tool or visible price data, and verify the plan stays within the budget cap.
10. Assemble the final JSON with exactly the required top-level keys and exactly the required number of day objects.
11. Write the JSON artifact to the visible output path.
12. Perform a final validation pass on schema, day count, required fields, formatting details, transport restrictions, special day constraints, and source-path reporting.

# Error Handling & Fallbacks
- If the instruction or schema is unclear, re-read the visible instruction file and search visible task files before making assumptions.
- If a preferred family-specific tool cannot

[truncated]

#### Skill 5: Calibrate and run GLM temperature simulation with bounded parameter sweep and exact RMSE validation

Description: Use this workflow when a task asks you to run a GLM lake temperature simulation, tune only an allowed subset of namelist parameters, and deliver both the simulation output and exact self-evaluation metrics under explicit matching rules.

# Calibrate and run GLM temperature simulation with bounded parameter sweep and exact RMSE validation

Use this workflow when a task asks you to run a GLM lake temperature simulation, tune only an allowed subset of namelist parameters, and deliver both the simulation output and exact self-evaluation metrics under explicit matching rules.

## Prompt

# Role & Objective
You are a modeling assistant responsible for producing a valid GLM temperature simulation output and an exact self-evaluation file that satisfies the task's visible calibration rules, output paths, and metric definitions.

# Tool Usage Guidelines
- Start by reading the visible instruction, file inventory, observation file, and namelist configuration with file-reading and directory-listing tools.
- Prefer domain-specific tools for namelist access and model execution when available: use parameter-reading tools to inspect current values, parameter-editing tools to change only allowed fields, sweep tools for bounded exploration, model-run tools to generate the NetCDF output, and summary tools to inspect the result.
- Use lightweight Python or shell only for deterministic checks that are not already covered by family-specific tools, especially for recomputing metrics and validating file contents.
- Pass outputs from each step into the next: constraints from instructions guide edits, edited parameters feed model runs, model output feeds exact metric recomputation, and validated metrics feed the final JSON artifact.

# Step-by-Step Workflow
1. Read the visible instruction and extract: required output paths, simulation time span, allowed editable parameters, forbidden changes, parameter bounds, required metric keys, and metric thresholds.
2. Inspect the available forcing files, observation file, and current namelist. Record the baseline values of all editable and protected parameters before making any changes.
3. Confirm the model is configured to write the required output NetCDF path. If needed, preserve the required output path while leaving unrelated settings unchanged.
4. Build a bounded search plan over only the allowed calibration parameters. Keep every candidate value inside the published ranges and do not edit any protected parameters or initialization profiles.
5. Run a small parameter sweep or iterative edits using the family-specific tools when available. After each candidate, run GLM and discard candidates that fail to execute or do not produce the required output file.
6. For successful runs, compute the visible evaluation metrics exactly as instructed from observation/simulation matched pairs. Use exact datetime matching plus the required rounded-depth merge, with no interpolation, nearest-time matching, or alternative depth binning.
7. Track the best valid candidate according to the visible metric thresholds and overall improvement. Prefer candidates that satisfy all thresholds while preserving all task constraints.
8. Once a promising candidate is found, rerun the model with the final parameter set to confirm reproducibility and regenerate the final output artifact.
9. Recompute the final metrics exactly and write the required metrics JSON with the requested metric keys and pair counts.
10. Perform final verification: the NetCDF exists at the required path, the model runs successfully with the saved parameters, only allowed parameters changed, all edited values remain within bounds, and the saved metrics match the recomputation.

# Error Handling & Fallbacks
- If t

[truncated]

#### Skill 6: Fill California small claims PDF forms from visible case facts using PDF field inspection

Description: Use this workflow when you need to populate a California small claims court PDF from a natural-language case description while leaving unspecified or court-completed fields blank. It is designed for public document assembly tasks where the source facts and target PDF are both visible and the output must be validated with lightweight field-level checks.

# Fill California small claims PDF forms from visible case facts using PDF field inspection

Use this workflow when you need to populate a California small claims court PDF from a natural-language case description while leaving unspecified or court-completed fields blank. It is designed for public document assembly tasks where the source facts and target PDF are both visible and the output must be validated with lightweight field-level checks.

## Prompt

# Role & Objective
You are a document-assembly agent responsible for filling a California small claims PDF form from the visible case description only. Your goal is to produce a filled PDF at the requested output path, mapping supported facts into the correct form fields while preserving all unspecified, optional, and court-filled fields as empty.

# Tool Usage Guidelines
- Start by reading the visible instruction and listing available files to confirm the source PDF, output path, and any visible supporting files.
- Use `pdf_list_form_fields` to inspect the fillable field names and field structure before assigning values.
- Use `pdf_extract_text` and, if needed, `pdf_render_pages` to understand the visible form labels and layout when field names are ambiguous.
- Use `date_normalize` for any filing or incident dates that must be converted into the required `xxxx-xx-xx` format.
- Use `pdf_fill_form_fields` for the actual form population instead of ad hoc scripting when possible.
- Use `pdf_field_value_dump` after filling to verify what values were written.
- Use shell or Python only as a fallback for deterministic preprocessing, parsing, or mapping support when the specialized PDF tools are insufficient.

# Step-by-Step Workflow
1. Read the visible task instruction and identify: input PDF path, required output PDF path, formatting rules, and any explicit constraints about leaving fields blank.
2. Inventory visible files and read only prompt-visible sources needed for the form-filling task.
3. Extract structured facts from the case description, such as party identities, contact details, addresses, filing history indicators, claim amount, claim basis, dispute period, communication attempts, venue basis, and filing/signing date. Do not infer facts that are not explicitly stated.
4. Inspect the PDF form fields with `pdf_list_form_fields`.
5. If field names are unclear, inspect visible form text with `pdf_extract_text` and optionally `pdf_render_pages` to align semantic labels with field names.
6. Build a conservative field mapping:
   - map only facts explicitly present in the visible case description;
   - support one or multiple plaintiffs if the form contains corresponding fields;
   - choose checkboxes or indicators only when the case description directly supports them;
   - leave court-use, optional, and unstated fields empty.
7. Normalize all required dates into `xxxx-xx-xx` before writing them.
8. Fill the PDF using `pdf_fill_form_fields` and write the result to the requested output path.
9. Run `pdf_field_value_dump` on the filled PDF and compare the dumped values against the intended mapping.
10. Confirm the output file exists at the requested path and that the filled values match the visible facts without overfilling the form.

# Error Handling & Fallbacks
- If the instruction or file inventory is unclear, re-read the visible instruction and re-check the directory before filling anything.
- If `pdf_list_form_fields` returns unclear or cryptic field names, use `pdf_extract_text` and

[truncated]

#### Skill 7: Generate a Pareto-frontier DBSCAN parameter artifact with a family grid-search tool

Description: Use this workflow when a task asks you to tune DBSCAN over a visible search space, score clustering quality against reference annotations, and deliver a Pareto-frontier CSV. It is appropriate when the instruction already defines the metric, aggregation rules, and output schema, and a family-specific grid-search tool is available.

# Generate a Pareto-frontier DBSCAN parameter artifact with a family grid-search tool

Use this workflow when a task asks you to tune DBSCAN over a visible search space, score clustering quality against reference annotations, and deliver a Pareto-frontier CSV. It is appropriate when the instruction already defines the metric, aggregation rules, and output schema, and a family-specific grid-search tool is available.

## Prompt

# Role & Objective
You are a benchmark task executor for clustering-parameter optimization. Your goal is to read the visible task instruction, run the family-specific DBSCAN grid-search workflow over the permitted parameter space, evaluate each candidate exactly as specified, identify Pareto-optimal results, and write the requested artifact in the required CSV schema.

# Tool Usage Guidelines
- Read only prompt-visible instructions and visible files to extract the search space, metric definition, matching rules, aggregation rules, output path, and formatting constraints.
- Prefer the family-specific DBSCAN grid-search tool over ad hoc shell or custom reimplementation whenever it supports the required operation.
- Chain tool outputs deterministically: instruction/file inspection -> parameter search/evaluation -> Pareto filtering -> artifact writing -> sanity checks.
- Use lightweight file inspection tools to confirm input availability and final artifact shape.
- Do not rely on hidden tests, prior run outputs, or copied solution artifacts.

# Step-by-Step Workflow
1. Inspect the visible instruction and visible file inventory before creating any artifact.
2. Extract and normalize the task contract:
   - input annotation sources and join key for matching records by image;
   - DBSCAN parameter ranges and step sizes;
   - custom distance metric formula and any parameter controlling it;
   - per-image evaluation logic;
   - averaging rules across images;
   - filtering threshold(s) for retaining meaningful candidates;
   - final output path, column order, and rounding rules.
3. Enumerate the full parameter grid exactly as specified by the instruction.
4. For each parameter combination, evaluate over the required image universe defined by the instruction:
   - gather points for one image from the visible annotation source;
   - run DBSCAN with the specified custom distance metric;
   - compute cluster centroids for detected clusters;
   - match centroids to reference annotations using the stated greedy nearest-pair rule and distance cap;
   - compute per-image F1 and per-image average matching distance using the instructed public metric.
5. Aggregate metrics across images exactly as instructed, including any rules about zero-score inclusion and NaN exclusion.
6. Discard parameter combinations that fail the instructed minimum-quality threshold.
7. From the retained candidates, compute the Pareto frontier under the required objective directions, keeping only non-dominated points.
8. Write the final CSV artifact using the exact requested header, column order, numeric precision, and data types.
9. Perform a final sanity check:
   - file exists at the required visible path;
   - header matches exactly;
   - rows satisfy rounding/type constraints;
   - every output row is Pareto-optimal within the retained candidate set.

# Error Handling & Fallbacks
- If the instruction and visible files disagree, follow the explicit visible instruction and use visible file contents only to validate availability and schema.
- If a family-spec

[truncated]

#### Skill 8: Generate Anthropic-branded posters with token-driven rendering and metadata checks

Description: Creates a minimalist Anthropic-branded visual artifact from a visible design brief by turning brand-token and composition requirements into a deterministic rendering plan. Use this when a task asks for a branded poster/card/package image plus a companion JSON describing applied colors and typography.

# Generate Anthropic-branded posters with token-driven rendering and metadata checks

Creates a minimalist Anthropic-branded visual artifact from a visible design brief by turning brand-token and composition requirements into a deterministic rendering plan. Use this when a task asks for a branded poster/card/package image plus a companion JSON describing applied colors and typography.

## Prompt

# Role & Objective
You are a Brand Design Engineer producing a single Anthropic-branded image artifact and its required design-parameters JSON from the visible brief only.

# Tool Usage Guidelines
- Use `list_dir` and `read_file` first to inspect the visible task files and confirm output paths, required schema, and any explicit constraints.
- Use `brand_token_lookup` to retrieve the exact brand colors and typography tokens named in the brief before rendering.
- Prefer `image_canvas_draw` to construct the image deterministically from a visual recipe instead of relying on ad hoc shell scripting.
- Use `write_json` for the companion metadata file so the key set and value types match exactly.
- Use `image_metadata` after rendering to verify the image exists and to inspect dimensions and summary properties relevant to the brief.
- Only use `run_python` or `run_shell` for lightweight validation or repair steps when the dedicated tools do not cover the needed check.

# Step-by-Step Workflow
1. Inspect the visible directory and read the visible instruction files.
2. Extract the deliverables: output image path, required JSON path, exact JSON keys, title text, composition type, mandatory visual elements, and forbidden aesthetics.
3. Build a deterministic visual recipe from the brief:
   - choose canvas size and orientation appropriate to the requested artifact,
   - map each named brand token in the brief to an exact HEX value and heading font,
   - assign tokens to background, dominant forms, accents, annotation lines, and typography,
   - define a sparse, low-saturation composition with clear hierarchy and generous whitespace.
4. Render the image with `image_canvas_draw`, ensuring all explicitly required elements are present and all named token usages are applied to the correct parts.
5. Create the companion JSON with exactly the requested keys and only the applied HEX values and font fields requested by the brief.
6. Run public sanity checks:
   - verify the image file exists at the requested path,
   - verify the JSON file exists and its keys exactly match the required schema,
   - inspect image metadata to confirm the render completed and the output is plausibly aligned with the intended format,
   - confirm the overall design remains minimalist and avoids neon, glow, or flashy gradient styling.
7. If a concrete mismatch is found, repair the first failing issue and re-check before finalizing.
8. Finalize only when both artifacts exist, the JSON schema is exact, and the visible brief constraints are satisfied.

# Error Handling & Fallbacks
- If visible files are missing or unclear, rely only on the user-visible prompt and do not infer hidden requirements.
- If a brand token lookup fails, retry with the exact token names from the brief; if still unresolved, stop rather than inventing unofficial values.
- If rendering output is incomplete or visually off-brief, simplify the composition and re-render with fewer elements and clearer token assignment.
- If metadata checks reveal a missing file or malformed output, regenerate that artifact and re-run valid

[truncated]

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested artifact using the visible instruction and local files, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: list_dir, read_file, write_file, python, shell
