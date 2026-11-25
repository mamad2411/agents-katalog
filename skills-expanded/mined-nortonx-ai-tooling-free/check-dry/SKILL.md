---
name: check-dry
description: "Detect DRY violations and recommend refactoring strategies. Args: [branch | <path>]"
argument-hint: "[branch | <path>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[branch | <path>]`

- Optional. Pass `branch` to diff against the resolved base branch; pass a file/directory path to scope; omit to scan the full codebase.
- If you pass anything else (a non-existent path, an unrecognized flag), the skill stops and asks for clarification rather than guessing.
- **Examples**: `/check-dry`, `/check-dry branch`, `/check-dry src/services`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Check DRY Violations

Analyze `$ARGUMENTS` for DRY violations that signal missing abstractions.

## Scope

Determine scope from `$ARGUMENTS`, in this order:

1. Literal `branch` -> diff between this branch and the base branch. Resolve the base branch as: `git symbolic-ref refs/remotes/origin/HEAD` if it resolves, else `main` if it exists, else `master`. If neither exists, stop and ask.
2. An existing file or directory path -> analyze that specific target only.
3. Empty -> scan the full codebase under the current working directory (excluding `node_modules`, `dist`, `build`, `.git`, and any path in `.gitignore`).
4. Anything else (a non-existent path, a flag the skill does not recognize) -> stop and ask the user to clarify rather than guess.

## Detection Criteria

Flag duplication only when it meets **all** of these:
1. Code appears 3+ times (two occurrences may be coincidental)
2. The duplicated blocks change together: shared intent, not just shared syntax
3. A single abstraction (function, component, module) can replace all occurrences without forced generality

Ignore: boilerplate required by the framework, test setup/fixtures, and config files.

## Output format

For each finding, report:

- **File and line number(s)** of every duplicate occurrence
- **What is duplicated** and why it matters (shared intent vs coincidental similarity)
- **Proposed abstraction**: name, signature, and placement, with a code example
- **Risk**: what breaks if refactored incorrectly

Group findings by severity:

- **Critical**: the duplication crosses module/package boundaries AND the same logic appears in 4+ places OR a divergence has already produced a bug (look for `git log -S <duplicated-snippet>` showing two parallel fixes). These usually want a new shared module/package.
- **Improvement**: duplicated within a single module, 3+ occurrences, no divergence yet. Refactor with a local helper.
- **Quick win**: small repeated patterns (<=5 lines each) that share intent but no behavior risk yet. Cosmetic.

End with a **Mentoring** section ONLY if at least one finding hits the rule-of-three boundary or shows a premature-abstraction risk. Skip the section entirely if findings are all mechanical duplication; do not pad.

End with an **Audit** line stating exactly what was scanned and what was returned:

`Audit: scope=<branch | path | full>, files scanned=N, findings=M (critical=A, improvement=B, quick-win=C). Excluded: <list>.`

If scope detection took the fallback (e.g., neither `main` nor `master` exists, or the user passed a non-existent path), the audit line must say so explicitly.

## Rules

- **DO NOT implement fixes. DO NOT edit any files. Report only.**
- Technical facts and data overrule opinions and personal preferences.
- Match the codebase existing module/file naming when proposing a new shared abstraction; do not introduce a new naming convention.
- Focus on the code, not the developer.
- Be concise: the proposed abstraction signature plus a 5 to 10 line code example beats a paragraph of prose.

## Next Step

After review, proceed with guided implementation or your chosen feature development workflow to implement the approved refactoring.