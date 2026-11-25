---
name: repository-governance
description: Use when auditing repository governance read-only, or when explicitly initializing or repairing governance and patching an agent guide without destructive rewrites.
---

# Repository Governance

Use this skill when a repository needs OpenArc governance setup, drift review, or source-of-truth discovery. Audit and review requests are read-only by default.

## Goal

Help agents understand repository structure, identify governance documents, preserve existing conventions, and create or patch a project agent guide.

## Workflow

1. Scan the repository before changing files.
2. Detect the repository profile: `script`, `library`, `app`, `plugin`, `docs`, or `unknown`.
   - For `unknown`, use a minimal baseline: README plus one agent guide. Report missing files, but create them only when setup is explicitly requested.
   - Do not infer product, design, brand, spec, plan, task, or archive requirements from `unknown` alone.
3. Detect existing conventions, docs, architecture notes, specs, plans, tasks, conditional product/design/brand files, assets, and agent guides.
4. Detect existing code style signals and ask only for material code style preferences not already shown by the repo.
5. For UI, frontend, desktop, mobile, or component repositories, detect design signals and ask only for material design preferences not already shown by the repo.
6. Identify conflicts between existing docs and requested OpenArc structure.
7. For audit, review, scan, or "what is missing?" requests, stop after reporting findings; do not write files.
8. Only for explicit setup, initialization, apply, repair, or migration requests, patch existing files when they already carry project intent.
9. Create missing files only when explicitly authorized, relevant to the detected profile, and no suitable existing source exists.
10. Keep diffs small and reviewable.

If `scripts/openarc.py` is available, run or request:

```bash
python3 plugins/openarc/scripts/openarc.py scan .
```

Use the result as a starting point, then verify important findings manually.

## Source Of Truth

Prefer existing repository files over generated defaults. Common OpenArc sources:

Default read priority:

- `docs/PROJECT_BRIEF.md`
- `docs/CODE_STYLE.md`
- `docs/TASKS.md`
- existing `AGENT.md` or `AGENTS.md`

Conditional read:

- `docs/PRD.md`
- latest `docs/specs/*.md`
- `docs/ARCHITECTURE.md`
- `docs/DESIGN.md` for UI, frontend, desktop, mobile, or component work
- `docs/BRAND.md` for brand, marketing, public-facing, or visual identity work
- `docs/assets/*` when the repo has UI, screenshots, icons, brand assets, or visual references
- `docs/CHANGELOG_AI.md`

Rarely read:

- `docs/archive/*`

## Context Budget Rule

Use the smallest context required to safely complete the task.

Do not automatically load:

- archived changelogs
- old completed tasks
- deprecated specs
- outdated implementation notes
- unrelated source files

Only load archived context when the task explicitly requires historical investigation.

## Agent Guide Rules

If an agent guide exists, preserve its intent and patch only missing governance sections.

If none exists, create one from `templates/AGENT.template.md` and adapt paths to the repository.

The guide should cover:

- Source-of-truth documents
- Working rules
- Code style source and unresolved style preferences
- Execution workflow
- Validation expectations
- Repository-specific constraints
- Profile-specific conditional docs; for pure script repositories, prefer runbook, validation, and change-memory guidance over design or brand scaffolding.

## Hard Rules

- Keep audits read-only unless the user explicitly asks to apply findings.
- Do not make governance setup a prerequisite for routine implementation requests.
- Use `docs/specs/*` for specs and `docs/TASKS.md` for active tasks; do not create parallel spec or task trees.
- Do not rewrite existing governance docs just to match the template.
- Do not invent architecture facts the repository does not show.
- Do not invent code style preferences when the repository has no evidence; ask concise questions or leave the gap visible in `docs/CODE_STYLE.md`.
- Do not create product, design, brand, or assets governance for repo profiles that do not need them.
- Do not leave temporary files or duplicate documentation trees.
- Do not make `docs/archive/*` part of default reading.
- Report created files, modified files, detected governance docs, conflicts, and recommended next steps.
