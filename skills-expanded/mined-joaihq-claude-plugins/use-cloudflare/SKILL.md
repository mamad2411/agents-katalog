---
name: use-cloudflare
description: Use the Cloudflare JoAi app plugin when the task needs Cloudflare tools or workflows.
---

# Cloudflare

Connect Cloudflare to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Cloudflare tools available in this app.
- Explain what setup or authentication Cloudflare needs before I run an action.
- Use Cloudflare to help me with the task I describe next.

## Action Inventory

- `cloudflare-create-dns-record` (collect) — Create a new DNS record in a Cloudflare zone.
- `cloudflare-delete-dns-record` (collect) — Delete a DNS record from a Cloudflare zone.
- `cloudflare-kv-read` (collect) — Read a value from a Cloudflare Workers KV namespace.
- `cloudflare-kv-write` (collect) — Write a value to a Cloudflare Workers KV namespace.
- `cloudflare-list-dns-records` (collect) — List DNS records for a Cloudflare zone.
- `cloudflare-list-kv-namespaces` (collect) — List all Workers KV namespaces in your Cloudflare account.
- `cloudflare-list-workers` (collect) — List all Workers scripts in your Cloudflare account.
- `cloudflare-list-zones` (collect) — List all zones (domains) in your Cloudflare account.
- `cloudflare-purge-cache` (collect) — Purge cached content for a Cloudflare zone. Purge everything or specific URLs.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
