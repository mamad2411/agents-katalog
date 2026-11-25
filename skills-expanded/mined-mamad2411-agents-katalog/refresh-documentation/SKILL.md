---
name: refresh-documentation
description: Review and update all project documentation to keep it accurate and current. Use this skill when asked to refresh, update, or audit documentation, README files, AGENTS.md files, skill descriptions, or any markdown docs across the codebase.
license: MIT
---

# Refresh Documentation

This skill guides a systematic review and refresh of all documentation across the codebase. It is also invoked automatically each week by the `refresh-documentation` GitHub Actions workflow, which creates a GitHub issue assigned to Copilot.

## When to Use This Skill

- When asked to "refresh documentation", "update docs", or "audit documentation"
- When documentation may be stale after significant code changes
- On the weekly scheduled cadence (triggered automatically via GitHub issue)

## Scope

Documentation to review and update:

| Path                         | Description                                                          |
| ---------------------------- | -------------------------------------------------------------------- |
| `README.md`                  | Root codebase README                                                 |
| `documentation/**/*.md`      | Core documentation files                                             |
| `AGENTS.md`                  | Workspace-level Copilot instructions — skill table must stay in sync |
| `*/AGENTS.md`                | Per-project Copilot instructions                                     |
| `*/README.md`                | Project README files                                                 |
| `.github/skills/**/SKILL.md` | Skill files (mirrored to `documentation/skills/`)                    |

## Step-by-Step Workflow

### Phase 1 — Audit

For each path in scope, read the documentation and cross-check it against the actual codebase. Classify every finding into one of three categories:

| Category       | Criteria                                                                               | Action                              |
| -------------- | -------------------------------------------------------------------------------------- | ----------------------------------- |
| **Deprecated** | Documents a feature, command, file, or API that no longer exists                       | **Remove** the section or file      |
| **Outdated**   | Content exists but is inaccurate — wrong path, outdated command, incorrect description | **Update** to match current reality |
| **Missing**    | A feature, project, convention, or workflow exists in the codebase but is undocumented | **Create** new documentation        |

### Phase 2 — Act

1. **Remove deprecated content** — Delete sections, files, or entries that document things that no longer exist. This includes dead links, removed commands, retired projects, and superseded conventions.

2. **Update outdated content** — Fix inaccurate content by cross-checking against actual source files:
   - Code examples: verify commands, file paths, and APIs against the codebase
   - README files: check that project structure, commands, and purpose are accurate
   - AGENTS.md files: verify quick-reference commands still work and descriptions match current conventions
   - Cross-references: fix broken internal links

3. **Create missing documentation** — Write new content for undocumented areas:
   - New projects added since the last documentation refresh
   - New conventions, tools, or workflows not yet documented
   - Features documented in code comments but absent from markdown docs

## References

- [AGENTS.md](../../../AGENTS.md) — Workspace-level instructions
- [documentation/](../../../documentation/) — Core documentation directory
