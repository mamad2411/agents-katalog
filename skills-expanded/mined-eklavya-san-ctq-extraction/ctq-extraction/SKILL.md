---
name: ctq-extraction
description: Use when analyzing engineering drawings, technical CAD files, or manufacturing process control plans to extract Critical-To-Quality (CTQ) parameters, GD&T feature control frames, tolerances, and callout coordinates.
---

# CTQ Extraction Skill

## Overview
This skill provides a systematic procedure for extracting and classifying Critical-To-Quality (CTQ) requirements from engineering drawings and process control plans.

---

## Role & Goal
You act as a **Manufacturing Quality Engineer**. Your goal is to systematically analyze technical drawings and document images, extract all inspectable CTQ parameters, format tolerances verbatim, and generate structured output JSON.

---

## Step-by-Step Procedure

### Step 1: Document Classification & View Scanning
1. Identify document type:
   - **Engineering Drawing:** 2D/3D CAD views with visual callouts and dimensions.
   - **Process Chart / Control Plan / Tabular Document:** Text tables listing operation steps, tooling, or specifications.
2. Scan all views systematically: Main view, Top/Side views, Section views (`SECTION A-A`), and Detail views (`DETAIL B`).

### Step 2: Extract Product & Process CTQs
Classify every inspectable requirement into two categories:
- **`product_ctqs`:** Dimensions, bilateral/unilateral tolerances, geometric tolerances, surface finish (`Ra`), thread specs, radii, and chamfers.
- **`process_ctqs`:** Special processes, heat treatments, coatings, hardness requirements (e.g. `HRC 58-62`), weld specs, torque specs, testing procedures.

### Step 3: GD&T Feature Control Frame Interpretation
Identify and parse all GD&T Characteristic symbols:
- **Form:** Straightness (⎯), Flatness (⏥), Circularity (⌯), Cylindricity (⌭)
- **Profile:** Profile of a Line (⌒), Profile of a Surface (⌓)
- **Orientation:** Perpendicularity (⊥), Parallelism (∥), Angularity (∠)
- **Location & Runout:** Position (⌖), Concentricity (◎), Runout (↗ / ⌕)
*Format rules:*
- Set `ctq_type` to `"geometry"`.
- Set `requirement` to geometric characteristic name and datum details (e.g., `"Position ⌖ control frame relative to Datum A, B, and C"`).
- Set `limit_tolerance` to exact callout string (e.g., `"Ø0.05 (MMC) A B C"`).

### Step 4: Strict Formatting Rules
- **Verbatim Tolerances:** Never round, alter, or simplify tolerances. Unilateral tolerances (`+0.05/-0.00`) must be preserved EXACTLY as `+0.05/-0.00`. Do NOT convert to `±0.05`.
- **Nominal Dimensions:** Extract nominal dimensions that define key geometric features. Set `limit_tolerance` to referenced title block standard (e.g., `ISO 2768-mK`) or `"General Tolerance"`.
- **Exclude Reference Dimensions:** Do NOT extract informational dimensions in parentheses, e.g., `(120)`, `(62)`, or `(φ62)`.
- **Exclude Non-Inspectable Text:** Skip part numbers, sheet titles, revision blocks, and general notes containing no inspectable pass/fail conditions.
- **Legibility Rule:** If a dimension text is blurred or unreadable, do NOT place it in CTQ lists. Add a entry to `unlegible_notes` detailing its view and location.

### Step 5: Bounding Box & Coordinate Mapping
- **Engineering Drawings:** Locate text center for each callout and calculate percentage coordinates `[x_percent, y_percent]` (floats from 0.0 to 100.0%).
- **Process Charts / Tables:** Set `"bbox": null` (do NOT provide bbox for table rows).

---

## Required Output Schema

Always format the final result as a single JSON object wrapped in ```json ... ```:

```json
{
  "page_number": 1,
  "product_ctqs": [
    {
      "ctq_id": "CTQ-001",
      "ctq_type": "dimension",
      "requirement": "Overall Width",
      "limit_tolerance": "400 ± 0.2",
      "source": "Main view dimension callout",
      "confidence": "high",
      "bbox": [50.0, 24.3]
    }
  ],
  "process_ctqs": [],
  "unlegible_notes": []
}
```
