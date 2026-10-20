---
name: prompt-engineering-system-prompt-arch
description: "Organize identity, rules, tools, and output contracts into sections that evolve without breaking behavior."
---
# Architect a maintainable system prompt

> Organize identity, rules, tools, and output contracts into sections that evolve without breaking behavior.

**Track:** 🤖 AI Engineering · **Domain:** Prompt Engineering · **Level:** foundation · **~30 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Organize identity, rules, tools, and output contracts into sections that evolve without breaking behavior.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Section order: identity, capabilities, hard rules, task guidance, output format, examples
2. State hard rules as short imperatives; explain rationale only when it changes behavior
3. Put the output contract last and show one canonical example
4. Version the prompt like code; change one concern per revision
5. Keep a regression set of 15 prompts run after every edit
6. Delete anything that survived three revisions without effect

## Common Pitfalls

- Conflicting rules buried mid-prompt that silently override each other
- Examples contradicting the stated format

## Success Signals

- Regression pass rate 100% on releases
- Prompt length trending down

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill prompt-engineering-system-prompt-arch
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill prompt-engineering-system-prompt-arch -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills