---
paths:
  - "app/**/*.php"
  - "resources/js/**/*.vue"
  - "resources/js/**/*.ts"
  - "resources/js/**/*.tsx"
  - "tests/**/*.php"
  - "e2e/**/*.ts"
---

# Use `software-engineer` Skill for All Code Changes

## ⚠️ STOP - Before Making Changes

**You MUST use the `software-engineer` skill before writing or modifying any code.**

```
Skill tool with skill: "software-engineer"
```

## Why?

The `software-engineer` skill includes:
- Automatic code review by specialized reviewers
- Convention compliance checking
- Architecture validation
- Up to 3 review iterations to catch issues

Direct code changes bypass these safeguards and often introduce convention violations.

## What Triggers This Rule?

Any task involving:
- Creating new files (classes, components, tests)
- Modifying existing code
- Fixing bugs
- Refactoring
- Adding features

## Exceptions

You may work directly (without the skill) for:
- Reading/exploring code (investigation only)
- Configuration file changes (`.env`, `config/*.php`)
- Documentation updates (markdown files)
- Simple one-line fixes explicitly requested by user

## How to Use

Instead of writing code directly, invoke the skill:

```
User: "Add a logout button to the header"

✅ CORRECT:
→ Use Skill tool with skill: "software-engineer"
→ Let the skill orchestrate implementation and review

❌ WRONG:
→ Directly edit Header.vue
→ Skip review cycle
```

