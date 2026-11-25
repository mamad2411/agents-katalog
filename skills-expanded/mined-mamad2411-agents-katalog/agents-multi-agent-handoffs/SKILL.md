---
name: agents-multi-agent-handoffs
description: "Split work across specialized agents with typed handoff contracts so context survives delegation without ballooning."
---
# Structure multi-agent handoffs

> Split work across specialized agents with typed handoff contracts so context survives delegation without ballooning.

**Track:** 🤖 AI Engineering · **Domain:** AI Agents · **Level:** advanced · **~50 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Split work across specialized agents with typed handoff contracts so context survives delegation without ballooning.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Give each agent one role, its own system prompt, and a minimal toolset
2. Define handoff payloads as typed objects: goal, constraints, artifacts, done-criteria
3. Pass summaries and pointers between agents, never full transcripts
4. Keep an orchestrator that owns retries and escalation to humans
5. Log which agent produced each artifact for attribution and debugging
6. Load-test worst-case fan-out before enabling parallel subagents

## Common Pitfalls

- Agents debating in circles because ownership is ambiguous
- Context bloat from forwarding entire conversation histories

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill agents-multi-agent-handoffs
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill agents-multi-agent-handoffs -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills