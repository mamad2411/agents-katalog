---
name: use-medium
description: Use the Medium JoAi app plugin when the task needs Medium tools or workflows.
---

# Medium

Connect Medium to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Medium tools available in this app.
- Explain what setup or authentication Medium needs before I run an action.
- Use Medium to help me with the task I describe next.

## Action Inventory

- `medium-create-post` (collect) — Create a new post on Medium with HTML content. Supports draft and public publish statuses, and tags.
- `medium-get-user` (collect) — Retrieve information about the authenticated Medium user including username, name, and profile URL.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
