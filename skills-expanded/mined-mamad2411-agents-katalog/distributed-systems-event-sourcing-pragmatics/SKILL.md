---
name: distributed-systems-event-sourcing-pragmatics
description: "Command/event separation, upcasting discipline, and projection rebuild strategies that survive year three."
---
# Adopt event sourcing without the graveyard mistakes

> Command/event separation, upcasting discipline, and projection rebuild strategies that survive year three.

**Track:** ⚙️ Backend Engineering · **Domain:** Distributed Systems · **Level:** advanced · **~45 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Command/event separation, upcasting discipline, and projection rebuild strategies that survive year three.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Store commands' resulting EVENTS as truth; never store mutable state alongside
2. Version events immutably; upcast old versions at read boundaries only
3. Build projections as disposable rebuilds from the stream — test rebuilds regularly
4. Snapshot aggressively enough that replays don't take hours
5. Keep event payloads primitively typed; rich behavior belongs in handlers
6. Answer 'why did state change' queries from streams — that's the payoff

## Common Pitfalls

- Events named after tables (UserUpdated) carrying no business meaning
- Schema changes editing history instead of adding versions

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill distributed-systems-event-sourcing-pragmatics
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill distributed-systems-event-sourcing-pragmatics -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills