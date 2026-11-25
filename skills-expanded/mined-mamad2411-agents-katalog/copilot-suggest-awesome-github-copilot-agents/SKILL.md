---
name: copilot-suggest-awesome-github-copilot-agents
display_name: Suggest Awesome Github Copilot Agents
skill_id: ACU-SKILL-1993
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

# Suggest Awesome Github Copilot Agents

## Description
Suggest relevant GitHub Copilot Custom Agents files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing custom agents in this repository, and identifying outdated agents that need updates.

## Acuterium Integration
- **Thread:** T04 — ACIW
- **Shard:** AcuTect-CODEX
- **Layers:** L5, L6, L7, L8
- **Governance:** mandatory
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/suggest-awesome-github-copilot-agents/SKILL.md
- **Author:** GitHub Copilot Community
