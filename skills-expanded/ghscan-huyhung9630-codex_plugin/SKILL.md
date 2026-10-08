---
name: omc-ai-slop-cleaner
description: OMC-style anti-slop trigger for deletion-first code cleanup with behavior locked by tests.
argument-hint: "<target files, module, or --review>"
---

# OMC AI Slop Cleaner

Use this skill when the user asks to deslop, remove AI slop, simplify noisy
generated code, or run a bounded cleanup pass on working code.

Default role: `code-simplifier`. Add `test-engineer` when behavior needs a
regression harness, and `code-reviewer` for `--review` mode. Role contracts live
in `../../agents/`.

## Goal

Preserve intended behavior while deleting needless code, reducing duplication,
and tightening boundaries. This is a cleanup workflow, not a feature workflow.

## Use When

- The user explicitly says `AI slop`, `deslop`, `anti-slop`, or similar.
- Code works but is bloated, repetitive, over-abstracted, or weakly tested.
- Recent agent work introduced wrappers, duplicate branches, stale helpers,
  dead code, broad error handling, or inconsistent patterns.
- The request is a reviewer-only anti-slop pass using `--review`.

## Do Not Use When

- The main task is new functionality or a product redesign.
- Behavior is unclear and cannot be protected by tests, examples, or a concrete
  verification plan.
- The request is only formatting, naming preference, or broad aesthetic cleanup.
- The user expects a large rewrite rather than incremental simplification.

## Cleanup Posture

- Preserve behavior unless the user explicitly asks to change it.
- Lock behavior with the narrowest practical tests before editing.
- Prefer deletion over addition.
- Prefer existing project utilities and patterns over new abstractions.
- Remove single-use indirection before adding shared helpers.
- Avoid new dependencies.
- Keep the scope bounded to requested files, changed files, or one module.
- Verify after each meaningful pass, not only at the end.
- If a cleanup becomes risky, stop and report the risk instead of forcing it.

## Workflow

1. Establish scope.
   Identify requested files, modules, changed files, and out-of-scope areas.
   Check `git status` when concurrent edits may exist.

2. Protect behavior.
   Run existing targeted tests first. If tests are missing, add a focused
   regression test or state the verification plan before editing.

3. Write a short cleanup plan.
   Name the specific smells to remove and order them from safest deletion to
   riskier consolidation.

4. Classify the slop.
   Use these categories:
   - dead code: unused exports, unreachable branches, stale flags, leftover
     debug code, obsolete comments;
   - duplication: copy-paste logic, repeated parsing, repeated validation,
     parallel helpers that should be one path;
   - needless abstraction: pass-through wrappers, speculative interfaces,
     single-use factories, layers that hide simple code;
   - boundary leaks: wrong-layer imports, hidden side effects, config scattered
     across unrelated modules;
   - weak tests: behavior not locked, broad snapshots, missing edge cases.

5. Run deletion-first passes.
   Start with dead code and obsolete comments. Then remove duplication. Then
   simplify names, errors, and control flow. Add or tighten tests only where
   they protect behavior or cover the cleanup risk.

6. Verify.
   Run the relevant test, lint, typecheck, build, or plugin validation commands
   for the touched area. If a command cannot run, say why and provide the
   closest evidence used instead.

7. Report evidence.
   List changed files, what was deleted or simplified, what behavior was locked,
   verification commands, and remaining risks.

## Review Mode

When invoked with `--review`, do not edit files first. Review the cleanup plan,
diff, and verification evidence.

Check for:

- behavior changes hidden inside cleanup;
- missing regression coverage;
- deleted code that still has reachable callers;
- abstractions that should have been deleted but remain;
- new helpers or dependencies that make the code larger;
- broad scope creep beyond the requested cleanup area.

Return a reviewer verdict and required follow-ups. Keep writer and reviewer
responsibilities separate for high-impact cleanup.

## Output

For implementation mode, report:

1. Changed files.
2. Deletions and simplifications.
3. Tests or other behavior locks.
4. Verification commands and results.
5. Remaining risks.

For review mode, lead with findings ordered by severity, then summarize the
cleanup quality and verification gaps.
