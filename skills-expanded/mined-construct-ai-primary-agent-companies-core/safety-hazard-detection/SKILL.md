---
title: Safety Hazard Detection
description: Computer vision-based detection of physical safety hazards on construction sites from camera feeds
frequency: Per camera frame or request
success_rate: 90%
tags:
  - domainforge_ai
  - safety
  - hazard-detection
  - computer-vision
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
---

# Safety Hazard Detection

## Overview
Computer vision-based detection of physical safety hazards on construction sites including open edges, unguarded openings, unshored excavations, blocked access routes, unsafe scaffolding, fire hazards, and hazardous material exposures. Primary agent: CV/IoT Integration Specialist.

## Steps
1. **Image Preprocessing** → Prepare camera frame or photo for analysis
2. **Scene Understanding** → Identify the environment type and current work activities
3. **Hazard Detection** → Analyse for hazards: open edges without protection, unguarded openings, unshored excavations, blocked access or egress routes, unsafe scaffolding, fire hazards, hazardous material exposures, falling object risks
4. **Severity Assessment** → Classify hazard severity: Low, Moderate, High, Critical
5. **Location Tagging** → Record hazard location relative to camera and coordinates if known
6. **Alert Generation** → Generate immediate alert for high or critical hazards
7. **Documentation** → Log hazard with evidence photograph for follow-up

## Success Criteria
- Hazard detection accuracy > 90% for defined hazard types
- Classification matches actual hazard severity
- Alerts generated for serious hazards without delay
- All detections documented with evidence

## Common Pitfalls
1. Similar objects → Temporary materials confused with hazards
2. Transient conditions → Temporary conditions detected as hazards
3. Camera coverage → Hazards in blind spots not detected

## Cross-References
- `safety-PPE-detection/SKILL.md` — PPE compliance detection
- `safety-alert-system/SKILL.md` — Alert generation