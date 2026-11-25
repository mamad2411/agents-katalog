---
name: debug-craft-production-debugging-java
description: "Safe live diagnosis using flags, traces, and snapshots instead of restart roulette."
---
# Debug production without stopping the world (Java/JVM)

> Safe live diagnosis using flags, traces, and snapshots instead of restart roulette.

**Track:** 🧰 Engineering Essentials · **Domain:** Debugging Craft · **Level:** advanced · **~40 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Safe live diagnosis using flags, traces, and snapshots instead of restart roulette.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Correlate user report to trace IDs through gateway → service → data layer
2. Capture state non-invasively: heap/profile snapshots over process restarts
3. Enable dynamic log levels temporarily rather than redeploying
4. Test hypotheses against staging replicas of prod data shape
5. Timebox live debugging; mitigate via rollback/flag if past window
6. Write postmortem linking timeline to evidence artifacts
7. Tune GC logs review into routine; watch allocation pressure
8. Use JFR recordings for production-safe continuous profiling

## Common Pitfalls

- Restarting away evidence mid-diagnosis
- Debugging against sanitized data missing the trigger shape

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill debug-craft-production-debugging-java
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill debug-craft-production-debugging-java -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills