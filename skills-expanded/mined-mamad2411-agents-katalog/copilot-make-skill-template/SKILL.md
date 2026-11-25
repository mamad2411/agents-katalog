---
name: copilot-make-skill-template
display_name: Make Skill Template
skill_id: ACU-SKILL-1926
version: 1.0.0
category: agent-patterns
thread: T01
domain: cognitive
shard_affinity:
  - Diaran-MOE
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

# Make Skill Template

## Description
Create new Agent Skills for GitHub Copilot from prompts or by duplicating this template. Use when asked to "create a skill", "make a new skill", "scaffold a skill", or when building specialized AI capabilities with bundled resources. Generates SKILL.md files with proper frontmatter, directory structure, and optional scripts/references/assets folders.

## Acuterium Integration
- **Thread:** T01 — COSM
- **Shard:** Diaran-MOE
- **Layers:** L5, L6, L7, L8
- **Governance:** mandatory
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/make-skill-template/SKILL.md
- **Author:** GitHub Copilot Community
