---
name: copilot-terraform-azurerm-set-diff-analyzer
display_name: Terraform Azurerm Set Diff Analyzer
skill_id: ACU-SKILL-1998
version: 1.0.0
category: cloud-azure
thread: T13
domain: infrastructure
shard_affinity:
  - Marel
layer_access:
  - L5
  - L6
  - L7
sovereignty_score: 8
governance_level: restricted
source_repo: github/awesome-copilot
triggers:

---

# Terraform Azurerm Set Diff Analyzer

## Description
Analyze Terraform plan JSON output for AzureRM Provider to distinguish between false-positive diffs (order-only changes in Set-type attributes) and actual resource changes. Use when reviewing terraform plan output for Azure resources like Application Gateway, Load Balancer, Firewall, Front Door, NSG, and other resources with Set-type attributes that cause spurious diffs due to internal ordering changes.

## Acuterium Integration
- **Thread:** T13 — ACAI V2
- **Shard:** Marel
- **Layers:** L5, L6, L7
- **Governance:** restricted
- **Sovereignty Score:** 8/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/terraform-azurerm-set-diff-analyzer/SKILL.md
- **Author:** GitHub Copilot Community
