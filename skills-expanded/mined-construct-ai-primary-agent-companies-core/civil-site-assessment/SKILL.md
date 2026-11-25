---
title: Civil Site Assessment
description: Execute Phase 1 civil engineering site assessment workflow covering project brief, site survey, geotechnical investigation, and environmental constraints
version: 1.0
frequency_percent: 90.0
success_rate_percent: 95.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-site-assessment
gigabrain_tags: civil-engineering, site-assessment, survey, geotechnical, environmental, feasibility, phase-1
openstinger_context: site-feasibility, phase-1-workflow
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
  - civil-dwg-processing
---

# Civil Site Assessment

## Overview

Execute Phase 1 of the 5-phase civil engineering design workflow: Site Assessment & Requirements. This covers project brief analysis, site survey data collection, geotechnical investigation integration, and environmental constraint mapping to establish a comprehensive foundation for all subsequent design decisions.

**Announce at start:** "I'm using the civil-site-assessment skill to conduct Phase 1 site evaluation for the civil engineering project."

## When to Use This Skill

**Trigger Conditions:**
- New civil engineering project requiring site feasibility assessment
- Phase 1 of the 5-phase design workflow needs execution
- Site data needs to be collected and validated for design input
- Client requirements need to be translated into engineering parameters
- Environmental and regulatory constraints need identification

**Prerequisites:**
- Project brief or client requirements document available
- Site location identified (coordinates, boundaries, address)
- Access to survey data or GIS mapping tools
- CE-SITE-001 agent or equivalent site assessment capability
- Preliminary budget and timeline constraints defined

## Step-by-Step Procedure

### Step 1: Project Brief Analysis

**Extract and structure project requirements:**
1. Review project objectives, scope, and constraints
2. Identify deliverables and success criteria
3. Extract key parameters:
   - Site area and boundaries
   - Intended use and capacity requirements
   - Budget envelope and timeline
   - Stakeholder list and their requirements
4. Map requirements to regulatory frameworks

**Output:** Structured project brief with engineering parameters

### Step 2: Site Survey Data Integration

**Process and validate available site data:**

**Required survey data:**
- Topographic survey (contours at 0.5m intervals minimum)
- Site boundaries and legal survey markers
- Existing infrastructure locations (roads, utilities, structures)
- Natural features (watercourses, vegetation, rock outcrops)
- Access points and existing easements

**Data sources (in priority order):**
1. Recent professional topographic survey (< 12 months old)
2. RTK GPS field survey data
3. Drone photogrammetry with ground control
4. Satellite imagery + GIS analysis (preliminary only)

**Validation checks:**
- [ ] Survey date within acceptable timeframe
- [ ] Coordinate system matches project requirements
- [ ] Contour intervals sufficient for design purpose
- [ ] Benchmark/TPM locations documented
- [ ] Survey accuracy stated and acceptable

**If survey data is insufficient:** Commission new survey, flag specific deficiencies.

### Step 3: Geotechnical Investigation Assessment

**Evaluate existing geotechnical data or commission new investigation:**

**Required geotechnical data:**
- Borehole locations and logs (minimum 1 per 500m² for preliminary)
- Soil classification per layer
- Groundwater table depth and seasonal variation
- Bearing capacity estimates
- Settlement potential assessment
- Recommended foundation type

**Assessment checklist:**
- [ ] Number of boreholes adequate for site size
- [ ] Borehole depth sufficient for anticipated loads
- [ ] Laboratory test results available
- [ ] Groundwater data included
- [ ] Geotechnical report with recommendations provided

**If geotechnical data is insufficient:** Scope geotechnical investigation, specify borehole locations and depths, identify specialist.

### Step 4: Environmental Constraints Mapping

**Identify and document environmental constraints:**

**Constraint categories:**
| Category | Data Required | Source |
|----------|---------------|--------|
| Flood Risk | Flood zone classification, return period, design flood level | Municipal flood maps, hydrological study |
| Protected Habitats | Protected species, wetlands, conservation areas | Environmental registry, ecological survey |
| Contamination | Historical land use, contamination assessment | Phase 1 ESA, site history records |
| Heritage | Heritage sites, archaeological features | Heritage registry, cultural survey |
| Erosion Risk | Slope stability, soil erosion potential | Site inspection, geotechnical report |
| Noise/Air Quality | Ambient conditions, nearby sensitive receptors | Baseline monitoring, municipal data |

**Output:** Environmental constraint map with overlay analysis

### Step 5: Regulatory Compliance Matrix

**Identify all applicable regulations and approval requirements:**

| Regulatory Area | Applicable Requirements | Approval Authority | Timeline |
|-----------------|------------------------|-------------------|----------|
| Zoning | Permitted uses, density, height, setbacks | Municipal planning | 2–6 months |
| Building Code | Structural, fire, accessibility standards | Building control | 1–3 months |
| Environmental | EIA, water use license, waste management | Environmental authority | 3–12 months |
| Transportation | Road connections, traffic impact | Roads authority | 1–6 months |
| Water/Sewer | Water rights, discharge permits | Water utility | 1–6 months |

### Step 6: Feasibility Assessment Report

**Compile comprehensive site feasibility assessment:**

**Report structure:**
1. Executive summary with go/no-go recommendation
2. Site description and location analysis
3. Topographic conditions and constraints
4. Geotechnical conditions and foundation recommendations
5. Environmental constraints and mitigation requirements
6. Regulatory approval requirements and timeline
7. Access and infrastructure availability
8. Preliminary layout options
9. Risk register with probability and impact ratings
10. Cost implications and order-of-magnitude estimate

**Go/No-Go Decision Framework:**
| Factor | Green (Proceed) | Amber (Investigate) | Red (Stop) |
|--------|-----------------|---------------------|------------|
| Geotechnical | Bearing capacity > 150 kPa | Bearing capacity 100–150 kPa | Bearing capacity < 100 kPa, deep foundation required |
| Flood Risk | Outside 1% flood zone | Edge of flood zone | Within 1% flood zone, no viable mitigation |
| Environmental | No protected features | Mitigatable impacts | Protected habitat on 50%+ of site |
| Access | Existing adequate access | Minor upgrades needed | No feasible access solution |
| Regulatory | All approvals achievable | Long approval timeline (>12 months) | Prohibited use |

## Success Criteria

- [ ] Project brief translated to clear engineering parameters
- [ ] Topographic survey data validated and sufficient for preliminary design
- [ ] Geotechnical conditions assessed or investigation scoped
- [ ] All environmental constraints identified and mapped
- [ ] Regulatory compliance matrix complete with timeline
- [ ] Feasibility report with clear go/no-go recommendation
- [ ] Risk register with probability and impact ratings
- [ ] Cost estimate with stated assumptions and confidence level

## Common Pitfalls

1. **Using Outdated Survey Data** — Site conditions change. Always verify survey date and check for recent development. If survey is >12 months old, commission a spot-check survey.
2. **Assuming Uniform Soil Conditions** — Soil conditions can vary significantly across a site. Ensure boreholes are distributed to cover all areas of development.
3. **Missing Heritage Constraints** — Heritage designations can halt a project entirely. Always check heritage registries early before any site works.
4. **Underestimating Approval Timelines** — Environmental approvals for complex sites can take 12+ months. Build realistic timelines into project program.
5. **Ignoring Seasonal Conditions** — Groundwater levels, flood risk, and accessibility can change seasonally. Account for worst-case seasonal scenarios.

## Cross-References

### Related Skills
- `civil-dwg-processing` — Process survey DWG files and topographic data
- `civil-design-development` — Feasibility output feeds Phase 2 design
- `pre-task-assessment-readiness` — Assess data readiness before starting

### Related Agents
- `CE-SITE-001` (OpenClaw) — Primary site assessment agent
- `CE-GEO-001` (deep-agents) — Geotechnical analysis support
- `CE-GIS-001` (deep-agents) — Spatial analysis and constraint mapping
- `CE-FIELD-001` (OpenClaw) — Mobile field data collection
- `CE-ENV-001` (deep-agents) — Environmental impact assessment

## Example Usage

**Scenario:** Assess a 2.5-hectare site for mixed-use development on a sloping coastal location

1. **Project Brief:** 200 residential units + commercial podium, 3 basement levels, $45M budget, 24-month program
2. **Survey:** RTK topographic survey available (6 months old), 1:500 scale, 0.5m contours, 12 benchmarks
3. **Geotech:** 4 boreholes drilled (1 per 6,250m²), variable sand/clay profile, groundwater at 3–5m, bearing capacity 180–250 kPa, raft or pile foundation recommended
4. **Environment:** Site partly in 1% flood zone (southern 15%), no protected species, moderate contamination from historical filling
5. **Regulatory:** Residential use permitted in zoning, EIA required, flood study needed, water/sewer connection available at site boundary
6. **Verdict:** AMBER — Proceed with flood mitigation study and contamination assessment before detailed design

## Performance Metrics

**Target Performance:**
- Assessment completeness: All 6 checklist categories completed
- Data sufficiency: ≥90% of required data available or gaps scoped for specialist
- Risk identification: Top 10 site risks identified with mitigation strategies
- Timeline estimate: Approval timeline within ±25% of actual
- Cost estimate: Order-of-magnitude within ±40% of detailed estimate