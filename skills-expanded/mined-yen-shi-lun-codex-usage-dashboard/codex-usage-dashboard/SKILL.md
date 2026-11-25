---
name: codex-usage-dashboard
description: Install, start, stop, diagnose, or update a local Codex usage dashboard that reads ~/.codex/sessions and shows token totals, Codex credit estimates, weekly allowance estimates, model rates, and game-style levels. Use when a user asks to install, open, refresh, troubleshoot, or inspect their Codex usage dashboard or local Codex token history.
---

# Codex Usage Dashboard

Operate the bundled local-only dashboard with the deterministic scripts in `scripts/`.

## Workflow

1. Check that Node.js 20+ and npm are available.
2. Run `scripts/install.ps1` on Windows or `scripts/install.sh` on macOS/Linux when dependencies are missing or the dashboard changed.
3. Run `scripts/start.ps1` on Windows or `scripts/start.sh` on macOS/Linux.
4. Open `http://localhost:4173`.
5. Use `scripts/diagnose.ps1` when startup, session discovery, or port 4173 fails.

## Truth boundaries

- Treat token counts read from `~/.codex/sessions` as local recorded usage.
- Label Codex Credits as estimates derived from the bundled rate card.
- Label USD as API-equivalent estimates, not ChatGPT subscription charges.
- Keep research-preview models without final rates explicitly unpriced.
- Never upload session data, prompts, project paths, or token history.
- Do not modify or delete files under `~/.codex/sessions`.

## Commands

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
powershell -ExecutionPolicy Bypass -File scripts/start.ps1
powershell -ExecutionPolicy Bypass -File scripts/stop.ps1
powershell -ExecutionPolicy Bypass -File scripts/diagnose.ps1
```

macOS/Linux:

```bash
bash scripts/install.sh
bash scripts/start.sh
```

Read `references/rates.md` only when verifying or updating model pricing.
