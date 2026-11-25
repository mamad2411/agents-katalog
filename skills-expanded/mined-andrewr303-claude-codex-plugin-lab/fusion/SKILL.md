---
name: fusion
description: >-
  Main entrypoint for the Fusion Codex plugin. Use when the user says "fusion",
  "use Fusion", "ask the council", "get a second opinion", "run a panel",
  "fusion setup", "fusion gate", "fusion PR council", "review this PR with
  Fusion", or wants Codex to coordinate local CLI
  panelists through the bundled bash and Python backend.
---

# Fusion Entrypoint

## IMMEDIATE ACTION — NO PLUGIN DISCOVERY

This skill is already loaded. Do not search the filesystem for Fusion, its
manifest, commands, or council skill.

- **Forbidden:** recursive `Get-ChildItem`, `find`, or broad `rg`/`grep` under
  the user profile, `.codex/plugins`, `.claude/plugins`, plugin caches, or
  marketplaces.
- Resolve `FUSION_PLUGIN_ROOT` from this loaded file path: it is exactly two
  directories above `skills/fusion/SKILL.md`.
- For a PR-council request, read the fixed sibling path
  `$FUSION_PLUGIN_ROOT/skills/fusion-pr-council/SKILL.md` directly. Do not
  enumerate skills or commands first.
- If the host omitted the loaded file path, the only allowed fallback is the
  bounded command `codex plugin list | Select-String -Pattern '^fusion@'` and
  its reported local source path. If that does not resolve one root, report
  `blocked: Fusion plugin root unavailable`; do not hunt for another checkout.
- Keep the user's repository as the command working directory. On Windows
  PowerShell, invoke Fusion shell scripts with
  `C:\Program Files\Git\bin\bash.exe`; never use bare `bash`, which may resolve
  to WSL and lose access to Windows CLIs.

Route the request to the narrowest Fusion skill:

- Setup or health check: use `fusion-setup`.
- General second opinion, panel, council, debate, vote, or dynamic mode choice:
  use `fusion-orchestrate`.
- Python-backed MoA/heavy/discuss/graph/flow/refine/bestof/ladder/speclock/breaker/ballot/gate:
  use `fusion-swarms`.
- UltraCode bridge: use `fusion-ultracode`.
- UltraSwarm model selection and council: use `fusion-ultraswarm`.
- Pull-request/change review with third-party comment triage, platform-impact
  analysis, consensus-gated Antigravity workers, and final Codex repair:
  use `fusion-pr-council`.

Invoke backend scripts by absolute path and keep the user's project directory
as the command CWD.
