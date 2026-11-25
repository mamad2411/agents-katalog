---
name: use-mregld
description: Use the MrEGLD JoAi app plugin when the task needs MrEGLD tools or workflows.
---

# MrEGLD

Connect MrEGLD to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the MrEGLD tools available in this app.
- Explain what setup or authentication MrEGLD needs before I run an action.
- Use MrEGLD to help me with the task I describe next.

## Action Inventory

- `mregld-claim-rewards` (contract) — Claim your eGold (EGLD) staking rewards from MrEGLD.
- `mregld-redelegate-egld` (contract) — Restake your eGold (EGLD) staking rewards with MrEGLD.
- `mregld-stake-egld` (contract) — Stake your EGLD with MrEGLD, a trusted staking provider on the MultiversX network. Earn consistent delegation rewards while helping secure the blockchain with one of the ecosystem's dedicated validators.
- `mregld-undelegate-egld` (contract) — Unstake your eGold (EGLD) you have previously staked with MrEGLD.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
