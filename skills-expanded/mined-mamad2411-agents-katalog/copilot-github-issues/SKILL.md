---
name: copilot-github-issues
display_name: Github Issues
skill_id: ACU-SKILL-1910
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

# Github Issues

## Description
Create, update, and manage GitHub issues using MCP tools. Use this skill when users want to create bug reports, feature requests, or task issues, update existing issues, add labels/assignees/milestones, set issue fields (dates, priority, custom fields), set issue types, or manage issue workflows. Triggers on requests like "create an issue", "file a bug", "request a feature", "update issue X", "set the priority", "set the start date", or any GitHub issue management task.

## Acuterium Integration
- **Thread:** T01 — COSM
- **Shard:** ADOCP
- **Layers:** L5, L6
- **Governance:** mandatory
- **Sovereignty Score:** 9/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/github-issues/SKILL.md
- **Author:** GitHub Copilot Community
