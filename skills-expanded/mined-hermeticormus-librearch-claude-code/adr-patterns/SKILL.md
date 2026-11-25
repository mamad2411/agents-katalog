---
name: "adr-patterns"
description: "Architecture Decision Record templates and practices: complete MADR and Nygard templates, Y-statement summaries, supersession, rejected ADRs, ArchUnit fitness functions, and linking ADRs from code. Use when writing, reviewing, or organizing ADRs."
---

# ADR Patterns

> Named patterns, complete templates, and anti-patterns for Architecture Decision Records. Covers Nygard format, MADR, Y-Statements, status lifecycle, fitness functions, and linking decisions to code.

## Patterns

### Pattern: Complete MADR Template

The MADR format captures the full decision space including rejected alternatives. This is the template for medium-to-large scope decisions.

```markdown
# ADR-0023: Use UUID v7 for Entity Identifiers

Status: Accepted
Date: 2024-03-15
Deciders: @alice (arch), @bob (backend lead), @carol (DBA)
Supersedes: ADR-0012 (Use UUID v4 for Entity Identifiers)

## Context and Problem Statement

We generate UUIDs as primary keys for all entities. UUID v4 is fully random,
which causes index fragmentation in PostgreSQL B-tree indexes as rows are
inserted in random UUID order. At 10M+ rows, INSERT performance degrades
measurably due to page splits and cache misses.

## Decision Drivers

- INSERT throughput on high-write tables (orders, events: ~50k/day)
- Index fragmentation under sustained write load
- Need for sortable IDs for pagination (cursor-based)
- No leaking of insertion order or business information

## Considered Options

1. UUID v7 (time-ordered, random suffix)
2. ULID (Universally Unique Lexicographically Sortable Identifier)
3. Snowflake ID (Twitter-style, requires coordination)
4. Sequential integer (BIGSERIAL)
5. Status quo: UUID v4

## Decision Outcome

Chosen: UUID v7, because it is time-ordered (improving index locality),
cryptographically random in the low bits (preventing enumeration), and
is now an IETF standard (RFC 9562, 2024). Libraries exist in all our
languages. No coordination service required.

### Positive Consequences

- Reduced B-tree page splits on INSERT-heavy tables
- Cursor-based pagination is simple: WHERE id > :cursor ORDER BY id
- IDs remain opaque to clients (no sequential business information exposed)
- Standard format — no proprietary encoding

### Negative Consequences

- Existing UUID v4 data cannot be retroactively converted without a migration
- UUID v7 encodes approximate creation timestamp — not a security concern
  for internal IDs but must not be used where creation time is sensitive
- Requires library support: uuid-v7 npm package, com.github.f4b6a3:uuid-creator (Java)

## Reversibility

Hard (months) — Changing ID format requires migrating all foreign keys
and all client-side code that persists or references entity IDs.

## Links

- Supersedes: ADR-0012 (Use UUID v4 for Entity Identifiers)
- RFC 9562: Universally Unique IDentifiers (UUIDs) — IETF, 2024
- Code: src/shared/id-generator.ts, src/shared/id-generator.test.ts
```

### Pattern: Nygard Format (Compact)

For quick internal decisions where the decision space is clear:

```markdown
# ADR-0031: Use Structured Logging (JSON) Over Plain Text

Status: Accepted
Date: 2024-05-10

## Context

We have 12 services logging in different formats. Aggregating logs in
Datadog requires parsing regex for each service. New engineers cannot
easily search across services. Datadog costs are higher because unstructured
logs require more processing.

## Decision

All services will emit JSON-structured logs using Pino (Node.js),
Logback with logstash-logback-encoder (Java), and slog (Go). Required
fields: timestamp (ISO 8601), level, service, version, trace_id,
span_id, message. All additional context as top-level JSON fields.

## Consequences

- Positive: Consistent log schema across services. Datadog facets work
  without parsing rules. Trace correlation is automatic.
- Negative: Logs are less readable in raw terminal output. Developers
  must use `jq` or a log viewer locally. Existing services need migration
  (estimated: 2 weeks per service).
```

### Pattern: Y-Statement as Decision Summary

Write the Y-Statement before the full ADR to test whether the decision is clear:

```
In the context of a high-write event stream (50k events/day),
facing B-tree index fragmentation from random UUID v4 primary keys,
we decided to adopt UUID v7 (time-ordered UUIDs, RFC 9562),
to achieve sequential write locality in PostgreSQL indexes and enable
cursor-based pagination,
accepting that UUID v7 encodes approximate creation timestamp in the
high bits and requires a library dependency for generation.
```

If you cannot complete the "accepting" clause concretely, the decision is not yet ready to accept.

### Pattern: Supersession — Updating an Old ADR

When ADR-0005 supersedes ADR-0002, update both files:

Old ADR (`ADR-0002-use-uuid-v4.md`) — add to Status section:
```markdown
Status: Superseded by [ADR-0005](ADR-0005-use-uuid-v7.md)
Date superseded: 2024-03-15
```

New ADR (`ADR-0005-use-uuid-v7.md`) — add to Links section:
```markdown
## Links
- Supersedes: [ADR-0002](ADR-0002-use-uuid-v4.md) — UUID v4 for entity identifiers
```

### Pattern: Rejected ADR (Valuable Negative Knowledge)

Rejected ADRs prevent re-debating settled questions. Keep them in the log:

```markdown
# ADR-0027: [REJECTED] Use MongoDB for Order Storage

Status: Rejected
Date: 2024-01-20

## Context

Team proposed MongoDB to avoid schema migrations as the order data model evolves.

## Decision

Rejected. Orders require ACID transactions across order, line_items, and inventory
tables. MongoDB's multi-document transactions (4.0+) have higher write latency
and require careful session management. PostgreSQL provides ACID guarantees
natively with mature tooling. Schema evolution is handled via Flyway migrations.

## Why This Record Is Kept

Future teams should not re-propose document databases for transactional
financial data without addressing: ACID semantics, cross-collection transactions,
and audit trail requirements.
```

### Pattern: Fitness Function for ADR Enforcement (ArchUnit)

ADR-0003 states: "The domain layer must not depend on any framework or infrastructure class."

```java
// src/test/java/com/example/arch/DomainIsolationTest.java
// Fitness function — enforces ADR-0003 in CI

@AnalyzeClasses(packages = "com.example", importOptions = ImportOption.DoNotIncludeTests.class)
public class DomainIsolationTest {

    // ADR-0003: Domain layer must not depend on Spring
    @ArchTest
    static final ArchRule domain_free_of_spring =
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("org.springframework..");

    // ADR-0007: Services must not access another service's repository
    @ArchTest
    static final ArchRule no_cross_service_repository_access =
        noClasses()
            .that().resideInAPackage("..orders..")
            .should().dependOnClassesThat()
            .resideInAPackage("..inventory..repository..");

    // ADR-0011: All use cases must be in the application layer
    @ArchTest
    static final ArchRule use_cases_in_application_layer =
        classes()
            .that().haveNameMatching(".*UseCase")
            .should().resideInAPackage("..application..");
}
```

These run on every PR. A PR that violates ADR-0003 fails CI — not code review.

### Pattern: Linking ADRs from Code

```typescript
// src/shared/id-generator.ts
// ADR-0023: Use UUID v7 for entity identifiers (docs/decisions/ADR-0023-use-uuid-v7.md)
// Rationale: time-ordered for B-tree index locality, opaque for security
import { v7 as uuidv7 } from 'uuid';

export function generateEntityId(): string {
  return uuidv7();
}
```

```java
// OrderRepository.java
// ADR-0007: Orders service reads only from orders schema — never inventory
// See: docs/decisions/ADR-0007-service-database-isolation.md
@Repository
public class JpaOrderRepository implements OrderRepository {
    // ...
}
```

## Anti-Patterns

### Anti-Pattern: The Stale ADR

ADR says "Use RabbitMQ for messaging." The team migrated to Kafka eight months ago. Status still reads "Accepted." New engineers implement RabbitMQ consumers. Two weeks of work undone.

Prevention:
- Architecture review checklist includes: "Are there ADRs for components being replaced?"
- When a service is significantly refactored, run `grep -r "ADR-" docs/decisions/` and verify currency
- ADRs for infrastructure components should be reviewed when the component is upgraded or replaced
- Consider a `reviewed_date` field in the MADR front matter

### Anti-Pattern: The Decision Without Context

```markdown
# ADR-0008: Use Redis

Status: Accepted

## Decision

We use Redis.
```

This tells future engineers nothing. Why Redis and not Memcached? What is it caching? What was the traffic/latency problem that motivated caching at all? What happens when Redis is unavailable?

A decision without context has negative value — it creates false authority without actual knowledge transfer.

### Anti-Pattern: The ADR Written After the Fact

The team implemented a solution two months ago. Now someone is writing the ADR retrospectively to justify the choice. The alternatives section is thin. The "accepting" clause is vague. The Consequences section is optimistic.

ADRs written retrospectively miss the live decision process — the alternatives actually considered, the constraints that were real at the time. Write ADRs during the decision, not after.

### Anti-Pattern: Decision by Dictate (No Alternatives Recorded)

```markdown
## Considered Options
1. PostgreSQL

## Decision Outcome
Chosen: PostgreSQL.
```

Only one option means no real decision was made — it was a decree. The value of the ADR is in recording why the other options were rejected. "We considered MySQL, but our team has more PostgreSQL expertise and we need JSONB columns" is useful. A single option is just documentation of the status quo.

### Anti-Pattern: Architecture Decision Sprawl Without Index

A `docs/decisions/` directory with 200 ADRs and no index, no categorization, and inconsistent titling. Engineers cannot find the relevant ADR when they need it.

Mitigation:
- Maintain a `docs/decisions/README.md` with a categorized index (Data, Infrastructure, Architecture, Security, API)
- Use consistent imperative-mood titles ("Use X for Y", "Reject X for Y")
- Consider per-bounded-context ADR directories for large systems: `orders/docs/decisions/`, `inventory/docs/decisions/`

## References

- Nygard, Michael. "Documenting Architecture Decisions." cognitect.com/blog, 2011.
- Kopp, Oliver. MADR project. adr.github.io/madr. Template v3.0.
- Ford, Neal, Rebecca Parsons, Patrick Kua. _Building Evolutionary Architectures_. O'Reilly, 2017.
- ArchUnit: archunit.org — Java architecture fitness functions.
- npryce/adr-tools: github.com/npryce/adr-tools — CLI for ADR management.
- RFC 9562: Universally Unique IDentifiers (UUIDs). IETF, 2024.
- Thoughtworks Technology Radar Vol. 19: Architecture Decision Records.
