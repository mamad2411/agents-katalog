---
name: check-tests
description: "Check test coverage for changes on the current branch. Args: [<file-or-module>]"
argument-hint: "[<file-or-module>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[<file-or-module>]`

- Optional. Narrows the scope to a specific file or module; default is the branch diff vs the resolved base branch (`origin/HEAD`, else `main`, else `master`).
- If the value does not resolve to an existing file or directory, the skill stops and asks rather than silently falling back to the whole branch diff.
- **Examples**: `/check-tests`, `/check-tests src/auth.ts`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Check Branch Tests

Analyze test coverage for this branch changes.

## Scope

Diff between this branch and the base branch. Resolve the base branch in this order:

1. If the user prompt names a branch explicitly, use it.
2. Else `git symbolic-ref refs/remotes/origin/HEAD` if it resolves.
3. Else `main` if it exists locally, else `master`.
4. If neither exists, stop and ask which branch to diff against.

If `$ARGUMENTS` is non-empty and resolves to an existing file or directory, narrow the scope to it. If `$ARGUMENTS` is a string that does not resolve to a real path, stop and ask; do not silently fall back to the whole branch diff.

## Task

For each changed file in the diff:
1. Identify functions/methods that were added or modified
2. Check whether adequate tests exist for those changes
3. Flag untested code paths, missing edge cases, and regression gaps
4. Check if test format is consistent with other existing tests in the project
5. **AAA adherence**: flag tests missing clear Arrange / Act / Assert separation or with multiple logical assertions crammed in
6. **FIRST compliance**: flag tests that are slow, order-dependent, non-repeatable (unmocked `time.now` / random), or rely on `print` instead of assertions
7. **Flaky-test smells**: `sleep` / `setTimeout` / timing waits, unmocked clock or randomness, shared mutable state between tests
8. **Mock placement**: flag mocks of the SUT or its internal helpers: mocks belong at boundaries (network, filesystem, clock, randomness) only
9. **Behavior vs implementation**: flag assertions on private methods / internal data structures; public-contract assertions only
10. **Near-duplicate tests**: flag pairs that differ only by input: should be parameterised
11. **Name quality**: flag vague names like `test_1`, `works`, `happy`; expect `should_<expected>_when_<condition>` or `given_<state>_when_<action>_then_<outcome>`

## Output format

For each finding, report:

- **File and line number(s)** of the changed code
- **What is untested** and why it matters (risk, edge cases, regression surface)
- **Suggested test cases**: with a code example of the missing test

Group findings by severity: **Critical** (Untested: core logic, error paths) -> **Improvement** (Partially tested: missing edge cases) -> **Quick win** (Minor gaps: trivial branches)

### Verdict

- Total changed functions: N
- Fully covered: N
- Gaps found: N
- Estimated branch coverage on scope: %
- Flakiness-risk flags: N
- Risk assessment:
  - **LOW**: >=80% estimated branch coverage AND zero flakiness flags AND no critical gaps.
  - **MEDIUM**: 50 to 79% coverage, OR any flakiness flag, OR any improvement-severity gap.
  - **HIGH**: <50% coverage, OR any critical gap (untested error path / untested core logic).

(80% is the LOW threshold because error-handling branches are the most common regression source in production code; lower coverage typically leaves an entire `catch` or fallback branch untested. If the user passes `--coverage <n>`, use `<n>` instead.)

### Audit

Before the Next Steps block, print:

`Audit: scope=<path | branch-diff>, base=<resolved-branch>, files scanned=N, functions found=F, with tests=T, gaps=G, skipped (non-code)=<list>. Subagents dispatched=0 (synchronous skill).`

If any changed file could not be parsed (binary, unsupported language), the audit must list it under `skipped (non-code)`. Do not silently drop.

### Next steps

- If gaps exist: `Run /create-unit-tests <same scope> to close the gaps.`
- Always: `Re-run /check-tests <same scope> after creating tests to verify.`

End with a **Mentoring** section: if any gap is a good learning opportunity, briefly explain the underlying principle (e.g. testing behavior vs implementation, boundary testing, arrange-act-assert). Sharing knowledge improves code health over time.

## Rules

- **DO NOT write tests. DO NOT edit any files. Report only.**
- Technical facts and data overrule opinions and personal preferences.
- Match the project existing test framework, file layout, and naming when suggesting new tests; do not propose Jest patterns in a Vitest project, etc.
- Focus on the code, not the developer.
- Suggested-test examples should be 5 to 15 lines of runnable code, not prose.
