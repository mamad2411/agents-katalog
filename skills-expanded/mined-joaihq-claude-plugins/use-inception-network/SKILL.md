---
name: use-inception-network
description: Use the Inception Network JoAi app plugin when the task needs Inception Network tools or workflows.
---

# Inception Network

Connect Inception Network to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Inception Network tools available in this app.
- Explain what setup or authentication Inception Network needs before I run an action.
- Use Inception Network to help me with the task I describe next.

## Action Inventory

- `inception-network-claim-rewards` (contract) — Claim your eGold (EGLD) staking rewards from Inception Network.
- `inception-network-redelegate-egld` (contract) — Restake your eGold (EGLD) staking rewards with Inception Network.
- `inception-network-stake-egld` (contract) — Delegate your EGLD to Inception Network and earn staking rewards on MultiversX. Inception Network provides reliable validator infrastructure, helping you grow your eGold while securing the blockchain.
- `inception-network-undelegate-egld` (contract) — Unstake your eGold (EGLD) you have previously staked with Inception Network.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
