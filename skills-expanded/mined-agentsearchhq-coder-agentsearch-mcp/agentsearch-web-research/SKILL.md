---
name: agentsearch-web-research
description: Use when a task needs current information from the web (docs, release notes, error messages, news, prices) or the readable text of a specific URL. Picks the right AgentSearch MCP tool and keeps calls inside the free tier unless the user configured a wallet.
---

# Web research with AgentSearch

The AgentSearch MCP server (bundled with this plugin) gives you these tools:

| Need | Tool | Cost without a wallet key |
| --- | --- | --- |
| Find pages for a query | `agentsearch_web_search` | Free (25 free searches per IP in total, then pay per call) |
| Read one known URL as markdown | `agentsearch_extract` | Free trial (5/day per IP) |
| Read a JavaScript-heavy page | `agentsearch_render` | Free trial (3/day per IP) |
| Search and read top results in one call | `agentsearch_search_and_read` | Needs wallet key |
| Recent news for a topic | `agentsearch_news_search` | Needs wallet key |
| Image of a page | `agentsearch_screenshot` | Needs wallet key |
| Check whether an agent tool/API works | `agentsearch_review_lookup` | Free |

## How to work

1. Start with `agentsearch_web_search` using a specific query (2+ characters; include library names and versions).
2. Pick the 1-3 most relevant results and read them with `agentsearch_extract`. Use `agentsearch_render` only when extract returns empty or obviously incomplete content (client-rendered pages).
3. Cite the URLs you used in your answer.
4. Do not retry a call that failed with an input error; fix the input instead. On a free-limit error (the 25 free searches per IP are a lifetime allowance; the extract/render trials are daily), tell the user and continue with what you have.

## Paid calls (optional)

Paid tools only run when the user has set `AGENTSEARCH_WALLET_PRIVATE_KEY` (a dedicated wallet holding a little USDC on Base) in the server's environment. Prices per successful call: extract $0.002, search/news $0.003, search_and_read $0.005, render $0.005, screenshot $0.004. Never ask the user to paste a private key into chat. Setup: https://github.com/agentsearchhq-coder/agentsearch-mcp#cursor
