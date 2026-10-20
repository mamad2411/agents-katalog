---
name: python-pre-mortem
description: Imagine future bug post-mortems for the codebase. Identifies fragile code, implicit assumptions, and likely failure modes by writing realistic incident reports for bugs that haven't happened yet.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: honnibal
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F52E"
    homepage: https://github.com/honnibal/claude-skills
---

# Pre-Mortem: Future Bug Post-Mortems

Read production code, identify areas of fragility and implicit assumptions, then write realistic post-mortem reports for bugs that **haven't happened yet** — but plausibly could.

This is not a bug hunt. The code may be perfectly correct today. You're looking for places where the code is **fragile against future edits**.

## Scope

- If the user names specific files or directories, scope analysis to those.
- Focus on production code with meaningful logic.

## Fragility Catalogue

### 1. Implicit ordering dependencies
Code that must run in a specific order but doesn't enforce it.

### 2. Semantic coupling through shared mutable state
Components communicating through shared objects rather than explicit arguments.

### 3. Stringly-typed contracts
Logic depending on exact string values — dict keys, status fields, format strings.

### 4. Assumptions baked into data transformations
Functions assuming a particular shape or range that nothing enforces.

### 5. Coincidental correctness
Code producing the right result for the wrong reason.

### 6. Non-atomic compound operations
Sequence of operations that should be atomic but aren't.

### 7. Invisible invariants
Relationships between data enforced only by convention.

### 8. Load-bearing defaults
Defaults the code subtly depends on for correct behaviour.

### 9. Implicit resource lifecycle
Resources whose cleanup depends on a particular control flow.

### 10. Version-coupled assumptions
Code depending on specific behaviour of a dependency version.

## Post-Mortem Format

```markdown
### <Short incident title>

**Severity:** Critical | High | Medium | Low
**Component:** <file(s) and function(s) involved>
**Fragility type:** <category from catalogue>

#### What happened
<2-4 sentences describing the bug as if it already occurred.>

#### The change that caused it
<Describe the edit a future developer made. Make it sound reasonable.>

#### Why it broke
<Explain the hidden assumption or fragility that the change violated.>

#### How it was caught
<Would tests catch it? Would it fail silently?>

#### Hardening suggestions
<1-3 concrete, actionable suggestions.>
```

## Critical Rules

- Be specific. Every post-mortem must reference actual functions, variables, and file paths.
- Be plausible. Imagine changes a reasonable developer would make.
- Don't fix the code. Your job is the report.
- Quality over quantity. 3-7 post-mortems per module.

## Cross-References

- `python-try-except` — error handling audit
- `python-mutation-testing` — test suite strength
