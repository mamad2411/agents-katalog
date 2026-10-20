# Copilot Instructions for Lok

## Project Overview

Lok is a Rust CLI tool for declarative multi-LLM orchestration. Workflows are defined in TOML and executed against multiple backends (Claude, Gemini, Codex, Ollama, Bedrock) with DAG-based step execution, consensus strategies, retries, and template interpolation.

Package name: `lokomotiv`. Binary name: `lok`.

## Build and Validation

```bash
cargo build                       # Build
cargo test                        # Run all tests (unit + integration)
cargo clippy -- -D warnings       # Lint (warnings are errors)
cargo fmt --check                 # Check formatting
```

Always run `cargo test && cargo clippy -- -D warnings` before approving changes.

## Project Layout

```
src/
  main.rs          - CLI entry point (clap)
  workflow.rs      - Core workflow engine: StepResult, step execution, DAG runner,
                     template interpolation, condition evaluation (~3800 lines)
  backend/
    mod.rs         - Backend trait, QueryOutput, create_backend(), run_query_with_config()
    claude.rs      - Claude API + CLI backend
    gemini.rs      - Gemini CLI backend
    codex.rs       - Codex CLI backend
    ollama.rs      - Ollama HTTP backend
    bedrock.rs     - AWS Bedrock SDK backend (feature-gated)
  consensus.rs     - Multi-backend consensus strategies (vote, weighted_vote, synthesis)
  conductor.rs     - Multi-step conductor for interactive workflows
  config.rs        - TOML config parsing
  spawn.rs         - Parallel backend spawning
  debate.rs        - Multi-model debate mode
  team.rs          - Team-based multi-backend queries
  tasks/           - Task-specific modules (hunt, review, etc.)
tests/
  integration.rs   - Integration tests using shell backend
docs/
  design-docs/     - Design documents for each task (clo-XX-description.md)
  plans/           - Implementation plans (clo-XX-description.md)
  prds/            - Product requirements documents
  reviews/         - AI review outputs
  status/          - Workflow state files (clo-XX-workflow.yaml)
```

## Task Context for PR Reviews

Each PR is linked to a Linear task (CLO-XX). To understand the full scope of a change:

1. **Design document**: `docs/design-docs/clo-XX-*.md` - contains the architecture, detailed design, constraints, and acceptance criteria
2. **Implementation plan**: `docs/plans/clo-XX-*.md` - phased task breakdown
3. **Workflow state**: `docs/status/clo-XX-workflow.yaml` - tracks phase progression and history
4. **Discovery report** (if exists): `docs/prds/discovery-report-*-clo-XX.md` - prior art research and assumption mapping
5. **PR description** - links to the Linear task URL and summarizes the change

When reviewing a PR, read the design document first to understand the intent and constraints, then verify the implementation matches the acceptance criteria listed there.

## Architecture Principles

- `Backend` trait is the central abstraction - all LLM queries go through `Backend::query()`
- `QueryOutput { stdout, stderr, exit_code }` is the structured return type from backends
- `StepResult` carries the output of every workflow step through the DAG
- CLI backends capture stderr separately; API backends return `stderr: None, exit_code: None`
- New fields on public structs must be `Option<T>` to avoid breaking changes
- Shell steps use `run_shell()` which returns `ShellOutput` with separated stdout/stderr
- Error paths use `StepResult::error()` constructor; success paths use explicit struct literals

## Coding Conventions

- Rust 2021 edition, async with tokio
- `anyhow::Result` for error handling, `anyhow::bail!` for early returns
- `#[derive(Debug, Clone)]` on public data types
- No unnecessary comments or docstring churn on unchanged code
- `cargo fmt` and `cargo clippy -- -D warnings` must pass
- Feature gates for optional backends: `#[cfg(feature = "bedrock")]`
- Test fixtures live in `#[cfg(test)] mod tests` within each source file

## Review Checklist

When reviewing PRs, check:

1. **Design alignment**: Do changes match the design doc's acceptance criteria?
2. **All construction sites updated**: If a struct gains fields, every construction site must be updated
3. **No behavioral regressions**: Existing tests pass without assertion changes
4. **Option fields for new struct members**: New public fields should be `Option<T>` or have defaults
5. **Error paths use StepResult::error()**: Not manual struct construction with all-None fields
6. **CLI vs API backend distinction**: CLI backends populate stderr/exit_code; API backends use None
7. **No merged stdout/stderr**: Shell and CLI outputs keep streams separate
