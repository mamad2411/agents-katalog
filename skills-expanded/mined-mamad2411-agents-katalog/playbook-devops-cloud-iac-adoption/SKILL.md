---
name: playbook-devops-cloud-iac-adoption
description: "Bring existing cloud infra under versioned, reviewed management without downtime."
---
# Playbook: Adopt infrastructure-as-code incrementally

> Bring existing cloud infra under versioned, reviewed management without downtime.

**Track:** 🗺️ DevOps & Cloud · **Domain:** Journey Playbooks · **Level:** journey · **~70 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Bring existing cloud infra under versioned, reviewed management without downtime.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Design Terraform modules people reuse: start with "One module = one architectural decision (a network, a service, a store)"
2. Step 2 — Manage IaC state safely as a team: start with "Remote backends with locking enabled; never local state for shared infra"
3. How it fits together: Import one resource class at a time starting with stateless pieces. State hygiene from day zero.

### Referenced Skills

- `infrastructure-as-code-terraform-module-design`
- `infrastructure-as-code-state-management`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill infrastructure-as-code-terraform-module-design && npx skills add aniruddhaadak80/skills --skill infrastructure-as-code-state-management
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills