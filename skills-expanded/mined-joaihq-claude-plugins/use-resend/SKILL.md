---
name: use-resend
description: Use the Resend JoAi app plugin when the task needs Resend tools or workflows.
---

# Resend

Connect Resend to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Resend tools available in this app.
- Explain what setup or authentication Resend needs before I run an action.
- Use Resend to help me with the task I describe next.

## Action Inventory

- `resend-send-email` (collect) — Send transactional or marketing emails with full HTML and plain text support. Includes CC, BCC, reply-to, and custom headers for newsletters, notifications, and automated email workflows.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
