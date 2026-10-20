---
name: application-security-secrets-hygiene
description: "Generation, storage, rotation, and leak response for credentials humans inevitably touch."
---
# Enforce secrets hygiene end to end

> Generation, storage, rotation, and leak response for credentials humans inevitably touch.

**Track:** 🔐 Cybersecurity · **Domain:** Application Security · **Level:** foundation · **~25 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Generation, storage, rotation, and leak response for credentials humans inevitably touch.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Generate long random secrets via managers; ban hand-invented passwords
2. Inject at runtime from vault/KMS; forbid .env commits with real values
3. Pre-commit hooks scanning for high-entropy strings and known key formats
4. Rotate on schedule AND immediately after any suspected exposure
5. Scope every key least-privilege; prefer short-lived credentials
6. Practice the leak playbook: revoke → rotate → audit access → postmortem

## Common Pitfalls

- Rotated old keys never actually revoked
- Service accounts sharing one god-mode credential

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill application-security-secrets-hygiene
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill application-security-secrets-hygiene -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills