---
name: gbrain-upgrade
description: Check and apply upstream gbrain upgrades safely, while keeping the Codex port's local substrate honest.
---

# GBrain Upgrade

Use this skill when the user asks to update, upgrade, or verify upstream GBrain availability.

This port was reconciled against `garrytan/gbrain` at commit
`a64fb58b9d407f4ee412249dbf4660b158f55f31`.

## Workflow

1. Determine which layer is being updated:
   - upstream `gbrain` CLI
   - this Codex port's GBrain skill files
   - this repo's local `brain/` substrate
2. Check local state before mutation:
   - `git status --short`
   - `codex --version`
   - `command -v gbrain`
   - `python3 scripts/brain_doctor.py`
3. Refresh the current official Codex manual before judging whether a local fallback is still necessary:
   - `node "${CODEX_HOME:-$HOME/.codex}/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs"`
   - review the relevant skills, MCP, plugins, memories, automations, sandboxing, and local environment sections
4. If the upstream CLI exists, use read-only upgrade checks first:
   - `gbrain self-upgrade --check-only --json` when available
   - `gbrain --version`
   - `gbrain doctor`
5. Apply upgrades only after the user approves, unless they explicitly requested the upgrade.
6. Re-run local validation after any update.

## Verify a live service upgrade

Use the configured release channel. On a host with active workers, record
whether autopilot was already paused. Pause intake for the upgrade and let
active jobs drain. Preview restarts with
`gbrain upgrade --restart-only --dry-run --json` when the installed CLI
supports it. A refused restart identifies a process that needs its owner.
Check the new executable version and run
`gbrain doctor --only runtime_build_skew,serve_build_drift --json`.
Resume intake only if it was running before and verification passed.

Upstream also offers Codex MCP setup, optional hooks and a plugin. Inspect
`gbrain setup codex --dry-run` when connection setup is in scope.
Connecting hosted storage, importing a corpus and enabling capture are
separate decisions.

[Upstream operator workflow](https://github.com/garrytan/gbrain/tree/a64fb58b9d407f4ee412249dbf4660b158f55f31/skills/gbrain-upgrade) · [Codex integration](https://github.com/garrytan/gbrain/blob/a64fb58b9d407f4ee412249dbf4660b158f55f31/docs/mcp/CODEX.md)

## Codex Adaptation

- This skill never runs a command parsed out of an `UPGRADE_AVAILABLE` marker.
- The only allowed upstream self-upgrade commands are hardcoded `gbrain self-upgrade` or `gbrain upgrade`.
- If the upstream CLI is absent, continue with this repo's file-backed GBrain port and report the absence plainly.
- Prefer current documented Codex capabilities over older Claude Code compatibility fallbacks; keep the file-backed brain and CLI/MCP fallbacks only where current host state requires them.

## Guardrails

- Do not block unrelated work on an optional upstream CLI upgrade.
- Do not convert this repo's local `brain/` corpus into another storage backend during an upgrade.
- Do not claim full upstream parity after only updating the Codex skill port.
- Do not rely on stale memory for Codex host behavior when the official manual can be refreshed.
