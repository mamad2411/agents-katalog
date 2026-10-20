---
name: mongodb-review
description: "Review MongoDB changes to documents, queries, indexes, transactions, tenant isolation, or migrations."
---

# MongoDB Review

Review MongoDB changes for access-pattern fit, index coverage, consistency, concurrency, tenant isolation, operational impact, and data lifecycle safety.

## Trigger boundary

Use this skill when a MongoDB diff changes document shape, access patterns, indexes, transactions, tenant isolation, migrations, operational behavior, or data lifecycle.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no MongoDB schema, query, consistency, security, or operational impact; follow the repository's established convention directly.

## Coordination

Use this skill together with `itsol-task-intake` for ambiguous work, `itsol-self-review` before handoff, and focused `security-*` or `infra-*` skills when the change touches trust boundaries or deployment behavior.

## Focused References

- [01-overview.md](./references/01-overview.md) - Overview; Cel dokumentu; Zasady ogólne; Kiedy MongoDB pasuje do problemu
- [02-projektowanie-modelu-danych.md](./references/02-projektowanie-modelu-danych.md) - Projektowanie modelu danych; Embedding vs references; Rozmiar dokumentu i zagnieżdżenia; Nazewnictwo i konwencje schematu
- [03-indeksy.md](./references/03-indeksy.md) - Indeksy; Query optimization; Paginacja
- [04-aggregation-pipeline.md](./references/04-aggregation-pipeline.md) - Aggregation pipeline; Update, upsert i atomicity; Transakcje; Idempotencja i retry
- [05-connection-pooling-i-konfiguracja-drivera.md](./references/05-connection-pooling-i-konfiguracja-drivera.md) - Connection pooling i konfiguracja drivera; Read concern, write concern i read preference; Replica set; Sharding
- [06-sekrety-i-connection-stringi.md](./references/06-sekrety-i-connection-stringi.md) - Sekrety i connection stringi; Observability i monitoring; Index builds i zmiany indeksów; Importy, eksporty i bulk operations
- [07-aplikacyjny-repository-data-access-layer.md](./references/07-aplikacyjny-repository-data-access-layer.md) - Aplikacyjny repository/data access layer; Komunikacja API i persistence; Testowanie aplikacji z MongoDB; Scenariusze QA i edge case'y
- [08-checklist-do-code-review.md](./references/08-checklist-do-code-review.md) - Checklist do code review; Minimalny standard dla nowej kolekcji
