---
name: pm-os-onboarding
description: Interactive setup for PM-Operating-System in Codex. Use when the user says onboard, PM-OS setup, set up PM-OS, or asks to configure this repo for Codex or dual-runtime.
---

# PM-OS Onboarding

Collect PM context, write `config/pm-os-config.yaml`, create a product dossier, run setup.

## When to use

- onboard
- PM-OS setup
- set up PM-OS
- configure this repo

## Workflow

1. Confirm you will write config, copy `knowledge/products/_template/` to a named product folder, and run `./scripts/setup.sh`.
2. Runtime: default `codex`. Offer `both` if they still use Cursor. Codex scope: `repo` or `user`.
3. Ask in small batches: company + role; product name + type; manager/VIPs; goals + deprioritize; Slack/Drive/GitHub/Figma/Jira/browser; MCP now or skip.
4. After company + role, offer a short public-web research pass. Skip unless they want it.
5. Write `config/pm-os-config.yaml` with `runtime.primary` and `runtime.codex_install_scope`. Keep template booleans unless they opted out. Set `skills.eval_brief: true`.
6. Copy `knowledge/products/_template/` → `knowledge/products/<slug>/` if that folder does not exist.
7. Run from repo root:
   - Codex: `./scripts/setup.sh --runtime codex --codex-scope <repo|user>`
   - Dual: `./scripts/setup.sh --runtime both --codex-scope <repo|user>`
   - Cursor only if they asked: `./scripts/setup.sh --runtime cursor`
8. Next steps: fill `brief.md`, then `evals.md` if the product is AI; example at `knowledge/products/harbor-copilot/`; Codex context in `PM-OS-AGENTS.md`; MCP in `.codex/config.toml`. `continual-learning` is Cursor-first.

Keep the conversation short. Do not invent company facts. Do not depend on Cursor-only tools.
