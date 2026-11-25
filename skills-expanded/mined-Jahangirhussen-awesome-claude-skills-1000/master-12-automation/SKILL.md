---
name: master-12-automation
description: 12-AUTOMATION domain of the master skills library (browser automation, scraping, workflows, file automation and scheduling). Use when the task needs repeatable automations and scripted workflows and no more specific installed skill matches. Not when a SaaS integration with a dedicated installed skill exists.
---

# 12-AUTOMATION

## Purpose
Index for browser automation, scraping, workflows, file automation and scheduling: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs repeatable automations and scripted workflows.

## When NOT to use
- A SaaS integration with a dedicated installed skill exists.
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
- `file-automation/file-organizer/SKILL.md` - Intelligently organizes your files and folders across your computer by understanding context, finding duplicates, suggesting better structur
- `file-automation/youtube-downloader/SKILL.md` - Download YouTube videos with customizable quality and format options. Use this skill when the user asks to download, save, or grab YouTube v

## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.
