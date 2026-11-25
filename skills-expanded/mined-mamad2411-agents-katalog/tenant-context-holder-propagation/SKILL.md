---
name: tenant-context-holder-propagation
description: Set TenantContextHolder.INSTANCE.setTenantId(orgId) on the current thread so MongoDB tenant-isolated templates route queries correctly, always clearing in a finally block
triggers:
  - TenantContextHolder
  - tenant context propagation
  - multi-tenant thread local
  - MONGODB_TEMPLATE_ISOLATION
  - tenant isolation mongodb
scope: user
source_project: lucida-domain-sms
version: 0.1.0-draft
tags: [spring, multi-tenant, threadlocal, mongodb, isolation]
category: arch
---

# Tenant Context Holder Propagation

## Problem
In a multi-tenant system backed by MongoDB, every query must be scoped to the correct tenant (organization). Passing an `orgId` parameter through every method signature is verbose, error-prone, and pollutes service APIs. A ThreadLocal holder lets the current execution context carry tenant identity transparently.

## Pattern
- `TenantContextHolder.INSTANCE` is a singleton backed by a `ThreadLocal<String>`.
- Call `TenantContextHolder.INSTANCE.setTenantId(orgId)` at the entry point of any operation that requires tenant-scoped queries.
- MongoDB repositories and templates annotated/qualified with `@Qualifier(MONGODB_TEMPLATE_ISOLATION)` read the tenant ID from the holder to scope their queries automatically.
- Always call `TenantContextHolder.INSTANCE.clear()` in a `finally` block to prevent tenant ID leakage to the next task on a pooled thread.
- In `@Transactional` service methods, set the tenant before the transaction opens and clear after it completes.

## Example (sanitized)

```java
// Service method — tenant set by caller before entering
@Service
public class ItemServiceImpl implements ItemService {

    private final ItemRepository itemRepository; // uses MONGODB_TEMPLATE_ISOLATION internally

    @Override
    public Page<Item> findItems(Criteria criteria, Pageable pageable) {
        // TenantContextHolder already set by the caller; just query
        return itemRepository.findByCriteria(criteria, pageable);
    }
}

// Entry-point that owns the lifecycle (e.g. a Kafka consumer or migration processor)
public void processForOrg(String orgId, ConfigurationProcessRequest request) {
    TenantContextHolder.INSTANCE.setTenantId(orgId);
    try {
        boolean ok = migrationProcessor.processResourceMigration(request);
        if (!ok) {
            log.warn("Migration failed for orgId={}", orgId);
        }
    } finally {
        TenantContextHolder.INSTANCE.clear(); // MUST run even on exception
    }
}

// Controller that owns the lifecycle (test/internal endpoint)
@GetMapping("/orgs/{orgId}/items")
public ApiResponseData<Object> listItems(
    @PathVariable String orgId,
    @RequestBody FiltersPageableDto dto) {

    TenantContextHolder.INSTANCE.setTenantId(orgId);
    try {
        return itemController.listItems(dto);
    } finally {
        TenantContextHolder.INSTANCE.clear();
    }
}

// MongoDB config — isolated template bean
@Bean
@Qualifier(TenantMongoDBConstants.MONGODB_TEMPLATE_ISOLATION)
public MongoTemplate mongoTemplateIsolation(MongoDatabaseFactory factory) {
    return new MongoTemplate(factory) {
        @Override
        protected String getCollectionName(Class<?> entityClass) {
            String tenantId = TenantContextHolder.INSTANCE.getTenantId();
            // prefix or suffix collection name with tenantId
            return tenantId + "_" + super.getCollectionName(entityClass);
        }
    };
}
```

## When to Use
- Any MongoDB operation that must be scoped to the current organization in a multi-tenant deployment.
- Kafka consumer handlers and migration processors where no HTTP request context is available to carry JWT claims.
- Batch jobs that iterate over multiple organizations sequentially.

## Pitfalls
- **Missing `clear()` in finally**: stale tenant ID is silently reused by the next task on the same thread pool thread. This is the most dangerous failure mode.
- **Async boundaries**: `ThreadLocal` does not cross thread boundaries. Propagate the tenant ID explicitly to `CompletableFuture`, `@Async` methods, or virtual threads.
- **Transaction scope mismatch**: setting tenant after a `@Transactional` proxy opens the connection may route the connection to the wrong database. Set tenant before the transactional method is called.
- **Test isolation**: in integration tests, always `clear()` in `@AfterEach` so leaked tenant state doesn't affect subsequent test cases.

## Related
- `migration-processor-pipeline` — the canonical usage pattern of set/clear inside a migration processor.
