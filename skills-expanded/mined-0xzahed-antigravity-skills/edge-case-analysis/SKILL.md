---
name: edge-case-analysis
description: Identify and reason about edge cases for features and code changes.
  Use when designing or reviewing robustness.
metadata:
  tags: edge, case, analysis
---

# Edge Case Analysis

## Use this skill when
- Finding boundary values and failure modes for a feature
- Reviewing whether edge cases are handled safely
- Building a regression checklist from edge cases

## Do not use this skill when
- The feature is trivial and stateless
- You are running tests (tests should already encode these)

## Instructions
1. Enumerate input boundaries: empty, min, max, null, negative, duplicate, unicode.
2. Identify state-based edges: first use, expiry, concurrent access.
3. Check failure edges: network error, timeout, partial data, quota.
4. Verify each edge case has a defined safe behavior.
5. Record each edge case and its expected handling.

## Checklist
- Every input boundary has a defined behavior
- Concurrency and idempotency are addressed
- Errors degrade gracefully

## Output Format
- Edge case | Trigger | Expected behavior | Actual risk if missed

## Common Mistakes
- Only testing the happy path
- Assuming inputs are sanitized without verification
- Handling errors by crashing or leaking internals
