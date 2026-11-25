---
name: json-api
description: >-
  JSON:API 1.1: design, build and review APIs that exchange application/vnd.api+json documents, with resource objects, relationships, compound documents, sparse fieldsets, sorting, pagination, filtering, error objects, extensions and profiles. Use when implementing or reviewing a JSON:API server or client: content negotiation with the ext and profile media type parameters (415 and 406), the top-level data, errors, meta, links, included and jsonapi members, type, id and lid, attributes and relationships, resource linkage and full linkage, include, fields[TYPE], sort, page[...] and filter[...] query parameter families, implementation-specific query parameter naming, POST, PATCH and DELETE on resources and relationship links, client-generated IDs, 201, 202, 204, 403, 404 and 409 responses, error objects with source.pointer, and the Atomic Operations extension (atomic:operations, atomic:results). Targets JSON:API 1.1; supports JSON:API 1.0, and tracks the JSON:API 1.2 draft.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# JSON:API

JSON:API is a specification, published at jsonapi.org by its editors, for how a client requests that resources be fetched or modified and how a server responds, using the `application/vnd.api+json` media type. With this skill the agent designs endpoints, produces and parses JSON:API documents, negotiates extensions and profiles, and implements the Atomic Operations extension.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

JSON:API sections have anchors but no numbers, so citations name the heading, for example (Compound Documents).

## Inputs (fill in, or ask before starting)

- Role: server, client, or both.
- Target version: JSON:API 1.1 (default; finalized 2022-09-30). JSON:API 1.0 is supported: target it only for a named peer that rejects the `ext` and `profile` media type parameters. The JSON:API 1.2 draft is a preview (posture: track): never claim it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the jsonapi.org milestones and the `_format/` folder of the GitHub repository for a new version, and update the pins.
- Features: which of `include`, sparse fieldsets, `sort`, pagination, `filter`, client-generated IDs, relationship endpoints and writes the API supports.
- Extensions and profiles: the URIs the API applies, for example `https://jsonapi.org/ext/atomic`.

## Invariants

1. **Media type and parameters.** Every JSON:API payload is sent with `Content-Type: application/vnd.api+json`; the only allowed parameters are `ext` and `profile`, each a quoted space-separated list of URIs (Universal Responsibilities; Rules for Media Type Parameters).
2. **Server negotiation.** A request `Content-Type` with any other parameter, or with an unsupported `ext` URI, gets `415`. An `Accept` whose JSON:API instances all carry other parameters, or all carry an unsupported `ext`, gets `406`. Unknown profiles are ignored (Server Responsibilities).
3. **Top level.** A document has at least one of `data`, `errors`, `meta` or an extension member; `data` and `errors` never coexist; `included` needs `data` (Top Level).
4. **Collections are arrays.** Primary data for a collection is an array, even with one or zero items; a single resource is an object or `null` (Top Level).
5. **Identity.** Every resource object has a string `type` and `id`; only a client-originated new resource may omit `id`, and may use `lid` instead. `type` plus `id` identifies exactly one resource in the API (Identification).
6. **Shared field namespace.** Attributes and relationships share one namespace with `type` and `id`: no field named `type` or `id`, and no attribute and relationship with the same name. Foreign keys such as `author_id` should be relationships, not attributes (Fields; Attributes).
7. **Full linkage, no duplicates.** Every included resource is reachable through a chain of relationships from the primary data, unless sparse fieldsets removed the linkage, and each `type` and `id` pair appears at most once (Compound Documents).
8. **No extra members.** Objects defined by the specification or an applied extension contain no other members, and implementations ignore non-compliant members (Document Structure).
9. **Member names.** Implementation and profile member names are case sensitive, start and end with `a-z`, `A-Z`, `0-9` or U+0080 and above, may contain `-`, `_` or space inside, and never contain the reserved characters such as `+ , . [ ] : / @` (Member Names). Extension members are `namespace:name` (Extension Members).
10. **Query parameter names.** Implementation-specific parameters belong to a family whose base name is a legal member name with at least one character outside `a-z` (camelCase recommended); an unknown or non-conforming parameter gets `400` (Implementation-Specific Query Parameters).
11. **Unsupported features fail loudly.** `include` on an endpoint that does not support it, an unknown relationship path, or an unsupported `sort` gets `400` (Inclusion of Related Resources; Sorting).
12. **Writes are all or nothing.** A request completely succeeds or fails; no partial updates (Creating, Updating and Deleting Resources).
13. **PATCH is a merge.** Missing attributes and relationships keep their current values and are never read as `null` (Updating a Resource's Attributes; Updating a Resource's Relationships).
14. **Errors.** Error objects go in a top-level `errors` array; each has at least one member, and `status`, when present, is a string (Error Objects).

## Workflow

1. **Pick the version.** Use JSON:API 1.1 unless a named peer only speaks 1.0.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not the 1.2 draft.
2. **Model resources.** Choose `type` values, attributes and relationships; give every relationship a `self` and/or `related` link or linkage.
   -> [`references/document-structure.md`](references/document-structure.md)
   ✓ No field is named `type` or `id`, no foreign key is an attribute, and every member name passes the Member Names rules.
3. **Implement content negotiation.** Send the media type with `ext` and `profile` when applied, answer `415` and `406` as the rules say, and send `Vary: Accept` when the server supports `ext` or `profile`.
   -> [`references/errors-and-extensions.md`](references/errors-and-extensions.md)
   ✓ A request with `Content-Type: application/vnd.api+json; charset=utf-8` gets `415`.
4. **Implement fetching.** Serve every `self` and `related` URL you emit; add `include`, `fields[TYPE]`, `sort`, `page[...]` and `filter[...]` as chosen.
   -> [`references/fetching.md`](references/fetching.md)
   ✓ A compound document has full linkage, unrequested resources are absent, and unsupported features return `400`.
5. **Implement writes.** `POST` to collections, `PATCH` and `DELETE` on resources, and `PATCH`, `POST` and `DELETE` on relationship links, with the status codes each response section requires.
   -> [`references/writing.md`](references/writing.md)
   ✓ Each write returns the status the spec requires for its outcome, and a `PATCH` without an attribute leaves it unchanged.
6. **Return errors.** Build error objects with `status`, `title`, `detail` and `source.pointer`, `source.parameter` or `source.header`; pick the most generally applicable status for several errors.
   -> [`references/errors-and-extensions.md`](references/errors-and-extensions.md)
   ✓ Every `source.pointer` points at a value that exists in the request document.
7. **Add extensions or profiles** (only when needed). Implement Atomic Operations for ordered, atomic batches; define a profile for shared implementation semantics.
   -> [`references/errors-and-extensions.md`](references/errors-and-extensions.md)
   ✓ Every extension member and query parameter is namespaced, and `atomic:results` has the same length as `atomic:operations`.
8. **Upgrade** (only when asked). Follow the 1.0 to 1.1 steps.
   -> [`references/versions.md`](references/versions.md)
   ✓ 1.0 clients still work, and the 1.1 features you claim follow the 1.1 rules.

## Verify before done

- [ ] Every response and request body carries `application/vnd.api+json`, with `ext` and `profile` listed when applied and no other parameter (Universal Responsibilities).
- [ ] `415`, `406` and `400` are returned in exactly the cases the spec names (Server Responsibilities; Query Parameters; Inclusion of Related Resources; Sorting).
- [ ] No document has both `data` and `errors`, or `included` without `data` (Top Level).
- [ ] Every resource object has string `type` and `id` (or `lid` for a new client resource), and `type` and `id` pairs are unique in compound documents (Identification; Compound Documents).
- [ ] Sparse fieldsets never return a field the client did not ask for (Sparse Fieldsets).
- [ ] Pagination links use only `first`, `last`, `prev` and `next`, omitted or `null` when unavailable (Pagination).
- [ ] `201` responses carry the created resource and a `Location` that matches `links.self` when both are present (201 Created).
- [ ] Custom query parameters contain a non `a-z` character, and extension parameters are `namespace:name` (Query Parameters).
- [ ] Nothing claims JSON:API 1.2 in `jsonapi.version`.

## Reference index

- **`references/versions.md`**: JSON:API 1.1, 1.0 and the 1.2 draft, which to use, what 1.1 added, the 1.0 to 1.1 upgrade, and the preview. Load for steps 1 and 8.
- **`references/document-structure.md`**: top level, resource objects, `lid`, relationships, linkage, compound documents, links and link objects, meta, the `jsonapi` object, member names and @-Members. Load for step 2.
- **`references/fetching.md`**: fetching resources and relationships, `include`, sparse fieldsets, sorting, pagination, filtering, query parameter families and parsing. Load for step 4.
- **`references/writing.md`**: creating, updating and deleting resources and relationships, client-generated IDs, and every write status code. Load for step 5.
- **`references/errors-and-extensions.md`**: content negotiation, error objects, extensions and profiles, and the Atomic Operations extension. Load for steps 3, 6 and 7.

## Related skills

- `http-semantics` for methods, status codes, `Location`, `Vary` and content negotiation in general: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.
- `problem-details` for RFC 9457 errors on endpoints that are not JSON:API: `npx skills add ScaleDockHQ/scaledock-skills --skill problem-details`.
- `openapi` for describing a JSON:API in an OpenAPI document, for example as the target of a `describedby` link: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `json-schema` for validating documents and attribute shapes: `npx skills add ScaleDockHQ/scaledock-skills --skill json-schema`.
- `graphql` when comparing JSON:API with a GraphQL endpoint on the same service: `npx skills add ScaleDockHQ/scaledock-skills --skill graphql`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [JSON:API Latest Specification](https://jsonapi.org/format/): latest specification page, serves v1.1, checked 2026-10-05.
- [JSON:API v1.1](https://jsonapi.org/format/1.1/): Stable (archived copy, normative text frozen), v1.1 finalized 2022-09-30, checked 2026-10-05.
- [JSON:API v1.0](https://jsonapi.org/format/1.0/): archived copy, normative text frozen, v1.0 final 2015-05-29, checked 2026-10-05.
- [JSON:API v1.2](https://jsonapi.org/format/1.2/): Still in Development (working draft), checked 2026-10-05.
- [Atomic Operations extension](https://jsonapi.org/ext/atomic/): extension listed by the editors, unversioned, URI `https://jsonapi.org/ext/atomic`, checked 2026-10-05.
- [Extensions and Profiles](https://jsonapi.org/extensions/): registry page maintained by the editors, checked 2026-10-05.
- [JSON:API home page](https://jsonapi.org/): milestones list, checked 2026-10-05.
- [json-api/json-api repository](https://github.com/json-api/json-api): source of jsonapi.org, `gh-pages` at `bde79ce` (2026-10-04), tag `v1.1` at `db7abaa` (2022-09-30), checked 2026-10-05.
