---
name: install-agentic-skills
description: Refresh this agentic-skills checkout into local Claude and Codex skill directories by running the repository install script, verify global skill links, uninstall repo-managed links when requested, and route project-local pack setup to the pack skill. Use when Codex needs to make all global agentic-skills skills available on the current machine, repair stale symlinks, confirm installation status, or explain how to install packs for a project.
type: ops
version: v0.1
argument-hint: "[install|status|--uninstall]"
---

# Install Agentic Skills

Invoke as `$install-agentic-skills`.

Refresh global skill symlinks for both Claude and Codex from this `agentic-skills` checkout. Keep domain packs project-local; use `$pack` from the target project when packs are needed.

## Workflow

1. Parse `$ARGUMENTS`:
   - No args, `install`, `refresh`, or `sync`: run `scripts/install-agentic-skills.sh`.
   - `status`: run `scripts/install-agentic-skills.sh`, then inspect `~/.claude/skills`, `~/.codex/skills`, and the root installer summary.
   - `--uninstall`, `uninstall`, or `remove`: run `scripts/install-agentic-skills.sh --uninstall` only after confirming the user wants repo-managed global symlinks removed.
   - `help`, `--help`, or `-h`: run `scripts/install-agentic-skills.sh --help`.
2. Report the installer command, the Claude and Codex skill directories, installed/skipped counts, and warnings about non-symlink collisions.
3. Explain pack access separately:
   - Do not install `packs/*` globally.
   - In the project that needs domain workflows, run `$pack` for guided setup or `$pack install <pack-or-skill>` for an explicit pack or individual pack skill.
   - If a project already has `.agents/project.json`, use `$pack refresh` after this global install to recreate local pack links.
4. If the active session still cannot see a newly installed skill, tell the user to start a fresh Claude Code or Codex session.

## Constraints

- Delegate global installation to `scripts/install-agentic-skills.sh`; do not recreate symlink logic by hand.
- Do not overwrite real directories or files under `~/.claude/skills`, `~/.codex/skills`, `.claude/skills`, or `.codex/skills`.
- Treat packs as project-local capabilities managed by `scripts/pack.sh` through `$pack`.
- Stop and report exact errors if the launcher cannot resolve the repository root or if root `install.sh` fails.
