---
name: playbook-cybersecurity-cloud-hardening-sprint
description: "Close the common cloud misconfiguration classes auditors and attackers both look for."
---
# Playbook: Harden cloud accounts in a sprint

> Close the common cloud misconfiguration classes auditors and attackers both look for.

**Track:** 🗺️ Cybersecurity · **Domain:** Journey Playbooks · **Level:** journey · **~75 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Close the common cloud misconfiguration classes auditors and attackers both look for.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Right-size IAM to least privilege: start with "Inventory every identity: humans, services, CI roles, third parties"
2. Step 2 — Run a patch cadence that actually closes windows: start with "Aggregate findings from scanners, dependabots, and CISA feeds weekly"
3. How it fits together: Inventory identities before touching policies. Least privilege without inventory breaks production.

### Referenced Skills

- `cloud-hardening-iam-least-privilege`
- `cloud-hardening-patch-cadence`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill cloud-hardening-iam-least-privilege && npx skills add aniruddhaadak80/skills --skill cloud-hardening-patch-cadence
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills