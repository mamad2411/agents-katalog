---
name: postman
description: Full API lifecycle via the Postman MCP Server — sync OpenAPI specs to collections, generate typed clients, run API tests, create mocks, publish docs, OWASP audits. Use for Postman, collections, specs, mocks, or SDKs.
---

# Postman

Full API lifecycle management through the Postman MCP Server (111+ tools for workspaces, collections, specs, environments, mocks, and monitors). Sync specs, generate code, run tests, create mocks, publish docs, and audit security.

## Prerequisites

**Setup check**: Call `getAuthenticatedUser` via MCP. If it succeeds, you're connected. If it fails, walk through Setup below.

## Setup

If MCP tools are not available or `getAuthenticatedUser` fails:

1. Get a Postman API key at https://postman.postman.co/settings/me/api-keys — "Generate API Key", name it "Claude Code", copy the key (starts with `PMAK-`).
2. Set the environment variable — `export POSTMAN_API_KEY=PMAK-your-key-here` (add to `~/.zshrc` or `~/.bashrc` to persist).
3. Verify: call `getAuthenticatedUser`, then list workspaces and collection counts so the user sees they're connected.

## Routing

Match the user's intent to a workflow, then read that workflow's reference file and follow it. Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

| User intent | Workflow reference |
|-------------|--------------------|
| Import a spec, push spec to Postman, create collection from spec, sync changes | `references/sync-collections.md` |
| Generate client code, SDK, wrapper, typed client, consume an API | `references/generate-client-code.md` |
| Find API, search endpoints, what's available, discover APIs | `references/discover-apis.md` |
| Run tests, check if tests pass, validate API, test collection | `references/run-collection-tests.md` |
| Create mock server, fake API, mock for frontend, mock URL | `references/create-mock-servers.md` |
| Generate docs, improve documentation, publish docs, API docs | `references/api-documentation.md` |
| Security audit, vulnerabilities, OWASP, security check | `references/security-audit.md` |

**Routing rules:**
1. Specific workflows take priority. If intent clearly maps to one, use it.
2. Ambiguous requests: ask the user what they need.
3. Multi-step requests chain workflows. "Import my spec and run tests" = Sync then Test.
4. Only use `mcp__postman__*` tools directly for single targeted updates or when the user explicitly asks.

## References

- `references/mcp-limitations.md` — known MCP behaviors and workarounds (300KB+ payloads from `getWorkspaces`/`getCollection model=full`, async HTTP 202 polling, plan-gated tag tools, aggregate-only `runCollection`, public-only `searchPostmanElements`) · read **before composing any tool calls** a workflow doesn't already cover.
- `references/mcp-tools.md` — the complete tool catalog by category · read when picking the right tool outside a workflow.

## Error Handling

These patterns apply across all workflows:

| Error | Response |
|-------|----------|
| MCP tools not available | "The Postman MCP Server isn't configured. Set your POSTMAN_API_KEY environment variable and restart your editor." |
| 401 Unauthorized | "Your Postman API key was rejected. Generate a new one at https://postman.postman.co/settings/me/api-keys" |
| Network timeout | Retry once. Check https://status.postman.com for outages. |
| Async operation stuck | If polling shows no progress after 30 seconds, inform user and suggest checking Postman app directly. |
| Collection not found | "No collection matching that name. Try discovering APIs across your workspace." |
| Empty collection | "This collection has no requests. Add endpoints in Postman or sync from a local spec." |
| Invalid spec | Report specific parse errors with line numbers. Offer to fix common YAML/JSON syntax issues. |
| Plan limitations | "Some features may require a paid Postman plan. Core operations work on all plans." |
