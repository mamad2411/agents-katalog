---
name: playbook-devops-cloud-ci-from-zero
description: "Every PR tested, every merge deployable, every deploy reversible — in week one."
---
# Playbook: Stand up CI/CD from zero

> Every PR tested, every merge deployable, every deploy reversible — in week one.

**Track:** 🗺️ DevOps & Cloud · **Domain:** Journey Playbooks · **Level:** journey · **~100 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Every PR tested, every merge deployable, every deploy reversible — in week one.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Structure a fast, honest CI pipeline: start with "Fail cheapest first: format+lint under 2 minutes before anything heavy"
2. Step 2 — Choose and execute deploy strategies: start with "Default to rolling with readiness gates for stateless services"
3. Step 3 — Write production-grade Dockerfiles: start with "Start from slim/distroless variants pinned by digest, not :latest"
4. How it fits together: Fast feedback beats comprehensive coverage initially. Fail cheap, then deepen.

### Referenced Skills

- `ci-cd-pipeline-stages`
- `ci-cd-deploy-strategies`
- `containers-dockerfile-production`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill ci-cd-pipeline-stages && npx skills add aniruddhaadak80/skills --skill ci-cd-deploy-strategies && npx skills add aniruddhaadak80/skills --skill containers-dockerfile-production
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills