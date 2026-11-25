---
title: Civil Design Development
description: Execute Phases 2-3 of civil engineering design workflow: conceptual design, preliminary design, and detailed design with engineering calculations and analysis
version: 1.0
frequency_percent: 85.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-design-development
gigabrain_tags: civil-engineering, design-development, conceptual-design, preliminary-design, detailed-design, calculations
openstinger_context: design-phases, phase-2-3-workflow
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_GLOSSARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/00850_AGENTS-REGISTRY-SUMMARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/prompts/00850_CIVIL-DOCUMENTATION-WORKFLOW-PROMPT.md
  - docs_construct_ai/disciplines/00850_civil-engineering/workflow_docs/main/0000_CIVIL_ENGINEERING_DESIGN_WORKFLOW.MD
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
  - civil-site-assessment
  - civil-dwg-processing
---

# Civil Design Development

## Overview

Execute Phases 2 and 3 of the 5-phase civil engineering design workflow: Conceptual Design (Phase 2), Preliminary Design (Phase 3), and transition to Detailed Design (Phase 4). Covers design options analysis, engineering calculations, model development, and preliminary documentation for stakeholder approval.

**Announce at start:** "I'm using the civil-design-development skill to progress the civil engineering design through conceptual and preliminary phases."

## When to Use This Skill

**Trigger Conditions:**
- Phase 1 (Site Assessment) completed with go/no-go decision = GO
- Conceptual design alternatives need development and comparison
- Preliminary engineering calculations required
- Design needs coordination with other disciplines
- Stakeholder approval package needs preparation

**Prerequisites:**
- Phase 1 feasibility report available and approved
- Site survey data validated and sufficient
- Geotechnical recommendations received
- Environmental constraints mapped and understood
- Budget envelope confirmed
- CE-DESIGN-001 agent or equivalent design capability available

## Step-by-Step Procedure

### Step 1: Conceptual Design — Options Development

**Generate and evaluate design alternatives:**

**Options analysis framework:**
| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Cost (capital) | 25% | Estimate with assumptions | Estimate with assumptions | Estimate with assumptions |
| Constructability | 20% | Risk rating + commentary | Risk rating + commentary | Risk rating + commentary |
| Environmental Impact | 15% | Impact rating | Impact rating | Impact rating |
| Maintainability | 10% | Access + lifecycle rating | Access + lifecycle rating | Access + lifecycle rating |
| Regulatory Compliance | 15% | Compliance gaps listed | Compliance gaps listed | Compliance gaps listed |
| Schedule Impact | 10% | Duration estimate | Duration estimate | Duration estimate |
| Risk Level | 5% | Risk score | Risk score | Risk score |

**Minimum 3 options to develop:**
1. **Base case:** Conventional, proven approach with lowest risk
2. **Optimized case:** Cost/schedule optimized with moderate risk
3. **Innovative case:** Novel approach with higher risk but potential benefits

**Decision deliverables:**
- [ ] Options comparison matrix with weighted scores
- [ ] Preliminary layout sketches for each option
- [ ] Risk register with option-specific risks
- [ ] Recommendation report with justified preferred option

### Step 2: Preliminary Design — Engineering Analysis

**Develop detailed engineering analysis for the selected option:**

**Analysis categories by design element:**

**Roads and Access:**
- Horizontal alignment (curves, transition, superelevation)
- Vertical alignment (gradients, vertical curves, sight distance)
- Cross-section (lanes, shoulders, cross-fall, drainage)
- Pavement design (CBR-based, traffic loading, layer thickness)

**Drainage Systems:**
- Catchment delineation and area calculation
- Time of concentration for each sub-catchment
- Rational Method peak discharge calculation (Q = CiA)
- Preliminary pipe sizing using Manning's equation
- Detention basin sizing (if downstream capacity limited)
- Open channel design (velocity, depth, freeboard)

**Earthworks:**
- Cut/fill volume calculation (average end area method)
- Mass haul diagram for earthwork balance
- Borrow disposal assessment
- Slope stability preliminary analysis

**Retaining Structures:**
- Retaining wall type selection (gravity, cantilever, MSE)
- Preliminary sizing based on wall height and soil parameters
- Stability checks (overturning, sliding, bearing)

**Water Supply and Sewer:**
- Demand calculation based on population/use
- Pipe sizing for water supply (velocity 0.6–3.0 m/s)
- Gravity sewer sizing (self-cleansing velocity ≥ 0.6 m/s)
- Pump station requirements (if gravity not feasible)

### Step 3: Multi-Discipline Coordination

**Identify and resolve interfaces with other disciplines:**

**Coordination checklist:**
| Discipline | Interface Point | Resolution Action |
|------------|-----------------|-------------------|
| Structural | Foundation loads, basement walls, column positions | Verify bearing capacity vs. structural loads; coordinate column grid with road/driveway alignment |
| MEP/Services | Underground routing, manhole positions, penetration locations | Coordinate utility corridors; ensure drainage inverts clear foundation zones |
| Architectural | Building entrances, landscape integration, sightlines | Verify access grades meet architectural intent; coordinate hardscape/softscape boundaries |
| Geotechnical | Foundation type, excavation support, ground improvement | Confirm preliminary foundation type matches geotechnical recommendations |
| Environmental | Water quality treatment, erosion control, habitat offsets | Verify SuDS design meets environmental requirements; confirm erosion control measures |
| Transportation | Traffic signals, road connections, pedestrian links | Verify geometric design matches transportation model |

### Step 4: Cost Estimation and Value Engineering

**Develop preliminary cost estimate and identify value engineering opportunities:**

**Estimate structure:**
| Cost Category | Unit | Quantity | Unit Rate | Total | Confidence |
|---------------|------|----------|-----------|-------|------------|
| Earthworks | m³ | — | — | — | ±30% |
| Pavement | m² | — | — | — | ±25% |
| Drainage pipes | m | — | — | — | ±30% |
| Structures | No. | — | — | — | ±35% |
| Water/Sewer | m | — | — | — | ±35% |
| Landscaping | m² | — | — | — | ±40% |
| Contingency | % | — | — | — | 15–25% |

**Value engineering opportunities to explore:**
- Material substitution (e.g., HDPE vs. concrete pipe)
- Construction method optimization
- Phasing alternatives
- Standard vs. custom element trade-offs
- Life-cycle cost comparison (initial capital vs. maintenance)

### Step 5: Preliminary Documentation Package

**Prepare documentation for stakeholder review and approval:**

**Required deliverables:**
1. **Design Basis Report:** Assumptions, standards, codes, data sources
2. **Preliminary Drawings:** Site plan, road layout, drainage layout, profiles, cross-sections
3. **Calculations Summary:** Key engineering calculations for roads, drainage, earthworks
4. **Cost Estimate:** Bill of quantities with unit rates and confidence level
5. **Risk Register:** Updated with design-phase risks and mitigations
6. **Environmental Management Plan:** Construction and operational environmental controls
7. **Program/Timeline:** Construction schedule with critical path
8. **Stakeholder Presentation:** Non-technical summary for community/client review

**Quality checks before issue:**
- [ ] All drawings cross-referenced and consistent with calculations
- [ ] Quantities in BOQ match drawing take-offs
- [ ] Drawings have revision control and issue status
- [ ] Calculations reference applicable codes and standards
- [ ] Assumptions clearly stated and justified
- [ ] Design meets all regulatory requirements from Phase 1 compliance matrix

## Success Criteria

- [ ] Minimum 3 design options developed and compared
- [ ] Multi-criteria decision matrix with weighted scores completed
- [ ] Preferred option selected with justification
- [ ] All engineering calculations completed and checked
- [ ] Multi-discipline coordination done (no major clashes at preliminary stage)
- [ ] Cost estimate within ±30% accuracy (preliminary standard)
- [ ] Preliminary drawings issued for stakeholder review
- [ ] Risk register updated with design-phase risks
- [ ] Environmental management plan included

## Common Pitfalls

1. **Jumping to Single Option** — Never develop only one design option. Minimum 3 alternatives with documented trade-offs are required before selection.
2. **Skipping Value Engineering** — Value engineering at the preliminary stage can save 10–30% of capital cost. Don't skip it to meet schedule pressure.
3. **Ignoring Buildability** — A design that cannot be built safely or economically is worthless. Always consider construction methodology and access.
4. **Not Coordinating with Other Disciplines** — Civil design interfaces with every other discipline. Uncoordinated designs cause expensive changes later.
5. **Using Code Minimums Only** — Codes define the minimum acceptable. Best practice often exceeds code minimums for durability, maintainability, and safety.
6. **Omitting Sensitivity Analysis** — Key parameters (traffic volume, rainfall intensity, soil bearing) have uncertainty. Show how the design performs under variation.

## Cross-References

### Related Skills
- `civil-site-assessment` — Phase 1 input feeds design development
- `civil-documentation` — Design output feeds documentation package
- `civil-dwg-processing` — Process design drawings for extraction
- `civil-quality-assurance` — Design review and compliance checking
- `pre-task-assessment-readiness` — Assess data readiness before starting

### Related Agents
- `CE-DESIGN-001` (OpenClaw) — Primary design development agent
- `CE-STRUCT-001` (deep-agents) — Structural analysis support
- `CE-HYDRO-001` (deep-agents) — Hydraulic analysis and pipe sizing
- `CE-GEO-001` (deep-agents) — Geotechnical design support
- `CE-TRAFFIC-001` (deep-agents) — Traffic flow analysis
- `CE-QA-001` (OpenClaw) — Design quality validation

## Example Usage

**Scenario:** Preliminary design for a 1.2 km subdivision road with stormwater drainage

1. **Options:** Developed 3 options for road alignment — Option A (direct, max cut/fill), Option B (contour-following, minimal earthworks), Option C (hybrid, optimal balance). Weighted score: Option C selected at 78/100.
2. **Road Design:** Horizontal: 2x reverse curves (R=200m), 6% cross-fall superelevation. Vertical: 3.5% max gradient, 2% min gradient, 800m crest VC for 150m sight distance. Pavement: CBR 8%, 350,000 ESALs → 40mm AC wearing + 150mm G5 base + 200mm G7 sub-base.
3. **Drainage:** 6 sub-catchments (0.8–3.2 ha), CiA method, 5–20 year return periods. Pipe network: 12 pipes (300–600mm HDPE), gradients 0.3–2.0%, velocities 0.8–2.5 m/s. Detention basin: 850m³ storage volume for 1:20 year event.
4. **Coordination:** Structural column at Grid C3 conflicts with drainage MH-04 — resolved by relocating MH-04 3m south.
5. **Cost Estimate:** R18.2M ±30% for all civil works (roads + drainage + water + sewer + electricity conduits).
6. **Output:** 8 preliminary drawings issued for client + municipal review.

## Performance Metrics

**Target Performance:**
- Options analysis: ≥3 options with ≥5 criteria each
- Calculation completeness: All 5 design elements analyzed (roads, drainage, earthworks, retaining, utilities)
- Coordination: Zero major clashes remaining at preliminary design review
- Cost accuracy: Preliminary estimate within ±30% of tender price
- Schedule: Preliminary design completed within 4–8 weeks of Phase 1 approval