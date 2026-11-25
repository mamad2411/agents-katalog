---
name: ai-toolbox-tdd-planning
description: Strict TDD-focused implementation planning. Creates plans with Red-Green-Commit/Rollback cycles for each step.
---

# TDD Planning Skill

This skill provides a disciplined TDD workflow where no implementation code is written without a failing test first.

## Working Agreement
- **RED**: Write a failing test (must fail for the right reason).
- **GREEN**: Write minimal code to make the test pass (nothing more).
- **COMMIT/ROLLBACK**: If green, commit. If stuck, rollback to last green state.
- Always use `ask_user` for strategy, design decisions, and approvals.

## Process Workflow

### 1. Context Gathering & Test Infrastructure Analysis
- Use `codebase_investigator` to map the task and understand dependencies.
- Read existing test patterns (e.g., in `tests/` or `__tests__/`).
- Use `read_file` to understand current implementation.
- Identify the test command (e.g., `npm test`, `pytest`).

### 2. Test Strategy Design
- Break the implementation into small, testable units.
- Design a progression from simple (happy path) to complex (edge cases, error handling).

### 3. Plan Structure Development
- Create an implementation plan consisting of TDD cycles.
- Each cycle MUST specify the **RED** (test code, failure message) and **GREEN** (minimal code) phases.
- Use the provided [template.md](references/template.md).

## Constraints
- **NO** implementation code without a failing test first.
- **MINIMAL** implementation: only what is needed to pass the current test.
- **CLEAR** rollback points: commit frequently.
