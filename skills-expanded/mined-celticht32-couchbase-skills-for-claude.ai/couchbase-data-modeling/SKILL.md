---
name: couchbase-data-modeling
description: "Design document models, choose document boundaries, and pick access patterns for Couchbase. Use whenever the user asks about document model, schema design, key design, document shape, embed vs reference, denormalization, scope vs collection vs bucket, modeling for query / index / FTS / vector search, time-series in Couchbase, TTL strategies, anti-patterns, migrating from SQL / MongoDB / DynamoDB / DocumentDB, or general 'how should I structure this data.' Triggers on design-phase conversations before any tools are called — distinct from the couchbase-mcp skill, which is for operating an existing cluster. Use proactively for: greenfield Couchbase projects, schema migrations, re-architecting an existing model, deciding between scopes/collections/buckets, modeling time-series or vector embeddings, planning denormalization tradeoffs, naming keys, choosing between embedded sub-documents and references."
license: MIT
---

# Couchbase data modeling

A skill for *designing* what to put in Couchbase, not operating an existing cluster. The companion `couchbase-mcp` skill is for executing operations; this one is for the architectural decisions that come before any tool is called.

## When this skill applies

Use this skill whenever the conversation is about *what shape the data should take*, not *what tool to call*. Concrete signals:

- "How should I model X in Couchbase?"
- "Should I embed this or use references?"
- "What's the right key format?"
- "Bucket vs scope vs collection?"
- "I'm coming from [MongoDB / Postgres / DynamoDB] — how do I think about this?"
- "How do I model time-series / events / logs?"
- "Where do I put the embedding vector?"
- "Schema migration in Couchbase?"

If the conversation has already moved to "now run this tool," switch to `couchbase-mcp`. These skills are designed to compose — modeling first, then operation.

## Pick the right reference

| Question | Read |
|---|---|
| "What should my keys look like?" | `references/keys.md` |
| "Should I embed or reference?" / "How big should one document be?" | `references/document-shape.md` |
| "Bucket vs scope vs collection?" | `references/boundaries.md` |
| "How do I model for fast queries / FTS / vector search?" | `references/access-patterns.md` |
| "Time-series, event logs, anything with timestamps and TTL" | `references/time-series-and-ttl.md` |
| "I think I'm doing something wrong" | `references/anti-patterns.md` |
| "I'm coming from a relational DB" | `references/migration-from-relational.md` |

Each reference is self-contained with a decision tree at the end.

## The five-question design pass

Before reaching for any reference, walk the user through these five questions. The answers determine which references matter and which patterns apply:

1. **What does the application read most often?** Read patterns drive denormalization. The data you fetch together should live together.
2. **What changes together?** Write patterns drive document boundaries. Things that change together should be in the same document, OR separate documents with a transactional update path.
3. **What's the unit of access?** A document is the atomic unit in Couchbase. If you frequently need a subset of a "document," it's probably actually multiple documents.
4. **What's the lifespan?** Permanent data, session data with TTL, time-series with rolling windows — these belong in different collections or even buckets.
5. **What's the worst-case query?** The slowest legitimate query in your workload defines your indexing strategy and possibly your modeling choices.

Don't skip this pass even on "simple" cases. The most common modeling failure is jumping to "I'll just put it all in one document" before thinking about (1) and (4).

## Three core principles

**Principle 1 — Model the read, not the write.**
If you fetch user + their last 10 orders together 95% of the time, embed (or denormalize) the orders. The 5% write cost is worth the 95% read win. The opposite is also true: if you write to orders 100× per read of user+orders, separate them so you're not rewriting the user doc on every order.

**Principle 2 — A document is the atomic unit.**
Couchbase guarantees atomicity at the document level (KV ops) or across multiple documents only via transactions (`cb_transaction_run`, slower). If two things MUST stay consistent, either put them in one document or accept the transaction tax.

**Principle 3 — Boundaries are about lifecycle, not topic.**
Use buckets for fundamentally different lifecycles (different backup schedules, different TTL behavior, different access patterns). Use scopes for multi-tenant or multi-environment separation. Use collections for type-grouped documents within a tenant. See `references/boundaries.md`.

## Common shapes to recognize

The user is often describing one of these shapes without knowing the canonical name:

| User says | Pattern name | Reference |
|---|---|---|
| "Each user has a list of orders" | One-to-many (embed vs reference) | `document-shape.md` |
| "Each order has line items" | Nested aggregate | `document-shape.md` |
| "Users follow other users" | Many-to-many | `document-shape.md` |
| "I want to query by [field X]" | Index-friendly modeling | `access-patterns.md` |
| "Search across descriptions / text" | FTS modeling | `access-patterns.md` |
| "Semantic search over docs" | Vector modeling | `access-patterns.md` |
| "Log entries / metrics / events" | Time-series | `time-series-and-ttl.md` |
| "Session data that expires" | TTL-bounded | `time-series-and-ttl.md` |
| "User profiles with versioned history" | Versioned aggregate | `document-shape.md` |

## What this skill won't help with

- **Capacity planning** ("how much RAM do I need?") — that's a sizing question. Use the `couchbase-sizing` skill instead.
- **Running operations** ("create this index") — that's the `couchbase-mcp` skill.
- **Application code** — modeling is database-side; how your app code consumes the model is out of scope here.

Hand off explicitly when a conversation crosses these lines.
