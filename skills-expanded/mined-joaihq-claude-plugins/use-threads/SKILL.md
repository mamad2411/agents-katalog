---
name: use-threads
description: Use the Threads JoAi app plugin when the task needs Threads tools or workflows.
---

# Threads

Connect Threads to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Threads tools available in this app.
- Explain what setup or authentication Threads needs before I run an action.
- Use Threads to help me with the task I describe next.

## Action Inventory

- `threads-create-text-post` (collect) — Create a text post container on Threads. Use publish-post to publish it.
- `threads-get-insights` (collect) — Get insights and metrics for your Threads account.
- `threads-get-profile` (collect) — Get your Threads profile information.
- `threads-publish-post` (collect) — Publish a previously created Threads media container.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
