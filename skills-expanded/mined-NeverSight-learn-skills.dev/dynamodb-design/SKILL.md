---
name: dynamodb-design
description: Designs DynamoDB data models from access patterns first. Use this whenever the user needs help modeling a DynamoDB schema, choosing between single-table and multi-table design, defining partition and sort keys, GSIs, item collections, one-to-many or many-to-many relationships, filtering, sorting, uniqueness, TTL, pagination, or deciding whether DynamoDB is even the right fit for the workload.
---

# dynamodb-design

Use this skill to produce a DynamoDB design, not just a table definition.

The guidance in this skill is based on:

- modeling from access patterns
- item collections
- single-table tradeoffs
- relationship strategies
- filtering and sorting strategies
- uniqueness, pagination, and TTL
- implementation boundaries

## When to use

Use this skill when the user asks for any of the following:

- a DynamoDB schema or table design
- partition key and sort key design
- GSI or sparse index design
- single-table versus multi-table guidance
- modeling relationships in DynamoDB
- filtering, sorting, pagination, or uniqueness patterns
- reviewing whether an existing DynamoDB model is sound
- deciding whether DynamoDB fits a workload at all

## What to produce

Unless the user explicitly asks for code first, produce a design package in this order:

1. workload summary
2. access patterns
3. recommended table strategy
4. key design
5. indexes
6. item families
7. write-path rules
8. operational risks
9. implementation notes

## References

Load only the references needed for the task:

- `references/modeling-workflow.md` for the default DynamoDB design process
- `references/strategy-patterns.md` for relationships, filtering, sorting, uniqueness, pagination, and TTL strategies
- `references/implementation-guidance.md` for translating the model into code without leaking DynamoDB details through the whole app
- `references/schema-reference-pattern.md` for generating or updating `docs/schema-reference.md` when the schema is concrete

## Source of truth

Use this order when applying the skill in a real repository:

1. the target repository's existing DynamoDB conventions, repository shape, and schema docs
2. the patterns in this skill
3. the inline examples in this skill

If local code differs from the skill examples, follow local code unless the user explicitly wants to replace it.

## Instructions

### 1. Start with the workload

Understand the application before suggesting keys or indexes.

Before proposing a new design, do a short discovery pass through the target repository.

Look for:

- existing DynamoDB repositories
- whether repositories inline final key strings directly on items and query call sites
- entity type or `Type` conventions
- existing PK/SK and GSI attribute names
- cursor and pagination helpers
- uniqueness or lookup record patterns
- TTL and expiry conventions
- `docs/schema-reference.md` or equivalent schema docs

After discovery, choose one mode and state it:

- `Existing pattern mode`: extend the repository's current DynamoDB conventions
- `Pattern generation mode`: introduce the missing DynamoDB pattern because the repository does not have a coherent one

Capture:

- the core entities
- how those entities relate
- expected scale
- latency expectations
- whether analytics or ad hoc querying is important
- whether the query surface is already known or still evolving

If the workload is vague, call that out. DynamoDB design depends on known access patterns.

### 2. Write the access patterns down explicitly

Modeling in DynamoDB is driven by access patterns, not by normalized entities.

List every important read and write:

- point reads
- list queries
- time-ordered queries
- relationship traversals
- filtered queries
- writes and updates
- deletes and expiry flows
- background jobs or ETL reads

For each access pattern, capture:

- operation name
- caller or feature
- parameters
- exact result shape
- expected item count
- required sort order
- consistency needs
- any special constraints

Be specific. If the access pattern is still fuzzy, say so before locking in a design.

### 3. Choose the table strategy deliberately

Do not default blindly to either single-table or multi-table.

Recommend `single-table` when:

- several entities participate in the same query paths
- item collections will reduce round trips
- the access patterns are known and stable enough
- performance matters more than query flexibility
- the workload is tenant-scoped and most reads should stay within one tenant partition

Recommend `multi-table` when:

- aggregates are mostly independent
- the application needs more flexibility while still using DynamoDB
- the complexity cost of single-table design is not justified
- the user is in an early stage where developer agility matters more than absolute performance

Recommend `DynamoDB may not be the best fit` when:

- the user needs broad ad hoc querying
- OLAP or analytics-heavy usage is primary
- relational joins are central
- the access patterns are too undefined to design around yet

Even when recommending multi-table, apply proper DynamoDB thinking. Do not fall back to SQL mental models without noting the tradeoff.

For B2B SaaS workloads, explicitly ask whether most application reads are tenant-scoped. If they are, treat "one tenant partition containing multiple item types" as a candidate default and treat cross-tenant queries as exceptional paths that may deserve GSIs.

### 4. Design keys from the access patterns

After the access patterns are clear:

- define the partition key and sort key templates
- define item collections
- add GSIs only for real alternate access patterns
- prefer sparse indexes when only a subset of items belongs in the index

For each key or index, state which access pattern it serves.

Prefer key templates that are easy to read directly in the repository item and query code. Do not introduce or recommend a shared `keys.ts`, centralized key-builder object, or helper layer whose main job is string interpolation.

Prefer explicit templates such as:

```text
PK = USER#{userId}
SK = ORDER#{createdAt}#{orderId}

GSI1PK = EMAIL#{email}
GSI1SK = USER#{userId}
```

Do not present keys without attaching them to the read or write they enable.

### 5. Use strategy patterns where they simplify the model

Pull from the strategy reference when needed:

- one-to-many: composite primary key, duplicated data, secondary indexes, hierarchical sort keys
- many-to-many: shallow duplication, adjacency list, materialized graph, or multiple requests
- filtering: prefer partition key, sort key, composite sort keys, or sparse indexes before filter expressions
- sorting: encode sort order into the sort key and think through changing attributes
- uniqueness: use dedicated uniqueness items and conditional writes
- pagination: design around DynamoDB pagination instead of bolting it on afterward
- TTL: use TTL for expiry cleanup, but do not rely on TTL timing alone for correctness

### 6. Check operational constraints before finalizing

Always review the design for:

- hot partitions
- uneven partition key distribution
- large item collections
- write concentration over time
- index sprawl
- large item sizes
- migration difficulty
- analytics and export needs
- correctness around uniqueness and multi-item writes

Be concrete about partition risk. If a design could concentrate traffic on a small set of keys, call that out explicitly and suggest bucketing, sharding, alternate partitioning, or a different retrieval pattern.

Prefer `GetItem`, `BatchGetItem`, and `Query` for primary application access. Treat `Scan` on large tables as exceptional and call out its throughput cost when a proposed design depends on it.

Call out where the design is optimized for OLTP and where it will be awkward for analytics.

When the task creates or materially changes a concrete DynamoDB schema, generate or update `docs/schema-reference.md` in the repository. Use it to record access patterns, key templates, item families, indexes, pagination rules, uniqueness conventions, TTL behavior, notable operational constraints, and a Mermaid diagram that makes the table layout easy to scan.

If the schema is already deployed in production, prefer additive changes, repository-layer shielding, and staged migrations over destructive redesigns. Do not optimize for migration complexity when nothing is deployed yet.

### 7. Keep implementation details at the boundary

When the user wants code:

- prefer a repository pattern for DynamoDB access so the domain and business layer are unaware of DynamoDB specifics
- keep final PK/SK/GSI string literals visible in the repository item payloads and DynamoDB call sites
- keep indexing attributes separate from application attributes
- implement DynamoDB mapping at the data-access boundary
- do not let raw key templates leak through the application layer
- use a `Type` attribute on every item unless the repository already has an equivalent convention
- avoid reusing one index attribute across multiple indexes just to save bytes
- prefer small debug scripts or focused repository methods over opaque abstractions or generic ORMs

If the repository does not already have a coherent DynamoDB structure, introduce the smallest reusable pattern that makes future access patterns easier to implement, usually a repository plus mapper with explicit inline key strings instead of one-off request code or a shared key-helper module.

Do not recommend a generic ORM as the main way to interact with DynamoDB.

Repository methods should be named after domain operations or access patterns, not after raw DynamoDB APIs. The service or business layer should ask for things like `findProjectById`, `listTenantProjects`, or `saveSubscription`, not construct keys or call `Query` directly.

Inside the repository, prefer readable duplication over indirection for key strings. A reader should be able to look at the `Item`, `Key`, or `ExpressionAttributeValues` block and immediately see the stored PK/SK/GSI values without jumping to a helper file.

## Response style

When giving a recommendation, use concise sections:

- `Recommendation`
- `Access Patterns`
- `Table Strategy`
- `Key Design`
- `Indexes`
- `Tradeoffs`
- `Next Steps`

If the user provides an existing design, review it against the same framework rather than inventing a totally new model immediately.
