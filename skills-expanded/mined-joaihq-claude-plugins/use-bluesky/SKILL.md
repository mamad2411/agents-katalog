---
name: use-bluesky
description: Use the Bluesky JoAi app plugin when the task needs Bluesky tools or workflows.
---

# Bluesky

Connect Bluesky to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Bluesky tools available in this app.
- Explain what setup or authentication Bluesky needs before I run an action.
- Use Bluesky to help me with the task I describe next.

## Action Inventory

- `bluesky-create-post` (collect) — Create a new post on Bluesky using the AT Protocol.
- `bluesky-get-author-feed` (collect) — Get posts from a Bluesky user's feed.
- `bluesky-get-profile` (collect) — Get a Bluesky user's profile information including followers and post count.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
