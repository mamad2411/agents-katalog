---
name: use-readwise
description: Use the Readwise JoAi app plugin when the task needs Readwise tools or workflows.
---

# Readwise

Connect Readwise to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Readwise tools available in this app.
- Explain what setup or authentication Readwise needs before I run an action.
- Use Readwise to help me with the task I describe next.

## Action Inventory

- `readwise-get-document` (collect) — Retrieve a single Readwise Reader document by ID.
- `readwise-list-documents` (collect) — List documents from Readwise Reader with filtering and pagination support.
- `readwise-list-tags` (collect) — List available Readwise Reader tags.
- `readwise-on-document-saved-ingest` (action) — Automatically ingests a document when it is saved to Readwise Reader, extracting structured knowledge from the article.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
