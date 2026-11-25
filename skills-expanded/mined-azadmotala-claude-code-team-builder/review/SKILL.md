---
name: review
description: Code review for TenantFlow. Checks security, correctness, and quality. Focuses on tenant isolation, Stripe webhooks, and Clerk auth.
---

# Code Review

Reviews staged/recent changes in TenantFlow for security, correctness, and quality.

## Workflow

1. **Identify what changed** — `git diff --stat` to see scope
2. **Security pass** — check for: tenant data leaks (missing tenantId filters), exposed secrets, auth bypass, IDOR, Stripe webhook signature skipping
3. **Correctness pass** — does the logic match the intent? edge cases handled? subscription tier gates enforced?
4. **Quality pass** — readability, test coverage, adherence to CLAUDE.md conventions
5. **Report** — categorize findings as: 🔴 Must fix, 🟡 Should fix, 🟢 Suggestion
6. **Summary** — overall assessment: ready to merge / needs work

## Project specifics
- High-risk areas: tenant isolation in every DB query, Stripe webhook signature verification, Clerk organization scoping, invoice state transitions
- Conventions: shadcn/ui over custom components, tenantId on all queries, no direct DB modifications outside Prisma
