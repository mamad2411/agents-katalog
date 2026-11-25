---
title: PPE Detection
description: Computer vision-based detection and classification of personal protective equipment compliance on construction sites
frequency: Per camera frame or request
success_rate: 95%
tags:
  - domainforge_ai
  - safety
  - PPE-detection
  - computer-vision
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
---

# PPE Detection

## Overview
Computer vision-based detection and classification of personal protective equipment compliance on construction sites. Analyses video feeds or photographs to identify persons and check PPE against organisational requirements. Primary agent: CV/IoT Integration Specialist.

## Steps
1. **Image Preprocessing** → Prepare camera frame or photo: resize, normalise, enhance
2. **Person Detection** → Identify all persons in the image using object detection model
3. **PPE Analysis** → For each detected person, analyse: hard hat (on/off), high-vis vest (on/off), safety boots (on/off), eye protection, hearing protection, gloves, fall protection
4. **Compliance Assessment** → Compare detected PPE against required PPE for the zone or activity
5. **Violation Documentation** → Document any violations with person location, timestamp, missing PPE
6. **Alert Generation** → Generate real-time alert for serious or immediate danger violations
7. **Data Logging** → Log all PPE detection results for trend analysis

## Success Criteria
- Detection accuracy > 90% for each PPE type in good conditions
- False positive rate < 5%
- Violations documented with evidence
- Real-time alerts generated for serious violations

## Common Pitfalls
1. Poor lighting conditions → Affects detection accuracy
2. Occlusion → PPE partially obscured or person blocked
3. Camera angle → PPE not visible from certain angles
4. Similar objects → Non-PPE objects confused with PPE

## Cross-References
- `safety-hazard-detection/SKILL.md` — Hazard detection companion
- `safety-alert-system/SKILL.md` — Alert generation