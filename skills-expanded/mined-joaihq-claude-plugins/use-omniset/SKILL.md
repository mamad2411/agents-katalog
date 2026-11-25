---
name: use-omniset
description: Use the OmniSet JoAi app plugin when the task needs OmniSet tools or workflows.
---

# OmniSet

Connect OmniSet to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the OmniSet tools available in this app.
- Explain what setup or authentication OmniSet needs before I run an action.
- Use OmniSet to help me with the task I describe next.

## Action Inventory

- `omniset-deposit-arbitrum` (contract, contract) — Deposit a blockchain asset from Arbitrum to OmniSet.
- `omniset-deposit-ethereum` (contract, contract) — Deposit a blockchain asset from Ethereum to OmniSet.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
