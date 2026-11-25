---
name: exploratory-analysis-dataset-health-check
description: "Profile distributions, missingness, leakage risks, and unit sanity before trusting any result."
---
# Run a dataset health check before modeling

> Profile distributions, missingness, leakage risks, and unit sanity before trusting any result.

**Track:** 📊 Data Science & Analytics · **Domain:** Exploratory Analysis · **Level:** foundation · **~30 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

Profile distributions, missingness, leakage risks, and unit sanity before trusting any result.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Check shape, dtypes, and unique counts; flag columns failing expectations
2. Plot distributions for numeric columns; eyeball impossible values
3. Quantify missingness patterns: MCAR vs structured gaps telling stories
4. Hunt leakage: fields created after outcome timestamps
5. Verify joins didn't fan-out rows silently (count before/after)
6. Write a one-page data dictionary others can trust

## Common Pitfalls

- Aggregating across mixed currencies/timezones
- Imputing before understanding why data is missing

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill exploratory-analysis-dataset-health-check
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill exploratory-analysis-dataset-health-check -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills