---
name: use-allowance
description: Use the Allowance JoAi app plugin when the task needs Allowance tools or workflows.
---

# Allowance

Connect Allowance to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Allowance tools available in this app.
- Explain what setup or authentication Allowance needs before I run an action.
- Use Allowance to help me with the task I describe next.

## Action Inventory

- `allowance-fund` (contract) — Create or top up a spending allowance for an AI agent. Deposit EGLD or tokens and set per-transaction and periodic spending limits.
- `allowance-pause` (contract) — Temporarily freeze an allowance to prevent agent spending. Funds remain in the contract.
- `allowance-revoke` (contract) — Revoke an allowance and withdraw all remaining funds back to the owner.
- `allowance-spend` (contract) — Transfer tokens from an allowance to a destination address. Only the authorized agent can execute this.
- `allowance-spend-and-call` (contract) — Spend tokens from an allowance to call a smart contract endpoint directly. Enables trustless DeFi interactions through the allowance.
- `allowance-view` (query) — View the details of an allowance including balance, spending limits, and usage.
- `allowance-view-agent-ids` (query) — Get all allowance IDs assigned to an agent address.
- `allowance-view-owner-ids` (query) — Get all allowance IDs created by an owner address.
- `allowance-whitelist` (contract) — Add an allowed destination address to an allowance. When set, the agent can only spend to whitelisted addresses.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
