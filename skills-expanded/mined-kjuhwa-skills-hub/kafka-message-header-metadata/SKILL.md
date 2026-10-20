---
name: kafka-message-header-metadata
description: Attach org-id, user-id, and timestamp as RecordHeader[] on a ProducerRecord to enable multi-tenant event routing without polluting the Avro payload
triggers:
  - kafka record headers
  - ProducerRecord headers
  - organization-id header kafka
  - multi-tenant kafka routing
  - RecordHeader metadata
scope: user
source_project: lucida-domain-sms
version: 0.1.0-draft
tags: [kafka, avro, multi-tenant, headers, spring]
category: backend
---

# Kafka Message Header Metadata

## Problem
Kafka Avro payloads are schema-versioned and shared across services. Adding routing metadata (tenant ID, acting user, timestamp) directly to the Avro schema pollutes it with infrastructure concerns and requires schema evolution for every new metadata field. Kafka's native record headers provide an out-of-band metadata channel.

## Pattern
- Build a `List<Header>` containing `RecordHeader` instances for each metadata field.
- Construct a `ProducerRecord` with explicit `null` for partition/key and pass the header list as the last argument.
- Consumers extract headers via `record.headers().lastHeader("organization-id")` — no changes needed to the Avro schema.
- Standard header keys: `organization-id`, `user-id`; timestamp is carried implicitly by the record offset or added as a header when the agent-side timestamp is needed.

## Example (sanitized)

```java
// Producer helper (reusable private method in any service/processor)
private void sendToKafka(String orgId, String userId, String topic, Object avroPayload) {
    List<Header> headers = new ArrayList<>();
    headers.add(new RecordHeader("organization-id", orgId.getBytes(StandardCharsets.UTF_8)));
    if (userId != null) {
        headers.add(new RecordHeader("user-id", userId.getBytes(StandardCharsets.UTF_8)));
    }

    ProducerRecord<String, Object> record =
        new ProducerRecord<>(topic, null, null, null, avroPayload, headers);

    kafkaProducer.sendToKafka(record);
}

// Call site — after persisting entity
sendToKafka(organizationId, getMigrationUserId(), CM_SAVE_REQUEST_TOPIC, configTopic);

// Consumer side — extracting the header
@KafkaListener(topics = "#{someTopicConfig}")
public void consume(ConsumerRecord<String, SpecificRecordBase> record) {
    Header orgHeader = record.headers().lastHeader("organization-id");
    String orgId = orgHeader != null
        ? new String(orgHeader.value(), StandardCharsets.UTF_8)
        : null;
    if (orgId == null) {
        log.warn("Missing organization-id header, skipping record offset={}", record.offset());
        return;
    }
    TenantContextHolder.INSTANCE.setTenantId(orgId);
    try {
        process(orgId, record.value());
    } finally {
        TenantContextHolder.INSTANCE.clear();
    }
}
```

## When to Use
- Any service that produces Kafka events in a multi-tenant deployment where consumers need to identify the owning organization.
- When Avro schemas are shared across microservices and must not be changed for routing metadata.
- Migration processors and configuration sync events that carry a `userId` for audit trails.

## Pitfalls
- **Character encoding**: always specify `StandardCharsets.UTF_8` explicitly when converting strings to/from `byte[]`. Default platform encoding is not portable.
- **Header key naming**: agree on a project-wide standard (`organization-id` vs `orgId` vs `X-Org-Id`). Inconsistent names force every consumer to handle aliases.
- **Missing header handling**: consumers must handle a missing header gracefully (skip, DLQ, or default tenant) rather than throwing a NullPointerException.
- **Header size**: Kafka headers are included in the message size. Avoid putting large values (JWTs, full payloads) in headers; keep them to short identifiers.

## Related
- `tenant-context-holder-propagation` — consumer side sets tenant ID from the extracted header.
- `migration-processor-pipeline` — the canonical producer-side usage pattern.
