---
name: code-test
description: Audit test suites for quality, coverage gaps, missing tests, and mutation resistance.
---

# Code Test Audit

## Interactive mode (no arguments or partial arguments)

If the user did not provide all three pieces of information (language, practice, targets), print a single prompt that lists every missing piece and ask the user to reply with their choices. For prompts with at most 3 short enumerated options, ask the user to select from options; for open-ended choice lists (languages, targets), output the choices as formatted text directly in the conversation.

For each missing piece, print a numbered section:

1. **Language** (if `$0` is missing or invalid); list all languages from the table below with their available practices.
2. **Practice** (if `$1` is missing or invalid); list every valid practice for the chosen/given language.
3. **Targets** (if no targets were provided); explain the target syntax (see below) and list files matching the chosen language in the current workspace to surface candidate source files. Suggest them as `file:` targets. If there are too many candidates, ask for a glob pattern instead.

Present everything in one message so the user can answer all at once (e.g., "go, edge-cases, file:pkg/auth/login.go file:pkg/auth/session.go"). Wait for their reply, then proceed to the audit steps below.

## Target syntax

All targets use a prefix to indicate the type of input:

| Prefix | Format | Description |
| --- | --- | --- |
| `file:` | `file:PATH` or `file:PATH#L1-L2` | Single file, optional line range |
| `folder:` | `folder:PATH` | All source files within the dir (recursive) |
| `symbol:` | `symbol:PATH:LINE` or `symbol:PATH:LINE#L1-L2` | Function/struct/class/method at LINE, optional focus range |
| `diff:` | `diff:local`, `diff:branch[:REF]`, `diff:pr:NUMBER_OR_URL`, `diff:commit:SHA` | Changes from a diff source |

Bare paths (no prefix) are shorthand for `file:PATH`.

### Resolution rules

**`file:PATH[#L1-L2]`**: Read the file. If `#L1-L2` is present, analyze only that line range but read enough surrounding context (imports, type definitions) to understand it.

**`folder:PATH`**: List files within PATH matching the language's typical extensions. Treat each discovered file as a `file:` target.

**`symbol:PATH:LINE[#L1-L2]`**: Read the file at PATH. Identify the innermost function, method, struct, class, enum, or trait definition containing LINE. Analyze that symbol boundary (from signature to closing delimiter). If `#L1-L2` is appended, focus on that range within the symbol. When invoked standalone (not by deep-review), do not chase callers/implementations outside the file. When run under deep-review, callers, callees, type definitions, and related tests will already be supplied in the `## Gathered Context` section of the prompt, so rely on those rather than re-gathering. After resolving the symbol, also locate the corresponding test file using project test conventions. The symbol gives the source region; test-file discovery gives the test region to evaluate against it.

**`diff:SOURCE`**: Resolve the diff:

| Source | Resolution |
| --- | --- |
| `diff:local` | `git diff HEAD` for tracked changes + `git ls-files --others --exclude-standard` for untracked |
| `diff:branch` | Detect default branch (`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null \| sed 's@^refs/remotes/origin/@@'`, falling back to `main`), then `git diff <default>...HEAD` |
| `diff:branch:REF` | `git diff REF...HEAD` |
| `diff:pr:N` or `diff:pr:URL` | GitHub: `gh pr diff N`, GitLab: `glab mr diff N`. Parse owner/repo/number from URL if needed |
| `diff:commit:SHA` | `git show SHA --stat` for overview, then `git show SHA` for full diff. Read the commit message for intent context |

After resolving the diff, extract changed files and changed line regions (hunks). Apply analysis to the changed code regions (reading full context around hunks). After resolving changed source files, locate corresponding test files. If changed source code lacks test coverage, report it as a finding even if no test file was found.

### Edge cases

- `symbol:` LINE on blank/comment/import to scan up/down ~20 lines for nearest symbol; error if none found.
- Nested symbols (closures, inner functions) to resolve to innermost enclosing.
- `#L1-L2` where L2 > file length to clamp to file length; L1 > file length to error.
- `folder:` with no matching files to report "No source files found."
- Empty diff to report "No changes found" and stop.

## Audit steps

- **Language:** $0
- **Practice:** $1
- **Targets:** all arguments after the second are targets to analyze (see Target syntax above).

1. Open [`lang/$0.md`](lang/$0.md) to confirm the practice is valid for this language and load language-specific testing patterns.
2. Open [`practice/$1.md`](practice/$1.md) to load the testing practice methodology and checklist.
3. Resolve all targets into concrete code regions using the target resolution rules.
4. **Locate test files**: for each target source file (or resolved source region), find the corresponding test file(s) using the project's test conventions (co-located `_test.go`, `mod_test.rs`, `*.test.ts`, `*Test.java`, `test_*.py`, etc.). Read each test file in full. If no test file exists, report it as a critical finding.
5. **Read source files**: read every target source file in full. Build a model of: all functions/methods, their parameters (types and domains), return types, branching structure, error paths, and side effects.
6. Apply the loaded practice checklist against the source-test pair.

## Rules

- Read each source and test file in full rather than sampling it.
- **Derive test expectations from the interface, not the implementation.** Examine parameter types, return types, and documented contracts. For each input, enumerate the equivalence classes and boundary values of its domain. Flag any equivalence class that has no corresponding test, even if the current code does not distinguish it; that is precisely where bugs hide.
- For each finding provide:
  - **Source file** and **line number(s)** of the untested or poorly tested code.
  - **Test file** and **line number(s)** of the relevant test (if it exists).
  - **Practice** (`branch-coverage`, `edge-cases`, `assertions`, `isolation`, `negative-testing`, `mutation-resistance`).
  - **Severity**:
    - `critical`: no tests exist, or tests are provably unable to detect faults in critical logic.
    - `high`: significant branches or failure modes are untested.
    - `medium`: edge cases or secondary paths lack coverage.
    - `low`: minor improvements to test quality or structure.
  - **Description**: what is missing or wrong and why it matters.
  - **Suggested test**: a concrete test case description (inputs, expected outcome, what bug it would catch). Describe the test; do not write full implementation code.
- When analyzing a `symbol:` target, report the symbol name and its span in the heading for that target's findings.
- When analyzing a `diff:` target, focus on changed and added code. Flag pre-existing issues in unchanged lines only if a change makes them actively dangerous.
- If you find no issues for a section, say so explicitly; do not invent problems.
- Do not modify any files. This is analysis only.
- At the end, produce a summary table of all findings grouped by severity.

## Available languages

| Language | Practices |
| --- | --- |
| `c` | branch-coverage, edge-cases, assertions, isolation, negative-testing, mutation-resistance |
| `go` | branch-coverage, edge-cases, assertions, isolation, negative-testing, mutation-resistance |
| `java` | branch-coverage, edge-cases, assertions, isolation, negative-testing, mutation-resistance |
| `python` | branch-coverage, edge-cases, assertions, isolation, negative-testing, mutation-resistance |
| `rust` | branch-coverage, edge-cases, assertions, isolation, negative-testing, mutation-resistance |
| `ts` | branch-coverage, edge-cases, assertions, isolation, negative-testing, mutation-resistance |
| `zig` | branch-coverage, edge-cases, assertions, isolation, negative-testing, mutation-resistance |
