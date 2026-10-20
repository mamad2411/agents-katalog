---
name: write-agent-documentation
description: "Create, maintain, and improve repository documentation that helps coding agents understand the project, follow engineering standards, make safe changes, and work consistently across tools such as Claude Code, Cursor, GitHub Copilot, Codex, and other AI coding agents."
---

# Write Agent Documentation

## Purpose

Create, maintain, and improve repository documentation that helps coding agents understand the project, follow engineering standards, make safe changes, and work consistently across tools such as Claude Code, Cursor, GitHub Copilot, Codex, and other AI coding agents.

This skill provides operational guidance for Write Agent Documentation, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with Write Agent Documentation.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is unrelated to Write Agent Documentation or covered by a more specific skill.
- When required integrations or credentials are unavailable.

## Expected Outcome

- Correct use of domain tools with verified results (not fabricated).
- Clear summary of actions taken, data returned, and recommended next steps.
- Errors and missing permissions reported explicitly.

## Inputs to Gather

- User goal, constraints, and any identifiers (URLs, IDs, project keys).
- Available tool sets and connection status.
- Relevant context from related systems before destructive writes.

## Workflow

1. Confirm the request maps to Write Agent Documentation and required tools are available.
2. Gather identifiers and scope (project, channel, repo, date range, etc.).
3. Follow the domain guidance below; prefer list/search before get/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

# Skill: Write Agent Documentation

## Description
Create, maintain, and improve repository documentation that helps coding agents understand the project, follow engineering standards, make safe changes, and work consistently across tools such as Claude Code, Cursor, GitHub Copilot, Codex, and other AI coding agents.

---

## Purpose
This skill ensures that every repository contains a clear, aligned, and practical documentation layer for AI coding agents.

The goal is not only to document the codebase for humans, but to create a reliable operating manual for agents: what the system does, how the code is structured, how changes should be made, how tests should be run, which decisions must be respected, and which patterns should or should not be followed.

Well-written agent documentation should reduce hallucinations, prevent inconsistent implementations, improve task execution quality, and make future agents more effective from the first interaction.

---

## Responsibilities

- Create and maintain agent-facing documentation files for repositories
- Translate architecture, conventions, and engineering decisions into actionable instructions
- Keep documentation compatible with multiple coding agents and IDEs
- Document development workflows, validation commands, testing expectations, and review standards
- Capture project structure, coding patterns, design decisions, and known constraints
- Ensure documentation is concise enough to be useful in an agent context window
- Keep documentation accurate as the codebase evolves
- Use Jira to understand documentation goals, gaps, and requested improvements
- Use GitHub to inspect the actual repository before writing or updating documentation

---

## Supported Documentation Targets

This skill should support any agent documentation system, including but not limited to:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/*.mdc`
- `.github/copilot-instructions.md`
- `README.md` agent-specific sections
- `docs/ai/*.md`
- `docs/architecture/*.md`
- `docs/decisions/*.md`
- `docs/development/*.md`
- Repository-specific onboarding or engineering guides

When possible, prefer a vendor-neutral source of truth such as `AGENTS.md` or `docs/ai/agent-guide.md`, and adapt tool-specific files from it.

---

## Core Principle

Agent documentation must be:

- **Accurate** — based on the actual repository, not assumptions
- **Actionable** — written as instructions an agent can follow
- **Specific** — tailored to the repository, not generic boilerplate
- **Concise** — focused on what agents need during implementation
- **Structured** — easy to scan, reference, and update
- **Safe** — avoids secrets, credentials, private tokens, or sensitive data
- **Maintainable** — updated when architecture, commands, or conventions change

---

## Workflow

### 1. Understand the Documentation Request

Use Jira to identify:

- The requested documentation scope
- The target audience:
  - Coding agents
  - Human developers
  - Both
- The target agent environment:
  - Claude Code
  - Cursor
  - GitHub Copilot
  - Codex
  - Generic agent setup
- The repository areas that need documentation
- Any known pain points:
  - Agents making wrong assumptions
  - Agents ignoring architecture
  - Agents writing inconsistent code
  - Agents failing to run correct tests
  - Agents misunderstanding project structure

If Jira is unclear, infer the most useful documentation improvement from the repository structure and document assumptions.

---

### 2. Inspect the Repository Before Writing

Use GitHub to inspect the actual codebase.

Review:

- Repository structure
- Existing documentation
- Build and run commands
- Test commands
- Linting and formatting setup
- Package or dependency files
- CI configuration
- Important modules and boundaries
- Existing architecture or decision documents
- Naming conventions and style patterns
- Existing agent instruction files

Do not write generic instructions without first understanding the repository.

---

### 3. Identify the Agent Documentation Architecture

Decide which documentation files should exist and what each one should own.

A strong structure may include:

```text
AGENTS.md
docs/
  ai/
    agent-guide.md
    agent-workflows.md
    agent-review-checklist.md
  architecture/
    overview.md
    module-boundaries.md
    decisions.md
  development/
    setup.md
    testing.md
    coding-standards.md
.cursor/
  rules/
    project-rules.mdc
.github/
  copilot-instructions.md
CLAUDE.md
```

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `github`
- `jira`
- `google-docs`
- `notion`
- `docs-as-code`



## Review / Decision / Execution Criteria

- Prefer smallest safe change; confirm destructive actions with the user.
- Use evidence from tool responses; cite IDs and links when present.
- Match integration-specific conventions (JQL, RFC3339, A1 notation, etc.).

## Output Format

Report:

1. What was requested and what was done.
2. Key results (tables or bullets).
3. Errors, blockers, or missing permissions.
4. Suggested next steps.

## Quality Bar

- Specific, actionable, and grounded in tool output.
- Concise unless the user asked for detail.
- Respect rate limits, pagination, and API semantics.

## Safety and Boundaries

- Do not commit secrets, tokens, or PII into skills or user-visible logs.
- Do not fabricate validation, send, or write confirmations.
- Confirm destructive operations (delete, destroy, mass update) when appropriate.

## Escalation / Dispatch Rules

- If the task spans multiple domains, use or suggest related skills via `relationships.skills`.
- If write access is required but unavailable, dispatch or ask the user to enable tools.

## References

- Legacy content migrated from `skills/old_skills.json` (`write-agent-documentation`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
