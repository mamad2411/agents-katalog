---
name: use-gumroad
description: Use the Gumroad JoAi app plugin when the task needs Gumroad tools or workflows.
---

# Gumroad

Connect Gumroad to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Gumroad tools available in this app.
- Explain what setup or authentication Gumroad needs before I run an action.
- Use Gumroad to help me with the task I describe next.

## Action Inventory

- `gumroad-get-product` (collect) — Retrieve details of a specific product by ID.
- `gumroad-list-products` (collect) — Retrieve all products from your Gumroad account.
- `gumroad-list-sales` (collect) — Retrieve a list of sales from your Gumroad account.
- `gumroad-list-subscribers` (collect) — Retrieve a list of subscribers for a specific product.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
