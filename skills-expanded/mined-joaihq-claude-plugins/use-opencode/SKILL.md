---
name: use-opencode
description: Use the OpenCode JoAi app plugin when the task needs OpenCode tools or workflows.
---

# OpenCode

Connect OpenCode to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the OpenCode tools available in this app.
- Explain what setup or authentication OpenCode needs before I run an action.
- Use OpenCode to help me with the task I describe next.

## Action Inventory

- `opencode-add-followup` (prompt) — Send a follow-up instruction through the local OpenCode CLI.
- `opencode-cancel-task` (prompt) — Request cancellation through the local OpenCode CLI.
- `opencode-get-task-status` (prompt) — Check task status by asking the local OpenCode CLI for a one-line status update.
- `opencode-launch-task` (prompt) — Launch a task through the local OpenCode CLI on the repository's existing dev branch and report the result.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
