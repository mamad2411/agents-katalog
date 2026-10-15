---
name: "spring-mongodb-conventions"
description: "Enforces Spring MongoDB database design, query, index, and Spring Data usage conventions. Invoke when designing documents/collections, writing MongoDB queries, creating indexes, or reviewing Spring Data MongoDB code."
---

# Spring MongoDB Database Conventions

This skill encodes Spring MongoDB best practices. Apply when designing document schemas, writing queries/aggregations, creating indexes, or reviewing Spring Data MongoDB code.

| Section | Reference File | When to Read |
|---------|---------------|-------------|
| Document Design | `references/document-design.md` | When designing collections, choosing field types, embedding vs referencing, naming |
| Base Document Class | `references/base-document.md` | When creating entity classes, designing BaseMongoDoc<ID>, configuring ID generation + auditing + optional version/deleted |
| Query Rules | `references/query-rules.md` | When writing find/aggregation queries, pagination, transactions |
| Index Rules | `references/index-rules.md` | When creating indexes, optimizing queries, reviewing query plans |
| Spring Data Rules | `references/spring-data-rules.md` | When writing Repository interfaces, using @Transactional, mapping annotations, MongoTemplate, EntityCallback |

## How to Apply

### When Designing Documents
Read `references/document-design.md` -> follow naming -> choose embed vs reference -> define common fields -> set BSON types.

### When Creating Entity Classes
Read `references/base-document.md` -> extend BaseMongoDoc<ID> (specify ID type) -> configure MongoDocIdCallback (BeforeConvertCallback) -> enable auditing -> add version/deleted as needed.

### When Writing Queries
Read `references/query-rules.md` -> check find/aggregation rules -> verify pagination -> review transaction scope.

### When Creating Indexes
Read `references/index-rules.md` -> name correctly -> follow ESR rule -> avoid invalidation patterns -> use covered queries.

### When Using Spring Data MongoDB
Read `references/spring-data-rules.md` -> verify Repository patterns -> check mapping annotations -> use audit listeners -> apply EntityCallback API.

### When Reviewing MongoDB Code
1. Read the corresponding reference file based on the code area
2. Verify each rule against the code
3. Categorize violations as **Mandatory** (must fix), **Recommended** (should fix), or **Reference** (nice to have)