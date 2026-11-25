---
name: guardrails
description: Use in any repo with a guardrails.config.json or guardrails.md, before writing or changing tests, docs, dependencies or architecture, and before every commit. It explains how to pass the guardrails checks without padding or weakening tests.
---

# Working under @ws42ca/guardrails

The repo enforces its testing, docs and architecture rules with `guardrails`. CI blocks on the same checks, so run them yourself first.

## Journeys
The product is described as Critical User Journeys (MCP `guardrails_list_journeys`, `npx guardrails journeys list`). Check `guardrails_journey_coverage` to see which enforced (approved or client-provided) journeys lack an e2e test. For journeys with `run` steps, use `guardrails journeys scaffold`, `guardrails journeys generate-tests`, and `guardrails journeys run --base-url <url>` (optionally `--ids` or `--only-enforced`). Use `generate-tests --check` to verify generated files; never hand-edit them (JRN-6). Resolve tokens through `journeys.dataFile` (`.guardrails/client-data.json`) and mock every write endpoint (`mockRoute`).

Write the one e2e test for a journey under `e2e/`, titled with its ID (`test("CUJ-REVIEW client submits a choice", …)`), walking its steps. Use `guardrails journeys import <file.json>` only for configured base-branch `journeys.trustedProducers`. Imports never approve or overwrite approved/client-provided journeys; unapproved inferred/template journeys only warn until human approval. Protected journey edits and trust settings require a code owner's `guardrails:journeys-approved` label [JRN-3]. Agents may preview heuristic drafts with `npx guardrails journeys draft --dry-run` (no model call or write), but writing drafts and `guardrails journeys approve` are human-only; if a journey seems missing or wrong, call `guardrails_flag`.

## Before you write a test
1. Find the behaviour's spec ID: MCP `guardrails_list_specs`, or `npx guardrails specs`.
2. Validate it: MCP `guardrails_validate_test { specId, testFile, plannedLines }`, or `npx guardrails validate-test <ID> --file <path> --lines <n>`.
3. If the ID doesn't exist, stop. Ask the owner to add the behaviour to `specs.items`; don't invent an ID or edit the config yourself.
4. Ensure Vitest `setupFiles` includes `@ws42ca/guardrails/vitest-setup` (or `expect.hasAssertions()`), as TEST-9 blocks whenever test files exist and is never baselined.
5. Start the title with the ID: `it("REVIEW-02 expired token returns 410", …)`. Prefer one `it.each` table over several near-identical tests (cap 8 tests per ID, 300 lines per file).
6. Assert observable results: return values, written data, response status. Don't only assert that a mock was called.
7. Freeze time (`vi.useFakeTimers(); vi.setSystemTime(new Date("2026-01-01"))`). Use fixed inputs, no unseeded randomness.

## Stop and flag
If a test conflicts with the spec, seems impossible, or would need a special case to pass: STOP and call MCP `guardrails_flag { specId, file, reason }` (or `npx guardrails flag <ID> "<reason>" --file <path>`, where `reason` is at least 10 characters). Then tell the user. Never change code or tests just to satisfy a test. Flagging is the right move, not a failure: open flags block merge (FLAG-1) until a human resolves them.

## Before you commit
- Run MCP `guardrails_check { base: "origin/<base branch>" }`, or `npx guardrails check --base origin/<base>` (use `--base <base>` locally if no remote exists yet). Fix every ✖. Read every ⚠.
- Exit codes: `0` pass/ok, `1` blocking findings, `2` bad usage or setup error (`hook-guard` also exits `2` when denying a locked edit).
- In a PR branch add `--fails-on-base`: every new or changed test must fail on the base branch and pass on yours [TEST-11]. A test that already passes on base doesn't test your change.
- Run `npx guardrails labels plan --base origin/<base>` for an advisory summary (always exits `0`) of any code-owner approval labels the PR will need.
- For TEST-8, MCP `guardrails_mutants` (or `npx guardrails mutants --base origin/<base>`) lists surviving mutants (file, line, mutator). Kill them with real assertions. Never report a mutation score yourself; CI recomputes it.
- For a rule you don't understand, run `guardrails_explain_rule { id }` or `npx guardrails explain <ID>` (omit `<ID>` to list all 49 rules). Use `npx guardrails --help` or `npx guardrails <command> --help` for CLI usage.

## Never do these (they block, and a human has to approve them)
- Delete or loosen an existing test, remove an `expect`, or swap `toEqual` for `toMatchObject`/`toContain`, or `toBe` for `toBeTruthy` [TEST-7].
- Lower a threshold or mode, or widen an allowlist, in `guardrails.config.json`, `guardrails.md`, Vitest or Stryker config [TEST-7].
- Add entries to `.guardrails/baseline.json` or `.guardrails/test-suite-baseline.json` (baselines only shrink; ratcheting down after a fix is fine) [BASE-1, SUITE-6].
- Add a dependency that isn't in `deps.allow` or invent package names (new packages are checked against the npm registry) [ARCH-4].
- Add markdown/txt/rst docs outside `docs.allow` [DOC-1]. Put the content in `AGENTS.md` or a check.
- Add `.only`, `.skip`, `test.todo`, snapshots in T1 tests, or `// Stryker disable` [TEST-5].
- Make product code detect tests (`NODE_ENV === 'test'`, `VITEST`, `JEST_WORKER_ID`, `import.meta.vitest`), call `process.exit` outside a CLI entry, add `valueOf`/`equals`/`Symbol.toPrimitive` to pass comparisons, add `expect.extend`, count calls, or hard-code a test's expected value [ARCH-7].
- Copy-paste existing code instead of reusing it [ARCH-8].
- Edit spec-tagged tests or locked guardrails files (`guardrails.config.json`, `guardrails.md`, `.guardrails/**`, CODEOWNERS, workflows, hook settings) through any route, including the shell. Hooks deny it; humans unlock with `GUARDRAILS_ALLOW_TEST_EDITS=1`.

## If a check seems wrong
Flag it (`guardrails_flag`) and say so in your report: name the rule ID, file and why. Don't work around it. Workarounds like moving test code into helpers, renaming files or splitting lines get caught by other rules and by review.
