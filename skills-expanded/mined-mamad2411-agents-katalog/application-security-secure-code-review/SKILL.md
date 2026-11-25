---
name: application-security-secure-code-review
description: "Focused pass over authz, injection, secrets, and deserialization on risky diffs."
---
# Security-review code with a repeatable checklist

> Focused pass over authz, injection, secrets, and deserialization on risky diffs.

**Track:** 🔐 Cybersecurity · **Domain:** Application Security · **Level:** intermediate · **~35 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Focused pass over authz, injection, secrets, and deserialization on risky diffs.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Check authorization at object level: can user A read/write user B's records?
2. Trace all external input into queries/commands/paths for injection sinks
3. Scan diffs for hardcoded secrets; verify new config uses secret manager
4. Flag unsafe deserialization and eval-adjacent constructs
5. Verify security headers and CORS changes are intentional, not permissive defaults
6. Document accepted risks inline with ticket references

## Common Pitfalls

- IDOR missed because tests only use one user
- 'Temporary' debug endpoints reaching production

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill application-security-secure-code-review
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill application-security-secure-code-review -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills