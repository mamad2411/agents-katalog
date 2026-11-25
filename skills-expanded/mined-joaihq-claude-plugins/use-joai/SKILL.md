---
name: use-joai
description: Use the JoAi platform plugin when the task needs JoAi MCP tools, board callbacks, or agent workflows.
---

# JoAi

Connect to JoAi's hosted MCP app server for agents, contacts, tasks, and related workflows.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the JoAi tools available in this app.
- Explain what setup or authentication JoAi needs before I run an action.
- Use JoAi to help me with the task I describe next.

## Usage Notes

- Prefer JoAi MCP tools when the platform plugin is connected.
- Board callback commands bind this workspace to JoAi item webhooks when needed.
