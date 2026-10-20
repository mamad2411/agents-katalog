---
name: detection-purple-detection-rule-lifecycle-sentinel
description: "Ship detection rules like code: versioned, tested, tuned, and retired deliberately."
---
# Engineer detections through a full lifecycle (Microsoft Sentinel)

> Ship detection rules like code: versioned, tested, tuned, and retired deliberately.

**Track:** 🛡️ Cyber Defense & SOC · **Domain:** Detection & Purple Team · **Level:** advanced · **~40 min**

**Who this is for:** SOC Analysts, Detection Engineers, Threat Hunters, Blue Teams

## When to Use This Skill

Ship detection rules like code: versioned, tested, tuned, and retired deliberately.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Draft rule from hunt/intel with explicit logic rationale documented
2. Backtest against 30 days of data; measure raw hit volume
3. Tune out benign-true noise using environment baselines, not blanket exclusions
4. Stage: silent-run in prod for one week comparing predicted vs actual hits
5. Enable with severity matched to expected fidelity; document false-positive budget
6. Review rule precision quarterly; retire or rewrite below threshold
7. Deploy analytics rules as code via ARM/Bicep pipelines
8. Watch ingestion latency when setting query frequency

## Common Pitfalls

- Rules enabled then never revisited until they page falsely
- Exclusions so broad they hollow out the logic

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill detection-purple-detection-rule-lifecycle-sentinel
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill detection-purple-detection-rule-lifecycle-sentinel -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills