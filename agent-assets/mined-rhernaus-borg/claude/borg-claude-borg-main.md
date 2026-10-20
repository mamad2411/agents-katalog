# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
# Build
cargo build
cargo build --release

# Run the agent
cargo run                           # Main autonomous mode
cargo run -- info                   # Show agent info
cargo run -- improve                # Single improvement iteration
cargo run -- objective list         # List strategic objectives
cargo run -- plan show              # Show current plan

# Testing
cargo test                          # Run all tests
cargo test <test_name>              # Run a specific test
cargo test --test <file_name>       # Run tests in a specific file

# Full quality gate (format, lint, test, audit, build)
cargo fmt --all && \
    cargo clippy --all-targets --all-features -- -D warnings -W clippy::cognitive_complexity && \
    cargo test --all --locked && \
    cargo audit --deny warnings && \
    cargo build --release --locked --all-features
```

## Architecture Overview

Borg is an autonomous self-improving AI agent. The codebase is organized into these major modules (see `src/lib.rs`):

- **core**: Agent logic, configuration, planning, ethics, strategies, authentication, and the mode dispatcher
- **code_generation**: LLM-powered code generation with tool-use protocol and iterative refinement
- **providers**: LLM provider implementations (OpenRouter, Anthropic, OpenAI)
- **model_selection**: Dynamic model selection with policy-based intent routing
- **modes**: Six-mode architecture (Orchestrate, Architect, Code, Review, Debug, Ethical)
- **database**: Persistence layer (file-based and MongoDB)
- **version_control**: Git operations and autonomous GitOps
- **testing**: Test runners, coverage analysis, result evaluation
- **resource_monitor**: System resource monitoring

### Key Architectural Patterns

**Modes v2 Dispatcher** (`src/core/mode_dispatcher.rs`): When `modes.v2_enabled` is true, routes work through six specialized modes. Only Code mode can modify files; Review and Ethical are read-only.

**LLM Tool Protocol**: Code generation uses a JSON-lines tool protocol (`{"tool":"Name","args":[...]}`) with up to 25 iterations (configurable via `code_generation.max_tool_iterations`).

**Strategy System** (`src/core/strategy.rs`): Goals are executed via strategies (CodeImprovement, ApiClient, WebResearch, etc.) that implement a common interface.

## Configuration

- Template: `config.sample.toml` (committed, placeholder values)
- User config: `config.toml` (gitignored, contains your API keys)
- Copy the sample to get started: `cp config.sample.toml config.toml`

LLM configuration supports multiple providers with these optional fields:
- `api_base`, `headers`, `enable_streaming`, `enable_thinking`
- `reasoning_effort`, `reasoning_budget_tokens`
- `first_token_timeout_ms`, `stall_timeout_ms`

## Testing Notes

- Integration tests create per-test configs with temp workspaces
- Tests rely on `env!("CARGO_BIN_EXE_borg")` for binary path
- Tests requiring LLM providers are marked with `#[ignore]` and need real API keys to run

## Important Implementation Details

- Workspace bootstrap: Git repo always initialized in `agent.working_dir` with an initial commit to ensure HEAD exists
- File targeting: Code blocks without a file indicator default to `src/main.rs`; always be explicit with `// File: path/to.rs`
- Commit messages are LLM-generated; mainline branch is chosen dynamically (master if present, else main)
- Merge conflicts abort without auto-resolution
