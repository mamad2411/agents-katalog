---
name: cloud-hardening-patch-cadence
description: "Triage vulnerabilities by exploitability and ship patches within defined SLAs."
---
# Run a patch cadence that actually closes windows

> Triage vulnerabilities by exploitability and ship patches within defined SLAs.

**Track:** 🔐 Cybersecurity · **Domain:** Cloud Hardening · **Level:** intermediate · **~30 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Triage vulnerabilities by exploitability and ship patches within defined SLAs.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Aggregate findings from scanners, dependabots, and CISA feeds weekly
2. Classify by exploitability × exposure; internet-facing criticals patch in 72h
3. Automate dependency bumps with test-gated PRs
4. Maintain golden base images patched monthly
5. Track mean-time-to-patch per severity; report trend to leadership
6. Keep an exception register with expiries, not permanent waivers

## Common Pitfalls

- Scanner noise drowning real risk; tune detections
- Patching libraries while base images rot

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill cloud-hardening-patch-cadence
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill cloud-hardening-patch-cadence -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills