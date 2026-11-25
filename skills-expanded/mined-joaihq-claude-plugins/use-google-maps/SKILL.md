---
name: use-google-maps
description: Use the Google Maps JoAi app plugin when the task needs Google Maps tools or workflows.
---

# Google Maps

Connect Google Maps to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Google Maps tools available in this app.
- Explain what setup or authentication Google Maps needs before I run an action.
- Use Google Maps to help me with the task I describe next.

## Action Inventory

- `google-maps-place-details` (collect) — Get full details for a specific place by its Google Place ID, including phone number, website, address, hours, and ratings.
- `google-maps-places-text-search` (collect) — Search for businesses and places on Google Maps by text query. Returns name, address, phone number, website, rating, and review count.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
