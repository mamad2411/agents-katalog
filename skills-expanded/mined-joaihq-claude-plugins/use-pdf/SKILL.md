---
name: use-pdf
description: Use the PDF JoAi app plugin when the task needs PDF tools or workflows.
---

# PDF

Connect PDF to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the PDF tools available in this app.
- Explain what setup or authentication PDF needs before I run an action.
- Use PDF to help me with the task I describe next.

## Action Inventory

- `pdf-render` (collect) — Convert HTML content to a PDF document using DomPDF. The generated PDF is stored in the team media library for sharing and download.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
