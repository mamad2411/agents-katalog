---
name: verify-test-cases
version: 1.4.1
description: Verify test cases in all test files modified since branching out from base branch. Checks that test cases make sense, have no duplications, and provide meaningful coverage. Spawns parallel agents for multi-file analysis. After the user confirms test-case changes, runs coverage (npm test:coverage or Jest/Vitest fallback) and fixes tests until coverage passes.
argument-hint: ""
---

Verify the quality and correctness of test cases in all test files modified since branching out from the base branch.

**Usage:**
- `/verify-test-cases` - Verify test files modified since branching from base branch

**Instructions:**

1. **Determine the base branch:**
   - Check if a `.agent` file exists in the current directory
   - If it exists, read it and look for a `baseBranch=<value>` line to extract the base branch
   - If no `.agent` file or no `baseBranch` key, default to `main`

2. **Identify modified test files since branching:**
   - Run `git diff --name-only <base-branch>...HEAD` to get all files modified since branching from the base branch
   - Filter for test files using common patterns:
     - `*.test.*`, `*.spec.*` (JS/TS)
     - `test_*.py`, `*_test.py` (Python)
     - `*_test.go` (Go)
     - `*_test.rs`, files under `tests/` (Rust)
     - Files under `__tests__/`, `test/`, `tests/`, `spec/` directories
   - If no test files were modified, inform the user and STOP

3. **Analyze test files using a team:**

   Spawn parallel agents to analyze test files concurrently. Each agent reviews one or more test files independently.

   **a) Determine team size** based on the number of test files:
   - 1–2 test files → analyze directly (no team needed)
   - 3–5 test files → spawn 2 reviewer agents
   - 6+ test files → spawn 3 reviewer agents

   **b) If spawning a team:**
   - Use `TeamCreate` with name `verify-tests`
   - Use `TaskCreate` to create one task per reviewer: "Review test files: `<file1>`, `<file2>`, ..."
   - Divide test files across reviewers, grouping files that test the same source module together when possible
   - Spawn reviewers using the `Task` tool (`subagent_type: general-purpose`) with `run_in_background: true` and the team name
   - Each reviewer receives:
     - The list of test files to analyze
     - Instructions to also read the source files being tested for context
     - The full verification checklist (steps 4 and 5 below)
   - Reviewers must mark their tasks as completed and message the team lead with findings
   - Wait for all reviewers to finish, then aggregate results

   **c) If analyzing directly (1–2 files):**
   - Read and analyze the test file(s) yourself following steps 4 and 5

4. **Verify test cases make sense:**
   For each test file, check that:

   a. **Test descriptions match behavior:**
      - Test names/descriptions accurately reflect what is being tested
      - The test body actually tests what the name says it does

   b. **Assertions are meaningful:**
      - Tests have actual assertions (not just running code without checking results)
      - Assertions verify the right thing (not just `toBeTruthy()` on everything)
      - Edge cases and boundary conditions are covered where appropriate

   c. **Test setup is correct:**
      - Mocks and stubs make sense for what's being tested
      - Test fixtures and data are realistic
      - Setup/teardown properly initializes and cleans up state

   d. **Tests are independent:**
      - Tests don't rely on execution order
      - Shared state isn't leaking between tests

   e. **Tests match the source code:**
      - Tests cover the actual function signatures and behavior
      - Tests aren't testing stale or non-existent APIs

5. **Check for duplications:**
   For each test file and across all modified test files:

   a. **Exact duplicates:**
      - Tests with identical or near-identical test bodies
      - Copy-pasted tests that weren't modified

   b. **Logical duplicates:**
      - Different tests that verify the exact same behavior
      - Tests that overlap significantly in what they cover

   c. **Redundant assertions:**
      - Multiple assertions in separate tests that check the same thing
      - Tests that are strict subsets of other tests

6. **Report findings:**

   If a team was used, aggregate all reviewer findings and clean up the team (send `shutdown_request` to each reviewer, then `TeamDelete`).

   Format the output as follows:

```
## Test Verification Report

### Files Analyzed
- `path/to/file.test.ts` (N tests)
- `path/to/other.spec.js` (N tests)

### Issues Found

#### Nonsensical / Incorrect Tests
- **file.test.ts:42** `"should handle empty input"` - Test passes a non-empty string, contradicting its description
- **file.test.ts:67** `"should return user"` - No assertion on the return value

#### Duplicate Tests
- **file.test.ts:30** and **file.test.ts:55** - Both test the same "valid email" scenario with identical logic
- **other.spec.js:12** and **other.spec.js:40** - Logically equivalent: both verify default config values

#### Missing Coverage
- `createUser()` has no test for the error/rejection path
- Edge case: empty array input is not tested for `processItems()`

### Summary
- Total test files analyzed: N
- Total test cases reviewed: N
- Issues found: N
- Duplicates found: N
- Verdict: PASS / NEEDS ATTENTION
```

7. **Coverage gate (mandatory after test-case changes are final):**
   - Wait for the user to explicitly confirm that test-case work is done: either they approve your proposed edits (after you apply them), they confirm they applied changes themselves, or they confirm the report required no test changes and they are ready to proceed.
   - **Choose the coverage command** (repository root). If there is no `package.json`, tell the user coverage cannot be run for this workspace and STOP after the report.
   - **Node.js projects:** Read `package.json` `scripts` and dependencies (`dependencies` / `devDependencies` / `peerDependencies`):
     1. If a `test:coverage` script exists, use **`npm run test:coverage`**.
     2. Otherwise, if the project uses **Vitest** (e.g. `vitest` in deps or a `test` script invoking vitest), run **`npx vitest run --coverage`**.
     3. Otherwise, if the project uses **Jest** (e.g. `jest` in deps or a `test` script invoking jest), run **`npx jest --coverage`**.
     4. Otherwise, if another script clearly runs tests with coverage (e.g. `coverage`, `test -- --coverage`), run that via **`npm run <script>`**.
     5. If none of the above apply, tell the user no coverage command could be determined and STOP after the report.
   - Run the chosen command. If it fails (non-zero exit, failing tests, or coverage thresholds not met per the project’s configuration), fix the tests (or adjust tests only when production code is correct and the test is wrong). **Re-run the same command. Iterate until it exits successfully.**
   - Do not treat the verification report as complete until this step succeeds.

8. **Handle edge cases:**
   - If there are no commits on the branch compared to the base branch, inform the user and STOP
   - If modified files include both test and source files, use the source files for context but only report on the test files
   - If a test file imports from files you can't find, note it but continue analysis
   - For very large test files (>500 lines), focus on the changed sections using `git diff` for those specific files
