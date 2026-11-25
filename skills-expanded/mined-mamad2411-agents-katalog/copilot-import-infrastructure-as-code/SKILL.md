---
name: copilot-import-infrastructure-as-code
display_name: Import Infrastructure As Code
skill_id: ACU-SKILL-1913
version: 1.0.0
category: malware
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
source_repo: github/awesome-copilot
triggers:

---

# Import Infrastructure As Code

## Description
Import existing Azure resources into Terraform using Azure CLI discovery and Azure Verified Modules (AVM). Use when asked to reverse-engineer live Azure infrastructure, generate Infrastructure as Code from existing subscriptions/resource groups/resource IDs, map dependencies, derive exact import addresses from downloaded module source, prevent configuration drift, and produce AVM-based Terraform files ready for validation and planning across any Azure resource type.

## Acuterium Integration
- **Thread:** T08 — ZURD
- **Shard:** Tenebris-ACIWS
- **Layers:** L8, L9, L10
- **Governance:** sovereign
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/import-infrastructure-as-code/SKILL.md
- **Author:** GitHub Copilot Community
