---
name: project-init
description: Set up CodeRail in a repository: goal file, task list, and the three everyday commands (start / check / done).
---

# project-init

Run `scripts/init_project.py` from the selected source-linked or installed exact
runtime, then fill `docs/NORTH_STAR.md` and run the project launcher `check`.
Do not overwrite non-empty files without explicit user approval.

## Rules

- Keep output concise.
- Prefer G/T/S/V/X/P over duplicated fields.
- Do not write business code unless this skill explicitly covers execution.
- Do not hide failed verification.
- Commit only `required_version` and the distribution identity; keep
  `linked_tool_root` or `version_store` in ignored `config.local.json`.
- Never choose `latest` or another available version when the exact runtime is
  missing. Report the mismatch before project mutation.
- Legacy `coderail_home` migration is preview-first and requires explicit
  `runtime migrate --accept`; preserve unknown keys and non-empty governance.
