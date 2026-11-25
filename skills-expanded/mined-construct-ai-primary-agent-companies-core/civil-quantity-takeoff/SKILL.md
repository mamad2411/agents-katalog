---
title: Civil Quantity Takeoff
description: Extract material quantities from civil engineering drawings and specifications for BOQ generation, cost estimation, and procurement planning
version: 1.0
frequency_percent: 60.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-quantity-takeoff
gigabrain_tags: civil-engineering, quantity-takeoff, boq, cost-estimation, material-extraction, procurement
openstinger_context: material-quantities, boq-generation
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_GLOSSARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/prompts/00850_CIVIL-DOCUMENTATION-WORKFLOW-PROMPT.md
related_skills:
  - pre-task-assessment-readiness
  - civil-dwg-processing
  - civil-documentation
  - civil-tender-preparation
---

# Civil Quantity Takeoff

## Overview

Extract and calculate material quantities from civil engineering drawings and specifications for Bill of Quantities (BOQ) generation, cost estimation, and procurement planning. Uses automated DWG extraction combined with specification analysis to produce accurate quantity schedules with traceability.

**Announce at start:** "I'm using the civil-quantity-takeoff skill to extract material quantities for BOQ generation."

## When to Use This Skill

**Trigger Conditions:**
- BOQ needs preparation for tender
- Cost estimation required for design option comparison
- Material procurement quantities need verification
- Variation order quantities need to be calculated
- Progress payment quantities need to be measured

**Prerequisites:**
- Construction drawings at sufficient detail (minimum preliminary design, preferably IFC)
- Specifications available for material identification
- CE-QS-001 agent or equivalent quantity capability available
- DWG files available for automated extraction (or clear PDFs for manual takeoff)

## Step-by-Step Procedure

### Step 1: Drawing and Specification Review

**Review source documents for quantity extraction:**

**Required drawings:**
- [ ] Site plan (overall layout)
- [ ] Earthworks plan (cut/fill contours)
- [ ] Road profiles and cross-sections
- [ ] Drainage layout and profiles
- [ ] Water reticulation layout
- [ ] Sewer reticulation layout
- [ ] Details (kerbs, pavements, structures)

**Required specifications:**
- [ ] Earthworks specification (compaction, material types)
- [ ] Pavement specification (layer types, thicknesses)
- [ ] Drainage specification (pipe types, bedding)
- [ ] Structures specification (concrete grades, reinforcing)

### Step 2: Quantity Categories Definition

**Define the quantity breakdown structure:**

**Standard BOQ categories for civil engineering:**
```
1. Preliminaries
   1.1 Site establishment
   1.2 Temporary works
   1.3 Site management

2. Site Preparation
   2.1 Clearing and grubbing (m²)
   2.2 Topsoil strip (m³)
   2.3 Demolition (m²)
   2.4 Service relocation (No.)

3. Earthworks
   3.1 Cut to spoil (m³)
   3.2 Fill from borrow (m³)
   3.3 Fill from cut material (m³)
   3.4 Subgrade preparation (m²)
   3.5 Geotextile separation (m²)
   3.6 Geogrid reinforcement (m²)
   3.7 Disposal of surplus material (m³)
   3.8 Haulage (ton.km)

4. Roads and Pavements
   4.1 Sub-base (G7) (m³)
   4.2 Base course (G5) (m³)
   4.3 Asphalt wearing course (mm AC) (m²)
   4.4 Concrete kerbs (m)
   4.5 Concrete channels (m)
   4.6 Sidewalks/pavers (m²)

5. Stormwater Drainage
   5.1 Pipes: [diameter] HDPE/Reinforced Concrete (m)
   5.2 Manholes: [Type] (No.)
   5.3 Catch basins (No.)
   5.4 Headwalls (No.)
   5.5 Rip-rap (m³)
   5.6 Detention basin excavation (m³)
   5.7 Detention basin lining (m²)

6. Water Reticulation
   6.1 Pipes: [diameter] [material] (m)
   6.2 Valves: [type, size] (No.)
   6.3 Fire hydrants (No.)
   6.4 Meter chambers (No.)

7. Sewer Reticulation
   7.1 Pipes: [diameter] [material] (m)
   7.2 Manholes: [diameter/depth] (No.)
   7.3 Pump stations (No.)

8. Retaining Structures
   8.1 Gravity walls (m³ concrete)
   8.2 Cantilever walls (m³ concrete + kg rebar)
   8.3 MSE walls (m² face area)
   8.4 Gabion baskets (m³)
   8.5 Soil nailing (No.)

9. Landscaping
   9.1 Topsoil replacement (m³)
   9.2 Grassing/seeding (m²)
   9.3 Trees planted (No.)
   9.4 Irrigation (m²)

10. Provisional Sums
    10.1 [Item description] (Lump Sum)
```

### Step 3: Automated Quantity Extraction

**Use CE-DWG-001 and CE-QS-001 agents to extract quantities from drawings:**

**Extraction methods by quantity type:**

| Quantity | Method | Data Source |
|----------|--------|-------------|
| Linear pipes | DWG polyline length extraction | Drainage layout DWG |
| Areas (pavement, grassing) | DWG polygon area calculation | Site plan DWG |
| Volumes (earthworks) | Cross-section integration or grid method | Earthworks contours DWG |
| Numbered items (manholes, valves) | Block count extraction | Layout DWG |
| Concrete volumes | Dimension-based calculation | Detail drawings/spec |
| Reinforcement weight | Detail drawing bar schedules | Reinforcement DWG |

**Extraction accuracy checks:**
- [ ] DWG extraction counts match manual count for 3 random items
- [ ] Pipe lengths match chainage measurements from profiles
- [ ] Earthworks volumes reasonable for site area
- [ ] Areas sum to approximately site extent

### Step 4: Manual Verification and Adjustment

**Verify and adjust automated extractions:**

**Adjustment factors to apply:**
- Waste factor: +5–15% depending on material (concrete +5%, piping +8%, asphalt +10%)
- Shrinkage/swell: +10–15% for fill volume (material expands when excavated, compacts when placed)
- Over-excavation allowance: +150mm typical for pipe trenches
- Embedment depths: Ensure pipe quantities include correct depth for cover requirements

**Verification checklist:**
- [ ] Units correct (m vs m² vs m³ vs No. vs ton)
- [ ] Quantities match independent calculation for key items
- [ ] All drawings at same revision used
- [ ] Overlaps and double-counting eliminated
- [ ] Spec requirements incorporated (e.g., bedding thickness, haunching)

### Step 5: BOQ Assembly

**Compile quantities into BOQ format:**

**BOQ entry structure:**
| Item | Description | Unit | Quantity | Rate (R) | Amount (R) |
|------|-------------|------|----------|----------|------------|
| 3.2 | Topsoil strip: Strip and stockpile topsoil to average depth of 150mm for re-use in landscaping areas. Area: [measurement from drawings] | m³ | — | — | — |
| 5.1.1 | HDPE SN4 pipe: 300mm nominal diameter, SN4 stiffness Class, with Class C bedding per SANS 1200 DB | m | — | — | — |

### Step 6: Cost Estimation (with unit rates)

**Apply unit rates to quantities:**

**Estimate confidence by design stage:**
| Stage | Accuracy | Typical Contingency |
|-------|----------|---------------------|
| Conceptual (Card 5-6) | ±40% | 30–40% |
| Preliminary (Card 7-8) | ±25% | 20–30% |
| IFC (Card 9-10) | ±10% | 10–15% |

**Rate sources:**
- Previous project awards (most reliable)
- Supplier/quotation data
- Published rate books (Rawlinsons, SPONS, local equivalent)
- Estimator's experience

### Step 7: Material Schedule for Procurement

**Generate material procurement schedule from BOQ:**

**Procurement schedule output:**
| Material | Quantity | Unit | Lead Time | Order By | Delivery Window | Priority |
|----------|----------|------|-----------|---------|-----------------|----------|
| 300mm HDPE SN4 pipe | — | m | 4 weeks | — | — | Medium |
| MH-1200 manholes | — | No. | 6 weeks | — | — | Medium |
| G7 sub-base material | — | m³ | 2 weeks | — | — | High |

## Success Criteria

- [ ] All BOQ categories populated with quantities
- [ ] Extraction accuracy verified by random spot-check (≥3 items)
- [ ] Units correct and consistent throughout BOQ
- [ ] Quantities traceable to specific drawing numbers and revisions
- [ ] Waste and adjustment factors applied and stated
- [ ] BOQ formatted to client/contract standard
- [ ] Material schedule generated for all long-lead items
- [ ] Cost estimate with confidence level stated

## Common Pitfalls

1. **Unit Confusion** — m vs m² vs m³ is the #1 cause of quantity errors. Always verify the unit for each BOQ line item.
2. **Double Counting** — Overlapping drawing areas or pipe networks that appear on multiple sheets can be counted twice. Check for overlaps.
3. **Missing Details** — Quantities from detail drawings (kerb returns, headwalls) are easily missed. Systematically review every drawing sheet.
4. **Not Accounting for Waste** — Raw calculated quantities are NEVER what you order. Always add waste factors appropriate to the material.
5. **Wrong Drawing Revision** — Using an old drawing revision for quantities leads to pricing the wrong work. Always confirm drawing revision.

## Cross-References

### Related Skills
- `civil-dwg-processing` — DWG extraction pipeline for quantity source data
- `civil-documentation` — BOQ is a documentation deliverable
- `civil-tender-preparation` — BOQ feeds tender documents
- `civil-design-development` — Design output drives quantities

### Related Agents
- `CE-QS-001` (deep-agents) — Primary quantity surveying agent
- `CE-DWG-001` (deep-agents) — DWG extraction support
- `CE-DOCS-001` (OpenClaw) — BOQ document assembly

## Example Usage

**Scenario:** BOQ for stormwater drainage package (5km development)

1. **Extraction:** 345m of 300mm HDPE, 220m of 450mm HDPE, 380m of 600mm HDPE, 22 manholes, 14 catch basins, 6 headwalls
2. **Adjustment:** +8% waste factor on HDPE pipe, +150mm over-excavation on trench depth, manholes counted direct from blocks
3. **BOQ:** 12 drainage line items, 6 structure line items, 3 earthwork items, total R4.8M estimated
4. **Verification:** 5 random spot-checks against manual calculation — all within 3% of BOQ quantities
5. **Procurement Schedule:** HDPE pipe 4-week lead time, manholes 6-week lead time, HDPE order placed 8 weeks before needed

## Performance Metrics

**Target Performance:**
- Extraction accuracy: >95% of quantities within ±3% of manual verification
- BOQ completeness: 100% of applicable BOQ categories populated
- Processing time: <30 minutes for full BOQ extraction from drawings
- Unit consistency: Zero unit errors in final BOQ
- Revision currency: All quantities sourced from current drawing revision