---
name: workspai-workspace-intelligence
description: Use Workspai workspace intelligence reports to answer, repair, verify, and release with evidence
---

# Workspai Workspace Intelligence

Use this skill for workspace architecture, project lifecycle, blocker repair, release readiness, agent grounding, and CI evidence questions.

## Decision flow

1. Load `resources/scope-model.md`.
2. Load `.workspai/reports/INDEX.json`.
3. Load `.workspai/reports/workspace-context-agent.json`.
4. Load `.workspai/reports/workspace-skills-index.json` when operational playbooks are needed.
5. Load the smallest evidence report required for the task.
6. Answer with Scope, Evidence, Diagnosis, Fix Plan, Run, Verify, Assumptions.

## Rules

- Prefer Workspai reports over full-repo scans.
- Never claim a gate passed without a cited report.
- Separate display commands from execution requests.
- Keep project-scoped fixes inside the active project unless workspace evidence says otherwise.

## Operational skills (canonical)

Read workspace-native playbooks from `.workspai/skills/` before generic repo scans. Legacy `.rapidkit/skills/` playbooks are read only when already present from older workspaces:

- `.workspai/skills/workspai-dependency-upgrade.md` — Dependency upgrade (`workspai-dependency-upgrade`)
- `.workspai/skills/workspai-diagnose-api-failure.md` — Diagnose API failure (`workspai-diagnose-api-failure`)
- `.workspai/skills/workspai-release-readiness.md` — Release readiness (`workspai-release-readiness`)
- `.workspai/skills/workspai-rename-contract.md` — Rename contract safely (`workspai-rename-contract`)
- `.workspai/skills/workspai-safe-schema-migration.md` — Safe schema migration (`workspai-safe-schema-migration`)

Regenerate:

```bash
npx workspai workspace agent-sync --write --refresh-context
```
