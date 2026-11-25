---
name: use-sentry
description: Use the Sentry JoAi app plugin when the task needs Sentry tools or workflows.
---

# Sentry

Connect Sentry to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Sentry tools available in this app.
- Explain what setup or authentication Sentry needs before I run an action.
- Use Sentry to help me with the task I describe next.

## Action Inventory

- `sentry-get-issue` (collect) — Retrieve detailed information about a specific Sentry issue including status, level, occurrence count, and timestamps.
- `sentry-list-events` (collect) — List individual error occurrences (events) for a specific Sentry issue.
- `sentry-list-issues` (collect) — List issues for a specific project in a Sentry organization. Supports searching with a query string.
- `sentry-list-projects` (collect) — List all projects in a Sentry organization.
- `sentry-on-error-task-create` (action) — Automatically creates a task when a Sentry error webhook is received. Maps the error title, culprit, and permalink into a trackable task.
- `sentry-resolve-issue` (collect) — Mark a Sentry issue as resolved.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
