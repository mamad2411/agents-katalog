---
title: Safety Alert System
description: Management of safety alert generation, distribution, escalation, and tracking
frequency: Per safety event
success_rate: 98%
tags:
  - domainforge_ai
  - safety
  - alert-system
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
---

# Safety Alert System

## Overview
End-to-end management of safety alerts including generation, distribution, escalation, acknowledgment, and closure. Covers automatic alerts from PPE-detection, hazard-detection, sensor-integration, incident reports, and manual alert generation. Primary agents: HSE Safety Manager, CV/IoT Integration Specialist.

## Triggers
- PPE-detection violation identified
- Hazard-detection event
- Sensor threshold exceeded
- Incident reported
- Inspection finding classified as major
- Manual alert generation by user

## Steps
1. **Alert Generation** → Create alert from trigger with severity and location
2. **Alert Classification** → Classify severity: Information, Warning, Critical, Emergency
3. **Distribution** → Send to appropriate recipients based on severity and type
4. **Acknowledgment Tracking** → Track which recipients have acknowledged
5. **Escalation** → Escalate if not acknowledged within time thresholds
6. **Resolution & Closure** → Verify alert condition resolved, document closure

## Success Criteria
- Alerts generated for all trigger events
- Correct recipients receive correct alerts
- Escalation occurs when acknowledgment not received
- Alerts resolved and documented

## Common Pitfalls
1. Alert fatigue → Too many minor alerts cause important alerts to be ignored
2. Incorrect recipients → Wrong people receive alerts
3. No resolution → Alerts acknowledged but action not taken

## Cross-References
- `safety-PPE-detection/SKILL.md` — PPE violation alerts
- `safety-hazard-detection/SKILL.md` — Hazard detection alerts
- `safety-sensor-integration/SKILL.md` — Sensor threshold alerts