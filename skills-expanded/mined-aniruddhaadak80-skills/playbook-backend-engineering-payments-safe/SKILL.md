---
name: playbook-backend-engineering-payments-safe
description: "Process money mutations with idempotency guarantees and clean audit trails."
---
# Playbook: Take payments without duplicates

> Process money mutations with idempotency guarantees and clean audit trails.

**Track:** 🗺️ Backend Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~90 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Process money mutations with idempotency guarantees and clean audit trails.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Make writes safe with idempotency keys: start with "Require an Idempotency-Key header on POST payments, orders, and signups"
2. Step 2 — Validate all external input at the boundary: start with "Define schemas per endpoint covering body, query, params, headers"
3. Step 3 — Build trustworthy background job processing: start with "Make handlers idempotent; assume at-least-once delivery"
4. How it fits together: Money endpoints get idempotency keys, validation schemas, and job-based side effects. No exceptions.

### Referenced Skills

- `api-design-idempotency-keys`
- `auth-security-input-validation-zod`
- `caching-queues-background-jobs`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-idempotency-keys && npx skills add aniruddhaadak80/skills --skill auth-security-input-validation-zod && npx skills add aniruddhaadak80/skills --skill caching-queues-background-jobs
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills