---
name: use-aiustria
description: Use the AIustria JoAi app plugin when the task needs AIustria tools or workflows.
---

# AIustria

Connect AIustria to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the AIustria tools available in this app.
- Explain what setup or authentication AIustria needs before I run an action.
- Use AIustria to help me with the task I describe next.

## Action Inventory

- `aiustria-placeholder` (action) — AIustria private warp placeholder.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
