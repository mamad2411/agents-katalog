---
name: saas-pro
description: "Multi-tenant architecture, billing, subscription management, onboarding, RBAC. Use when building or reviewing SaaS platform features."
---

# SaaS Pro

## Purpose

Build production SaaS platforms: multi-tenancy, subscription billing, user onboarding, RBAC, feature flags, and usage metering.

## When to Use

**Use this when:**
- Building or extending a multi-tenant application with per-tenant data isolation
- Integrating Stripe subscriptions, webhooks, or usage-based billing
- Designing RBAC, feature flags, or onboarding flows for a B2B SaaS product

**Use this ESPECIALLY when:**
- The data model mixes tenant rows in shared tables and there is no enforced isolation layer
- Subscription state in the database can drift from Stripe (missing webhook handlers, no idempotency)
- A new pricing tier or feature gate needs to roll out gradually without a full redeploy

**Don't skip when:**
- Any endpoint reads or writes tenant data — every query must be scoped to the authenticated tenant
- Handling Stripe webhook events — payment failures and subscription changes require explicit, idempotent handlers
- Adding a plan-gated feature — usage limits and feature flags must be checked server-side, never only in the UI

## Core Patterns

### 1. Multi-Tenant Architecture

```typescript
// Row-level security for tenant isolation
// Option A: Discriminator column (simpler, shared DB)
interface Project {
  id: string
  name: string
  tenantId: string  // Every row belongs to a tenant
  // ...
}

// Global middleware enforces tenant isolation
async function requireTenant(req, res, next) {
  const tenantId = req.headers['x-tenant-id']
  if (!tenantId) return res.status(400).json({ error: 'X-Tenant-Id header required' })
  req.tenantId = tenantId

  // Verify user has access to this tenant
  const membership = await db.tenantMembership.findUnique({
    where: { userId_tenantId: { userId: req.user.id, tenantId } }
  })
  if (!membership) return res.status(403).json({ error: 'Not a member of this tenant' })

  next()
}

// All queries scoped by tenantId
const projects = await db.projects.findMany({
  where: { tenantId: req.tenantId, ownerId: req.user.id }
})
```

### 2. Subscription & Billing

```typescript
// Stripe integration
stripe.subscriptions.create({
  customer: customer.id,
  items: [{ price: priceId }],
  trial_period_days: 14,
  metadata: { tenantId: tenant.id },
})

// Webhook handler
app.post('/webhooks/stripe', async (req, res) => {
  const event = stripe.webhooks.constructEvent(req.body, signature, webhookSecret)

  switch (event.type) {
    case 'customer.subscription.updated':
    case 'customer.subscription.deleted':
      await updateTenantSubscription(event.data.object)
      break
    case 'invoice.payment_succeeded':
      await handlePaymentSuccess(event.data.object)
      break
    case 'invoice.payment_failed':
      await handlePaymentFailure(event.data.object)
      break
  }
  res.json({ received: true })
})
```

### 3. Feature Flags

```typescript
// DB-backed feature flags
interface FeatureFlag {
  name: string
  enabled: boolean
  tenantOverrides: Record<string, boolean>  // per-tenant overrides
  userOverrides: Record<string, boolean>    // per-user overrides
  rolloutPercentage: number                  // gradual rollout
}

function isFeatureEnabled(flagName: string, req: Request): boolean {
  const flag = await db.featureFlags.findUnique({ where: { name: flagName } })
  if (!flag) return false

  // Per-user override (highest priority)
  if (flag.userOverrides?.[req.user.id] !== undefined) return flag.userOverrides[req.user.id]
  // Per-tenant override
  if (flag.tenantOverrides?.[req.tenantId] !== undefined) return flag.tenantOverrides[req.tenantId]
  // Gradual rollout
  if (flag.rolloutPercentage < 100) {
    return hash(`${req.tenantId}:${flagName}`) % 100 < flag.rolloutPercentage
  }
  return flag.enabled
}
```

### 4. Usage Metering

```typescript
// Track API usage per tenant
async function trackUsage(tenantId: string, metric: string, amount: number = 1) {
  const key = `usage:${metric}:${tenantId}:${formatDate(new Date(), 'yyyy-MM')}`
  await redis.incrby(key, amount)
  await redis.expire(key, 60 * 60 * 24 * 32)  // Keep for 32 days
}

// Check limits
async function checkUsageLimit(tenantId: string, metric: string, limit: number): Promise<boolean> {
  const current = await redis.get(`usage:${metric}:${tenantId}:${formatDate(new Date(), 'yyyy-MM')}`)
  return parseInt(current || '0') < limit
}
```

### Checklist

- [ ] Tenant isolation at DB level (RLS or discriminator)
- [ ] Subscription plans with feature mapping
- [ ] Trial period with clear upgrade path
- [ ] Usage metering and rate limiting per tenant
- [ ] Feature flags for gradual rollouts
- [ ] Onboarding flow (wizard, template, integration)
- [ ] Analytics dashboard (MRR, churn, LTV, NPS)
- [ ] Self-serve billing (upgrade, downgrade, cancel)
- [ ] Proration handling for plan changes
- [ ] Multi-tenant data export/deletion (GDPR)

## Related Skills

- **backend-senior-engineer** — tenant middleware, webhook handlers, and usage-tracking endpoints are backend code; use for implementation guidance once SaaS architecture decisions are made here
- **postgres-pro** — row-level discriminator columns, RLS policies for tenant isolation, and schema migrations for plan changes require advanced PostgreSQL; defer to postgres-pro for query and migration specifics
- **supabase-pro** — when the SaaS stack is built on Supabase, RLS and auth patterns from supabase-pro replace the custom middleware shown here; the two skills are complementary
- **security-reviewer** — tenant isolation boundaries, API key scoping, and GDPR data-deletion flows are security concerns; cross-reference when designing data export, deletion, or impersonation features
- **code-reviewer** — subscription tier enforcement and usage limit checks must be consistent across all API endpoints; use when auditing gating logic at the route layer
- **test-engineer** — multi-tenant test isolation (separate tenants per test, seeded plans) is non-trivial; use together when writing integration tests for billing or feature-flag paths
