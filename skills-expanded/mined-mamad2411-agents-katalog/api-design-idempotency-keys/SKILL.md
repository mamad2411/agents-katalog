---
name: api-design-idempotency-keys
description: "Accept retried mutations gracefully by keying operations so duplicates return the original result."
---
# Make writes safe with idempotency keys

> Accept retried mutations gracefully by keying operations so duplicates return the original result.

**Track:** ⚙️ Backend Engineering · **Domain:** API Design · **Level:** intermediate · **~30 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Accept retried mutations gracefully by keying operations so duplicates return the original result.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Require an Idempotency-Key header on POST payments, orders, and signups
2. Store key + request hash + response in a table with TTL cleanup
3. On replay with same payload, return stored response with replayed flag
4. On same key different payload, reject with 422 conflict
5. Expire keys after 24-48h depending on client retry windows
6. Load-test double-submit behavior before launch week

## Common Pitfalls

- Keying only by user ID, colliding legitimate new requests
- Storing responses forever without TTL or encryption

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-idempotency-keys
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-idempotency-keys -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills