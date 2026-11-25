---
name: sp-requesting-code-review
description: 'You MUST use this, and not the upstream superpowers requesting-code-review skill, when completing tasks, implementing major features, or before merging to verify work meets requirements. The review itself runs the scrutinize-dispatch skill.'
---

# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation — never your session's history.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## Model Selection

Use the least powerful model that can handle the review, and **always state it
explicitly in the dispatch**. An omitted model inherits your session's model —
often the most capable and most expensive — so a two-file diff gets reviewed at
architecture-tier cost, silently and with no error.

Scale it to **the reading the review requires, not the diff's line count.**
The diff is the obvious input and the misleading one. What actually drives a
review's cost is the scope *you* assign in the prompt: a single 200-line file
checked for consistency against twenty others is a twenty-file review, while a
thousand-line mechanical rename read on its own is a small one. Size the model
to the reading — and notice that the reading is something you chose.

- **Small, mechanical diff, read on its own** (one or two files, clear spec,
  no concurrency or security surface): a fast, cheap model.
- **Multi-file or judgment-heavy diff** (cross-module coordination, subtle
  state, non-obvious failure modes): a standard model.
- **Whole-branch review before merge; anything touching concurrency, security
  or data integrity; or any review whose assignment sends the reviewer across
  many files it must hold at once**: the most capable available model.

This is the same rule sp-subagent-driven-development applies to every seat it
dispatches; that skill's
[Model Selection](../sp-subagent-driven-development/SKILL.md#model-selection)
section is the fuller treatment, including fix-loop escalation and why turn
count beats token price.

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:**

Dispatch a `general-purpose` subagent, filling the template at [code-reviewer.md](code-reviewer.md)

**Placeholders:**
- `{MODEL}` - REQUIRED. The reviewer's model, per Model Selection above.
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  MODEL: a fast, cheap model - two functions, clear spec
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Spec Compliance: ✅ Spec compliant
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself instead of dispatching a reviewer" | You're the coordinator — reviewing the diff inline burns the context window you need to keep driving the work. Dispatch a reviewer subagent: the diff and the evaluation live in its context, and only the findings come back to you. |
| "I'll leave the model off and let it pick" | There is no "it" that picks. An omitted model inherits your session's, which is usually the most expensive one you have - so the cheapest review you could have run costs the most. State the model on every dispatch. |
| "The reviewer needs my whole session history to understand the change" | Hand it precisely crafted context, never your session's history. That keeps the reviewer on the work product, not your thought process. |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: [code-reviewer.md](code-reviewer.md)
