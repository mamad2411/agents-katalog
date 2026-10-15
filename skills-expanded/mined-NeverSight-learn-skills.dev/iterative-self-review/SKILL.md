---
name: iterative-self-review
description: Use this skill when the user asks for iterative self-review, repeated fix-and-recheck cycles, post-review remediation, or to keep reviewing until no issues remain. Always compare current code against previous code and the repository default branch, not only latest edited hunks. For PR/diff/merge-readiness discovery, run `code-review` first and hand findings here.
license: MIT
metadata: { author: BlizzardBlast, version: '1.0.4' }
---

# Iterative Self-Review

## When to use this skill

Use this skill whenever:

- You write new code.
- You refactor existing code.
- The user asks to "review your work" or requests a self-check.
- You need the review scope to cover the full current code state against both
  the previous code and the repository default branch.

## Activation boundaries

Prefer this skill when correctness and regression risk matter more than speed.

Do use it for:

- Pre-merge or pre-commit quality passes.
- Bug-fix verification after code edits.
- Sensitive changes (data flow, auth, validation, migrations).
- Follow-up iterative remediation after `code-review` findings.

Do not over-apply it for:

- Purely informational responses with no code edits.
- Trivial non-behavioral changes (e.g., comment-only wording tweaks), unless the
  user explicitly requests a full review loop.

If a request includes PR/diff/merge-readiness analysis, do not replace
`code-review`; use this skill after first-pass findings are available.

## Goal

Rigorously review the current code by comparing it to the previous code and to
the repository default branch, identify concrete issues, and iteratively fix
them until the codebase is clean while preventing regression loops.

## Required comparison scope

On every review pass, inspect both of these comparisons before deciding whether
issues exist:

- Current code vs previous code.
- Current code vs the repository default branch.

Use both comparisons to identify impacted files, behavioral drift, and missed
regressions. Do not limit the review scope to files the agent edited in the
current turn.

## Companion usage with `code-review`

When this skill is used after `code-review` findings:

- Treat incoming P0/P1 findings as mandatory fix-first blockers.
- Fix in severity order (P0 → P1 → P2 → P3) unless the user overrides.
- Preserve traceability: map each fix to the finding it resolves.
- Do not mark completion while blocker findings remain unresolved.

## Iterative review loop (required order)

Follow these steps in exact order:

1. **Initial code review**
   - Compare the current code against the previous code.
   - Compare the current code against the repository default branch.
   - Analyze the resulting current code using both comparisons, not just the
     agent's latest edits.
   - Check for syntax errors, logic bugs, edge-case failures, performance
     issues, and prompt-requirement mismatches.
2. **Status check**
   - If **no issues** are found, output: `Code review complete. No issues found.`
     and exit the loop.
   - If **issues** are found, continue.
3. **Log issues before editing**
   - Explicitly list each issue before applying fixes.
4. **Apply fixes**
   - Update the code to resolve the logged issues.
5. **Update regression ledger**
   - Track fixed issues in a mental "Regression Ledger."
   - Explicitly verify new changes do not reintroduce previously fixed problems
     relative to both the previous code and the repository default branch.
6. **Repeat**
   - Return to step 1 and rerun both required comparisons on updated code.

## Strict constraints and anti-loop rules

- **No guessing:** Do not stop until a full pass finds zero issues.
- **Break infinite loops:** If you toggle between the same fixes more than
  3 times, stop and ask the user for intervention.
- **No regressions:** Never sacrifice an earlier fix to solve a newer one.
  Rethink the approach if fixes conflict.
- **No narrow diff reviews:** Do not review only the files or hunks the agent
  most recently edited.

## Gotchas

- Do not skip the issue log step before making fixes.
- Do not skip either required comparison: current vs previous code, and current
  vs the repository default branch.
- Do not claim completion without an explicit zero-issue final pass.
- Do not collapse multiple distinct issues into one vague bullet.
- Do not hide unresolved conflicts; surface them clearly when blocked.
- If the same issue recurs across passes, compare against the regression ledger
  before editing again.

## Required output for each pass

Use this structure during the loop:

1. `Review pass N`
2. `Comparison scope:`
   - `- Current code vs previous code`
   - `- Current code vs default branch`
3. `Issues found:`
   - `- <issue 1>`
   - `- <issue 2>`
4. `Fixes applied:`
   - `- <fix 1>`
5. `Regression check:`
   - `- Verified no reintroduction of <prior issue>`
6. `Next status:`
   - `Continue loop` or `Code review complete. No issues found.`
