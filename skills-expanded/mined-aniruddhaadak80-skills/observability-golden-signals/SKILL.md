---
name: observability-golden-signals
description: "Latency, traffic, errors, saturation per service with SLO thresholds that map to user pain."
---
# Instrument the four golden signals

> Latency, traffic, errors, saturation per service with SLO thresholds that map to user pain.

**Track:** ☁️ DevOps & Cloud · **Domain:** Observability · **Level:** intermediate · **~35 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Latency, traffic, errors, saturation per service with SLO thresholds that map to user pain.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Emit RED metrics per endpoint: rate, errors, duration histograms
2. Track saturation of the true bottleneck (connections, queue depth, CPU steal)
3. Define SLOs from user journeys, not server uptime vanity
4. Burn-rate alerts on fast+slow windows to catch real incidents early
5. Dashboards ordered by journey, not by org chart
6. Review signal usefulness quarterly; delete dashboards nobody opens

## Common Pitfalls

- CPU alerts while users suffer on queue lag
- Averages hiding p99 cliffs

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill observability-golden-signals
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill observability-golden-signals -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills