---
name: skill-unified-analytics
description: Use for SaaS/product analytics architecture, event taxonomy, telemetry instrumentation, funnels, admin dashboards, billing metrics, activation, retention, attribution, privacy guardrails, observability, and cross-provider reporting.
category: analytics
risk: low
source: local-product-analytics-patterns
---

# Skill Unified Analytics

Use this skill when adding or improving telemetry, metrics, funnels, product dashboards, admin reporting, billing analytics, or usage observability. Treat analytics as a product contract, not incidental logging.

## Workflow

1. Define the decision the metric supports before adding events or charts.
2. Inventory existing providers, server logs, database tables, queues, webhooks, feature flags, and analytics helpers.
3. Choose the source of truth: client event, server event, durable audit log, billing provider, warehouse table, or pre-aggregated view.
4. Define the event or metric contract before implementation: name, trigger, owner, required properties, optional properties, identity fields, privacy level, and version.
5. Instrument once at the boundary that best represents truth. Avoid duplicate client and server events unless reconciliation is intentional.
6. Validate with a local log, test, provider debugger, database row, or dashboard query before completion.

## Event Taxonomy

- Use names in a stable pattern such as `object_action` or the project's existing convention.
- Prefer business events over UI implementation details: `checkout_started`, `subscription_upgraded`, `report_exported`.
- Include context that enables segmentation: tenant/account, user role, plan, feature, source, campaign, environment, and request/job identifiers where allowed.
- Do not send raw secrets, tokens, passwords, full payment data, private content, or unnecessary PII.
- Version payloads when shape or semantics change: `schema_version`, migration notes, or compatibility handling.
- Keep idempotency keys or event IDs for server events that may retry.

## SaaS Metric Map

- Activation: signup completed, onboarding completed, first useful action, invitation accepted, workspace created.
- Engagement: active account, retained user, feature used, report viewed, export completed, workflow completed.
- Revenue: trial started, checkout started, payment succeeded, subscription changed, invoice failed, refund, churn.
- Usage and cost: quota consumed, job processed, AI tokens/spend, storage used, seats used, API calls.
- Reliability: job failed, webhook failed, sync delayed, queue latency, API error, retry exhausted.
- Admin and security: permission changed, manual override, impersonation started, user blocked, audit export, policy violation.

## Dashboard Rules

- Put metric definitions next to the dashboard code or query when the project has no central metric registry.
- Show period, timezone, freshness, filters, and data source for decision-making dashboards.
- Use indexed tables, materialized views, cached summaries, or warehouse queries for growing datasets.
- Make breakdowns actionable: plan, cohort, channel, workspace, role, geography, feature, or lifecycle stage.
- Include no-data and partial-data states so blank charts are not mistaken for zero.
- Align chart formatting with product UI: units, precision, currency, date granularity, and comparison periods.

## Privacy And Reliability

- Separate behavioral analytics from trusted business records. Use server-side durable records for billing, entitlements, security, and admin actions.
- Respect consent, regional rules, and tenant boundaries already present in the product.
- Keep analytics failures from breaking the user flow unless the event is part of a required audit or billing path.
- Log enough implementation detail to debug missing events without exposing sensitive data.
- Document intentional sampling, filtering, deduplication, and backfills.

## Validation Checklist

- Event fires exactly once for the intended trigger.
- Required properties are present and typed.
- Tenant/user identity is correct and privacy-safe.
- Failure paths and retries are handled.
- Dashboard queries match the event definition and use realistic sample data.
- Tests, provider debug output, query results, or logs are checked before claiming completion.

