---
title: Civil DWG Processing
description: Process civil engineering DWG/DXF files through standardized cleaning, extraction, and validation pipeline before AI-assisted analysis
version: 1.0
frequency_percent: 85.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-dwg-processing
gigabrain_tags: civil-engineering, dwg-processing, cad, extraction, geometry, cleaning, validation, domainforge-ai
openstinger_context: dwg-pipeline, geometry-extraction
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_GLOSSARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/00850_AGENTS-REGISTRY-SUMMARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/prompts/00850_CIVIL-DOCUMENTATION-WORKFLOW-PROMPT.md
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
---

# Civil DWG Processing

## Overview

Process civil engineering DWG/DXF files through a standardized 7-stage pipeline: file reception, deterministic cleaning, feature classification, data extraction, validation, provenance tagging, and integration handoff. This ensures geometry-derived data is accurate, structured, and safe for downstream AI processing.

**Announce at start:** "I'm using the civil-dwg-processing skill to extract structured data from CAD drawing files."

## When to Use This Skill

**Trigger Conditions:**
- Incoming civil engineering drawings (DWG/DXF) require data extraction
- DWG geometry needs analysis or conversion to structured data (CSV/JSON)
- Drawing-to-document consistency checking is required
- Quantity takeoff from CAD drawings is needed
- Clash detection between disciplines requires model extraction

**Prerequisites:**
- DWG/DXF file available with revision metadata
- Extraction schema defined for the drawing type (site plan, drainage layout, road alignment, structural GA, etc.)
- CE-DWG-001 agent or equivalent CAD processing capability available
- Target data schema ready to receive extracted features

## Step-by-Step Procedure

### Step 1: File Reception & Pre-Check

**Verify input integrity before processing:**
1. Confirm DWG/DXF file is readable (not corrupted)
2. Verify revision number matches expected version
3. Check file size is within processing limits (<500MB recommended)
4. Identify drawing type from title block or filename convention
5. Confirm required extraction schema exists for this drawing type

**Pre-check checklist:**
- [ ] File opens in CAD viewer without errors
- [ ] Drawing units confirmed (metric/imperial)
- [ ] Coordinate system identified
- [ ] Title block present with revision info
- [ ] Relevant layers identified
- [ ] No unresolved Xrefs

**If any check fails:** Flag for human CAD review, do NOT proceed to extraction.

### Step 2: Deterministic DWG Cleaning (7-Stage Pipeline)

Run these cleaning stages in order. Each stage must complete before the next:

**Stage 1 — AUDIT:** Run CAD audit/repair to fix database errors and corrupt entities.

**Stage 2 — PURGE (Pass 1):** Remove unused layers, blocks, text styles, linetypes, regapps.

**Stage 3 — OVERKILL:** Merge overlapping/duplicate lines, arcs, polylines; delete zero-length or tiny stray objects.

**Stage 4 — PURGE (Pass 2):** Re-purge after overkill to catch newly orphaned entries.

**Stage 5 — EXTENTS FIX:** Zoom to extents, identify and remove far-away ghost objects that corrupt bounding boxes.

**Stage 6 — XREF CLEAN:** Bind or detach unnecessary Xrefs; resolve missing references or flag for human review.

**Stage 7 — LAYER STANDARDIZATION:** Map incoming layers to project standard naming (e.g., "WALLS" → "A-WALL", "DRAIN" → "C-DRAIN").

**Post-cleaning verification:**
- [ ] File size reduced by ≥20% (typical)
- [ ] No audit errors remaining
- [ ] Bounding box matches expected drawing extents
- [ ] Layer mapping completed successfully

### Step 3: Feature Classification & Extraction

**Classify drawing elements into the extraction schema:**

| Feature Category | Drawing Elements | Extraction Method |
|-----------------|-----------------|-------------------|
| Survey Points | Point entities, coordinate blocks | Block attribute extraction |
| Contours | Polyline entities on contour layers | Polyline vertex extraction with elevation |
| Drainage Networks | Lines, blocks, text on drainage layers | Network topology extraction |
| Road Alignments | Polylines, curves, chainage markers | Alignment geometry extraction |
| Structures | Blocks, hatches, text on structural layers | Block + attribute extraction |
| Dimensions | Dimension entities | Value + reference extraction |
| Annotations | Text, MText entities | Text content extraction with coordinates |

**Classification rules:**
- Only extract from layers matching the schema's target layers
- Ignore presentation-only content (hatches, image references, viewport boundaries)
- Flag elements with low classification confidence (<80%) for human review

### Step 4: Data Structuring (CSV/JSON Output)

**Transform extracted features into structured data:**

```json
{
  "extraction_metadata": {
    "source_file": "original_filename.dwg",
    "revision": "C",
    "extraction_date": "2026-03-31",
    "drawing_type": "site_drainage_plan",
    "coordinate_system": "Local Grid"
  },
  "features": {
    "drainage_pipes": [
      {
        "tag": "P-001",
        "start_node": {"x": 100.0, "y": 200.0},
        "end_node": {"x": 150.0, "y": 225.0},
        "diameter_mm": 300,
        "gradient": "1:100",
        "invert_level_start": 52.350,
        "invert_level_end": 52.250,
        "provenance": "layer=C-DRAIN-PIPE, entity=LWPOLYLINE, id=4521"
      }
    ],
    "manholes": [
      {
        "tag": "MH-01",
        "location": {"x": 100.0, "y": 200.0},
        "cover_level": 53.500,
        "invert_level": 52.350,
        "provenance": "layer=C-DRAIN-STRUCT, entity=BLOCK, name=MH_STD_1200"
      }
    ]
  },
  "validation": {
    "total_features": 245,
    "flagged_for_review": 3,
    "confidence_score": 0.96
  }
}
```

### Step 5: Validation & Range Checking

**Run validation rules against extracted data:**

| Validation Rule | Description | Action on Failure |
|-----------------|-------------|-------------------|
| Unit sanity check | No pipe diameter > 5000mm, no chainage < 0 | Flag for human review |
| Topology check | All pipe endpoints connect to nodes | Flag disconnected elements |
| Gradient check | Drainage gradients between 0.1% and 10% | Flag out-of-range values |
| Elevation check | Invert levels below cover levels | Flag inverted pairs |
| Duplicate check | No identical feature at same coordinates within tolerance | Remove duplicates |

**If any validation fails:** Do NOT pass to LLM layer. Flag specific failures for human CAD review.

### Step 6: Provenance Tagging

**Attach provenance metadata to every extracted feature:**
- Source drawing filename and revision
- Original entity type (LWPOLYLINE, BLOCK, TEXT, etc.)
- Original entity ID in DWG
- Layer name before standardization
- Extraction timestamp

This enables click-through from extracted data back to the source drawing element.

### Step 7: Integration Handoff

**Pass validated, structured data to downstream consumers:**
- **Quantity takeoff agents** → BOQ generation
- **Design consistency checkers** → Drawing-to-spec comparison
- **BIM coordinators** → Clash detection
- **Documentation agents** → Drawing schedules and references

**Handoff payload:** Structured JSON with metadata, features, validation results, and provenance tags.

## Success Criteria

- [ ] All 7 cleaning stages completed without errors
- [ ] Extraction schema matched drawing type successfully
- [ ] All features classified with ≥80% confidence (or flagged)
- [ ] Validation rules passed (or failures flagged and isolated)
- [ ] Provenance tags attached to all extracted features
- [ ] Structured JSON output generated and delivered to downstream agents
- [ ] LLM layer received only validated, structured data — never raw geometry

## Common Pitfalls

1. **Skipping DWG Cleaning** — Never feed raw/un-cleaned DWG files into extraction. Corrupted entities and junk layers cause extraction errors.
2. **Assuming Geometry = Truth** — DWG geometry must be validated before use. Drawing errors exist; do not let LLM "invent" values to fill gaps.
3. **Ignoring Provenance** — Without provenance tags, reviewers cannot trace extracted values back to source elements. Always attach source metadata.
4. **Over-Extraction** — Only extract what the schema defines. Do not extract everything in the file; this creates noise and false positives.
5. **Missing Xref Dependencies** — If the drawing references external files that are unresolved, extraction may be incomplete. Verify Xrefs before proceeding.

## Cross-References

### Related Skills
- `civil-quantity-takeoff` — Use extracted data for BOQ generation
- `civil-site-assessment` — DWG processing for survey data
- `civil-design-development` — Extraction feeds design calculations
- `pre-task-assessment-readiness` — Assess readiness before starting extraction

### Related Agents
- `CE-DWG-001` (deep-agents) — Primary DWG processing agent with KIMI Vision Analysis
- `CE-LIB-001` (OpenClaw) — Knowledge management and provenance tracking
- `CE-QA-001` (OpenClaw) — Quality validation of extraction results

## Example Usage

**Scenario:** Extract drainage network from site drainage plan (Revision C)

1. **Reception:** File `DWG-0043-REV-C.dwg` received, 45MB, drainage layout
2. **Cleaning:** 7-stage pipeline completed, file reduced to 32MB, 0 audit errors
3. **Extraction:** 12 drainage pipes, 8 manholes, 4 catch basins, 3 outfalls
4. **Validation:** All topology checks passed, 1 pipe gradient at 0.08% flagged (marginally below 0.1% minimum)
5. **Provenance:** All 27 features tagged with source layer, entity ID, and extraction timestamp
6. **Handoff:** Structured JSON passed to quantity takeoff agent for pipe length schedules

## Performance Metrics

**Target Performance:**
- Processing time: <30 seconds for files up to 100MB
- Extraction accuracy: >95% feature recognition
- Validation pass rate: >98% of features within expected ranges
- False positive rate: <5% of extracted features flagged incorrectly