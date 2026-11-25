---
title: Security Surveillance
description: CCTV monitoring, anomaly detection, recording management for the ConstructAI security system
frequency: Continuous monitoring
success_rate: 99%
tags:
  - domainforge_ai
  - security
  - surveillance
  - 02500_security
docs:
  - docs_construct_ai/disciplines/02500_security/agent-data/domain-knowledge/02500_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02500_security/agent-data/prompts/02500_AI-NATIVE-SECURITY-OPERATIONS-PROMPT.md
---

# Security Surveillance

## Overview
End-to-end management of CCTV monitoring, anomaly detection, recording management for site security. Primary agent: SEC-CCTV-001.

## Triggers
- Camera detects anomaly
- Motion detected in restricted zone
- Patrol coverage requires camera support
- Incident requires video review
- Recording retention review due

## Steps
1. **CCTV Monitoring** → Real-time monitoring of camera feeds with anomaly detection
2. **Alert Classification** → Review anomaly alerts and classify severity
3. **Recording Management** → Verify recordings are active and stored per retention policy
4. **Evidence Retrieval** → Retrieve video evidence for incident investigations
5. **System Health Checks** → Verify camera connectivity, storage capacity, feed quality

## Success Criteria
- All cameras operational with active recordings
- Anomaly alerts reviewed within required timeframe
- Video evidence retrievable within 5 minutes
- Recordings retained per policy requirements

## Common Pitfalls
1. Cameras offline → Regular health checks and immediate alert when cameras fail
2. Anomaly false positives → Calibrate detection algorithms over time
3. Storage capacity exceeded → Monitor capacity and extend before full

## Cross-References
- `security-incident-management/SKILL.md` — Video evidence for incident investigations
- `security-access-control/SKILL.md` — CCTV monitoring of access points