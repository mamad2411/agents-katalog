---
name: use-ai-email
description: Use the AI Email JoAi app plugin when the task needs AI Email tools or workflows.
---

# AI Email

Connect AI Email to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the AI Email tools available in this app.
- Explain what setup or authentication AI Email needs before I run an action.
- Use AI Email to help me with the task I describe next.

## Action Inventory

- `email-send` (collect) — Send an email to a contact. Resolves or creates a conversation room for the recipient so replies are tracked.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
