---
name: code-comments-docstrings
description: Writes docstrings and comments that explain why the code is the way it is, and removes stale or noisy ones, without changing behavior.
---

# Code comments and docstrings

Comments explain why. The code already shows what.

## Steps

1. Pick the scope (a file, a folder or the diff) and detect the project's docstring style from existing code: Google or NumPy for Python, JSDoc or TSDoc for JavaScript, rustdoc, Javadoc. Follow it; do not mix styles.
2. Read each function fully before writing about it. For public APIs, write a docstring with: a one-line summary in the imperative, parameters, return value, raised errors, and one short example when behavior is not obvious.
3. Add a comment only where the reason is not visible: a workaround and the bug it avoids, a performance choice, a unit or invariant, a surprising order of operations, a link to a spec.
4. Check every existing comment against the code. Fix it if it is wrong, delete it if it only repeats the code, keep it if it carries a reason.
5. Convert TODOs without owner or issue into either a concrete issue reference or a deletion proposal.

## Rules

- Never change executable code, formatting or imports in the same pass.
- Do not write a docstring you cannot support after reading the body. If behavior is unclear, say "unclear" in the report and skip it.
- No commented-out code; remove it, git remembers.
- Keep comments under 3 lines; longer thoughts go to docs.

## Report

Counts of docstrings added, comments rewritten and removed, plus the places where the code itself needs renaming instead of a comment.
