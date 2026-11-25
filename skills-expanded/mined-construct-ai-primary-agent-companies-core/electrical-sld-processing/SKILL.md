---
title: Electrical SLD Processing
description: Process electrical single-line diagrams (SLD) and DWG files through a standardized AUDIT → PURGE → symbol extraction → topology validation → structured JSON pipeline for power distribution systems
version: 1.0
frequency_percent: 80.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/electrical-sld-processing
gigabrain_tags: electrical-engineering, sld-processing, dwg-processing, cad, symbol-extraction, topology-validation, power-distribution, domainforge-ai
openstinger_context: sld-pipeline, symbol-extraction, topology-validation
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_GLOSSARY.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/ELECTRICAL_AGENTS-REGISTRY-SUMMARY.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/prompts/ELECTRICAL-SLD-WORKFLOW-PROMPT.md
related_skills:
  - electrical-load-analysis
  - electrical-protection-coordination
  - pre-task-assessment-readiness
  - workflow-implementation
---

# Electrical SLD Processing

## Overview

Process electrical single-line diagrams (SLD) and DWG files through a standardized 6-stage pipeline: audit drawing, purge unnecessary layers, extract symbols, validate topology, convert to structured JSON, and perform quality check. This ensures power distribution system data is accurately captured, topologically sound, and ready for downstream electrical analysis (load flow, protection coordination, arc flash).

**Announce at start:** "I'm using the electrical-sld-processing skill to extract structured power system data from SLD/DWG drawing files."

## When to Use This Skill

**Trigger Conditions:**
- Incoming electrical SLD drawings (DWG/DXF) require data extraction for analysis
- Single-line diagram needs conversion to structured model for load flow or protection study
- Equipment schedule needs to be reconciled against the SLD
- As-built drawings need to update the digital power system model
- Power distribution documentation needs consistency checking

**Prerequisites:**
- SLD/DWG file available with revision metadata (minimum 1-line diagram, preferably complete)
- Symbol library or legend available for the drawing (IEC 60617 or project-specific symbols)
- EE-DWG-001 agent or equivalent CAD processing capability available
- Target data schema ready to receive extracted power system topology

## Step-by-Step Procedure

### Step 1: File Reception & Pre-Check

**Verify input integrity before processing:**
1. Confirm DWG/DXF file is readable (not corrupted)
2. Verify revision number matches expected version
3. Check file size is within processing limits (<500MB recommended)
4. Identify drawing type from title block (incoming SLD, main distribution, sub-distribution, motor control, etc.)
5. Confirm symbol library or legend is available for symbol identification

**Pre-check checklist:**
- [ ] File opens in CAD viewer without errors
- [ ] Drawing units confirmed (typically metric for electrical)
- [ ] Title block present with revision info, project name, voltage levels
- [ ] Symbol legend/ID list present on drawing or in separate document
- [ ] Relevant layers identified (busbars, feeders, equipment, annotations)
- [ ] No unresolved Xrefs

**If any check fails:** Flag for human CAD review, do NOT proceed to extraction.

### Step 2: Deterministic DWG Cleaning (AUDIT → PURGE Pipeline)

Run these cleaning stages in order. Each stage must complete before the next:

**Stage 1 — AUDIT:** Run CAD audit/repair to fix database errors, corrupt entities, and malformed blocks that could affect symbol recognition.

**Stage 2 — PURGE (Pass 1):** Remove unused layers, blocks, text styles, linetypes, dimension styles, and regapps that are not part of the active SLD.

**Stage 3 — OVERKILL:** Merge overlapping/duplicate lines, arcs, and polylines; delete zero-length or stray objects that create noise in symbol boundary detection.

**Stage 4 — PURGE (Pass 2):** Re-purge after overkill to catch newly orphaned layer and block entries.

**Stage 5 — EXTENTS FIX:** Zoom to extents, identify and remove far-away ghost objects that corrupt bounding boxes and symbol classification.

**Stage 6 — LAYER STANDARDIZATION:** Map incoming layers to project standard naming (e.g., "E-POWER" → "E-POWER-FEEDER", "E-EQPT" → "E-EQUIPMENT", "E-TEXT" → "E-ANNOTATION").

**Post-cleaning verification:**
- [ ] File size reduced by ≥15% (typical for electrical drawings)
- [ ] No audit errors remaining
- [ ] Bounding box matches expected drawing extents
- [ ] Layer mapping completed successfully
- [ ] All symbol blocks preserved and intact

### Step 3: Symbol Extraction & Classification

**Extract and classify electrical symbols from the SLD:**

| Symbol Category | Typical Elements | Extraction Method |
|-----------------|-----------------|-------------------|
| Power Source | Utility supply, generators, transformers (primary) | Block attribute extraction + connection analysis |
| Transformers | Power transformers, MV/LV transformers, instrument CTs/VTs | Block recognition by shape + attribute extraction |
| Switchgear | Circuit breakers, switches, disconnectors, contactors | Block recognition + trip unit rating extraction |
| Protection | Relays, fuses, MCCBs, ELCBs/RCDs | Block recognition + setting value extraction |
| Busbars | Main bus, section bus, neutral bus | Polyline extraction by layer + current rating from annotation |
| Feeders | Outgoing circuits, feeder labels, cable tags | Line/polyline extraction + text association |
| Loads | Motors, panel boards, major equipment, lighting | Block recognition + kW/kVA annotation extraction |
| Annotations | Equipment tags, ratings, cable sizes, notes | Text/MText extraction with coordinate association |

**Symbol extraction rules:**
- Only extract symbols from layers matching the SLD target layers
- Ignore presentation-only content (title block decoration, border, revision clouds that don't affect topology)
- Flag symbols with low recognition confidence (<80%) for human review
- Cross-reference extracted symbols against the drawing's symbol legend

**Extraction output format per symbol:**
```json
{
  "symbol_id": "CB-001",
  "symbol_type": "circuit_breaker",
  "ieee_symbol": "IEC-60617-S01474",
  "location": {"x": 245.0, "y": 180.0},
  "attributes": {
    "rating_amps": 400,
    "breaking_capacity_ka": 25,
    "trip_unit": "LSIG",
    "manufacturer": "ABB"
  },
  "connections": ["BUS-MAIN-A", "FEEDER-001"],
  "provenance": "layer=E-EQUIPMENT, entity=BLOCK, name=CB_MCCB_400A, id=4521"
}
```

### Step 4: Topology Validation

**Validate the power system topology extracted from the SLD:**

| Validation Rule | Description | Action on Failure |
|-----------------|-------------|-------------------|
| Source-to-load path | Every load has a valid connection path back to a power source | Flag orphaned loads |
| Voltage level consistency | Transformer ratios match voltage levels on connected sides | Flag mismatched voltage levels |
| Bus connectivity | All devices connected to a bus actually attach to bus geometry | Flag floating connections |
| Protection device presence | Every feeder has at least one protective device upstream | Flag unprotected feeders |
| Duplicate tags | No two devices share the same equipment tag | Flag duplicate tags |
| Rating sanity | No feeder rated higher than upstream breaker, no cable ampacity below load | Flag rating violations |

**Topology validation output:**
- Validated connection matrix (device-to-device)
- Voltage level ladder (HV → MV → LV mapping)
- Protection device hierarchy (upstream/downstream relationships)
- List of topology violations with severity classification

**Topology violations classification:**
| Severity | Description | Example | Action |
|----------|-------------|---------|--------|
| Critical | Topology broken or unsafe | Load with no power source path | STOP — requires human review |
| Major | Protective device missing | Feeder without upstream protection | Flag — proceed with caution |
| Minor | Rating inconsistency or annotation mismatch | Feeder annotated as 200A but breaker rated 160A | Flag — needs verification |

### Step 5: Convert to Structured JSON

**Transform validated SLD data into structured power system model JSON:**

```json
{
  "sld_metadata": {
    "source_file": "SLD-MV-MAIN-REV-C.dwg",
    "revision": "C",
    "extraction_date": "2026-03-31",
    "drawing_type": "main_single_line_diagram",
    "voltage_levels": ["11kV", "400V"],
    "coordinate_system": "Drawing Grid"
  },
  "power_system_model": {
    "sources": [
      {
        "tag": "UTILITY-01",
        "type": "utility_supply",
        "voltage_kv": 11,
        "fault_level_mva": 250,
        "connection": "BUS-MV-01"
      }
    ],
    "transformers": [
      {
        "tag": "TX-01",
        "type": "power_transformer",
        "primary_voltage_kv": 11,
        "secondary_voltage_kv": 0.4,
        "rating_kva": 1600,
        "impedance_percent": 6.0,
        "vector_group": "Dyn11",
        "upstream_connection": "BUS-MV-01",
        "downstream_connection": "BUS-LV-01"
      }
    ],
    "buses": [
      {
        "tag": "BUS-MV-01",
        "voltage_kv": 11,
        "type": "main_bus"
      }
    ],
    "protection_devices": [
      {
        "tag": "CB-001",
        "type": "circuit_breaker",
        "rating_amps": 400,
        "breaking_capacity_ka": 25,
        "trip_unit": "LSIG",
        "upstream": "BUS-MV-01",
        "downstream": "FEEDER-001"
      }
    ],
    "loads": [
      {
        "tag": "MOTOR-001",
        "type": "motor",
        "rating_kw": 75,
        "voltage_v": 400,
        "power_factor": 0.85,
        "efficiency_percent": 94.5,
        "feeder": "FEEDER-001",
        "protection": "CB-001"
      }
    ],
    "cables": [
      {
        "tag": "CBL-FDR-001",
        "from": "CB-001",
        "to": "MOTOR-001",
        "type": "XLPE/PVC/SWA",
        "cores": 3,
        "size_mm2": 95,
        "length_m": 45,
        "installation": "Cable Tray"
      }
    ]
  },
  "validation": {
    "total_devices": 48,
    "total_connections": 52,
    "topology_violations": 1,
    "flagged_for_review": 2,
    "confidence_score": 0.94
  }
}
```

### Step 6: Quality Check & Integration Handoff

**Run final quality checks before handoff:**

**Quality checklist:**
- [ ] All 6 cleaning stages completed without errors
- [ ] Symbol extraction matches symbol legend on drawing (spot-check ≥5 symbols)
- [ ] All extracted devices have unique equipment tags
- [ ] Topology validation passes with no critical violations
- [ ] Voltage levels consistent across source → transformer → bus → load chain
- [ ] Rated current of feeders ≥ connected load (checked for major loads)
- [ ] Protection devices present for all outgoing feeders
- [ ] Provenance tags attached to all extracted symbols
- [ ] Structured JSON verified as valid (parseable, no null references)

**Integration handoff:**
- **Load analysis agents** → Structured load model with kW, PF, efficiency data
- **Protection coordination agents** → Device hierarchy, ratings, relay settings data
- **Cable sizing agents** → Feeder-to-load mapping with cable specification data
- **Arc flash agents** → Bus fault current data, protection clearing times

**Handoff payload:** Structured JSON with power system model, validated topology, extraction metadata, and provenance tags.

## Success Criteria

- [ ] All 6 cleaning stages completed without errors
- [ ] Symbol extraction accuracy ≥95% (spot-verified against drawing legend)
- [ ] Topology validated — zero critical violations (source-to-load path exists for every load)
- [ ] All extracted devices assigned unique equipment tags
- [ ] Voltage levels consistent across all transformer and bus connections
- [ ] Protection devices identified for all outgoing feeders
- [ ] Structured JSON output generated, validated, and delivered to downstream agents
- [ ] Provenance tags attached to all extracted symbols and connections
- [ ] LLM layer received only validated, structured data — never raw geometry

## Common Pitfalls

1. **Skipping DWG Cleaning** — Never feed raw/un-cleaned DWG files into symbol extraction. Corrupted entities and junk layers cause false positives in symbol recognition.
2. **Assuming SLD = As-Built** — SLDs are often not updated to match as-built conditions. Always note the drawing revision date and flag discrepancies for verification.
3. **Ignoring Protection Settings** — Protection device settings may be on separate datasheets, not on the SLD itself. Extract what is on the drawing; do NOT invent settings.
4. **Missing Xref Dependencies** — Equipment schedules, relay settings, or cable schedules may be in Xref files. Verify all linked documents before declaring extraction complete.
5. **Topology Assumptions** — Do NOT assume connections that are not explicitly drawn. If a bus connection is ambiguous, flag it rather than guessing the topology.
6. **Over-Extraction of Non-Electrical Content** — Architectural elements, structural grids, and mechanical equipment may appear on electrical drawings. Only extract electrical system content.

## Cross-References

### Related Skills
- `electrical-load-analysis` — Extracted load model feeds demand calculation
- `electrical-protection-coordination` — Device hierarchy and settings feed coordination study
- `electrical-cable-sizing` — Feeder-to-load mapping feeds cable sizing
- `electrical-arc-flash-analysis` — Bus data and protection settings feed arc flash model
- `civil-dwg-processing` — DWG cleaning pipeline concepts adapted for electrical drawings
- `pre-task-assessment-readiness` — Assess drawing readiness before starting extraction

### Related Agents
- `EE-DWG-001` (deep-agents) — Primary SLD/DWG processing agent with KIMI Vision Analysis
- `EE-PROT-001` (deep-agents) — Protection device data interpretation
- `EE-QA-001` (OpenClaw) — Quality validation of extraction results
- `EE-LIB-001` (OpenClaw) — Knowledge management, symbol library, and provenance tracking

### Standards & References
- IEC 60617 — Graphical symbols for diagrams (primary symbol reference)
- IEEE 315 — American National Standard for Graphic Symbols for Electrical and Electronics Diagrams
- IEC 61850 — Communication networks and systems for power utility automation (data model reference)

## Example Usage

**Scenario:** Extract power system model from 11kV/400V main SLD (Revision C)

1. **Reception:** File `SLD-MV-MAIN-REV-C.dwg` received, 28MB, main single-line diagram, title block shows Revision C dated 2026-01-15
2. **Cleaning:** AUDIT → PURGE → OVERKILL → PURGE → EXTENTS FIX → LAYER STANDARDIZATION completed, file reduced to 19MB, 0 audit errors
3. **Extraction:** 1 utility source (11kV, 250MVA fault level), 2 power transformers (2×1600kVA, 11/0.4kV, Dyn11), 3 main buses (1×MV, 2×LV), 14 circuit breakers, 8 MCCBs, 6 fuses, 4 motor loads (37kW–160kW), 8 feeder circuits, 12 cable runs
4. **Topology Validation:** All load-to-source paths verified, 1 minor violation (feeder FDR-007 annotated load 15kW exceeds upstream MCB 10A rating — flag for verification), 0 critical violations
5. **Conversion:** Structured JSON generated with 48 devices, 52 connections, confidence score 0.94
6. **Handoff:** JSON passed to:
   - EE-LOAD-001 for load analysis (total connected load: 847kW, calculated demand: 612kW)
   - EE-PROT-001 for protection coordination study
   - EE-CABLE-001 for cable sizing verification on critical feeders

## Performance Metrics

**Target Performance:**
- Processing time: <30 seconds for files up to 100MB
- Symbol extraction accuracy: >95% correct symbol identification (verified against drawing legend)
- Topology accuracy: >98% of connections correctly mapped
- Validation pass rate: >97% of extracted devices pass rating and connectivity checks
- False positive rate: <5% of extracted symbols are false recognitions
- JSON output validity: 100% valid, parseable JSON on first pass
