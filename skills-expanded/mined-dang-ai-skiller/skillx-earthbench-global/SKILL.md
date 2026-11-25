---
name: skillx-earthbench-global-skill
description: Global one-shot skillx skill library injection for earthbench executor
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
  source_method: skillx
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-20T09:27:04Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: ATI, ChangeOS, InstructSAM, MSCN, RemoteSAM, SAM2, SM3Det, analyze_hotspot_direction, apply_cloud_mask, average_ratio_exceeding_threshold, band_ratio, bboxes2centroids, calc_batch_fire_pixels, calc_batch_image_hotspot_percentage, calc_batch_image_hotspot_tif, calc_batch_image_max, calc_batch_image_mean, calc_batch_image_mean_max_min, calc_batch_image_mean_mean, calc_batch_image_mean_threshold, calc_batch_image_sum, calc_extreme_snow_loss_percentage_from_binary_map, calc_threshold_value_mean, calculate_area, calculate_band_mean_by_condition, calculate_batch_nbr, calculate_batch_ndsi, calculate_batch_ndti, calculate_batch_ndvi, calculate_batch_ndwi, calculate_bbox_area, calculate_intersection_percentage, calculate_max_lst_by_ndvi, calculate_mean_lst_by_ndvi, calculate_multi_band_threshold_ratio, calculate_threshold_ratio, calculate_tif_average, calculate_tif_difference, calculate_water_turbidity_ntu, ceil_number, centroid_distance_extremes, coefficient_of_variation, compute_linear_trend, compute_tvdi, count_above_threshold, count_connected_components, count_images_exceeding_mean_multiplier, count_images_exceeding_threshold_ratio, count_pixels_satisfying_conditions, count_spikes_from_values, create_fire_increase_map, difference, division, get_filelist, get_list_object_via_indexes, get_percentile_value_from_image, glob_search, identify_fire_prone_areas, image_division_mean, kelvin_to_celsius, kurtosis, list_dir, lst_multi_channel, lst_single_channel, mann_kendall_test, max_value_and_index, mean, min_value_and_index, modis_day_night_lst, multiply, percentage_change, read_file, run_python_script, run_shell, sens_slope, skewness, split_window, subtract, temperature_emissivity_separation, threshold_segmentation, ttm_lst

### Method Skill Library

#### Skill 1: pair_multiband_rasters_by_acquisition_date

Description: Use this skill when a remote-sensing index requires multiple raster bands captured at the same time. It lists available files, extracts the acquisition date and band identity from each filename, groups files by date, and keeps only dates where all required bands are present before downstream computation. Parameters: file_listing (list[str]), required_bands (list[str]), date_pattern (str or parser rule). Outputs: paired_band_files (list[object]) where each object contains a date and one file per required band; incomplete_dates (list[str]) for dates missing any required input. Caveat: verify that filenames encode dates and band labels consistently before pairing.

1. Retrieve the candidate raster filenames for the current task.
2. For each filename, parse two fields: the acquisition date and the spectral band identifier.
3. Build a date-keyed mapping that stores the file path for each required band.
4. For every date, check whether all required bands are present.
5. Keep only complete date groups as valid inputs for index computation.
6. Record any incomplete date groups separately so missing inputs do not silently contaminate the time series.
7. Return the ordered list of complete date-band pairs, sorted by acquisition date.

#### Skill 2: compute_dryness_indicator_from_paired_rasters

Description: Derive a per-date dryness indicator raster from paired vegetation-index and surface-temperature rasters so later averaging and trend analysis operate on one consistent metric. Trigger this after date-matched input pairs have been assembled and before any temporal aggregation. Validate that each pair is spatially compatible, ignore invalid or nodata pixels, and keep the derived raster aligned with the original grid for downstream statistics. Parameters: paired_inputs: list[object] with date, vegetation_raster, temperature_raster; method: str for the dryness-indicator variant expected by the workflow; nodata_policy: str; output_dir: str. Outputs: derived_rasters: list[object] with date and output_raster; warnings: list[str] for skipped dates or data-quality issues.

1. Take the chronologically ordered paired rasters for the current task.
2. For each date pair, verify that the two rasters can be compared pixelwise.
   - Confirm they refer to the same observation date.
   - Check grid shape, projection, extent, and resolution; if needed, apply the workflow's standard alignment rule before computing the indicator.
3. Build a valid-data mask that excludes nodata, missing, or physically invalid pixels from either raster.
4. Run the dryness-indicator computation tool on the masked vegetation and temperature inputs using the method required by the current workflow.
5. Preserve the source raster georeferencing and write one derived raster per date.
6. If a date cannot be computed because of missing inputs, incompatible grids, or too few valid pixels, skip it and record a warning for downstream interpretation.
7. Return the list of derived rasters in date order so later steps can summarize them consistently across time.

#### Skill 3: aggregate_dryness_rasters_to_annual_region_means

Description: Summarize per-date dryness rasters into annual mean dryness values for a target region before fitting a temporal trend. Trigger this after the dryness indicator has been computed for each acquisition date and when the task asks for year-level change rather than single-scene values. Use a consistent spatial footprint and nodata policy across all dates, and track data coverage so sparse years are interpreted cautiously. Parameters: dryness_rasters: list[object] with date and raster path; region_mask: raster|geometry|None; nodata_policy: str; annual_aggregation: str. Outputs: annual_means: list[object] with year, mean_dryness, observation_count; warnings: list[str] for skipped rasters, missing years, or low-coverage years.

1. Start from the derived dryness rasters for the current task, each tagged with its acquisition date.
2. Group the rasters by calendar year using the date associated with each file.
3. For each raster in a given year, compute the regional mean dryness with the averaging tool.
   - Apply the same target region or mask each time if the workflow uses one.
   - Exclude nodata or invalid pixels consistently across all dates.
4. Collect the per-date mean dryness values for that year and check data coverage.
   - If a raster cannot be averaged, skip it and record a warning.
   - If a year has too few valid observations for reliable interpretation, keep that fact in the output metadata or warnings.
5. Aggregate the valid per-date means within each year using the workflow's annual rule, typically the arithmetic mean.
6. Return the annual series in chronological order with each year's mean dryness and the number of contributing observations.
7. Pass this annual series to the downstream trend-fitting step, along with any warnings about gaps or uneven coverage.

#### Skill 4: fit_linear_trend_from_annual_dryness_series

Description: Fit a linear trend to yearly regional dryness values to estimate the overall rate and direction of change across time. Trigger this after annual mean dryness has already been computed and the task asks for a trend slope plus a short qualitative description. Ensure the annual series is chronological, handle missing or invalid years before fitting, and report both the fitted slope and an interpretation of whether dryness is increasing, decreasing, or broadly stable. Parameters: annual_means: list[object] with year and mean_dryness; regression_method: str; stability_rule: str for interpreting near-flat slopes. Outputs: trend_result: object with slope, trend_direction, and brief annual trend description; warnings: list[str] for missing years, insufficient coverage, or unreliable fit.

1. Start from the annual dryness series produced for the current task.
2. Remove years with missing, invalid, or non-comparable annual mean values, and record any gaps.
3. Sort the remaining yearly observations in chronological order.
4. Convert each year into a consistent time variable for regression so the fitted slope is interpretable on a per-year basis.
5. Fit a linear regression of annual mean dryness against time using the workflow's standard method.
6. Extract the slope from the fitted line as the overall dryness trend rate.
7. Interpret the slope sign and magnitude using the workflow's stability rule:
   - positive slope: dryness is increasing over time
   - negative slope: dryness is decreasing over time
   - near-flat slope: dryness is broadly stable over time
8. Summarize the result in plain language, combining the numeric slope with the annual trend direction.
9. If the annual series is too sparse or uneven for a reliable fit, return the slope with a warning and state that the trend description should be treated cautiously.

#### Skill 5: pair_time_ordered_rasters_by_date_and_modality

Description: Build date-aligned input pairs from a directory of raster files when a downstream index requires one file from each modality per observation date. Trigger this before any multi-source environmental index calculation. Match files by parsed observation date and modality label, then sort chronologically and flag missing or duplicate inputs instead of guessing. Parameters: file_inventory: list[str], required_modalities: list[str], date_parser: callable|pattern. Outputs: paired_observations: list[{date: str, files: dict[str, str]}], validation_report: dict.

1. List all candidate raster files for the current task.
2. For each file, parse two fields from its name or metadata: the observation date and the modality label.
3. Keep only files whose modality is in `<required_modalities>`.
4. Group the remaining files by observation date.
5. For each date group, verify that exactly one file exists for each required modality.
6. If a modality is missing or duplicated for a date, record it in a validation report and exclude that date from downstream computation unless the task explicitly allows partial data.
7. Build a structured record for each valid date: `{date, files_by_modality}`.
8. Sort the valid records by date in ascending order.
9. Return both the ordered pairs and the validation report so later steps can compute the index only on complete observations.

#### Skill 6: compute_drought_index_from_paired_rasters

Description: Compute a comparable drought index for each observation date from chronologically matched vegetation and surface-temperature rasters. Trigger this after building complete per-date modality pairs and before any temporal aggregation or spike detection. Ensure each pair is spatially compatible, preserve date ordering, and propagate nodata masks so invalid pixels do not distort the index. Parameters: paired_observations: list[{date: str, files: dict[str, str]}], vegetation_key: str, temperature_key: str. Outputs: drought_index_rasters: list[{date: str, file: str}], computation_report: dict.

1. Take the validated per-date raster pairs produced by the pairing step.
2. For each observation, load the vegetation raster and the temperature raster using the modality keys for the current task.
3. Check that the two rasters are spatially compatible for pixelwise computation; if they are not, align them using the task's standard reprojection or resampling rule before continuing.
4. Build a shared validity mask so pixels marked invalid in either input remain invalid in the output.
5. Apply the drought-index computation method implemented by the available tool to convert the paired indicators into a single drought raster for that date.
6. Save the resulting raster with its observation date attached, and record any alignment, masking, or tool-level warnings in a computation report.
7. Preserve chronological order across all outputs so later steps can aggregate or compare dates without re-sorting.
8. Return both the dated drought-index rasters and the computation report; if a date cannot be processed reliably, flag it explicitly instead of fabricating an output.

#### Skill 7: summarize_dated_index_rasters_to_regional_time_series

Description: Convert a chronologically ordered set of per-date index rasters into a 1D regional time series for later temporal analysis. Trigger this after the index rasters have already been computed and validated. Apply one consistent spatial reducer across all dates, exclude invalid pixels, and preserve date alignment so later steps can detect peaks or trends reliably. Parameters: dated_rasters: list[{date: str, file: str}], reducer: str='mean', nodata_policy: str. Outputs: time_series: list[{date: str, value: float}], summary_report: dict.

1. Take the per-date index rasters in chronological order.
2. Choose a single regional reducer for the whole sequence, typically `<reducer>` such as spatial mean.
3. For each raster, apply the reducer only over valid pixels according to `<nodata_policy>` so missing areas do not bias the result.
4. Record one scalar value for each date as `{date, value}`.
5. If a raster has too few valid pixels or the reducer fails, flag that date in the summary report instead of inventing a value.
6. Preserve the original date ordering in the output sequence.
7. Return the full time series together with any warnings about missing data, invalid rasters, or inconsistent coverage that could affect downstream spike detection.

#### Skill 8: detect_spikes_in_ordered_index_time_series

Description: Identify severe-event candidates by scanning a chronological index time series for sharp local peaks or increases. Trigger this after spatial aggregation has reduced each dated raster to one ordered scalar value. Validate date order and missing values before detection, use a consistent spike criterion across the full series, and report ambiguous boundary cases separately if the first or last observation cannot be judged as a full local peak. Parameters: time_series: list[{date: str, value: float}], spike_rule: str|dict, missing_value_policy: str. Outputs: spike_count: int, spike_events: list[{date: str, value: float, reason: str}], detection_report: dict.

1. Take the index values as a chronological sequence of `{date, value}` records.
2. Verify the sequence is sorted by date and remove or flag records with invalid or missing values according to `<missing_value_policy>`.
3. Apply one explicit spike definition across the entire sequence, such as a local peak, an abrupt rise relative to neighboring dates, or the tool's built-in event rule from `<spike_rule>`.
4. Evaluate each candidate point against its temporal neighbors so ordinary fluctuations are not counted as severe-event spikes.
5. Treat boundary observations carefully: if a point lacks enough neighbors to satisfy the chosen rule, mark it as ambiguous unless the task explicitly allows endpoint spikes.
6. Count only the observations that meet the spike criterion.
7. Return both the total `spike_count` and a dated list of detected spike events, plus any warnings about gaps, ties, or borderline cases that could affect interpretation.

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested verifier-visible artifact, run /tests/test.sh when possible, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: ATI, ChangeOS, InstructSAM, MSCN, RemoteSAM, SAM2, SM3Det, analyze_hotspot_direction, apply_cloud_mask, average_ratio_exceeding_threshold, band_ratio, bboxes2centroids, calc_batch_fire_pixels, calc_batch_image_hotspot_percentage, calc_batch_image_hotspot_tif, calc_batch_image_max, calc_batch_image_mean, calc_batch_image_mean_max_min, calc_batch_image_mean_mean, calc_batch_image_mean_threshold, calc_batch_image_sum, calc_extreme_snow_loss_percentage_from_binary_map, calc_threshold_value_mean, calculate_area, calculate_band_mean_by_condition, calculate_batch_nbr, calculate_batch_ndsi, calculate_batch_ndti, calculate_batch_ndvi, calculate_batch_ndwi, calculate_bbox_area, calculate_intersection_percentage, calculate_max_lst_by_ndvi, calculate_mean_lst_by_ndvi, calculate_multi_band_threshold_ratio, calculate_threshold_ratio, calculate_tif_average, calculate_tif_difference, calculate_water_turbidity_ntu, ceil_number, centroid_distance_extremes, coefficient_of_variation, compute_linear_trend, compute_tvdi, count_above_threshold, count_connected_components, count_images_exceeding_mean_multiplier, count_images_exceeding_threshold_ratio, count_pixels_satisfying_conditions, count_spikes_from_values, create_fire_increase_map, difference, division, get_filelist, get_list_object_via_indexes, get_percentile_value_from_image, glob_search, identify_fire_prone_areas, image_division_mean, kelvin_to_celsius, kurtosis, list_dir, lst_multi_channel, lst_single_channel, mann_kendall_test, max_value_and_index, mean, min_value_and_index, modis_day_night_lst, multiply, percentage_change, read_file, run_python_script, run_shell, sens_slope, skewness, split_window, subtract, temperature_emissivity_separation, threshold_segmentation, ttm_lst
