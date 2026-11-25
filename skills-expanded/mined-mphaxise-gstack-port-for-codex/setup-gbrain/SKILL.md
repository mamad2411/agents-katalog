---
name: setup-gbrain
description: Set up or verify the local GBrain-style brain substrate, Codex skill links, optional upstream gbrain CLI/MCP, and worktree/local-environment expectations for this port.
---

# Setup GBrain

Use this skill when the user asks to set up, connect, install, or verify GBrain for this Codex port.

This is a Codex-native adaptation of upstream GStack's `setup-gbrain`. Upstream can install the real `gbrain` CLI and MCP stack; this port first preserves the local file-backed `brain/` substrate already used in this repo, then reports where true upstream GBrain integration is still needed.

## Workflow

1. Inspect the repo-local substrate:
   - confirm `brain/README.md` exists
   - confirm `scripts/brain_init.py`, `scripts/brain_search.py`, `scripts/brain_put.py`, `scripts/brain_link.py`, and `scripts/brain_doctor.py` exist
   - run `python3 scripts/brain_doctor.py` when available
2. Check for upstream GBrain availability:
   - run `command -v gbrain`
   - if present, report `gbrain --version` or equivalent status
   - if absent, do not fake CLI support; state that the local file-backed substrate is active
   - if configuration identifies a remote MCP thin client, treat the missing
     local engine as intentional; verify configuration without claiming the
     remote service is reachable until a real query succeeds
3. Check the current Codex install surface:
   - verify repo-owned skills are visible under the documented user surface at `~/.agents/skills`
   - preserve shared symlinks and user-owned directories; install only missing
     skills or update copies with this package's ownership receipt
4. Check worktree/local-environment expectations when Codex app worktrees or automations are in scope:
   - note that ignored private brain folders are not copied into worktrees unless intentionally included
   - do not add private brain corpus paths to `.worktreeinclude`
   - use tracked setup docs or local environment actions for reproducible setup steps
5. Initialize missing local folders only when they are expected by the repo and safe to create.
6. Summarize:
   - local substrate status
   - upstream CLI/MCP status
   - Codex skill install status
   - local-vs-worktree caveats when relevant
   - recommended next step, usually `sync-gbrain` or `capture`

## Guardrails

- Do not overwrite existing `brain/` pages.
- Do not install global tools unless the user explicitly asked for installation.
- Do not claim full upstream GBrain parity when only the local substrate is active.
- Do not diagnose a configured remote thin client as a broken local database.
- Treat untracked `brain/` content as user data.
- Use `gbrain-advisor` for read-only setup advice and `gbrain-upgrade` for upstream CLI upgrades.
