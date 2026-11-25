---
title: Hazard Identification
description: Systematic identification, categorisation, and documentation of workplace hazards across construction activities
frequency: Per work activity assessment or site inspection
success_rate: 95%
tags:
  - domainforge_ai
  - safety
  - hazard-identification
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
---

# Hazard Identification

## Overview
Systematic identification, categorisation, and documentation of workplace hazards across construction activities. Supports RAMS development, permit-to-work processes, and safety inspections. Primary agents: RAMS Review Specialist, HSE Safety Manager.

## Triggers
- New work activity planned
- Site condition change requiring reassessment
- Safety review or audit triggered
- Incident requiring additional hazard identification

## Steps
1. **Activity Analysis** → Break down the work task into individual steps
2. **Hazard Recognition** → For each step, identify energy sources, hazardous materials, environmental conditions
3. **Categorisation** → Classify each identified hazard by type: Physical, Chemical, Biological, Ergonomic, Psychosocial, Electrical, Mechanical, Radiation, Working at Height, Excavation/Trenching, Lifting/Rigging, Confined Space
4. **Documentation** → Record hazard description, location, activity, and associated tasks
5. **Validation** → Cross-reference with historical hazard databases and regulatory requirements
6. **Control Mapping** → Link each hazard to appropriate control measures from organisational control library

## Success Criteria
- All work steps analysed
- Hazards identified by type and severity
- Each hazard mapped to at least one control measure
- Hazard register updated and accessible

## Common Pitfalls
1. Missing environmental hazards (weather, atmospheric conditions)
2. Focusing only on obvious hazards while missing secondary/indirect hazards
3. Not considering adjacent activities that may introduce new hazards
4. Incomplete categorisation leading to inappropriate controls

## Cross-References
- `safety-RAMS-review/SKILL.md` — RAMS document input
- `safety-risk-assessment/SKILL.md` — Risk assessment follows hazard identification