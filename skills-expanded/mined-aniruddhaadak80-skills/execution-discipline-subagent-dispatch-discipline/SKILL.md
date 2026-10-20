---
name: execution-discipline-subagent-dispatch-discipline
description: "Fresh implementer per task, brief files as single source of truth, two-stage review, capped fix loops."
---
# Dispatch subagents with fresh-context discipline

> Fresh implementer per task, brief files as single source of truth, two-stage review, capped fix loops.

**Track:** 🔄 Agentic Methodology · **Domain:** Execution Discipline · **Level:** advanced · **~40 min**

**Who this is for:** Agent Power Users, AI-Native Engineers, Teams Shipping With Agents, Solo Builders

## When to Use This Skill

Fresh implementer per task, brief files as single source of truth, two-stage review, capped fix loops.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Extract each task's brief to its own file; the brief is the ONLY requirements source
2. Dispatch a FRESH subagent per task — context pollution breeds confident errors
3. Require two-stage review per task: spec compliance first, then code quality
4. Cap fix loops at three resumes; beyond that, fresh agent + more capable model
5. Batch trivially-same-shaped small edits into ONE dispatch, reviewed as one diff
6. Keep a findings ledger: parked minors get adjudicated, never silently dropped

## Common Pitfalls

- Session-model inheritance silently spending premium tokens on mechanical tasks
- Fix loops where the same blind implementer retries identical failures

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill execution-discipline-subagent-dispatch-discipline
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill execution-discipline-subagent-dispatch-discipline -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills