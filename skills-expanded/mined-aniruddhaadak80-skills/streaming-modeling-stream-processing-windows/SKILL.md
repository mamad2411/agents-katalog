---
name: streaming-modeling-stream-processing-windows
description: "Event-time vs processing-time decisions, late-data handling, and exactly-once semantics."
---
# Choose windowing and watermarks correctly

> Event-time vs processing-time decisions, late-data handling, and exactly-once semantics.

**Track:** 🛢️ Data Engineering · **Domain:** Streaming & Modeling · **Level:** advanced · **~40 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Event-time vs processing-time decisions, late-data handling, and exactly-once semantics.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Timestamp on event time extracted from payload, not arrival
2. Set watermark delay from measured lateness distribution p99, not guesswork
3. Decide allowed-lateness policy: update vs side-output for stragglers
4. Key by cardinality you can hold state for; watch idle-key eviction
5. Verify exactly-once end-to-end through failure injection tests
6. Monitor watermark lag as the primary stream health metric

## Common Pitfalls

- Processing-time windows rewriting history on replays
- Unbounded state growth from high-cardinality keys

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill streaming-modeling-stream-processing-windows
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill streaming-modeling-stream-processing-windows -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills