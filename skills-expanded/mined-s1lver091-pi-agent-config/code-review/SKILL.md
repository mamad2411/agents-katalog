---
name: code-review
description: Review code changes for bugs, security vulnerabilities, performance issues, and maintainability. Use when asked to review code, a PR, a diff, or recent changes.
---

# Code Review

## Step 1: Understand the change

Run `git diff` to see what changed. If reviewing a specific commit: `git show <hash>`.
Read the modified files in full, not just the diff. Context matters.

## Step 2: Trace the impact

For every modified function or type:
- Find its callers with `grep`
- Check if the change breaks any existing contract (signature, return type, side effects)
- Check if related tests still cover the new behavior

## Step 3: Check for issues

Go through each changed file and look for:

**Correctness**
- Logic errors, wrong conditions, off-by-one
- Missing null/undefined checks at system boundaries
- Unhandled error cases or silently swallowed exceptions
- Incorrect async handling (missing await, unhandled promise rejections)
- Race conditions in concurrent code

**Security**
- Injection: SQL, shell command, path traversal, XSS
- Hardcoded secrets, tokens, or credentials
- Missing input validation on user-controlled data
- Missing authorization checks
- Insecure deserialization or parsing

**Performance**
- N+1 queries or loops that could be batched
- Unnecessary re-renders, recomputations, or allocations
- Blocking I/O in async code
- Missing indexes for new query patterns

**Maintainability**
- Unclear naming or misleading comments
- Functions doing too many things
- Dead code or unused imports left behind
- Duplicated logic that should be shared

## Step 4: Report

Format your review as follows. Be direct. Do not pad with praise. Only mention things that matter.

**Summary**
One sentence describing what the change does.

**Critical** (must fix before merge)
- `file.ts:42` — Exact problem. Why it is a bug or security issue.

**Warnings** (should fix)
- `file.ts:100` — Problem and suggested fix.

**Suggestions** (optional)
- `file.ts:150` — Improvement with rationale. Clearly marked as optional.

**Verdict**
One of: `APPROVE` / `REQUEST CHANGES` / `NEEDS DISCUSSION` with a one-sentence reason.
