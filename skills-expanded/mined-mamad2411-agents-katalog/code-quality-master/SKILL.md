---
name: code-quality-master
description: Master hub for Code review, security & quality. Use to review code, audit security/performance, find bugs, and simplify code. Bundles 16 specialized skills (in skills/<name>/GUIDE.md). Use this for any code quality task.
---

# Code review, security & quality — Master Hub

Use to review code, audit security/performance, find bugs, and simplify code.

## How to use this hub

This single skill bundles **all 16 code quality skills**. Each bundled skill's full instructions live in `skills/<name>/GUIDE.md` (plus any `scripts/`, `data/`, `references/` next to it).

**Workflow:**
1. Match the user's request to one or more skills in the list below.
2. Read that skill's `skills/<name>/GUIDE.md` for full instructions before acting.
3. Combine multiple bundled skills when a task spans several areas.

## Bundled skills

- **auditing-performance** — Audit and optimize application performance, including bundle size, rendering, database queries, and Core Web Vitals.  
  → `skills/auditing-performance/GUIDE.md`
- **auditing-security** — Perform a systematic security audit of a codebase, checking for OWASP Top 10 vulnerabilities, secrets exposure, and insecure patterns.  
  → `skills/auditing-security/GUIDE.md`
- **auto-type-checking** — Run TypeScript type checking after file edits and immediately flag type errors before moving on. Uses Cursor hooks for automatic enforcement.  
  → `skills/auto-type-checking/GUIDE.md`
- **fixing-broken-links** — Crawl all links in a file or project, test each for a valid HTTP response, report broken ones, and fix or remove them.  
  → `skills/fixing-broken-links/GUIDE.md`
- **mattpocock-migrate-to-shoehorn** — Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.  
  → `skills/mattpocock-migrate-to-shoehorn/GUIDE.md`
- **parallel-code-review** — Run four parallel read-only subagents that each review the same diff from a different lens — security, performance, correctness, and readability — then merge findings into one report. Use before me...  
  → `skills/parallel-code-review/GUIDE.md`
- **reviewing-code** — Perform a thorough code review focused on correctness, maintainability, performance, and best practices.  
  → `skills/reviewing-code/GUIDE.md`
- **sentry-code-review** — Perform code reviews following Sentry engineering practices. Use when reviewing pull requests, examining code changes, or providing feedback on code quality. Covers security, performance, testing, ...  
  → `skills/sentry-code-review/GUIDE.md`
- **sentry-code-simplifier** — Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Use when asked to "simplify code", "clean up code", "refactor for clarity", "improve re...  
  → `skills/sentry-code-simplifier/GUIDE.md`
- **sentry-django-access-review** — Django access control and IDOR security review. Use when reviewing Django views, DRF viewsets, ORM queries, or any Python/Django code handling user authorization. Trigger keywords: "IDOR", "access ...  
  → `skills/sentry-django-access-review/GUIDE.md`
- **sentry-django-perf-review** — Django performance code review. Use when asked to "review Django performance", "find N+1 queries", "optimize Django", "check queryset performance", "database performance", "Django ORM issues", or a...  
  → `skills/sentry-django-perf-review/GUIDE.md`
- **sentry-find-bugs** — Find bugs, security vulnerabilities, and code quality issues in local branch changes. Use when asked to review changes, find bugs, security review, or audit code on the current branch.  
  → `skills/sentry-find-bugs/GUIDE.md`
- **sentry-gha-security-review** — GitHub Actions security review for workflow exploitation vulnerabilities. Use when asked to "review GitHub Actions", "audit workflows", "check CI security", "GHA security", "workflow security revie...  
  → `skills/sentry-gha-security-review/GUIDE.md`
- **sentry-security-review** — Security code review for vulnerabilities. Use when asked to "security review", "find vulnerabilities", "check for security issues", "audit security", "OWASP review", or review code for injection, X...  
  → `skills/sentry-security-review/GUIDE.md`
- **sentry-typing-exclusion-worker** — Python typing exclusion worker: remove assigned mypy exclusion modules in small scoped batches, fix typing issues, run validation, and produce a structured completion summary. Use when running para...  
  → `skills/sentry-typing-exclusion-worker/GUIDE.md`
- **verifying-markdown-formatting** — Verify that a Markdown file has correct formatting — headings, lists, links, code blocks, spacing, and consistent style.  
  → `skills/verifying-markdown-formatting/GUIDE.md`

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are `GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant `GUIDE.md` on demand.
