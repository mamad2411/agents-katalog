---
name: migration-processor-pipeline
description: Abstract migration processor template — validate → load → transform → emit Kafka Avro event with org-id header → audit log, multi-tenant safe
triggers:
  - migration processor
  - data migration pipeline
  - legacy data import
  - migration with kafka
scope: user
source_project: lucida-domain-sms
version: 0.1.0-draft
tags: [spring, kafka, avro, migration, multi-tenant, mongodb]
category: backend
---

# Migration Processor Pipeline

## Problem
Migrating legacy data into a multi-tenant system requires: validating incoming records, transforming them into the current domain model, persisting to MongoDB, and broadcasting a Kafka Avro event so downstream services stay consistent — all while keeping tenant identity scoped to the current thread.

## Pattern
- Define a `ResourceMigrationProcessor` interface with `validateResourceAttributes(request)` + `processResourceMigration(request)`.
- Default methods on the interface provide shared utilities (attribute-list → Map conversion, migration user ID).
- Each concrete `@Component` processor handles one resource type; Spring discovers them all.
- The process method follows the same pipeline order:
  1. Set `TenantContextHolder.INSTANCE.setTenantId(orgId)` at entry.
  2. Validate required attributes; return `false` early on failure.
  3. Check idempotency (skip if already migrated).
  4. Load supporting data (policies, tags) from MongoDB.
  5. Persist the new entity.
  6. Emit a `ProducerRecord` with a `RecordHeader` carrying `organization-id`.
  7. Call `TenantContextHolder.INSTANCE.clear()` in a `finally` block (or at end of success path).

## Example (sanitized)

```java
// Interface
public interface ResourceMigrationProcessor {
    boolean validateResourceAttributes(ConfigurationProcessRequest request);

    @Transactional
    boolean processResourceMigration(ConfigurationProcessRequest request);

    default Map<String, String> convertAttributesToMap(List<Map<String, Object>> attrs) {
        Map<String, String> map = new HashMap<>();
        if (attrs != null) {
            for (Map<String, Object> attr : attrs) {
                if (attr.containsKey("k") && attr.containsKey("v")) {
                    map.put((String) attr.get("k"), attr.get("v").toString());
                }
            }
        }
        return map;
    }

    default String getMigrationUserId() { return "migration"; }
}

// Concrete processor
@Slf4j
@Component
public class WidgetMigrationProcessor implements ResourceMigrationProcessor {

    private final WidgetRepository widgetRepository;
    private final SmsKafkaProducer<String, Object> kafkaProducer;
    private final AuditService auditService;

    // constructor injection...

    @Override
    public boolean validateResourceAttributes(ConfigurationProcessRequest request) {
        Map<String, String> attrs = convertAttributesToMap(request.getAttributeList());
        for (String required : REQUIRED_ATTRS) {
            if (!StringUtils.hasText(attrs.get(required))) {
                log.warn("Missing required attr: {} for resourceId={}", required, request.getResourceId());
                return false;
            }
        }
        return true;
    }

    @Override
    @Transactional
    public boolean processResourceMigration(ConfigurationProcessRequest request) {
        String orgId = request.getOrganizationId();
        TenantContextHolder.INSTANCE.setTenantId(orgId);
        try {
            Map<String, String> attrs = convertAttributesToMap(request.getAttributeList());

            if (widgetRepository.existsById(attrs.get("widgetId"))) {
                return true; // idempotent — already migrated
            }

            Widget entity = new Widget(attrs.get("widgetId"), attrs.get("name"));
            auditService.save(entity);

            sendToKafka(orgId, TOPIC, buildAvroPayload(entity));
            return true;
        } finally {
            TenantContextHolder.INSTANCE.clear();
        }
    }

    private void sendToKafka(String orgId, String topic, Object payload) {
        List<Header> headers = List.of(
            new RecordHeader("organization-id", orgId.getBytes())
        );
        ProducerRecord<String, Object> record =
            new ProducerRecord<>(topic, null, null, null, payload, headers);
        kafkaProducer.sendToKafka(record);
    }
}
```

## When to Use
- Importing records from a legacy system into the current multi-tenant domain model.
- Each legacy resource type has a distinct validation rule and transformation logic.
- Downstream services must be notified of new records via Kafka events.

## Pitfalls
- **Missing `clear()` call**: forgetting to clear `TenantContextHolder` leaves a stale tenant on the thread pool thread. Always use `try/finally`.
- **Non-idempotent writes**: check existence before inserting; migrations may be replayed on failure.
- **Attribute key typos**: legacy attribute names are often inconsistent — define constants for required keys and validate them in `validateResourceAttributes`.
- **Transaction boundary**: `@Transactional` on `processResourceMigration` will not cover the Kafka send. Emit Kafka only after the DB commit succeeds, or use an outbox pattern.

## Related
- `tenant-context-holder-propagation` — describes the TenantContextHolder pattern used inside each processor.
- `kafka-message-header-metadata` — describes the ProducerRecord header convention used in `sendToKafka`.
