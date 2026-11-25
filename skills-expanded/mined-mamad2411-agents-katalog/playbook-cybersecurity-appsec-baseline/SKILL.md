---
name: playbook-cybersecurity-appsec-baseline
description: "From nothing to systematic threat modeling, secrets hygiene, and review gates."
---
# Playbook: Establish an AppSec baseline

> From nothing to systematic threat modeling, secrets hygiene, and review gates.

**Track:** 🗺️ Cybersecurity · **Domain:** Journey Playbooks · **Level:** journey · **~100 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

From nothing to systematic threat modeling, secrets hygiene, and review gates.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Threat model a feature before building it: start with "Diagram the feature: actors, data flows, trust boundaries, stores"
2. Step 2 — Enforce secrets hygiene end to end: start with "Generate long random secrets via managers; ban hand-invented passwords"
3. Step 3 — Security-review code with a repeatable checklist: start with "Check authorization at object level: can user A read/write user B's records?"
4. How it fits together: Secrets first (fastest win), threat models next (cheapest prevention), reviews last (ongoing habit).

### Referenced Skills

- `application-security-threat-model-feature`
- `application-security-secrets-hygiene`
- `application-security-secure-code-review`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill application-security-threat-model-feature && npx skills add aniruddhaadak80/skills --skill application-security-secrets-hygiene && npx skills add aniruddhaadak80/skills --skill application-security-secure-code-review
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills