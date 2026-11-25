---
name: integrations-master
description: >-
  Master hub for integrating with the world's SaaS, dev tools, clouds, and APIs — at staff/principal
  depth. Includes Cloudixia full integrations ecosystem (17 modules, marketplace, certified apps).
  GitHub/GitLab, OAuth 2.1 + PKCE, webhooks, CI/CD, AWS/GCP/Azure, Slack, CRM, Zapier/n8n, CDC.
  Stripe → payments-master. Bundles 17 skills. Start with integrations-architecture-foundation.
---

# Integrations — Master Hub (World APIs & SaaS)

Connect your product to **any external system** — reliably, securely, idempotently, per-tenant.

> No hub can cover every API on Earth. This one gives **battle-tested patterns + category playbooks +
> a platform index** so the agent picks the right guide and implements it correctly the first time.

## Operating principles (every skill assumes these)

1. **Verify webhooks on the raw body**, dedupe by event id, ACK in <1s, process async.
2. **Idempotency everywhere** — keys on creates, a dedupe ledger on receives.
3. **Retry with jittered backoff + budget; circuit-break; DLQ + replay.** Never a bare `fetch`.
4. **OAuth 2.1 defaults** — PKCE on every code flow, refresh rotation, exact redirect match.
5. **Per-tenant, KMS-encrypted credentials**; least-privilege scopes; SSRF-guard outbound URLs.
6. **Adapter behind a port** — no vendor URLs leaking into business logic.

## Start here

1. **`integrations-architecture-foundation`** ⭐ — patterns, idempotency, retries, DLQ (always first)
2. Pick the auth model (`oauth-api-keys` or `webhooks-events`)
3. Pick the category skill (GitHub, Slack, CRM, …) or search **`integrations-platform-index`**
4. Layer in **`resilience-rate-limits`** and **`sync-engine-cdc`** for scale/reliability

## Workflow

```
Brief (what system? read vs write? per-user or org-wide? push or pull?)
  → architecture-foundation (shape + reliability)
  → oauth-api-keys OR webhooks-events (auth + verification)
  → category skill (provider deltas: endpoints, scopes, signature scheme)
  → resilience-rate-limits + sync-engine-cdc (throughput, drift, DLQ)
  → implement adapter + tests (fixtures/signatures) + observability
```

## Bundled skills (17)

**Platform ecosystems**
- **cloudixia-integrations-ecosystem** ⭐ — Cloudixia: 17 modules, Integration Marketplace (Cloudflare/Supabase/Vercel/Stripe tier), 100+ providers, **Certified Apps**, unified schema, APIs, UI, billing, RBAC, full catalog YAML. → `skills/cloudixia-integrations-ecosystem/GUIDE.md`

**Core patterns**
- **integrations-architecture-foundation** ⭐ — Hexagonal adapter, inbound/outbound webhooks, sync shapes, idempotency, DLQ, rate limits, KMS secrets, observability. → `skills/integrations-architecture-foundation/GUIDE.md`
- **integrations-oauth-api-keys** — OAuth 2.1 + PKCE, refresh rotation, client-credentials, JWT-bearer (GitHub App, Salesforce), DPoP/mTLS, KMS token vault. → `skills/integrations-oauth-api-keys/GUIDE.md`
- **integrations-webhooks-events** — Per-provider signature schemes (GitHub, Stripe, Shopify, Slack, Discord Ed25519, HubSpot v3, Notion, Linear, GitLab), raw-body HMAC, replay defense, signed outbound delivery. → `skills/integrations-webhooks-events/GUIDE.md`
- **integrations-resilience-rate-limits** 🆕 — Token bucket per tenant, adaptive concurrency, retries w/ budget, circuit breakers, queue topology + DLQ + replay. → `skills/integrations-resilience-rate-limits/GUIDE.md`
- **integrations-sync-engine-cdc** 🆕 — Full/incremental/CDC sync, durable cursors, transactional outbox, reconciliation, conflict resolution, resumable backfill. → `skills/integrations-sync-engine-cdc/GUIDE.md`

**Category playbooks**
- **integrations-github-gitlab-bitbucket** — GitHub App JWT→installation, Checks API, secondary rate limits, GitLab token, Bitbucket OAuth, gh CLI. → `skills/integrations-github-gitlab-bitbucket/GUIDE.md`
- **integrations-cicd-devops** — Actions/GitLab CI/Jenkins/CircleCI/Azure DevOps, **OIDC federation (no stored keys)**, deploy gates, signed artifacts/SLSA. → `skills/integrations-cicd-devops/GUIDE.md`
- **integrations-cloud-aws-gcp-azure** — Workload identity, presigned uploads, SQS/PubSub/Service Bus + DLQ, KMS, data residency. → `skills/integrations-cloud-aws-gcp-azure/GUIDE.md`
- **integrations-google-microsoft** — Google incremental sync + push; Microsoft Graph change-notification subscriptions (validation, lifecycle, expiry). → `skills/integrations-google-microsoft/GUIDE.md`
- **integrations-slack-discord-teams** — Slack v0 signing + 3s ACK, Discord Ed25519 interactions, Teams Graph/Bot Framework, per-workspace tokens. → `skills/integrations-slack-discord-teams/GUIDE.md`
- **integrations-pm-notion-linear-jira** — Linear GraphQL, Jira REST v3, Notion 2026 webhooks, loop-safe two-way sync. → `skills/integrations-pm-notion-linear-jira/GUIDE.md`
- **integrations-crm-salesforce-hubspot** — SF JWT-bearer + Bulk 2.0 + CDC, HubSpot batch upsert + v3 webhooks, external-id upsert. → `skills/integrations-crm-salesforce-hubspot/GUIDE.md`
- **integrations-commerce-shopify-woocommerce** — Shopify Admin GraphQL + base64 HMAC + GDPR webhooks, WooCommerce; payments → payments-master. → `skills/integrations-commerce-shopify-woocommerce/GUIDE.md`
- **integrations-marketing-analytics** — Server-side CDP, Meta CAPI + pixel dedup, GA4 MP, SHA-256 PII hashing, Consent Mode v2. → `skills/integrations-marketing-analytics/GUIDE.md`
- **integrations-ipaas-n8n-zapier** — Zapier REST Hooks vs polling, exposing your product as a platform (OAuth + MCP), embedding n8n. → `skills/integrations-ipaas-n8n-zapier/GUIDE.md`
- **integrations-platform-index** — 90+ platforms → skill + auth type + current docs URL + an unknown-platform protocol. → `skills/integrations-platform-index/GUIDE.md`

## Pairs well with

`backend-api-master` (integrations-pro, google-sign-in), `payments-master` (Stripe/PSPs),
`communications-master`, `git-workflow-master` (gh CLI), `devops-master`, `business-master` (CRM/ERP),
`ai-mcp-master` (expose tools to agents via MCP), `analytics-master` (PostHog/flags).

## Note

Bundled skills use `GUIDE.md` so only this master appears in Cursor's skills list. Each GUIDE keeps its
`name` stable for routing; read the GUIDE for copy-paste production code.
