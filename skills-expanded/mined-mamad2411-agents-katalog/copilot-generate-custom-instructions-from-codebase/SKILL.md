---
name: copilot-generate-custom-instructions-from-codebase
display_name: Generate Custom Instructions From Codebase
skill_id: ACU-SKILL-1905
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

# Generate Custom Instructions From Codebase

## Description
Migration and code evolution instructions generator for GitHub Copilot. Analyzes differences between two project versions (branches, commits, or releases) to create precise instructions allowing Copilot to maintain consistency during technology migrations, major refactoring, or framework version upgrades.

## Acuterium Integration
- **Thread:** T04 — ACIW
- **Shard:** AcuTect-CODEX
- **Layers:** L5, L6, L7, L8
- **Governance:** mandatory
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/generate-custom-instructions-from-codebase/SKILL.md
- **Author:** GitHub Copilot Community
