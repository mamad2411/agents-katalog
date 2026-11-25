---
name: earthbench-boot-al-global-static-v21-noqid-generalize-repair2
description: Global static Earth-Bench executor skill for routing remote-sensing questions
  by filename and task family, then applying the correct thermal, index, aggregation,
  scene, change, counting, or geometry tools. Use for benchmark tasks over spectrum,
  raster products, and RGB imagery when the executor must stay within the current
  question directory, pick tools from file cues, reduce outputs into scalar evidence,
  and emit a calibrated final answer.
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
  version: '1.0'
  benchmark: Earth-Bench
  release: boot-al-global-static-v21-noqid-generalize-repair2
  parent: train124-r1-source
  graph_policy: internal_graph_global_static
---

Earth-Bench global static skill.

Skill metadata:
- benchmark: Earth-Bench
- version: boot-al-global-static-v21-noqid-generalize-repair2
- parent: train124-r1-source
- graph_policy: internal_graph_global_static

Induction source:
- This route policy is induced from train124 folded G2 supervision using gold_tool_names, gold_tool_chain_truth, and gold_trajectory.
- Treat that induction as a reusable routing prior only. Do not memorize instances, hidden answers, prompt snippets, task ids, sample ids, concrete filenames, or question-specific constants.
- Use placeholders such as `<current-question>`, current file list, current filenames, `benchmark/data/<current-question>`, and `benchmark/out/<current-question>`.

Global route scaffold:
- INIT -> CLASSIFY -> one of SPECTRUM / PRODUCTS / RGB -> CALIBRATE -> CONCLUDE.
- This graph is internal planning only. Never print phase names, next tags, transition markers, or state.
- Any node may emit a final `<ANSWER>...</ANSWER>` immediately when evidence is sufficient.
- Use only relative paths inside the current task directory tree. Read from `benchmark/data/<current-question>` and write or consume derived outputs under `benchmark/out/<current-question>`.

## Phase: INIT
**Goal**
- Build a minimal evidence inventory for the current task without leaking across tasks.

**Instructions**
1. Always start with `get_filelist` on `benchmark/data/<current-question>`.
2. Inspect the returned filenames before choosing any algorithm. File extension and recurring tokens are the primary router.
3. Mentally record: image type, number of dates, paired bands, whether there are support masks such as `QA_PIXEL`, whether outputs must be generated first, and whether the question asks for a scalar, ranking, date, trend, count, ratio, area, or class tally.
4. Keep all later tool arguments anchored to the current filenames only. Never borrow an output path from another task.
5. Use `read_file` only for small support files in the same question directory when the prompt clearly depends on side metadata.
6. If evidence is already direct, for example a single raster and a single mean request, you may solve from here by moving directly to calibration and answer emission.

**Tool patterns**
- `get_filelist(dir_path='benchmark/data/<current-question>')`
- `read_file(file_path='benchmark/data/<current-question>/<support-file>')`

**Exit evidence**
- You have the current file list.
- You know whether the task is spectrum, products, or RGB.
- You know the likely family and the expected final output form.

## Phase: CLASSIFY
**Goal**
- Convert filename cues plus prompt wording into one modality route and one family route.

**Instructions**
1. Route to RGB when the current file list is mostly `.jpg`, `.jpeg`, or `.png` and the task asks about scene category, counting visible objects, change masks between two images, or object geometry.
2. Route to SPECTRUM when filenames imply sensor-band retrieval or thermal physics, for example tokens such as `LST`, `NDVI` together with thermal data, `BT10`, `BT_31`, `BT_32`, `Band 31`, `Band 32`, `Bands 10-12`, `Bands 10-14`, `Day`, `Night`, emissivity, ATI inputs, or reflectance triplets used to derive temperature or drought variables.
3. Route to PRODUCTS when filenames are already geophysical or simple raster products: precipitation, nighttime light, built volume, MaxFRP, NDVI/NDWI/NDSI/NDTI/NBR rasters, cloud-masked surface reflectance, QA masks, turbidity, or annual / monthly comparisons over rasters.
4. Within SPECTRUM choose the family by cue:
- `NDVI` plus `LST` or drought language -> TVDI.
- `BT10` plus red / NIR style cues -> single-channel LST.
- `BT_31` plus `BT_32` -> split-window or multi-channel LST.
- `Bands 10-14` or emissivity separation -> TES.
- `Bands 10-12` -> TTM.
- `Day` plus `Night` MODIS thermal -> MODIS day-night LST.
- day/night temperature plus albedo -> ATI.
- reflectance bands `2/5/17/18/19` -> band-ratio atmospheric absorption or water vapor.
5. Within PRODUCTS choose the family by cue:
- `QA_PIXEL` plus `SR_B3/SR_B5` -> cloud-mask then NDWI.
- surface reflectance with index names or bands for NDVI / NDWI / NDSI / NDTI / NBR / turbidity -> derived-index.
- precipitation, avg_rad, B10 temperature summaries, simple time averages -> timeseries-aggregation.
- `built_volume_total` or `built_volume_nres` -> arithmetic.
- `MaxFRP` or change in fire intensity -> hotspot-fire.
6. Within RGB choose the family by cue:
- scene class counting over many chips -> scene.
- 'how many', 'sort by count', facilities, ships, courts -> counting.
- before/after buildings or disaster damage -> area-change.
- centroid, closest, farthest, westmost, northmost, roundabout, storage tank, harbor, field, plane -> grounding-geometry.
7. Prefer filename-first routing even if the natural-language prompt is vague.

**Tool patterns**
- `get_filelist(dir_path='benchmark/data/<current-question>')`
- Family selection examples: `BT10 + b4 + b5 -> lst_single_channel`; `QA_PIXEL + SR_B3 + SR_B5 -> apply_cloud_mask + calculate_batch_ndwi`; `A.png/B.png pre/post -> ChangeOS`; `many .jpg chips -> MSCN`.

**Exit evidence**
- One modality route is chosen.
- One tool family is chosen.
- You know the first computational tool to call.

## Phase: SPECTRUM
**Goal**
- Derive thermal, drought, emissivity, ATI, or band-ratio evidence and reduce it to the requested scalar, ranking, trend, or date.

**Instructions**
1. Use this route for physics-style raster derivations. Start from the raw band filenames and create derived outputs in `benchmark/out/<current-question>` only.
2. TVDI route:
- If the task asks for drought index, dryness, spikes in TVDI, threshold exceedance, or drought severity from NDVI and LST, call `compute_tvdi` using the current paired date files.
- Then use reducers according to the question: `calc_batch_image_mean`, `calc_batch_image_mean_mean`, `calculate_tif_average`, `count_spikes_from_values`, `calculate_threshold_ratio`, `count_images_exceeding_threshold_ratio`, `calc_threshold_value_mean`, or `compute_linear_trend`.
3. Single-channel Landsat LST route:
- If the current files imply `BT10` plus red and NIR inputs, call `lst_single_channel`.
- For vegetation-conditioned summaries use `calculate_mean_lst_by_ndvi` or `calculate_max_lst_by_ndvi`.
- For overall means or threshold area use `calc_batch_image_mean`, `calc_batch_image_mean_mean`, `calculate_threshold_ratio`, `calc_batch_image_mean_threshold`, or `kelvin_to_celsius` when choices are in Celsius.
4. Split-window / multi-channel thermal route:
- If the task uses `BT_31` and `BT_32`, choose `lst_multi_channel` or `split_window` according to the wording. Both belong to the same family of two-band temperature retrieval.
- Then reduce by count, mean, mean-threshold, ratio, or trend with `calc_batch_image_mean`, `calc_batch_image_mean_mean`, `calculate_threshold_ratio`, `count_images_exceeding_threshold_ratio`, `count_images_exceeding_mean_multiplier`, `calc_batch_image_mean_threshold`, `max_value_and_index`, `min_value_and_index`, or `compute_linear_trend`.
5. TES route:
- If the task uses ASTER thermal bands 10-14 or mentions emissivity separation, call `temperature_emissivity_separation`.
- Then use `calculate_multi_band_threshold_ratio`, `calculate_band_mean_by_condition`, `image_division_mean`, or `calculate_threshold_ratio` depending on whether the question is about combined LST-emissivity conditions, mean emissivity within hot regions, `LST/epsilon`, or emissivity variation above threshold.
6. TTM route:
- If the task uses ASTER bands 10-12, call `ttm_lst`.
- For urban-rural or region comparisons use `calculate_band_mean_by_condition`, `calculate_threshold_ratio`, `calc_batch_image_max`, `calc_batch_image_mean_mean`, `difference`, or centroid-derived geometry if the prompt also asks about region location.
7. MODIS day-night route:
- If the current files contain day and night brightness temperature plus emissivity, call `modis_day_night_lst`.
- Then use `calculate_threshold_ratio`, `count_images_exceeding_threshold_ratio`, `average_ratio_exceeding_threshold`, or `calc_batch_image_mean_threshold` for extreme-heat style tasks.
8. ATI route:
- If filenames imply day temperature, night temperature, and albedo or the prompt names Apparent Thermal Inertia, call `ATI`.
- Then use `calc_batch_image_mean`, `calc_batch_image_mean_mean`, `calc_batch_image_mean_threshold`, `calculate_threshold_ratio`, `difference`, or `multiply` when the threshold is a scaled mean such as 115 percent of average.
9. Band-ratio atmospheric absorption route:
- If reflectance bands `2`, `5`, `17`, `18`, and `19` are present, call `band_ratio`.
- Then use `calc_batch_image_mean`, `calc_batch_image_mean_mean`, `mean`, `count_spikes_from_values`, `compute_linear_trend`, `count_images_exceeding_mean_multiplier`, or `calculate_threshold_ratio` after scaling the mean with `multiply`.
10. Common reducer rules:
- `calculate_tif_average` creates an averaged raster. Follow it with mean, sum, hotspot percentage, or another reducer only if the question asks for a statistic of the averaged raster.
- `calc_batch_image_mean` returns per-image means as a list. Use `mean` only when a second-stage aggregation across dates or cities is required.
- `calc_batch_image_mean_mean` already behaves like a higher-level aggregate. Do not add extra `mean` unless the prompt explicitly asks for a second aggregation.
- Use `max_value_and_index` or `min_value_and_index` when the answer is a date or choice tied to the extreme value.
- Use `compute_linear_trend` for linear slope questions and `sens_slope` for Sen's Slope questions.
11. Threshold repair rules:
- If the tool gives proportion above threshold but the question asks for below threshold, compute the complement with `difference` from 100.
- If the threshold is a scaled mean like 110 percent or 115 percent of average, first compute the mean, then `multiply`, then apply the threshold ratio or count tool.
- Distinguish percent outputs from fraction outputs. Many ratio tools already return percent-like values; do not multiply by 100 unless the evidence clearly remains in `[0,1]`.
12. Temporal grouping rules:
- Group by date string in the current filenames only.
- For month, season, or year comparisons, reduce within each period before comparing periods.
- For adjacent-date change logic, keep the current chronological order implied by filenames.

**Tool patterns**
- `compute_tvdi(lst_path='benchmark/data/<current-question>/<lst-file>')`
- `lst_single_channel(bt_path='benchmark/data/<current-question>/<bt10-file>')`
- `lst_multi_channel(band31_path='benchmark/data/<current-question>/<bt31-file>')`
- `temperature_emissivity_separation(tir_band_paths=['benchmark/data/<current-question>/<band10-file>', '...'])`
- `ttm_lst(tir_band_paths=['benchmark/data/<current-question>/<band10-file>', '...'])`
- `modis_day_night_lst(BT_day_path='benchmark/data/<current-question>/<day-file>')`
- `ATI(day_temp_path='benchmark/data/<current-question>/<day-file>')`
- `band_ratio(sur_refl_b02_path='benchmark/data/<current-question>/<b02-file>')`
- `calculate_threshold_ratio(image_paths=['benchmark/out/<current-question>/<derived-file>'])`
- `count_images_exceeding_threshold_ratio(image_paths=['benchmark/out/<current-question>/<derived-file>', '...'])`
- `compute_linear_trend(y=[<period-means>])`

**Exit evidence**
- You have derived the requested physical quantity.
- You have reduced it to a comparable scalar, ordered list, trend, date, count, or ratio.
- You can now map that evidence to answer choices or emit a direct numeric answer.

## Phase: PRODUCTS
**Goal**
- Solve raster-product, index, aggregation, arithmetic, turbidity, and fire-summary tasks that do not require RGB object grounding.

**Instructions**
1. Use this route when the task already lives in raster-product space or only needs simple index derivation plus aggregation.
2. Cloud-mask plus NDWI route:
- If the current directory contains `QA_PIXEL`, apply `apply_cloud_mask` to each required reflectance band before NDWI.
- Then call `calculate_batch_ndwi` on the cloud-masked current files.
- Reduce with `calc_batch_image_mean`, `mean`, `compute_linear_trend`, `difference`, or `coefficient_of_variation` depending on whether the question asks for mean, trend, change, or volatility.
3. Derived-index route:
- NDVI: `calculate_batch_ndvi`, then `calc_batch_image_mean`, `mean`, `calc_batch_image_hotspot_percentage`, `max_value_and_index`, or `difference`.
- NDSI: `calculate_batch_ndsi`, then `calc_batch_image_mean`, `calculate_tif_average`, `calc_batch_image_hotspot_percentage`, `percentage_change`, or `difference`.
- NDTI: `calculate_batch_ndti`, then `calc_batch_image_mean`, `mean`, `max_value_and_index`, `calculate_tif_average`, `multiply`, and `calculate_threshold_ratio` for high-turbidity area tasks.
- NBR: `calculate_batch_nbr`, then `calc_batch_image_mean`, `mean`, `sens_slope`, `calc_batch_image_hotspot_tif`, or `analyze_hotspot_direction`.
- Turbidity from red reflectance: `calculate_water_turbidity_ntu`, then `calc_batch_image_mean`, `mean`, `max_value_and_index`, `skewness`, or multi-day rolling comparison.
4. Timeseries-aggregation route:
- For precipitation, nighttime light, plain NDVI rasters, B10 temperatures, or simple daily products, call `calc_batch_image_mean` first.
- Use `mean` for period averages, `percentage_change` for consecutive or period-to-period change, `max_value_and_index` / `min_value_and_index` for extremes, `compute_linear_trend` for slope, `kurtosis` or `skewness` for distribution shape, and `kelvin_to_celsius` when the underlying values are Kelvin.
- When the question asks for the average of an already aggregated list, do the second reduction explicitly with `mean`.
5. Arithmetic route:
- For built volume or similar paired metrics, gather the necessary means or sums first.
- Use `calc_batch_image_sum` when the question is about total intensity or total volume after an averaged raster.
- Use `division` for ratios such as non-residential over total or light intensity per unit building volume.
- Use `difference` and `percentage_change` after the base quantities are aligned.
6. Fire / hotspot route:
- For MaxFRP counts over time, use `calc_batch_fire_pixels`, then `compute_linear_trend`, `kurtosis`, or `max_value_and_index`.
- For fire-intensity increases across periods, create comparable average rasters with `calculate_tif_average`, use `subtract` or `create_fire_increase_map`, and then `count_above_threshold`.
- For vegetation change hotspot maps across adjacent dates, use repeated `calculate_tif_difference`, then `calc_batch_image_mean`, `calc_batch_image_hotspot_percentage`, and `max_value_and_index`.
- For directional hotspot concentration after NBR, use `calculate_batch_nbr` -> `calc_batch_image_hotspot_tif` -> repeated `analyze_hotspot_direction`, then identify the dominant compass direction.
7. Common reducer rules:
- `mean` is for a list of scalar summaries, not for raw rasters.
- `calculate_tif_average` is for creating a multi-date mean map before later area or threshold analysis.
- When a question asks for the date of peak pollution or max vegetation threshold exceedance, pair the ordered statistics with filename order and use `max_value_and_index`.
- For average daily value over a period, first get per-image means, then reduce those means.
8. Statistical repair rules:
- `coefficient_of_variation`, `skewness`, and `kurtosis` summarize the distribution of already reduced time-series values.
- If a single bad value is returned as `NaN`, avoid inventing a fix; rely on the statistic tool if it still returns a usable benchmark value.
- For descriptive choices, match both sign and interpretation: increasing vs decreasing, right-skewed vs left-skewed, leptokurtic vs platykurtic.

**Tool patterns**
- `apply_cloud_mask(sr_band_path='benchmark/data/<current-question>/<sr-file>')`
- `calculate_batch_ndwi(input_nir_paths='benchmark/out/<current-question>/<masked-nir-file>')`
- `calculate_batch_ndsi(green_file_list='benchmark/data/<current-question>/<green-file>')`
- `calculate_batch_ndti(input_red_paths='benchmark/data/<current-question>/<red-file>')`
- `calculate_batch_nbr(input_nir_paths='benchmark/data/<current-question>/<nir-file>')`
- `calculate_water_turbidity_ntu(input_red_path='benchmark/data/<current-question>/<red-file>')`
- `calc_batch_image_mean(file_list=['benchmark/data/<current-question>/<product-file>'])`
- `calculate_tif_average(file_list=['benchmark/out/<current-question>/<derived-file>', '...'])`
- `calc_batch_fire_pixels(file_list=['benchmark/data/<current-question>/<maxfrp-file>', '...'])`
- `percentage_change(a=<old-value>, b=<new-value>)`

**Exit evidence**
- You have a reduced statistic or ordered comparison that matches the product-style question.
- You know whether the answer is a raw number, a trend description, a date, or a multiple-choice mapping.

## Phase: RGB
**Goal**
- Solve scene classification, visible-object counting, change detection, and geometry queries on RGB imagery.

**Instructions**
1. Scene route:
- If the prompt asks how many image chips belong to a land-use class such as industrial, airport, mountain, bridge, or farmland, run `MSCN` on each current image and count the chips whose predicted class matches the target class.
- Use the predicted top class first. Only rely on lower-ranked classes when the prompt explicitly asks for uncertainty handling.
2. Counting route:
- For questions about courts, diamonds, ships, or other repeated visible objects, prefer `InstructSAM` when the task is pure counting from a short text prompt.
- Prefer `SM3Det` when you also need bounding boxes, area ranking, or geometric follow-up on detected objects.
- For ranking tasks, compare counts or computed areas across A/B/C images and produce the full order, not only the largest.
3. Area-change route:
- For before/after building damage or change, run `ChangeOS` on the paired pre/post images in the current question directory.
- Then use `calculate_area` for changed area in pixels or real units if GSD is supplied.
- Use `count_connected_components` when the answer asks for number of fully destroyed buildings or number of changed building blobs.
- For two-region comparisons, run the full route independently for each region before comparing.
4. Geometry / grounding route:
- When the prompt names a semantic target such as roundabout, harbor, storage tank, tennis court, ground track field, or plane, use `RemoteSAM` if the query is language-rich and refers to attributes like largest, westernmost, northernmost, closest, or farthest.
- Use `SM3Det` when object class detection with boxes is sufficient.
- Convert boxes to centroids with `bboxes2centroids`.
- For closest or farthest pairs, call `centroid_distance_extremes` on the centroid list, then recover the corresponding objects with `get_list_object_via_indexes` if the task asks for boxes, or multiply the pixel distance by GSD with `multiply` if the task asks for meters.
5. Object-area route:
- If the prompt asks for area of detected facilities from boxes, use `SM3Det` followed by `calculate_bbox_area`.
- Then optionally use `division` and `ceil_number` to convert into equivalent numbers of courts or other reference units.
6. Mask-area route:
- If the prompt asks for actual object area rather than box proxy, use `SAM2` or `ChangeOS` to obtain a mask, then `calculate_area`.
- When comparing two images with different GSD, compute each area in real units before `difference`.
7. Grounding repair rules:
- 'westernmost' means smallest x among relevant candidates.
- 'northernmost' means smallest y.
- 'largest' should be resolved before or together with the positional constraint when the prompt combines both.
- If the tool already supports the composite text prompt, ask for the composite target directly instead of resolving the pieces separately.
8. Counting repair rules:
- For ranking A/B/C images, keep each image's evidence separate and only then compare.
- Use exact counts when available. Do not infer ties without counting.
- When the answer choices are qualitative rankings, numeric counts or areas are only intermediate evidence.

**Tool patterns**
- `MSCN(input_image_path='benchmark/data/<current-question>/<chip>.jpg')`
- `InstructSAM(text_prompt='basketball court')`
- `SM3Det(text_prompt='tennis court')`
- `ChangeOS(pre_image_path='benchmark/data/<current-question>/<pre-image>')`
- `calculate_area(input_image_path='benchmark/out/<current-question>/<mask-file>')`
- `count_connected_components(image_path='benchmark/out/<current-question>/<change-mask>')`
- `RemoteSAM(text_prompt='the largest roundabout on the westernmost side')`
- `bboxes2centroids(bboxes=[[x1, y1, x2, y2], ...])`
- `centroid_distance_extremes(centroids=[[cx, cy], ...])`
- `calculate_bbox_area(bboxes=[[x1, y1, x2, y2], ...])`

**Exit evidence**
- You have class counts, object counts, mask area, centroid coordinates, pairwise distances, or bounding boxes.
- You can now map those quantities to the provided options or emit the direct numeric/string answer.

## Phase: CALIBRATE
**Goal**
- Convert raw tool outputs into the exact answerable form expected by the benchmark.

**Instructions**
1. Normalize the statistic before comparing choices: know whether the evidence is a pixel count, real area, mean value, proportion, percentage, slope, intercept, date, order, or direction label.
2. Preserve sign semantics. Increasing vs decreasing, warmer vs cooler, north vs south, June lower vs August lower, and urban vs rural all matter before nearest-number matching.
3. Use complement logic when needed:
- If the question asks for below-threshold share and the tool returned above-threshold share, use `difference` from 100.
- If the question asks for unaffected share after obtaining changed share, use the same complement rule.
4. Use scale logic when needed:
- For '115 percent of mean' or similar phrases, compute the mean first, then `multiply`, then apply the threshold tool.
- Do not multiply a value by 100 unless it is clearly still a fraction and the choices are percentages.
5. Use ordering logic when needed:
- `max_value_and_index` / `min_value_and_index` give the winning statistic; map the index back to the current filenames or ordered choice set.
- For closest or farthest object tasks, use the centroid-extremes output to recover the correct pair before answering.
6. Use comparison logic when needed:
- `difference` is for absolute gap or signed gap between two already aligned values.
- `percentage_change` is for relative change from an old baseline to a new value.
- `division` is for ratios such as per-unit-area intensity or nres over total.
7. For descriptive choices, match all constraints, not only the number:
- trend direction plus slope magnitude
- date plus value
- category order plus tie structure
- location word plus count
- skewness or kurtosis plus narrative description
8. For open numeric questions with no options, obey precision requests exactly, usually with three decimals or a single concise numeric/string output inside `<ANSWER>...</ANSWER>`.
9. If several options are numerically close, reject any option that conflicts with units, direction, time period, or object identity.
10. Once one choice fully fits all evidence, stop and answer. Do not keep calling tools after calibration is decisive.

**Tool patterns**
- `difference(a=<value-a>, b=<value-b>)`
- `percentage_change(a=<baseline>, b=<new-value>)`
- `multiply(a=<mean>, b=<multiplier>)`
- `max_value_and_index(x=[<values>])`
- `min_value_and_index(x=[<values>])`
- `kelvin_to_celsius(kelvin=<kelvin-value>)`

**Exit evidence**
- Exactly one answer candidate remains consistent with the evidence.
- The answer can be emitted in the required capture format.

## Execution guards
- Use `read_file` only for prompt-required small text metadata inside the current question tree; never use it to inspect raster/image files or guessed derived artifacts.
- Do not use `run_python_script` as a fallback for path or tool issues unless calling an existing packaged helper that is already present; otherwise continue with benchmark tools only.
- Preserve tool-returned numeric lists as typed lists and keep filename order aligned; never stringify or comma-join values before `count_spikes_from_values`, `compute_linear_trend`, `sens_slope`, `kurtosis`, or `skewness`.
- Prefer batch-capable reducers over repeated single-image loops for temporal counts, means, threshold ratios, and similar multi-date statistics; if some discovered files fail, continue only on the validated subset without extrapolating.
- Before nearest-choice matching, verify quantity type, units or scale, sign, threshold direction, and aggregation level; use 'closest option' only after those semantics already match.
- After one successful `get_filelist` on the current task directory, do not re-run the same inventory unless you intentionally need to confirm newly produced artifacts under `benchmark/out/<current-question>`.
- If the same directory listing repeats or a chosen tool is unavailable or fails on the first clean attempt, commit to the routed next computation or switch immediately to the nearest already-supported alternative within the same family or simplest neighboring supported path instead of retrying or detouring.
- Never choose an option from plausibility, typical ranges, or nearest-looking intuition when the intended quantity was not directly measured or when validated measurements conflict with the choice text; after one successful measurement on the intended quantity, either map that evidence directly with unit/sign/order checks or switch once to the nearest supported direct-measurement path, then conclude without further probing.
- For RGB bbox-area tasks, keep centroid/distance reasoning separate from area reasoning; before `calculate_bbox_area`, ensure detected boxes match the coordinate representation the area tool expects, and if GSD is provided convert pixel area to real area with GSD squared exactly once, using linear GSD only for distances.

## Phase: CONCLUDE
**Goal**
- Emit the final benchmark answer in the exact capture format.

**Instructions**
1. Output exactly two lines and nothing after them:
- `<THOUGHT>brief evidence-based summary</THOUGHT>`
- `<ANSWER>final</ANSWER>`
2. When choices are present, emit exactly one multiple-choice letter in the answer tag. Use the interface letter only. In this benchmark, the default expected form is one of `<ANSWER>A</ANSWER>`, `<ANSWER>B</ANSWER>`, `<ANSWER>C</ANSWER>`, or `<ANSWER>D</ANSWER>`.
3. When no choices are present, emit the final numeric or string answer only inside the answer tag and honor the requested precision.
4. Keep the thought line short, factual, and grounded in tool evidence.
5. Do not output JSON, bullet lists, phase names, extra explanations, or multiple answer tags.
6. If evidence becomes sufficient in INIT, CLASSIFY, SPECTRUM, PRODUCTS, RGB, or CALIBRATE, you may conclude immediately without waiting for any later node.

**Tool patterns**
- No more tool calls when you are already certain.

**Exit evidence**
- The final answer has been emitted in the exact capture format.