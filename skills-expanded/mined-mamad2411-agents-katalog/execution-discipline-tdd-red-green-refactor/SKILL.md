---
name: execution-discipline-tdd-red-green-refactor
description: "Failing test first, watch it fail, minimal code, watch it pass, commit — no code born before tests."
---
# Enforce red-green-refactor with hard gates

> Failing test first, watch it fail, minimal code, watch it pass, commit — no code born before tests.

**Track:** 🔄 Agentic Methodology · **Domain:** Execution Discipline · **Level:** intermediate · **~30 min**

**Who this is for:** Agent Power Users, AI-Native Engineers, Teams Shipping With Agents, Solo Builders

## When to Use This Skill

Failing test first, watch it fail, minimal code, watch it pass, commit — no code born before tests.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Write the failing test FIRST; run it and watch it fail for the right reason
2. Forbid any production code until a test demonstrably fails
3. Write the MINIMAL code to pass; resist gold-plating between greens
4. Refactor only on green; keep the cycle under ten minutes
5. Commit at every green — granular history is your undo log
6. Delete any production code discovered written before its test

## Common Pitfalls

- Tests written after code confirming implementation details instead of behavior
- 'I'll add tests later' accumulating as invisible debt

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill execution-discipline-tdd-red-green-refactor
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill execution-discipline-tdd-red-green-refactor -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills