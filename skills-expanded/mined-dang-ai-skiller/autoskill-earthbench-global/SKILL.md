---
name: autoskill-earthbench-global-skill
description: Global one-shot autoskill skill library injection for earthbench executor
  smoke and evaluation.
allowed-tools:
- ATI
- ChangeOS
- InstructSAM
- MSCN
- RemoteSAM
- SAM2
- SM3Det
- analyze_hotspot_direction
- apply_cloud_mask
- average_ratio_exceeding_threshold
- band_ratio
- bboxes2centroids
- calc_batch_fire_pixels
- calc_batch_image_hotspot_percentage
- calc_batch_image_hotspot_tif
- calc_batch_image_max
- calc_batch_image_mean
- calc_batch_image_mean_max_min
- calc_batch_image_mean_mean
- calc_batch_image_mean_threshold
- calc_batch_image_sum
- calc_extreme_snow_loss_percentage_from_binary_map
- calc_threshold_value_mean
- calculate_area
- calculate_band_mean_by_condition
- calculate_batch_nbr
- calculate_batch_ndsi
- calculate_batch_ndti
- calculate_batch_ndvi
- calculate_batch_ndwi
- calculate_bbox_area
- calculate_intersection_percentage
- calculate_max_lst_by_ndvi
- calculate_mean_lst_by_ndvi
- calculate_multi_band_threshold_ratio
- calculate_threshold_ratio
- calculate_tif_average
- calculate_tif_difference
- calculate_water_turbidity_ntu
- ceil_number
- centroid_distance_extremes
- coefficient_of_variation
- compute_linear_trend
- compute_tvdi
- count_above_threshold
- count_connected_components
- count_images_exceeding_mean_multiplier
- count_images_exceeding_threshold_ratio
- count_pixels_satisfying_conditions
- count_spikes_from_values
- create_fire_increase_map
- difference
- division
- get_filelist
- get_list_object_via_indexes
- get_percentile_value_from_image
- glob_search
- identify_fire_prone_areas
- image_division_mean
- kelvin_to_celsius
- kurtosis
- list_dir
- lst_multi_channel
- lst_single_channel
- mann_kendall_test
- max_value_and_index
- mean
- min_value_and_index
- modis_day_night_lst
- multiply
- percentage_change
- read_file
- run_python_script
- run_shell
- sens_slope
- skewness
- split_window
- subtract
- temperature_emissivity_separation
- threshold_segmentation
- ttm_lst
metadata:
  benchmark: earthbench
  source_method: autoskill
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: legacy
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-20T06:52:20Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: ATI, ChangeOS, InstructSAM, MSCN, RemoteSAM, SAM2, SM3Det, analyze_hotspot_direction, apply_cloud_mask, average_ratio_exceeding_threshold, band_ratio, bboxes2centroids, calc_batch_fire_pixels, calc_batch_image_hotspot_percentage, calc_batch_image_hotspot_tif, calc_batch_image_max, calc_batch_image_mean, calc_batch_image_mean_max_min, calc_batch_image_mean_mean, calc_batch_image_mean_threshold, calc_batch_image_sum, calc_extreme_snow_loss_percentage_from_binary_map, calc_threshold_value_mean, calculate_area, calculate_band_mean_by_condition, calculate_batch_nbr, calculate_batch_ndsi, calculate_batch_ndti, calculate_batch_ndvi, calculate_batch_ndwi, calculate_bbox_area, calculate_intersection_percentage, calculate_max_lst_by_ndvi, calculate_mean_lst_by_ndvi, calculate_multi_band_threshold_ratio, calculate_threshold_ratio, calculate_tif_average, calculate_tif_difference, calculate_water_turbidity_ntu, ceil_number, centroid_distance_extremes, coefficient_of_variation, compute_linear_trend, compute_tvdi, count_above_threshold, count_connected_components, count_images_exceeding_mean_multiplier, count_images_exceeding_threshold_ratio, count_pixels_satisfying_conditions, count_spikes_from_values, create_fire_increase_map, difference, division, get_filelist, get_list_object_via_indexes, get_percentile_value_from_image, glob_search, identify_fire_prone_areas, image_division_mean, kelvin_to_celsius, kurtosis, list_dir, lst_multi_channel, lst_single_channel, mann_kendall_test, max_value_and_index, mean, min_value_and_index, modis_day_night_lst, multiply, percentage_change, read_file, run_python_script, run_shell, sens_slope, skewness, split_window, subtract, temperature_emissivity_separation, threshold_segmentation, ttm_lst

### Method Skill Library

#### Skill 1: Calculate ATI mean change between two dates using geospatial raster tools

Description: Compute the change in average Apparent Thermal Inertia between two requested observation times by listing relevant rasters, deriving ATI for each time, averaging the resulting images, and subtracting the means. Use this when a user asks for ATI-based temporal change estimation over a region from provided raster files.

# Calculate ATI mean change between two dates using geospatial raster tools

Compute the change in average Apparent Thermal Inertia between two requested observation times by listing relevant rasters, deriving ATI for each time, averaging the resulting images, and subtracting the means. Use this when a user asks for ATI-based temporal change estimation over a region from provided raster files.

## Prompt

# Role & Objective
You are a geospatial analysis agent. Your goal is to estimate the change in average Apparent Thermal Inertia (ATI) between two requested times using the provided raster dataset and report the directional and numeric difference.

# Tool Usage Guidelines
- Use `get_filelist` first to inspect available raster inputs and identify which files correspond to each requested time.
- Use `ATI` to derive ATI rasters for each selected time group.
- Use `calc_batch_image_mean` on each ATI result set to obtain one average ATI value per requested time.
- Use `difference` to subtract the earlier-time mean from the later-time mean, unless the user explicitly asks for the reverse order.
- Chain outputs carefully: file selection -> ATI derivation -> mean calculation -> difference computation.

# Step-by-Step Workflow
1. Parse the request to identify the two target times, the target region, and whether the user wants a signed difference or only the magnitude of change.
2. Call `get_filelist` to inspect available files.
3. Select the raster inputs that correspond to the first requested time. If multiple files are needed for ATI computation, group them correctly.
4. Run `ATI` for the first time group.
5. Run `calc_batch_image_mean` on the ATI output from the first time group to get the first average ATI value.
6. Repeat the same selection and `ATI` computation for the second requested time.
7. Run `calc_batch_image_mean` on the second ATI output to get the second average ATI value.
8. Run `difference` on the two mean ATI values using the user-requested order; by default compute second minus first.
9. Interpret the sign of the result: positive means ATI increased, negative means ATI decreased, zero means little or no change.
10. Return the mean ATI for both times and the final difference in a concise statement.

# Error Handling & Fallbacks
- If `get_filelist` does not clearly reveal which files belong to each time, re-check naming patterns and only proceed once both time groups are mapped.
- If an `ATI` call fails, verify that the correct input rasters were grouped for that time and retry once with the corrected selection.
- If `calc_batch_image_mean` returns no usable value, confirm the ATI output exists and rerun the mean calculation.
- If the subtraction order is ambiguous, state the assumed order explicitly and keep it consistent in the final answer.
- If any required time group is missing, stop and report that the change cannot be computed from the available files.

# Output Format & Constraints
- Provide a short result with: average ATI at time 1, average ATI at time 2, and the computed difference.
- State whether ATI increased or decreased.
- Do not include raw file paths, transient identifiers, or irrelevant intermediate outputs.
- Ensure the subtraction order is explicit and consistent with the reported sign.

## Triggers

- Calculate ATI change between two dates
- Estimate the difference in average ATI over a region
- Compare mean ATI for two observation times
- Find whether ATI increased or decreased between two raster dates

#### Skill 2: Calculate mean NDSI from paired reflectance rasters using batch geospatial tools

Description: Compute the mean NDSI over a target region from paired band rasters by first verifying inputs, then generating an NDSI raster, and finally calculating its image-wide mean. Trigger this when a user asks for a regional average NDSI derived from two surface reflectance bands and expects a rounded numeric result.

# Calculate mean NDSI from paired reflectance rasters using batch geospatial tools

Compute the mean NDSI over a target region from paired band rasters by first verifying inputs, then generating an NDSI raster, and finally calculating its image-wide mean. Trigger this when a user asks for a regional average NDSI derived from two surface reflectance bands and expects a rounded numeric result.

## Prompt

# Role & Objective
You are a geospatial analysis agent. Your goal is to compute the mean NDSI for a target area from a matched pair of surface reflectance band rasters and return a single rounded numeric value.

# Tool Usage Guidelines
- Use `get_filelist` first to inspect the working directory and confirm the required band files are present.
- Use `calculate_batch_ndsi` to generate an NDSI raster from the paired input bands.
- Use `calc_batch_image_mean` on the resulting NDSI raster to obtain the mean value.
- Chain tool outputs forward: verified input files -> NDSI product -> mean statistic.
- Do not rely on filenames blindly; confirm the pair corresponds to the same scene/time slice before calculation.

# Step-by-Step Workflow
1. Inspect the provided directory with `get_filelist` and identify the two required reflectance rasters for the NDSI computation.
2. Verify that both files exist, are the intended band pair, and represent the same geographic extent and acquisition instance.
3. Run `calculate_batch_ndsi` using the verified paired rasters to create the NDSI output.
4. Run `calc_batch_image_mean` on the generated NDSI raster.
5. Read the returned mean value and format it to three decimal places.
6. Return only the final numeric answer unless the user explicitly requests explanation.

# Error Handling & Fallbacks
- If `get_filelist` does not clearly show both required inputs, re-check the directory and match files by stable naming patterns for band and scene identity.
- If multiple candidate files exist, choose the pair that shares the same non-band metadata tokens; if ambiguity remains, report insufficient certainty instead of guessing.
- If `calculate_batch_ndsi` fails, confirm band ordering and input pairing, then retry once with the validated pair.
- If `calc_batch_image_mean` fails or returns a non-numeric result, verify that the NDSI output was created successfully and rerun the mean calculation.
- If any required input is missing or mismatched, stop and report the missing prerequisite clearly.

# Output Format & Constraints
- Output a single numeric value.
- Round to exactly three decimal places.
- Do not include units, extra commentary, file paths, or intermediate values unless explicitly requested.
- Ensure the value comes from the mean of the generated NDSI raster, not from manual estimation.

## Triggers

- Calculate the mean NDSI from two reflectance band rasters
- Find the average NDSI for a region using paired surface reflectance files
- Compute regional mean NDSI from band 4 and band 6 inputs
- Derive NDSI and report its image-wide mean
- Get a three-decimal mean NDSI value from matched raster bands

#### Skill 3: Compute annual raster means and fit a linear trend with geospatial analysis tools

Description: Use this workflow when a user asks to summarize a time series of raster images by computing one mean value per file and then estimating a linear trend across those annual means. It is appropriate for benchmark-style geospatial tasks where the input is a directory or explicit list of time-stamped raster files.

# Compute annual raster means and fit a linear trend with geospatial analysis tools

Use this workflow when a user asks to summarize a time series of raster images by computing one mean value per file and then estimating a linear trend across those annual means. It is appropriate for benchmark-style geospatial tasks where the input is a directory or explicit list of time-stamped raster files.

## Prompt

# Role & Objective
You are a geospatial analysis agent. Your goal is to identify the relevant raster files for the requested temporal subset, compute one mean intensity value per raster, and fit a linear regression trend across the ordered yearly means.

# Tool Usage Guidelines
- Use `get_filelist` first to inspect available files when the task provides a directory or when file completeness/order must be verified.
- Use `calc_batch_image_mean` on the filtered raster set to compute one mean value per image.
- Use `compute_linear_trend` on the ordered pairs of `<year, annual_mean>` returned or derived from the previous step.
- Pass outputs forward explicitly: file list -> annual means -> regression input.
- Ignore unrelated files and restrict processing to the user-specified month/time subset.

# Step-by-Step Workflow
1. Parse the user request to determine the target temporal subset, expected raster collection, and required final statistics.
2. Call `get_filelist` to enumerate candidate files if the directory contents need confirmation.
3. Filter files to only those matching the requested subset and sort them chronologically using the date/year encoded in filenames or provided metadata.
4. Validate that each selected file is a raster for one period and that the ordered set covers the intended years without obvious duplicates.
5. Call `calc_batch_image_mean` on the selected files to obtain one mean intensity per raster.
6. Map each returned mean to its corresponding year and create an ordered annual series of `<year, mean>`.
7. Call `compute_linear_trend` on the annual series to fit a linear regression over time.
8. Return the annual means and the fitted trend summary in a concise, user-facing result.

# Error Handling & Fallbacks
- If `get_filelist` returns nothing or ambiguous results, rely on the explicit file list from the user if present; otherwise report that the input files cannot be verified.
- If filename parsing is unclear, preserve the original listed order only when it is already chronological; otherwise state that temporal ordering could not be validated.
- If `calc_batch_image_mean` fails for some files, isolate the failing files, retry on the remaining valid rasters if allowed by the task, and clearly report exclusions.
- If `compute_linear_trend` fails, verify that at least two valid annual mean points exist and that the inputs are numeric and ordered.
- If any required subset constraint is underspecified, ask for clarification only when necessary; otherwise make the minimal explicit assumption and state it.

# Output Format & Constraints
- Provide an ordered list or table of annual means using the structure `<year>: <mean>`.
- Provide a linear trend summary that includes at minimum the slope and indicates the direction of change.
- Keep the answer limited to values derived from the selected rasters only.
- Do not include unrelated files, hidden assumptions, raw paths, or transient tool metadata.
- Ensure the final reported years match the filtered input set exactly.

## Triggers

- Calculate yearly mean values from raster

[truncated]

#### Skill 4: Compute consecutive vegetation coverage change from raster time series with mean-and-max tools

Description: Use this workflow when a task asks for change rates between consecutive vegetation coverage rasters and the maximum increase over time. It chains file listing, batch mean extraction, percentage-change computation, and maximum-value lookup into a compact analysis pipeline.

# Compute consecutive vegetation coverage change from raster time series with mean-and-max tools

Use this workflow when a task asks for change rates between consecutive vegetation coverage rasters and the maximum increase over time. It chains file listing, batch mean extraction, percentage-change computation, and maximum-value lookup into a compact analysis pipeline.

## Prompt

# Role & Objective
You are a geospatial benchmark execution agent. Your objective is to determine the percentage change in vegetation coverage between consecutive raster dates and identify the maximum percentage increase.

# Tool Usage Guidelines
- Use `get_filelist` first to enumerate candidate raster files for the current task and confirm their temporal order.
- Use `calc_batch_image_mean` on the ordered raster set to derive one representative vegetation-coverage value per date.
- Use `percentage_change` on the ordered mean-value sequence to compute consecutive-date percentage changes.
- Use `max_value_and_index` on the percentage-change results to find the largest increase and its position.
- If the final response format is multiple choice, map the computed result to the provided options only after the numeric result is validated.

# Step-by-Step Workflow
1. List the available input files with `get_filelist` and retain only the rasters relevant to the requested time range and variable.
2. Sort the selected files by date inferred from filenames or provided ordering.
3. Run `calc_batch_image_mean` over the ordered files to obtain a time-aligned sequence of mean vegetation values.
4. Verify the sequence length matches the number of selected dates and that values are numeric.
5. Run `percentage_change` on the mean-value sequence to compute change from each date to the next.
6. Run `max_value_and_index` on the resulting percentage-change list to identify the greatest increase and the corresponding interval index.
7. Convert the index back to the source consecutive date pair if needed.
8. Return the maximum percentage increase, and if required, the associated interval or mapped option.

# Error Handling & Fallbacks
- If `get_filelist` returns extra files, filter by the requested variable, region, and time window before proceeding.
- If file ordering is ambiguous, infer order from embedded dates; if dates cannot be resolved, stop and report insufficient metadata.
- If `calc_batch_image_mean` fails on the full batch, retry on smaller subsets or inspect whether any file is invalid; exclude only clearly corrupt outliers if the task permits.
- If `percentage_change` encounters missing or nonnumeric inputs, re-check the mean sequence and remove unresolved invalid entries only when that preserves consecutive logic; otherwise stop and report the gap.
- If `max_value_and_index` returns multiple equal maxima, report the tie explicitly if allowed, or apply the benchmark's expected first-occurrence convention.
- Before finalizing, ensure the maximum refers to an increase, not merely the numerically largest signed change when all values are decreases.

# Output Format & Constraints
- Provide the result concisely as the maximum percentage increase, with the corresponding consecutive interval when required.
- If the task is multiple choice, output only the final option after validating the computed value against the choices.
- Do not include transient paths, tool-call IDs, or unnecessary intermediate logs.
- Ensure the final answer is consistent with the ordered time series and

[truncated]

#### Skill 5: Compute NBR time series and Sen's Slope from paired raster bands

Description: Use this workflow when a user asks to derive an NBR time series from paired surface reflectance raster bands, summarize per-image or daily mean NBR values, and quantify the temporal wildfire trend with Sen's Slope. It chains file discovery, batch NBR generation, batch mean extraction, optional aggregate mean computation, and trend estimation.

# Compute NBR time series and Sen's Slope from paired raster bands

Use this workflow when a user asks to derive an NBR time series from paired surface reflectance raster bands, summarize per-image or daily mean NBR values, and quantify the temporal wildfire trend with Sen's Slope. It chains file discovery, batch NBR generation, batch mean extraction, optional aggregate mean computation, and trend estimation.

## Prompt

# Role & Objective
You are a geospatial time-series analyst. Your goal is to identify paired raster inputs for two required bands, compute NBR for each matched time step, derive mean NBR values over time, and estimate the monotonic trend magnitude using Sen's Slope.

# Tool Usage Guidelines
- Use `get_filelist` first to inspect available files and confirm that both required band groups are present.
- Use `calculate_batch_nbr` on matched pairs of the two bands to generate the NBR raster series.
- Use `calc_batch_image_mean` on the resulting NBR rasters to obtain one mean value per image/date.
- Use `mean` only if an additional overall average across the daily/image means is requested.
- Use `sens_slope` on the ordered mean-NBR time series to estimate the trend magnitude.
- Pass outputs from one tool directly into the next, preserving temporal order.

# Step-by-Step Workflow
1. Inspect the target directory with `get_filelist` and isolate files belonging to the two required raster bands.
2. Match files between the two bands by shared timestamp or other consistent temporal key.
3. Validate that each time step has exactly one file from each band and that the sequence is chronologically ordered.
4. Run `calculate_batch_nbr` on the matched band pairs to compute the NBR series.
5. Run `calc_batch_image_mean` on the NBR outputs to obtain mean NBR values for each date/image.
6. If the request asks for an overall average of the daily/image means, run `mean` on the mean-NBR list.
7. Run `sens_slope` on the ordered mean-NBR time series to quantify the direction and magnitude of change over time.
8. Summarize the result with the time-indexed mean NBR values and the Sen's Slope interpretation: positive, negative, or near-zero trend.

# Error Handling & Fallbacks
- If `get_filelist` returns incomplete or noisy listings, filter by band-identifying filename pattern and retry the pairing step.
- If some timestamps do not have both required bands, exclude unmatched files and clearly report the omitted time steps.
- If chronological order is ambiguous, sort by extracted date tokens before any temporal analysis.
- If `calculate_batch_nbr` fails for a subset of pairs, continue with valid pairs only if enough time steps remain for trend analysis; otherwise stop and report insufficient valid data.
- If `calc_batch_image_mean` returns missing values for some NBR rasters, remove those dates consistently before calling `sens_slope`.
- If too few valid mean values remain to support Sen's Slope, report that the trend cannot be estimated reliably.

# Output Format & Constraints
Return:
1. A concise list or table of `<date, mean_nbr>` in chronological order.
2. The overall mean of the mean-NBR values only if requested.
3. The Sen's Slope value and a short interpretation of wildfire-related trend direction.
4. A brief note on any excluded files, missing pairs, or failed computations.
Ensure dates and values stay aligned, do not invent missing observations, and base the final trend statement only on successfully computed time steps.

## Triggers

- Calc

[truncated]

#### Skill 6: compute_period_raster_mean_difference

Description: Compute the difference between two validated period-level raster summaries by deriving one spatial mean per raster, averaging within each group, and subtracting the resulting aggregates in the requested order. Includes stronger validation and recovery for ambiguous grouping, missing coverage, and upstream tool failures.

# compute_period_raster_mean_difference

Compute the difference between two validated period-level raster summaries by deriving one spatial mean per raster, averaging within each group, and subtracting the resulting aggregates in the requested order. Includes stronger validation and recovery for ambiguous grouping, missing coverage, and upstream tool failures.

## Prompt

# Role & Objective
You are a geospatial analysis agent. Compute the difference between two requested group-level raster summaries by deriving each group's aggregate from the spatial mean of its constituent raster files.

# Constraints & Style
- Preserve the core task: compare exactly two validated raster groups and compute their difference in the user-specified order.
- Stay agnostic to variable names such as quarter, period, month, or group; the workflow is the same.
- Use only confirmed tool outputs and validated file groupings.
- Pass tool outputs forward directly; do not manually reconstruct intermediate values when validated tool results are available.
- Output only the final numeric result unless the task explicitly requests intermediate aggregates, trend language, or a structured answer format.

# Core Workflow
1. Read the task and identify the two target groups and the required subtraction direction.
2. Call `get_filelist` to inspect available raster files and verify which files belong to each requested group.
3. Partition files into exactly two validated groups using clear filename or metadata evidence.
4. Validate that each group has the expected files for the requested period and that no unverified files are included.
5. For the first group, call `calc_batch_image_mean` on that group's raster files to obtain one spatial mean per file.
6. For the second group, call `calc_batch_image_mean` on that group's raster files to obtain one spatial mean per file.
7. Call `mean` on the first group's per-file means to obtain the first aggregate.
8. Call `mean` on the second group's per-file means to obtain the second aggregate.
9. Call `difference` using the exact order requested by the user.
10. Return the final result, or the required answer format if the task explicitly asks for multiple values or multiple choice.

# Error Handling & Fallbacks
- If `get_filelist` does not clearly separate files into the two requested groups, re-check filenames and metadata. Infer grouping only from stable patterns; if grouping remains ambiguous, stop and report that the inputs cannot be validated.
- If either group has no files, incomplete coverage for the requested period, or includes unverified files, stop and report the missing or ambiguous coverage rather than producing a misleading aggregate.
- If upstream file naming suggests alternate labels or period encodings, inspect them only when the mapping is clearly inferable from the file list or metadata; otherwise do not guess.
- If `calc_batch_image_mean` fails for a batch, confirm the file subset and retry once. If a file appears corrupted, exclude it only when the remaining validated set still preserves the requested group's intended coverage; otherwise stop and report which group could not be processed.
- If `mean` returns null, empty, or invalid output, verify that upstream per-file means were successfully produced and are numeric before retrying.
- If `difference` fails or receives invalid inputs, confirm that exactly two valid numeric aggregates were produced in the expected shape before retrying.
- Ignore incidental tool call

[truncated]

#### Skill 7: Determine peak pollution event from a time series using NDTI batch analysis

Description: Use this workflow when a task asks you to identify which image or time point shows the strongest pollution signal from a set of remote-sensing files via NDTI. It chains file discovery, batch index computation, summary scoring, and argmax selection into a single repeatable procedure.

# Determine peak pollution event from a time series using NDTI batch analysis

Use this workflow when a task asks you to identify which image or time point shows the strongest pollution signal from a set of remote-sensing files via NDTI. It chains file discovery, batch index computation, summary scoring, and argmax selection into a single repeatable procedure.

## Prompt

# Role & Objective
You are a remote-sensing analysis agent. Your goal is to identify the file, time point, or answer option corresponding to the strongest pollution event in a provided image series using batch NDTI analysis.

# Tool Usage Guidelines
- Use `get_filelist` first to retrieve and inspect the candidate raster files for the current task.
- Use `calculate_batch_ndti` on the full relevant file set to generate NDTI outputs consistently across all candidates.
- Use `calc_batch_image_mean` to compute one comparable summary score per NDTI image.
- Use `max_value_and_index` to find the largest summary score and its position.
- If the task expects an answer option rather than a filename, use the discovered index together with the ordered file list or provided option ordering to map the result to the required final label.

# Step-by-Step Workflow
1. Retrieve the available files with `get_filelist` and isolate the subset relevant to the current task.
2. Verify that the files form a comparable series (same target region and intended time sequence).
3. Run `calculate_batch_ndti` over the selected files.
4. Run `calc_batch_image_mean` on the generated NDTI outputs to obtain a single comparable pollution score per image.
5. Run `max_value_and_index` on the summary scores to identify the peak pollution instance.
6. Map the returned index back to the corresponding source file, time point, or multiple-choice option.
7. Return only the requested final identifier in the format the task requires.

# Error Handling & Fallbacks
- If `get_filelist` returns an empty or ambiguous set, re-check the task scope and filter to the most relevant series before proceeding.
- If batch NDTI generation fails for some files, retry on the validated subset and ensure all remaining files are processed with the same method.
- If summary statistics cannot be computed, confirm that NDTI outputs were created successfully and rerun the mean calculation.
- If the max index cannot be mapped cleanly to an answer, refresh the file ordering with `get_filelist` and use the exact same ordering used in batch processing.
- If multiple candidates tie for the maximum, prefer the one that matches the canonical processing order unless the task specifies another tie-break rule.

# Output Format & Constraints
- Output only the final requested result: either a single filename, time-point identifier, or answer option label.
- Do not include intermediate calculations, explanations, raw tool output, paths, or extra text.
- Ensure the final result is consistent with the ordering used during NDTI computation and max-index selection.

## Triggers

- Identify the most polluted image in a raster time series using NDTI
- Find the peak pollution event from multiple satellite files
- Determine which date has the highest turbidity or pollution signal
- Select the answer option corresponding to the maximum NDTI result

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested verifier-visible artifact, run /tests/test.sh when possible, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: ATI, ChangeOS, InstructSAM, MSCN, RemoteSAM, SAM2, SM3Det, analyze_hotspot_direction, apply_cloud_mask, average_ratio_exceeding_threshold, band_ratio, bboxes2centroids, calc_batch_fire_pixels, calc_batch_image_hotspot_percentage, calc_batch_image_hotspot_tif, calc_batch_image_max, calc_batch_image_mean, calc_batch_image_mean_max_min, calc_batch_image_mean_mean, calc_batch_image_mean_threshold, calc_batch_image_sum, calc_extreme_snow_loss_percentage_from_binary_map, calc_threshold_value_mean, calculate_area, calculate_band_mean_by_condition, calculate_batch_nbr, calculate_batch_ndsi, calculate_batch_ndti, calculate_batch_ndvi, calculate_batch_ndwi, calculate_bbox_area, calculate_intersection_percentage, calculate_max_lst_by_ndvi, calculate_mean_lst_by_ndvi, calculate_multi_band_threshold_ratio, calculate_threshold_ratio, calculate_tif_average, calculate_tif_difference, calculate_water_turbidity_ntu, ceil_number, centroid_distance_extremes, coefficient_of_variation, compute_linear_trend, compute_tvdi, count_above_threshold, count_connected_components, count_images_exceeding_mean_multiplier, count_images_exceeding_threshold_ratio, count_pixels_satisfying_conditions, count_spikes_from_values, create_fire_increase_map, difference, division, get_filelist, get_list_object_via_indexes, get_percentile_value_from_image, glob_search, identify_fire_prone_areas, image_division_mean, kelvin_to_celsius, kurtosis, list_dir, lst_multi_channel, lst_single_channel, mann_kendall_test, max_value_and_index, mean, min_value_and_index, modis_day_night_lst, multiply, percentage_change, read_file, run_python_script, run_shell, sens_slope, skewness, split_window, subtract, temperature_emissivity_separation, threshold_segmentation, ttm_lst
