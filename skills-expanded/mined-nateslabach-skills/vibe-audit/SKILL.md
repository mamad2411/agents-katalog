---
name: vibe-audit
description: Runs a comprehensive 20-point code quality audit on a "vibe-coded" codebase that was shipped fast and now needs hardening. Use this skill whenever the user mentions vibe coding, vibe audit, code audit, code review, code cleanup, hardening a prototype, productionizing a codebase, technical debt cleanup, or asks Claude to "audit my code", "review my codebase", "clean up my project", or check a freshly-shipped project for common quality issues. Also use when a user shares a repo and asks what's wrong with it or how to make it production-ready.
---

# Vibe Audit

A 20-point audit for codebases that were shipped fast and need hardening. Work through every check in order. For each check: search the codebase, report findings with file paths and line numbers, then apply the fix (or propose it clearly if the change is large). Do not skip checks — report "none found" rather than omitting.

## The 20 Checks

1. **Duplicate utilities.** Search for duplicate utility functions across the codebase. Consolidate all duplicates into a single shared utility file and update every import.

2. **Secrets in config.** Scan all committed config files for secrets or credentials. Flag anything that should have been an environment variable and move it.

3. **Giant functions.** Find any functions over 400 lines. Break them into smaller, single-responsibility functions with clear, descriptive names.

4. **Giant components.** Find any component over 200 lines. Split data fetching, business logic, and UI into separate layers.

5. **Dead code.** Scan for functions and variables that are defined but never called or referenced. Remove all dead code and flag anything that's unclear.

6. **Silent catches.** Find all empty or silent catch blocks. Add meaningful error logging and make sure failures are surfaced to the caller or the user.

7. **API call states.** Find every API call in the UI. Verify each one has a loading state, an error state, and prevents duplicate requests on re-render.

8. **DB in route handlers.** Check if any database queries are written directly inside route handlers. Extract all data access logic into a dedicated service or repository layer.

9. **Sync I/O in handlers.** Search for synchronous I/O operations inside request handlers. Replace with async equivalents so the event loop stays unblocked.

10. **Unbounded lists.** Check every endpoint that returns a list. Add pagination to any that fetch unbounded results.

11. **Inconsistent response shapes.** Audit all API endpoints for consistent response shapes. Standardize to one envelope structure and update every endpoint and client that doesn't match.

12. **Floats for money.** Search for any place floating point numbers are used for currency or financial values. Replace with integer arithmetic in cents and convert only at the display layer.

13. **String dates.** Find all dates stored as plain strings. Convert to ISO 8601 format or Unix timestamps and ensure timezone context is always preserved.

14. **No retry on external calls.** Find every external API call in the codebase. Add retry logic with exponential backoff to any that currently fail silently on a single error.

15. **Stale comments.** Find all code comments in the codebase. Verify each one still accurately describes the code it sits next to and delete or rewrite anything that no longer matches.

16. **Unvalidated input.** Find every place user input is accepted. Add validation and sanitization before it touches any business logic, database query, or API call.

17. **Missing auth.** Check every API route for missing authentication middleware. Add auth checks to any endpoint that should require a logged-in user.

18. **Missing indexes.** Check for missing indexes on columns used in WHERE clauses or joins. Add indexes to any high-frequency query columns.

19. **N+1 queries.** Find any place related data is fetched inside a loop. Replace with a batched query or join.

20. **Duplicated SDK init.** Search for third-party SDKs that are initialized in multiple places. Consolidate into a single shared instance.

## How to Run

Go through the checks in order. For each: state the check, show what you searched, list findings (path:line), then fix or propose the fix. At the end, give a summary table of all 20 checks with status (fixed / proposed / none found). Ask the user before making sweeping changes that touch many files.
