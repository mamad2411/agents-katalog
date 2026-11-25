---
name: use-asset
description: Use the Asset JoAi app plugin when the task needs Asset tools or workflows.
---

# Asset

Connect Asset to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Asset tools available in this app.
- Explain what setup or authentication Asset needs before I run an action.
- Use Asset to help me with the task I describe next.

## Action Inventory

- `asset-transfer` (transfer) — Transfer EGLD, ESDT tokens, or NFTs on MultiversX from one wallet to another. Send any blockchain asset quickly and securely to any recipient address on the network.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
