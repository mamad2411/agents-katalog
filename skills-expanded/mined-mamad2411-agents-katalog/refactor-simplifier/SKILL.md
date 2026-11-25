---
name: refactor-simplifier
description: "Simplify after it works: remove clever code, duplication, dead abstraction. Use when reducing complexity in working code without changing behavior."
---

# Refactor Simplifier

## Overview

After code works and is tested, simplify. Remove cleverness, eliminate duplication, flatten abstractions. The best code is the code that isn't there.

**Core principle:** CLEVER CODE IS BUGS IN DISGUISE. THE SIMPLEST SOLUTION IS THE MOST MAINTAINABLE.

## The Iron Law

```
IF YOU NEED A COMMENT TO EXPLAIN WHAT IT DOES, THE CODE IS TOO COMPLEX
```

Rewrite it so the code speaks for itself.

## When to Use

**Use this when:**
- A feature is working and tests are passing, and you want to reduce future maintenance cost
- A code review surfaces readability concerns (deep nesting, cryptic variable names, duplicated logic)
- A module is being revisited for a new feature and the existing code is visibly complex

**Use this ESPECIALLY when:**
- A new team member cannot understand a function without a walkthrough
- The same logic appears in three or more places in the codebase
- A function takes a boolean parameter that changes its behavior entirely

**Don't skip when:**
- "We just need to ship" — complexity accumulates and becomes unmovable technical debt
- "It's working, don't touch it" — working code that nobody understands will break and nobody will be able to fix it
- "The original author knows what it means" — code is read far more often than it is written, by people who weren't the original author

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for all naming, and respect the decisions recorded in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## The 10 Simplifications

| # | Rule | Fix |
|---|------|-----|
| 1 | Nested ternaries > 1 level | Guard clauses or if/else |
| 2 | Short variable names (x, tmp) | Descriptive names |
| 3 | Method chaining > 3 calls | Intermediate variables |
| 4 | Dead code / commented code | Delete it |
| 5 | Duplication (3+ occurrences) | Extract function |
| 6 | Single-implementation interface | Remove abstraction |
| 7 | Deep nesting (> 3 levels) | Early returns |
| 8 | Magic numbers/strings | Named constants |
| 9 | Unnecessary variables | Inline |
| 10 | Boolean parameters | Options object |

## Decision Tree

Use this before touching any code.

```
Is the code working and all tests green?
├── NO  → Stop. Do not refactor broken code. Fix it first.
└── YES ↓

Is there a test covering the behaviour you're about to touch?
├── NO  → Write the test first. Then refactor.
└── YES ↓

Is the complexity hurting you RIGHT NOW (reading, extending, debugging)?
├── NO  → Leave it alone. Come back when you have a real reason.
└── YES ↓

Is the complex part shared / called from 3+ places?
├── YES → Extract a named function. One authoritative place.
└── NO  ↓

Is it a single-use abstraction (one interface, one impl)?
├── YES → Delete the abstraction. Inline the implementation.
└── NO  ↓

Is the logic nested > 3 levels or guarded by a boolean param?
├── YES → Apply early returns / split into two named functions.
└── NO  ↓

Is this a "clever" trick that requires a comment to explain?
├── YES → Rewrite for clarity. Delete the comment.
└── NO  → The code is fine. Stop here.

─────────────────────────────────────────────────────────────
Refactor BEFORE a feature when: you need to extend this code
  and the current shape will force you to write bad code.
Refactor AFTER a feature when: you just shipped and can see
  what settled — don't pre-optimise shape before usage is clear.
A "clever" abstraction earns its keep when: it is used in 5+
  call sites AND any change to the rule flows from one place.
Delete the abstraction when: fewer than 3 callers, OR callers
  keep passing exceptions / flags to work around it.
```

## Worked Example

A full before → after walkthrough (three atomic steps, tests green after each) lives in [REFERENCE.md](REFERENCE.md). Summary:

- **Before:** `processUserData(data, true)` — boolean flag, nested ternaries, inline validation repeated three times, one "strategy" interface with a single implementation.
- **Step 1:** Replace boolean flag with two explicit functions. Tests green.
- **Step 2:** Extract duplicated validation into `validateEmail`. Tests green.
- **Step 3:** Delete the single-impl interface; inline the one concrete class. Tests green.
- **After:** Four small, named functions. Zero comments needed. Cyclomatic complexity halved.

## Red Flags — STOP

**Refactor anti-patterns that feel like progress but aren't:**

- **Refactoring without tests.** If there is no test covering the code you are about to change, you do not know whether you have preserved behavior. Write the test first.
- **Changing behavior while "cleaning up."** A refactor MUST leave observable behavior identical. If you are also fixing a bug or adding handling, commit that separately — do not bundle it with structural cleanup.
- **Premature DRY.** Two things that look alike but serve different domains will diverge. Extracting them into a shared abstraction now forces you to add parameters later to handle the divergence. Wait for the third repetition, and confirm the repetitions are actually identical in intent, not just shape.
- **Gold-plating.** Adding a plugin system, a registry, a factory, or a strategy pattern because "we might need it" is new complexity disguised as cleanup. Remove abstractions; do not add them.
- **Big-bang rewrite.** Rewriting a function or module in one commit makes review impossible and is indistinguishable from a behavior change. Refactor in the smallest step that leaves tests green, then commit.

Clever code is not impressive — it's a future bug. "We might need this later" is YAGNI. Delete it. "I'll refactor next PR" = never. Refactor now.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's clever, it works" | Clever code works until it doesn't, then no one can fix it. |
| "We might need this abstraction" | Add it when you actually need it. Not before. |
| "Duplication is only in two places" | Two is the beginning of three. Extract now. |
| "I'll refactor it in the next PR" | You won't. Next PR adds more code on top. |
| "I'm just cleaning up, tests aren't needed" | Tests are the only proof behavior is preserved. |
| "This DRY extraction will save us later" | Premature DRY creates coupling between things that will diverge. |
| "A full rewrite is simpler than small steps" | Big-bang rewrites cannot be reviewed or rolled back safely. |
| "The abstraction adds flexibility" | Flexibility not yet needed is complexity you carry today. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "I can't follow what this function does" — variable names are opaque or logic is too nested; simplify before continuing
- "Why are there three versions of this helper?" — duplication was not extracted; consolidate into a single function
- "This used to be simpler" — the refactor introduced new abstractions that weren't needed; revert the over-engineering
- "Can you add a comment explaining this?" — if a comment is needed, the code is too clever; rewrite it to be self-explanatory
- "What does `true` mean here?" — a boolean parameter is being used; replace with an options object or two explicit functions
- "Did this change break something?" — you changed behavior during a refactor; separate the fix from the cleanup

**When you see these:** STOP. Apply the relevant simplification from the 10 rules before adding any new code.

## Verification

- [ ] No nested ternaries deeper than one level remain
- [ ] Every variable name describes what it holds (no `x`, `tmp`, `data`, `val`)
- [ ] No method chain longer than three calls without an intermediate variable
- [ ] All dead code and commented-out blocks deleted
- [ ] Logic duplicated in three or more places extracted into a named function
- [ ] No interface or abstract class with only one concrete implementation
- [ ] No function with nesting deeper than three levels (early returns applied)
- [ ] No magic numbers or magic strings — all replaced with named constants
- [ ] No boolean function parameters — replaced with options object or separate functions
- [ ] Each step of the refactor was committed separately with tests green at each commit
- [ ] No behavior change bundled into a structural cleanup commit
- [ ] All simplifications verified against existing tests — no tests broken

## Related Skills

- **code-reviewer** — use before refactor-simplifier to identify which areas have the highest complexity burden
- **test-engineer** — run tests after each simplification step to confirm behavior is preserved
- **spec-first-development** — if simplification reveals ambiguous behavior, return to spec to clarify intent before rewriting
- **task-breaker** — use to split a large refactor across multiple atomic commits so each step is independently reviewable
