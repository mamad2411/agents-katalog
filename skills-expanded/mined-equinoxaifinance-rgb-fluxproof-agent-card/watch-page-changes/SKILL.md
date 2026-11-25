---
name: watch-page-changes
description: Watch a public web page (pricing, policy, changelog, terms) and get hashed before/after evidence when its meaningful text changes, through FluxProof. Use when a user wants to know when a page changes, or needs proof of what a page said before and after. Free for one page for 30 days; $9 for five pages for 30 days.
---

# Watch public pages for changes with FluxProof

Use this skill when the user wants to be told when a public page changes (a competitor's pricing, a vendor's terms, a changelog, a regulation page), or needs evidence of what changed. FluxProof normalizes the page so layout and footer churn is ignored. Each change comes with the prior and current SHA-256 hashes, the observation time and short added/removed excerpts.

It proves that the normalized public text changed between two observations. It does not prove why the page changed or who changed it.

## 1. Connect

Remote MCP server (Streamable HTTP):

```
https://fluxproof.steellantern.com/mcp
```

Free tools: `fluxproof_preflight` (can this page be watched?), `fluxproof_offer` (plans and prices) and `fluxproof_get_free_key` (a free key, shown once). The tools `fluxproof_create_monitor`, `fluxproof_check_now` and `fluxproof_list_changes` need the user's API key in their arguments, so keep those transcripts private.

## 2. Check the page first (free)

Call `fluxproof_preflight` with the URL. If the page can't be read, tell the user and stop.

## 3. Start watching

- **Free:** call `fluxproof_get_free_key`, or `POST https://fluxproof.steellantern.com/v1/keys/free`. Either returns a key, shown once; give it to the user. The free plan covers one page, checked daily for 30 days, with the latest change only and no webhook.
- **Paid (needs the user's approval):** $9 once covers 30 days, five pages, checks every 15 minutes, full history and signed webhooks. The user can buy on https://fluxproof.steellantern.com/, or an agent with the user's payment authority calls `POST /v1/passes`. That returns a Stripe MPP 402 challenge, and nothing is charged if the page can't be read.

Then create the monitor with `fluxproof_create_monitor` (or `POST /v1/monitors`), passing `url`, a `label`, and optional `watch_terms` such as `["price"]`. The first check is only a baseline, not a change.

## 4. Report changes

Use `fluxproof_list_changes`. Report what changed using the excerpts, give the observation times and keep the hashes as evidence. Say plainly when nothing meaningful changed.

Contracts: [OpenAPI](https://fluxproof.steellantern.com/openapi.json), [offers](https://fluxproof.steellantern.com/.well-known/agent-commerce.json), [policies](https://fluxproof.steellantern.com/policies).
