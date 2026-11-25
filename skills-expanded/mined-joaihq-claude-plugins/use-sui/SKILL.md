---
name: use-sui
description: Use the Sui JoAi app plugin when the task needs Sui tools or workflows.
---

# Sui

Connect Sui to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Sui tools available in this app.
- Explain what setup or authentication Sui needs before I run an action.
- Use Sui to help me with the task I describe next.

## Action Inventory

- `sui-get-balance` (query) — Retrieve the SUI token balance for a specific wallet address on the Sui blockchain by querying the first coin object.
- `sui-get-object` (query) — Retrieve information about a specific object on the Sui blockchain by its object ID.
- `sui-get-stakes` (query) — Retrieve staking information for a specific staked SUI object ID on the Sui blockchain.
- `sui-get-sui-system-state` (query) — Retrieve the current Sui system state including validator information and network parameters.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
