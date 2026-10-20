---
name: detection-purple-purple-validation
description: "Safe technique emulation proving alerts fire end-to-end, producing concrete coverage evidence."
---
# Validate detections with purple-team exercises

> Safe technique emulation proving alerts fire end-to-end, producing concrete coverage evidence.

**Track:** 🛡️ Cyber Defense & SOC · **Domain:** Detection & Purple Team · **Level:** intermediate · **~40 min**

**Who this is for:** SOC Analysts, Detection Engineers, Threat Hunters, Blue Teams

## When to Use This Skill

Safe technique emulation proving alerts fire end-to-end, producing concrete coverage evidence.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Select atomic tests matching your mapped priority techniques
2. Run in isolated lab mirroring production logging config exactly
3. Trace: did endpoint event reach SIEM parse correctly AND alert fire?
4. Record three states: detected / ingested-not-alerted / not-ingested
5. File engineering tickets per gap with retest dates
6. Report coverage trend to leadership in techniques-validated terms

## Common Pitfalls

- Testing in labs whose log pipelines differ from production
- Emulations risky enough to trigger real incidents uncontrolled

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill detection-purple-purple-validation
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill detection-purple-purple-validation -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills