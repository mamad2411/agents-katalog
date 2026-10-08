---
name: receiving-review
description: Use when receiving code review feedback. Requires technical rigor and verification, not performative agreement or blind implementation.
when-to-use:
  - Reviewer leaves comments on a PR or diff
  - User provides feedback on your implementation
  - CI/linter flags issues in your changes
when-not-to-use:
  - You are the one performing the review (use the review module)
  - Feedback is purely about preferences with no technical basis
---

# Receiving Code Review

## When to use

When someone provides feedback on your code. The goal is to improve
the code, not to agree performatively.

## Procedure

1. **Read all comments first.** Understand the full picture before
   responding to any individual point.
2. **Classify each comment.**
   - Correctness issue → must fix.
   - Style/convention → follow the project's existing convention.
   - Suggestion → evaluate on merit; it's OK to disagree with evidence.
   - Question → answer clearly with code references.
3. **Verify before implementing.** If a suggestion seems wrong, test
   it before saying so. "I tried X and it causes Y" is better than
   "I don't think that's right."
4. **Fix in minimal scope.** Address the review point without
   introducing unrelated changes.
5. **Re-verify.** After all fixes, run the full test suite. Use the
   verification-before-completion skill.

## Anti-patterns

- Blindly implementing every suggestion without understanding why.
- Agreeing with feedback you haven't verified ("good catch, fixed!").
- Making defensive arguments without evidence.
- Bundling unrelated improvements into the review-fix commit.
