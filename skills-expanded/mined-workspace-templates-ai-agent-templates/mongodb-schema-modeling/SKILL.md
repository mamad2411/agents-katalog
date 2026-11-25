---
name: mongodb-schema-modeling
description: Decides between embedding and referencing in MongoDB and shapes documents around the actual read and write patterns of the app.
---

# MongoDB schema modeling

Model for access patterns. Data that is read together lives together.

## Steps

1. List the queries and writes with frequency: "load an order with its lines (very often)", "update one line status (often)", "report by month (nightly)".
2. For each relationship decide:
   - Embed when the child is read with the parent, belongs to one parent, and stays small and bounded.
   - Reference when the child is shared, queried alone, or grows without limit.
   - Use the subset pattern when you need only the latest few children (embed 10 recent comments, reference the rest).
3. Never allow an unbounded array. Put growing lists in their own collection with the parent id and an index.
4. Precompute values read far more than written (order totals, counters) and update them in the same write; use the bucket pattern for time series.
5. Keep documents under a few hundred KB. Note the 16 MB hard limit.
6. Design indexes from the queries: compound indexes follow equality, sort, range order. Use `explain("executionStats")` and compare `totalDocsExamined` with `nReturned`.
7. Add schema validation (`$jsonSchema`) with required fields and types, and a `schemaVersion` field to allow later changes.
8. Use multi-document transactions only when the model truly spans documents; a better embed often removes the need.

## Rules

- Do not copy relational tables one to one.
- Avoid `$lookup` on hot paths; denormalize deliberately and write down who updates the copy.

## Report

Collections with sample documents, indexes, and one line of reasoning per embed or reference choice.
