---
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
description: Investigate a reported bug, find root cause, and create a GitHub issue with a TDD fix plan
argument-hint: [description of the bug or problem]
model: opus
---

# Purpose

Triage a reported problem by exploring the codebase to find its root cause, then create a GitHub issue with a TDD-based fix plan. This is a hands-off workflow — investigate autonomously and minimize questions to the user. Follow the Instructions and Workflow below.

## Variables

PROBLEM_DESCRIPTION: $ARGUMENTS

## Instructions

- If PROBLEM_DESCRIPTION is empty, ask ONE question: "What's the problem you're seeing?" Then proceed immediately — no follow-up questions.
- Investigate deeply and autonomously. Do not ask clarifying questions before exploring.
- Trace the full code path: where the bug manifests, what's involved, why it fails, what related code exists.
- Check recent git history on affected files to spot regressions.
- Look at existing tests to understand what's covered and what's missing.
- Find similar patterns elsewhere in the codebase that work correctly for comparison.
- Design the fix as vertical RED-GREEN TDD cycles — one test at a time, not all tests first.
- Tests must verify behavior through public interfaces, not implementation details.
- Tests must assert on observable outcomes (API responses, UI state, user-visible effects), not internal state.
- Describe modules, behaviors, and contracts in the issue — NOT specific file paths, line numbers, or implementation details that couple to current code layout.
- The issue should remain useful even after major refactors. A good suggestion reads like a spec; a bad one reads like a diff.
- Create the GitHub issue directly using `gh issue create` — do NOT ask user to review before creating.

## Workflow

1. Parse the PROBLEM_DESCRIPTION. If empty, ask the user for a brief description, then proceed.
2. Explore the codebase to understand the problem:
   - Search for related source files and their dependencies
   - Read relevant code paths and trace the flow
   - Check existing tests for coverage gaps
   - Run `git log` on affected files to spot recent changes
   - Examine error handling in the code path
   - Find similar working patterns for comparison
3. Identify the root cause — distinguish between regression, missing feature, or design flaw.
4. Determine the minimal fix approach: which modules/interfaces are affected and what behaviors need verification.
5. Design a TDD fix plan as ordered RED-GREEN cycles, each a vertical slice:
   - RED: A specific test capturing broken/missing behavior
   - GREEN: The minimal code change to make that test pass
   - Include a final REFACTOR step if cleanup is needed after all tests pass.
6. Create a GitHub issue using `gh issue create` with this structure:
   - **Problem**: Actual behavior, expected behavior, reproduction steps
   - **Root Cause Analysis**: Code path involved, why it fails, contributing factors (described as modules/behaviors/contracts, not file paths)
   - **TDD Fix Plan**: Numbered RED-GREEN cycles
   - **Acceptance Criteria**: Checkbox list including "All new tests pass" and "Existing tests still pass"
7. Print the issue URL and a one-line summary of the root cause.

## Report

Return the GitHub issue URL and a one-line summary of the root cause found during investigation.