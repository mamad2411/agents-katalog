# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

Since this is a methodology/documentation repository without traditional build tools, use these scripts for development:

```bash
# Feature development workflow (requires feature branch format: 001-feature-name)
./scripts/setup-plan.sh            # Initialize feature planning structure
./scripts/get-feature-paths.sh     # Get paths for current feature
./scripts/create-new-feature.sh    # Create new feature branch and structure
./scripts/update-agent-context.sh  # Update agent context for parallel work
./scripts/check-task-prerequisites.sh  # Verify task prerequisites
```

## Architecture Overview

This repository implements an **Agentic Coding Framework** - a comprehensive methodology for AI-assisted software development with three key layers:

### 1. Constitutional Layer (`/memory/constitution.md`)
Defines immutable principles governing all development:
- **Component-First Development**: Every feature as self-contained modules
- **Interface Standardization**: Text-based I/O protocols
- **Test-First (TDD)**: Mandatory test-driven development cycle
- **Integration Verification**: Contract testing at boundaries
- **Observability**: Structured logging and debugging
- **Versioning**: Semantic versioning with migration paths
- **Simplicity**: YAGNI principles, composition over inheritance

### 2. Agent System (`/agents/`, `/SUBAGENT.md`)
Specialized agents act as "context firewalls" - doing heavy work and returning concise summaries:
- **test-runner**: Executes tests, analyzes failures, returns actionable insights
- **code-analyzer**: Deep-dive bug hunting across files without context pollution
- **file-analyzer**: Summarizes verbose files (80-90% size reduction)
- **parallel-worker**: Coordinates multiple parallel work streams

Agents preserve main thread context by processing large amounts of data internally and returning only essential information.

### 3. Feature Development System (`/scripts/`, `/specs/`)
Feature branches follow `NNN-feature-name` format with structured specs:
- `spec.md`: Feature specification
- `plan.md`: Implementation plan
- `tasks.md`: Granular task breakdown
- `research.md`: Technical research
- `contracts/`: API contracts and interfaces

## Critical Rules from AGENTS.md

1. **Before ANY code change**: Read entire files end-to-end, trace all call paths
2. **Small changes only**: Keep commits, PRs, and tasks minimal
3. **Document assumptions**: Record in Issues/PRs/ADRs
4. **Security first**: No secrets in code/logs, validate all inputs
5. **Compare approaches**: Evaluate ≥2 options before deciding

### Code Limits (enforce via refactoring)
- Files ≤ 300 LOC
- Functions ≤ 50 LOC  
- Parameters ≤ 5
- Cyclomatic complexity ≤ 10

### Commit Convention
Follow `@commitlint/config-conventional`:
```
<type>[optional scope]: <description>
```
Types: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`

## Code Review Focus (REVIEW.md)

When reviewing code, prioritize:
1. Security vulnerabilities and input validation
2. Test coverage and edge cases
3. Performance bottlenecks
4. Clean code principles
5. Documentation completeness

## Working with Agents

Use agents proactively for context-heavy tasks:
```bash
# Instead of reading 10 files in main thread:
# Use code-analyzer agent to search and return summary

# Instead of dumping test output to console:
# Use test-runner agent to analyze and return insights

# For parallel work:
# Use parallel-worker to coordinate multiple streams
```
@STANDARDS.md
@TESTING.md
@TDD.md
@memory/constitution.md
@SUBAGENT.md
