---
name: follow-tool-madge
description: Audit dependencies and circular imports with Madge
argument-hint: [path/to/module]
related:
- run-verify
- run-test
- run-scan
---

# Follow Tool Madge

## Goal

Use `madge` to analyze a module's dependency graph — find circular imports, orphan files, and leaf/dependency queries — then hand the list of things to fix back to the requester

## Scope

For JS/TS projects with `madge` installed. Covers circular detection, per-file dependency queries, graph rendering, and CI gating — `madge` checks dependency structure only; unused exports/files detection uses `knip`, and duplicate code uses jscpd (different purposes)

- Latest: `madge@8.0.0` (npm, verified 2026-09-13)

## Execute

### 1. Check Prerequisites
> Goal: make sure madge is ready to run before scanning

```sh
madge --version
```

- If `command not found` → suggest `npm install --save-dev madge` (`pnpm`/`bun` also work) — no global install needed
- For large TS projects: if a `tsconfig.json` exists, pass it via `--ts-config`

### 2. Run Circular Detection
> Goal: find circular dependencies that must be fixed

```sh
madge --circular src/
madge --circular --ts-config tsconfig.json --extensions ts,tsx src/
```

- Circular imports bloat bundles, break init order, and split test isolation
- If a cycle is found → list the cycling file pairs for the requester to decide (extract a shared module / use dependency injection / move type-only imports behind `import type`)

### 3. Run Dependency Queries
> Goal: find orphans, leaves, and dependents of a target file

```sh
madge --orphans src/
madge --leaves src/
madge --depends path/to/file.ts src/
```

- `--orphans` = files nobody imports → deletion candidates
- `--leaves` = files that import nothing → leaf utilities/entry points
- `--depends` = which files (transitively) import the target — measure the blast radius before refactoring

### 4. Export And Render Graph
> Goal: produce reusable output (JSON for CI/scripts, images for review)

```sh
madge --json src/ > deps.json
madge --image graph.svg src/
madge --image graph.svg --layout dot --extensions ts,tsx src/
```

- `--image` requires Graphviz (the `dot` binary) — if missing, skip it or use `--json` instead
- `--extensions ts,tsx` forces parsing only the listed extensions; `--exclude <regex>` drops paths
- `--warning` shows skipped files; `--debug` reveals parse details when results look odd

### 5. Wire Into CI
> Goal: fail the pipeline when a new circular dependency appears

```sh
madge --circular --exit-code 1 --extensions ts,tsx src/
```

- The default exit code is 0 even with circulars — `--exit-code` is required (or combine `--no-color` with a pipe)
- Put it in the CI lint job or a hook; if the repo has a `.moon/workspace.yml`, run it as a moon task and gate with `vcs.hooks`
- For other repos, use `hk` or `lefthook` when a hook-level check is wanted

### 6. Verify
> Goal: confirm results before reporting

- If circulars are found → summarize the cycle count + involved files + fix approaches
- Run `/run-verify` (build/typecheck/tests) to confirm nothing broke after fixing a cycle; if code changed, run `/run-test` for the touched modules
- Run `/run-scan` when a broader audit is needed (unused deps, secrets, lint)

## Rules

- A `src/` path (or the path the requester provides) is required — if missing, ask first
- Report circulars for the requester to fix — don't refactor on your own without assignment
- `--exit-code` is always required in CI (default = 0)

- Use /run-verify to confirm build/typecheck/tests after a cycle fix
- Use /run-test to confirm touched modules after refactoring
- Use /run-scan for audits beyond the dependency graph

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A dependency graph report with the circular list and per-file impact
- Orphan/leaf candidates for cleanup
- JSON/image artifacts for CI or review
