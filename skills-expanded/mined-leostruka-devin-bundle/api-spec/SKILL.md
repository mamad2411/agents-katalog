---
name: api-spec
description: Use when the user wants to design, review, or document an API (REST, OpenAPI, versioning, error models, contract testing, authentication), or when generating/maintaining OpenAPI specs as machine-readable context for AI agents.
triggers: [user, model]
---

# API Spec

Design and review HTTP/gRPC/GraphQL APIs, and keep the contract explicit,
versioned, and machine-readable (OpenAPI). The spec is the primary context
for agents — they work from the spec, not from implementation memory.

## Design protocol

1. **Collect constraints** — consumers, auth, rate limits, error handling,
   versioning.
2. **Choose style** — REST, gRPC, GraphQL, or hybrid per use case.
3. **Design endpoints** — nouns as resources, consistent paths, status
   codes, error model.
4. **Specify input/output/behavior** — every endpoint declares input schema,
   output schema, observable behavior. A spec lacking I/O is incomplete.
5. **Write the contract** — OpenAPI spec (or proto), validated with tools.
6. **Add tests** — contract, serialization, happy/unhappy paths.
7. **Document + sync** — spec stays in version control, in sync with code.

## What a spec must include

1. **Endpoints** — paths, methods, parameters, request/response schemas.
2. **Authentication** — type, headers, token format.
3. **Error responses** — status codes, error schemas, retry semantics.
4. **Versioning** — version, deprecation policy, migration path.
5. **Rate limits** — rps, burst, backoff strategy.

## Process

```
Design/review API → generate/update OpenAPI → validate against impl →
use spec as agent context → keep in VCS
```

## Anti-patterns

- No spec, or an outdated one.
- Spec in prose instead of OpenAPI.
- Spec not versioned / not in version control.
- Agents reading implementation code instead of the spec.

## Output rule

Deliver a spec file, examples, and a test command. Validate with
`swagger-codegen` or equivalent when available.
