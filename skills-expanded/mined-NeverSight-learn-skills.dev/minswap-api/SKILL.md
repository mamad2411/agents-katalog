---
name: minswap-api
description: Work with the Minswap-hosted public APIs documented at `https://docs.minswap.org/developer/aggregator-api` and `https://docs.minswap.org/developer/minswap-apis`. Use when Codex needs to choose endpoints, explain request or response shapes, build integrations against Minswap API routes, fetch wallet or token data, estimate swaps, build or submit aggregator transactions, inspect pending orders, or query Minswap asset and pool market-data endpoints.
---

# Minswap API

## Overview

Use this skill only for the Minswap-hosted APIs documented in the official Minswap docs:

- Aggregator API at `https://agg-api.minswap.org/aggregator`
- Market-data API at `https://api-mainnet-prod.minswap.org`
- Official docs: `https://docs.minswap.org/developer/aggregator-api`
- Official docs: `https://docs.minswap.org/developer/minswap-apis`

Do not assume this skill covers other Minswap services, SDK methods, indexer internals, or undocumented endpoints.

## Reference Map

Load only the reference file that matches the user's request:

- Read [references/aggregator-api.md](references/aggregator-api.md) for wallet lookup, token search, route estimation, unsigned swap tx building, signed tx submission, pending orders, and cancellation flows.
- Read [references/market-data-api.md](references/market-data-api.md) for asset discovery, asset metrics, asset price history, pool metrics, pool price history, pool TVL, pool volume, and pool fee timeseries.

## Workflow

Follow this order:

1. Identify whether the request is about aggregator trading flows or market-data analytics.
2. If a reference summary looks incomplete, prefer the official Minswap docs.
3. Select the exact endpoint before writing code or examples.
4. Preserve the documented request method, path, and parameter location.
5. Keep asset identifiers in the documented formats such as `lovelace` or `<policyId><tokenNameHex>`.
6. Call out pagination cursors, decimal-vs-smallest-unit handling, and currency options when they affect behavior.

## Endpoint Selection

Use the Aggregator API when the user needs:

- ADA price lookup in a fiat currency
- wallet balances and token metadata
- token search for widget or swap UI flows
- best-route swap estimation
- unsigned transaction construction
- signed transaction submission
- pending order lookup or order cancellation

Use the market-data API when the user needs:

- asset discovery and metrics
- asset price candlesticks or timeseries
- pool metrics and verification-filtered pool lists
- pool price, volume, TVL, or fee history

## Critical Rules

- Treat the documented base URL as authoritative for each API family.
- Preserve `GET` versus `POST`; several list endpoints use `POST` bodies instead of query strings.
- Do not invent authentication requirements. The provided docs describe public APIs.
- Do not collapse `amount_in_decimal` behavior into numeric types. The APIs deliberately use strings for many amounts.
- Mention `search_after` whenever the endpoint is paginated.
- Mention that Minswap protocols remain included when aggregator routing filters are used.

## Response Style

Keep answers practical:

- Start with the exact endpoint and HTTP method.
- Show only the request fields relevant to the task.
- Use one short example request instead of dumping full schemas unless the user asks for exhaustive detail.
- Pull exact enum lists, parameter names, and response shapes from the appropriate reference file.
