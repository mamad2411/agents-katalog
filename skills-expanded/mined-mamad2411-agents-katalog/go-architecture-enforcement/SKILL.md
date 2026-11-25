---
name: go-architecture-enforcement
description: >-
  Enforce repository-owned Go architecture with go-arch-lint v1.19.0. Use when a Go repository needs
  architecture rules, dependency-boundary checks, forbidden imports, proposed-vs-actual architecture review,
  CI enforcement, or safe rule changes. Trigger for go-arch-lint, architecture lint, layer violations, forbidden
  package dependencies, or Go dependency direction questions.
metadata:
  version: 1.0.0
  tool: go-arch-lint
  tool-version: v1.19.0
allowed-tools: Read, Glob, Grep, Bash
---

# Go architecture enforcement

Use `go-arch-lint` as a repository-owned check, not as a substitute for design. The repository owns the rule
file, scope, and failure policy. Keep the architecture vocabulary small and project-specific. Do not impose a
four-layer directory layout or rename code merely to fit a tool.

## Workflow

1. **Discover actual structure.** Read `go.mod`, package paths, build tags, generated-code boundaries, and tests.
   Classify the packages selected by the rule as nonempty. Report the actual dependency graph separately from any
   proposed architecture. A proposed rule is not evidence that the current code already satisfies it.
2. **Inspect the pinned tool.** Use a repository-owned script such as `scripts/arch-check` with `go run` pinned to
   `go-arch-lint@v1.19.0`; pass the absolute project path it expects. Run `go-arch-lint --help` and the help for
   selected scan/config commands before relying on flags or output. A tested configuration uses native JSON objects
   and `deepScan: false` intentionally. Record the observed command shape in the change or review note. Do not
   auto-install tools or dependencies without approval; a repository-owned pinned `go run` is an allowed alternative.

3. **Define rules in the repository.** Keep the config beside the module, review it like source, and use package
   globs that resolve to real packages. Use the narrowest rule set that expresses the intended boundary.
4. **Classify findings.** Separate violations in existing code from violations introduced by the proposed change.
   An empty selector, unmatched package, or missing module dependency is a setup error, not a passing scan.
5. **Verify the gate.** Run the normal Go tests and the architecture command. Add a real forbidden dependency
   fixture or test package for the rule, and confirm the gate fails before removing the fixture. Keep allowed and
   forbidden examples both real and readable.
6. **Report honestly.** Include tool version, command observed from help, selected package counts, findings, and
   limitations. Report target-repository evidence generically and do not infer rollout success from a local run.

## Rule contract

- A `deps` collection written as `{}` is rejected by the tested configuration. For stdlib-only packages, a
  self-only `mayDependOn` entry for the same component is valid.
- Root scans can include embedded `node_modules` Go trees. Exclude installed dependencies explicitly rather than
  treating them as repository packages.
- Unknown package names fail clearly. Preserve that failure instead of widening selectors.
- Import checks describe dependency structure only. They do not prove CI authorization, endpoint authorization, or
  write behavior; keep those as separate behavior tests.

- A forbidden edge must be demonstrated by an actual import or dependency in a test fixture, not by a comment.
- Detect missing dependencies and malformed module/package selection before interpreting architecture findings.
- Do not weaken a rule to make an existing violation disappear. Record an explicit design decision or fix the edge.

## Safe command shape

```bash
# Inspect the installed/pinned interface first.
go-arch-lint --help
# Then use only flags and output formats confirmed by help.
go-arch-lint <confirmed-scan-command> <confirmed-options>
```

Do not assume a deep scan default, a JSON schema, or a particular config filename. If the tool is unavailable,
report that dependency and show the exact pinned command the repository can run. Do not install a global tool.

## Review examples

**Allowed:** `internal/handler` imports `internal/service` because the repository's rule permits that edge.

**Forbidden:** `internal/handler` imports `internal/storage` when the repository rule requires handlers to use the
service boundary. The fixture must compile far enough for the linter to observe the import.

The skill's examples are scenarios, not proof of a consumer rollout. See `references/scenario-review.md` for the
review matrix and observed limitations. See `evals/evals.json` for portable behavior cases.
