---
name: dwara-ai-gateway
description: Configure Dwara's AI gateway to proxy, route, budget, and govern LLM traffic - providers (OpenAI, Anthropic, Gemini, Azure OpenAI, Bedrock), model aliases with failover/canary/routing policies, token budgets and cost caps, prompt/response guardrails, semantic caching, prompt logging, model governance, MCP gateway, and A2A agents. Use for any task involving the `ai:` config block, /v1/chat/completions proxying, model failover, AI cost control, or turning Dwara into an MCP server.
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec. Needs a running Dwara gateway and dwara-cli for validation.
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.1"
---

# Dwara AI gateway

Dwara proxies LLM traffic as a first-class citizen: clients speak the
OpenAI chat-completions shape (Anthropic Messages and Gemini
`generateContent` dialects are also accepted), the gateway translates to
each provider, applies budgets/guardrails/caching, and returns an
OpenAI-shaped response.

## The three config pieces (always all three)

1. **An `upstreams[]` entry per provider** carrying the transport:
   `endpoints` (e.g. `api.openai.com:443`), `protocol: https`, generous
   `timeouts.read_ms` (LLMs are slow: 120000 is a sane default).
2. **The `ai:` block**: `providers`, `models` (the alias table), and
   optionally `pricing`, `routing_policies`, `guardrails`, `logging`,
   `semantic_cache`, `governance`, `experiments`, `mcp`, `a2a`.
3. **A route with `action: { type: ai }`** matching `/v1/chat/completions`
   (or your chosen path), typically `auth_required: true` with an
   `ai-token-budget` policy attached.

The client's `model` field names an **alias** from `ai.models` - never a raw
provider model. Unknown alias -> `404 model_not_found`.

## Pipeline (what runs, in order)

| # | Phase | Rejection |
| --- | --- | --- |
| 1 | Budget pre-check (before body read) | 429 `ai_budget_exceeded` (+`Retry-After`) |
| 2 | Parse body (dialects accepted; prompt templates resolved) | 400 `invalid_json` |
| 3 | Model governance (alias vs team allowlist) | 403 `model_denied_by_policy` |
| 4 | Prompt guardrails | 400 `guardrail_blocked` |
| 5 | Semantic cache (hit = no provider call; replays cached SSE frames) | - |
| 6 | Alias resolution (direct/failover/canary/policy/A-B) | 404 `model_not_found` |
| 7 | Adapter translation to provider wire format | 502 |
| 8 | Credential pick (pool rotation is Ent) | - |
| 9 | Upstream send (failover retries happen here) | 502 `provider_unreachable` |
| 10 | Response translation to canonical shape | 502 `provider_malformed_response` |
| 11 | Cost & spend (provider-reported tokens x pricing) | - |
| 12 | Response guardrails | 400 `guardrail_blocked` / `response_schema_violation` |
| 13 | Cache store + prompt logging (fire-and-forget) | - |
| 14 | Return OpenAI-shaped response | - |

Errors use the OpenAI error envelope with a `request_id`. Streaming is
`text/event-stream` with `chat.completion.chunk` frames carrying **your
alias**; a terminal usage frame (`"choices": []` + `usage`) and `data:
[DONE]` are emitted by the gateway for every provider; mid-stream provider
death yields an error chunk (`provider_stream_aborted`) then `[DONE]`, not a
connection reset. Body limit 16 MiB (413 `body_too_large`). The gateway
injects `X-Consumer-Name`/`X-Consumer-Type` toward the provider.

## Deep references

- Providers, provider kinds, auth, alias table, failover/canary rules:
  [references/providers-and-models.md](references/providers-and-models.md)
- `routing_policies` (fallback_chain, latency_cost) and token budgets /
  pricing / spend:
  [references/routing-and-budgets.md](references/routing-and-budgets.md)
- Guardrails (kinds/actions/phases), semantic cache, prompt logging,
  governance:
  [references/guardrails-cache-logging.md](references/guardrails-cache-logging.md)
- MCP gateway (Dwara as an MCP server) and A2A agents:
  [references/mcp-and-a2a.md](references/mcp-and-a2a.md)
- Runnable starting point: [assets/ai-gateway.yaml](assets/ai-gateway.yaml)

## Workflows

**Add a provider + alias (happy path)**
1. Add an `upstreams[]` entry (https, provider host, long read timeout).
2. Add an `ai.providers[]` entry: `name`, `kind`, `upstream`, `auth.header`
   + `auth.value: ${ENV_HOLDING_BEARER_PREFIX}` (whole-value rule).
3. Add an alias under `ai.models`: `provider` + `provider_model`.
4. `dwara-cli validate` -> reload -> `curl` the ai route with
   `"model": "<alias>"`.

**Control spend**: pricing table (micro-USD per 1K tokens) + a
`token_budget` policy (`tokens_per_min`, `cost_per_day_micros`, `scope`) or
consumer-direct `token_budget`. Without a pricing entry a model costs 0
(tracked, never blocked) - if spend control matters, price every alias.

**Shrink latency/cost**: `routing_policies` - `fallback_chain`
(cheap-model-first with a classifier signal) or `latency_cost`
(preference: cost|latency|balanced, optionally live-latency-driven).

**Gate teams**: `governance.team_allowlists` keyed by consumer policy name +
`governance.audit: true`.

## Gotchas

- `failover`, `canary`, `routing_policy`, `ab_test` on an alias are
  **mutually exclusive** - pick one shape per alias.
- Failover chains: max 4 alternates; deterministic errors (bad key, unknown
  model) are not retried; if everything fails the client sees the *last*
  provider's answer.
- Budget mid-stream cutoff (`ai_budget_exceeded_midstream`) only exists for
  providers that report usage during the stream (Anthropic); others enforce
  on the next pre-check. Already-streamed content stands.
- Semantic cache is per-alias, chat-only, in-memory (survives reloads, not
  restarts), fail-open on embedding-service errors, and skips streams over
  1 MiB (served but not cached).
- `credential_pool` is enterprise-only: the block is schema-accepted in OSS
  but **rejected at publish**.
- Everything in the `ai:` block hot-reloads; budget/spend windows survive
  reloads.
