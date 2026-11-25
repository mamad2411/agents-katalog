---
name: error-handling-patterns
description: Designs consistent error types and propagation, and rewrites swallowed or blindly rethrown errors so failures stay visible and messages help the user.
---

# Error handling patterns

Handle an error where you can do something about it; otherwise let it travel with context.

## Steps

1. Search for the smells: empty catch, `catch (e) { log(e) }` followed by continuing, `catch` that returns null or `false`, `throw new Error(e.message)` (drops the cause), and `except Exception: pass`.
2. Classify each failure: expected (bad input, not found, conflict), environmental (network, disk, timeout) or a bug (broken invariant). Expected ones become typed errors with a stable code. Environmental ones may be retried. Bugs should crash loudly and be logged once.
3. Define a small hierarchy or tagged result: a base error, plus a few kinds such as `ValidationError`, `NotFoundError` and `UpstreamError`. Each carries a machine code and keeps the original as `cause`.
4. Wrap at boundaries only. When crossing a module or network edge, add what you were doing ("loading invoice 42") and attach the cause. Do not wrap at every call.
5. Log once, at the place that handles the error, not at every layer it passes through.
6. At the outermost layer, map error kinds to responses: a user-safe message and a status code. Show an error id the user can quote; keep details in the logs.
7. Add a test for each expected error path.

## Rules

- Never catch just to rethrow the same error.
- Never return a default that hides a failure unless the caller documents it.
- Clean up resources in `finally`, `defer` or a context manager.
- Messages say what failed and what to do next, without internals.

## Report

Table of changes by file, with the smell found and the replacement, plus any place the right behavior needs a product decision.
