---
name: use-cursor
description: Use the Cursor JoAi app plugin when the task needs Cursor tools or workflows.
---

# Cursor

Connect Cursor to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Cursor tools available in this app.
- Explain what setup or authentication Cursor needs before I run an action.
- Use Cursor to help me with the task I describe next.

## Action Inventory

- `cursor-add-followup` (collect) — Add a followup instruction to an existing cloud agent. Provide additional tasks or modifications for the agent to execute.
- `cursor-delete-agent` (collect) — Delete a cloud agent. This action is permanent and cannot be undone.
- `cursor-get-agent` (collect) — Retrieve the current status and results of a cloud agent. Get agent details including status, repository information, branch name, pull request URL, and summary.
- `cursor-get-conversation` (collect) — Retrieve the conversation history of a cloud agent, including all user prompts and assistant responses.
- `cursor-get-me` (collect) — Retrieve information about the API key being used for authentication, including the API key name, creation date, and user email.
- `cursor-joai-plugin-install` (action) — Open Cursor with the JoAi app prefilled for one-click MCP installation, or copy the hosted MCP URL manually if needed.
- `cursor-launch-agent` (collect) — Start a new cloud agent to work autonomously on your GitHub repository. The agent will execute tasks, make code changes, and optionally create pull requests.
- `cursor-list-agents` (collect) — List all cloud agents for the authenticated user. Retrieve agent status, repository information, and pull request details.
- `cursor-list-models` (collect) — Retrieve a list of recommended models for cloud agents. Get available LLM models that can be used for agent execution.
- `cursor-list-repositories` (collect) — Retrieve a list of GitHub repositories accessible to the authenticated user. Get repository URLs, owners, and names for use with cloud agents.
- `cursor-stop-agent` (collect) — Stop a running cloud agent. This pauses the agent's execution without deleting it. Stopped agents cannot be resumed.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
