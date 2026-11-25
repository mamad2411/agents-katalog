---
name: huanglangjian-specs
description: "Typed models, routes, and security; OpenAPI 3.2 & JSON Schema 2020-12 generation. Use when declaring typed request/response models, building a router, emitting OpenAPI or JSON Schema, configuring API key / OpenID Connect security, or writing field titles/descriptions."
---

# @huanglangjian/specs

## Workflow

1. Check [Model kinds](./references/model-kinds.md) for available types and factory signatures.
2. Define data models with factory functions (`record`, `enums`, `union`, `taggedUnion`, etc.).
3. Group routes with `router({ id, routes, tag?, basePath?, description? })`.
4. Call `generateOpenapi()` or `generateJsonSchema()` to produce output.

## Key constraints

- `record`, `enums`, `union`, `taggedUnion` must have an `id` — they become named schemas.
- `router` generates an OpenAPI tag from `tag ?? id`. Do NOT set `tags` on individual routes unless extra tags are needed.
- Never write raw `{ kind: "..." }` objects — always use factory functions.

## References

- [Model kinds](./references/model-kinds.md)
- [API reference](./references/api-reference.md)
- [Security](./references/security.md)
- [Usage example](./references/usage-example.md)
- [Init guide](./references/init-guide.md)
- [Patterns & best practices](./references/patterns.md)
- [Writing guide](./references/writing-guide.md)
- [Source map](./references/source-map.md)
