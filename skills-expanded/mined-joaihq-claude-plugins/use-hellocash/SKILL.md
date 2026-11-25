---
name: use-hellocash
description: Use the helloCash JoAi app plugin when the task needs helloCash tools or workflows.
---

# helloCash

Connect helloCash to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the helloCash tools available in this app.
- Explain what setup or authentication helloCash needs before I run an action.
- Use helloCash to help me with the task I describe next.

## Action Inventory

- `hellocash-create-invoice` (collect) — Create a new invoice in your helloCash account.
- `hellocash-get-invoice` (collect) — Retrieve a specific invoice by ID from your helloCash account.
- `hellocash-list-articles` (collect) — Retrieve articles and products from your helloCash catalog.
- `hellocash-list-customers` (collect) — Retrieve customers from your helloCash account.
- `hellocash-list-invoices` (collect) — Retrieve invoices from your helloCash account.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
