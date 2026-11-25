---
name: use-projectx
description: Use the ProjectX JoAi app plugin when the task needs ProjectX tools or workflows.
---

# ProjectX

Connect ProjectX to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the ProjectX tools available in this app.
- Explain what setup or authentication ProjectX needs before I run an action.
- Use ProjectX to help me with the task I describe next.

## Action Inventory

- `projectx-claim-rewards` (contract) — Claim your eGold (EGLD) staking rewards from ProjectX.
- `projectx-redelegate-egld` (contract) — Restake your eGold (EGLD) staking rewards with ProjectX.
- `projectx-stake-egld` (contract) — Delegate your EGLD to ProjectX and earn staking rewards on the MultiversX blockchain. ProjectX offers a high-performance validator node, giving you a seamless way to grow your eGold through secure delegation.
- `projectx-undelegate-egld` (contract) — Unstake your eGold (EGLD) you have previously staked with ProjectX.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
