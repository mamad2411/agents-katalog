---
name: review
version: 1.0.0
description: |
  Pre-landing PR review. Analyzes diff against main for type safety issues,
  security boundaries, silent failures, and structural problems that tests
  don't catch. Two-pass: CRITICAL (blocking) vs INFORMATIONAL.
  Adapted from gstack for TypeScript/Next.js/Supabase.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# Pre-Landing PR Review

You are running the `/review` workflow. Analyze the current branch's diff against main for structural issues that tests don't catch.

---

## Step 1: Check branch

1. Run `git branch --show-current` to get the current branch.
2. If on `main`, output: **"Nothing to review -- you're on main or have no changes against main."** and stop.
3. Run `git fetch origin main --quiet && git diff origin/main --stat` to check if there's a diff. If no diff, output the same message and stop.

---

## Step 2: Get the diff

Fetch the latest main to avoid false positives:

```bash
git fetch origin main --quiet
```

Run `git diff origin/main` to get the full diff. This includes both committed and uncommitted changes.

---

## Step 3: Two-pass review

Apply the checklist against the diff in two passes:

1. **Pass 1 (CRITICAL):** Type Safety, Auth & Data Safety, Security Boundaries
2. **Pass 2 (INFORMATIONAL):** Silent Failures, Dead Code, Test Gaps, Performance, UI/UX

Follow the output format. Respect the suppressions.

---

## Step 4: Output findings

**Always output ALL findings** -- both critical and informational.

- If CRITICAL issues found: output all findings, then for EACH critical issue use a separate AskUserQuestion with the problem, your recommended fix, and options (A: Fix it now, B: Acknowledge, C: False positive).
  After all critical questions are answered, if any A chosen, apply fixes. If only B/C, no action needed.
- If only non-critical: output findings. No further action needed.
- If no issues: output `Pre-Landing Review: No issues found.`

---

## Important Rules

- **Read the FULL diff before commenting.** Do not flag issues already addressed in the diff.
- **Read-only by default.** Only modify files if the user explicitly chooses "Fix it now."
- **Be terse.** One line problem, one line fix. No preamble.
- **Only flag real problems.** Skip anything that's fine.

---

## Review Checklist

### Pass 1 -- CRITICAL (blocks /ship)

#### Type Safety
- `as any` or `as unknown as X` casts that bypass type checking on user input or API responses
- Missing null checks on `.data` from Supabase queries (always check `.error` first)
- `!` non-null assertions on values that could genuinely be null at runtime
- Generic `catch (e)` without typing -- use `catch (e: unknown)` and narrow

#### Auth & Data Safety
- Supabase queries missing RLS context (using service role key when anon key + RLS would suffice)
- Direct object access without ownership check (user A accessing user B's data via ID manipulation)
- API routes missing auth middleware or session validation
- `update()` or `delete()` without `.eq('user_id', userId)` -- relies solely on RLS (verify RLS exists)
- String interpolation in raw SQL (use parameterized queries)

#### Security Boundaries
- Unsafe HTML rendering (React's dangerous innerHTML prop) on user-controlled or LLM-generated content without sanitization (use DOMPurify or similar)
- LLM-generated values (URLs, emails, names) written to DB without format validation
- API keys or secrets in client-side code (anything in `app/` without `use server`)
- Missing CORS or CSP headers on new API routes
- Dynamic code execution patterns with user-controlled strings

### Pass 2 -- INFORMATIONAL (non-blocking)

#### Silent Failures
- `catch` blocks that swallow errors (empty catch, or only `console.log`)
- Async functions without error handling (`await` without try/catch and no `.catch()`)
- Conditional side effects where one branch forgets an important action
- Supabase `.single()` without handling the "no rows" case

#### Dead Code & Consistency
- Variables assigned but never read
- Imports that are unused after refactoring
- Comments/docstrings that describe old behavior after the code changed
- Inconsistent naming (mixing camelCase and snake_case in same module)

#### Test Gaps
- New API routes without corresponding test files
- Negative-path tests that assert status but not the error message/body
- Missing edge case tests for new validation logic
- Security features (rate limiting, auth checks) without integration tests

#### Performance
- N+1 queries: Supabase `.select()` in a loop instead of batch query
- Missing indexes on columns used in `.eq()`, `.order()`, or `.filter()` queries
- Large data fetched client-side that should be server-side (RSC opportunity)
- `useEffect` with missing or overly broad dependency arrays causing re-renders
- Images without `next/image` optimization

#### UI/UX
- Missing loading states for async operations
- Missing error states (what does the user see when the API call fails?)
- Form submissions without optimistic updates or loading indicators
- Missing `aria-label` or `role` on interactive elements
- Hardcoded strings that should be in a constants file or i18n

---

## Gate Classification

```
CRITICAL (blocks /ship):          INFORMATIONAL (in PR body):
-- Type Safety                    -- Silent Failures
-- Auth & Data Safety             -- Dead Code & Consistency
-- Security Boundaries            -- Test Gaps
                                  -- Performance
                                  -- UI/UX
```

---

## Suppressions -- DO NOT flag these

- Style-only suggestions (formatting, import ordering) -- let prettier/eslint handle it
- "Add a comment explaining why" -- comments rot, code should be self-explanatory
- "This could be more generic" -- premature abstraction is worse than repetition
- Suggesting consistency-only changes that don't affect behavior
- console.log in development-only code paths
- Harmless type widening that doesn't affect runtime behavior
- ANYTHING already addressed in the diff you're reviewing
