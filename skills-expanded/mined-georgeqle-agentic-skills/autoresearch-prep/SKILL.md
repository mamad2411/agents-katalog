---
name: autoresearch-prep
description: Scaffold a program.md for $autoresearch by auto-detecting codebase signals and interviewing for what can't be inferred
type: planning
version: v0.0
invocation: chained
argument-hint: "[output-path]"
context_intake: scoped
---

# Autoresearch Prep

Invoke as `$autoresearch-prep`.

Scaffolds a `program.md` research program for `$autoresearch`. Auto-detects benchmark commands, test commands, sandbox boundaries, and exclude patterns from the codebase, then asks the user only what it can't infer: metric command and direction, research directions, and budget.

## When to Use

When the user wants to start an `$autoresearch` loop but doesn't have a `program.md` yet.

## Preconditions

- A git repository with code to optimize
- The user has a measurable property in mind (benchmark, bundle size, test coverage, etc.)

## Process

### 0. Resolve Output Path

1. If `$ARGUMENTS` is provided and non-empty, use it as the output path.
2. Otherwise default to `./program.md`.
3. If the file already exists, warn the user and ask whether to overwrite or pick a new path.

### 1. Auto-Detect Codebase Signals

Scan the repository for:

**Benchmark commands:**
- `package.json` scripts containing `bench` or `benchmark`
- `bench/`, `benchmarks/`, or `perf/` directories
- `Makefile` targets: `bench`, `benchmark`, `perf`
- Language-specific: `cargo bench`, `go test -bench`, `pytest-benchmark`, `hyperfine` usage

**Test commands:**
- `package.json` `test` script
- `Makefile` `test` target
- Language-specific: `pytest`, `cargo test`, `go test`, `jest`, `vitest`, `mocha`

**Sandbox globs** (based on what directories exist):
- `src/**`, `lib/**`, `app/**`, `pkg/**`, `internal/**`, `crates/**`
- Include only directories that actually exist in the repo

**Exclude patterns:**
- Test files: `**/*.test.*`, `**/*.spec.*`, `**/test/**`, `**/tests/**`, `**/__tests__/**`
- Config: `*.config.*`, `.eslintrc*`, `tsconfig*`, `.prettierrc*`
- Benchmark harness: `bench/**`, `benchmarks/**`, `perf/**`
- Build output: `dist/**`, `build/**`, `target/**`, `out/**`, `.next/**`
- Lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `go.sum`
- VCS/tooling: `.git/**`, `node_modules/**`, `.autoresearch/**`

### 2. Light Interview

Present the detected signals as a summary, then ask:

1. **Metric command + direction** (always required): "What shell command prints your target metric as a single number? Is higher or lower better?"
2. **Research directions** (always required): "What optimization directions should the agent explore? List 2-5 ideas."
3. **Budget** (offer default): "How many iterations? (default: 20)"

If benchmark commands were detected, suggest them as starting points for the metric command.
If test commands were detected, note they'll be included as the test command with `required: true`.

### 3. Findings Validation

Show the complete proposed `program.md` content to the user. Let them confirm or adjust any section before writing.

### 4. Validate Metric Command

1. Run the metric command once from the project root.
2. Parse the last number from stdout.
3. If the command fails or produces no parseable number, stop and ask the user to fix it.
4. Record the parsed value as the baseline for the Context section.

### 5. Write program.md

Write the file in the exact format expected by `$autoresearch`:

```markdown
# Research Program

## Metric
command: <user-provided command>
direction: <higher-is-better | lower-is-better>

## Budget
max_iterations: <user-provided or 20>

## Sandbox
files:
  - <detected or user-adjusted globs>
exclude:
  - <detected or user-adjusted patterns>

## Test Command
command: <detected test command>
required: true

## Research Directions
1. <direction one>
2. <direction two>
...

## Context
Baseline metric value: <measured value>
<any additional context from interview>
```

Omit the `Test Command` section if no test command was detected or provided.

### 6. Route

**Recommended next command:** `$autoresearch <output-path>`

## Constraints

- Do not run the autoresearch loop — only scaffold `program.md`.
- Do not modify any source files in the repository.
- Do not create the `.autoresearch/` directory.
- Do not create alignment pages.
- Do not follow the shared shipping contract — this skill writes one local file, not tracked repo changes.
