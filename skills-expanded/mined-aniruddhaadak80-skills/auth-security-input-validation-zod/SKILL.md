---
name: auth-security-input-validation-zod
description: "Parse, don't validate: coerce untrusted input into typed values once at the edge."
---
# Validate all external input at the boundary

> Parse, don't validate: coerce untrusted input into typed values once at the edge.

**Track:** ⚙️ Backend Engineering · **Domain:** Auth & Security Basics · **Level:** foundation · **~25 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Parse, don't validate: coerce untrusted input into typed values once at the edge.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define schemas per endpoint covering body, query, params, headers
2. Reject unknown fields by default; allowlists beat blocklists
3. Coerce types explicitly; fail closed on ambiguity
4. Return field-level errors machines can render
5. Reuse the same schemas for client-side forms where possible
6. Fuzz one nasty payload corpus against public endpoints in CI

## Common Pitfalls

- Validating in UI but trusting raw req.body server-side
- Mass assignment from spreads straight into ORM updates

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill auth-security-input-validation-zod
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill auth-security-input-validation-zod -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills