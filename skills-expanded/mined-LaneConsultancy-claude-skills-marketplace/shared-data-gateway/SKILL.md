---
name: shared-data-gateway
description: Use George's authenticated DataForSEO and Apify gateway from Codex cloud for any DataForSEO v3 operation, any Apify v2 actor or API path, search demand, SERP research, local-business discovery, competitor research, website verification, and other cross-project data tasks.
---

# Shared data gateway

Use the installed `seo-gateway` client as a shared data capability. If it is not on `PATH`, invoke `/root/.local/bin/seo-gateway` directly.

Never print `SEO_GATEWAY_TOKEN`, provider credentials, request headers, credential-bearing URLs, or environment-variable values. Report only whether named configuration is present.

## Start safely

Run `seo-gateway capabilities` when the required operation is unclear. Run `seo-gateway status` only to diagnose connectivity; it checks both providers without launching paid jobs.

`capabilities` confirms provider-wide access and quotas, not the provider price or account balance. There is no dry-run or cost-preview command.

Do not bypass the gateway with direct DataForSEO or Apify credentials. Do not invent routes, actor IDs, task IDs, run IDs, or dataset IDs.

## Full provider access

The generic command accepts any DataForSEO v3 operation and any Apify v2 API path or actor:

```sh
seo-gateway request dataforseo request.json
seo-gateway request apify request.json
```

The request file contains `method`, `path`, optional `query`, and optional JSON `body`. Do not include a full URL, credentials, or headers; the gateway supplies provider authentication.

DataForSEO example:

```json
{"method":"POST","path":"/v3/serp/google/maps/live/advanced","body":[{"keyword":"plumber exeter","location_code":2826,"language_code":"en"}]}
```

Apify example for any actor:

```json
{"method":"POST","path":"/v2/acts/USERNAME~ACTOR-NAME/runs","query":{"waitForFinish":0},"body":{"startUrls":[{"url":"https://example.com"}]}}
```

Supported upstream methods are GET, HEAD, POST, PUT, PATCH, and DELETE. DataForSEO paths must remain under `/v3/`; Apify paths must remain under `/v2/`. GET and HEAD cannot include a body.

This authority includes expensive and destructive provider actions, storage changes, schedules, webhooks, and deletions. Check the official operation documentation before using a new paid or destructive endpoint, use conservative inputs, and state what will be started, changed, or deleted. Quotas count requests/tasks, not exact provider spend.

## Legacy guarded DataForSEO helpers

Write one JSON task array, then use one guarded operation:

```sh
seo-gateway dataforseo serp-google-organic tasks.json
seo-gateway dataforseo google-ads-search-volume tasks.json
seo-gateway dataforseo google-keyword-ideas tasks.json
```

Examples:

```json
[{"keyword":"emergency plumber exeter","location_code":2826,"language_code":"en","device":"desktop"}]
```

```json
[{"keywords":["boiler repair exeter","emergency plumber exeter"],"location_code":2826,"language_code":"en"}]
```

Use these shortcuts for common market sizing, topic demand, competitor visibility, search-result evidence, content planning, and local-search research. Use the generic request command when another DataForSEO operation is required.

## Legacy guarded Apify helpers

The guarded actors are `compass/crawler-google-places` and `apify/rag-web-browser`. Start asynchronously, poll the returned run ID, then read its registered dataset:

```sh
seo-gateway apify-run apify/rag-web-browser input.json
seo-gateway apify-status RUN_ID
seo-gateway apify-items DATASET_ID 20 0
```

For one-URL verification, use:

```json
{"query":"https://example.com/page","maxResults":1,"outputFormats":["markdown"]}
```

Google Places is capped at 15 places per search and paid enrichment is blocked only on this legacy helper. Use the generic request command to run another actor or use its full input schema.

## Spend and integrity rules

- Use the smallest result size that answers the task.
- Batch DataForSEO task objects when the endpoint supports it; generic quota usage counts each array item.
- The client generates a valid idempotency key automatically. Set `SEO_IDEMPOTENCY_KEY` only when an exact retry must reuse the original key; use 8-128 letters, numbers, dots, colons, underscores, or hyphens.
- Never retry around quota or duplicate-request errors.
- For generic access, treat provider IDs as account-wide authority and verify the target before mutation or deletion. The legacy `apify-status` and `apify-items` commands remain restricted to gateway-created IDs.
- Inspect DataForSEO response `status_code`, task status, and reported cost; HTTP success alone is not proof of task success.
- Distinguish provider evidence from inference in the final answer.
