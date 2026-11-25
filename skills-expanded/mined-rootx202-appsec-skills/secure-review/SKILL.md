---
name: secure-review
description: Lightweight secure-code-review checklist for a single pull request, diff, function, or file — as opposed to a full-project audit. Use when the user shares a diff/PR and asks for a review before merge, wants a quick pre-merge security pass, or asks for a secure coding checklist to follow while actively developing a feature.
---

# Secure Review — Fast Pre-Merge Security Checklist

A fast, focused security review for a single diff, PR, or file — not a full-project audit (that's `code-audit`).

## When to use this
- The user shares a diff or a single file and asks for a review
- Before merging a branch
- As a running checklist during active development

## Quick Checklist

### User Input
- [ ] Is every user input validated (type, length, format) before use?
- [ ] Is a trusted validation library used (zod, joi, pydantic, class-validator) instead of scattered manual checks?

### Queries and Commands
- [ ] Parameterized queries only — zero string concatenation in SQL/NoSQL queries
- [ ] No system command invoked with raw user input

### Output
- [ ] Any HTML rendering of user input goes through proper escaping
- [ ] API responses don't leak sensitive fields (password hashes, internal-only IDs, other users' data)

### Authorization
- [ ] Every new route/endpoint is protected by identity + authorization middleware
- [ ] No reliance on client-supplied values to determine permissions

### Secrets and Configuration
- [ ] No hardcoded keys/secrets anywhere in the diff
- [ ] New environment variables are documented in `.env.example` without real values

### Errors and Logging
- [ ] User-facing error messages are generic; technical detail goes to logs only
- [ ] No sensitive data (passwords, tokens, PII) written to logs

### Dependencies (if the diff adds any)
- [ ] New dependency is from a reputable source, actively maintained, and doesn't introduce a known CVE (spot-check via `dependency-security` if unsure)

## Output Style
For every unmet item, show:
```
⚠️ [Issue title]
File: path:line
Why it's a problem: [one line]
Suggested fix: [one line or short snippet]
```

Always close with a summary: items met / total, and a clear verdict — **Approve**, or **Request changes** — with a one-line justification.

## Rules
- Stay fast and focused; don't turn this into a full-project audit unless explicitly asked (then hand off to `code-audit`).
- Never evaluate code you can't actually see — if the referenced file wasn't shared, ask for it rather than assuming.
