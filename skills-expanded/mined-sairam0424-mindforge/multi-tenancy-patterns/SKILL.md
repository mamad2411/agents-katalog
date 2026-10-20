---
name: multi-tenancy-patterns
version: 1.0.0
min_mindforge_version: 0.3.0
status: stable
triggers: multi-tenancy, tenant isolation, shared database tenancy, row-level security, tenant context, data isolation, tenant provisioning, tenant migration, tenant routing, schema per tenant, tenant-aware query, tenant onboarding
---

# Skill — Multi-Tenancy Patterns

## When this skill activates
Any task involving multi-tenant architecture, tenant isolation, shared database
strategies, tenant context propagation, or tenant provisioning workflows.

## Mandatory actions when this skill is active

### Before designing multi-tenancy
1. Assess isolation requirements (regulatory, security, performance).
2. Determine tenant scale (10 tenants vs 10,000 tenants).
3. Choose isolation level based on business requirements, not engineering convenience.

### Isolation levels

**Shared Database + Row-Level Security (RLS):**
- Single database, single schema, tenant_id column on every table.
- Cheapest to operate, easiest to deploy.
- Least isolated — bugs can leak data between tenants.
- Best for: SaaS with many small tenants, cost-sensitive.
- Risk: a missing WHERE clause exposes all tenant data.

**Schema per tenant:**
- Single database, separate schema per tenant.
- Moderate isolation and moderate cost.
- Migrations must run per-schema (automation required).
- Best for: moderate tenant count (< 1000), need logical separation.

**Database per tenant:**
- Completely separate database per tenant.
- Maximum isolation, maximum cost.
- Independent scaling, independent backup/restore.
- Best for: enterprise customers, regulatory requirements, high-value tenants.

### RLS implementation (PostgreSQL)

```sql
-- Enable RLS on the table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policy that filters by tenant
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Force RLS even for table owner
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- Set tenant context at connection level
SET app.current_tenant = 'tenant-uuid-here';
```

**Critical rules:**
- RLS policies must be impossible to bypass from application code.
- NEVER use a superuser connection that bypasses RLS in application code.
- Test RLS with a dedicated "tenant leak" test suite.
- Add a CHECK constraint: `tenant_id IS NOT NULL` on every tenant-scoped table.

### Tenant context propagation

**Middleware pattern:**
```
Request → Extract tenant → Validate → Set context → Handler → Response
```

**Extraction sources (priority order):**
1. JWT claim (most secure — server-signed).
2. Subdomain: `tenant1.app.com` → tenant_id lookup.
3. Path prefix: `app.com/tenant1/...` → extract from URL.
4. Header: `X-Tenant-ID` (for service-to-service only).

**Propagation through the stack:**
- HTTP layer: middleware sets tenant in request context.
- Service layer: receives tenant from context, passes to repositories.
- Data layer: sets session variable before executing queries.
- Background jobs: serialize tenant_id in job payload, restore before processing.

### Tenant routing

**Subdomain routing:**
- `tenant1.app.com`, `tenant2.app.com`
- Requires wildcard DNS and TLS certificate.
- Clean separation, easy to identify tenant.
- Custom domains: CNAME tenant1.com → tenant1.app.com.

**Path-based routing:**
- `app.com/tenant1/dashboard`, `app.com/tenant2/dashboard`
- Simpler DNS/TLS setup.
- Requires path prefix stripping in routing layer.

**Header-based routing (internal only):**
- `X-Tenant-ID: tenant-uuid`
- For service-to-service communication within the platform.
- Never expose to end users (spoofing risk).

### Tenant provisioning

**Onboarding workflow:**
1. Create tenant record (name, plan, config).
2. Provision resources (schema/database if applicable).
3. Run seed data (default roles, settings, sample data).
4. Configure DNS/routing (subdomain or custom domain).
5. Send welcome notification.

**Automation requirements:**
- Provisioning must be fully automated (no manual steps).
- Must complete in < 30 seconds for shared DB, < 5 minutes for isolated DB.
- Rollback on failure — no half-provisioned tenants.

### Tenant-aware migrations

**Shared DB (RLS):**
- Standard migrations — all tenants share the schema.
- Add tenant_id to new tables, backfill existing tables.

**Schema per tenant:**
- Migration runner must iterate all tenant schemas.
- Parallel execution for speed, with error handling per-tenant.
- Failed migrations must not block other tenants.

**Database per tenant:**
- Migration runner connects to each tenant DB.
- Version tracking per-tenant (some may be ahead/behind during rollout).
- Canary strategy: migrate one tenant first, verify, then batch.

### Testing multi-tenancy

- **Isolation tests:** Create 2+ tenants, write data as tenant A, verify tenant B cannot see it.
- **Context tests:** Verify tenant context survives async operations (background jobs, event handlers).
- **Edge cases:** What happens with no tenant context? (Must fail closed, not open.)
- **Performance:** Verify RLS does not degrade query performance significantly (check EXPLAIN).
- **All environments** must have multiple tenants configured (including development).

## Self-check before task completion
- [ ] Did I follow the mandatory actions for this skill?
- [ ] Did I apply the patterns appropriate to the context?
- [ ] Did I verify the implementation meets the criteria above?
- [ ] Did I document decisions and trade-offs made?
