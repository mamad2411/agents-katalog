---
name: nodejs-24-code-review
description: Reviews Node.js 24 code for runtime compatibility, security, dependency hygiene, module-system correctness, test coverage, maintainability, performance, and operational risk. Use before merging Node.js 24 changes.
license: MIT
compatibility: Requires repository access and Node.js 24.x context for command examples.
---

# Node.js 24 Code Review

Use this skill to review Node.js 24 code changes.

## Workflow

Use [code-review-workflow](workflows/code-review-workflow.md) before merging a Node.js 24 change.

## Resources

Use [review-checklist](resources/review-checklist.md) for structured review coverage.

## Instructions

1. Review for Node.js 24 compatibility first.
2. Check whether the change affects:
   - runtime behavior
   - module loading
   - package metadata
   - dependency graph
   - filesystem access
   - subprocess execution
   - network behavior
   - secrets or credentials
   - tests and CI scripts
3. Prefer root-cause feedback over style-only comments.
4. Distinguish blockers from suggestions.
5. Verify that tests cover the changed behavior.
6. Watch for supply-chain risk in new dependencies.
7. Ensure TypeScript runtime stripping is not mistaken for type checking.
8. Check operational concerns:
   - logging
   - graceful shutdown
   - error handling
   - resource cleanup
   - performance under concurrency
9. Ask for explicit approval before recommending destructive commands.
10. Summarize commands run and checks not run.
