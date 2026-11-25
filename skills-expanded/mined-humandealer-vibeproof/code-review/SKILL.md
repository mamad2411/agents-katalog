---
name: code-review
description: Use before merging a diff. A structured review pass for correctness bugs, safety issues, and needless complexity.
---

# Code Review

Review a diff the way a careful senior would — looking for what will break in
production, not just style. Be specific: cite file and line, explain the
failure, propose the fix.

## When to use

Before merging any non-trivial PR, or when the human asks to "review this",
"check my diff", or "is this safe to merge".

## What to review

Run `git diff origin/main...HEAD` (or the PR diff) and check each dimension:

### 1. Correctness
- Edge cases: empty input, null, zero, very large values, unicode.
- Off-by-one, boundary conditions, loop termination.
- Error handling: are failures caught and surfaced, or swallowed?
- Does the change actually do what the PR says?

### 2. Safety
- **Secrets:** nothing sensitive in the diff (rules/security-and-secrets.md).
- **Injection:** untrusted input concatenated into SQL / shell / HTML?
- **Trust boundaries:** is external/user data validated before use?
- **Permissions:** least privilege respected?

### 3. Side effects & data
- Does a conditional path have an unexpected write / delete / external call?
- Any irreversible operation (drop, overwrite, mass update) without a guard?
- Migration / schema change that's not backward compatible?

### 4. Simplicity & reuse
- Is there a simpler way that's just as correct?
- Duplicated logic that should be shared?
- Dead code, leftover debug prints, commented-out blocks?

### 5. Tests
- Does the change have tests? Do they cover the failure modes, not just happy
  path? Did they actually run and pass?

## Output

For each finding: **severity** (blocker / should-fix / nit), **location**
(`file:line`), **what's wrong**, **suggested fix**. End with a clear verdict:
**ready to merge** or **needs changes**.

Default to caution on anything touching auth, money, data deletion, or
external side effects.
