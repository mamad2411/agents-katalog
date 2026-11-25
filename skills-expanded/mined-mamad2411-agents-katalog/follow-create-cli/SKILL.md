---
name: follow-create-cli
description: Build CLI applications with Rust or Bun, picking the right stack and architecture
argument-hint: "[scope]"
related:
  - follow-create-bun-cli
  - follow-create-rust-cli
  - deep-review-codebase
  - flatten-directory
  - ship
  - rethink
  - run-test

---
## Goal

Build CLI applications with Rust or Bun according to context and requirements, with quality review via `/deep-review-codebase`

## Scope

Use when creating a new CLI or CLI tools (e.g. `tools/review-codebase`, `tools/analyze`) — this skill is a dispatcher only: pick the stack, then always delegate implementation to `/follow-create-rust-cli` or `/follow-create-bun-cli`; never implement the CLI inside this skill

- Frameworks: Bun → `cac`/`clipanion`/`commander` + `picocolors`; Rust → `clap` — always confirm the latest versions via `/deep-research` + `/follow-best-practice` (no version pins in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and framework patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Record the rationale for the chosen stack and libraries for future reference (create cli)

### 2. Decide CLI Stack

> Goal: evaluate and pick the right stack

1. Analyze requirements: performance, distribution, ecosystem, team skill
2. Choose Rust when: a single binary is required, high performance, zero runtime dependency
3. Choose Bun when: the team uses TypeScript, rapid development is needed, and the Bun runtime is installed
4. If unclear → use `/ask-me` or `/apply choose` first

### 3. Create CLI Project

> Goal: scaffold the structure for the chosen stack

1. If Rust → run `/follow-create-rust-cli`
2. If Bun → run `/follow-create-bun-cli`
3. Run `/deep-review-codebase` to pick the architecture per context — Clean is not mandatory
4. If directories nest deeper than 3 levels without need → run `/flatten-directory --mode code`
5. If the CLI needs tables, commands, prompts, or a TUI → run `/deep-review-codebase` to select libraries per the defined tech stack
6. Create `tools/<tool-name>/` when it is a tooling CLI in a monorepo

### 4. Review CLI

> Goal: check CLI quality after creation

1. Run `/deep-review-codebase-then-fix` to inspect design, structure, UX, and error handling
2. Fix according to the findings from `/deep-review-codebase-then-fix`
3. Run lint and tests per the chosen stack

### 5. Integrate Into Workspace

> Goal: wire the CLI into the workspace

1. Add scripts to the package manifest or task runner per `/follow-tasks`
2. If monorepo → run `/follow-monorepo` to define workspace and dependencies
3. Update references in `README.md` and `AGENTS.md` if needed

### 6. Ship

> Goal: deliver the work

1. Run `/ship`
2. If `/ship` fails → report the status

## Rules

### 1. Stack Selection

- Rust: suited for binary distribution, performance-critical, no runtime → delegate to `/follow-create-rust-cli`
- Bun: suited for TypeScript teams, rapid iteration, Bun runtime available → delegate to `/follow-create-bun-cli`
- Never force a stack that does not fit the context
- Once the stack is chosen, always delegate to `/follow-create-bun-cli` or `/follow-create-rust-cli`; never implement in this skill
- Record the stack rationale in `README.md` or the plan

### 2. Architecture Selection

- Every CLI must separate concerns clearly
- Use `/deep-review-codebase` to pick the architecture per context — Clean or Layered is not mandatory
- The domain layer must be pure with no side effects where appropriate
- Adapters handle I/O and external dependencies
- Presentation holds the entry points

### 3. Library Selection

- CLI needs to render tables → use libraries from `/deep-review-codebase`, e.g. `comfy-table` (Rust) or `TanStack Table` (Bun/TS)
- CLI needs commands/subcommands → use `clap` (Rust) or `cac` (Bun/TS)
- CLI needs interactive prompts → use `dialoguer`/`inquire` (Rust) or `@clack/prompts`/`inquirer` (Bun/TS)
- CLI needs a TUI → use `ratatui` (Rust) or `blessed`/`ink` (Bun/TS)
- Run `/deep-review-codebase` before choosing new libraries so they do not conflict with the current tech stack

### 4. Review Before Ship

- Run `/deep-review-codebase` before committing
- Support `--help`, `--version`, and clear error messages
- Have tests covering critical paths
- Have logging or tracing per stack

- Use /rethink if needed
- Use /deep-test cli if needed
- Use /run-test if needed


## File Structure

Canonical file structure + layer table: [templates/file-structure-cli.md](templates/file-structure-cli.md)
- Use /deep-test cli to verify the CLI contract (flags, exit codes, stdout/stderr) after scaffolding

## Expected Outcome

- CLI project with a properly chosen stack
- Structure follows the selected architecture — Clean not mandatory
- Directories not nested too deep (use `/flatten-directory` if needed)
- Passes `/deep-review-codebase`
- Integrated into the workspace
