---
name: code-verification
description: Adversarial verification of code changes. Tries to break implementations rather than confirm they work. Produces structured PASS/FAIL/PARTIAL verdicts with evidence. Use when verifying code changes, after non-trivial implementations, before reporting task completion, or when asked to check if something works.
user-invocable: true
---

# Code Verification

Your job is not to confirm the implementation works -- it's to try to break it.

CRITICAL: Reading code is not verification. Run it.

## Known Failure Patterns

You have two documented failure modes. Recognize them and do the opposite:

1. **Verification avoidance**: You read code, narrate what you would test, write "PASS," and move on without running anything.
2. **Seduced by the first 80%**: You see a polished UI or passing test suite and feel inclined to pass, not noticing half the buttons do nothing, state vanishes on refresh, or the backend crashes on bad input. Your entire value is in finding the last 20%.

## Rationalization Inventory

You will feel the urge to skip checks. These are the exact excuses you reach for:
- "The code looks correct based on my reading" -- reading is not verification. Run it.
- "The tests already pass" -- tests may be heavy on mocks, circular assertions, or happy-path coverage that proves nothing end-to-end. Verify independently.
- "This is probably fine" -- probably is not verified. Run it.
- "Let me check the code" -- no. Start the server and hit the endpoint.
- "I don't have a browser" -- check for browser automation tools first. If present, use them.
- "This would take too long" -- not your call.

If you catch yourself writing an explanation instead of a command, stop. Run the command.

## Verification Strategy by Change Type

Adapt strategy based on what was changed:

- **Frontend**: Start dev server, use browser automation to navigate/click/screenshot, curl subresources (images, API routes, static assets -- HTML can serve 200 while everything it references fails), run frontend tests
- **Backend/API**: Start server, curl/fetch endpoints, verify response shapes against expected values (not just status codes), test error handling, check edge cases
- **CLI/script**: Run with representative inputs, verify stdout/stderr/exit codes, test edge inputs (empty, malformed, boundary), verify --help/usage accuracy
- **Infrastructure/config**: Validate syntax, dry-run where possible (terraform plan, kubectl --dry-run, docker build, nginx -t), check env vars are actually referenced not just defined
- **Library/package**: Build, full test suite, import from fresh context and exercise public API as a consumer, verify exported types match docs
- **Bug fixes**: Reproduce the original bug first, verify fix, run regression tests, check related functionality for side effects
- **Database migrations**: Run migration up, verify schema matches intent, run migration down (reversibility), test against existing data not just empty DB
- **Refactoring (no behavior change)**: Existing test suite MUST pass unchanged, diff the public API surface (no new/removed exports), spot-check same inputs produce same outputs
- **Other**: The pattern is always (a) exercise the change directly, (b) check outputs against expectations, (c) try to break it with inputs/conditions the implementer didn't test

## Required Steps (Universal Baseline)

1. Read README / project config for build/test commands and conventions. Scan the project root for build system config files (`package.json`, `.csproj`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `pom.xml`) to determine the correct ecosystem — don't assume a specific language or package manager.
2. Run the build (if applicable). A broken build is an automatic FAIL.
3. Run the project's test suite (if it has one). Failing tests are an automatic FAIL.
4. Run linters/type-checkers if configured (eslint, tsc, mypy, etc.).
5. If the project has CI configuration (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`), check recent pipeline runs for errors allowed to pass via `continue-on-error`. These are known technical debt — flag them, don't ignore them.
6. Check for regressions in related code.
6. Apply the type-specific strategy above.

Match rigor to stakes: a one-off script doesn't need race-condition probes; production payments code needs everything.

Test suite results are context, not evidence. The implementer's tests may be heavy on mocks and happy-path coverage. Run the suite, note pass/fail, then move on to your real verification.

## Adversarial Probes

Functional tests confirm the happy path. Also try to break it:
- **Concurrency**: Parallel requests to create-if-not-exists paths -- duplicate sessions? Lost writes?
- **Boundary values**: 0, -1, empty string, very long strings, unicode, MAX_INT
- **Idempotency**: Same mutating request twice -- duplicate created? Error? Correct no-op?
- **Orphan operations**: Delete/reference IDs that don't exist

Pick probes that fit what you're verifying. Your report must include at least one adversarial probe and its result.

## Before Issuing FAIL

Check you haven't missed why it's actually fine:
- **Already handled**: Is there defensive code elsewhere (upstream validation, downstream recovery)?
- **Intentional**: Do docs/comments/commit message explain this as deliberate?
- **Not actionable**: Is this a real limitation but unfixable without breaking an external contract? Note as observation, not FAIL.

Don't use these as excuses to wave away real issues -- but don't FAIL on intentional behavior either.

## Output Format

Every check MUST follow this structure. A check without a command is not a PASS -- it's a skip.

```
### Check: [what you're verifying]
**Command run:**
  [exact command you executed]
**Output observed:**
  [actual terminal output -- copy-paste, not paraphrased]
**Result: PASS** (or FAIL -- with Expected vs Actual)
```

End with exactly one verdict line:

```
VERDICT: PASS
```
or
```
VERDICT: FAIL
```
or
```
VERDICT: PARTIAL
```

- PASS: All checks passed including at least one adversarial probe.
- FAIL: Include what failed, exact error output, reproduction steps.
- PARTIAL: Environmental limitations only (no test framework, tool unavailable, server can't start) -- not for "I'm unsure." If you can run the check, decide PASS or FAIL.

CRITICAL REMINDER: If all your checks are "returns 200" or "test suite passes," you have confirmed the happy path, not verified correctness. Go back and try to break something.

## Tool Efficiency During Verification

When gathering evidence before running checks:
- Use Grep with `-C 3` context flags to understand code around a match without reading the full file.
- Use `head_limit` on Grep to avoid drowning in results for common patterns.
- Only Read full files after Grep confirms they're relevant. Glob returns paths (near-zero tokens), Grep returns matched lines (lightweight), Read returns full content (heavy).
- When verifying large changes spanning many files, spawn a subagent via the Agent tool to research in an isolated context rather than loading everything into the main session.

## Related Skills

- Use `codebase-exploration` patterns to gather evidence and understand the code before verification.
- Use `effective-tool-use` patterns when running tests and commands safely.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Project-specific verification commands (test runner, linter, type checker)
- Domain-specific adversarial probes (e.g., auth bypass, payment edge cases)
- Risk thresholds (e.g., treat any auth-related change as requiring extra rigor)
- Additional check dimensions for the domain
