---
name: api-design-rest-resource-modeling-rpc
description: "Design stable resource-oriented endpoints with deliberate error contracts and pagination."
---
# Model REST resources without leaking internals (gRPC services)

> Design stable resource-oriented endpoints with deliberate error contracts and pagination.

**Track:** ⚙️ Backend Engineering · **Domain:** API Design · **Level:** foundation · **~30 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Design stable resource-oriented endpoints with deliberate error contracts and pagination.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. List nouns (resources) from the domain; map verbs to HTTP methods
2. Pluralize collections; nest at most one level for ownership
3. Standardize errors as {code, message, details} with correct status codes
4. Paginate every collection by cursor; never offset past 10k rows
5. Version in the URL path from v1; document deprecation policy
6. Publish an OpenAPI spec and generate clients from it
7. Define proto packages with backward-compatible field numbering
8. Map gRPC status codes to HTTP at the gateway

## Common Pitfalls

- RPC-in-disguise endpoints like /getUserData
- Leaking column names and internal IDs in payloads

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-rest-resource-modeling-rpc
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-rest-resource-modeling-rpc -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills