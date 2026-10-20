---
name: senior-development
description: Senior fullstack engineering standards — SOLID, DRY, KISS, YAGNI, clean and highly maintainable code, security-first, no deprecated APIs, and docs-first (exhaust built-in/framework and existing-dependency capabilities before building from scratch). Use when implementing features, modules, APIs, UI, or database schemas. Covers cross-platform UI/UX and database design via references. Primary skill of the fullstack-developer.
---

# Senior Development

Run `project-adaptation` first; the project's `CLAUDE.md` and conventions outrank these defaults on conflict.

## Engineering standards
- **SOLID** for module/feature design; **DRY** (extract, don't duplicate); **KISS** (simplest thing that works); **YAGNI** (build only what's needed now).
- **Clean & maintainable:** small focused units, clear names, match the surrounding style and comment density. (Test authoring belongs to QA — see `qa-testing`.)
- **No deprecated code:** never use deprecated/sunset APIs, libraries, or patterns; prefer current, supported equivalents; flag deprecations you encounter.
- **Security-first:** validate/sanitize all input, parameterized queries, authn/authz on every entry point, no secrets in code, safe defaults. (QA hardens this further — see `qa-testing`.)

## Error handling & resilience
- Handle errors explicitly — **never swallow them.** Fail loudly with clear, actionable messages; log with context; clean up resources (close connections, release locks) in `finally`/`defer`.
- **Transactions:** wrap multi-step writes that must all succeed or all fail in a database transaction — commit on success, **roll back on any error**; keep transactions short to limit lock contention.
- Validate at boundaries; distinguish *expected* errors (handle/return) from *unexpected* ones (propagate/surface); never leak internals or stack traces to users.
- **Idempotency — only where it's needed (YAGNI):** make operations that can be retried or delivered more than once safe to repeat — payments, webhooks/message consumers, deploys, `PUT`/`DELETE`, "create-if-not-exists". Use idempotency keys, upserts, or natural-key checks. Don't add it where retries/duplicates can't happen.

## Docs-first, build-last
1. Check the framework/platform's **built-in / out-of-the-box** capability first — follow its official documentation.
2. Then look to **existing dependencies** — read what's already available in `node_modules/`, `vendor/`, etc.; reuse and compose it creatively before adding anything new.
3. Build from scratch only as a **last resort**, and document why.

## Prioritize security + user experience
When trading off, these two win: code is judged by whether it's safe and whether it serves the user well.

## UI/UX
Cross-platform (web / mobile / desktop) and a uniform design system (palette, icons, tokens) — see `references/ui-ux.md`.

## Database
Schema design, normalization, indexing, and optimization — see `references/database-design.md`.
