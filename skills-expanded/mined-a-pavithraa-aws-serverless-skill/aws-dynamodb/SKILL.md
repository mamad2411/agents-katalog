---
name: aws-dynamodb
description: "Use when designing or reviewing a DynamoDB table: access patterns, partition and sort keys, single-table design, GSIs and sparse indexes, hot partitions, one-to-many and many-to-many modeling, capacity mode and cost, or the Terraform for the table."
---

# AWS DynamoDB

## Get the access patterns before you design

A DynamoDB schema follows the queries. A table designed before the queries are known has to be redesigned, and a key change means a backfill of every item.

If the user asks for a table design and has not listed the access patterns, stop. Do not write tables, keys, GSIs, or a "starting schema" in that reply, not even one built on assumed patterns. Instead:

1. Say in one or two sentences why the design must wait: the keys come from the queries, and DynamoDB has no joins.
2. If the user proposed one table per entity, say that this is the relational habit and that the access patterns decide between one table and several.
3. Ask for the access patterns as a numbered list. For each pattern, ask what the query is looked up by, what it returns, the sort order, and how often it runs. Ask which entities are read together, the expected item counts and write rates, and any uniqueness or tenant-isolation rules.
4. Offer a few example patterns from the user's domain for the user to confirm, change or extend. Present them as questions, not as a design.

The same rule applies when the user pushes back ("just give me a starting schema", "we can migrate later"). Explain that a migration means a scan and rewrite of every item. Then offer to draft the access-pattern list with the user. Design only after the user confirms a list.

The rule is for data-model design. It does not stop a build. When the user asks you to build a service and the table is one part of it, such as "an API that reads and writes an `orders` table", build the table and do not stop:

- Use the entity's ID as the partition key (`order_id`), with no sort key and no GSIs. A GSI added later backfills itself. A changed primary key does not.
- Say in your final message that the key assumes lookups by ID only.
- End by asking for the other access patterns, such as "orders for a customer, newest first", because each one can need a GSI.

If the build needs several related entities, such as users, organizations and projects, the data model is the design question. Stop and ask as described above.

## Quick Reference

> All patterns are in [`references/dynamodb-patterns.md`](references/dynamodb-patterns.md).

| Topic | Key Insight |
|-------|-------------|
| Data modeling | Design access patterns FIRST, schema second |
| Single-table design | Items queried together live together |
| GSIs | Multi-attribute composite keys avoid synthetic key hacks |
| Cost optimization | Filter expressions do NOT reduce read costs |
| Sort order control | `#` prefix positions parent at sort boundary; numeric difference enables reverse integer ordering |
| Sparse indexes | Entity-type filter (always-on attr) vs conditional filter (add/remove attr on state change) |
| Reference counts | TransactWriteItems: child PutItem (attribute_not_exists) + parent UpdateItem increment |
| Hot partitions | Timestamp-shard GSI PK by day; read-shard caches across N copies |
| Many-to-many | Adjacency list: link item in base table + GSI projects into second parent's collection |
| Uniqueness enforcement | Uniqueness tracking item (no data) + TransactWriteItems with attribute_not_exists on each |

## Critical Anti-Patterns

- **Don't** design schema first, then figure out queries — list access patterns first
- **Don't** use filter expressions expecting them to reduce read costs — they don't
- **Don't** store frequently-updated data with large static data — use vertical sharding
- **Don't** manually concatenate synthetic GSI keys (`TOURNAMENT#X#REGION#Y`) — use [multi-attribute composite keys](references/dynamodb-patterns.md#multi-attribute-composite-keys) (provider v6.29.0+)
- **Don't** put bare integers in sort keys — `ISSUE#9` sorts after `ISSUE#100` lexicographically; zero-pad to fixed width (`ISSUE#00000009`)
- **Don't** use a filter expression when its hit rate is poor — a partition with 10,000 open issues and 5 closed ones: filtering for closed reads all 10,005 items and returns 5; embed status in the sort key instead (`ISSUE#CLOSED#<id>`)
- **Don't** count children at read time via Query+count — store a reference count on the parent and increment atomically via TransactWriteItems
- **Don't** assume TTL-expired items are gone immediately — DynamoDB TTL has a 48h deletion window; guard reads with `FilterExpression: TTL > current_epoch`
- **Don't** put two entity types in the same PK namespace without a shared-namespace decision — if names must be globally unique (e.g., users vs orgs), use the same PK prefix intentionally and let `attribute_not_exists` enforce the constraint

## Decision Frameworks

### Single-Table vs Multi-Table
| Use Single Table When | Use Multiple Tables When |
|----------------------|-------------------------|
| Items queried together | Completely independent data |
| Same team owns all data | Different teams, different access |
| Need transactional writes | Data has vastly different access patterns |

### Schema Migration Strategy

Migrations are ranked by difficulty. Always check if a change is purely additive before planning ETL.

| Situation | Additive? | ETL Required? | Strategy |
|-----------|-----------|---------------|----------|
| New optional attribute on existing entity | Yes | No | Handle missing attribute with a default in app code (lazy loading) |
| New entity, no relational access pattern | Yes | No | Start writing new items immediately — zero changes to existing data |
| New entity co-located with existing parent | Yes | No | Match parent PK, assign new SK prefix — no backfill |
| New entity needing a new GSI item collection | No | Yes | `Scan + UpdateItem` to add GSI attributes to all existing parent items |
| Refactoring an existing access pattern | No | Yes | Redesign SK + new GSIs + `Scan + UpdateItem` on all affected items |

For large tables, use parallel scans (`TotalSegments` + `Segment`) to distribute the ETL job — DynamoDB handles all worker coordination.

---

### Synthetic Keys vs Multi-Attribute Composite Keys (GSI)
| Use Multi-Attribute Keys | Keep Synthetic Keys |
|--------------------------|---------------------|
| New GSIs on existing tables (no backfill) | Base table PK/SK (not supported) |
| Attributes have distinct types (Number + String) | Need `begins_with()` across entity types |
| Hierarchical drill-down queries | Single-table overloaded GSI with mixed entities |
| Terraform AWS provider v6.29.0+ | Legacy tables where migration cost > benefit |

## Version Matrix

| Feature | AWS GA | Terraform AWS Provider |
|---------|--------|------------------------|
| Multi-attribute composite GSI keys | Nov 2025 | v6.29.0+ ([PR #45357](https://github.com/hashicorp/terraform-provider-aws/pull/45357)) |

## Cost questions

For prices, use the AWS Pricing MCP server (`awslabs.aws-pricing-mcp-server`). Its [README](https://github.com/awslabs/mcp/tree/main/src/aws-pricing-mcp-server) has the setup. Prices in this skill are dated examples, not quotes.

---

## Reference Loading Strategy

Load `references/dynamodb-patterns.md` for all DynamoDB questions — it covers modeling patterns (item collections, # prefix trick, sparse indexes, reference counts, TTL guard), GSI design (composite keys, multi-attribute keys), cost, and Terraform examples.
