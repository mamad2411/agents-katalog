---
name: critical-consumption-ab-test-reading-checklist
description: "Validity checklist catching underpowered tests, peeking, and metric tricks in published results."
---
# Read other people's A/B tests critically

> Validity checklist catching underpowered tests, peeking, and metric tricks in published results.

**Track:** 📊 Data Science & Analytics · **Domain:** Critical Consumption · **Level:** intermediate · **~25 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

Validity checklist catching underpowered tests, peeking, and metric tricks in published results.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Check sample size math against claimed effect size first
2. Look for stopping rules: when did they decide it was over?
3. Verify primary metric matches headline claim exactly
4. Inspect guardrails: what degraded while the winner won?
5. Segment sanity: does the effect survive obvious subgroups?
6. Estimate business impact yourself from raw numbers provided

## Common Pitfalls

- Headline metrics switched post-hoc from preregistered ones
- Relative percentages hiding absolute effects near zero

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill critical-consumption-ab-test-reading-checklist
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill critical-consumption-ab-test-reading-checklist -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills