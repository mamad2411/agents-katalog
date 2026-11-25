---
name: workspace-migration
description: Use when migrating an existing repository or workspace into OpenArc conventions, aligning docs, specs, plans, assets, agent guides, versions, and release workflow without destructive rewrites.
---

# Workspace Migration

Use this skill when a user wants an existing workspace adjusted to OpenArc conventions.

## Goal

Move an existing repository toward OpenArc structure while preserving working project intent and minimizing churn.

## Migration Workflow

1. Inventory the workspace:
   - agent guides
   - README and docs
   - code style docs, formatter config, lint config, tests, and naming conventions
   - repo profile and profile-relevant PRD/design/brand materials
   - `docs/specs/*`, `docs/plans/*`, and `docs/TASKS.md`
   - assets
   - changelog and releases
   - CI and GitHub workflows
2. Map existing files to OpenArc targets.
3. Identify missing code style preferences that cannot be inferred from existing config or code.
4. For UI, frontend, desktop, mobile, or component profiles, identify missing design preferences that cannot be inferred from existing design docs, components, CSS, or assets.
5. Classify actions:
   - keep as-is
   - patch in place
   - move or rename
   - create missing
   - archive duplicate
6. Produce a migration plan before editing.
7. Ask for confirmation before moving or renaming files.
8. Apply small patches first.
9. Validate links, docs, JSON/YAML, tests, and release workflow as applicable.
10. Report all created, modified, moved, and skipped files.

If `scripts/openarc.py` is available, start with:

```bash
python3 plugins/openarc/scripts/openarc.py scan .
```

Use the scan to seed the migration plan, not to auto-move files.

## Profile-Aware Target Structure

For an `unknown` profile, stop at the existing repository conventions plus a README and one agent guide. Do not create the `docs/` tree below from the profile alone.

```txt
AGENT.md or AGENTS.md
README.md
docs/
  PROJECT_BRIEF.md # when durable project intent needs a home
  CODE_STYLE.md    # when stable conventions need a home
  TASKS.md         # multi-stage or multi-person/agent coordination only
  specs/           # behavior or compatibility contracts only
  plans/           # sequencing, migration, rollback, or validation risk only
  CHANGELOG_AI.md  # when AI change memory is explicitly used
  archive/         # when historical context needs archiving
  PRD.md        # app/product profile when needed
  DESIGN.md     # UI/frontend/desktop/mobile profile when needed
  BRAND.md      # public brand or identity profile when needed
  assets/       # existing assets or explicitly requested organization only
```

## Rules

- Existing files win over templates.
- Use `docs/specs/*` for specs and `docs/TASKS.md` for active tasks; do not create parallel spec or task trees.
- Preserve inferred code style in `docs/CODE_STYLE.md`; ask only for preferences the repo cannot reveal.
- Repo profile controls target scope; script, CLI, automation, library, and docs-only repositories do not need design or brand scaffolding by default.
- Do not flatten useful project-specific organization.
- Do not move files only for aesthetics.
- Do not delete legacy docs unless the user explicitly confirms deletion.
- Prefer aliases, index links, or patching when moving would break references.
- Use `templates/MIGRATION.template.md` for persistent migration plans.
