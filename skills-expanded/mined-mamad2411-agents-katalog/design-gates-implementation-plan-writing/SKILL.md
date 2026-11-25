---
name: design-gates-implementation-plan-writing
description: "Bite-sized tasks (2-5 min each) with exact file paths, complete specs, and per-task verification steps."
---
# Write plans a context-free agent could execute

> Bite-sized tasks (2-5 min each) with exact file paths, complete specs, and per-task verification steps.

**Track:** 🔄 Agentic Methodology · **Domain:** Design Gates · **Level:** intermediate · **~35 min**

**Who this is for:** Agent Power Users, AI-Native Engineers, Teams Shipping With Agents, Solo Builders

## When to Use This Skill

Bite-sized tasks (2-5 min each) with exact file paths, complete specs, and per-task verification steps.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Split work into tasks completable in 2-5 minutes by a fresh agent
2. Each task lists exact file paths and complete expected content — zero-context assumption
3. Attach a verification step per task: command + expected observable output
4. Order tasks so every dependency precedes its consumer; flag exceptions loudly
5. Include the 'why' once at plan top; tasks carry only the 'what'
6. Dry-run read: could an eager junior with no project context follow task #7 alone?

## Common Pitfalls

- Tasks referencing 'as discussed' knowledge agents don't have
- Verification steps like 'check it works' proving nothing

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill design-gates-implementation-plan-writing
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill design-gates-implementation-plan-writing -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills