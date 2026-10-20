---
name: observability-structured-logging
description: "JSON logs with trace correlation and disciplined fields you can actually query at 3am."
---
# Adopt structured logging that answers questions

> JSON logs with trace correlation and disciplined fields you can actually query at 3am.

**Track:** ☁️ DevOps & Cloud · **Domain:** Observability · **Level:** foundation · **~25 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

JSON logs with trace correlation and disciplined fields you can actually query at 3am.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Log JSON with timestamp, level, service, route, request_id, user_id
2. Propagate trace IDs across services and into log lines
3. Reserve ERROR for things needing action; INFO is default heartbeat
4. Never log secrets or PII; enforce with lint rules and sampling reviews
5. Sample high-volume debug logs; keep 100% of errors
6. Practice one query drill: 'find all errors for this user yesterday'

## Common Pitfalls

- String-interpolated logs unsearchable in aggregators
- Stack traces swallowed into single-line messages

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill observability-structured-logging
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill observability-structured-logging -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills