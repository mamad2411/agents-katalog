---
name: review-testability
description: |
  Review code or diffs with a focus on testability, simplicity,
  managing technical debt, and sustainable design.
---

## Testability Review Skill

Review code (a diff or the entire codebase) with a focus on testability, simplicity, technical-debt management, and sustainable software development.

### Review Target

1. If there are uncommitted changes or staged diffs, review those.
2. If the user specifies files or a PR, review those.
3. Otherwise, ask the user what to review.

### Review Perspectives

Evaluate the code against the following principles:

#### 1. Testability

- Is the code easy to test? Can each unit be tested in isolation?
- Are dependencies injectable rather than hard-coded?
- Are side effects separated from pure logic?
- Would a test for this code be testing **behavior** (good) or **implementation details** (fragile)?

#### 2. Test Quality

- Do existing tests cover the meaningful behaviors?
- Are tests written at the right level of abstraction?
- Do test failure messages provide enough information to diagnose the problem? (Would power-assert style assertions help?)
- Are there tests that would break on harmless refactoring? (over-mocking, asserting on internal state, etc.)

#### 3. Simplicity & YAGNI

- Is there unnecessary abstraction, indirection, or generalization?
- Is there code written for hypothetical future requirements rather than actual current needs?
- Could the same goal be achieved with less code or fewer concepts?
- Are there premature optimizations that sacrifice readability?

#### 4. Quality and Speed

- Does the change support the principle that quality and speed reinforce each other?
- Will this code be easy to change next week? Next month?
- Are there shortcuts that will slow the team down later?

#### 5. Technical Debt

- Does the change introduce new technical debt? If so, is it intentional and documented?
- Are there opportunities to pay down existing debt nearby?
- Is the debt/shortcut ratio appropriate for the context?

#### 6. Refactoring Opportunities

- Are there structural improvements that can be made without changing behavior?
- Is there duplication that should be consolidated?
- Are names (variables, functions, classes) clear and intention-revealing?
- Is the code organized so that related things are together and unrelated things are apart?

### Output Format

```
## Testability Review

### Summary
<Overall assessment in 2-3 sentences — would this code pass a rigorous testability-focused review?>

### Findings

#### [Severity] Finding title
- **Where**: file:line
- **What**: Description of the issue
- **Why it matters**: Impact on testability, maintainability, or development speed
- **Suggestion**: Concrete improvement

...

### Positive Points
- <What the code does well from these perspectives>

### Key Takeaway
<The single most important thing to address, framed as actionable advice>
```

Severity levels:
- **Critical**: Actively harmful — will cause bugs, block testing, or create significant debt
- **Warning**: Not ideal — reduces testability, readability, or maintainability
- **Note**: Minor improvement opportunity or style suggestion

### Guidelines

- Be direct and specific. Reference actual code, not abstract principles.
- Praise good design decisions — don't only point out problems.
- Prioritize findings by impact. A few important findings are better than an exhaustive list of nitpicks.
- Frame suggestions in terms of **concrete benefit** (easier to test, safer to refactor, clearer intent), not dogma.
- Do NOT make changes. This skill only produces the review.
