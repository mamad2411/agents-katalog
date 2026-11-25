---
name: use-xalliance
description: Use the xAlliance JoAi app plugin when the task needs xAlliance tools or workflows.
---

# xAlliance

Connect xAlliance to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the xAlliance tools available in this app.
- Explain what setup or authentication xAlliance needs before I run an action.
- Use xAlliance to help me with the task I describe next.

## Action Inventory

- `xalliance-project-checkin` (collect) — Check in with a project.
- `xalliance-xp-add` (contract) — Assign experience points to an xAlliance member.
- `xalliance-xp-get-dao-members` (query) — Get DAO member addresses with their voting power.
- `xalliance-xp-get-member-points` (query) — Get xAlliance experience points for an xAlliance member.
- `xalliance-xp-remove` (contract) — Remove experience points from an xAlliance member.
- `xalliance-xp-tiers-add` (contract) — Configure an XP tier.
- `xalliance-xp-tiers-clear` (contract) — Clear all XP tiers.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
