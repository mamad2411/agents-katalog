---
name: api-marketplace
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: API marketplace internal, API discovery platform, API versioning governance, API deprecation workflow, API developer onboarding, API portal, API catalog, API consumer management, API usage tracking, API lifecycle governance, internal API standard, API documentation portal
compose: api-versioning
---

# Skill — API Marketplace

## When this skill activates

This skill activates when the user is designing or implementing an internal API marketplace. This includes API discovery platforms, versioning governance, deprecation workflows, developer onboarding for API consumers, API portals, API catalogs, consumer management, usage tracking, API lifecycle governance, internal API standards, and documentation portals.

## Mandatory actions when this skill is active

### Before writing any code

1. Inventory all internal APIs (REST, GraphQL, gRPC, event streams) and assess current discoverability and documentation quality.
2. Define API lifecycle stages (proposal, alpha, beta, stable, deprecated, retired) and governance requirements for each stage.
3. Identify API consumer personas (internal developers, data teams, mobile engineers) and their discovery and onboarding needs.
4. Establish API standards (authentication, versioning, error handling, pagination, rate limiting) that all APIs must follow.
5. Assess current API sprawl: duplicate APIs, shadow APIs (not documented), orphaned APIs (no owner).

### During implementation

- **API Discovery:** Central catalog searchable by domain, team, capability, or keyword. Each API should have: name, description, owner, SLA, OpenAPI spec, example requests, status (alpha/beta/stable/deprecated). Discovery should return results in under 500ms.
- **API Portal:** Single entry point for all internal APIs. Include: catalog, interactive docs (Swagger UI, GraphQL Playground), try-it-now sandbox, code examples in 3+ languages, changelog per API. Portal must be indexed by internal search.
- **Versioning Governance:** Enforce consistent versioning strategy (see `api-versioning` skill). APIs must publish a deprecation policy (minimum 6-month notice for stable APIs). Breaking changes require new major version.
- **Deprecation Workflow:** Automated workflow: API owner announces deprecation → sunset headers added → usage monitoring dashboard → consumer outreach (email + Slack) → grace period (6 months) → removal. Track deprecation status in catalog.
- **Developer Onboarding:** New API consumers should go from discovery to first successful API call in under 15 minutes. Include: API key provisioning (self-service), quick-start guide, sandbox environment, example code, troubleshooting tips.
- **Consumer Management:** Track which teams consume which APIs. Use API keys or OAuth clients for attribution. Consumer dashboard shows: usage metrics, quota limits, deprecation notices, breaking change alerts.
- **Usage Tracking:** Collect per-consumer metrics: request count, error rate, latency, quota consumption. Expose to API owners via dashboard. Alert when consumers exceed 80% of quota or hit high error rates.
- **API Lifecycle Governance:** Alpha APIs can break without notice. Beta APIs require 1-month deprecation notice. Stable APIs require 6-month notice. Retired APIs return 410 Gone. Enforce via automated policy checks.
- **Internal API Standards:** All APIs must: use standard authentication (OAuth2 or API keys), include OpenAPI spec, provide health check endpoint, emit structured logs, track RED metrics. Standards enforced via linting (Spectral) and API gateway policies.

### After implementation

- Verify the API catalog includes 100% of production-facing internal APIs with ownership and OpenAPI specs.
- Confirm API portal enables discovery-to-first-call in under 15 minutes via user testing.
- Validate deprecation workflows include automated sunset headers and consumer outreach.
- Ensure usage tracking is per-consumer with dashboards for API owners.
- Check that API standards are enforced via automated linting and gateway policies.

## Self-check before task completion

- [ ] API catalog is searchable and includes 100% of internal APIs with ownership and specs.
- [ ] API portal enables discovery-to-first-call in under 15 minutes.
- [ ] Versioning governance enforces consistent strategy across all APIs.
- [ ] Deprecation workflow includes sunset headers, monitoring, and 6-month grace period.
- [ ] Developer onboarding is self-service with API key provisioning and sandbox access.
- [ ] Consumer management tracks per-team usage with quota limits and alerts.
- [ ] Usage tracking provides per-consumer metrics to API owners via dashboard.
- [ ] API lifecycle governance enforces deprecation policies automatically.
- [ ] Internal API standards are enforced via linting and API gateway policies.
