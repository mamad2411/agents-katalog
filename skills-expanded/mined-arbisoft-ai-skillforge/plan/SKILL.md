---
name: plan
description: "Skill that instructs an agent to turn a research.md file into a test-driven, task-by-task implementation plan — structured so any downstream LLM agent can pick up individual tasks and execute them independently."
---

# Plan Skill

When this skill is active, follow this process to produce the implementation plan.

## Step 1 — Read and Internalize the Research

Read the research file provided as input in full before doing anything else:
- Understand the user's original query and intent
- Note every file listed in the Relevant Files section
- Understand the impact surface — what must change and what is affected
- Absorb the patterns, conventions, and constraints — the plan must respect all of them

Do not begin planning until you have fully read the research file.

## Step 2 — Identify the Task Breakdown

Decompose the implementation into the smallest independently executable tasks possible:
- Each task must have a single, clear responsibility
- A downstream agent must be able to pick up a task and complete it without reading any other task
- Order tasks so that no task depends on a later task — dependencies flow downward only
- Group related changes (e.g. model + serializer + view) only if they cannot be meaningfully separated

## Step 3 — Apply Test-Driven Structure to Every Task

For each task, define the tests before the implementation:
- Identify what behavior needs to be verified
- Specify the test file, test class or function name, and what each test asserts
- Tests must cover the happy path, at least one edge case, and any error conditions relevant to the task
- The implementation steps follow only after the test specification

## Step 4 — Make Every Task Self-Contained

Each task must include enough context for a downstream agent to execute it with no prior knowledge:
- Reference the exact files to modify or create, with paths relative to the project root
- State the pattern or convention to follow, with a concrete example from the codebase if applicable
- List any other tasks this task depends on
- Do not use vague instructions like "update accordingly" or "handle as needed" — be explicit

## Self-Check Before Output

Before writing the plan file, verify:
- [ ] Every task is independently executable — no implicit cross-task knowledge required
- [ ] Tests are specified before implementation steps in every task
- [ ] File paths are exact — no approximations
- [ ] The ordering is correct — no task requires a later task to be done first
- [ ] The plan covers the full impact surface from the research file — nothing is skipped
