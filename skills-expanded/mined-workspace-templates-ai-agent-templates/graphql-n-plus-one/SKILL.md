---
name: graphql-n-plus-one
description: Finds resolvers that fire one query per parent object and fixes them with request-scoped dataloaders, batching and proof from query counts.
---

# GraphQL N+1

Count queries before and after. No count, no fix.

## Steps

1. Reproduce with one realistic query that returns a list with nested fields. Enable query logging (ORM debug flag, `pg_stat_statements` or a logging data source) and count statements for that single request. Record the number.
2. Find the pattern: a resolver on a child type that runs a lookup by the parent's id, for example `Order.customer` calling `db.customer.findById(order.customerId)`.
3. Add a dataloader per resolver family. Create loaders in the per-request context, never at module level, so one user's cache and permissions never leak to another.
4. The batch function receives an array of keys and must return an array of the same length and order. Fetch with one `WHERE id IN (...)` query, then map back by key and return `null` or an error for the missing ones.
5. For one-to-many fields, load by foreign key and group the rows into an array per key.
6. Where a query can join cheaply (the parent query already knows the children are always wanted), prefer a join or a lookahead on the selected fields over a loader.
7. Add a test that runs the query against a fixture of 20 parents and asserts the statement count (for example 3, not 41).

## Rules

- Never share a loader between requests.
- Never rely on the batch result order from the database; reorder it.
- Do not add loaders for fields that are not in a list; it adds code with no gain.

## Report

Query count before and after, resolvers changed, loaders added and the test that guards them.
