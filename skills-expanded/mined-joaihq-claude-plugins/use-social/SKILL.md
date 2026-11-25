---
name: use-social
description: Use the Social JoAi app plugin when the task needs Social tools or workflows.
---

# Social

Connect Social to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Social tools available in this app.
- Explain what setup or authentication Social needs before I run an action.
- Use Social to help me with the task I describe next.

## Action Inventory

- `social-critique-refine` (prompt) — Critique a social media post, identify its weaknesses, then deliver an improved rewrite.
- `social-expand` (prompt) — Expand a short post into a fuller, more detailed piece of social media content.
- `social-make-punchier` (prompt) — Rewrite a social media post to be more direct, punchy, and scroll-stopping.
- `social-make-shorter` (prompt) — Condense a social media post while preserving its core message and impact.
- `social-match-voice` (prompt) — Rewrite a post to match the author's personal voice and style as defined in the agent's character.
- `social-optimize-hook` (prompt) — Rewrite only the opening line of a post to be more attention-grabbing and scroll-stopping.
- `social-write-variations` (prompt) — Generate three distinct variations of a social media post from the same core message.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
