---
name: curl-md
description: Fetch web pages and docs as optimized markdown with curl.md. Use when the user shares a URL, asks about page content, or you need to read web page or webfetch.
---

# curl.md

Use curl.md to turn URLs into agent-friendly markdown with less noise and fewer tokens.

## When to Use

Use curl.md when:

- The user shares a URL or asks what a page says
- You just need to quickly fetch one page without setting up a deeper integration
- You need docs, changelogs, articles, reference pages, or API docs as markdown before answering
- You want to narrow a long page to a specific question or task
- You need current curl.md usage for the CLI, hosted HTTP endpoint, skills, or MCP

## Preferred Entry Points

Prefer these in order:

- The local `curl.md` CLI or `md` alias when available
- The hosted HTTP endpoint at `https://curl.md/<url>`
- For curl.md's own docs, the canonical `.md` docs endpoints or `Accept: text/markdown`

For normal page fetches, prefer the stable top-level fetch interface (`curl.md/<url>` or `client.fetch(...)`). Avoid lower-level experimental `/api` routes unless the task is specifically about auth, orgs, tokens, invites, or request history.

## Stable Request Vocabulary

Prefer these names in new usage:

- `objective` — narrow output to a specific question or task
- `keywords` — pre-filter the page before extraction; comma-separated in HTTP/CLI strings
- `mode` — `smart` or `rush`; only matters with `objective`
- `fresh` — bypass cache and force a fresh fetch
- `token` — API key auth in the CLI; raw HTTP should prefer `Authorization: Bearer <token>`

`smart` is the default and best for most docs lookups. Use `rush` when speed matters more than recall.

HTTP aliases still work (`q`/`o`, `k`, `m`, `f`), but prefer the full names above in new examples and instructions.

## CLI

Prefer the CLI when it is installed locally. It handles auth, organization context, higher-level commands, and agent-friendly workflows.

```sh
# Basic fetch
curl.md example.com
md example.com

# Narrow to a specific task
curl.md docs.github.com/en/webhooks/webhook-events-and-payloads \
  --objective "pull request webhook event payload and actions" \
  --keywords pull_request

# Faster, less thorough pass
curl.md developers.cloudflare.com/d1/get-started \
  --objective "how to query D1 from a worker" \
  --keywords D1,bindings \
  --mode rush

# Force a fresh fetch
curl.md example.com --fresh

# Use API key auth
curl.md example.com --token "$CURLMD_API_KEY"
```

Notes:

- No protocol required for the target URL. curl.md normalizes to HTTPS unless the URL already specifies `http://` or `https://`.
- `curl.md fetch <url>` is equivalent to the root `curl.md <url>` command.
- If the user asks for latest or recent content, add `--fresh`.

## Hosted HTTP Endpoint

Use the hosted HTTP endpoint when the CLI is unavailable or when you just need to quickly fetch one page.

## Examples

```sh
# Default response is markdown
curl "https://curl.md/example.com"

# Narrow with stable query names
curl "https://curl.md/developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch?objective=streaming+response+body&keywords=ReadableStream,getReader"

# Force a fresh fetch
curl "https://curl.md/example.com?fresh"

# Request JSON instead of markdown
curl "https://curl.md/example.com" -H 'Accept: application/json'

# Authenticated request
curl "https://curl.md/example.com" -H "Authorization: Bearer $CURLMD_API_KEY"
```

Successful fetches return markdown by default. JSON responses have the shape:

```json
{
  "content": "# Example\n..."
}
```

## Agent Setup

When the user asks to install or wire curl.md into an agent/editor, use the current setup commands:

```sh
# Install hosted skills
npx skills add https://curl.md --yes

# Sync CLI-generated skills into supported agents
curl.md skills add
curl.md skills add --no-global

# Run as MCP stdio server
curl.md --mcp

# Register the MCP server with an agent
curl.md mcp add
curl.md mcp add --agent claude-code
```

Prefer first-party plugins over raw CLI or MCP when the target agent has an official curl.md integration.

## Best Practices

- Use `objective` when only part of a long page matters.
- Add `keywords` when you already know the terms that matter and want to shrink the search space first.
- Use `fresh` for changelogs, status pages, release notes, or any request where freshness matters.
- Use auth when the user needs higher limits, paid usage, or account/org-scoped behavior.
- For curl.md docs, prefer `.md` docs pages or `llms.txt` over HTML fetches.

## Limitations

- Paywalled or authenticated content still requires valid access.
- Some highly dynamic pages may still be incomplete or noisy.
- Errors are returned as JSON with stable string `code` and human-readable `message` fields.
