---
name: Operating Framework Meta-Skill
description: Process checks for applying the operating framework before actions and task transitions.
---

# Operating Framework Meta-Skill

> Process discipline enforcement layer. Always active. No exceptions.

## Triggers

This skill activates **automatically before every action**. It is not invoked manually.

## The 1% Rule

If there is even a **1% chance** that a Operating Framework skill applies to your current task, you **MUST** check and follow it. Do not rationalize skipping.

### Quick-Scan Checklist

Before every action, mentally scan this list:

| If you are about to... | Check this skill |
|------------------------|------------------|
| Write production code | `test-driven-development` |
| Fix a bug | `debug` command (root cause gate) |
| Claim something is "done" | `verification-before-completion` |
| Start coding from a brainstorm | `sc:brainstorm` (approval gate) |
| Execute a plan | `executing-plans` |
| Spawn subagents | `subagent-development` |
| Work on a feature branch | `branch-finishing`, `git-worktrees` |
| Receive review feedback | `receiving-code-review` |
| Start any implementation | `confidence-check` (pre-existing) |
| Start any meaningful task | `operating-framework` — Lane? Risk tier? Council mode? |

## Anti-Rationalization Table

These are the 8 most common excuses for skipping process. **None are valid.**

| Excuse | Reality | Rule |
|--------|---------|------|
| "It's too small for TDD" | Small changes break systems. Tests take 30 seconds. | Write the test. |
| "I'll add tests later" | You won't. Technical debt compounds. | Write the test NOW. |
| "The code is obvious" | Obvious code still has edge cases. Tests document behavior. | Write the test. |
| "I already know the root cause" | Confirmation bias. Your first guess is often wrong. | Show the evidence first. |
| "This is just a quick fix" | Quick fixes cause regressions. | Follow the full debug cycle. |
| "The user wants it fast" | The user wants it RIGHT. Rework is slower than discipline. | Follow the process. |
| "I verified it mentally" | Mental verification misses runtime behavior. | Run the actual verification. |
| "This skill doesn't really apply" | If you're debating it, the 1% rule says it applies. | Check the skill. |

## Priority Order

When instructions conflict, follow this priority:

1. **User's explicit instructions** (highest)
2. **Operating Framework hard gates** (cannot be silently skipped)
3. **Existing skills and commands**
4. **Default Claude Code behavior** (lowest)

## Hard Gates Summary

These gates **block forward progress** until their conditions are met:

| Gate | Blocks | Until |
|------|--------|-------|
| TDD Gate | Writing production code | A failing test exists for the feature |
| Root Cause Gate | Applying a fix | Root cause is stated with evidence |
| Approval Gate | Coding from brainstorm | User explicitly approves the spec |
| Verification Gate | Claiming "done" | Evidence (test output, logs) is shown |
| Branch Gate | Starting implementation | You are on a feature branch, not main |

## What This Skill Does NOT Do

- Does not replace existing skills or commands
- Does not add overhead to simple file reads or exploratory work
- Does not require gates for non-code tasks (research, explanation, documentation)
- Does not override the user's explicit `--skip-gate` instruction
