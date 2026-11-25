---
name: master-01-development
description: 01-DEVELOPMENT domain of the master skills library (software, web, frontend, backend, fullstack, mobile, API, architecture and code review). Use when the task needs architecture, API, backend or implementation guidance beyond a specific installed skill and no more specific installed skill matches. Not when a framework-specific installed skill (react-expert, nextjs-developer, flutter-expert...) already matches.
---

# 01-DEVELOPMENT

## Purpose
Index for software, web, frontend, backend, fullstack, mobile, API, architecture and code review: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs architecture, API, backend or implementation guidance beyond a specific installed skill.

## When NOT to use
- A framework-specific installed skill (react-expert, nextjs-developer, flutter-expert...) already matches.
- Another domain fits better (see `../ROUTER.md`).

## Inputs
The task, project context, and constraints; domain is inferred by the orchestrator.

## Core workflow
1. Check the imported skills below; if one fits, open its `SKILL.md` and follow it.
2. Otherwise open `INSTALLED.md` in this folder (installed skills per subdomain) and invoke the matching skill with the Skill tool.
3. For cross-domain needs follow `../DEPENDENCIES.md` instead of duplicating instructions.
4. Execute, verify, report.

## Decision rules
- Prefer the most specific skill; prefer installed canonical skills over imported generic ones.
- Open one skill at a time; do not read the whole folder.

## Edge cases and failure handling
- No fitting skill -> use general capability and say no adequate skill exists; do not invent one.
- Imported skill depends on an unavailable external service -> use the nearest installed alternative.

## Validation
Check the chosen skill's instructions match the task and that its output is verified with the matching testing/validation approach.

## Output requirements
The task result as a short `DONE`; no routing narration.

## Example
Request in this domain -> orchestrator selects the skill from the list below or `INSTALLED.md` -> follow its steps -> verify -> report.

## Imported skills (read the SKILL.md at the path when relevant)
- `api/api-scaffolder/SKILL.md` - Trigger when the user wants to scaffold REST or GraphQL API endpoints, route handlers, controllers, or middleware. Also trigger for adding v
- `backend/db-schema-designer/SKILL.md` - Trigger when the user wants to design, generate, or evolve a database schema from a plain English description, requirements list, or data mo
- `software-development/developer-growth-analysis/SKILL.md` - Analyzes your recent Claude Code chat history to identify coding patterns, development gaps, and areas for improvement, curates relevant lea

## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.
