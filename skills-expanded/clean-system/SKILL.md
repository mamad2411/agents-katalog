---
name: clean-system
description: Reclaim disk space or clear the clutter Claude Code, Codex and Elpis leave (old chat logs, file history, logs, backups), or name or remove single sessions. Agent clutter goes without asking; caches and Docker need a yes.
---

# System clean-up

## 1. Agent clutter: clear it without asking (rule 27)

Run `python3 clean.py` from this folder (dry run), show the per-category totals, then run it with `--apply`.
- **What it clears:** old Claude, Codex and Elpis chat logs, Claude file history and scratch, Codex and Elpis logs, Codex per-run configs, and backups (`*.bak`, `*.pre-*`, `*.before-*`, `*backup*`) in the agent config folders.
- **One-off targets:** add them with `--also PATH ...`.
- **What it always spares:**
  - anything touched in the last 24 hours, or open in a running process;
  - memory folders, credentials, live `config.toml` and `settings.json`, databases, prompt history;
  - skills, plugins, jobs, plans, `ES.md`.
- Everything goes to the trash (`gio trash`).
- If an auto-mode classifier blocks `--apply`, don't work around it. Give the user the exact `! python3 … --apply` command to run.

## 2. Everything else: audit, then ask

Package caches and Docker hold other projects' state, so list the targets with sizes and get the user's yes per category.
- **Caches:**
  - **uv:** `du -sh ~/.cache/uv`, cleaned by `uv cache clean`.
  - **pip:** `~/.cache/pip`, cleaned by `pip cache purge`.
  - **conda:** `~/miniconda3/pkgs`, cleaned by `conda clean --all -y`.
  - **npm:** `~/.npm/_cacache`, cleaned by `npm cache clean --force`.
  - **pnpm:** `pnpm store prune`. Never delete the store folder.
- **Docker:** run `docker system df`. Images, containers and build cache are separate approvals. Volumes need their own explicit yes because they may hold irreplaceable data.
- Never target a home directory, workspace root, unresolved variable or broad glob.

## 3. Verify

Rerun the dry run and `df -h /`. Report what moved and how much space was freed. Note that it all sits in the trash until the user empties it.

## 4. Single sessions: name or remove one at a time

For a recent session the user wants named or judged individually, read only its product's own history root (Claude Code `~/.claude/projects/`, Codex `~/.codex/sessions/`, Elpis `~/.elpis-next/sessions/`), list id, short summary, last activity and message count in one table, and propose a 3 to 6 word name from the first meaningful user message. Rename or remove only through the product's own command, never by editing raw logs or indexes, and never the current session or one with a live writer.
