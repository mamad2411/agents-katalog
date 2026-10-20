---
name: incident-response-security-phishing-defense-program
description: "Technical controls + easy reporting + blameless drills reducing real click-through damage."
---
# Stand up phishing defense beyond training videos

> Technical controls + easy reporting + blameless drills reducing real click-through damage.

**Track:** 🔐 Cybersecurity · **Domain:** Security Incident Response · **Level:** intermediate · **~30 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Technical controls + easy reporting + blameless drills reducing real click-through damage.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Enforce MFA everywhere, preferring phishing-resistant methods (FIDO2)
2. Deploy DMARC with enforcement; monitor failing sources
3. One-click report button feeding a monitored mailbox
4. Simulate quarterly; measure report-rate not just click-rate
5. Auto-quarantine messages matching reported patterns
6. Blameless follow-ups: fix the process that made the lure plausible

## Common Pitfalls

- Shaming clickers, teaching people to hide clicks
- SMS OTP treated as phishing-resistant

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill incident-response-security-phishing-defense-program
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill incident-response-security-phishing-defense-program -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills