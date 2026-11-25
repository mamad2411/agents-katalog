---
name: debugging-mindset
description: Use this skill when debugging code, diagnosing unexpected behavior, troubleshooting errors, or approaching a problem systematically. Trigger on keywords: debug, bug, error, not working, unexpected behavior, troubleshoot, investigate, root cause, why is this, something is wrong, failing test, crash.
---

# Debugging Mindset

## Core Principle

**Debug the system, not your assumptions.**

Most bugs persist because developers debug what they *think* is happening instead of what's *actually* happening. Every assumption is a potential hiding place for a bug.

---

## The Scientific Debugging Method

```
1. OBSERVE     — What exactly is the symptom? (not interpretation, raw facts)
2. HYPOTHESIZE — What are the possible causes?
3. TEST        — Design the smallest possible test to confirm/deny each hypothesis
4. CONCLUDE    — What does the evidence tell you?
5. FIX         — Address the root cause, not the symptom
6. VERIFY      — Confirm the fix works and nothing else broke
7. PREVENT     — Add a test that would catch this regression
```

Never skip step 7. Every bug is a test that doesn't exist yet.

---

## Start Here: The Five Questions

Before writing a single line of debug code, answer these:

1. **What did I expect to happen?**
2. **What actually happened?** (exact error message, exact output)
3. **What changed recently?** (last commit, dependency update, config change)
4. **Can I reproduce it reliably?** (if not, it might be timing/state/environment)
5. **Is this the first time this happened?** (regression vs new bug)

Answering these five questions often reveals the bug before you even look at code.

---

## Divide and Conquer

For complex bugs in large codebases:

```
1. Identify the full path of execution involved
2. Pick the midpoint
3. Add a check there — does the data look correct?
4. If yes → bug is in second half. If no → bug is in first half.
5. Repeat until you've narrowed to a single function or line.
```

This is binary search for bugs. Cuts debugging time in half at each step.

---

## Read the Error Message (Actually Read It)

Most developers skim error messages. Read them:
- **What** failed (error type)
- **Where** it failed (file, line, function name)
- **Why** it failed (message body)
- **Stack trace** — read bottom-up to find *your* code vs framework code

For cryptic errors: paste the exact error into the AI with context, not a paraphrase.

---

## Common Bug Patterns

| Pattern | Signs | Fix |
|---|---|---|
| **Off-by-one** | Wrong count, first/last element skipped | Check loop bounds and index math |
| **Null / undefined** | "Cannot read property of undefined" | Add null guards, check API contracts |
| **Async/await** | Data appears empty, timing-sensitive | Ensure every async call is awaited |
| **Stale state** | Works sometimes, not always | Check state mutation, cache invalidation |
| **Type mismatch** | Unexpected behavior with numbers/strings | Check types explicitly, don't trust coercion |
| **Environment diff** | Works locally, fails in prod | Check env vars, dependency versions, OS differences |
| **Race condition** | Fails under load, works in isolation | Add locks, use atomic operations, review shared state |

---

## Debugging Strategies by Context

### Frontend / UI Bugs
1. Open DevTools → Console (errors), Network (failed requests), Elements (DOM state)
2. Check if the issue is data (wrong value) or rendering (correct value, wrong display)
3. Isolate: reproduce in the smallest possible component
4. Check browser compatibility if intermittent

### Backend / API Bugs
1. Check request payload first — is the input correct?
2. Check database state — is the data what you expect?
3. Trace through the service layer step by step
4. Add temporary logging at key points to see actual values

### Database / Query Bugs
1. Run the query directly against the DB (not through ORM)
2. Check actual data vs expected data
3. Watch for N+1 queries (loop with individual DB calls)
4. Check indexes for slow queries

### Intermittent Bugs
1. Add comprehensive logging — capture state at every step
2. Look for shared mutable state
3. Check for timing dependencies
4. Reproduce under load (concurrency issues)
5. Check for memory leaks or resource exhaustion

---

## The Rubber Duck Method

Explain the bug out loud (to a rubber duck, a colleague, or an AI) as if they know nothing:
1. What the code is supposed to do
2. What it's actually doing
3. Walk through the code line by line

The act of explaining forces you to examine every assumption. 60-70% of the time, you find the bug while explaining — before anyone responds.

---

## When You're Stuck

After 20-30 minutes without progress:

1. **Take a break** — 10 minutes away often produces the insight
2. **Rubber duck** — explain the problem from scratch
3. **Question your most confident assumption** — bugs often hide behind certainties
4. **Simplify** — reduce to the minimal reproduction case
5. **Revert** — if the bug is recent, git bisect or revert to last working state
6. **Ask for help** — but prepare a clear problem statement first

### Asking for Help Effectively
```
Context: [what the code is doing]
Expected: [what should happen]
Actual: [what is happening — exact error/output]
Tried: [what you've already attempted]
Suspicion: [your current best hypothesis]
```

---

## After Fixing the Bug

1. **Write a test** that would have caught this bug
2. **Document** if the root cause was non-obvious
3. **Check for similar bugs** elsewhere in the codebase
4. **Update the lessons log** if it was a new class of mistake you want to remember
5. **Commit message** should explain the root cause, not just the fix:
   ```
   fix(auth): handle null session on token refresh
   
   Previously crashed when session expired during token refresh.
   Root cause: session.user was null after expiry but code assumed 
   it was always present. Added null guard and redirect to login.
   ```
