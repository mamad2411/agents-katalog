---
name: code-review-methodology
version: 1.0.0
min_mindforge_version: 0.1.0
status: stable
triggers: code review methodology, review framework design, review checklist creation, PR review strategy, what to review guide, review comment style, LGTM criteria definition, PR sizing guideline, review feedback technique, constructive review approach, review priority matrix, review depth strategy
---

# Skill — Code Review Methodology

## When this skill activates
Any task involving establishing code review practices, creating review checklists,
defining PR standards, improving review feedback quality, or performing a structured review.

## Mandatory actions when this skill is active

### Before starting a review
1. Check PR size — if >800 lines, request the author split it.
2. Read the PR description to understand intent before reading code.
3. Identify the review depth needed (critical path = deep, config = surface).

### During review
- Review in priority order: correctness → security → performance → readability → style.
- Categorize every comment (blocking, suggestion, question, praise).
- Ask "What about X?" not "You should X."
- Limit blocking comments to actual blockers — save nitpicks for suggestions.

### After review
- Summarize overall assessment in the review summary.
- State clearly: Approve, Request Changes, or Comment.
- If Request Changes, list the specific blocking items.

## Review priority matrix

| Priority | Category | Examples |
|----------|----------|----------|
| 1 (Critical) | Correctness | Logic bugs, data loss, race conditions |
| 2 (High) | Security | Auth bypass, injection, secret exposure |
| 3 (Medium) | Performance | N+1 queries, missing indexes, memory leaks |
| 4 (Low) | Readability | Unclear names, missing comments, complex nesting |
| 5 (Minimal) | Style | Formatting, import order, bracket placement |

Focus 80% of review effort on priorities 1-3. Style issues should be handled by linters, not humans.

## PR sizing guidelines

| Size | Lines Changed | Review Time | Quality |
|------|--------------|-------------|---------|
| XS | <50 | 5 min | Excellent |
| S | 50-200 | 15 min | Good |
| M | 200-400 | 30 min | Acceptable |
| L | 400-800 | 60 min | Risky |
| XL | >800 | ??? | Split it |

Rules:
- Ideal PR: <400 lines of meaningful changes (exclude generated code, lockfiles).
- If a PR is large, split into: refactoring prep → core change → cleanup.
- One logical change per PR. "While I was here" changes go in separate PRs.

## Comment types

### Blocking (must fix before merge)
```
[blocking] This SQL query is vulnerable to injection.
Use parameterized queries: `db.query('SELECT * FROM users WHERE id = $1', [id])`
```

### Suggestion (consider, but not required)
```
[suggestion] Consider extracting this into a helper function —
it appears three times across this file and `utils.ts`.
```

### Question (help me understand)
```
[question] What happens if `user` is null here?
I don't see a null check upstream.
```

### Praise (reinforce good patterns)
```
[praise] Great use of the builder pattern here —
much cleaner than the previous imperative approach.
```

## LGTM criteria

A PR is ready to merge when ALL of these are true:
- [ ] No blocking comments remain unresolved.
- [ ] Tests exist for the change (unit + integration where appropriate).
- [ ] CI pipeline passes (lint, type check, tests, build).
- [ ] Documentation updated if public API or behavior changed.
- [ ] No TODOs added without a linked issue/ticket.
- [ ] PR title and description accurately describe the change.

## Review depth by change type

### Deep Review (read every line, trace data flow)
- Auth/security code
- Payment/billing logic
- Data migrations
- Public API changes
- Core business logic

### Standard Review (understand intent, spot issues)
- New features
- Bug fixes
- Internal refactoring
- Test additions

### Surface Review (sanity check, trust CI)
- Dependency updates (check changelog, breaking changes)
- Config changes (verify values are correct)
- Documentation updates (check accuracy)
- Generated code (verify generator config, spot-check output)

## Feedback style guide

### Do
- "What about handling the case where X is empty?"
- "Nice pattern — this is cleaner than the previous approach."
- "Could you add a comment explaining why this timeout is 30s?"
- "I think there's an edge case: [describe scenario]"

### Don't
- "You should use X instead." (prescriptive without context)
- "This is wrong." (unconstructive)
- "Why didn't you just do X?" (implies incompetence)
- "Nit: [style preference]" on every other line (use a linter)

### Principles
- Assume the author had a reason. Ask before suggesting alternatives.
- Be specific: "line 42 could throw if `data` is null" not "error handling is missing."
- Offer solutions with your criticism — show a better approach.
- Praise patterns you want to see more of (positive reinforcement works).

## Common things to check

### Correctness
- Off-by-one errors in loops and ranges.
- Null/undefined handling on external data.
- Race conditions in async code.
- Error paths — what happens when things fail?

### Security
- User input flows to SQL/HTML/shell without sanitization?
- Auth checks on every protected endpoint?
- Secrets hardcoded or logged?
- CORS/CSRF properly configured?

### Performance
- N+1 queries in loops?
- Missing database indexes for query patterns?
- Unbounded data fetches (no LIMIT)?
- Expensive operations in hot paths?

### Maintainability
- Will the next developer understand this in 3 months?
- Are there tests to catch regressions?
- Is the abstraction level consistent?
- Are error messages actionable?

## Anti-patterns to avoid
- Rubber-stamping (approving without reading — defeats the purpose).
- Nitpick storms (10 style comments on a 20-line PR — use a linter).
- Gatekeeping (blocking for subjective preferences, not objective issues).
- Drive-by reviews (leaving one comment, never returning for follow-up).
- "I would have done it differently" without identifying an actual problem.
- Reviewing only the diff, not the context (the bug might be in surrounding code).

## Self-check before task completion

Before marking a task done when this skill was active:

- [ ] Reviewed in priority order (correctness → security → performance → readability)?
- [ ] Every comment categorized (blocking/suggestion/question/praise)?
- [ ] No nitpicks marked as blocking?
- [ ] Summary provided with clear approve/request-changes verdict?
- [ ] Feedback is specific, constructive, and offers solutions?
- [ ] PR size is within guidelines (or split requested)?
