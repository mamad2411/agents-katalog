---
name: code-simplify
description: Review changed code for reuse, simplification, efficiency, and altitude cleanups, then apply fixes.
---

# Code Simplify — 4-Angle Cleanup

Extracted from Claude Code's bundled `simplify` skill.

You are improving the quality of changed code, not hunting for bugs. Review for reuse, simplification, efficiency, and altitude issues, then fix what you find.

## Phase 0 — Gather the diff

Run `git diff @{upstream}...HEAD` to get the unified diff. If uncommitted changes exist, also run `git diff HEAD`.

## Phase 1 — Review (4 cleanup angles)

### Reuse

Flag new code that re-implements something the codebase already has. Grep shared/utility modules and name the existing helper to call instead.

### Simplification

Flag unnecessary complexity: redundant or derivable state, copy-paste with slight variation, deep nesting, dead code left behind. Name the simpler form.

### Efficiency

Flag wasted work: redundant computation or repeated I/O, independent operations run sequentially, blocking work on startup or hot paths. Name the cheaper alternative.

### Altitude

Check that each change is implemented at the right depth, not as a fragile bandaid. Special cases layered on shared infrastructure = fix isn't deep enough. Prefer generalizing the underlying mechanism.

## Phase 2 — Apply fixes

Fix each finding directly. Skip any fix that would change intended behavior, require changes outside the reviewed diff, or is a false positive. Finish with a summary of what was fixed and what was skipped.
