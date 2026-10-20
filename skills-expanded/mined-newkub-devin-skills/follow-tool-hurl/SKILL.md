---
name: follow-tool-hurl
description: Use the Hurl CLI to run and test HTTP requests from plain-text files with assertions
argument-hint: "[scope]"
related:
  - deep-test
  - run-test
  - follow-test
  - follow-tool-bruno
  - follow-tool-github-actions

---

## Goal

Use Hurl to write and run API tests from `.hurl` plain-text files — built-in assertions, request chaining, CI-friendly

## Scope

Use for projects that want API test files diffable in Git, run on a pure CLI with no GUI or extra runtime

- Latest: `hurl@8.0.1` (verified 2026-09-13) — Rust single binary, powered by libcurl
- Need GUI/collections → `/follow-tool-bruno`; need docs/mock server from a spec → `/follow-tool-scalar`

## Execute

### 1. Installation

> Goal: install the Hurl binary

1. Windows: `scoop install hurl` or `winget install hurl` (requires Visual C++ Redistributable)
2. Global via mise: `mise use -g hurl` if that registry is supported
3. Rust: `cargo install --locked hurl`; npm dev-dep: `bun add -D @orangeopensource/hurl`
4. Docker: `docker pull ghcr.io/orange-opensource/hurl:latest`
5. Verify with `hurl --version`

### 2. Write Hurl Files

> Goal: create `.hurl` files that assert the correct response

1. Keep tests in a directory such as `tests/api/` or put `.hurl` files beside the feature
2. Format: a request block followed by the expected response — at minimum a status code
3. Add `[Asserts]` with queries: `jsonpath`, `xpath`, `header`, `status`, `duration`, `body`, `regex`, `sha256`
4. Use predicates: `==`, `!=`, `contains`, `startsWith`, `matches`, `exists`, `>`, `<`
5. See full syntax in 

### 3. Chain Requests

> Goal: reuse values from earlier responses in subsequent requests

1. Add a `[Captures]` section to store values, e.g. `csrf_token: xpath "..."`, `id: jsonpath "$.id"`
2. Interpolate with `{{name}}` in the next request (URL, headers, body)
3. Use chains for login → create → verify → cleanup flows

### 4. Run Tests

> Goal: run tests with reporting for local and CI

1. Run with `hurl --test tests/api/` (a directory = run all `*.hurl` recursively)
2. Variables: `--variable key=value` or `--variables-file vars.env` (don't commit secrets — use env vars `HURL_*`)
3. Reports: `--report-junit out.xml`, `--report-html out/`, `--report-json out.json`, `--test` exits non-zero on failure
4. Debug: `--very-verbose`, `--error-format long`, `--retry`, `--max-time`
5. See all options in [references/cli.md](references/cli.md)

### 5. Integrate CI

> Goal: gate the pipeline on hurl's exit code

1. Use `hurl --test` + `--report-junit` in a CI step
2. No official GitHub Action — install with a package manager or the npm binary in the workflow
3. Store reports as artifacts; pair with JUnit reporters (dorny/test-reporter etc.)
4. See examples in 

## Rules

### 1. File Format

- One entry = request + expected response; the response block holds the asserts
- Use the `HTTP 200` shorthand, or `HTTP *` + `[Asserts]` when more detail is needed
- Secrets go only in `--variables-file` or env vars — never hard-code them in `.hurl`

### 2. Testing Discipline

- Every assert must be deterministic — use `jsonpath`/`xpath` queries, not whole-body compares, when fields are dynamic
- Chain with captures when a flow needs sequential requests
- Always use `--test` in CI to get the correct exit code

### 3. Limitations

- HTTP/HTTPS only — no gRPC/WebSocket/MQTT (consider `/follow-tool-bruno` or a dedicated tool)
- No full scripting language — for complex logic split files or use the `/deep-test api` script approach

- Use /deep-test api if needed
- Use /follow-tool-github-actions if needed (tool hurl)

## References

- [CLI options](references/cli.md)




- Use /run-test if needed
- Use /follow-test if needed


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `.hurl` test files live in version control and pass `hurl --test`
- Assertions cover status, headers, and key body fields
- Chaining works correctly for multi-step flows
- CI gates on exit code + JUnit report
