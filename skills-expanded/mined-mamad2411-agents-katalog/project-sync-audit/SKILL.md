---
name: project-sync-audit
description: Use when checking whether project memory is synchronized with code after meaningful changes, before final delivery of multi-file work, during project cleanup, or when .ai_project.md/docs may be stale, incomplete, inconsistent, or missing.
---

# Project Sync Audit

## Purpose

Detect drift between code, `.ai_project.md`, and `docs/`. This is a verification skill, not a place to write broad architecture essays.

Use with `project-assistant` after meaningful file changes and with `docs-index-maintainer` when docs indexing is stale.

V5.0 audit scope includes reuse drift: a document can be present but still useless if no future task knows when to read it.

## Audit Levels

| Level | Use when | Checks |
|---|---|---|
| L1 Quick | Small code change | Changed files vs `.ai_project.md`/docs triggers |
| L2 Standard | Multi-file feature/refactor | L1 + Docs Index + module boundaries + commands/tests |
| L3 Release | Before release/major handoff | L2 + roadmap/changelog/ADR/known issues/production readiness |
| L4 Governance | Prompt/skill/project-memory redesign | L3 + skill routing, user-skills, security audit, install/distribution files |

## Workflow

1. Identify changed files from git diff or file list.
2. Classify changes by feature, API, database, desktop, UI, deployment, tests, docs, or prompt/skill.
3. Check whether `.ai_project.md` has matching Stack, Commands, Directory Map, Module Boundaries, Features, APIs, Database, Desktop, Docs Index, Current Progress, and Known Risks entries.
4. Check whether relevant `docs/` files exist and are current.
5. Check that every docs file is indexed and every Docs Index path exists.
6. Check that durable docs have a `Read When` path from `.ai_project.md`, `AGENTS.md`, a user skill index, or the doc header/body.
7. Check for large or mixed-responsibility files that should be recorded as technical debt or refactor candidates.
8. Produce fixes directly when safe; otherwise report drift with exact files to update.

## Bundled Resources

- `scripts/audit-project-sync.ps1`: scans for missing `.ai_project.md`, required sections, unindexed docs files, missing docs folder, and large code files.

Run example:

```powershell
.\codex-v5.0-skill-pack\51-project-sync-audit\scripts\audit-project-sync.ps1 -Root .
```

Use script output as evidence, not as a substitute for judgment. It cannot know every semantic doc drift.

## Useful Commands

PowerShell examples:

```powershell
git status --short
git diff --name-only
Get-ChildItem -Recurse -File docs | Select-Object -ExpandProperty FullName
Get-ChildItem -Recurse -File | Where-Object {
  $_.Extension -in '.ts','.tsx','.js','.jsx','.py','.rs','.go','.java','.cs','.vue','.svelte'
} | ForEach-Object {
  $lines = (Get-Content -LiteralPath $_.FullName | Measure-Object -Line).Lines
  if ($lines -ge 900) { [pscustomobject]@{ Lines=$lines; Path=$_.FullName } }
}
```

Do not run expensive recursive scans in very large repositories unless needed; narrow by changed paths first.

## Drift Findings

Use these categories:

- `Missing Context`: `.ai_project.md` or relevant docs absent.
- `Stale Index`: Docs Index references missing files or omits existing docs.
- `Undocumented Change`: code changed behavior/contract but docs did not.
- `Boundary Drift`: files/modules violate documented ownership.
- `Large File Risk`: file near/exceeds 1000 lines or mixes responsibilities.
- `Verification Gap`: changed behavior lacks tests/build/manual verification.
- `Reuse Gap`: docs or records exist but have no clear Read When / future trigger.
- `Skill Routing Drift`: prompt references missing skills or skill triggers no longer match installed skill names.
- `Memory Ownership Gap`: record exists but no role owns updates.

## Output

```markdown
同步审计：
- OK：...
- Drift：...
- 已修复：...
- 待处理：...
```

If no drift:

```markdown
同步审计：
- 未发现 `.ai_project.md` / `docs/` 与本次变更不一致的问题。
```

## Avoid

- Treating docs as optional after API/database/desktop/release changes.
- Updating docs without checking whether paths and commands still exist.
- Recording noisy command logs instead of durable project facts.


