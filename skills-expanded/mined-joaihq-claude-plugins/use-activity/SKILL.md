---
name: use-activity
description: Use the Activity JoAi app plugin when the task needs Activity tools or workflows.
---

# Activity

Connect Activity to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Activity tools available in this app.
- Explain what setup or authentication Activity needs before I run an action.
- Use Activity to help me with the task I describe next.

## Action Inventory

- `activity-running-log` (collect) — Record a completed run so the coach can track your progress and adjust the plan.
- `activity-running-onboard` (collect) — Tell the coach your goal, current fitness level, and availability so it can build your personal training plan.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
