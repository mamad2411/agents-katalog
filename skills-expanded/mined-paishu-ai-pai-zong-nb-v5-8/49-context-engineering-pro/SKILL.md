---
name: context-engineering-pro
description: Manage project context, memory, docs, prompts, skills, and working notes so future agent sessions can retrieve the right information with minimal noise. Use when project knowledge is growing, docs are fragmented, skills overlap, context is stale, or a project needs durable AI-readable structure.
---

# Context Engineering Pro

## Purpose

Make the right context easy to retrieve and the wrong context easy to ignore.

## Workflow

1. Identify durable context vs temporary task notes.
2. Put project index information in `.ai_project.md`.
3. Put detailed references in the right `docs/` subfolder.
4. Put repeatable procedures in skills.
5. Put decisions in ADRs.
6. Prune stale, duplicated, or misleading context.
7. Keep references linked from the project index.

## Context Types

- Project identity: `.ai_project.md`.
- Architecture: `docs/architecture/`.
- Feature behavior: `docs/features/`.
- API/database/deployment: their own docs folders.
- Decisions: `docs/decisions/`.
- Known risks and debt: `docs/maintenance/`.
- Reusable workflows: skills.

## Quality Rules

- Prefer structured headings over long prose.
- Keep one source of truth per topic.
- Link related docs instead of duplicating details.
- Mark stale or superseded docs.
- Remove context that misleads future work.

## Output

State context problem, new organization, files updated, and retrieval rule for future sessions.

## Boundaries

- Do not claim files, generated media, deployments, scans, account changes, or external writes unless the active tool or command output proves them.
- Do not override system, developer, user, project, or selected-skill rules.
- If another skill is more specific for the user's intent, hand off or use it as the main skill instead of duplicating its workflow.
