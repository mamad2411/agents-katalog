---
name: use-linear
description: Use the Linear JoAi app plugin when the task needs Linear tools or workflows.
---

# Linear

Connect Linear to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Linear tools available in this app.
- Explain what setup or authentication Linear needs before I run an action.
- Use Linear to help me with the task I describe next.

## Action Inventory

- `linear-add-comment` (collect) — Add a comment to a Linear issue. Supports Markdown formatting.
- `linear-create-issue` (collect) — Create a new issue in a Linear team. Supports title, description, assignee, and priority.
- `linear-get-issue` (collect) — Retrieve detailed information about a specific Linear issue including description, state, assignee, and comments.
- `linear-list-issues` (collect) — List issues in a Linear team. Supports filtering by assignee, state, and pagination.
- `linear-list-teams` (collect) — Retrieve a list of all teams in your Linear workspace with their IDs and names.
- `linear-update-issue` (collect) — Update an existing Linear issue. Change title, description, assignee, state, or priority.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
