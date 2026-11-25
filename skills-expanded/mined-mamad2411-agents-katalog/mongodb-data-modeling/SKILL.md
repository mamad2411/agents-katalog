---
name: mongodb-data-modeling
description: "Design MongoDB collections, validation, indexes, transactions, TTL, and outbox."
---

# MongoDB Data Modeling

Model MongoDB from access patterns and lifecycle first; encode consistency through document shape, indexes, validation, write concern, and application boundaries.

## Process

1. Identify access patterns, trust boundaries, runtime constraints, ownership, and operational requirements before choosing structure.
2. Prefer the simplest design that satisfies current requirements and leaves clear extension points for known near-term changes.
3. Make data flow, failure handling, observability, and rollout constraints explicit.
4. Translate the design into concrete implementation and review checks before coding.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Zasady ogólne; Kiedy MongoDB pasuje do problemu
- [02-schema-validation.md](./references/02-schema-validation.md) - Schema validation; Schema versioning i migracje danych; Indeksy
- [03-query-optimization.md](./references/03-query-optimization.md) - Query optimization; Paginacja; Aggregation pipeline; Update, upsert i atomicity
- [04-idempotencja-i-retry.md](./references/04-idempotencja-i-retry.md) - Idempotencja i retry; Dane tymczasowe, TTL i retencja; Time series collections; Change streams
- [05-audyt-i-historia-zmian.md](./references/05-audyt-i-historia-zmian.md) - Audyt i historia zmian; Dane wrażliwe i prywatność; Aplikacyjny repository/data access layer; Komunikacja API i persistence
- [06-minimalny-standard-dla-nowej-kolekcji.md](./references/06-minimalny-standard-dla-nowej-kolekcji.md) - Minimalny standard dla nowej kolekcji
