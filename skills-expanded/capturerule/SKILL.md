---
name: captureRule
description: Turn something matt tells the agent ("we never use kebab-case", "every commit updates log.md") into a hard rule in AGENTS.md, plus the check or skill that enforces it, in the same session.
---

# captureRule

When matt says how things are done, it becomes a fact in `AGENTS.md`, not
something the next session has to rediscover.

## Hard boundaries

1. **Same session, same commit.** Add the rule in the commit that applies
   it, not later.
2. **One dated line per rule** under `## Hard rules (from matt)`, written as a
   fact ("camelCase everywhere, never kebab-case"), not a suggestion.
3. **Never delete or soften a rule** without matt saying so. If a new
   instruction contradicts an old rule, ask matt which one wins.

## The routine

1. Write the rule as one line in matt's meaning, in plain words. Number it
   and date it (`9. 2026-10-18 · ...`).
2. Make it enforceable where you can:
   - a check in `scripts/checks/checkNamingConventions.mjs` or a test, or
   - a step in the skill that covers the routine (`skills/<name>/SKILL.md`).
3. Fix everything the rule already breaks in the repo, in the same commit.
4. Put the rule in the `log.md` entry's `Why:` line.
5. If it's a new routine, add `skills/<camelCaseName>/SKILL.md` and list it in
   `skills.md`.
