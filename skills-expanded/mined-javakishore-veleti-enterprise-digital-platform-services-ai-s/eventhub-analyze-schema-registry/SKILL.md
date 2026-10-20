---
name: eventhub-analyze-schema-registry
description: Analyze Azure Event Hubs Schema Registry usage, schema groups, Avro/JSON Schema/Protobuf contracts, producer/consumer compatibility, evolution, serialization, and governance. Use for schema errors, contract evolution, incompatible consumers, or event-payload governance.
---

# Analyze Schema Registry

1. Identify schema group, serialization format, producer, consumers, and current schema versions.
2. Inspect producer serialization and consumer deserialization behavior.
3. Compare schema changes with compatibility and rollout expectations.
4. Identify missing registration, wrong schema ID, incompatible field evolution, or client mismatch.
5. Correlate schema failures with producer/consumer deployment versions.
6. Do not infer business field semantics absent domain documentation.

## Output
- Schema Topology
- Producer/Consumer Versions
- Compatibility Findings
- Failure Evidence
- Recommended Evolution Plan
