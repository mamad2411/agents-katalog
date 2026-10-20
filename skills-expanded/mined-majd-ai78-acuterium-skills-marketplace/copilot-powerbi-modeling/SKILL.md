---
name: copilot-powerbi-modeling
display_name: Powerbi Modeling
skill_id: ACU-SKILL-1967
version: 1.0.0
category: mcp
thread: T01
domain: infrastructure
shard_affinity:
  - ADOCP
layer_access:
  - L5
  - L6
sovereignty_score: 9
governance_level: mandatory
source_repo: github/awesome-copilot
triggers:

---

# Powerbi Modeling

## Description
Power BI semantic modeling assistant for building optimized data models. Use when working with Power BI semantic models, creating measures, designing star schemas, configuring relationships, implementing RLS, or optimizing model performance. Triggers on queries about DAX calculations, table relationships, dimension/fact table design, naming conventions, model documentation, cardinality, cross-filter direction, calculation groups, and data model best practices. Always connects to the active model first using power-bi-modeling MCP tools to understand the data structure before providing guidance.

## Acuterium Integration
- **Thread:** T01 — COSM
- **Shard:** ADOCP
- **Layers:** L5, L6
- **Governance:** mandatory
- **Sovereignty Score:** 9/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/powerbi-modeling/SKILL.md
- **Author:** GitHub Copilot Community
