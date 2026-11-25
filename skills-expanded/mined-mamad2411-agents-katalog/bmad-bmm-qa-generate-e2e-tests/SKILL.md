---
name: bmad-bmm-qa-generate-e2e-tests
description: >-
  Use this skill to generate automated API and end-to-end tests for already-
  implemented features using the project's existing test framework. Invoke when
  the user says "create QA automated tests for [feature]", "generate e2e
  tests", or when implemented code needs verified test coverage. The skill
  detects the existing test framework, identifies the features or components to
  test, generates readable and maintainable test files focusing on happy paths
  and critical error cases, then executes the tests and fixes any failures
  before producing a coverage summary document. Input is a feature name,
  component path, or directory. Output is test files and a coverage summary.
  Unlike bmad-bmm-code-review (which validates story acceptance criteria),
  this skill is purely about generating test code. Do not use on features that
  do not yet exist — implement first with bmad-bmm-dev-story or bmad-bmm-quick-
  dev, then generate tests. For advanced test strategy, use the TEA module.
argument-hint: "Provide a feature name, component path, or directory to scan for testable features."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# QA Generate E2E Tests

Generate end-to-end automated tests for existing features.

## Outcome

Automated API and E2E tests generated for implemented code, verified passing, with a coverage summary document.

## Your Role

QA automation engineer. You generate tests ONLY — no code review or story validation (use Code Review for that). Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- Generate tests ONLY — no code review or story validation.
- Use whatever test framework the project already has.
- Focus on happy path + critical error cases.
- Write readable, maintainable tests.
- Run tests to verify they pass.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `implementation_artifacts`, etc.).
2. Resolve:
   - `date` as system-generated current datetime
   - `test_dir` = project's test directory (discover from project structure)
   - `default_output_file` = `{implementation_artifacts}/tests/test-summary.md`
   - `project_context` = `**/project-context.md` (load if exists)

## Execution Order

Follow these steps in order.

1. [Detect Test Framework](./steps/detect-test-framework.md) — Identify the project's existing test framework and patterns
2. [Identify Features](./steps/identify-features.md) — Determine which features or components need automated tests
3. [Generate Tests](./steps/generate-tests.md) — Generate API and/or E2E test files for identified features
4. [Run Tests and Create Summary](./steps/run-and-summarize.md) — Execute tests, fix failures, and produce a coverage summary

## Halt Conditions

- HALT if no test framework can be identified or agreed upon.
- HALT if user cannot confirm which features to test.

## Quality Guidelines

**Do:**
- Use standard test framework APIs
- Focus on happy path + critical errors
- Write readable, maintainable tests
- Run tests to verify they pass

**Avoid:**
- Complex fixture composition
- Over-engineering
- Unnecessary abstractions

**For Advanced Features:**
If the project needs risk-based test strategy, test design planning, quality gates, NFR assessment, comprehensive coverage analysis, or advanced testing patterns — recommend installing the Test Architect (TEA) module.

## Data Files

- [./data/checklist.md](./data/checklist.md) — Validation checklist for generated tests

## External Skill Dependencies

This skill operates independently and does not invoke other BMAD skills at runtime. It is typically run after `bmad-bmm-dev-story` or `bmad-bmm-quick-dev` completes implementation, and before `bmad-bmm-code-review` validates the story — but those skills are not called from within this skill.

## When to Use

Use this skill when:
- The user says "create qa automated tests for [feature]" or "generate e2e tests"
- Existing features need automated API and E2E tests generated and verified passing
- The user provides a feature name, component path, or directory to scan for testable features

## Boundaries

This skill should NOT:
- Generate tests for features that do not yet exist — implement the feature first using `bmad-bmm-dev-story` or `bmad-bmm-quick-dev`, then generate tests
- Perform code review or story validation — it generates test code only; use `bmad-bmm-code-review` to validate story acceptance criteria against implementation
- Install or introduce a new test framework — it must use whatever test framework is already present in the project
- Produce tests with complex fixture composition or unnecessary abstractions — keep tests readable, linear, and maintainable
- Recommend advanced test strategy (risk-based testing, quality gates, NFR assessment) — direct users to the TEA module for that

