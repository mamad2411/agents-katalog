---
name: use-rating
description: Use the Rating JoAi app plugin when the task needs Rating tools or workflows.
---

# Rating

Connect Rating to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Rating tools available in this app.
- Explain what setup or authentication Rating needs before I run an action.
- Use Rating to help me with the task I describe next.

## Action Inventory

- `rating-setup` (collect) — Set up the rating form: customize the prompt text shown above the stars, and set the external review URL (e.g. Google Review) for 5-star ratings.
- `rating-star` (collect) — Rate your visit. Your feedback is stored on your contact profile so the team can follow up personally.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
