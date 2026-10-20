---
name: clinical-workflow-shift-handoff-isbar
description: "Transfer patient care using Identify-Situation-Background-Assessment-Recommendation so nothing critical drops between shifts."
---
# Run structured shift handoffs with ISBAR

> Transfer patient care using Identify-Situation-Background-Assessment-Recommendation so nothing critical drops between shifts.

**Track:** 🏥 Healthcare & Clinical · **Domain:** Clinical Workflow · **Level:** foundation · **~20 min**

**Who this is for:** Nurses, Physicians, Clinical Managers, Health Informaticists

## When to Use This Skill

Transfer patient care using Identify-Situation-Background-Assessment-Recommendation so nothing critical drops between shifts.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Identify: name, age, location, attending team for each patient
2. Situation: current diagnosis and reason for admission in one sentence
3. Background: relevant history, allergies, code status, isolation needs
4. Assessment: latest vitals trends and your clinical concern level
5. Recommendation: pending tasks, watch-fors, escalation thresholds
6. Receiver reads back action items before closing each handoff

## Common Pitfalls

- Social chat interleaved with handoff losing structure
- Vague watch-fors like 'if worse, call' without thresholds

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill clinical-workflow-shift-handoff-isbar
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill clinical-workflow-shift-handoff-isbar -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills