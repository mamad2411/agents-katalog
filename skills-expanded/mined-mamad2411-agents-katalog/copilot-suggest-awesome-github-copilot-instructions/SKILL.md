---
name: copilot-suggest-awesome-github-copilot-instructions
display_name: Suggest Awesome Github Copilot Instructions
skill_id: ACU-SKILL-1994
version: 1.0.0
category: code-review
thread: T04
domain: cognitive
shard_affinity:
  - AcuTect-CODEX
layer_access:
  - L5
  - L6
  - L7
  - L8
sovereignty_score: 10
governance_level: mandatory
source_repo: github/awesome-copilot
triggers:

---

# Suggest Awesome Github Copilot Instructions

## Description
Suggest relevant GitHub Copilot instruction files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing instructions in this repository, and identifying outdated instructions that need updates.

## Acuterium Integration
- **Thread:** T04 — ACIW
- **Shard:** AcuTect-CODEX
- **Layers:** L5, L6, L7, L8
- **Governance:** mandatory
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/suggest-awesome-github-copilot-instructions/SKILL.md
- **Author:** GitHub Copilot Community
