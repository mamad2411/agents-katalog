---
name: snyk-agent-scan
display_name: Snyk Agent Security Scanner
skill_id: ACU-SKILL-2143
version: 1.0.0
category: security
thread: T08
domain: security
shard_affinity:
  - Tenebris-ACIWS
layer_access:
  - L8
  - L9
  - L10
sovereignty_score: 10
governance_level: sovereign
source_repo: snyk/agent-scan
triggers:
  - snyk
  - security-scan
  - vulnerability
  - SAST
  - SCA
---

# Snyk Agent Security Scanner

## Description
Security scanning agent for detecting vulnerabilities in code and dependencies. SAST, SCA, and IaC scanning.

## Acuterium Integration
- **Thread:** T08 — ZURD
- **Shard:** Tenebris-ACIWS
- **Layers:** L8, L9, L10
- **Governance:** sovereign
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** snyk/agent-scan
- **File:** SKILL.md
- **Author:** snyk/agent-scan
