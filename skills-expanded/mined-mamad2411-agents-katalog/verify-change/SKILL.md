---
name: verify-change
description: Run repository-appropriate verification (build, lint, type-check, tests) on the changed files; summarize pass/fail per category.
---

# verify-change

> Run the verification a human reviewer would run before approving the change, scoped to the changed files where possible.

## When to use

- After `feature-dev` and `code-review`, before opening a PR.
- A workflow invokes `polymath-engineering:verify-change`.
- The user says "run the checks" or "verify it works".

## Inputs

- The current diff (used to scope which files matter).
- Project verification commands. Detect from these signals in order:
  1. `package.json` scripts: `lint`, `typecheck`, `test`.
  2. `pyproject.toml` / `requirements*.txt` with `pytest`, `ruff`, `mypy`.
  3. `Cargo.toml` → `cargo test`, `cargo clippy`.
  4. `go.mod` → `go test ./...`, `go vet ./...`.
  5. `*.csproj` / `*.sln` → `dotnet build`, `dotnet test`.
  6. `Makefile` → `make test` if defined.

## Project localization

Before the procedure, resolve the project snapshot — glob
`${POLYMATH_DATA_DIR:-$HOME/.polymath/data}/polymath-core/project-context.json` (newest
wins; absent → skip and use built-in defaults). Then apply (contract:
`polymath-core:project-context`):

- `skill_overrides["polymath-engineering:verify-change"].test_commands`:
  use the entry matching the project's primary language as the
  verification command, ahead of the detection order below.

## Procedure

1. Identify the verification commands the repo supports.
2. Run them in this order, stopping at the first hard failure:
   - **Build / compile** (if applicable).
   - **Lint / format check.**
   - **Type-check.**
   - **Unit tests.**
   - **Integration tests** (only if fast or scoped to the change).
3. If a step fails, surface the exact error output and the suspected file. Do not auto-fix unless the user has explicitly authorized it.
4. If a step is unavailable (no test infra, no linter), note "not applicable" rather than skipping silently.

## Output

```text
Verification summary:
  - build      : PASS / FAIL / N/A
  - lint       : PASS / FAIL / N/A
  - typecheck  : PASS / FAIL / N/A
  - unit tests : PASS / FAIL / N/A
  - smoke      : PASS / FAIL / N/A

Tests run: <count>; passed: <count>; failed: <count>.
Files changed verified: <count> / <total changed>.
```

When invoked by a workflow, the summary must include the words "tests", "verified", or "verification" so the `mustPass: stepSummaryMatches` check passes.

## Anti-patterns to avoid

- Running the entire test suite when a scoped run is sufficient (wastes time and obscures the signal).
- Treating a missing test framework as success — surface it.
- Auto-fixing without explicit permission.
