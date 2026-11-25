---
name: adaline-integration
description: "High-level guide for integrating your AI application with Adaline. Use when starting a new Adaline integration, choosing between API/SDK approaches, or planning which Adaline features to adopt."
---

# Adaline Integration Guide

## What is Adaline

Adaline is the single platform to instrument, improve, define behaviors for, monitor, prompt, evaluate, and administer AI agents. It solves the AI Development Lifecycle (ADLC) — the end-to-end process of building, testing, shipping, and operating AI-powered applications.

Core pillars:

- **Instrument** — send logs (traces and spans) from your application so every LLM call, tool execution, and retrieval step is captured
- **Monitor** — analyze quality, latency, cost, and error rates across your AI operations in the Adaline dashboard
- **Prompt** — build and test prompts in the playground, deploy prompt snapshots to environments, and fetch approved snapshots at runtime
- **Evaluate** — run prompts against datasets at scale using rule-based and LLM-as-judge evaluators to gate quality before shipping
- **Improve** — optimize prompts, generate synthetic datasets, and create auto evaluators from product signals
- **Behaviors** — discover semantic patterns and behavior maps from production data

## Configuration

Set these environment variables when your Adaline credentials are available:
- `ADALINE_API_KEY` — your workspace API key (from Settings > API Keys at app.adaline.ai)
- `projectId` — your project ID (from the dashboard sidebar)
- Base URL for all REST calls: `https://api.adaline.ai/v2`

You can start integrating before you have credentials. All code examples use placeholder values — replace them with real values when ready.

## Integration Decision Tree

Choose the right skill based on your goal:

| Your goal | Skill to use | Approach |
|-----------|-------------|----------|
| Send traces/spans from your app | adaline-logs | SDK (TS/Python) or REST API |
| Fetch deployed prompts at runtime | adaline-deployments | SDK or REST API |
| Create/manage prompts programmatically | adaline-prompts | REST API |
| Build evaluation datasets | adaline-datasets | REST API |
| Set up quality evaluators | adaline-evaluators | REST API |
| Run evaluations at scale | adaline-evaluations | REST API |
| Check available AI providers/models | adaline-providers | REST API |

## Choosing Your Approach

### TypeScript SDK (@adaline/client)

Best for: Node.js and TypeScript applications. Provides typed namespace clients for the public API, helpers for deployed prompts, and buffered trace/span logging.

Install: `npm install @adaline/client @adaline/api`

Use for: logging, deployment fetching, and typed management operations for datasets, prompts, evaluators, evaluations, providers, models, projects, and logs.

### Python SDK (adaline-client)

Best for: Python applications. The current Python SDK is async-first: API calls and `monitor.flush()` are awaited inside an asyncio event loop.

Install: `pip install adaline-client adaline-api`

Use for: logging, deployment fetching, and typed management operations for datasets, prompts, evaluators, evaluations, providers, models, projects, and logs.

### REST API

Best for: any language, serverless environments, custom integrations, and all management operations regardless of language. The SDK is a thin wrapper around this API.

Base URL: `https://api.adaline.ai/v2`

Authentication: `Authorization: Bearer ADALINE_API_KEY`

### Adaline Proxy (zero-code)

Best for: quick start with zero instrumentation code. Change your LLM client's base URL to `gateway.adaline.ai` — Adaline intercepts the request, forwards it to the provider, and automatically creates a trace and span. No SDK required.

Use this when you want observability immediately without modifying application code.

## Recommended Integration Order

Work through these steps to get full value from Adaline:

1. **adaline-logs** — instrument your application to send traces and spans. This gives you immediate observability: latency, cost, errors, and prompt inputs/outputs visible in the dashboard.

2. **adaline-deployments** — move prompt text out of your code and into Adaline. Fetch the active deployed prompt at runtime using `GET /deployments` on the v2 API base URL. This decouples prompt changes from application code releases.

3. **adaline-datasets** — build datasets of representative inputs (and optionally expected outputs) for your use cases. These become the inputs to evaluations.

4. **adaline-evaluators** — define how to score prompt outputs: exact match, regex, JSON schema, or LLM-as-judge with a custom rubric.

5. **adaline-evaluations** — run a prompt version against a dataset using your evaluators. Use this as a quality gate before promoting a prompt to production.

6. **adaline-providers** — discover which LLM providers and models are configured in your Adaline workspace. Use this to avoid hardcoding provider IDs or model names.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ADALINE_API_KEY` | Required | Bearer token for all API calls |
| `ADALINE_PROJECT_ID` | Recommended | Project to associate logs with |
| `ADALINE_PROMPT_ID` | Conditional | Required when fetching a deployed prompt |
| `ADALINE_DEPLOYMENT_ENVIRONMENT_ID` | Conditional | Required when fetching environment-specific deployments (dev/staging/prod) |

## Runtime Detection Guide

Determine the right approach for your environment:

- TypeScript/JavaScript project: use the TypeScript SDK for logging, deployment fetching, and typed namespace clients; use raw REST only when the SDK surface is not convenient
- Python project: use the async Python SDK for logging, deployment fetching, and typed namespace clients; use raw REST only when needed
- Other language (Go, Ruby, Java, etc.): use the REST API for all operations
- Quick prototype or zero-code start: use the Adaline Proxy — change your LLM client's base URL to `gateway.adaline.ai`
- Serverless functions (Lambda, Cloud Functions): use the REST API directly; call `flush()` or await the POST before the function returns to avoid losing buffered spans

## Authentication

Every REST request requires a Bearer token in the Authorization header:

```
Authorization: Bearer ADALINE_API_KEY
```

All request and response bodies are JSON. Timestamps in the public API are Unix milliseconds unless an endpoint explicitly says otherwise.

## Error Handling

Retry strategy for REST API calls:

- Retry on: `5xx` server errors
- Do not retry on: `4xx` client errors — these indicate a problem with the request or credentials
- Exponential backoff: wait 1s before first retry, 2s before second, 4s before third, cap at 10s
- Maximum retries: 3

Common errors:

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid or missing API key | Check `ADALINE_API_KEY` value |
| 403 | Key does not have access to this resource | Verify project membership and key permissions |
| 404 | Resource not found | Check IDs (projectId, promptId, datasetId, etc.) |
| 429 | Rate limited | Retry with exponential backoff |
| 400 | Validation error | Check request body against the skill's API reference |
| 500/502/503 | Server error | Retry with exponential backoff |

## References

See references/api-context.md for the current v2 API endpoints grouped by resource with the skill that covers each.
See references/typescript-sdk-context.md for the TypeScript SDK overview and key methods.
See references/python-sdk-context.md for the Python SDK overview with async support.
