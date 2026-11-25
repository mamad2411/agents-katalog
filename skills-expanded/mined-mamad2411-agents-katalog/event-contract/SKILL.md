---
name: "event-contract"
description: "Event/message contract design: schema definition, versioning, compatibility rules, and a shared event catalogue across producers and consumers."
version: 1
created: "2026-06-09T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use whenever services exchange events/messages. Activate alongside any messaging skill (Kafka/SQS/Service Bus) to define the payloads.

## Procedure
1. Define each event schema explicitly (Avro/JSON Schema/Protobuf) in a shared, versioned location.
2. Carry an envelope: event id, type, version, occurred-at, correlation id, partition/group key.
3. Apply compatibility rules (backward/forward) so producers and consumers evolve independently.
4. Register schemas (schema registry) where the broker supports it; fail builds on incompatible changes.
5. Maintain an event catalogue: producer, schema, version, consumers, semantics.
6. Treat published events as a public API - additive changes only without a major version bump.

## Patterns
- Schema registry + compatibility enforcement
- Versioned envelope with id/correlation/key
- Additive-only evolution within a major version
- Single source-of-truth event catalogue
- Consumer-driven contract tests

## Anti-Patterns
- Implicit/undocumented payloads
- Breaking field changes without a version bump
- Different envelope shapes per event
- Coupling consumers to producer internal models
- No registry / no compatibility check in CI

## Tool Selection
- Generic: read_file, write_file, command_line, skills
- Intended (roadmap): schema_registry_client, contract_compatibility_checker

## Validation Rules
- Every event has a versioned, registered schema
- Envelope carries id + correlation + key
- CI fails on incompatible schema changes
- Event catalogue lists producers/consumers

## RAG Sources
- json-schema-spec
- avro-spec
- schema-registry-docs
- tsa.execution_chain.integration_points
