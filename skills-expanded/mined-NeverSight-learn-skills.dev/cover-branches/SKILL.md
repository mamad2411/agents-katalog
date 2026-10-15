---
name: cover-branches
description: >
  Find branch coverage gaps in changed code and fix them by writing missing tests.
  Two analysis layers: Source ↔ Test (logic branches vs test cases) and Spec ↔ Test
  (requirement scenarios vs test cases, when a spec file is provided).
  Use when verifying test completeness after implementing a feature or fixing a bug,
  when auditing whether tests match a spec, or when suspecting untested branches.
---

# cover-branches: Branch Coverage Gap Analysis & Fix

Find branch coverage gaps in changed code and write missing tests to fill them.

## Phase 1: Identify Changes

Run `git diff` (or `git diff HEAD` if there are staged changes) to identify changed source and test files.

If no git changes exist, fall back to files the user mentioned or edited earlier in the conversation.

## Phase 2: Launch Gap Analysis Agents in Parallel

Use the Agent tool to launch agents concurrently. Pass each agent the full diff for complete context.

### Agent 1: Source ↔ Test Branch Coverage (always launched)

For each changed source file:

1. Read the source file and identify all logic branches — conditional branches, error handling, early returns, default/fallback values, and any other branching constructs relevant to the file's language.
2. Find the corresponding test file(s) by inferring the mapping from project conventions (naming, directory structure, imports). If no test file exists, report that as a gap.
3. For each branch, determine if a test exercises that path.
4. Report gaps in natural language: which branches lack test coverage and what test scenarios are missing.

### Agent 2: Spec ↔ Test Scenario Coverage (launched only when user provides a spec file)

1. Read the spec file provided by the user.
2. Extract all testable scenarios: functional requirements, boundary conditions, error handling, edge cases, acceptance criteria, user stories.
3. Find the corresponding test file(s).
4. For each scenario, determine: **covered** or **gap**.
5. Report gaps in natural language: which scenarios lack test coverage and what is missing.

## Phase 3: Fix Gaps

1. Wait for all agents to complete.
2. Merge findings from both agents, avoiding obviously redundant test cases.
3. Write all missing test cases directly. Follow existing test file conventions (framework, naming, structure). If no test file exists, create one following project conventions.
4. When a spec contains contradictions, or when the correct test behavior cannot be inferred from the source code, ask the user before writing the test.
5. Run the tests to verify they pass. Infer the test command from project configuration (`package.json`, `Makefile`, `pom.xml`, etc.); if unable to infer, ask the user.
6. Summarize what was added, or confirm coverage is already complete.
7. If no spec file was provided, remind the user they can re-run with a spec file path for scenario coverage analysis. Otherwise, confirm both coverage layers have been addressed.
