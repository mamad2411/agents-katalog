---
name: self-serve-infrastructure
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: self-serve infrastructure, infrastructure abstraction layer, team resource provisioning, resource quota management, infrastructure guardrail, infrastructure self-service, cloud account vending, environment provisioning, developer infrastructure, resource request automation, infrastructure API, sandbox environment
---

# Skill — Self-Serve Infrastructure

## When this skill activates

This skill activates when the user is designing or implementing self-service infrastructure capabilities. This includes building infrastructure abstraction layers, enabling team resource provisioning, managing resource quotas, implementing infrastructure guardrails, cloud account vending, environment provisioning, and infrastructure APIs that allow developers to request and manage infrastructure without manual approval workflows.

## Mandatory actions when this skill is active

### Before writing any code

1. Audit current infrastructure request workflows: identify bottlenecks, approval layers, and average time from request to provisioned resource.
2. Define resource taxonomy (compute, storage, database, network, secrets) and ownership model (team-owned, platform-managed, shared).
3. Establish cost budgets and quota policies per team and environment type (production vs non-production).
4. Identify compliance requirements that must be enforced via policy-as-code (data residency, encryption, network isolation).
5. Map out the guardrails that prevent misconfiguration while still enabling developer autonomy.

### During implementation

- **Infrastructure Abstraction Layer:** Hide cloud provider primitives behind domain-specific abstractions (e.g., "web service", "background worker", "database" instead of EC2/RDS/ECS). Abstractions should map to 80% of use cases; provide escape hatches for the 20%.
- **Account Vending:** Automate AWS/GCP/Azure account creation with pre-configured networking, security groups, IAM roles, and cost monitoring. Vending should complete in under 10 minutes and include automatic tagging for cost attribution.
- **Resource Quotas:** Enforce per-team quotas on compute, storage, and API calls. Quotas should be soft limits with alerts (80% threshold) and hard limits that block provisioning. Include self-service quota increase requests with auto-approval for small increases (20%).
- **Guardrails (Policy-as-Code):** Use OPA, Sentinel, or Cloud Custodian to enforce rules: no public S3 buckets, require encryption, require tagging, enforce naming conventions, block expensive instance types in non-prod. Guardrails should fail-fast at provisioning time, not after resources are created.
- **Environment Provisioning:** Enable one-click environment creation (dev, staging, prod, per-developer sandbox). Environments should be ephemeral for non-prod, with automatic cleanup after N days of inactivity. Include cost estimates before provisioning.
- **Infrastructure API:** Expose infrastructure capabilities via REST or GraphQL API. Each endpoint should return a tracking ID for async provisioning, with status polling or webhooks. Include rate limiting and audit logging.
- **Sandbox Safety:** Sandboxes should auto-delete after 7 days, have cost caps ($50-$200/month), and include network isolation from production. Developers should receive cost alerts at 50%, 80%, 100% of quota.

### After implementation

- Verify infrastructure provisioning time is reduced by at least 80% (from days to minutes).
- Confirm guardrails prevent at least 90% of misconfiguration issues that previously required manual remediation.
- Validate resource quotas are enforced and quota breach attempts are logged and alerted.
- Ensure environment provisioning includes cost estimates and auto-cleanup for ephemeral environments.
- Check that infrastructure API requests include tracking IDs and status endpoints for async operations.

## Self-check before task completion

- [ ] Infrastructure abstraction layer covers 80% of use cases with escape hatches for the rest.
- [ ] Account vending completes in under 10 minutes with pre-configured security and networking.
- [ ] Resource quotas are enforced with soft limits (alerts at 80%) and hard limits (block at 100%).
- [ ] Guardrails use policy-as-code and fail at provisioning time, not post-creation.
- [ ] Environment provisioning includes cost estimates and automatic cleanup policies.
- [ ] Infrastructure API has async tracking, status polling, rate limiting, and audit logs.
- [ ] Sandbox environments have cost caps, auto-deletion, and network isolation from production.
