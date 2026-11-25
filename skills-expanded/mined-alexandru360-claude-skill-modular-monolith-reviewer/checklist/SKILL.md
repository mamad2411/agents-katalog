---
name: checklist
description: Review modified files against a 5-section quality checklist (Architecture, Clean Code, Maintainability, Reliability, Security). Structures findings by severity. Use when asked to review, audit, or check code quality of changed files.
allowed-tools: Read, Glob, Grep, Bash, Agent
model: sonnet
version: 1.0
---

# Checklist: Analiza Fisierelor Modificate

Run a structured code quality review on modified files, organized into 5 sections and sorted by severity within each section.

## Trigger

When the user asks to run a checklist, audit modified files, or review code quality against the 5-section checklist.

## Procedure

1. Identify modified files using `git diff --name-only` (staged + unstaged) or use the files the user specifies.
2. Read each modified file and analyze against ALL criteria below.
3. Output findings grouped by the 5 sections, sorted by severity (Critical > High > Medium > Low > Info) within each section.

## Severity Levels

| Level | Meaning |
|-------|---------|
| Critical | Security vulnerability, data loss risk, crash in production |
| High | Logic error, broken contract, performance regression, missing error handling |
| Medium | Design violation, code duplication, inconsistency with codebase conventions |
| Low | Minor style issue, naming, unnecessary complexity |
| Info | Suggestion for improvement, not a defect |

## Checklist Sections

### 1. Design & Structure (Architecture)

- **SOLID**: Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
- **GRASP**: Responsibilities assigned to correct objects (Creator, Information Expert, Controller, Low Coupling, High Cohesion)
- **Design Patterns**: Appropriate patterns used for the problem domain
- **Law of Demeter**: Objects communicate only with immediate collaborators, no deep chaining

### 2. Simplicity & Clarity (Clean Code)

- **DRY**: No unnecessary logic duplication
- **KISS**: Simplest solution that solves the problem
- **YAGNI**: No code or features that aren't strictly needed now
- **Principle of Least Surprise**: Code behaves as any reader would expect
- **Be Consistent**: Style and conventions aligned with the rest of the codebase
- **Occam's Razor**: Fewest assumptions and unnecessary complexities

### 3. Maintainability & Predictability

- **Convention over Configuration**: Framework defaults respected
- **Single Source of Truth**: Data and config managed from one place
- **Boy Scout Rule**: Code is cleaner after the change than before

### 4. Reliability & Performance

- **Testability**: Easy to test in isolation (injected deps, pure functions)
- **Edge Case Coverage**: Boundary values handled (null, empty arrays, invalid inputs)
- **Error Handling**: Errors handled specifically or propagated correctly, never swallowed
- **Logging & Tracing**: Relevant logs for production debugging
- **Performance (Big O)**: Algorithms efficient for expected data volume
- **Resource Management**: Resources (DB, memory, streams, listeners) properly released

### 5. Security

- **Input Validation**: All external data sanitized and validated
- **OWASP Top 10**: Changes don't expose common vulnerabilities (injection, data exposure, broken auth)

## Output Format

```markdown
# Checklist Review: [scope description]

## 1. Design & Structure (Architecture)

### [Severity] — [File:Line] — [Criterion violated]
Description of the issue and recommendation.

## 2. Simplicity & Clarity (Clean Code)
...

## 3. Maintainability & Predictability
...

## 4. Reliability & Performance
...

## 5. Security
...

## Summary
- Critical: N
- High: N
- Medium: N
- Low: N
- Info: N
```

If a section has no findings, write: "No issues found."

## Project-Specific Rules

When reviewing files in this project, also check against:
- `CLAUDE.md` project conventions (CONNECT components, semantic tokens, data-mode theming)
- `.claude/rules/*.md` (async patterns, zustand discriminated unions, no `as` casts, no `console.log`, etc.)
- Feature boundary rules (`eslint-plugin-boundaries` — no cross-feature imports)
