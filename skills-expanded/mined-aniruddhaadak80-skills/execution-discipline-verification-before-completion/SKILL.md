---
name: execution-discipline-verification-before-completion
description: "Fresh-command proof for every completion claim; 'it should work' is a confession."
---
# Verify before claiming done — evidence over claims

> Fresh-command proof for every completion claim; 'it should work' is a confession.

**Track:** 🔄 Agentic Methodology · **Domain:** Execution Discipline · **Level:** foundation · **~20 min**

**Who this is for:** Agent Power Users, AI-Native Engineers, Teams Shipping With Agents, Solo Builders

## When to Use This Skill

Fresh-command proof for every completion claim; 'it should work' is a confession.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Run the actual verification command fresh at claim time, not from memory
2. Paste real output into the completion report — truncated honestly if long
3. Re-test edge cases named in the original task, not just the happy path
4. Distinguish 'compiles', 'tests pass', and 'works' as three separate proofs
5. If anything remains unverified, say exactly what and why — never gloss
6. Treat any 'should' in your own status report as an unfinished task marker

## Common Pitfalls

- Agents declaring success on stale terminal output
- Confident summaries laundering unverified assumptions

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill execution-discipline-verification-before-completion
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill execution-discipline-verification-before-completion -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills