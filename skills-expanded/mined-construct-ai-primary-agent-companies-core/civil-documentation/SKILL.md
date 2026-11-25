---
title: Civil Documentation
description: Generate and manage civil engineering technical documentation including SOWs, specifications, ITPs, drawings, calculations, and contract annexures
version: 1.0
frequency_percent: 85.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-documentation
gigabrain_tags: civil-engineering, documentation, sow, specifications, itp, calculations, drawings, contract-annexures
openstinger_context: technical-documentation, phase-4-workflow
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_GLOSSARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/00850_AGENTS-REGISTRY-SUMMARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/prompts/00850_CIVIL-DOCUMENTATION-WORKFLOW-PROMPT.md
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
  - civil-design-development
  - sop-generation
---

# Civil Documentation

## Overview

Generate and manage the complete suite of civil engineering technical documentation: Scope of Work (SOW), technical specifications, construction drawings, calculation packages, inspection and test plans (ITPs), and contract annexures. Ensures all documentation meets applicable standards, is internally consistent, and ready for tender or construction issue.

**Announce at start:** "I'm using the civil-documentation skill to generate technical documentation for the civil engineering project."

## When to Use This Skill

**Trigger Conditions:**
- Design development (Phases 2-3) completed and approved
- Tender documentation package needs compilation
- Construction drawings and specifications need preparation
- ITPs need development for quality control
- Contract annexures need assembly
- SOW needs generation for subcontracting

**Prerequisites:**
- Preliminary design approved by stakeholder
- All engineering calculations completed and verified
- Geotechnical recommendations confirmed
- Multi-discipline coordination with no outstanding clashes
- CE-DOCS-001 agent or equivalent documentation capability available
- Document templates available for the project type

## Step-by-Step Procedure

### Step 1: Document Types Identification

**Identify all required documentation for the project scope:**

**Documentation categories:**
| Category | Documents | Issue Stage |
|----------|-----------|-------------|
| Scope of Work | SOW document, Scope delineations | Tender |
| Drawings | General arrangement, detailed design, profiles, cross-sections | Tender/IFC |
| Specifications | Technical specs, material specs, workmanship requirements | Tender |
| Calculations | Design calcs, hydraulic calcs, structural calcs | Review |
| ITPs | Inspection and test plans, hold point schedules | Construction |
| BOQ | Bill of quantities, schedule of rates | Tender |
| Annexures | Technical annexures, commercial annexures, admin annexures | Contract |

Generate a document register listing all required items with status, responsible party, and due date.

### Step 2: Scope of Work (SOW) Development

**Structure the SOW for civil engineering scope:**

**SOW Template Structure:**
```
1. Introduction and Project Overview
   1.1 Project Background
   1.2 Scope Boundaries and Exclusions
   1.3 Key Deliverables and Milestones
   1.4 Assumptions and Constraints

2. Technical Scope
   2.1 Earthworks and Site Preparation
   2.2 Roads, Pavements, and Access
   2.3 Stormwater Drainage Systems
   2.4 Water Supply and Sewer Reticulation
   2.5 Retaining Structures and Earthworks
   2.6 Landscaping and Site Works
   2.7 Interface with Other Disciplines

3. Performance Criteria
   3.1 Design Standards and Codes
   3.2 Material Specifications
   3.3 Quality Requirements
   3.4 Testing and Acceptance Criteria
   3.5 Environmental and Sustainability Requirements

4. Deliverables Schedule
   4.1 Document Delivery Milestones
   4.2 Construction Phase Gates
   4.3 Review and Approval Timelines
   4.4 Handover Requirements

5. Commercial Terms
   5.1 Pricing Schedule and Basis
   5.2 Payment Terms and Milestones
   5.3 Variation Procedures
   5.4 Liquidated Damages / Performance Incentives

6. Appendices
   Appendix A: Drawings List and Revisions
   Appendix B: Specifications
   Appendix C: ITPs
   Appendix D: BOQ/Schedule of Rates
   Appendix E: Contract Conditions
   Appendix F: Safety Plan Reference
```

### Step 3: Technical Specifications Development

**Develop discipline-specific specifications:**

**Specification sections for civil engineering:**
| Section | Content | Standard Reference |
|---------|---------|-------------------|
| Earthworks | Site clearance, excavation, backfill, compaction | SANS 1200 DB, ASTM standards |
| Pavements | Sub-base, base course, wearing course | AASHTO, TG1/TG2 |
| Drainage | Pipe networks, structures, SuDS | EN 752, CIRIA guidelines |
| Structural Concrete | Formwork, reinforcement, placing, curing | EN 206, ACI 318 |
| Structural Steel | Fabrication, erection, protection | EN 1993, AISC 360 |
| Landscaping | Topsoil, planting, irrigation | LANDSA standards |
| Testing | Materials testing, field testing | ASTM, SANS testing standards |

**Each specification section must include:**
- Scope and extent of work
- Reference standards and codes
- Materials requirements
- Workmanship and installation requirements
- Testing and acceptance criteria
- Submittals required (samples, test reports, shop drawings)
- Measurement and payment basis

### Step 4: Construction Drawings Preparation

**Organize and prepare construction drawing set:**

**Drawing register format:**
| Drawing No. | Title | Revision | Status | Discipline | Date |
|-------------|-------|----------|--------|------------|------|
| CE-0001-00 | General Site Plan | C | IFC | Civil | 2026-03-31 |
| CE-0001-01 | Road Horizontal Alignment | C | IFC | Civil | 2026-03-31 |
| CE-0001-02 | Road Vertical Profiles | C | IFC | Civil | 2026-03-31 |
| CE-0001-03 | Road Cross-Sections | C | IFC | Civil | 2026-03-31 |
| CE-0002-00 | Stormwater Drainage Layout | C | IFC | Civil | 2026-03-31 |
| CE-0002-01 | Stormwater Profiles | C | IFC | Civil | 2026-03-31 |
| CE-0003-00 | Water/Sewer Reticulation | C | IFC | Civil | 2026-03-31 |
| CE-0004-00 | Earthworks Plan | C | IFC | Civil | 2026-03-31 |
| CE-0004-01 | Cut/Fill Quantities | C | IFC | Civil | 2026-03-31 |

**Drawing quality checklist:**
- [ ] Title block complete with project info, drawing no., revision, scale
- [ ] Drawing scale appropriate for content (1:500 site, 1:100 details)
- [ ] North point, scale bar, coordinate system shown
- [ ] Dimensions complete, clear, non-conflicting
- [ ] Annotations legible at print size
- [ ] Cross-references to other drawings accurate
- [ ] Drawing revision clouded with revision history
- [ ] Drawings signed/stamped by responsible engineer

### Step 5: Calculation Package Assembly

**Compile and organize engineering calculations:**

**Calculation package structure:**
1. Design Basis (codes, loads, materials, assumptions)
2. Hydrological Calculations (catchment areas, CiA peak discharge, time of concentration)
3. Hydraulic Calculations (Manning's pipe sizing, detention volumes)
4. Pavement Design Calculations (CBR analysis, ESALs, layer thickness)
5. Earthworks Quantities (cross-section areas, volumes, balance)
6. Structural Calculations (retaining walls, foundations, load paths)
7. Software Input/Output (printouts from modeling software with validation notes)

**Calculation quality rules:**
- [ ] All calculations signed by originator and checker
- [ ] Input data source referenced
- [ ] Formula or method stated
- [ ] Safety factors explicitly shown
- [ ] Results checked against reasonableness bounds
- [ ] Software calculations verified by hand-check for 1 representative case
- [ ] Units consistent throughout

### Step 6: ITP (Inspection & Test Plan) Development

**Develop ITPs for all civil engineering construction activities:**

**ITP structure:**
| Activity | Inspection/Test | Hold/Witness | Reference | Responsibility |
|----------|-----------------|--------------|-----------|----------------|
| Site clearance | Visual inspection of extent | Witness (W) | Spec Sec 3.1 | Contractor |
| Earthworks compaction | Nuclear density test (95% MOD AASHTO) | Hold (H) | Spec Sec 3.4 | QA/QC |
| Pipe bedding | Granular material inspection + compaction test | W | Spec Sec 5.2 | Contractor |
| Pipe installation | Line, level, alignment check | W | EN 1610 | Contractor |
| Watertightness test | Exfiltration test per pipe run | H | Spec Sec 5.5 | QA/QC |
| Concrete pour | Slump test, cube sampling, temperature | H | EN 206 | QA/QC |
| Backfill compaction | Density test every 300mm lift | W | Spec Sec 3.4 | Contractor |
| Pavement layers | Thickness, density, smoothness | H | Spec Sec 4.3 | QA/QC |

**Hold vs. Witness rules:**
- **Hold Point (H):** Work MUST STOP until inspection completed and approved. Work may not proceed.
- **Witness Point (W):** Inspection must be notified. Contractor may proceed if inspector does not attend within specified time.

### Step 7: Contract Annexures Assembly

**Compile technical, commercial, and administrative annexures:**

**Annexure checklist:**
- [ ] Technical Annexure T1: Scope of Work
- [ ] Technical Annexure T2: Drawings List
- [ ] Technical Annexure T3: Specifications
- [ ] Technical Annexure T4: Calculation Package
- [ ] Technical Annexure T5: ITPs
- [ ] Commercial Annexure C1: Pricing Schedule / BOQ
- [ ] Commercial Annexure C2: Payment Milestones
- [ ] Commercial Annexure C3: Variation Procedures
- [ ] Administrative Annexure A1: HSE Plan Requirements
- [ ] Administrative Annexure A2: Quality Assurance Requirements
- [ ] Administrative Annexure A3: Programme Requirements
- [ ] Administrative Annexure A4: Document Submittal Procedures

### Step 8: Final Quality Review

**Conduct comprehensive documentation review before issue:**

**Review checklist:**
- [ ] All SOW sections completed, no blank templates
- [ ] Drawings cross-referenced to specifications (spec section matches drawing)
- [ ] BOQ quantities match drawing take-offs
- [ ] ITP hold/ witness points aligned with specification requirements
- [ ] Calculation package internally consistent
- [ ] Annexures cross-referenced correctly
- [ ] Document revision control applied
- [ ] Document formatting consistent
- [ ] All drawings signed/stamped
- [ ] Calculations signed by responsible engineer
- [ ] Compliance matrix verified against Phase 1 regulatory requirements

## Success Criteria

- [ ] Complete SOW document with no blank template fields
- [ ] All applicable specifications developed for project scope
- [ ] Drawing set complete with no missing sheets
- [ ] BOQ quantities match drawing take-offs within ±5%
- [ ] All ITPs completed with hold/witness points specified
- [ ] Calculation package complete and signed
- [ ] All 12 annexure items compiled
- [ ] Final quality review checklist completed
- [ ] Compliance with Phase 1 regulatory requirements verified

## Common Pitfalls

1. **Blank Template Fields** — Never issue SOW or specifications with placeholder text left in. Replace ALL examples with project-specific content.
2. **Drawing-Spec Mismatch** — Drawings show 300mm pipe, spec says 400mm. Always cross-reference specifications to drawings before issue.
3. **Missing ITP Points** — If the specification requires a test (e.g., pipe watertightness), the ITP must include it as a hold or witness point. Omitting ITP points creates quality gaps.
4. **Calculation Gaps** — Every design parameter used in drawings must have a calculation trail. If you can't show how a pipe size was determined, it's a gap.
5. **Incomplete Annexures** — BOQ missing items, incomplete specifications linked to annexures. Walk through each annexure as if you're the contractor: "Can I price this? Do I know what's required?"
6. **Version Control Failures** — Issuing Rev B drawings with Rev A spec. All documents must be at the same revision at issue.

## Cross-References

### Related Skills
- `civil-design-development` — Design output feeds documentation
- `civil-quality-assurance` — Documentation review and compliance
- `sow-generation` — General SOW generation framework
- `civil-dwg-processing` — Drawing extraction and validation
- `pre-task-assessment-readiness` — Assess readiness before starting

### Related Agents
- `CE-DOCS-001` (OpenClaw) — Primary documentation agent
- `CE-LIB-001` (OpenClaw) — Document organization and version control
- `CE-PROMPT-001` (OpenClaw) — Template optimization
- `CE-QA-001` (OpenClaw) — Documentation quality validation

## Example Usage

**Scenario:** Compile tender documentation package for stormwater drainage works

1. **SOW:** Generated 28-page SOW covering pipe installation, manhole construction, headwalls, detention basin, and erosion control during construction.
2. **Specifications:** Technical specs for HDPE pipe (SN4 and SN8 class), concrete manholes (Type A, B, C), rip-rap headwalls, geotextile under rip-rap, topsoil and seeding for disturbed areas.
3. **Drawings:** 6 drawings (layout, profiles x3, manhole details, detention basin details) — all at Rev C, signed.
4. **BOQ:** 42 line items totaling R8.2M ±15% accuracy.
5. **ITPs:** 5 ITPs covering pipe installation, manhole construction, concrete works, earthworks, and landscaping.
6. **Calculations:** Hydrological + hydraulic calcs showing pipe sizing rationale, detention volume calculation.
7. **Annexures:** All annexures T1-T5, C1-C3, A1-A4 compiled into single tender document.
8. **Review:** Complete quality checklist completed, 3 minor observations corrected before issue for tender.

## Performance Metrics

**Target Performance:**
- Documentation completeness: 100% of required documents produced
- Cross-reference accuracy: Zero mismatches between drawings and specs
- BOQ accuracy: Within ±10% of actual awarded quantities
- Review cycle time: <1 week per major review cycle
- Error rate: <2% of documents require correction after approval