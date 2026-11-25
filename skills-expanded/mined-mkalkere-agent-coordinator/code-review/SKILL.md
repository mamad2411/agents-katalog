---
name: code-review
version: 1.0.0
description: Evaluate code quality, patterns, and bugs — platform-agnostic
uses:
  - analysis/deep-analysis
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - file:read
  requires_approval: false
---

# Code Review

Evaluate code quality, patterns, and bugs — independent of any platform (not tied to PRs, GitHub, or specific review tools). This is the pure craft skill for reading and assessing code.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `review_code` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

**Distinction from PR review**: The `development/pr-review` and `review/pr-review` skills handle platform-specific PR workflows (fetching diffs, posting comments via GitHub API). This skill provides the underlying code assessment methodology that those skills build upon.

## When to Use

- Evaluating code quality before or after changes
- Reviewing code that isn't in a PR (local files, snippets, designs)
- Assessing technical debt in a module or codebase
- Evaluating code for security vulnerabilities
- Checking if code follows established patterns and conventions
- Assessing maintainability and readability

## Methodology

### 1. Understand the Context

Before reviewing, establish:
- **Purpose**: What is this code supposed to do?
- **Scope**: How much code are we reviewing? (file, module, feature)
- **Constraints**: What standards, conventions, or requirements apply?
- **Changes**: If reviewing changes, what was the code before?

### 2. Security Review (Always First)

Check for vulnerabilities following OWASP guidelines:

| Category | Check |
|----------|-------|
| **Injection** | SQL injection, command injection, XSS |
| **Authentication** | Proper credential handling, session management |
| **Authorization** | Access control checks on all operations |
| **Data exposure** | Sensitive data in logs, errors, or responses |
| **Input validation** | All external input validated and sanitized |
| **Cryptography** | Proper use of crypto, no hardcoded secrets |
| **Dependencies** | Known vulnerable dependencies |

### 3. Correctness Review

Verify the code is logically correct:
- Does it handle all expected inputs?
- Are edge cases covered (null, empty, boundary values)?
- Are error conditions handled (not swallowed)?
- Are return values correct for all paths?
- Are race conditions possible (shared mutable state)?
- Are resources properly managed (opened resources are closed)?

### 4. Design Review

Evaluate the design decisions:
- **Single Responsibility**: Does each function/class do one thing?
- **Naming**: Are names clear and descriptive?
- **Abstraction level**: Is the code at a consistent level of abstraction?
- **Coupling**: Are components appropriately decoupled?
- **Cohesion**: Are related things together?
- **DRY**: Is there unnecessary duplication?
- **YAGNI**: Is there speculative complexity (features not yet needed)?

### 5. Maintainability Review

Assess long-term maintainability:
- Can a new developer understand this code?
- Are complex sections explained with comments?
- Is the code testable (dependencies injectable, side effects isolated)?
- Is error handling informative (messages help diagnose problems)?
- Are magic numbers and strings extracted to constants?

### 6. Performance Review (When Relevant)

Check for performance concerns:
- Unnecessary computation in loops
- N+1 query patterns
- Blocking operations in async code
- Unbounded collections or memory allocation
- Missing caching for expensive operations

### 7. Prioritize Findings

Categorize each finding:

| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Security vulnerability, data loss risk | Must fix immediately |
| **Major** | Bug, incorrect behavior | Must fix before deployment |
| **Minor** | Code quality, maintainability | Should fix |
| **Suggestion** | Alternative approach, nice-to-have | Consider |

## Output Format

```
## Code Review: [Target]

### Summary
- Files reviewed: [count]
- Issues found: [count by severity]
- Overall quality: [good/acceptable/needs-work/concerning]

### Critical Issues
| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|
| 1 | [location] | [description] | [how to fix] |

### Major Issues
| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|

### Minor Issues
| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|

### Positive Observations
- [good pattern observed]
- [well-handled case]

### Recommendations
1. [prioritized action item]
2. [prioritized action item]
```

## Quality Criteria

- Security review is performed first, always
- All files in scope are reviewed (not just familiar ones)
- Issues include specific locations (file and line)
- Issues include specific fix recommendations
- Severity reflects actual impact (not inflated)
- Positive patterns are acknowledged (not just problems)
- Review is constructive (explains why, not just what)
- Review is complete (covers security, correctness, design, maintainability)

## Common Mistakes

- **Skipping security review**: Every code review must include security checks. Vulnerabilities are the highest-impact issues.
- **Style-only review**: Focusing on formatting and naming while missing logic errors and security issues. Go deep, not wide.
- **No fix suggestions**: Identifying problems without suggesting solutions is half the work. Always include how to fix.
- **Severity mismatch**: Marking a formatting issue as critical or a security vulnerability as minor. Severity must reflect real impact.
- **Not reading the full context**: Reviewing a function without understanding how it's called. Read callers and callees, not just the changed code.
- **Premature optimization feedback**: Suggesting performance optimizations without evidence of a performance problem. Focus on correctness first.
- **Ignoring positive aspects**: Only listing problems creates a negative feedback loop. Acknowledge good code and smart decisions.

## Completion

A code review is complete when:
- Security checklist is completed
- Correctness is verified for all code paths
- Design quality is assessed
- Maintainability is evaluated
- All issues are categorized by severity with fix recommendations
- Positive patterns are acknowledged
- Review is documented in the output format
