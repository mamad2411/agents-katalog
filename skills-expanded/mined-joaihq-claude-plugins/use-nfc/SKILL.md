---
name: use-nfc
description: Use the NFC JoAi app plugin when the task needs NFC tools or workflows.
---

# NFC

Connect NFC to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the NFC tools available in this app.
- Explain what setup or authentication NFC needs before I run an action.
- Use NFC to help me with the task I describe next.

## Action Inventory

- `nfc-write` (inline) — Create a short link and write it to a physical NFC tag. The link redirects to any URL you choose and tracks scans automatically. Just hold your phone near the tag to program it.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
