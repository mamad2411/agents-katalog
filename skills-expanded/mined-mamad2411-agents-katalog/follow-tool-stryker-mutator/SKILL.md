---
name: follow-tool-stryker-mutator
description: Set up and use Stryker Mutator for mutation testing in JavaScript/TypeScript projects
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - follow-test
  - update-tests
  - run-test
  - follow-tool-vitest
  - follow-lang-typescript
  - follow-lang-javascript

---

## Goal

Set up and use Stryker Mutator for mutation testing to improve the quality of JavaScript/TypeScript tests

## Scope

For JavaScript, TypeScript, React, Angular, Vue, Svelte, and Node.js projects with a supported test runner

- Stryker measures test quality through mutants — it is not a test runner or coverage tool; run tests via `/follow-test` and check coverage via `improve coverage`
- Use it once tests pass and are stable — if tests still fail or are flaky, fix them first with `/update-tests`

- Latest: `@stryker-mutator/core@10.0.0` (verified 2026-09-13) — v10 requires Node.js 22+ (dropped Node 20)

## Execute

### Workflows

> Goal: Dispatch to the workflow matching the topic

| Topic | Workflow |-------|----------| setup | `workflows/setup-stryker/SKILL.md` — install, stryker config, test runner integration | optimize | `workflows/optimize-mutation/SKILL.md` — incremental mode, mutator filtering, concurrency, thresholds 
1. If the argument matches a topic → read and follow `workflows/<name>/SKILL.md` instead of the steps below
2. If not → follow the steps below normally

### 1. Installation

> Goal: Install Stryker and the test runner plugin

1. Check Node.js >= 22 and the current test runner (jest, vitest, mocha, jasmine)
2. Install `@stryker-mutator/core` with `bun add -D @stryker-mutator/core`
3. Install the runner plugin, e.g. `bun add -D @stryker-mutator/vitest-runner`
4. Install the TypeScript checker if you use TypeScript: `bun add -D @stryker-mutator/typescript-checker`
5. See the details in 

### 2. Initialize and Configure

> Goal: Create the Stryker config

1. Run `bunx stryker init` to generate the config
2. Check `stryker.config.json` or `stryker.config.mjs`
3. Define `testRunner`, `mutator`, `reporters`, `coverageAnalysis`
4. Set the `mutate` and `ignorePatterns` globs
5. See the config options in 

### 3. Run Mutation Testing

> Goal: Run mutation testing and review the results

1. Run `bunx stryker run`
2. Use `bunx stryker run --logLevel trace` if you hit problems
3. Review the report in `reports/mutation/html/index.html`
4. Identify surviving mutants, `NOT CAUGHT`, and `timeout` mutants

### 4. Improve Tests

> Goal: Add tests for the mutants that survived

1. Analyze the surviving mutants
2. Write additional tests to catch the missing cases
3. Run `/update-tests` to write quality tests
4. Run the regular tests first, then re-run Stryker

### 5. CI Integration

> Goal: Integrate Stryker with the CI pipeline

1. Add a step running `bunx stryker run` in GitHub Actions
2. Set up the Stryker Dashboard if you want to track the score
3. Use a budget or threshold if you have one
4. Upload the reports for review

## Rules

### 1. Test Quality

- Use Node.js >= 22 (Stryker v10)
- Stable tests are required before running Stryker
- Don't run Stryker when tests are flaky
- The build must work on the host platform

### 2. Configuration

- Use `coverageAnalysis: 'perTest'` for efficiency
- Define `mutate` explicitly
- Use `ignorePatterns` for files you don't want mutated

### 3. Mutant Handling

- Add tests for surviving mutants
- Use `// Stryker disable` only when necessary
- Track the mutation score across runs

### 4. Reports

- View the HTML report after each run
- Use the dashboard for trends
- Check the `timeout` mutants

- Use /follow-test if needed
- Use /run-test if needed
- Use /follow-tool-vitest if needed
- Use /follow-lang-typescript if needed
- Use /follow-lang-javascript if needed

## References

- [CLI reference](references/cli.md)

- Use /deep-test mutation if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Stryker installed and working
- The mutation score is tracked
- Surviving mutants are identified and addressed
- Tests are of better quality
- CI runs mutation testing automatically

