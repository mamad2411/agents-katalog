---
name: keep-tidy
description: >-
  Keep the workspace tidy while the agent works: no orphan scratch docs/scripts,
  confine temp to .agent-scratch/ or tmp/agent-*, clean before declaring done.
  Use during implementation, multi-file edits, shell/write batches, or when
  marking work done — continuous hygiene, not post-hoc /cleanup.
compatibility: Works with Cursor stop/sessionEnd hygiene hooks when configured.
metadata:
  intent: Prevent repo and local-env clutter during agent sessions; deep audit remains /cleanup.
---

# keep-tidy

Continuous “clean as you go” for agent sessions. Complements (does not replace):
- `/cleanup` + **APPLY CLEANUP** — deep audit / MERGE / scripts consolidation
- `migration-and-doc-consolidation` — migrations and canonical runbook moves
- agent `hygiene` / verifier hygiene pass — post-work proposals

Deterministic enforcement (when configured): `hooks/stop_hygiene_nudge.py` on
`stop`, `hooks/session_end_hygiene_audit.py` on `sessionEnd`.

## Activation gate
Activate if any of:
- Implementing or editing files (Write / multi-file diffs)
- Running shells that create artifacts
- Declaring work done / DoD / verify-before-done
- User asks to keep tidy, avoid clutter, or clean as you go

Skip for pure Q&A with no file or env side effects.

## Must rules
1. Prefer editing **canonical** files (`docs/`, `README*`, existing modules). Do **not**
   create root orphans: `*_analysis.md`, `*_notes.md`, `fix-*.md`, `TEMP*.md`,
   `debug*.md`, `scratch*`, `tmp_*`.
2. Scratch / experiments → `.agent-scratch/` or `tmp/agent-<id>/` (gitignored).
   Delete that scratch **before** declaring done.
3. After a tool batch that creates files: `git status --porcelain` — remove or merge
   your own clutter before continuing.
4. Do **not** touch `.env*`, lockfiles, `node_modules/`, or commit caches
   (`__pycache__/`, `.next/`, `dist/`, coverage).
5. Do **not** run global environment prune (`docker system prune`, wiping OS `%TEMP%`
   / `/tmp` outside the session scratch dir, global npm/pip cache wipe) unless the
   user explicitly asks.
6. Before “done”: hygiene pass (delete/merge orphans you created). If MERGE target
   is unclear → point to `/cleanup` instead of inventing a new report file.
7. Large/experimental work: prefer an isolated git worktree over littering the main
   checkout.

## Mini-check (cheap)
```text
git status --porcelain
```
Act on untracked/modified paths matching scratch patterns or living only under
`.agent-scratch/` / `tmp/agent-*`.

## Relation to hooks
- **stop** nudge may `followup_message` listing remaining clutter — fix it, then stop.
- **sessionEnd** may wipe allowlisted scratch dirs only; it does not replace this skill.
- Uncertain consolidations still need `/cleanup` + **APPLY CLEANUP**.

## Output when activated mid-task
- Brief note of what was removed/merged (paths), or “workspace tidy”.
- If blocked: list UNCERTAIN paths and recommend `/cleanup`.
