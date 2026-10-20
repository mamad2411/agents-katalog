---
name: cspm-prowler
display_name: Cspm Prowler
skill_id: ACU-SKILL-2133
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
source_repo: Poatan222/Skills-security
triggers:

---

# Cspm Prowler

## Description
Analyze Prowler CSPM scan outputs, prioritize cloud misconfigurations by risk, and generate remediation plans with compliance mapping. Supports AWS, Azure, and GCP findings. Trigger when user uploads Prowler output files (.csv, .json, .html), mentions "Prowler", "CSPM", "cloud security posture", "cloud misconfiguration", "CIS benchmark", "cloud compliance scan", or asks about cloud security findings. Also trigger when user pastes Prowler CLI output or asks how to run Prowler against their cloud environment.


## Acuterium Integration
- **Thread:** T08 — ZURD
- **Shard:** Tenebris-ACIWS
- **Layers:** L8, L9, L10
- **Governance:** sovereign
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** Poatan222/Skills-security
- **File:** cspm-prowler/SKILL.md
- **Author:** Poatan222/Skills-security
