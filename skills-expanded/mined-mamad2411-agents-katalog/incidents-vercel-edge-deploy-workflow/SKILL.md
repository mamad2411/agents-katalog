---
name: incidents-vercel-edge-deploy-workflow
description: "Preview-per-PR, promotion flows, and env hygiene on platforms like Vercel/Netlify."
---
# Ship frontends via edge platforms safely

> Preview-per-PR, promotion flows, and env hygiene on platforms like Vercel/Netlify.

**Track:** ☁️ DevOps & Cloud · **Domain:** Incidents & Edge Deploys · **Level:** foundation · **~20 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Preview-per-PR, promotion flows, and env hygiene on platforms like Vercel/Netlify.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Every PR gets a preview URL wired to ephemeral env vars
2. Protect prod: deploys gated on checks, promotions explicit not accidental
3. Keep secrets in platform env settings, never committed .env files
4. Alias domains to immutable deployments for instant rollback
5. Use tokens/CI for machine deploys; browser OAuth breaks on clock drift
6. Watch function limits: cold starts, memory, execution caps per plan tier

## Common Pitfalls

- Team sharing one account instead of scoped tokens
- Preview branches hitting production databases

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill incidents-vercel-edge-deploy-workflow
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill incidents-vercel-edge-deploy-workflow -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills