---
name: use-openai
description: Use the OpenAI JoAi app plugin when the task needs OpenAI tools or workflows.
---

# OpenAI

Connect OpenAI to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the OpenAI tools available in this app.
- Explain what setup or authentication OpenAI needs before I run an action.
- Use OpenAI to help me with the task I describe next.

## Action Inventory

- `openai-add-followup` (collect) — Create a followup run continuing from a previous OpenAI run.
- `openai-cancel-task` (collect) — Cancel a running OpenAI background task. Stop an in-progress job to save resources or correct instructions before it completes.
- `openai-codex-add-followup` (prompt) — Send a follow-up instruction through Codex exec mode.
- `openai-codex-cancel-task` (prompt) — Request cancellation through Codex exec mode.
- `openai-codex-get-task-status` (prompt) — Check task status by asking Codex for a one-line status update.
- `openai-codex-launch-task` (prompt) — Launch a task through Codex CLI non-interactive exec mode.
- `openai-get-task-status` (collect) — Check the progress of an OpenAI background task. See whether your job is queued, processing, or completed, and review the results when ready.
- `openai-joai-app-connect` (prompt) — Connect a JoAi app to ChatGPT by pasting the hosted MCP URL.
- `openai-joai-plugin-install` (prompt) — Add the official JoAi Codex marketplace, then install any JoAi app plugin by name.
- `openai-launch-task` (collect) — Launch a new background task powered by OpenAI. Send instructions to be processed asynchronously, ideal for long-running AI jobs like content generation, data analysis, or batch processing.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
