---
name: deslop
# prettier-ignore
description: "Clean AI-generated code noise. Use when reviewing diffs, removing unnecessary comments, tightening verbose code, or desloping recent changes."
metadata:
  last_updated: "2026-05-15"
  verified_against: "current local skill refresh"
---

# Deslop

Remove AI-generated verbosity and low-value code noise from recent changes.

## Scope

Default to the smallest relevant diff:

```bash
git diff --cached --name-only
git diff HEAD~1 --name-only
```

If scope is unclear, ask whether to review staged changes, the last commit, or specific files. Skip markdown/docs unless the user asks.

## Fast Workflow

1. **Scan the diff** for patterns from [slop-patterns.md](references/slop-patterns.md).
2. **Auto-remove obvious noise** when it is mechanically safe: redundant comments, filler summaries, dead wrappers, duplicate branches.
3. **Ask before risky edits**: behavior changes, public API changes, validation removal, or unclear comments.
4. **Verify** with a targeted test/typecheck/lint when code changed.
5. **Report briefly**: files touched, noise removed, risky items left alone.

## What to Remove

- Comments that restate code
- Filler docstrings and section banners
- Over-explained temporary variables
- Defensive branches that cannot occur
- Boilerplate summaries added by generated code

## What to Keep

- Comments explaining non-obvious business logic
- Legal/license comments
- Public API documentation
- Compatibility notes
- Safety checks with real failure modes

## References

- [slop-patterns.md](references/slop-patterns.md) - AI slop detection patterns
- [review-workflow.md](references/review-workflow.md) - Interactive review for risky removals
