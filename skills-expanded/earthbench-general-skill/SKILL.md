---
name: earthbench-general-skill
description: Global static EarthBench skill for raster, image, geospatial, numeric, and choice-matching workflows.
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
  - calc_batch_image_mean_mean
  - calc_batch_image_mean_threshold
  - calc_batch_image_sum
  - calc_threshold_value_mean
  - calculate_area
  - calculate_band_mean_by_condition
  - calculate_batch_nbr
  - calculate_batch_ndsi
  - calculate_batch_ndti
  - calculate_batch_ndvi
  - calculate_batch_ndwi
  - calculate_bbox_area
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
  - count_spikes_from_values
  - create_fire_increase_map
  - difference
  - division
  - get_filelist
  - get_list_object_via_indexes
  - image_division_mean
  - kelvin_to_celsius
  - kurtosis
  - lst_multi_channel
  - lst_single_channel
  - max_value_and_index
  - mean
  - min_value_and_index
  - modis_day_night_lst
  - multiply
  - percentage_change
  - read_file
  - run_python_script
  - sens_slope
  - skewness
  - split_window
  - subtract
  - temperature_emissivity_separation
  - ttm_lst
metadata:
  benchmark: EarthBench
  generator: Manus
  baseline: manus_plain_skill
  generation_constraints: earthbench_v2_folded_gold_no_instance_memory_v4
  allowed_gold_input: train124_firstarg_folded_v2
  gold_trim_policy: "20260520_firstarg_shortnotice_repeatfold_v2"
  skill_injection_mode: global_static
  runtime_state_transitions: disabled
  date: "2026-05-20"
---

# EarthBench General Skill

## File Listing and Modality Triage

Every task begins with discovering available data files:

1. **List the data directory** using `get_filelist(dir_path="benchmark/data/question<ID>")`.
2. **Classify files by naming convention**:
   - Files containing `_LST` → Land Surface Temperature brightness temperature rasters.
   - Files containing `_NDVI` or `_b4`/`_b5`/`_Red`/`_NIR` → Vegetation reflectance bands.
   - Files containing `_BT_31`/`_BT_32` → MODIS thermal bands for split-window LST.
   - Files containing `_NBR`/`_NDSI`/`_NDTI`/`_NDWI` → Pre-computed spectral indices.
   - Files with RGB or multi-band indicators → Detection/segmentation inputs.
   - Files with fire/hotspot indicators → Fire analysis inputs.
3. **Determine the workflow family** from the question keywords and available file types.

## Raster Grouping

When multiple TIF files exist for a time series:

- Group files by date extracted from filenames (pattern: `Region_YYYY-MM-DD_Band.tif`).
- Process each temporal group with the same tool sequence.
- Collect per-date outputs before aggregation.
- When the gold shows repeated tool calls (e.g., multiple `compute_tvdi` or `lst_single_channel`), apply the same tool to each date's file set.

## RGB/Image Detection and Segmentation

For tasks requiring object detection, segmentation, or change detection:

### Object Detection

```
SM3Det(image_path="<path>", prompt="<object_category>")
RemoteSAM(image_path="<path>", prompt="<object_category>")
```

- Use `SM3Det` for small/medium object detection in remote sensing imagery.
- Use `RemoteSAM` for prompted segmentation of specific objects.
- Use `SAM2` for general-purpose segmentation.
- Use `InstructSAM` when natural language instructions guide segmentation.

### Change Detection

```
ChangeOS(image1_path="<before>", image2_path="<after>")
```

- Requires two temporally distinct images of the same region.
- Returns change mask or change statistics.

### Post-Detection Processing

```
bboxes2centroids(bboxes=<detection_output>)
calculate_bbox_area(bboxes=<detection_output>)
centroid_distance_extremes(centroids=<centroid_list>)
count_connected_components(mask_path="<segmentation_output>")
calculate_area(mask_path="<segmentation_output>")
```

## Spectral Index Workflows

### Vegetation Index (NDVI)

```
calculate_batch_ndvi(red_paths=[<red_band_files>], nir_paths=[<nir_band_files>], output_dir="benchmark/out/question<ID>")
```

### Water Index (NDWI)

```
calculate_batch_ndwi(green_paths=[<green_files>], nir_paths=[<nir_files>], output_dir="benchmark/out/question<ID>")
```

### Snow Index (NDSI)

```
calculate_batch_ndsi(green_paths=[<green_files>], swir_paths=[<swir_files>], output_dir="benchmark/out/question<ID>")
```

### Burn Ratio (NBR)

```
calculate_batch_nbr(nir_paths=[<nir_files>], swir_paths=[<swir_files>], output_dir="benchmark/out/question<ID>")
```

### Tillage Index (NDTI)

```
calculate_batch_ndti(swir1_paths=[<swir1_files>], swir2_paths=[<swir2_files>], output_dir="benchmark/out/question<ID>")
```

### Band Ratio (Generic)

```
band_ratio(numerator_path="<band_a>", denominator_path="<band_b>")
```

### Drought Index (TVDI)

```
compute_tvdi(lst_path="<LST_file>", ndvi_path="<NDVI_file>", output_dir="benchmark/out/question<ID>")
```

- Requires paired LST and NDVI files for the same date.
- Process each date independently, then aggregate.

## Land Surface Temperature (LST) Workflows

### Single-Channel Method (Landsat 8 Band 10)

```
lst_single_channel(bt_path="<BT10_file>", red_path="<Red_file>", nir_path="<NIR_file>", output_dir="benchmark/out/question<ID>")
```

- Requires brightness temperature (Band 10) plus Red and NIR bands for NDVI-based emissivity.
- Produces LST in Kelvin.

### Multi-Channel / Split-Window Method (MODIS Bands 31, 32)

```
lst_multi_channel(bt31_path="<BT31_file>", bt32_path="<BT32_file>", output_dir="benchmark/out/question<ID>")
split_window(bt31_path="<BT31_file>", bt32_path="<BT32_file>", output_dir="benchmark/out/question<ID>")
```

### MODIS Day/Night LST

```
modis_day_night_lst(day_path="<day_file>", night_path="<night_file>")
```

### Temperature-Emissivity Separation

```
temperature_emissivity_separation(thermal_paths=[<thermal_files>], output_dir="benchmark/out/question<ID>")
```

### TTM LST

```
ttm_lst(thermal_path="<file>", output_dir="benchmark/out/question<ID>")
```

### Kelvin to Celsius Conversion

```
kelvin_to_celsius(value=<kelvin_value>)
```

- Apply only when the question or choice explicitly uses Celsius.

## Product Raster Aggregation

After generating per-date product rasters (TVDI, LST, NDVI, etc.), aggregate:

### Spatial Averaging Per Image

```
calculate_tif_average(file_list=[<output_tifs>], output_dir="benchmark/out/question<ID>")
calc_batch_image_mean(file_list=[<output_tifs>])
```

- `calculate_tif_average` produces a single averaged raster from multiple inputs.
- `calc_batch_image_mean` returns a list of per-image spatial mean values.

### Batch Statistics

```
calc_batch_image_max(file_list=[<tifs>])
calc_batch_image_sum(file_list=[<tifs>])
calc_batch_image_mean_mean(file_list=[<tifs>])
calc_batch_image_mean_threshold(file_list=[<tifs>], threshold=<value>)
calc_batch_image_hotspot_percentage(file_list=[<tifs>], threshold=<value>)
calc_batch_image_hotspot_tif(file_list=[<tifs>], threshold=<value>)
calc_batch_fire_pixels(file_list=[<tifs>])
```

### Threshold and Exceedance Counting

```
calculate_threshold_ratio(image_paths=[<tifs>], threshold=<value>)
count_images_exceeding_threshold_ratio(image_paths=[<tifs>], threshold=<value>, ratio=<percentage>)
count_images_exceeding_mean_multiplier(image_paths=[<tifs>], multiplier=<value>)
count_above_threshold(values=[<list>], threshold=<value>)
average_ratio_exceeding_threshold(image_paths=[<tifs>], threshold=<value>)
```

### Trend and Statistical Analysis

```
compute_linear_trend(y=[<annual_values>])
sens_slope(values=[<time_series>])
coefficient_of_variation(values=[<list>])
kurtosis(values=[<list>])
skewness(values=[<list>])
count_spikes_from_values(values=[<list>])
```

### Arithmetic Helpers

```
difference(a=<value1>, b=<value2>)
subtract(a=<value1>, b=<value2>)
division(a=<numerator>, b=<denominator>)
multiply(a=<value1>, b=<value2>)
percentage_change(old=<value1>, new=<value2>)
mean(values=[<list>])
max_value_and_index(values=[<list>])
min_value_and_index(values=[<list>])
ceil_number(value=<float>)
image_division_mean(image_path="<tif>", divisor=<value>)
calculate_tif_difference(file1="<tif1>", file2="<tif2>")
```

### Conditional Band Analysis

```
calculate_band_mean_by_condition(band_path="<tif>", condition_path="<mask_or_index>", threshold=<value>, above=<bool>)
calculate_mean_lst_by_ndvi(red_paths="<red>", nir_paths="<nir>", lst_path="<lst>", ndvi_threshold=<value>, above=<bool>)
calculate_max_lst_by_ndvi(red_paths="<red>", nir_paths="<nir>", lst_path="<lst>", ndvi_threshold=<value>, above=<bool>)
calculate_multi_band_threshold_ratio(image_paths=[<tifs>], thresholds=[<values>])
```

### Fire and Hotspot Analysis

```
calc_batch_fire_pixels(file_list=[<tifs>])
calc_batch_image_hotspot_percentage(file_list=[<tifs>], threshold=<value>)
analyze_hotspot_direction(hotspot_map="<tif>")
create_fire_increase_map(before_path="<tif1>", after_path="<tif2>")
```

### Cloud Masking

```
apply_cloud_mask(image_path="<tif>", cloud_mask_path="<mask>")
```

- Apply before any spectral index or LST computation if cloud mask files are present.

### Water Turbidity

```
calculate_water_turbidity_ntu(red_path="<red_band>", nir_path="<nir_band>")
```

### ATI (Apparent Thermal Inertia)

```
ATI(day_lst_path="<day>", night_lst_path="<night>", albedo_path="<albedo>")
```

## Unit and Sign Guardrails

- LST outputs are in **Kelvin** unless explicitly converted. Check whether choices use K or C.
- TVDI is dimensionless [0, 1]. Higher values indicate drier conditions.
- NDVI is dimensionless [-1, 1]. Vegetation thresholds are typically 0.2–0.7.
- Percentage ratios from threshold tools are in **percent (0–100)**, not fractions.
- `difference(a, b)` computes `a - b`. Verify operand order matches the question's phrasing (e.g., "how much cooler" = warmer - cooler).
- `percentage_change(old, new)` computes `(new - old) / old * 100`.
- Linear trend slope sign: negative = decreasing, positive = increasing.
- When the question asks "proportion below X", compute `100 - proportion_above_X` using `difference`.

## Choice Matching

EarthBench tasks typically require selecting from multiple-choice options (A/B/C/D):

1. **Compute the numeric result** using the appropriate workflow.
2. **Compare to each choice**:
   - Extract the numeric value or key phrase from each option.
   - Match the computed result to the closest option.
3. **Tie-breaking rules**:
   - If the computed value falls between two options, choose the nearest.
   - If the question asks about a trend direction, match direction first, then magnitude.
   - If choices differ in units, ensure unit consistency before comparing.
4. **Return the letter only** (A, B, C, or D).

### Common Choice Patterns

- Trend questions: choices differ in direction (increasing/decreasing) and rate.
- Count questions: choices are integers; match exactly.
- Percentage questions: choices are percentages; match to nearest.
- Temperature difference questions: choices include units (K or C); verify unit match.

## Final Answer Normalization

- Return exactly one letter (A, B, C, or D) for multiple-choice questions.
- For numeric-answer questions, return the number in the requested format.
- Do not include explanation, units, or extra text in the final answer.
- Do not include the option text, only the letter.

## Recovery When Paths Conflict

If tool outputs, filenames, or choices produce unexpected results:

1. **Re-check file grouping** — ensure LST/NDVI/band files are correctly paired by date and region.
2. **Verify tool arguments** — confirm paths point to existing output files, not input files when aggregating.
3. **Check intermediate values** — use `read_file` or `run_python_script` to inspect raster statistics.
4. **Try alternative LST method** — if `lst_single_channel` produces unexpected values, check if `split_window` or `lst_multi_channel` is more appropriate for the sensor.
5. **Recompute with explicit paths** — if batch tools fail, process files individually and aggregate manually.
6. **Validate against choices** — if no choice matches, re-examine whether the question asks for "above" vs "below", "exceeding" vs "below", or requires a complement calculation.
7. **Use `run_python_script`** — as a last resort, write a Python script to manually read rasters and compute the answer using numpy/rasterio.

## Workflow Family Quick Reference

| Question Pattern | Typical Tool Chain |
|-----------------|-------------------|
| TVDI trend over years | `get_filelist` → `compute_tvdi` (per date) → `calculate_tif_average` (per year) → `calc_batch_image_mean` → `compute_linear_trend` |
| LST threshold proportion | `get_filelist` → `lst_single_channel`/`lst_multi_channel` → `calculate_threshold_ratio` → optionally `difference` |
| LST by vegetation class | `get_filelist` → `lst_single_channel` → `calculate_mean_lst_by_ndvi` (twice) → `difference` |
| Exceedance day count | `get_filelist` → LST tool (per date) → `count_images_exceeding_threshold_ratio` |
| Spike detection | `get_filelist` → index tool → `calc_batch_image_mean` → `count_spikes_from_values` |
| Object detection/counting | `get_filelist` → `SM3Det`/`RemoteSAM` → `bboxes2centroids` → counting/area tools |
| Change detection | `get_filelist` → `ChangeOS` → `count_connected_components`/`calculate_area` |
| Fire analysis | `get_filelist` → `calc_batch_fire_pixels` → aggregation → trend |
| Water turbidity | `get_filelist` → `calculate_water_turbidity_ntu` |
| NDVI/NDWI/NDSI batch | `get_filelist` → `calculate_batch_ndvi`/`ndwi`/`ndsi` → aggregation |
