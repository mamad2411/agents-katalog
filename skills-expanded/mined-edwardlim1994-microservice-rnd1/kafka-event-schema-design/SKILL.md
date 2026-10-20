# Kafka Event Schema Design

## Purpose
Designs Protobuf schemas for Kafka events that represent domain events flowing between services.

## Role
Data Engineer

## Phase
Planning (Stage 3, collaborates with Architect)

## Triggered By
Story requires Kafka events between services.

## Inputs
- Service boundaries and event flows from Architect

## Location
`contracts/proto/events/` — Data Engineer raises PR for event schemas. Architect reviews for domain alignment.

## Process

### Kafka Event Proto Conventions
- File naming: `{service}-events.proto`
- Message naming: `{EventName}Event` (e.g. `UserCreatedEvent`)
- Include: `event_id` (string, UUID), `occurred_at` (google.protobuf.Timestamp), `correlation_id` (string), `version` (int32)
- These metadata fields enable idempotency and tracing.

### Design Considerations
- Events are immutable facts — use past tense names (UserCreated, OrderPlaced).
- Include enough data for consumers to act without additional queries.
- But don't duplicate entire domain models — include key IDs and changed fields.
- Consider: will consumers need to join other data? If so, include the IDs.

## Outputs
Event proto schema PR in `contracts/proto/events/`.

## Quality Gates
- [ ] Past tense event names
- [ ] metadata fields included (event_id, occurred_at, correlation_id, version)
- [ ] Consumers can act on event without additional API calls for common cases
- [ ] Architect reviewed for domain alignment

## References
- `.claude/skills/backend-developer/kafka-driver-implementation/SKILL.md`
- `.claude/skills/data-engineer/apicurio-registration/SKILL.md`
