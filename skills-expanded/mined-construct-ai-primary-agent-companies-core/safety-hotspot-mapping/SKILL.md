---
title: Safety Hotspot Mapping
description: Identification and visualisation of areas with high incident frequency or hazard concentration
frequency: Monthly or per site layout change
success_rate: 90%
tags:
  - domainforge_ai
  - safety
  - hotspot-mapping
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
---

# Safety Hotspot Mapping

## Overview
Identification and visualisation of geographic areas on site where incidents and hazard concentration are above average. Primary agent: Predictive Analytics Specialist.

## Steps
1. **Data Collection** → Gather incident locations with coordinates, inspection findings by zone
2. **Geospatial Analysis** → Map incidents onto site layout and overlay zones with higher frequency
3. **Density Analysis** → Calculate incident density and identify areas exceeding the average threshold
4. **Hotspot Classification** → Classify areas as low, medium, high, or critical risk
5. **Recommendations** → Generate targeted interventions for hotspot areas
6. **Reporting** → Create visual hotspot maps for management review

## Success Criteria
- Hotspots accurately reflect incident patterns
- Maps clear and actionable for site teams
- Targeted interventions reduce hotspot risk

## Common Pitfalls
1. Small area of data → Insufficient incidents for reliable hotspot identification
2. Changing site layout → Hotspots become invalid when work moves
3. Ignoring context → Not considering work activity density in hotspot analysis

## Cross-References
- `safety-incident-tracking/SKILL.md` — Incident location data
- `safety-predictive-risk/SKILL.md` — Predictive analytics input