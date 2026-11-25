---
name: code-review
description: Automated code review for pull requests and code changes. Auto-invoked when PR context is detected.
allowed-tools: [Read, Grep, Glob]
---

# Code Review Skill

## When to Invoke
- Pull request review context
- After code changes are staged
- When user asks for review

## Review Checklist
1. **Correctness** — Logic errors, edge cases, null handling
2. **Security** — OWASP Top 10, hardcoded secrets, injection
3. **Performance** — N+1 queries, unbounded operations, caching
4. **Conventions** — Naming, file size (<800 lines), immutability
5. **Testing** — Coverage for new code paths, test quality
6. **Architecture** — Clean layers, dependency direction, SRP

## Output Format
Report findings by severity: CRITICAL > HIGH > MEDIUM > LOW.
Include file path, line number, issue description, and suggested fix.
