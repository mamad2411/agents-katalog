---
name: fabrico-preparing-applications-for-saas
description: "Prepares applications for SaaS delivery through tenant isolation, identity, roles, entitlements, metering, billing boundaries, auditability, lifecycle operations, and production safeguards. Use whenever building a new application, materially extending an existing application, adding organizations or subscriptions, or reviewing SaaS readiness."
---

# Preparing Applications for SaaS

Make every application ready to grow into a secure SaaS product. Establish tenant-aware boundaries and operational seams without adding speculative payment flows or features outside the product scope.

<readiness-boundary>

SaaS-ready means that identity, data ownership, authorization, limits, background work, and operations can support multiple customers safely. It does not require connecting a billing provider before pricing and billing are in scope.

</readiness-boundary>

## SaaS-Readiness Process

Track this checklist:

```text
Progress:
- [ ] Define tenant and account ownership
- [ ] Choose pooled, bridge, or silo isolation from current requirements
- [ ] Enforce tenant isolation across every execution path
- [ ] Centralize roles, entitlements, and limits
- [ ] Add metering and billing boundaries when required
- [ ] Cover onboarding, lifecycle, audit, and support operations
- [ ] Add production and compliance safeguards
- [ ] Prove isolation and lifecycle behavior with automated tests
```

### 1. Define tenant and account ownership

- Add a SaaS-readiness section to the existing research or implementation plan.
- Choose one canonical tenant concept, normally `Organization` or `Workspace`, and define membership, ownership, invitation, suspension, and deletion semantics.
- Default to pooled compute and a shared MySQL schema with explicit tenant ownership because this is normally the cheapest operational model. Use bridge or silo isolation only for measured noisy-neighbor, recovery, residency, regulatory, contractual, or tenant-economic requirements.
- Distinguish platform administrators, tenant owners, tenant members, and end users. Do not infer platform-level authority from tenant roles.
- Require every tenant-owned record to have an unambiguous ownership path. For MySQL, include tenant columns in relevant unique constraints and indexes.

### 2. Enforce tenant isolation

- Resolve tenant context once at each entry point and pass it explicitly through application services, policies, events, jobs, cache keys, file paths, search indexes, exports, and audit records.
- Scope reads and writes on the server. Never trust a tenant identifier supplied by the browser without membership and permission checks.
- Prefix Redis cache, lock, rate-limit, and idempotency keys with tenant identity. Serialize tenant context into queued jobs and re-authorize sensitive work when it executes.
- Prevent cross-tenant references with schema constraints where practical and application-level invariants where the database cannot express them.
- Add negative tests that attempt cross-tenant reads, writes, searches, exports, file access, and queued operations.

### 3. Centralize access and product policy

- Keep roles and permissions in policies or a central authorization layer. Do not scatter role-name checks through controllers and UI components.
- Model plan capabilities as entitlements and quantitative restrictions as limits. Evaluate both server-side; the UI may explain or disable unavailable actions but is not the enforcement boundary.
- Implement only entitlements and limits required by current plans. Do not build a generic pricing engine, experimentation platform, or policy language for hypothetical offers.
- Keep feature flags separate from commercial entitlements. Define precedence and safe defaults when configuration is missing.
- Apply rate limits and abuse controls per tenant and actor, not only per IP address.

### 4. Prepare metering and billing

- Define billable events with stable names, tenant identity, quantity, timestamp, source, idempotency key, and correlation ID.
- Keep usage measurement append-only or otherwise auditable. Do not calculate invoices from mutable operational rows without a reproducible ledger.
- Put billing providers behind an adapter when billing is in scope. Treat provider webhooks as untrusted: verify signatures, deduplicate events, preserve ordering rules, and make handlers replay-safe.
- Separate subscription state, entitlement state, and payment state so temporary provider failures do not corrupt authorization decisions.
- Do not connect a paid billing provider, create products, or send invoices without explicit user authorization.
- Do not implement metering tables or a billing ledger before a billable dimension is in scope. Preserve stable operation names and tenant context so metering can be added without rewriting domain behavior.

### 5. Cover tenant lifecycle and operations

- Implement or plan onboarding, invitations, member removal, ownership transfer, suspension, reactivation, export, retention, and deletion.
- Store timestamps in UTC and preserve user or tenant timezone and locale preferences at presentation boundaries.
- Add an audit trail for authentication, membership, permission, entitlement, billing, export, impersonation, and destructive events.
- Make support impersonation explicit, time-bounded, prominently indicated, reason-captured, least-privileged, and fully audited.
- Ensure backups, restores, imports, and exports preserve tenant boundaries and can target one tenant when required.

### 6. Add production safeguards

- Keep secrets out of source and tenant configuration. Validate configuration at startup and define secure defaults.
- Add health checks, structured logs, traces, tenant-aware metrics, queue monitoring, and alerts for saturation and repeated failures.
- Measure consumption per tenant before isolating infrastructure. Prefer quotas, indexes, queue lanes, and dedicated capacity for the offending workload before duplicating an entire tenant stack.
- Design migrations for rolling deployment and growing datasets. Avoid unbounded table rewrites and synchronous tenant-wide work in request paths.
- Define data classification, retention, deletion, portability, and incident-response ownership. Add region or residency controls only when requirements justify them.

### 7. Verify readiness

```text
Validation:
- [ ] Every tenant-owned record has a clear ownership path and suitable MySQL indexes
- [ ] HTTP, queue, event, cache, file, search, export, and audit paths preserve tenant context
- [ ] Cross-tenant access attempts fail in automated tests
- [ ] Roles, entitlements, feature flags, limits, and rate limits are enforced server-side
- [ ] Billable events and webhooks are idempotent and auditable when billing is in scope
- [ ] Suspension, ownership transfer, export, and deletion have defined behavior
- [ ] Platform-admin and support access is explicit and audited
- [ ] Logs, metrics, backups, and restore procedures remain tenant-aware
```

## Connected Skills

- `fabrico-architecture-designing` - for tenancy, service boundaries, and scaling decisions
- `fabrico-building-lean-applications` - for pooled defaults, build-versus-buy gates, cost allocation, and evidence-based isolation changes
- `fabrico-sql-and-database-understanding` - for tenant keys, constraints, indexes, and migration safety
- `fabrico-implementing-backend` - for policies, services, queues, webhooks, and tests
- `fabrico-managing-secrets` - for billing, email, storage, and integration credentials
- `fabrico-implementing-observability` - for tenant-aware metrics, traces, alerts, and SLOs
- `fabrico-preparing-applications-for-ai` - for tenant-aware AI data, quotas, metering, and tool authorization
