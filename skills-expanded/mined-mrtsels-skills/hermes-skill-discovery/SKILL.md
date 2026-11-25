---
name: hermes-skill-discovery
description: Use when skills vanish from skill_manage or discovery.
license: MIT
metadata:
  hermes:
    tags:
    - hermes
    - skills
    - symlink
    - discovery
    - skill-manage
    related_skills:
    - hermes-agent
    - skill-farm-maintenance
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
  imported_from: hermes
---

# Hermes Skill Discovery & skill_manage Resolution

Why `skill_view` shows a skill that `skill_manage` says does not exist, and where each operation actually writes. Verified 2026-08 on macOS, Python 3.13, `~/.hermes/hermes-agent` git checkout.

## The two discovery paths (they disagree)

| Path | Code | Symlinked skill dirs |
|---|---|---|
| Indexer / `skill_view` / system-prompt index | `agent/skill_utils.py::iter_skill_index_files()` — `os.walk(..., followlinks=True)` | **followed** (visible) |
| `skill_manage` (patch/edit/delete/write_file/remove_file) | `tools/skill_manager_tool.py::_find_skill()` + `_find_skill_in_other_profiles()` — `Path.rglob("SKILL.md")` | **NOT followed** (invisible) |

`Path.rglob` does not descend into symlinked directories (Py<3.13 has no `recurse_symlinks` param; 3.13 defaults it to `False`). So in any symlink-farm layout, `skill_manage` errors `Skill '<name>' not found in active profile` while `skill_view` resolves the same skill fine. `skill_manage create` also writes a **real dir** into `~/.hermes/skills/<cat>/<name>` — drift if the layout is supposed to be symlinks.

## Fix (upstream, don't local-patch)

`_find_skill` should use `iter_skill_index_files()` (the indexer's walker) instead of rglob. PR submitted upstream 2026-08; local branch `fix/skill-manage-follow-symlinks` in `~/.hermes/hermes-agent` carries the change + regression tests. Do NOT patch the checkout directly — `hermes update` resets/stashes local edits.

## Layout modes on this machine

- **external_dirs mode (current)**: `skills.external_dirs: [~/.agents/skills]` in config.yaml — Hermes reads the SSOT directly; `~/.hermes/skills` holds Hermes-only real skills by category; sensitive skills live in `.agents/skills/private/` (gitignored). Most skills are real dirs, so `skill_manage` works.
- **symlink-farm mode (retired 2026-08-06)**: `.hermes/skills` was a pure symlink farm into `.agents`. The audit script `~/.agents/skills/agent-patterns/skill-farm-maintenance/scripts/audit_symlink_farms.py` still encodes farm semantics — its "DRIFT" flags on real dirs are **obsolete** in external_dirs mode (real Hermes-only dirs are intentional).

## Pitfalls

- `skill_manage` "not found" while `skill_view` shows the skill → symlink resolution (or the skill was moved/merged — check the SSOT).
- Don't "fix" audit-script DRIFT output in external_dirs mode; verify the dir is truly orphaned first.
- File tools (`patch`/`write_file`) writing through a farm symlink path land in the SSOT target — safe and preferred for edits.
- Long multi-line `git commit -m` bodies containing shell-like tokens (e.g. `->`) can be falsely blocked by the terminal command-approval heuristic ("cannot restart or stop the gateway"); use short one-line messages or `git commit -F` / `--body-file`.
- New skill descriptions are hard-rejected above 60 chars (trigger first, ends with period).

## Related (external, SSOT-side)

`skill-farm-maintenance` and `agents-skills-repo` (in `~/.agents/skills`, external_dirs — read-only to autonomous curation) cover SSOT/git/manifest/merge workflows and the skill_manage limitation from the farm side.
