---
name: prompt-engineering-structured-output
description: "Get machine-parseable JSON reliably using schema-first prompting, constrained decoding, and repair loops."
---
# Guarantee structured outputs from LLMs

> Get machine-parseable JSON reliably using schema-first prompting, constrained decoding, and repair loops.

**Track:** 🤖 AI Engineering · **Domain:** Prompt Engineering · **Level:** intermediate · **~35 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Get machine-parseable JSON reliably using schema-first prompting, constrained decoding, and repair loops.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Provide the JSON Schema in the prompt and ask for schema-valid output only
2. Prefer provider-native structured-output or function-calling modes when available
3. Set temperature low for extraction; reserve high temperature for ideation tasks
4. Validate with a strict parser; reject unknown keys and wrong types
5. On failure, re-ask once including the validation error verbatim
6. Quarantine repeated failures to a dead-letter store for rubric fixes

## Common Pitfalls

- Parsing with regex instead of a real schema validator
- Accepting markdown-fenced JSON silently breaking downstream parsers

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill prompt-engineering-structured-output
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill prompt-engineering-structured-output -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills