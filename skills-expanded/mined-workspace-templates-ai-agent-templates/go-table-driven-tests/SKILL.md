---
name: go-table-driven-tests
description: Writes idiomatic table-driven Go tests with named subtests, golden files and race detector runs, and refactors repetitive tests into tables.
---

# Go table-driven tests

One table, one loop, one subtest per case, and a failure message that names the case.

## Steps

1. Define the case struct next to the test: `name`, inputs, `want`, and `wantErr` when errors matter. Add a case for each branch: empty, boundary, invalid, and the bug that prompted the test.
2. Loop and run subtests: `for _, tc := range tests { t.Run(tc.name, func(t *testing.T) { ... }) }`. Use descriptive names, because `go test -run 'TestParse/negative'` must target one row.
3. Compare with `cmp.Diff(tc.want, got)` from go-cmp and print `(-want +got)`. Check errors with `errors.Is` or `errors.As`, not string matching.
4. Call `t.Helper()` in helpers, `t.Cleanup` for teardown, `t.TempDir()` for files, `t.Setenv` for environment.
5. For parallel subtests call `t.Parallel()` inside `t.Run` and, on Go before 1.22, copy the loop variable with `tc := tc`.
6. For large output (rendered HTML, JSON, SQL) use golden files in `testdata/` with an `-update` flag, and review the diff before committing.
7. Run `go test -race -count=1 ./...` and, for flaky suspects, `-count=20`.

## Rules

- Test through the exported API when you can; use an internal test file only for unexported logic that is hard to reach.
- No assertions in goroutines that outlive the test.
- Use `testing/fstest` and interfaces instead of the real file system or network.

## Report

Cases added, packages covered, race detector result and any golden files created.
