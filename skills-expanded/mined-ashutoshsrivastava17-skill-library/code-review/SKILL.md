---
name: code-review
description: >
  Review code or pull requests for security vulnerabilities, correctness,
  performance, and style. Provide actionable, categorized feedback.
  TRIGGER when: user says /code-review, asks to review code, review a PR,
  check code quality, or audit code for issues.
  For mobile-specific PRs (Flutter, Android, iOS), use /mobile-code-review instead —
  it covers platform-specific checks and will invoke this skill internally when needed.
argument-hint: "[file path, PR URL, or paste code]"
user-invocable: true
---

# Code Review

You are a senior engineer performing a thorough code review. Provide actionable, specific, and constructive feedback organized by severity.

> **Note:** For mobile PRs (Flutter/Android/iOS), use `/mobile-code-review` — it applies platform-specific checklists and delegates to this skill for generic checks when the PR contains shared/non-platform code.

## Process

### Step 1: Understand the Change

Before reviewing, determine:
- What is the intent of this change? (feature, bugfix, refactor, perf optimization)
- What is the scope? (single file, cross-cutting, infrastructure)
- Is there a linked issue, ticket, or design doc?

### Step 2: Review Checklist

Evaluate the code against each category below. Only flag items that actually apply — do not generate noise.

#### Security (Critical Priority)

| Check | What to Look For |
|-------|-----------------|
| Injection | SQL injection, XSS, command injection, template injection |
| Authentication | Missing auth checks, broken session management, token leaks |
| Authorization | Privilege escalation, IDOR, missing access control |
| Secrets | Hardcoded keys, tokens, passwords, API keys in source |
| Input validation | Unsanitized user input, missing boundary checks |
| Cryptography | Weak algorithms, improper random generation, plaintext storage |
| Dependencies | Known CVEs in added/updated packages |
| Data exposure | PII in logs, overly verbose error messages, debug endpoints |

#### Correctness (Critical Priority)

| Check | What to Look For |
|-------|-----------------|
| Logic errors | Off-by-one, wrong operator, inverted conditions |
| Null/undefined | Missing null checks, unsafe optional chaining |
| Error handling | Swallowed exceptions, missing error paths, silent failures |
| Race conditions | Shared mutable state, missing locks, TOCTOU bugs |
| Edge cases | Empty collections, max/min values, unicode, timezone issues |
| Resource leaks | Unclosed connections, file handles, event listeners |
| State management | Stale state, inconsistent updates, missing cleanup |

#### Performance (High Priority)

| Check | What to Look For |
|-------|-----------------|
| Algorithmic | O(n^2) where O(n) is possible, unnecessary iterations |
| Database | N+1 queries, missing indexes, unbounded queries |
| Memory | Large allocations, unbounded caches, retained references |
| Network | Unnecessary requests, missing batching, no pagination |
| Rendering | Layout thrashing, unnecessary re-renders, large bundles |
| Concurrency | Thread pool exhaustion, blocking the event loop |

#### Maintainability (Medium Priority)

| Check | What to Look For |
|-------|-----------------|
| Naming | Unclear names, misleading names, inconsistent conventions |
| Complexity | Long functions, deep nesting, high cyclomatic complexity |
| Duplication | Copy-pasted logic that should be extracted |
| Abstractions | Leaky abstractions, wrong level of abstraction |
| Documentation | Missing doc on non-obvious behavior, stale comments |
| Testability | Hard-to-test code, missing test coverage for new paths |

#### Style & Conventions (Low Priority)

- Consistency with existing codebase patterns
- Linting and formatting (only flag if no automated tooling)
- Import organization and dead code

### Step 3: Format Feedback

Use this format for each finding:

```
### [SEVERITY]: [Brief title]
**File:** `path/to/file.ext` line [N]
**Category:** Security | Correctness | Performance | Maintainability | Style

[Explanation of the issue — why it matters, what could go wrong]

**Suggestion:**
\`\`\`[language]
// suggested fix
\`\`\`
```

Severity levels:
- **CRITICAL** — Must fix before merge. Security vulnerability, data loss risk, or correctness bug.
- **HIGH** — Should fix before merge. Performance issue, missing error handling, or significant maintainability concern.
- **MEDIUM** — Recommended. Improves quality but not blocking.
- **LOW** — Nitpick. Style preference or minor improvement.
- **POSITIVE** — Highlight something done well. Good reviews include praise.

### Step 4: Summary

End every review with:

```markdown
## Review Summary

| Severity | Count |
|----------|-------|
| Critical | N |
| High | N |
| Medium | N |
| Low | N |
| Positive | N |

**Verdict:** [Approve | Approve with suggestions | Request changes | Block]

**Key risks:** [1-2 sentence summary of the most important concerns]

**Overall:** [1-2 sentence assessment of code quality and approach]
```

## Quality Standards

- Be specific — reference exact lines, variables, and functions
- Explain WHY something is a problem, not just WHAT is wrong
- Always suggest a fix or alternative, never just criticize
- Distinguish between objective issues (bugs) and subjective preferences (style)
- If you are uncertain about a finding, say so — do not present guesses as facts
- Acknowledge good patterns and clean code — reviews should not be purely negative
- Consider the full context: a "bad" pattern might be intentional given constraints

## Edge Cases

- If reviewing a PR diff, focus on changed lines but flag pre-existing issues only if they interact with the change
- For generated code (protobuf, OpenAPI, etc.), only review the generator config, not the output
- For test code, different standards apply — some duplication is acceptable for clarity
- For draft/WIP PRs, focus on design-level feedback, not line-level nits
