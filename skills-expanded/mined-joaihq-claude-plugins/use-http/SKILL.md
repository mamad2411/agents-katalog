---
name: use-http
description: Use the HTTP JoAi app plugin when the task needs HTTP tools or workflows.
---

# HTTP

Connect HTTP to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the HTTP tools available in this app.
- Explain what setup or authentication HTTP needs before I run an action.
- Use HTTP to help me with the task I describe next.

## Action Inventory

- `http-json-delete` (collect) — Remove resources or delete data from any REST API endpoint using HTTP DELETE requests. Delete records from web services, APIs, and HTTP endpoints with customizable headers. Perfect for removing data, cleaning up resources, and managing deletions in external services.
- `http-json-get` (collect) — Retrieve data from any REST API endpoint using HTTP GET requests. Fetch information from web services, APIs, and HTTP endpoints with customizable query parameters and headers. Perfect for reading data from external services and integrating with third-party APIs.
- `http-json-post` (collect) — Create new resources or submit data to any REST API endpoint using HTTP POST requests. Send JSON payloads to web services, APIs, and HTTP endpoints with customizable headers. Ideal for creating records, submitting forms, and sending data to external services.
- `http-json-put` (collect) — Update existing resources or modify data on any REST API endpoint using HTTP PUT requests. Send JSON payloads to replace or update records in web services, APIs, and HTTP endpoints with customizable headers. Perfect for updating existing data and modifying resources in external services.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
