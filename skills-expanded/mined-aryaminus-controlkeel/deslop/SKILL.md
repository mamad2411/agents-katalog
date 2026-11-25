---
name: deslop
description: "Clean AI slop: remove narrative comments, verbosity, hallucinated patterns, padding. Also cleans AI-generated issue/PR text. Trigger: 'unslop', 'clean up AI code', 'remove slop', 'clean up issue description'. Complements aislop detection."
when_to_use: "Activate ONLY when explicitly asked to clean up AI-generated slop in code or issue/PR text. Do NOT auto-trigger during normal coding."
argument-hint: "[file, diff, or aislop findings to clean]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: quality
  ck_mcp_tools: [ck_validate, ck_git_diff, ck_git_commit, ck_finding]
  related_skills: [deep-code-quality-review]
---

# Deslop

Remove AI-generated slop while preserving behavior. Companion to aislop scanner — aislop detects, this skill cleans.

## Do NOT use when
- Normal coding or refactoring (use `deep-code-quality-review`)
- Security issues found (use `security-review`)
- Writing new code (not applicable)
- Reviewing issue/PR technical correctness (use `investigate` or appropriate review skill)

## Slop patterns (see [catalog](references/slop-patterns.md))

**Code patterns:**
1. Narrative comments — describing what code obviously does
2. Unnecessary verbosity — 10 lines where 3 suffice
3. Hallucinated imports — modules not used or not existing
4. Mechanical padding — single-call wrappers, unnecessary intermediates
5. Generic error messages — "An error occurred" instead of context
6. TODO stubs with no implementation
7. Redundant type annotations — already inferred

**Issue/PR text patterns:**
8. Over-confident root cause analysis without evidence
9. Generic implementation strategies without project-specific context
10. Long lists of irrelevant error classes
11. AI-generated issue expansion that broadens scope with hypotheses
12. Hallucinated code references or function names

## Subtraction rules

- **Delete, don't replace.** If a comment explains what → delete it, don't rewrite it.
- **Inline, don't redirect.** Single-call helper → inline and delete.
- **Shrink, don't reorganize.** 10-line function can be 3 → shrink, don't split.
- **Remove dead code.** Unused imports, unreachable branches.
- **Preserve intent.** Comments explaining **why** → keep. Helpers with meaningful naming → keep.

## Workflow

**For code cleanup:**
1. Run `ck_git_diff` to scope changes. Run `ck_validate` for aislop findings.
2. List slop patterns found. Plan removals — do not start editing until plan is clear.
3. Apply removals. Run tests after each logical group.
4. The diff must be **smaller** after cleanup, not just different.
5. Full suite must pass. Zero new failures.
6. `ck_validate` on cleaned diff. `ck_git_commit`.

**For issue/PR text cleanup:**
1. Identify the issue or PR description text to clean.
2. Run `ck_validate` with `source_type: "issue"` or `source_type: "pull_request"` to assess trust level.
3. List slop patterns found (over-confident analysis, generic strategies, hallucinated references).
4. Remove AI-generated expansions and stick to observed facts: command run, expected behavior, actual behavior, exact error/log.
5. Replace hallucinated code references with accurate ones after verification.
6. Remove generic implementation advice; keep only specific, actionable guidance.
7. Validate the cleaned text preserves the core issue report without the AI-generated noise.

## Rules

**For code:**
- Behavior preservation — every passing test stays passing
- No scope creep — fix slop only, do not refactor or add features
- Smaller diff — fewer lines after cleanup, not same or more

**For issue/PR text:**
- Fact preservation — keep the actual observed behavior and errors
- No scope narrowing — don't remove important context or edge cases
- Evidence-based — replace confident analysis with observed facts
- Specific over generic — keep concrete details, remove vague suggestions

## Output

**For code:**
- Cleaned code with slop removed
- Full suite passing
- Commit with cleanup

**For issue/PR text:**
- Cleaned description with AI-generated noise removed
- Preserved core issue report with observed facts
- Specific, actionable guidance without over-confident analysis
