---
name: cloud-hardening-iam-least-privilege
description: "Start scoped-down, expand only with evidence from real denied actions."
---
# Right-size IAM to least privilege

> Start scoped-down, expand only with evidence from real denied actions.

**Track:** 🔐 Cybersecurity · **Domain:** Cloud Hardening · **Level:** advanced · **~45 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Start scoped-down, expand only with evidence from real denied actions.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Inventory every identity: humans, services, CI roles, third parties
2. Replace wildcards with explicit actions gathered from access logs
3. Separate duties: deploy role cannot read databases
4. MFA enforced for console humans; no long-lived access keys
5. Set permission boundaries so escalation paths are capped
6. Quarterly access reviews with auto-expiring grants

## Common Pitfalls

- Admin roles 'temporarily' granted during setup, forever
- CI pipelines holding prod-write credentials

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill cloud-hardening-iam-least-privilege
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill cloud-hardening-iam-least-privilege -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills