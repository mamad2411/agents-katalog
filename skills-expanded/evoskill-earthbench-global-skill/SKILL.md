---
name: evoskill-earthbench-global-skill
description: Global one-shot evoskill skill library injection for earthbench executor
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
  source_method: evoskill
  source_dir: <SOURCE_DIR>
  disclosure: global_input
  artifact_fallback_mode: strict
  provenance: extracted_skill_artifacts
  no_instance_memory_guidance: light_generation_prompt_only
  generated_at: '2026-05-20T07:00:51Z'
---

## Method Skill Context

Instance-memory boundary: distill only reusable procedures. Do not write concrete task IDs, sample IDs, training filenames or paths, final answers, option mappings, URLs, named entities, dates, numeric constants, or verbatim question text from the source trajectory into any generated SKILL.md. Use placeholders such as <current task>, <current file>, <current option>, and <current value> when a rule needs a slot.

Use this skill as ordinary prompt context. Apply the relevant method skill below before choosing tools.
Read the actual task prompt, choices, local files, and prior tool observations. Keep concrete values tied to the current task.
You may call tools while evidence is missing. When the answer is ready, output it directly in the benchmark answer format.

Allowed tools: ATI, ChangeOS, InstructSAM, MSCN, RemoteSAM, SAM2, SM3Det, analyze_hotspot_direction, apply_cloud_mask, average_ratio_exceeding_threshold, band_ratio, bboxes2centroids, calc_batch_fire_pixels, calc_batch_image_hotspot_percentage, calc_batch_image_hotspot_tif, calc_batch_image_max, calc_batch_image_mean, calc_batch_image_mean_max_min, calc_batch_image_mean_mean, calc_batch_image_mean_threshold, calc_batch_image_sum, calc_extreme_snow_loss_percentage_from_binary_map, calc_threshold_value_mean, calculate_area, calculate_band_mean_by_condition, calculate_batch_nbr, calculate_batch_ndsi, calculate_batch_ndti, calculate_batch_ndvi, calculate_batch_ndwi, calculate_bbox_area, calculate_intersection_percentage, calculate_max_lst_by_ndvi, calculate_mean_lst_by_ndvi, calculate_multi_band_threshold_ratio, calculate_threshold_ratio, calculate_tif_average, calculate_tif_difference, calculate_water_turbidity_ntu, ceil_number, centroid_distance_extremes, coefficient_of_variation, compute_linear_trend, compute_tvdi, count_above_threshold, count_connected_components, count_images_exceeding_mean_multiplier, count_images_exceeding_threshold_ratio, count_pixels_satisfying_conditions, count_spikes_from_values, create_fire_increase_map, difference, division, get_filelist, get_list_object_via_indexes, get_percentile_value_from_image, glob_search, identify_fire_prone_areas, image_division_mean, kelvin_to_celsius, kurtosis, list_dir, lst_multi_channel, lst_single_channel, mann_kendall_test, max_value_and_index, mean, min_value_and_index, modis_day_night_lst, multiply, percentage_change, read_file, run_python_script, run_shell, sens_slope, skewness, split_window, subtract, temperature_emissivity_separation, threshold_segmentation, ttm_lst

### Method Skill Library

#### Skill 1: aggregate-batch-raster-stats-by-period

Description: Use this skill when a task asks you to compute a per-raster spatial statistic across many raster files, aggregate those values within named periods, and then compare the period-level results.

## When to use
- You have multiple raster files grouped into periods such as quarters, seasons, or other named windows.
- The task asks for a spatial summary per raster first, then a period-level aggregation across files.
- The final output is a simple comparison between periods, such as a difference, ratio, or ordering.
- You need to avoid mixing all rasters together before computing period summaries.

## Procedure
1. Identify each target period in <current task> and build a separate file list for each group.
2. For each file in each period, run the requested raster statistic (for example, spatial mean) independently and collect one numeric result per raster.
3. Verify that every period has the expected number of outputs and that each output is numeric and aligned to its source file.
4. Aggregate the per-file values within each period using the requested summary function, such as arithmetic mean, median, or sum.
5. Apply the requested comparison across the period-level aggregates in the exact order stated, using <current operation> on <period A> and <period B>.
6. Report the intermediate per-file statistics, the aggregate for each period, and the final comparison result.

## Notes / caveats
- Keep file groups strictly separated by period; do not merge period lists before aggregation.
- Compute the spatial statistic on each raster individually before averaging across time.
- Preserve operand order for directional operations such as subtraction or division.
- Check for missing files, nonnumeric outputs, or mismatched file counts before comparing periods.

## Example
Given two time windows, first compute one spatial summary per raster in each window, then average those per-file values within each window, and finally subtract the second window's aggregate from the first if that is the requested order.

#### Skill 2: aggregate-daily-raster-index-over-month

Description: Use this skill when a task asks you to compute a month-level aggregate from daily raster inputs by finding files in a date range, generating a per-day raster index, and summarizing valid pixels across the month.

## When to use
- The task asks for a monthly average or similar temporal aggregate derived from daily raster scenes.
- The needed quantity must be computed from raw daily inputs rather than read from a precomputed table.
- Each day requires combining multiple source rasters into one derived index before aggregation.
- The answer depends on valid-pixel statistics or an option selected from those statistics.

## Procedure
1. Identify the target window, study area, required per-day source rasters, and desired monthly statistic for <current task>.
2. List files under <data directory> and filter them to the requested date range <start date> to <end date>. Match all required daily inputs by date.
3. Verify that each retained day has the full input set <source raster A>, <source raster B>, ... needed for the index.
4. Run the domain-specific index computation for each day using <index tool or formula>, writing one derived raster per date.
5. Preserve nodata and valid-pixel masks during index generation. Exclude invalid pixels from later statistics.
6. Aggregate the daily derived rasters with a batch image statistics tool to compute the requested month-level value over valid pixels.
7. Confirm whether the task wants a pooled valid-pixel mean across the month or a mean of per-day scene means, and use the matching statistic.
8. Report the resulting <current value> or map it to <current option>.

## Notes / caveats
- Do not include files outside the requested time window or from mismatched dates.
- Do not average invalid or nodata pixels into the monthly result.
- Do not assume the monthly mean definition; pooled-pixel and mean-of-daily-means can differ.
- Check that output rasters are spatially aligned before batch summarization.

#### Skill 3: aggregate-daily-remote-sensing-retrievals

Description: Use this skill when a task asks for a monthly or other period average over a region, but the target variable must first be derived for each daily image from multiple remote-sensing bands using a specified retrieval method.

## When to use
- The requested output is a regional average over a month or similar time window.
- The source data are daily dated multispectral images rather than precomputed values.
- The target geophysical variable must be derived per image using a named spectral retrieval method.
- You may need to convert the final aggregate into a multiple-choice selection.

## Procedure
1. Inspect the available files in <current dataset> and identify all dated inputs that fall within <current time window> exactly.
2. Determine the required input bands or channels for <current retrieval method>, and confirm each selected day has the needed inputs.
3. Apply the retrieval method to each day to convert the multispectral inputs into a daily map or value of <current target variable> over <current region>.
4. Use the same regional mask or spatial subset for every day, and exclude invalid or missing pixels consistently.
5. Compute the regional mean for each daily derived output.
6. Aggregate the daily regional means across <current time window> to produce the final period average.
7. If the task is multiple choice, compare the computed value to <current options> and select the closest valid option.

## Notes / caveats
- Match the date filter to the requested period exactly; do not include adjacent days.
- Distinguish between the mean of daily regional means and a pixelwise temporal composite; use the one the task requests.
- Ensure the retrieval is run before aggregation; do not average raw bands when the target variable is derived.
- Keep masking, nodata handling, and region boundaries consistent across all days.

## Example
For a dated image collection, first list files for the requested month, then run the specified band-based retrieval on each daily scene, compute a regional mean per day, and finally average those daily means to obtain the monthly result.

#### Skill 4: aggregate-multi-day-image-measurements-by-location

Description: Use this skill when a task asks you to average measurement values across multiple dates for one or more locations and compare them, where the evidence is stored as separate daily images, maps, or raster snapshots rather than a table.

## When to use
- The task requests an average over a date window for one or more locations or entities.
- The source data is split across multiple image or raster files, typically one file per date.
- You must compare locations by difference, ordering, or ranking after aggregation.
- The values are not already tabulated and must be extracted consistently from each file.

## Procedure
1. List the files in <current directory> and identify the subset matching <requested date range> and <target locations>.
2. Group the matched files by <location> and align them by <date>; confirm each expected date is present for each group.
3. For each group, run the same image or raster summary method on every file to extract one comparable value per date.
4. Record the per-date outputs in a small table with columns <location>, <date>, <value>, and <unit>.
5. Compute the arithmetic mean across the requested dates for each <location>.
6. If the task asks for comparison, compute the required metric such as <difference>, <larger/smaller>, or <ranking> from the location means.
7. Report the per-date values, each location’s window average, and the requested comparison in consistent units.

## Notes / caveats
- Verify filenames and metadata carefully; nearby dates or similarly named locations are easy to mix up.
- Use exactly the same extraction settings for every image so the results remain comparable.
- Handle missing dates explicitly; do not silently average over fewer files unless the task allows it.
- Keep units and sign conventions consistent when reporting differences or rankings.

## Example
If daily measurement images are provided for two places over several consecutive dates, first extract one mean value from each image, then average the values within each place, and finally subtract one place’s average from the other if a comparison is requested.

#### Skill 5: aggregate-thermal-raster-temperature-series

Description: Use this skill when a task asks for an average temperature over a period from multiple thermal raster images in a directory, especially when you must extract per-image means and convert units such as Kelvin to Celsius before aggregating.

## When to use
- You have a folder or list of thermal raster images representing multiple timepoints.
- The task asks for a period-average temperature rather than a single-image statistic.
- You need to compute one mean value per image and then aggregate across images.
- The source temperature unit differs from the requested reporting unit.

## Procedure
1. Enumerate the relevant raster files from <input directory> or confirm the provided <file list>.
2. Identify the thermal band in each file, or use each file directly if it is already a single thermal band.
3. Compute the mean pixel value for each image with an image-statistics tool, handling <nodata rule> consistently.
4. Treat each image as one timepoint unless metadata specify a different temporal mapping.
5. Convert each per-image mean from <source unit> to <target unit> using the appropriate unit conversion.
6. Aggregate the converted per-image values according to <aggregation instruction>, such as taking the arithmetic mean.
7. Report the final aggregated temperature in <target unit>, and include intermediate per-image means if traceability is helpful.

## Notes / caveats
- Do not confuse averaging per-image means with computing one global mean across all pixels from all files combined.
- Check that the files actually match the intended time range and temporal granularity.
- Apply masking and nodata handling consistently across all images to avoid bias.
- If the task specifies averaging values after conversion, convert each image-level mean before the final aggregation.

## Example
Given a directory of daily thermal rasters, list the files, compute one mean temperature per raster, convert each mean from <source unit> to <target unit>, then average those daily values to produce the requested period-level temperature.

#### Skill 6: analyze-hotspot-direction-from-thresholded-raster

Description: Use this skill when a task asks which compass direction or regional sector contains the main concentration of anomaly, burn-scar, or hotspot pixels in a raster, especially after a thresholded index mask must be loaded or derived first.

## When to use
- The task asks where thresholded anomaly pixels are primarily concentrated within a region.
- You have spectral bands or a derived index raster and need to convert an index rule into a hotspot mask.
- The answer choices or requested output are directional labels such as north/south/east/west or quadrants.
- Multiple candidate rasters or dates exist and you must choose the correct region and time slice before comparing sectors.

## Procedure
1. Identify the raster inputs for <current region> and <current time window>. Confirm whether to use a single image, a composite, or a mosaic.
2. Load the derived index raster for <current condition>, or compute it from the required band pair using the task’s index definition.
3. Apply the threshold rule exactly as written to create a binary hotspot mask for <current threshold>. Verify the threshold sign and whether equality is included.
4. Limit analysis to <current region of interest> so pixels outside the requested bounds are excluded.
5. Partition the region using the requested directional schema, such as halves, quadrants, or named sectors.
6. Aggregate hotspot presence within each sector using pixel count, area, or another stated weighting.
7. Compare sector totals and identify the dominant direction label.
8. Sanity-check whether the leading sector is clearly stronger than the others; if the pattern is diffuse, mention that the dominance is weak.

## Notes / caveats
- Do not reverse the threshold inequality; this is a common source of flipped results.
- Do not mix dates unless the task explicitly requests summarization across multiple scenes.
- Do not double count overlapping rasters; clarify whether to mosaic first or analyze one combined product.
- Check that sector boundaries align with the region extent rather than the full raster extent.

## Example
Given band rasters for a target period, compute the requested burn-related index, threshold it into a hotspot mask, split the study area into directional sectors, count hotspot pixels per sector, and report the sector with the highest concentration plus a brief confidence note.

#### Skill 7: annual-raster-mean-trend

Description: Compute an annualized trend from a time-filtered collection of raster images when a task asks for year-over-year change from multiple dated files, especially using per-image summary statistics such as mean intensity.

## When to use
- The data are spread across many raster files with dates embedded in filenames or metadata.
- The task asks for a trend across years after restricting to a specific month, season, or other temporal subset.
- You need one comparable summary value per year, such as mean pixel intensity, before fitting a trend.
- The output must be a regression slope, trend direction, or mapped answer choice.

## Procedure
1. Enumerate all files in <data directory> and inspect names or metadata for date and location fields.
2. Filter files to those matching <location filter>, <temporal filter>, and <year range>. Exclude nonmatching months, duplicate captures, and unrelated areas.
3. Compute the requested per-image summary statistic for each selected raster, such as <statistic>.
4. Group results by year and reduce to exactly one annual value per year using <aggregation rule>. Sort the annual series by year.
5. Verify coverage: confirm the expected years are present, values are comparable, and no year has extra or missing observations unless the task allows it.
6. Fit a linear regression of <year> versus <annual value> using <trend method>.
7. Report the year-to-summary table and the regression result as <slope>, <sign>, <magnitude>, or <answer format>.

## Notes / caveats
- Do not mix files from different months or locations; filename filtering errors can invalidate the trend.
- Ensure annual values are derived consistently across all rasters with the same statistic and preprocessing assumptions.
- Check for multiple files in the same year after filtering; resolve them explicitly rather than silently averaging unless instructed.
- Preserve chronological ordering before regression and confirm the selected year range is complete.

## Example
Given a folder of dated raster images, isolate the files for a single recurring time window, compute one image summary per file, collapse to one value per year, then fit a linear trend to determine whether the annual signal is increasing or decreasing.

#### Skill 8: batch-ndvi-vegetation-timeseries

Description: Compute per-scene or daily vegetation metrics from multispectral imagery and use this skill when a task asks for mean NDVI, threshold-defined vegetation-cover proportion, and the date or scene with the highest NDVI.

## When to use
- The task provides a folder or list of multispectral scenes and asks for vegetation status over time.
- Vegetation is defined by an NDVI threshold and you must report both average NDVI and percent of pixels above that threshold.
- You need to compare scenes by date or identifier and find the peak NDVI entry.

## Procedure
1. List all candidate images in <input directory> or normalize the provided <file list>.
2. Filter to the requested <time window> and sort by <scene date or scene identifier> so downstream outputs stay aligned.
3. Run batch NDVI generation on each scene using the required <nir band> and <red band>, writing one NDVI image per input scene.
4. Compute the mean NDVI for each generated NDVI image and record results in the same order.
5. Compute the percentage of pixels with NDVI greater than <ndvi threshold> for each NDVI image to estimate vegetation cover.
6. Join <scene date or scene identifier>, mean NDVI, and vegetation-cover percentage into a single table.
7. Check whether “highest NDVI” means highest scene mean NDVI or another definition; if unspecified, use the scene-level mean series you computed.
8. Extract the maximum value and its index from the chosen NDVI series, then map that index back to the aligned <scene date or scene identifier>.
9. Return the table and the peak <scene date or scene identifier> with its corresponding NDVI value.

## Notes / caveats
- Keep the same <ndvi threshold> across all scenes; changing it breaks comparability.
- Preserve ordering between file listing, NDVI outputs, summary metrics, and max-index lookup.
- Verify all scenes belong to the requested period before computing summaries.
- Distinguish scene-mean NDVI from pixelwise extrema before selecting the final peak.

## Example
Given a monthly stack of multispectral scenes, generate NDVI for each image, summarize each NDVI raster by mean and percent above a vegetation threshold, align those metrics by date, and select the date associated with the largest scene-level mean NDVI.

## Answering Contract

Map the evidence already collected to the exact benchmark answer format.
For GAIA, return the shortest exact answer string requested by the question. For EarthBench, return the single best choice letter.
For SkillLearnBench, create the requested verifier-visible artifact, run /tests/test.sh when possible, then answer done.
Do not include explanations inside the answer tag.

Allowed tools: ATI, ChangeOS, InstructSAM, MSCN, RemoteSAM, SAM2, SM3Det, analyze_hotspot_direction, apply_cloud_mask, average_ratio_exceeding_threshold, band_ratio, bboxes2centroids, calc_batch_fire_pixels, calc_batch_image_hotspot_percentage, calc_batch_image_hotspot_tif, calc_batch_image_max, calc_batch_image_mean, calc_batch_image_mean_max_min, calc_batch_image_mean_mean, calc_batch_image_mean_threshold, calc_batch_image_sum, calc_extreme_snow_loss_percentage_from_binary_map, calc_threshold_value_mean, calculate_area, calculate_band_mean_by_condition, calculate_batch_nbr, calculate_batch_ndsi, calculate_batch_ndti, calculate_batch_ndvi, calculate_batch_ndwi, calculate_bbox_area, calculate_intersection_percentage, calculate_max_lst_by_ndvi, calculate_mean_lst_by_ndvi, calculate_multi_band_threshold_ratio, calculate_threshold_ratio, calculate_tif_average, calculate_tif_difference, calculate_water_turbidity_ntu, ceil_number, centroid_distance_extremes, coefficient_of_variation, compute_linear_trend, compute_tvdi, count_above_threshold, count_connected_components, count_images_exceeding_mean_multiplier, count_images_exceeding_threshold_ratio, count_pixels_satisfying_conditions, count_spikes_from_values, create_fire_increase_map, difference, division, get_filelist, get_list_object_via_indexes, get_percentile_value_from_image, glob_search, identify_fire_prone_areas, image_division_mean, kelvin_to_celsius, kurtosis, list_dir, lst_multi_channel, lst_single_channel, mann_kendall_test, max_value_and_index, mean, min_value_and_index, modis_day_night_lst, multiply, percentage_change, read_file, run_python_script, run_shell, sens_slope, skewness, split_window, subtract, temperature_emissivity_separation, threshold_segmentation, ttm_lst
