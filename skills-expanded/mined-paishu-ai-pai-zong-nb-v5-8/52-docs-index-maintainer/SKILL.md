---
name: docs-index-maintainer
description: Use when creating, moving, renaming, deleting, auditing, or reorganizing documentation files, or when .ai_project.md Docs Index must show what each docs/ file is for and when future Codex sessions should read it.
---

# Docs Index Maintainer

## Purpose

Keep `.ai_project.md` as a reliable map to `docs/`. Future sessions should know which document to read for a task without scanning every file.

Use with `project-assistant` whenever docs files change.

## Required Index Fields

Each Docs Index entry should contain:

- Path
- Purpose
- Read When
- Related Area
- Last Updated or Status when useful

Recommended compact format:

```markdown
## Docs Index

| Path | Purpose | Read When | Area |
|---|---|---|---|
| `docs/api/auth.md` | Auth endpoints, token flow, errors | Changing login/API auth | API/Auth |
```

## Workflow

1. List existing docs files.
2. Compare against `.ai_project.md` Docs Index.
3. Add missing docs entries.
4. Remove or update entries for moved/deleted docs.
5. Split vague entries into precise task-readable descriptions.
6. Keep index concise; detailed content belongs in the docs file.
7. If docs are reorganized, update references inside related docs when obvious.

## Bundled Resources

- `scripts/generate-docs-index.ps1`: generates a Markdown Docs Index from current `docs/**/*.md`.

Run example:

```powershell
.\codex-v5.0-skill-pack\52-docs-index-maintainer\scripts\generate-docs-index.ps1 -Root .
```

Paste or merge the generated table into `.ai_project.md`, then refine Purpose fields if needed.

## Category Rules

| Folder | Purpose |
|---|---|
| `docs/architecture/` | system structure, module boundaries, data flow |
| `docs/features/` | feature behavior, user flows, acceptance notes |
| `docs/api/` | endpoints, schemas, auth, errors, compatibility |
| `docs/database/` | schema, migrations, indexes, transactions |
| `docs/desktop/` | Tauri/native commands, permissions, updater |
| `docs/deployment/` | env vars, build, packaging, release, rollback |
| `docs/decisions/` | ADRs and significant tradeoffs |
| `docs/maintenance/` | technical debt, known issues, refactor candidates |
| `docs/roadmap/` | roadmap and feature lifecycle |
| `docs/changelog/` | durable development history and release notes |

## Quality Bar

Good index entry:

```markdown
| `docs/desktop/tauri-permissions.md` | Tauri permissions and command exposure rules | Adding native capabilities or changing IPC | Desktop |
```

Bad index entry:

```markdown
| `docs/desktop/tauri-permissions.md` | docs | sometimes | misc |
```

## Avoid

- Leaving new docs unindexed.
- Using broad “project docs” descriptions that do not guide retrieval.
- Turning Docs Index into a changelog.
- Duplicating full docs content inside `.ai_project.md`.


