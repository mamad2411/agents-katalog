---
name: soc-operations-alert-triage-discipline
description: "Enrichment order, true/false-positive calls with evidence, and escalation criteria applied identically every shift."
---
# Triage alerts with consistent depth

> Enrichment order, true/false-positive calls with evidence, and escalation criteria applied identically every shift.

**Track:** 🛡️ Cyber Defense & SOC · **Domain:** SOC Operations · **Level:** foundation · **~25 min**

**Who this is for:** SOC Analysts, Detection Engineers, Threat Hunters, Blue Teams

## When to Use This Skill

Enrichment order, true/false-positive calls with evidence, and escalation criteria applied identically every shift.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Pull alert context first: entity history, related alerts last 7 days
2. Enrich systematically: IP reputation, hash verdicts, identity risk, asset criticality
3. Validate against known-change calendar before calling malicious
4. Classify with evidence links attached — no verdict without artifact
5. Escalate by blast radius criteria written down, not gut feel
6. Log analyst notes reusable by the next person

## Common Pitfalls

- Auto-closing batches to clear the queue before events
- Verdicts without captured evidence being unreproducible

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill soc-operations-alert-triage-discipline
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill soc-operations-alert-triage-discipline -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills