---
name: playbook-agentic-methodology-agentic-dev-loop
description: "Design gate ? executable plan ? subagent execution with TDD and two-stage reviews ? verified completion."
---
# Playbook: Run the full agentic development loop

> Design gate ? executable plan ? subagent execution with TDD and two-stage reviews ? verified completion.

**Track:** 🗺️ Agentic Methodology · **Domain:** Journey Playbooks · **Level:** journey · **~150 min**

**Who this is for:** Agent Power Users, AI-Native Engineers, Teams Shipping With Agents, Solo Builders

## When to Use This Skill

Design gate ? executable plan ? subagent execution with TDD and two-stage reviews ? verified completion.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Brainstorm with the agent before any code: start with "State the rough idea in two sentences; let the agent ask ONE question at a time"
2. Step 2 — Write plans a context-free agent could execute: start with "Split work into tasks completable in 2-5 minutes by a fresh agent"
3. Step 3 — Dispatch subagents with fresh-context discipline: start with "Extract each task's brief to its own file; the brief is the ONLY requirements source"
4. Step 4 — Enforce red-green-refactor with hard gates: start with "Write the failing test FIRST; run it and watch it fail for the right reason"
5. Step 5 — Verify before claiming done — evidence over claims: start with "Run the actual verification command fresh at claim time, not from memory"
6. How it fits together: The gates exist in order for a reason: design kills wrong ideas cheapest, plans make execution mechanical, TDD keeps agents honest, verification keeps claims honest.

### Referenced Skills

- `design-gates-socratic-brainstorming`
- `design-gates-implementation-plan-writing`
- `execution-discipline-subagent-dispatch-discipline`
- `execution-discipline-tdd-red-green-refactor`
- `execution-discipline-verification-before-completion`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill design-gates-socratic-brainstorming && npx skills add aniruddhaadak80/skills --skill design-gates-implementation-plan-writing && npx skills add aniruddhaadak80/skills --skill execution-discipline-subagent-dispatch-discipline && npx skills add aniruddhaadak80/skills --skill execution-discipline-tdd-red-green-refactor && npx skills add aniruddhaadak80/skills --skill execution-discipline-verification-before-completion
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills