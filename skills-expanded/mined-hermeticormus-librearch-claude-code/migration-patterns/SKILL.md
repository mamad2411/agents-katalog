---
name: "migration-patterns"
description: "Migration patterns with code: a strangler fig proxy, expand-contract schema migration with Flyway, parallel run with reconciliation, branch by abstraction, and canary rollout with Argo Rollouts. Use when replacing a system or changing a live schema."
---

# Migration Patterns

> Named patterns with code for strangler fig routing, expand-contract schema migration, parallel run, branch by abstraction, and canary deployment with traffic splitting.

## Patterns

### Pattern: Strangler Fig Proxy (TypeScript/Express)

```typescript
// Proxy layer that routes to legacy or new service based on feature flags
// Deployed between clients and both systems — clients call the proxy

import express from 'express';
import httpProxy from 'http-proxy';

const app = express();
const proxy = httpProxy.createProxyServer({});

const LEGACY_URL = process.env.LEGACY_URL!;
const NEW_ORDER_SERVICE_URL = process.env.NEW_ORDER_SERVICE_URL!;

// Migrated endpoints — route to new service
const MIGRATED_PATHS = new Set([
  '/api/orders',
  '/api/orders/:id',
]);

function isMigrated(path: string): boolean {
  // Simple prefix matching — use proper router in production
  return path.startsWith('/api/orders');
}

app.use((req, res) => {
  const target = isMigrated(req.path) ? NEW_ORDER_SERVICE_URL : LEGACY_URL;

  // Log routing decision for observability
  console.log(JSON.stringify({
    path: req.path,
    method: req.method,
    routed_to: isMigrated(req.path) ? 'new' : 'legacy',
    timestamp: new Date().toISOString(),
  }));

  proxy.web(req, res, { target }, (err) => {
    // On new service error, fall back to legacy (optional safety net)
    console.error(`Proxy error to ${target}: ${err.message}`);
    proxy.web(req, res, { target: LEGACY_URL });
  });
});

app.listen(8080);
```

### Pattern: Expand-Contract Database Migration (SQL + Flyway)

```sql
-- V1__initial_schema.sql
CREATE TABLE orders (
    order_id VARCHAR(36) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL  -- old column: full name as one field
);

-- EXPAND PHASE: V2__expand_customer_columns.sql
-- Add new columns alongside old — backward compatible
ALTER TABLE orders
    ADD COLUMN customer_first_name VARCHAR(128),
    ADD COLUMN customer_last_name  VARCHAR(128);

-- Backfill: split existing data into new columns
UPDATE orders
SET
    customer_first_name = SPLIT_PART(customer_name, ' ', 1),
    customer_last_name  = SPLIT_PART(customer_name, ' ', 2)
WHERE customer_first_name IS NULL;

-- At this point: deploy application code that writes to ALL THREE columns
-- Old code still writes to customer_name (backward compatible)
-- New code writes to customer_first_name + customer_last_name AND customer_name

-- After all deployments use new columns and old column reads are removed:

-- CONTRACT PHASE: V3__contract_remove_old_column.sql
-- Safe to drop only when no code reads customer_name anymore
ALTER TABLE orders DROP COLUMN customer_name;
```

Application dual-write during expand phase:
```java
// Writes to both old and new columns during transition
public void saveOrder(Order order) {
    String fullName = order.firstName() + " " + order.lastName();
    jdbcTemplate.update(
        "INSERT INTO orders (order_id, customer_name, customer_first_name, customer_last_name) VALUES (?, ?, ?, ?)",
        order.id(), fullName, order.firstName(), order.lastName()
    );
}
```

### Pattern: Parallel Run with Reconciliation (Python)

```python
from decimal import Decimal
from dataclasses import dataclass
import logging

log = logging.getLogger("parallel_run")

@dataclass
class ReconciliationResult:
    order_id: str
    legacy_result: Decimal
    new_result: Decimal
    match: bool
    diff: Decimal

class ParallelRunCalculator:
    """
    Runs both old and new calculators, compares results,
    logs discrepancies, and returns legacy result until cutover.
    """

    def __init__(self, legacy, new, metrics):
        self.legacy = legacy
        self.new = new
        self.metrics = metrics
        self.shadow_mode = True  # Set to False to route production to new

    def calculate_total(self, order) -> Decimal:
        legacy_result = self.legacy.calculate(order)

        try:
            new_result = self.new.calculate(order)
            result = ReconciliationResult(
                order_id=order.id,
                legacy_result=legacy_result,
                new_result=new_result,
                match=(legacy_result == new_result),
                diff=abs(legacy_result - new_result),
            )

            if not result.match:
                log.warning("parallel_run_mismatch", extra={
                    "order_id": order.id,
                    "legacy": str(legacy_result),
                    "new": str(new_result),
                    "diff": str(result.diff),
                })
                self.metrics.increment("parallel_run.mismatch")
            else:
                self.metrics.increment("parallel_run.match")

        except Exception as e:
            log.error(f"New calculator failed: {e}", exc_info=True)
            self.metrics.increment("parallel_run.new_error")

        # Always return legacy until shadow_mode = False
        return new_result if not self.shadow_mode else legacy_result
```

### Pattern: Branch by Abstraction (Java)

```java
// Step 1: Create abstraction over existing implementation
public interface OrderTaxCalculator {
    Money calculateTax(Order order, Address deliveryAddress);
}

// Step 2: Wrap existing code behind the interface
@Primary  // Used by default
@Component
public class LegacyTaxCalculator implements OrderTaxCalculator {
    private final LegacyTaxEngine legacyEngine;  // Old implementation

    @Override
    public Money calculateTax(Order order, Address deliveryAddress) {
        return legacyEngine.computeTax(order.toDto(), deliveryAddress.toDto());
    }
}

// Step 3: Implement new version behind same interface
@Component("newTaxCalculator")
public class AvalaraTaxCalculator implements OrderTaxCalculator {
    private final AvalararClient avalaraClient;

    @Override
    public Money calculateTax(Order order, Address deliveryAddress) {
        return avalaraClient.calculate(order.id(), order.items(), deliveryAddress);
    }
}

// Step 4: Switch @Primary to new implementation after validation
// Step 5: Remove LegacyTaxCalculator and the @Primary annotation
```

### Pattern: Canary Deployment (Kubernetes + Argo Rollouts)

```yaml
# Argo Rollouts canary strategy
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: order-service
spec:
  strategy:
    canary:
      steps:
        - setWeight: 5     # Route 5% of traffic to new version
        - pause: {duration: 15m}  # Wait 15 minutes, check metrics
        - setWeight: 20
        - pause: {duration: 15m}
        - setWeight: 50
        - pause: {duration: 30m}
        - setWeight: 100   # Full cutover
      analysis:
        templates:
          - templateName: order-service-success-rate
        startingStep: 1
        args:
          - name: service-name
            value: order-service

---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: order-service-success-rate
spec:
  metrics:
    - name: success-rate
      interval: 5m
      failureLimit: 1      # Rollback automatically if metric fails
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="order-service",status!~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="order-service"}[5m]))
      successCondition: result[0] >= 0.99  # Require 99% success rate
```

## Anti-Patterns

### Anti-Pattern: Big Bang Migration

Stopping all development, migrating everything at once, and launching on a fixed date. Any bug discovered during migration requires delaying the launch. Staff works overtime. The launch fails because the new system has edge cases not covered by tests.

Fix: strangler fig — migrate incrementally, release continuously, reduce risk at every step.

### Anti-Pattern: Column Rename in One Step

```sql
-- WRONG: breaks any code reading the old column name immediately
ALTER TABLE orders RENAME COLUMN customer_name TO full_name;
```

Any service that hasn't been redeployed after this migration will fail with a missing column error. Fix: expand-contract — add `full_name`, dual-write, then drop `customer_name` in a later deployment.

### Anti-Pattern: Migrating the Database Before the Code

Deploying a schema migration that removes a column, then deploying the code that stops using it. During the window between migrations, old code reads the deleted column and fails.

Fix: deploy code changes before schema changes. Code should tolerate both old and new schema during the transition.

## References

- Newman, Sam. _Monolith to Microservices_. O'Reilly, 2019. (Strangler fig, branch by abstraction)
- Fowler, Martin. "Strangler Fig Application." martinfowler.com, 2004.
- Fowler, Martin. "Parallel Change." martinfowler.com.
- Sadalage, Pramod, and Martin Fowler. _Refactoring Databases_. Addison-Wesley, 2006. (Expand-contract)
- Argo Rollouts: argoproj.github.io/argo-rollouts (canary + analysis templates)
