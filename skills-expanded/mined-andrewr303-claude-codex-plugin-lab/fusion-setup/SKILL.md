---
name: fusion-setup
description: >-
  Set up and health-check Fusion: detect which panelist CLIs are installed and authed,
  confirm the default panel works end-to-end with a tiny live smoke test, and configure the
  panel (models, effort, timeouts, allowlist). Triggers: "fusion setup", "set up fusion",
  "check fusion providers", "fusion doctor", "configure the panel".
---

# Fusion — Setup

Get Fusion working on this machine and confirm it actually dispatches.
In Codex, resolve `FUSION_PLUGIN_ROOT` from the loaded `SKILL.md` path: it is two
directories above `skills/fusion-setup/SKILL.md`; invoke scripts by absolute path.

## 1. Detect
```
bash "$FUSION_PLUGIN_ROOT/scripts/fusion.sh" detect
```
Report each panelist's state. The default panel and what each maps to:
```
bash "$FUSION_PLUGIN_ROOT/scripts/fusion.sh" providers
```
- 🔴 codex → host-native by default; external gpt-5.5 only if `FUSION_HOST=none`
- 🔷 copilot → gemini-3.5-flash (GitHub Copilot CLI)
- 🟢 opencode → opencode-go/glm-5.2 (OpenCode) · ⬛ grok → grok-build (xAI Grok CLI)
- 🔵 codex (Codex host) is the orchestrator/judge — always available, never a subprocess.

For any `missing` panelist, point the user at the right CLI install + login; for `degraded`,
it's installed but auth/quota looks dead this session.

## 2. Smoke-test (prove it dispatches — don't assume)
Run a tiny live panel so the user sees real, non-simulated output:
```
bash "$FUSION_PLUGIN_ROOT/tests/smoke-providers.sh"
```
A panelist that returns the expected token is wired. One that 127s isn't installed; other
non-zero is an auth/runtime problem caught at dispatch (this is by design — detection is
fast/presence-only, auth is verified by actually running).

## 3. Configure the models (optional)
Configure with environment variables or `config/defaults.env`:
`FUSION_CODEX_MODEL`, `FUSION_CODEX_EFFORT`, `FUSION_COPILOT_MODEL`,
`FUSION_OPENCODE_MODEL`, `FUSION_OPENCODE_VARIANT`, `FUSION_GROK_MODEL`, and
`FUSION_<PROV>_TIMEOUT` (seconds). Restrict the panel with
`~/.fusion/panel-allowlist` (one provider per line); `~/.fusion/degraded-providers` marks
session-dead providers. Precedence: explicit `FUSION_*` env > `defaults.env` > host plugin option
env vars (if present) > baked default.

## 4. Confirm
End with a one-line readiness summary: how many panelists are live, whether the smoke test
passed, and the cost reminder (a panel is ~2–5× a single call — worth it when being wrong is
expensive). If ≥2 external panelists are live, Fusion is ready.
