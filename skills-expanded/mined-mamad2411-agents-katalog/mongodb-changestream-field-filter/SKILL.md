---
tags: [backend, mongodb, changestream, field, filter]
name: mongodb-changestream-field-filter
description: Filter MongoDB change stream UPDATE events by inspecting updateDescription.updatedFields so irrelevant mutations do not trigger downstream work; INSERT/DELETE fall through as always-relevant.
trigger: High-churn MongoDB collection drives a change stream but only a subset of field changes should cause downstream processing (policy re-eval, cache invalidation, re-index).
source_project: lucida-alarm
version: 1.0.0
category: backend
linked_knowledge:
  - mongodb-changestream-resubscribe
---

# MongoDB Change Stream Field Filter

## Shape

Listener receives `ChangeStreamDocument`. For `UPDATE`, read `updateDescription.updatedFields` (a BsonDocument of `dottedPath → value`). Return a boolean `isRelevant` before handing off to the expensive processor.

## Steps

1. Register listener via Spring Data MongoDB (reactive or blocking driver).
2. Branch on `OperationType`: `INSERT` / `DELETE` → always relevant.
3. `UPDATE` → `updatedFields = event.getUpdateDescription().getUpdatedFields()`.
4. Exact check: `updatedFields.containsKey("groupId")`.
5. Nested/wildcard: `updatedFields.keySet().stream().anyMatch(k -> k.startsWith("tags."))`.
6. Combine with OR over the "relevant fields" set; return the boolean.
7. Not relevant → log TRACE and skip. Relevant → delegate to processor.
8. Persist `resumeToken` so reconnection skips already-seen events.

## Counter / Caveats

- `updatedFields` is keyed by **dotted path at the leaf changed**. A whole-subdoc replace shows as `"parent"`, not `"parent.child"` — handle both.
- Full-document replaces (`$set` on root) may surface every field as "updated"; treat as relevant.
- Never skip DELETEs on field filter — there are no fields to inspect.
- Network hiccup / replica-set election → stream goes silent without exception; pair with `mongodb-changestream-resubscribe` knowledge.
