---
name: zno-upgrade
description: Use when the user writes /zno-upgrade, asks to update the zno-* skill package to the latest GitHub version, or wants to add missing template docs to a project initialized by an older skill version. Runs the matching upgrade script and records upgrade history.
---

# Zno-Upgrade — Skill Package / Project Docs Upgrade

This skill directory hosts the upgrade scripts for the whole zno-* command family: `scripts/update_installed_skills.py` (skill package) and `scripts/upgrade_project_docs.py` (project docs).

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Classify the request first: (a) update the installed skill package, or (b) upgrade an initialized project's docs.

### (a) Update the installed skill package

2. Run:

   ```bash
   python <skills-root>/zno-upgrade/scripts/update_installed_skills.py
   ```

   Use `--dry-run` first when the user only wants a preview. The script downloads the latest GitHub package, validates it, backs up existing skills under `<skills-root>/.backup/`, then replaces the installed skill folders.
3. Summarize: repository/branch downloaded, target install path, backup path if created, installed commands. Tell the user to restart the AI tool so skills are rescanned.

### (b) Upgrade an initialized project's docs

2. Run:

   ```bash
   python <skills-root>/zno-upgrade/scripts/upgrade_project_docs.py <project-root>
   ```

   Use `--check` to list missing docs without writing. The script copies only missing template files (never overwrites existing project docs) and appends to `docs/maintenance/12-upgrade-history.md`.
3. Summarize what was added. For new rules in the template, propose additive merges into the project's existing docs rather than replacement.
4. Update `docs/development/10-current-status.md` to note the upgrade.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
