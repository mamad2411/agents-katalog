---
name: gemini-google-search-mcp
description: Use the gemini-google-search-mcp MCP server to answer freshness-sensitive questions with Gemini CLI and Google Search grounding.
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["npx","gemini"]},"primaryEnv":"GEMINI_CMD","homepage":"https://github.com/truongezgg/agents/tree/main/mcps/gemini-google-search-mcp#readme","os":["darwin","linux","win32"]}}
---

# gemini-google-search-mcp

Use this skill when the task needs current web information and your agent can call MCP tools.

This MCP server runs locally over stdio and delegates web-backed search to Gemini CLI, asking Gemini to use its built-in Google Search grounding.

## When To Use

- Latest package versions
- Current documentation
- Release notes and changelogs
- Breaking changes
- Pricing, quotas, and availability
- Current news and recent announcements

## Requirements

- Node.js 20 or later
- Gemini CLI installed and authenticated
- The MCP client configured to launch the server with `npx`

Recommended MCP config:

```json
{
  "command": "npx",
  "args": ["-y", "gemini-google-search-mcp"]
}
```

If Gemini CLI is not on `PATH`, set `GEMINI_CMD` to the full executable path.

## Available Tool

- `gemini_web_search(query, maxSources?, freshness?, model?, timeoutMs?)`

Parameter guidance:

- `query`: a focused search query, not a long essay
- `maxSources`: how many citations to request, usually `3` to `5`
- `freshness`: `today`, `recent`, or `any`
- `model`: optional Gemini model override
- `timeoutMs`: optional timeout override for slower searches

## Query Guidelines

- Prefer narrow queries with one topic
- Ask for current or latest information explicitly when needed
- Split unrelated topics into separate searches
- Avoid vague prompts like `tell me everything about javascript`

Good examples:

- `latest TypeScript release notes`
- `Gemini CLI MCP server docs stdio`
- `current pnpm version installation docs`
- `Next.js caching docs 2026`

## How To Respond After Tool Use

- Summarize the answer clearly
- Include source links from the returned tool result
- Distinguish current web-backed facts from your own reasoning
- If the question mixes current facts and general explanation, use the tool for the current facts and your own reasoning for the rest

## Failure Handling

If the tool fails:

- say live web search is unavailable
- mention the likely setup issue if obvious, such as missing Gemini CLI or auth
- answer from local knowledge only when it is still useful and low-risk

## Caveats

- This wrapper does not call Google Search directly; it asks Gemini CLI to do it
- Result quality depends on Gemini actually using web grounding
- If you need deterministic extraction or strict schemas from a search API, a direct search API is more reliable than an LLM wrapper
