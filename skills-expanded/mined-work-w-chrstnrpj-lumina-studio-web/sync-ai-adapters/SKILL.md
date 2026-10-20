---
name: sync-ai-adapters
description: Generate or sync tool-specific AI adapter files from canonical `.agents/` sources. Use after changing roles, skills, overlays, workflows, or tool policies, or when setting up adapters for Codex, Claude Code, Cursor, GitHub Copilot, OpenCode, Aider, Cline, Kilo Code, Windsurf, Antigravity, or OpenHands.
---

# Sync AI Adapters

## Purpose

Sync generated tool-specific adapter files from canonical template sources.

Canonical sources:
- `AGENTS.md`
- `.agents/roles/`
- `.agents/skills/`
- `.agents/overlays/`
- `.agents/workflows/`
- `.agents/tools/`

Generated adapters must not be treated as the source of truth.

## Workflow

1. Inspect `AGENTS.md` and `.agents/README.md`.
2. Confirm canonical role, skill, overlay, workflow, or tool files are updated first.
3. Run the adapter sync script for the requested target.
4. Verify expected files were generated.
5. Check that stale deleted skills were not left in adapter folders.
6. Summarize generated/changed adapter files.

## Commands

Preferred:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target all
```

Targeted examples:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target opencode
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target claude
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target codex
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target cursor
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target copilot
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target aider
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target cline
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target kilo
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target windsurf
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target antigravity
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/sync-ai-adapters.ps1 -Target openhands
```

## Boundaries

- Do not create a command named `claude`; it conflicts with Claude Code's CLI.
- Do not manually edit generated adapter folders before updating canonical sources.
- Do not leave stale generated skills after pruning `.agents/skills/`.
- Do not invent unsupported tool features; use conservative markdown/rules adapters when exact support is uncertain.

## Output

- Target synced.
- Canonical files inspected.
- Adapter files generated/updated.
- Stale files removed, if any.
- Verification performed.
- Remaining assumptions or unsupported targets.
