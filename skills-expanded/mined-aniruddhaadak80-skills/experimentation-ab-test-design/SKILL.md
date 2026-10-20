---
name: experimentation-ab-test-design
description: "Power the test upfront, guard metrics, and commit to decision rules before peeking."
---
# Design an A/B test you can trust

> Power the test upfront, guard metrics, and commit to decision rules before peeking.

**Track:** 📊 Data Science & Analytics · **Domain:** Experimentation & A/B Testing · **Level:** intermediate · **~35 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

Power the test upfront, guard metrics, and commit to decision rules before peeking.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define one primary metric with minimum detectable effect from business value
2. Compute required sample size for 80% power at α=0.05 two-sided
3. Randomize at user level with sticky assignment across sessions
4. Add guardrail metrics: latency, error rate, unsubscribe, revenue per user
5. Commit to runtime and decision rule BEFORE launch; no mid-flight goalposts
6. Log the design doc; results include confidence intervals not just p-values

## Common Pitfalls

- Peeking daily and stopping at first significance
- Underpowered tests 'proving' null effects

## Success Signals

- 100% of launched tests with pre-registered designs
- SRM check passing (sample ratio mismatch)

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-ab-test-design
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-ab-test-design -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills