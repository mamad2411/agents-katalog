---
name: imlazy-bootstrap
description: Bootstrap skill loaded on every session — detects /imlazy and "i am lazy" triggers, routes through imlazy-router for tier-aware execution
---

# imlazy-bootstrap

## Triggers

When the user message starts with `/imlazy <task>` or `i am lazy, <task>` (at the start of a message or as a clear prefix), invoke `Skill(imlazy-router)` with the task description.

Additionally, detect VAULT triggers: "vault init", "vault save", "vault search", "create vault" — route these to `Skill(imlazy-router)` for vault-tier classification.

Do NOT trigger on "i am lazy" appearing mid-paragraph or without an actionable verb (e.g., "i am lazy and tired today" is not a trigger — no action to route).

The slash command `/imlazy` is a hard trigger. The chat phrase requires a clear actionable ask.

## The 1% rule

If a skill might apply to what you are doing, invoke it before responding. After triggering, the router decides which workflow skills to load — you do not need to pre-load anything yourself.

## Instruction priority

User instructions in CLAUDE.md / AGENTS.md take precedence over imlazy skills, which take precedence over default system behavior. The router never overrides explicit user requests — if the user says "skip the plan", honor it.

## Quick-tier completion gate

For Quick-tier tasks (classified as such by `imlazy-router`), before claiming completion:

1. Run the relevant verification command — test suite, build, or `git diff` for content-only edits.
2. Confirm exit code 0 and the intended change is present in the output.
3. If verification passes: claim completion, you are done.
4. If verification fails: do NOT claim completion. Escalate to Standard tier:
   - Invoke `Skill(imlazy-tdd)` and `Skill(imlazy-planning)` (light mode).
   - Invoke `Skill(imlazy-learn)` with predicted=quick, actual=standard, and a 50-char task summary.
   - Continue with the broader skill set loaded — do not restart the task from scratch.

## What this skill does not do

This bootstrap deliberately omits red-flags tables, rationalization lists, and workflow philosophy — those live in the tier-specific skills, loaded lazily by the router.
