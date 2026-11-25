---
name: data-and-api-design
description: Schema design, database migrations, and API contract discipline. Use when designing a new database schema, writing a migration, designing a REST or GraphQL API, adding a new field to an existing API, versioning an API, or evaluating backward compatibility of a change. Covers the expand/contract migration pattern, expensive schema mistakes, API versioning strategies, idempotency, and backward compatibility as a hard constraint. Does not cover query optimisation (see performance-engineering) or ORM configuration.
---

# Data and API Design

Schemas and API contracts are the most expensive things to change in a running system. A wrong variable name is fixed in one commit. A wrong schema or a broken API contract requires a coordinated migration across every client, every environment, and every piece of data that was written under the old shape.

For schema design and migration patterns see [schema-design.md](schema-design.md).
For API contract design and versioning see [api-design.md](api-design.md).

## The hard constraint

**API contracts and database schemas are effectively permanent once external clients or data depend on them.**

This is not hyperbole. Stripe has maintained every API field they have ever shipped. PostgreSQL has never broken a storage format across major versions. The reason is not sentimentality — it is that the cost of a breaking change falls on every consumer simultaneously, while the cost of maintaining backward compatibility falls only on the provider.

Before adding a field: it will exist forever or require a deprecation and migration campaign.
Before removing a field: every consumer that reads it will break.
Before changing a field's type or semantics: every consumer that relies on the current behaviour will break silently or loudly.

## The cost of getting it wrong

Schema mistakes compound. A boolean column that should have been an enum requires a migration to add the new states, a code change to every place that reads or writes it, and a data migration to backfill existing records. On a table with millions of rows, that migration may require a maintenance window or careful online migration tooling.

API mistakes distribute. Every client that has consumed the API needs to be updated. If clients are external (mobile apps, third-party integrations), you cannot force the update — you must maintain both the old and new behaviour simultaneously until the old clients are gone.

Design as if the first version is permanent, because for external consumers, it often is.
