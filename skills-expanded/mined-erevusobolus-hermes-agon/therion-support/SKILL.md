---
domain: therion-support
name: Therion Support Domain Skill
version: 1.0.0
description: Comprehensive domain skill for supporting, troubleshooting, and improving the Therion codebase across debugging, code quality, documentation, dev environment, testing, and data engineering.
keywords:
  - debug
  - error
  - fix
  - crash
  - bug
  - refactor
  - docs
  - readme
  - testing
  - vscode
  - linting
  - workspace
  - profiling
  - code review
  - data
specialists:
  - THERION_TROUBLESHOOTER
  - THERION_CODE_QUALITY_ENGINEER
  - THERION_DOCUMENTATION_ARCHITECT
  - THERION_DEVENV_SPECIALIST
  - THERION_TESTING_SPECIALIST
  - THERION_DATA_ENGINEER
---

# Therion Support Domain Skill

This domain skill groups six specialists that together cover the full lifecycle of Therion codebase support: from diagnosing crashes and fixing bugs, to enforcing code quality, maintaining documentation, curating a productive development environment, ensuring test coverage, and managing data workflows.

## Specialists

### THERION_TROUBLESHOOTER

**Purpose:** Diagnose, debug, and resolve runtime issues in the Therion codebase — crashes, panics, hangs, unexpected errors, and regressions.

**Responsibilities:**
- Investigate crash reports, stack traces, and error logs from Therion processes.
- Reproduce bugs in isolated or sandboxed environments.
- Identify root causes and propose or implement targeted fixes.
- Profile hot code paths to find performance bottlenecks.
- Maintain a library of known issues and their resolutions.
- Collaborate with THERION_TESTING_SPECIALIST to add regression tests for each fixed bug.

**Trigger keywords:** `debug`, `error`, `fix`, `crash`, `bug`

**Usage:**
```
@therion-support invoke THERION_TROUBLESHOOTER "Investigate crash in module X at line Y with stack trace Z"
```

---

### THERION_CODE_QUALITY_ENGINEER

**Purpose:** Enforce and improve the internal quality of the Therion codebase through static analysis, linting, refactoring, and code review.

**Responsibilities:**
- Run and maintain linters (e.g. clippy, ruff, eslint) and formatters across the workspace.
- Perform systematic refactoring to reduce technical debt and improve maintainability.
- Conduct code reviews with a focus on correctness, idiomatic patterns, and security.
- Track and enforce coding standards documented in the project style guide.
- Integrate quality gates into CI/CD pipelines.
- Advise on architecture decisions to prevent future quality erosion.

**Trigger keywords:** `refactor`, `linting`, `code review`

**Usage:**
```
@therion-support invoke THERION_CODE_QUALITY_ENGINEER "Review PR #42 for style and correctness"
```

---

### THERION_DOCUMENTATION_ARCHITECT

**Purpose:** Own, structure, and maintain all documentation for the Therion project — README files, API docs, developer guides, and onboarding material.

**Responsibilities:**
- Create and maintain the top-level README and per-module doc files.
- Ensure API documentation is accurate, complete, and generated from source annotations.
- Write and update developer guides, setup instructions, and troubleshooting runbooks.
- Maintain a changelog and versioned release notes.
- Audit documentation for stale or missing content after every significant change.
- Establish and enforce documentation conventions (structure, tone, formatting).

**Trigger keywords:** `docs`, `readme`

**Usage:**
```
@therion-support invoke THERION_DOCUMENTATION_ARCHITECT "Update README with new installation steps"
```

---

### THERION_DEVENV_SPECIALIST

**Purpose:** Own the Therion developer experience — VS Code workspace configuration, toolchain setup, build scripts, and environment reproducibility.

**Responsibilities:**
- Maintain the VS Code workspace file (`therion.code-workspace` or `.vscode/settings.json`), including recommended extensions, debug configurations, and task definitions.
- Manage linting and formatting tool configurations (e.g. `.clang-format`, `pyproject.toml`, `rustfmt.toml`).
- Ensure reproducible builds via `Dockerfile`, `devcontainer.json`, or equivalent environment definitions.
- Troubleshoot toolchain, dependency, and build issues across platforms (Linux, macOS, Windows).
- Automate common developer workflows with scripts and Makefile targets.
- Keep the project's `.gitignore`, `.editorconfig`, and other dotfiles current.

**Trigger keywords:** `vscode`, `workspace`

**Usage:**
```
@therion-support invoke THERION_DEVENV_SPECIALIST "Fix VS Code debug launch config for module X"
```

---

### THERION_TESTING_SPECIALIST

**Purpose:** Design, implement, and maintain the testing strategy for the Therion project — unit tests, integration tests, fuzz testing, and coverage reporting.

**Responsibilities:**
- Write and review unit and integration tests for new and existing code.
- Set up and maintain test runners, coverage tools, and CI test jobs.
- Identify gaps in test coverage and prioritize filling them.
- Maintain fuzz targets and property-based tests for critical components.
- Investigate flaky tests and implement fixes.
- Produce coverage reports and track trends over time.

**Trigger keywords:** `testing`

**Usage:**
```
@therion-support invoke THERION_TESTING_SPECIALIST "Add unit tests for module X and check coverage"
```

---

### THERION_DATA_ENGINEER

**Purpose:** Manage data pipelines, datasets, and data-driven workflows used within the Therion ecosystem — including telemetry, profiling data, logs, and experimental results.

**Responsibilities:**
- Build and maintain ETL pipelines that ingest, transform, and store Therion telemetry and logs.
- Structure and document datasets used for benchmarking, profiling, or ML training.
- Ensure data integrity, deduplication, and schema evolution across pipeline stages.
- Produce dashboards or reports from aggregated operational data.
- Collaborate with THERION_TROUBLESHOOTER to surface trends from crash/error data.
- Maintain scripts for data export, import, and anonymization.

**Trigger keywords:** `profiling`, `data`

**Usage:**
```
@therion-support invoke THERION_DATA_ENGINEER "Aggregate crash telemetry from last 30 days and produce a trend report"
```

---

## Workflow Integration

Specialists can be invoked individually or chained together. Common workflows:

| Workflow | Chain |
|---|---|
| Bug triage | THERION_TROUBLESHOOTER → THERION_TESTING_SPECIALIST → THERION_CODE_QUALITY_ENGINEER |
| Feature landing | THERION_CODE_QUALITY_ENGINEER → THERION_DOCUMENTATION_ARCHITECT → THERION_TESTING_SPECIALIST |
| Environment setup | THERION_DEVENV_SPECIALIST → THERION_TESTING_SPECIALIST |
| Post-mortem analysis | THERION_DATA_ENGINEER → THERION_TROUBLESHOOTER → THERION_DOCUMENTATION_ARCHITECT |

## Session Context

When this domain skill is loaded, the following context is available:
- `domain` — `therion-support`
- `workspace_path` — automatically resolved to the Therion repository root
- `specialists` — the six specialists listed above
- `keywords` — the full keyword list for automatic dispatch routing
