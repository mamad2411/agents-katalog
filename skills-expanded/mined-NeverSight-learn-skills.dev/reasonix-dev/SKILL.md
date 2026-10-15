---
name: reasonix-dev
description: "Claude Code plans, Reasonix executes. Analyzes the project, generates a detailed implementation plan, then hands it off to Reasonix for execution."
---

# cc-reasonix-dev — Claude Code Plans, Reasonix Executes

> Let Claude Code handle the thinking — project analysis, architecture decisions, and detailed planning. Then hand the plan to Reasonix for cost-effective execution powered by DeepSeek's prefix-cache stability.

## How It Works

```
User Task ──▶ Claude Code (analyze + plan) ──▶ .reasonix-plan.md ──▶ Reasonix (execute)
                                                        │
                                              cleaned up after run
```

1. **Analyze** — Claude Code scans the project: structure, tech stack, code patterns, dependencies
2. **Plan** — Generates a step-by-step implementation plan with file paths, code outlines, and pitfalls
3. **Execute** — Passes the plan to `reasonix run` for DeepSeek-powered execution
4. **Clean** — Removes the temporary plan file

## Usage

```
/reasonix-dev <task description>
```

### Examples

```
/reasonix-dev Add JWT authentication with login and registration endpoints
/reasonix-dev Refactor the database layer from raw SQL to Prisma ORM
/reasonix-dev Add unit tests for all API endpoints using Jest
/reasonix-dev Create a responsive dashboard with charts using Chart.js
/reasonix-dev Migrate the project from JavaScript to TypeScript
```

## Execution Steps

When this skill is invoked, follow these steps:

### Step 1: Project Analysis

Explore the project thoroughly:
- Directory structure and layout
- Tech stack, frameworks, and language versions
- Existing code patterns and naming conventions
- Dependencies (package.json, go.mod, requirements.txt, etc.)
- Configuration files and build system
- Test framework (if any)
- README or documentation

### Step 2: Generate Implementation Plan

Based on the analysis, create a detailed plan containing:
- **Objective**: What needs to be achieved (one sentence)
- **Files Involved**: List of files to create or modify
- **Steps**: Ordered list of operations, each with specific file paths and code locations
- **Code Conventions**: Follow the project's existing style
- **Pitfalls**: Potential issues, edge cases, things to watch out for

### Step 3: Write Plan File

Write the plan to `.reasonix-plan.md` in the project root using this template:

```markdown
# Implementation Plan: {Task Title}

## Objective
{One-sentence description of what to build}

## Project Context
- Tech stack: {framework, language, version}
- Project structure: {key directories}
- Code style: {naming conventions, indentation, etc.}

## Steps

### Step 1: {Step Title}
- File: `{file path}`
- Action: {create / modify / delete}
- Description: {what to do}
- Code notes:
  - {key implementation details}
  - {patterns to follow}

### Step 2: {Step Title}
...

## Pitfalls
- {things that could go wrong}
- {backward compatibility concerns}
- {tests to update}
```

### Step 4: Execute with Reasonix

Run the following command to hand off execution to Reasonix:

```bash
reasonix run --effort high \
  "Read .reasonix-plan.md and follow it exactly. Execute each step in order. Do not deviate from the plan. Task: {user's original task description}"
```

**Optional parameters** (if the user specifies them):
- `--model <id>` — Use a specific DeepSeek model
- `--budget <usd>` — Set a spending cap for this run
- `--transcript <path>` — Save a JSONL transcript of the run

### Step 5: Cleanup

After Reasonix completes, remove the temporary plan file:

```bash
rm -f .reasonix-plan.md
```

## Customization

Users can pass extra parameters in their task description:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `--model` | `/reasonix-dev --model deepseek-pro Add auth` | Use a specific model |
| `--budget` | `/reasonix-dev --budget 0.50 Refactor DB` | Cap spending at $0.50 |
| `--effort` | `/reasonix-dev --effort max Optimize perf` | Maximum reasoning effort |

When these are detected in the task, pass them as flags to `reasonix run`.

## Error Handling

- If `reasonix run` exits with a non-zero code, report the error to the user
- If the plan file is too large (>50KB), split into multiple phases
- If Reasonix seems stuck (no output for >2 minutes), suggest the user check the terminal
- Always clean up `.reasonix-plan.md` even if execution fails

## Notes

- Plans should be detailed enough that Reasonix needs no extra decision-making
- Each step should specify exact file paths and code locations
- For complex tasks, declare dependency order between steps
- Reasonix reads the project code itself — the plan focuses on "what to do", not "what the project is"
- This skill works best for tasks with clear scope; vague tasks like "make it better" should be refined first
