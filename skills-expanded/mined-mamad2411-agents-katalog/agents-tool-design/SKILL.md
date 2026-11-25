---
name: agents-tool-design
description: "Shape tool names, parameters, descriptions, and error messages so the agent calls the right tool with valid arguments."
---
# Design tools an agent can use reliably

> Shape tool names, parameters, descriptions, and error messages so the agent calls the right tool with valid arguments.

**Track:** 🤖 AI Engineering · **Domain:** AI Agents · **Level:** intermediate · **~40 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Shape tool names, parameters, descriptions, and error messages so the agent calls the right tool with valid arguments.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. One tool = one verb-noun responsibility; split anything doing two jobs
2. Write parameter descriptions that state format and units explicitly
3. Return structured errors the agent can self-correct from, never stack traces
4. Make tools idempotent where possible; require confirmation flags for destructive ones
5. Cap list results and paginate instead of dumping unbounded payloads
6. Test with adversarial phrasings that should NOT trigger the tool

## Common Pitfalls

- Overlapping tools forcing the model to guess between near-duplicates
- Boolean success returns hiding why a call failed

## Success Signals

- Tool-call validity rate above 95%
- Zero destructive calls without confirmation

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill agents-tool-design
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill agents-tool-design -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills