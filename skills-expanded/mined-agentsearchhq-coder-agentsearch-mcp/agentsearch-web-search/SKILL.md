---
name: agentsearch-web-search
description: Live web search, URL-to-markdown extract and JavaScript page render for agents via AgentSearch. Free tier with no API key or account (25 free searches per IP in total, small daily extract/render trials), then pay per call over x402 with USDC on Base (search $0.003). Use when a task needs current web results or the readable text of a URL.
version: 1.0.1
homepage: https://agentsearchhq.com
---

# AgentSearch web search (no API key)

## Use when

- The task needs current information from the web: docs, release notes, error messages, news, prices.
- You have a URL and need its readable text as markdown (extract), or the page is client-rendered (render).
- You have no search-provider key, or the user does not want to create one.

## Privacy

Search queries and URLs you send are processed by AgentSearch (https://agentsearchhq.com) and its upstream search providers to answer the request. Do not put passwords, API keys, personal data or other confidential details in queries, and do not send private or token-bearing URLs (signed links, URLs with session or auth parameters) to extract or render. If the task involves confidential material, ask the user before sending anything.

## Free tier (no key, no wallet)

Base URL: `https://relay.agentsearchhq.com`. Send JSON with `curl`.

Search (25 free searches per IP in total, then pay per call):

```bash
curl -s -X POST https://relay.agentsearchhq.com/v1/search \
  -H 'content-type: application/json' -H 'x-agent-client: agentsearch-skill/1.0.1' \
  -d '{"query":"openclaw web_search provider plugin","max_results":5}'
```

Each result has a title, URL, snippet and, when known, a publish date and site name.

Read one URL as markdown (free trial, 5 per IP per day):

```bash
curl -s -X POST https://relay.agentsearchhq.com/v1/extract \
  -H 'content-type: application/json' -H 'x-agent-client: agentsearch-skill/1.0.1' \
  -d '{"url":"https://example.com"}'
```

Render a JavaScript-heavy page (free trial, 3 per IP per day): same body, path `/v1/render`. Use render only when extract returns empty or clearly incomplete text.

The free relay also has a shared daily quota. When a free limit is reached it answers HTTP 429 with a JSON `error` that names the paid endpoints; once an IP's 25 lifetime free searches are used, search answers HTTP 402 with standard x402 payment requirements instead. Tell the user, and either continue with what you have or, only if the user has approved paid calls, use the paid endpoints below.

## Paid calls (x402, USDC on Base)

Paid calls spend the user's money, so only make them when the user has set up their own x402 wallet or client and has approved paying per call (ideally with a spend cap in that client). Ask before the first paid call in a task and stay within any budget the user gives.

Base URL: `https://api.agentsearchhq.com/x402/v1/`. No account or API key: an unpaid POST returns HTTP 402 with x402 v2 payment requirements, and any x402-capable client or wallet pays and retries. Prices per call: search $0.003, news $0.003, extract $0.002, search_and_read $0.005, render $0.005, screenshot $0.004.

| Path | Body |
| --- | --- |
| `search` | `{"query": "...", "max_results": 5}` |
| `news` | `{"query": "...", "max_results": 5}` |
| `extract` | `{"url": "https://..."}` |
| `render` | `{"url": "https://..."}` |
| `search_and_read` | `{"query": "...", "num_results": 3}` |
| `screenshot` | `{"url": "https://..."}` |

Discovery document: https://api.agentsearchhq.com/.well-known/x402 . Docs: https://agentsearchhq.com/docs/x402

## How to work

1. Search with a specific query (2+ characters; include product names and versions).
2. Read the 1-3 best results with extract; fall back to render only if needed.
3. Cite the URLs you used.
4. Do not retry a request that failed with HTTP 400; fix the input. Do not loop on 429.
5. Private keys stay out of chat: do not request or accept a wallet private key in the conversation. Paid calls need the user's own x402 wallet or client, set up outside the chat: https://agentsearchhq.com/wallet-setup

## Other ways to use AgentSearch

- OpenClaw web_search provider plugin: `openclaw plugins install npm:@agentsearchhq/openclaw-web-search@0.1.1`, then `openclaw config set tools.web.search.provider agentsearch`.
- Hosted MCP server (Streamable HTTP, free tier): `https://relay.agentsearchhq.com/mcp`
- MCP package (optional, local; pinned version, installs only when the user runs it): `npx @agentsearchhq/agentsearch-mcp@1.8.5`. Source: https://github.com/agentsearchhq-coder/agentsearch-mcp
