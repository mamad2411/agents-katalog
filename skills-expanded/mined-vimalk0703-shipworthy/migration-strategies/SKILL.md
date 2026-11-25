---
name: migration-strategies
description: Choose and execute the right migration strategy for system changes -- strangler fig, parallel run, expand-contract, blue-green, or feature flag migration. Each with rollback plans and verification strategies.
invoke_when: Use when migrating between systems, replacing a legacy service, changing databases, switching providers, refactoring a monolith into microservices, or planning any large-scale system change.
---

# Migration Strategies

## Core Principle

Every migration must be reversible until fully verified. Never cut over to a new system without running it alongside the old one first. The migration strategy you choose determines your risk profile, rollback speed, and verification confidence.

---

## Decision Matrix

| Strategy | Best For | Rollback Speed | Complexity | Data Migration? |
|---|---|---|---|---|
| Strangler Fig | Replacing a monolith with microservices | Fast (route traffic back) | Medium | Gradual |
| Parallel Run | Replacing a critical data processing system | Instant (read from old) | High | Yes, bidirectional |
| Expand-Contract | Database schema changes, API changes | Medium (revert schema) | Low-Medium | In-place |
| Blue-Green | Full application deployments | Instant (swap environments) | Medium | Shared or replicated |
| Feature Flag Migration | Replacing internal components or algorithms | Instant (toggle flag) | Low | Depends |

---

## 1. Strangler Fig Pattern

### When to Use

- Migrating from a monolith to microservices.
- Replacing a legacy system piece by piece over weeks or months.
- You want to avoid a big-bang rewrite.

### How It Works

1. Place a routing layer (API gateway, reverse proxy) in front of the legacy system.
2. Build new functionality in the new system.
3. Route traffic for specific endpoints/features to the new system.
4. Gradually expand the new system's surface area until the legacy system handles nothing.
5. Decommission the legacy system.

```
Phase 1:  Client -> Gateway -> Legacy System (all traffic)
Phase 2:  Client -> Gateway -> Legacy System (most traffic)
                            -> New Service A (/users)
Phase 3:  Client -> Gateway -> Legacy System (some traffic)
                            -> New Service A (/users)
                            -> New Service B (/orders)
Phase N:  Client -> Gateway -> New Services (all traffic)
                               Legacy System (decommissioned)
```

### Implementation

```typescript
// Gateway routing configuration -- gradually shift routes
const routes = [
  // Migrated routes -- point to new services
  { path: '/api/users/*', target: 'user-service.internal', migrated: true },
  { path: '/api/orders/*', target: 'order-service.internal', migrated: true },

  // Not yet migrated -- point to legacy
  { path: '/api/inventory/*', target: 'legacy-monolith.internal', migrated: false },
  { path: '/api/reports/*', target: 'legacy-monolith.internal', migrated: false },

  // Catch-all -- legacy handles anything not explicitly routed
  { path: '/*', target: 'legacy-monolith.internal', migrated: false },
];
```

### Rollback Plan

- Revert the gateway routing rule to send traffic back to the legacy system.
- Rollback time: seconds to minutes (just a config change).
- Data consideration: if the new service wrote data, you may need to sync it back to legacy.

### Verification Strategy

- Compare response bodies from old and new systems for the same requests (shadow traffic).
- Monitor error rates, latency, and business metrics per migrated route.
- Run functional tests against both systems in parallel before switching.

---

## 2. Parallel Run

### When to Use

- Replacing a critical system where correctness is paramount (payment processing, financial calculations, data pipelines).
- You need high confidence that the new system produces the same results.
- The cost of a bug in the new system is very high.

### How It Works

1. Send every request to both the old and new systems.
2. Return the response from the old system to the user (new system is in shadow mode).
3. Compare results from both systems, log discrepancies.
4. Fix discrepancies until the match rate is 99.99%+.
5. Switch reads to the new system, keep writes to both.
6. Once fully verified, decommission the old system.

```python
async def process_payment(request: PaymentRequest) -> PaymentResponse:
    # Run both systems in parallel
    old_result, new_result = await asyncio.gather(
        old_payment_service.process(request),
        new_payment_service.process(request),
        return_exceptions=True,
    )

    # Log discrepancies for analysis
    if not results_match(old_result, new_result):
        logger.warning("Payment processing discrepancy", extra={
            "request_id": request.id,
            "old_result": serialize(old_result),
            "new_result": serialize(new_result),
            "differences": diff(old_result, new_result),
        })
        metrics.increment("migration.discrepancy", tags={"system": "payments"})

    # Always return the old system's result during parallel run
    return old_result
```

### Rollback Plan

- Stop sending traffic to the new system.
- Rollback time: instant (old system was always the source of truth).
- No data migration needed -- old system was the authoritative source throughout.

### Verification Strategy

- Track match rate between old and new system responses.
- Categorize discrepancies (timing differences, floating point, genuine bugs).
- Set a threshold: do not cut over until match rate exceeds 99.99% for 7 consecutive days.
- Run a reconciliation report comparing stored outcomes from both systems.

---

## 3. Expand-Contract (Database Migrations)

### When to Use

- Database schema changes (renaming columns, changing types, splitting tables).
- API field changes that must remain backward compatible.
- Any change to a shared data structure that has multiple consumers.

### How It Works (Three Phases)

**Phase 1 -- Expand:** Add the new structure alongside the old one. Write to both.

**Phase 2 -- Migrate:** Backfill the new structure with existing data. Verify all consumers use the new structure.

**Phase 3 -- Contract:** Remove the old structure.

### Example: Renaming a Database Column

```sql
-- Phase 1: EXPAND -- Add new column, write to both
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);

-- Application code writes to both:
-- UPDATE users SET name = $1, display_name = $1 WHERE id = $2;

-- Phase 2: MIGRATE -- Backfill existing data
UPDATE users SET display_name = name WHERE display_name IS NULL;

-- Update application to read from display_name
-- Verify all consumers have migrated to reading display_name
-- Monitor: SELECT COUNT(*) FROM users WHERE display_name IS NULL; -- should be 0

-- Phase 3: CONTRACT -- Remove old column (only after all consumers are verified)
ALTER TABLE users DROP COLUMN name;
```

### Rollback Plan

- **Phase 1:** Drop the new column. No data loss.
- **Phase 2:** Revert application to read from the old column. Old column still has correct data.
- **Phase 3:** This is irreversible. Only execute after all consumers are verified and a sufficient bake period (minimum 7 days).

### Verification Strategy

- Phase 1: Verify both columns receive writes (query counts).
- Phase 2: Verify backfill completeness (no NULL values in new column). Run integration tests.
- Phase 3: Verify no application code references the old column name (code search).

---

## 4. Blue-Green Deployment

### When to Use

- Full application deployments where you want instant rollback.
- Infrastructure migrations (new Kubernetes cluster, new cloud region).
- When the application is stateless or uses a shared database.

### How It Works

1. **Blue** is the current production environment.
2. Deploy the new version to **Green** (identical but idle environment).
3. Run smoke tests against Green.
4. Switch the load balancer / DNS to point to Green.
5. Green is now production. Blue becomes idle (keep it for rollback).
6. After bake period, decommission Blue.

```
Before cutover:
  LB -> Blue (v1.2.3) [active]
        Green (v1.3.0) [idle, smoke-tested]

After cutover:
  LB -> Green (v1.3.0) [active]
        Blue (v1.2.3) [idle, ready for rollback]
```

### Rollback Plan

- Switch the load balancer back to Blue.
- Rollback time: seconds (DNS or LB config change).
- Data consideration: if both environments share a database, schema changes must be backward compatible (use expand-contract).

### Verification Strategy

- Run the full test suite against Green before switching.
- Perform synthetic transaction monitoring immediately after switch.
- Monitor error rates for 30 minutes before considering the deployment stable.
- Keep Blue running for at least 24 hours as a hot standby.

---

## 5. Feature Flag Migration

### When to Use

- Replacing an internal algorithm or component.
- Swapping a third-party service provider (e.g., email provider, payment gateway).
- Changes that affect a subset of users and benefit from gradual rollout.

### How It Works

1. Implement the new component behind a feature flag.
2. Route a percentage of traffic to the new component.
3. Compare metrics between old and new components.
4. Gradually increase the percentage as confidence grows.
5. Remove the flag and old code path after full rollout.

```typescript
async function sendEmail(to: string, template: EmailTemplate): Promise<void> {
  if (featureFlags.isEnabled('use_new_email_provider', { userId: to })) {
    // New provider
    await newEmailProvider.send({ to, template: mapTemplate(template) });
    metrics.increment('email.sent', { provider: 'new' });
  } else {
    // Old provider
    await oldEmailProvider.send({ to, template });
    metrics.increment('email.sent', { provider: 'old' });
  }
}
```

### Rollback Plan

- Toggle the feature flag to off. Instant revert.
- Rollback time: under 1 minute (no deployment needed).
- No data migration needed if both providers are stateless. If stateful, ensure data written by the new component is compatible with the old one.

### Verification Strategy

- Compare delivery rates, latency, and error rates between old and new providers.
- Follow the percentage rollout schedule (1% -> 5% -> 25% -> 50% -> 100%).
- Monitor business metrics (conversion rates, user complaints) per cohort.

---

## General Migration Checklist

- [ ] A rollback plan is documented and tested before the migration begins.
- [ ] Success criteria are defined with specific metrics and thresholds.
- [ ] A timeline is established with go/no-go checkpoints at each phase.
- [ ] Data integrity checks are automated and run continuously during migration.
- [ ] Monitoring dashboards exist that compare old and new system behavior side by side.
- [ ] Communication plan exists for stakeholders (when will migration happen, who to contact if something breaks).
- [ ] The migration does not require downtime. If it does, a maintenance window is scheduled and communicated.
- [ ] Each phase of the migration is independently deployable and reversible.
- [ ] A bake period is defined between each phase (minimum 24 hours for critical systems).
- [ ] The old system is not decommissioned until the new system has been verified in production for at least 7 days.
