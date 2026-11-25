---
name: install
description: Install or verify the local GBrain-style skill surface for Codex.
---

# Install

Use this skill when the user asks to install, reinstall, or verify the GBrain skillpack locally.

## Workflow

1. Inspect current user skills under `~/.agents/skills`, the user location in
   current official Codex documentation.
2. Distinguish package-owned directories from shared symlinks, user-authored
   directories, system skills, and repo-local `.agents/skills`.
3. Install missing repo-owned skills with `scripts/install_skills.py`.
4. Update only directories carrying this package's ownership receipt. Refuse
   to replace shared symlinks, user edits, or unowned files.
5. Run repo validation and a local skill discovery smoke check.
6. Report missing, installed, and already-present skills.

## Guardrails

- Do not overwrite a real directory or shared symlink.
- Do not install upstream global tools unless explicitly requested.
- Keep the install idempotent.
- Use the checked-in installer for copies so ownership and file hashes remain inspectable.
