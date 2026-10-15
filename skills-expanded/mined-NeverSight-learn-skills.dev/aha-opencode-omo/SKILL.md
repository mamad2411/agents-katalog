---
name: aha-opencode-omo
description: "Full-power + full-delegation mode for OpenCode+OMO. Only when user explicitly invokes 'aha-opencode-omo'. NOT for trivial edits, Q&A, or read-only."
---

# aha-opencode-omo — Full Delegation × Full Capability Surface

## What This Mode Activates

- **Full delegation**: every non-trivial task dispatched via `task()` to OMO (oh-my-openagent, https://github.com/code-yeongyu/oh-my-openagent) subagents
- **Full capability surface**: all 12 OMO agents + 8 `task()` categories available
- **Per-task sub-mode matching**: each task judged independently — never locked to one agent

## Pre-Check (Before Activating)

- Run `opencode agent list` and confirm OMO agents present (oracle, momus, sisyphus, explore min.)
- This mode is OpenCode-specific. If in Codex, use aha-codex-omx instead.

## Sub-Mode Matching (NOT locked — judge per task)

Do NOT default to sisyphus for every task. Match per nature:

| Task type | Agent(s) | task() category |
|---|---|---|
| Planning / architecture | prometheus, metis | `unspecified-high` |
| Multi-step execution | sisyphus, atlas | `quick`/`deep`/`ultrabrain` |
| Review / critique | momus | `unspecified-high` |
| Deep diagnosis | oracle, hephaestus | `deep`/`ultrabrain` |
| Discovery / research | explore, librarian | `unspecified-low` |
| Writing / docs | any | `writing` |
| Visual / UI | multimodal-looker | `visual-engineering` |

## Retained Safety Boundaries (mode does NOT override)

Full delegation does NOT extend to hard-deny actions. These remain forbidden without how confirmation:

- Reading `~/.local/share/opencode/auth.json`
- `opencode plugin <module>` / `opencode mcp add/auth/logout`
- Provider/auth commands, `--dangerously-skip-permissions`
- Browser/CDP attach, session write, live/publish/deploy/external-write
- Global runtime config mutation, primary gateway, root routing


## Do NOT Use This Mode For

- Trivial single-file edits or typo fixes
- Quick Q&A or informational lookups
- Read-only exploration (use `explore`/`librarian` directly)
- When user says "do it natively" or "don't delegate"

## Delegation Failure Handling

If a delegated subagent returns garbage or errors:
1. Re-delegate with clearer instructions and tighter scope
2. Escalate to a stronger agent (e.g., `ultrabrain` or `oracle`)
3. Fall back to native OpenCode execution

Do NOT silently accept garbage.

## Native-First Resting State

aha-opencode-omo is explicit opt-in per task chain. Native-first is the default. When not activated, execute natively via `opencode run`, `opencode agent`, or project-local rules.

## Cost Awareness

Multi-agent delegation consumes significantly more tokens than native execution.

## Rollback / Deactivation

- **Soft**: stop invoking aha-opencode-omo, return to native-first execution
- **Hard**: delete `~/.config/opencode/skills/aha-opencode-omo/` and restart OpenCode if hot-reload does not catch it
