---
name: use-xmoney
description: Use the xMoney JoAi app plugin when the task needs xMoney tools or workflows.
---

# xMoney

Connect xMoney to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the xMoney tools available in this app.
- Explain what setup or authentication xMoney needs before I run an action.
- Use xMoney to help me with the task I describe next.

## Action Inventory

- `xmoney-payment-link-create` (collect) — Create a crypto payment link with xMoney to accept payments for invoices, products, or services. Share the link with customers to collect cryptocurrency payments quickly and securely through the xMoney merchant platform.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
