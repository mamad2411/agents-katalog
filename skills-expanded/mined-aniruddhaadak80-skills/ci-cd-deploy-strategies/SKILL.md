---
name: ci-cd-deploy-strategies
description: "Rolling, blue-green, canary: pick per risk profile and wire automated rollback triggers."
---
# Choose and execute deploy strategies

> Rolling, blue-green, canary: pick per risk profile and wire automated rollback triggers.

**Track:** ☁️ DevOps & Cloud · **Domain:** CI/CD · **Level:** advanced · **~35 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Rolling, blue-green, canary: pick per risk profile and wire automated rollback triggers.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Default to rolling with readiness gates for stateless services
2. Canary risky changes: 5% traffic, auto-halt on error-rate delta
3. Blue-green for schema-sensitive releases needing instant revert
4. Every deploy ships with a one-command rollback rehearsed quarterly
5. Verify post-deploy: synthetic checks plus error-budget burn alerting
6. Record release notes linking PRs for audit trails

## Common Pitfalls

- Migrations entangled with app deploys violating expand-contract
- Rollback tested for the first time during an incident

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill ci-cd-deploy-strategies
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill ci-cd-deploy-strategies -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills