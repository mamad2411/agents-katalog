---
name: playbook-ai-engineering-agent-safety
description: "Ship an autonomous agent whose failure modes are cheap, visible, and reversible."
---
# Playbook: Harden an agent before giving it tools

> Ship an autonomous agent whose failure modes are cheap, visible, and reversible.

**Track:** 🗺️ AI Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~125 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Ship an autonomous agent whose failure modes are cheap, visible, and reversible.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Design tools an agent can use reliably: start with "One tool = one verb-noun responsibility; split anything doing two jobs"
2. Step 2 — Add guardrails to autonomous agent loops: start with "Set hard max-step and max-token budgets; treat exhaustion as a normal outcome"
3. Step 3 — Defend pipelines against prompt injection: start with "Separate instruction and data channels structurally, not just by prose"
4. How it fits together: Design tools and guardrails together; retrofitting safety after autonomy is how headlines happen.

### Referenced Skills

- `agents-tool-design`
- `agents-agent-loop-guardrails`
- `inference-mlops-prompt-injection-defense`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill agents-tool-design && npx skills add aniruddhaadak80/skills --skill agents-agent-loop-guardrails && npx skills add aniruddhaadak80/skills --skill inference-mlops-prompt-injection-defense
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills