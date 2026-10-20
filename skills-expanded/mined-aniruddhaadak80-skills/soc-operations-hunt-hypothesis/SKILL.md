---
name: soc-operations-hunt-hypothesis
description: "Structured hunts starting from TTP intelligence, producing detections or documented negatives."
---
# Hunt threats with falsifiable hypotheses

> Structured hunts starting from TTP intelligence, producing detections or documented negatives.

**Track:** 🛡️ Cyber Defense & SOC · **Domain:** SOC Operations · **Level:** advanced · **~45 min**

**Who this is for:** SOC Analysts, Detection Engineers, Threat Hunters, Blue Teams

## When to Use This Skill

Structured hunts starting from TTP intelligence, producing detections or documented negatives.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Pick one TTP from intel relevant to your stack this month
2. Write hypothesis: 'IF technique X used THEN artifacts Y visible in Z source'
3. Verify telemetry actually covers Z before hunting (coverage map)
4. Query broadly first, narrow on anomaly clusters
5. Outcome A: findings → immediate detection rule + IR handoff
6. Outcome B: negative → document coverage gap or baseline noise profile

## Common Pitfalls

- Hunting where logs don't exist, wasting hours
- Findings living in hunt notes, never becoming detections

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill soc-operations-hunt-hypothesis
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill soc-operations-hunt-hypothesis -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills