---
name: bc-issue-to-plan
description: Create a detailed implementation plan from a GitHub issue, exploring the codebase to identify specific files and changes needed. Use when user wants to plan an issue, create an implementation plan, start working on a ticket, convert an issue to a plan, or mentions "plan this issue".
argument-hint: "<issue-number-or-url>"
---

# Issue to Plan

Create a concrete implementation plan from a GitHub issue, saved as a Markdown file in `./plans/`.

This skill bridges the gap between a GitHub issue (the "what") and writing code (the "how"). The output is a plan detailed enough that an agent or developer can begin implementation without further design work.

## Process

### 1. Fetch the issue

Accept a GitHub issue number or URL as input. Fetch the issue with:

```
gh issue view <number> --comments
```

Extract:

- Title and body
- Acceptance criteria (if present)
- Labels and assignees
- Any linked issues or PRs

If the issue body references a parent PRD (look for patterns like `#<number>`, "Parent PRD", or links to other issues), fetch that too for broader context. The parent PRD provides architectural decisions and user stories that inform the plan.

### 2. Explore the codebase

Investigate the codebase to understand where changes need to happen. This is the most important step — the plan's value comes from grounding it in the actual code.

<exploration-checklist>
- Identify the tech stack, frameworks, and key dependencies
- Trace the code paths relevant to this issue end-to-end
- Find existing patterns for the type of change required (e.g., if adding an API endpoint, find an existing endpoint to use as a reference)
- Locate test infrastructure and conventions (test runner, test file locations, mocking patterns)
- Check for relevant configuration files, environment variables, or feature flags
- Note any shared utilities, types, or abstractions that should be reused
</exploration-checklist>

Use the Agent tool for broad exploration. Use Grep and Glob for targeted searches. Read specific files to understand implementation details.

### 3. Identify architectural decisions

Based on the issue and codebase exploration, surface any decisions that need to be made before implementation. Categorize each as:

- **Resolved**: Decisions already answered by the issue, the parent PRD, or codebase conventions. State the decision and its source.
- **Recommended**: Decisions not yet made where one option is clearly better. State the recommendation and reasoning.
- **Open**: Decisions that require user input. These block the plan.

### 4. Quiz the user

Present a summary of findings:

1. Restate the issue's goal in one sentence.
2. List the files and modules that will be touched.
3. Present any **Recommended** or **Open** architectural decisions for confirmation.
4. Propose the testing approach.

Ask the user to confirm or adjust. If there are **Open** decisions, these must be resolved before proceeding. Iterate until all decisions are resolved and the user approves the approach.

### 5. Write the plan

Create the plan file at `./plans/<issue-slug>.md` using the template below. The slug is derived from the issue title: lowercase, kebab-case, prefixed with the issue number (e.g., `042-add-user-auth.md`).

If the `./plans/` directory does not exist, create it.

<plan-template>
# Plan: <Issue Title>

> GitHub Issue: #<number>
> Parent PRD: #<number> (if applicable)
> Created: <YYYY-MM-DD>

## Goal

One to two sentences restating what this issue achieves from the user's perspective. Not a copy of the issue body — a distillation.

## Architectural Decisions

Decisions made during planning that inform the implementation. Each entry includes the decision, the reasoning, and the source (issue, PRD, codebase convention, or planning discussion).

- **Decision 1**: [What was decided]. [Why]. Source: [where this was decided].
- **Decision 2**: ...

## Implementation Steps

Ordered list of steps to implement this issue. Each step should be independently committable where possible. For each step:

### Step N: <Short description>

**Files to modify:**

- `path/to/file.ts` — <what changes and why>

**Files to create:**

- `path/to/new-file.ts` — <purpose of this file>

**Details:**
Describe what to implement in this step. Reference existing patterns in the codebase by file path. Be specific about function signatures, data shapes, or integration points where ambiguity would slow implementation.

**Acceptance signal:**
How to verify this step is complete (e.g., "test X passes", "endpoint returns expected response", "component renders correctly").

## Testing Strategy

### Unit Tests

- What to test and where the test files go
- Reference existing test patterns in the codebase

### Integration Tests

- End-to-end verification approach
- Key scenarios to cover

### Manual Verification

- Steps to manually verify the implementation works

## Acceptance Criteria

Checklist pulled from the issue (or derived from it if the issue lacks explicit criteria). Each item should be verifiable.

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Reference Files

Key files consulted during planning. Useful for the implementer to review before starting.

- `path/to/file.ts` — <why this file is relevant>
- `path/to/pattern.ts` — <pattern to follow>
  </plan-template>

### 6. Confirm output

After writing the plan, report:

- The path to the plan file
- A one-line summary of the approach
- The number of implementation steps
- Any risks or areas of uncertainty worth noting

Do NOT modify the original GitHub issue.
