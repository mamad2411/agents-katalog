---
name: llm-gateway-and-multi-provider-routing
description: >
  Configures an LLM gateway/proxy (LiteLLM, Portkey, OpenRouter-style)
  that sits between agent code and one or more model providers to unify
  routing, automatic fallback on a provider outage or rate-limit, and
  cost/rate-limit tracking across providers behind one API surface. Use
  when a user asks to "set up an LLM gateway/proxy," "route between
  OpenAI/Anthropic/Azure/Bedrock," "add a fallback model when a provider
  is down," "track spend/rate limits across multiple LLM providers in one
  place," "load-balance across API keys or regions," or reports a
  provider outage/rate-limit that should have failed over but didn't.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# LLM Gateway and Multi-Provider Routing

## Purpose

Calling model providers directly from application code works until you
need more than one provider — a fallback when a primary provider has an
outage or exhausts a rate limit, a way to shift traffic between
providers/regions/API keys for cost or availability, or a single place
to see spend and rate-limit headroom across every provider your agents
use. An LLM gateway (LiteLLM proxy, Portkey, OpenRouter, or an
equivalent internal proxy) solves this by presenting one unified API
surface backed by a routing/fallback layer, so application code targets
"the gateway" once instead of hand-rolling provider-specific retry and
failover logic in every agent. This skill covers configuring that
gateway layer specifically — provider/model routing rules, fallback
chains, load balancing, and unified rate-limit/cost tracking — not the
per-workflow cost/latency tuning of what you send to a model (see
[llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md))
or the fast triage of a single workflow's cost/latency spike (see
[agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md)),
both of which assume a gateway (if one exists) is already routing
correctly.

## When to use

- Standing up a gateway/proxy in front of two or more LLM providers (or
  two or more accounts/regions of the same provider) so agent code calls
  one endpoint instead of provider-specific SDKs directly.
- Adding a fallback model/provider that should take over automatically
  when the primary provider returns 5xx errors, times out, or returns a
  rate-limit (429) response.
- A provider outage or rate-limit event happened and fallback either
  didn't trigger, triggered too late, or routed to a fallback that
  itself failed silently.
- Setting per-team, per-project, or per-API-key budgets and rate limits
  that need to be enforced consistently across multiple providers, not
  per-provider in each provider's own console.
- Load-balancing traffic across multiple API keys/deployments of the
  same model to work around a single key's rate limit.
- Needing one place to see aggregate spend and usage across providers,
  rather than reconciling separate invoices/dashboards per vendor.

## Prerequisites & environment

- API credentials for each provider/deployment the gateway will route
  to, stored as secrets in your secrets manager and injected into the
  gateway's runtime — never committed to the gateway's config file in
  plaintext (see
  [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md)).
- A decision on gateway placement: a managed SaaS gateway (Portkey,
  OpenRouter) that calls providers on your behalf, versus a self-hosted
  proxy (LiteLLM proxy, or an internal equivalent) that you deploy and
  operate — this changes who holds provider credentials and where
  request/response payloads transit, which matters for data-handling
  requirements.
- Know each provider's actual rate limits (requests/minute,
  tokens/minute) and current status/incident page URL ahead of time —
  fallback logic is only as good as knowing what "the primary is down"
  actually looks like for that specific provider.
- A monitoring destination (see
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md))
  for the gateway to export routing/cost/error metrics to — a gateway
  with no observability into its own routing decisions is difficult to
  debug when fallback behaves unexpectedly.
- Application code updated to call the gateway's unified endpoint
  (commonly OpenAI-API-compatible across LiteLLM/Portkey/OpenRouter)
  rather than each provider's native SDK directly, so routing changes
  don't require an application redeploy.

## Step-by-step guidance

1. **Define named "model groups" that map a logical model name to one
   or more real provider deployments**, so application code requests a
   logical name and the gateway decides which underlying provider/
   deployment actually serves it. A self-hosted LiteLLM proxy example:

   ```yaml
   # litellm_config.yaml
   model_list:
     - model_name: primary-reasoning-model
       litellm_params:
         model: anthropic/claude-opus-4
         api_key: os.environ/ANTHROPIC_API_KEY
     - model_name: primary-reasoning-model
       litellm_params:
         model: azure/gpt-4o-deployment
         api_key: os.environ/AZURE_OPENAI_API_KEY
         api_base: os.environ/AZURE_OPENAI_ENDPOINT
       model_info:
         tier: fallback
   ```

   Application code calls `model="primary-reasoning-model"` once; which
   real provider actually serves the request is a gateway routing
   decision, not something the application needs to know.

2. **Configure automatic fallback on error/rate-limit, ordered
   explicitly**, rather than relying on the application's own retry
   logic to happen to hit a different provider:

   ```yaml
   router_settings:
     routing_strategy: usage-based-routing   # or: least-busy, latency-based-routing
     fallbacks:
       - primary-reasoning-model: ["fallback-azure-gpt4o"]
     context_window_fallbacks:
       - primary-reasoning-model: ["fallback-long-context-model"]
     num_retries: 2
     retry_after: 5              # seconds, before retrying the same deployment
     allowed_fails: 3            # consecutive fails before a deployment is cooled down
     cooldown_time: 60           # seconds a failing deployment is skipped for
   ```

   `fallbacks` is what fires on hard errors/timeouts;
   `context_window_fallbacks` fires specifically when a request's token
   count exceeds the primary model's context window — these are
   different failure modes and should route to different targets (a
   provider outage vs. a request simply too large for that model).

3. **For a managed gateway (Portkey/OpenRouter-style), configure the
   equivalent fallback/loadbalance config in its native format** rather
   than assuming identical field names — the concept (ordered fallback
   targets, retry count, condition to trigger on) is the same across
   vendors even though the config shape differs:

   ```json
   {
     "strategy": { "mode": "fallback" },
     "targets": [
       { "provider": "anthropic", "override_params": { "model": "claude-opus-4" } },
       { "provider": "azure-openai", "override_params": { "model": "gpt-4o-deployment" } }
     ],
     "retry": { "attempts": 2, "on_status_codes": [429, 500, 502, 503, 504] }
   }
   ```

   Confirm which HTTP status codes the vendor's fallback triggers on by
   default — a gateway that only retries on `5xx` and not `429` will not
   fail over during a rate-limit event, which is one of the two most
   common reasons to want a gateway in the first place.

4. **Load-balance across multiple API keys/deployments of the same
   model** to spread requests under a single key's rate limit, rather
   than one key absorbing all traffic and hitting its limit while
   others sit idle:

   ```yaml
   model_list:
     - model_name: extraction-model
       litellm_params: { model: openai/gpt-4o-mini, api_key: os.environ/OPENAI_KEY_1 }
     - model_name: extraction-model
       litellm_params: { model: openai/gpt-4o-mini, api_key: os.environ/OPENAI_KEY_2 }
   router_settings:
     routing_strategy: usage-based-routing   # spreads load by current usage, not round-robin
   ```

5. **Set per-key/per-team/per-project budgets and rate limits at the
   gateway**, so spend/throughput controls are enforced in one place
   regardless of which provider actually serves a given request:

   ```yaml
   # LiteLLM proxy virtual key example
   litellm_settings:
     max_budget: 500          # USD, per key, per budget_duration
     budget_duration: 30d
   general_settings:
     master_key: os.environ/LITELLM_MASTER_KEY
   ```
   ```bash
   curl -X POST http://<gateway>/key/generate \
     -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
     -d '{"models": ["primary-reasoning-model"], "max_budget": 500, "rpm_limit": 200}'
   ```
   A key scoped this way lets one team's runaway usage hit its own
   budget/rate-limit ceiling without silently consuming another team's
   provider-level quota.

6. **Export routing decisions and per-provider cost/latency as
   metrics**, not just aggregate totals — a fallback that fires
   silently and successfully is invisible without this, and looks
   identical to "everything is fine" until the fallback provider itself
   degrades:

   ```yaml
   litellm_settings:
     success_callback: ["prometheus"]
     failure_callback: ["prometheus"]
   ```
   Track, per provider/deployment: request count, error rate, p95
   latency, cost, and fallback-trigger count — wire alerting on
   fallback-trigger count so a fallback event pages someone even though
   requests are still succeeding (see
   [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)).

7. **Test failover deliberately before trusting it in production** —
   point a deployment's API key at an invalid value or a nonexistent
   endpoint in a staging config and confirm requests actually land on
   the fallback target with an acceptable latency penalty, rather than
   assuming the configuration works because it looks correct.

   > **Warning:** never test failover by revoking or rotating a
   > **production** API key to simulate an outage — this is a
   > destructive action against a live credential that can affect any
   > other system still using it. Use a disposable staging key, a
   > sandboxed deployment, or the gateway's own simulated-failure/chaos
   > testing feature if one exists.

8. **Pin gateway config as version-controlled infrastructure**, not
   console-clicked state, so a routing/fallback change is reviewable and
   revertible exactly like the rollback guidance in
   [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md) —
   a hand-edited routing config with no previous version saved turns a
   bad routing change into its own incident.

## Best practices

- Route application code through logical model-group names, never a
  provider-specific model string — this is what makes swapping,
  adding, or reordering providers a gateway config change instead of an
  application code change.
- Configure fallback to trigger on rate-limit responses (`429`)
  explicitly, not only on hard `5xx` errors — a provider under load that
  is technically "up" but rate-limiting you needs the same failover
  behavior as a genuine outage.
- Keep fallback chains short and deliberately ordered (primary →
  one or two known-good alternates), not "try every configured
  provider" — an unordered or overly long fallback chain makes latency
  under failure unpredictable and can mask which provider actually
  served a request.
- Alert on fallback-trigger rate as its own signal, separate from
  overall error rate — a fallback that's firing constantly means the
  primary is degraded even if end users never see a failed request.
- Scope budgets/rate limits per key or per team at the gateway rather
  than relying solely on each provider's own account-level limit — this
  is what prevents one workflow's runaway usage from silently consuming
  another team's quota on a shared provider account.
- Store every provider credential as a secret injected at runtime, and
  rotate gateway-held credentials on the same cadence as any other
  production API key (see
  [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md)).
- Treat a self-hosted gateway (LiteLLM proxy or equivalent) as a
  production service in its own right — give it its own health checks,
  its own on-call visibility, and redundancy, since it now sits on the
  critical path for every agent workflow behind it.

## Common pitfalls

- **Symptom:** A provider has a well-documented outage or is actively
  rate-limiting requests, but the gateway keeps sending traffic to it
  and requests fail instead of failing over.
  **Fix:** The fallback rule's trigger condition doesn't include the
  status code the provider is actually returning — most commonly, only
  `5xx` is configured and the provider is returning `429`. Add `429` (and
  timeout) explicitly to the fallback trigger condition and re-test.

- **Symptom:** Fallback fires correctly, but the fallback provider also
  starts failing shortly after, and nobody notices until users report
  the agent is completely down.
  **Fix:** Fallback-trigger events weren't monitored/alerted as their
  own signal — only end-to-end error rate was tracked, which stayed low
  right up until the fallback also failed. Alert on fallback-trigger
  count/rate directly so a primary-provider degradation pages someone
  before the fallback is also exhausted.

- **Symptom:** One team's high-volume, low-priority batch workflow
  consumes the shared provider account's entire rate limit, causing an
  unrelated, higher-priority interactive workflow to get rate-limited.
  **Fix:** No per-key/per-team rate limit was set at the gateway, so
  every workflow shared one undivided provider-level quota. Issue
  separate gateway virtual keys per team/workflow with their own
  `rpm_limit`/budget so one workflow's usage can't starve another's.

- **Symptom:** A routing config change (reordering fallback priority,
  swapping a model deployment) is pushed directly to the gateway's live
  config with no previous version saved, and a subsequent problem has
  no clean rollback target.
  **Fix:** Treat gateway config as version-controlled infrastructure
  (git-tracked YAML/JSON deployed via CI), the same discipline applied
  to prompt/routing rollbacks in
  [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md) —
  never hand-edit a live gateway config as the only copy of a change.

- **Symptom:** A "failover test" performed by revoking or rotating a
  production provider API key causes an unrelated production workflow
  (that also used that key directly, bypassing the gateway) to fail
  unexpectedly.
  **Fix:** This is a destructive action taken against shared,
  live credentials. Test failover with a disposable staging key or a
  deliberately misconfigured non-production deployment target instead
  of touching any credential still used in production.

## Worked example

**Scenario:** An internal agent platform serving several teams currently
calls Anthropic directly from each team's agent code. A recent
Anthropic API incident took down every team's agents simultaneously
with no fallback, and separately, one team's bulk-classification
workflow occasionally exhausts the shared account's rate limit and
starves an unrelated interactive support-bot workflow.

A self-hosted LiteLLM proxy is introduced as the single entry point:

```yaml
model_list:
  - model_name: support-bot-model
    litellm_params: { model: anthropic/claude-sonnet-4, api_key: os.environ/ANTHROPIC_API_KEY }
  - model_name: support-bot-model
    litellm_params: { model: azure/gpt-4o-deployment, api_key: os.environ/AZURE_OPENAI_API_KEY, api_base: os.environ/AZURE_OPENAI_ENDPOINT }
    model_info: { tier: fallback }

router_settings:
  routing_strategy: usage-based-routing
  fallbacks:
    - support-bot-model: ["support-bot-model"]   # resolves to the azure fallback entry
  num_retries: 2
  allowed_fails: 3
  cooldown_time: 60

litellm_settings:
  success_callback: ["prometheus"]
  failure_callback: ["prometheus"]

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

Two virtual keys are issued so the batch-classification workflow can no
longer starve the interactive support bot:

```bash
curl -X POST http://gateway.internal/key/generate \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
  -d '{"models": ["support-bot-model"], "max_budget": 2000, "rpm_limit": 300}'
# support bot: high priority, modest rpm ceiling

curl -X POST http://gateway.internal/key/generate \
  -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
  -d '{"models": ["support-bot-model"], "max_budget": 500, "rpm_limit": 60}'
# batch classification: capped rpm so it can't consume the shared account limit
```

Both application code paths are updated to call the gateway's unified
endpoint with their respective virtual key instead of the Anthropic SDK
directly. Fallback is deliberately tested against a staging deployment
with an intentionally invalid Anthropic key (not the production key)
before rollout, confirming requests land on the Azure fallback within
an acceptable latency penalty. Fallback-trigger count is added as a
Grafana panel and alert alongside per-key rate-limit-hit count, so the
next Anthropic incident degrades gracefully and pages the platform team
directly instead of silently failing every downstream agent.

## Cross-references

- [llm-cost-and-latency-optimization](../llm-cost-and-latency-optimization/SKILL.md) — the deliberate cost/latency tuning layer above routing; this skill only covers moving traffic between providers, not shrinking what's sent per call.
- [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md) — the fast-triage workflow to run when a spike is provider- or routing-correlated rather than workflow-specific.
- [agent-architecture-design](../agent-architecture-design/SKILL.md) — where gateway placement fits into an agent system's overall architecture.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) — storing and rotating the provider credentials a gateway holds.
- [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md) — wiring the gateway's routing/cost/error metrics into dashboards and alerts.
