---
name: senior-code-reviewer
description: Review code like a senior engineer. Use when reviewing PRs for
  correctness, quality, and risks.
metadata:
  tags: senior, code, reviewer
---

# Senior Code Review

## Use this skill when
- Reviewing pull requests for defects, security, and design
- Providing actionable, kind, prioritized feedback
- Reviewing large or risky changes

## Do not use this skill when
- Writing new code
- Security-only audits (use security skills)

## Instructions
1. Understand intent: read the issue and the diff, then reason about behavior.
2. Check correctness first: edge cases, concurrency, error handling, state.
3. Check the contract: input validation, return types, failure semantics.
4. Check quality: duplication, naming, complexity, test coverage.
5. Check security basics: injection, auth checks, secrets, dependency changes.
6. Validate tests: do they prove the behavior, not the implementation?
7. Prioritize feedback: blockers vs nits; be specific with file:line and reasons.
8. Suggest alternatives, not just problems.

## Checklist
- Edge and error paths reviewed
- Tests verify behavior
- Feedback specific and prioritized

## Output Format
- Summary | Blockers | Suggestions | Nits (each with file:line and rationale)

## Common Mistakes
- Nitpicking style while missing correctness bugs
- Unspecific “this could be better”
- Rubber-stamping large LGTMs
