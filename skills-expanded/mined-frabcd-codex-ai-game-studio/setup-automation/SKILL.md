---
name: setup-automation
description: Inspect a game project and propose the optional Codex hooks, scoped AGENTS.md guidance, and selected local agent profiles. Use when adopting the automation pack or changing its engine-specific project setup; never apply configuration before digest confirmation.
---

# Set up automation

Keep inspection and proposal read-only. Do not trust hooks, write project files, or materialize agents until the user confirms the exact transaction digest.

1. Run the core `doctor --project <root>` and report the detected OS, engine, existing guidance, active MCP hosts, and constraints.
2. Select one engine value: `unity`, `godot`, `unreal`, `browser`, or `generic`.
3. Run `scripts/project_setup.py plan --project <root> --engine <engine>` from this plugin. For an install proposal that may later be confirmed, add `--output <temporary-plan.json>` using a temporary path outside `<root>`.
4. Present the proposed root/path-scoped `AGENTS.md` files, common roles, selected engine specialists, permissions, backups, expiry, rollback operations, and digest. Mention that hooks remain disabled until separately reviewed and trusted through `/hooks`.
5. Wait for the user to confirm that digest verbatim.
6. Apply only with `scripts/project_setup.py apply --project <root> --plan <plan.json> --confirmed-digest <digest>`.
7. Validate the installed guidance and agent TOML, then report the transaction ID. If the user wants to undo it, generate a rollback proposal with the core `pack rollback <transaction-id>`; never roll back without a second digest confirmation.

Preserve existing files through the transaction backup. Agents inherit the active Codex model and permission mode; do not add model pins, unsupported tool declarations, memory fields, or fixed turn limits.

For preview-only requests, present the proposal and stop after step 4. Do not solicit confirmation, write a plan inside the project, or apply the plan.
