---
name: incident-response-security-breach-first-hour-ransomware
description: "Contain, preserve evidence, and communicate without tipping off or destroying forensics."
---
# Execute the first hour of a suspected breach (Ransomware scenario)

> Contain, preserve evidence, and communicate without tipping off or destroying forensics.

**Track:** 🔐 Cybersecurity · **Domain:** Security Incident Response · **Level:** advanced · **~30 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Contain, preserve evidence, and communicate without tipping off or destroying forensics.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Activate the IR channel; start a timestamped scribe log immediately
2. Preserve evidence BEFORE aggressive remediation (snapshots, memory dumps)
3. Contain: revoke sessions/keys, isolate affected hosts, block indicators
4. Determine blast radius: what data, which accounts, what timeframe
5. Engage legal/compliance early for notification obligations (e.g., 72h GDPR)
6. Brief executives with facts-not-speculation updates hourly
7. Isolate backups and verify offline copies intact before any recovery
8. Never negotiate or pay without legal + law-enforcement consultation

## Common Pitfalls

- Wiping compromised machines destroying evidence
- Silent handling violating breach-notification laws

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill incident-response-security-breach-first-hour-ransomware
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill incident-response-security-breach-first-hour-ransomware -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills