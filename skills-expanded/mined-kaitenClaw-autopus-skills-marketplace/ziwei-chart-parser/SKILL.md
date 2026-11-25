---
name: ziwei-chart-parser
description: Extract and organize text from 文墨天機 / 紫微斗數 chart screenshots before any explanation. Use when the user sends a fate chart, asks for chart reading from an image, wants OCR from a Ziwei chart, or wants chart text grouped by position/region instead of unreliable eyeballing.
---

# Ziwei Chart Parser

Run OCR first. Do not guess star names, palace labels, or chart content from the image itself.

## Quick start

1. If the skill venv does not exist, run:
   - `bash skills/ziwei-chart-parser/scripts/setup_env.sh`
2. Activate it:
   - `source .venvs/ziwei-chart-parser/bin/activate`
3. Archive the chart as a case folder first:
   - `python skills/ziwei-chart-parser/scripts/build_chart_case.py <image-path> --cases-root tmp/ziwei-cases`
4. This creates a per-chart folder named from name + birth time when available, plus:
   - original image
   - OCR json / summary / sqlite
   - 12 palace crops
   - center / header / timeline crops
   - manifest.json
5. Read the generated `*.summary.md` first.
6. Prefer a structured Traditional Chinese schema for final output:
   - `基本資料`
   - `十二宮`
   - `宮位關係`
   - nested `星曜 -> 主星 / 輔助吉星 / 煞星 / 雜曜`
7. Use the stored ground truth reference when calibrating or regression-testing:
   - `skills/ziwei-chart-parser/references/ground-truth/alton-test-chart-optimized.json`
8. If a reference report exists, compare it:
   - `python skills/ziwei-chart-parser/scripts/compare_reference_report.py <parsed-json> <report-text-file>`
9. Only then explain the chart in simple language.

## Required workflow for every chart image

1. **Archive**
   - Run the case builder first so every new chart gets its own folder, 12 palace crops, and structured OCR outputs.
2. **Extract / Verify**
   - Read `summary.md` or `json` to confirm which text is actually present.
   - If OCR is messy, say which regions are uncertain.
3. **Structure**
   - Use the region layout (`top_left`, `center`, `timeline`, etc.) rather than freehand visual guesses.
   - Prefer the parser's structured fields: `basic_info`, `palace_map`, `main_stars`, `aux_stars`, `status_words`.
   - If needed, query the SQLite file for exact tokens and coordinates.
4. **Cross-check**
   - If the user provides a reference report or another system's output, compare star/palace claims before finalizing.
   - If a stored ground truth JSON exists for the chart/person, treat it as the regression baseline and note mismatches explicitly.
5. **Explain**
   - Use plain Cantonese / plain Chinese.
   - Separate:
     - what the screenshot definitely shows
     - what is uncertain due to OCR quality
     - the interpretation
6. **Never do**
   - Never invent stars or palace labels that are not present in OCR output.
   - Never claim a region says something if it is not visible in the extracted text.

## Output files

See `references/output-format.md` for the JSON / SQLite / summary layout.

## Response style

When replying to the user:
- Start with what was extracted successfully.
- Quote key text from the OCR output when relevant.
- Keep the explanation beginner-friendly.
- If the chart is too blurry, say so and ask for a clearer crop instead of guessing.
