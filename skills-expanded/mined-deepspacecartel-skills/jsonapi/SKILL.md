---
name: jsonapi
description: How to design and review a JSON:API v1.1 response/request format (https://jsonapi.org/) - project-agnostic. Covers the application/vnd.api+json document shape (resource objects, relationships, compound documents), the reserved query-parameter families (include, fields, sort, page, filter), CRUD semantics and status codes for creating/updating/deleting resources and relationships, and error objects and content negotiation. Use when designing a REST API's response format, reviewing an endpoint for spec compliance, implementing include/sparse-fieldsets/sorting/pagination/filtering, or writing error responses.
---

# JSON:API (v1.1)

How to shape requests and responses so a JSON:API client can rely on
structure alone — no per-endpoint documentation needed for "where's the
id" or "how do I ask for related data." The spec is at
[jsonapi.org/format](https://jsonapi.org/format/).

Every JSON:API payload is served as `application/vnd.api+json`. The
spec draws a line between three kinds of meaning:
- **Specification semantics** — members, query parameters, and rules
  this document defines. You can't repurpose these.
- **Implementation semantics** — left to you (extra `meta`, custom
  `page` strategy, etc.).
- **Reserved semantics** — not yet defined, reserved for future spec
  versions. Don't squat on them.

The spec evolves by "never remove, only add" — a `1.x` server never
breaks a `1.0` client.

## The core idea

A handful of rules do most of the work of keeping a JSON:API document
predictable:
- A top-level document has `data` **or** `errors`, never both — plus
  optional `meta`, `links`, `included`, `jsonapi`. No `data`, no
  `included`.
- Every resource object needs `type` and `id` (a not-yet-created
  resource may use `lid` instead of `id`) — that pair is the resource's
  identity everywhere it appears in the document.
- Attributes and relationships are collectively "fields," and share one
  namespace with `type`/`id` — you can't have an attribute and a
  relationship with the same name, and neither can be named `type` or
  `id`.
- A compound document (one with `included`) needs **full linkage**:
  every included resource must be reachable by walking relationships
  from the primary data, or a sparse-fieldset request that explicitly
  drops that linkage.

## Where to look

| Reference | Covers |
|---|---|
| [`references/document-structure.md`](references/document-structure.md) | Top-level document shape, resource & resource-identifier objects, relationships and resource linkage, links, `meta`, the `jsonapi` object, member-name rules, compound documents |
| [`references/query-parameters.md`](references/query-parameters.md) | Fetching resources/relationships, `include`, sparse fieldsets (`fields[TYPE]`), `sort`, `page`, `filter`, and the general query-parameter-family rules |
| [`references/writing-resources.md`](references/writing-resources.md) | Creating, updating, and deleting resources; updating relationships directly (PATCH/POST/DELETE); the response-code table implementers get wrong most |
| [`references/errors-and-negotiation.md`](references/errors-and-negotiation.md) | Content negotiation (`Content-Type`/`Accept`, `ext`/`profile`), extensions vs. profiles, error objects |

## Quick orientation

A minimal document — one article resource with an attribute
and a to-one relationship, fetched via `GET /articles/1`:

```json
{
  "data": {
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "JSON:API paints my bikeshed!"
    },
    "relationships": {
      "author": {
        "links": {
          "self": "/articles/1/relationships/author",
          "related": "/articles/1/author"
        },
        "data": { "type": "people", "id": "9" }
      }
    },
    "links": { "self": "/articles/1" }
  }
}
```

Note what's *not* here: `author_id` as an attribute. Once a field is a
real relationship, its foreign key doesn't also appear as an attribute
— see
[`references/document-structure.md`](references/document-structure.md)
for why.
