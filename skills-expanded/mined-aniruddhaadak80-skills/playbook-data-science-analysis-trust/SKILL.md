---
name: playbook-data-science-analysis-trust
description: "From raw tables to defensible findings with documented caveats."
---
# Playbook: Produce an analysis stakeholders trust

> From raw tables to defensible findings with documented caveats.

**Track:** 🗺️ Data Science & Analytics · **Domain:** Journey Playbooks · **Level:** journey · **~85 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

From raw tables to defensible findings with documented caveats.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Run a dataset health check before modeling: start with "Check shape, dtypes, and unique counts; flag columns failing expectations"
2. Step 2 — Avoid correlation traps in stakeholder analyses: start with "Ask what could drive both variables; list top three confounders"
3. Step 3 — Write metric definitions as contracts: start with "Create a metric catalog entry per KPI: formula, grain, filters, owner"
4. How it fits together: Health check before insight. One canonical metric definition prevents the follow-up war.

### Referenced Skills

- `exploratory-analysis-dataset-health-check`
- `exploratory-analysis-correlation-causation`
- `experimentation-metric-definition-contracts`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill exploratory-analysis-dataset-health-check && npx skills add aniruddhaadak80/skills --skill exploratory-analysis-correlation-causation && npx skills add aniruddhaadak80/skills --skill experimentation-metric-definition-contracts
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills