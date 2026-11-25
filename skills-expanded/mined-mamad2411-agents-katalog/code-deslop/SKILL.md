---
name: code-deslop
description: Detect or fix code that reads as AI-generated ("slop") — redundant comments, defensive overdose (try/catch or null-checks for states that can't occur), type-bypass casts, unneeded abstraction layers, deep nesting, boilerplate tests, and generic naming/style fingerprints. Use when the user asks to "review this diff for AI slop," "check for over-engineering," "does this code look AI-generated," wants a PR "cleaned up before I ship it," or asks to deslop/audit code quality. Covers code only — not prose/writing (see the separate `deslop` skill for that).
metadata:
  short-description: Detect or fix AI-sounding code slop — comment noise, defensive overdose, over-engineering — without changing behavior
---

# Code Deslop

Fix code that reads as AI-generated without rewriting more than necessary. The goal is code that looks like a person who knows this codebase wrote it under normal time pressure — not a maximally "clean" rewrite. Preserve behavior; make targeted edits.

## Quick Start

1. **Pick a scope.** Diff-scoped review (default in a git repo with a divergent branch) or whole-file/whole-repo scan (when the user hands over specific files or asks for a general audit). See Scope below.
2. **Scan** against `references/patterns.md`, organized by category.
3. **Score** with `references/scoring-rubric.md` to gauge how much is actually wrong before touching anything.
4. **Fix** using the minimal-diff guardrail from `references/modes.md` — offer ambitious-restructuring mode only if asked.
5. **Verify** behavior is preserved (run tests/build if available — don't just assert it).
6. Output in the format under Output below.

## Scope

- **Diff-scoped** — in a git repo with commits ahead of main/master, or the user says "review this PR" / "check my changes": run `git diff main...HEAD` (or the appropriate base branch) and review only the changed lines. This is the default — most AI-slop review is a pre-ship gate on new work, not an audit of a whole codebase.
- **Scan mode** — the user hands over specific files, asks for a general audit, or there's no meaningful diff (on main, or no git): review the given files/directory directly.

## Instructions

1. **Scan for tells**, checking the code against every category in `references/patterns.md`. Check the architectural fingerprint first — line-by-line uniform but architecturally inconsistent code (every comment/function formatted identically, yet each function/module solves similar problems its own way) is the single highest-confidence signal. Any one tell alone is a hunch; treat 4-5 co-occurring tells across categories as a reliable diagnosis, especially when the question is "does this look AI-written?" rather than "fix this flagged issue."
   - Comment noise — redundant, obvious, or stale comments
   - Defensive overdose — try/catch, null-checks, or validation for states that can't occur given the call site (broad `except: pass` / bare `catch {}` swallows are the most common form)
   - Type bypass — `any` casts, unchecked assertions, silenced type errors
   - Over-engineering — abstraction layers with one caller, premature config/flags, YAGNI violations, or the same concern re-solved differently across files/modules
   - Duplicate/parallel implementations — the same logic reimplemented under different names because separate generation sessions didn't reuse existing code
   - Deep nesting — conditionals that should be early-returns
   - Test slop — boilerplate/AI-generated tests, redundant mocks, assertions that don't actually test the behavior claimed
   - Naming/style fingerprints — generic tutorial-style names (`data`, `result`, `handleClick2`) or iterative-regeneration names (`data2`, `resultFinal`), uniformly "textbook" formatting that doesn't match the surrounding file's style
   - Dead code — unused exports, unreachable branches, commented-out code, unused dependencies pulled in for an abandoned approach
   - Process/workflow smells — a whole feature landing as one giant commit instead of incremental steps (note, don't "fix")

2. **Score** with `references/scoring-rubric.md`. This decides how aggressive Step 3 should be — don't rewrite code that's mostly fine because it tripped one minor pattern. A single stray comment is not the same severity as a defensive try/catch masking a real bug.

3. **Fix with the minimal-diff guardrail** (default — see `references/modes.md`). For each flagged issue: one issue, one focused fix, no drive-by rewrites of adjacent code that wasn't flagged. Before cutting anything defensive, confirm the state it's guarding against genuinely can't occur — removing a check that's actually load-bearing is worse than leaving slop in place. If the user explicitly asks for a deeper refactor ("restructure this," "make this actually good," not just "clean it up"), switch to ambitious-restructuring mode per `references/modes.md`.

4. **Verify.** If tests or a build step exist, run them after edits and report the result — don't claim behavior is preserved without checking. If nothing is runnable in this context, say so explicitly rather than asserting correctness.

## Output

**Diff-scoped review (Detect):**
```
[file:line] — [category] — [what's wrong, 1 line]
[file:line] — [category] — [what's wrong, 1 line]
...
Score: [X]/[max] (see references/scoring-rubric.md if asked for the breakdown)
```

**Fix mode (Edit):**
```
[edited files]

What changed:
- [file:line] — [fix] — [which category it addressed]
```

Don't pad either output with commentary beyond what's asked. A findings list that's itself bloated with hedging and caveats is the same failure mode this skill exists to catch.
