---
name: infrastructure-as-code-state-management
description: "Remote state with locking, environment isolation, and least-privilege access so nobody corrupts prod."
---
# Manage IaC state safely as a team

> Remote state with locking, environment isolation, and least-privilege access so nobody corrupts prod.

**Track:** ☁️ DevOps & Cloud · **Domain:** Infrastructure as Code · **Level:** intermediate · **~30 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Remote state with locking, environment isolation, and least-privilege access so nobody corrupts prod.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Remote backends with locking enabled; never local state for shared infra
2.  Separate state per environment and blast-radius boundary
3. Plan applies through CI with reviewed plan artifacts
4. Restrict who can apply to prod; everyone can plan against staging copies
5. Backup state versions; rehearse recovery from zero
6. Import legacy resources deliberately with documentation

## Common Pitfalls

- Shared state across envs turning staging apply into prod apply
- -replace used casually against stateful resources

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill infrastructure-as-code-state-management
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill infrastructure-as-code-state-management -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills