---
name: copilot-git-commit
display_name: Git Commit
skill_id: ACU-SKILL-1907
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

# Git Commit

## Description
Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "/commit". Supports: (1) Auto-detecting type and scope from changes, (2) Generating conventional commit messages from diff, (3) Interactive commit with optional type/scope/description overrides, (4) Intelligent file staging for logical grouping

## Acuterium Integration
- **Thread:** T04 — ACIW
- **Shard:** AcuTect-CODEX
- **Layers:** L5, L6, L7, L8
- **Governance:** mandatory
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/git-commit/SKILL.md
- **Author:** GitHub Copilot Community
