---
name: use-eapes
description: Use the EAPES JoAi app plugin when the task needs EAPES tools or workflows.
---

# EAPES

Connect EAPES to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the EAPES tools available in this app.
- Explain what setup or authentication EAPES needs before I run an action.
- Use EAPES to help me with the task I describe next.

## Action Inventory

- `eapes-claim-rewards` (contract) — Claim your eGold (EGLD) staking rewards from EAPES.
- `eapes-redelegate-egld` (contract) — Restake your eGold (EGLD) staking rewards with EAPES.
- `eapes-stake-egld` (contract) — Stake your EGLD with EAPES, where capital meets culture on MultiversX. Earn staking rewards while supporting a community-driven validator that powers the chain and strengthens the tribe.
- `eapes-undelegate-egld` (contract) — Unstake your eGold (EGLD) you have previously staked with EAPES.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
