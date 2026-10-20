---
name: implement-features
description: "Build new features from specifications and requirements, ensuring production-ready, maintainable, and well-integrated code using GitHub and Jira."
---

# Implement Features

## Purpose

Build new features from specifications and requirements, ensuring production-ready, maintainable, and well-integrated code using GitHub and Jira.

This skill provides operational guidance for Implement Features, including tool usage patterns, workflows, and quality expectations aligned with Syncolab skill standards.

## When to Use

- Use when the user needs help with Implement Features.
- When integrations for this domain are available and the task matches the workflows below.

## When NOT to Use

- When the task is unrelated to Implement Features or covered by a more specific skill.
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

1. Confirm the request maps to Implement Features and required tools are available.
2. Gather identifiers and scope (project, channel, repo, date range, etc.).
3. Follow the domain guidance below; prefer list/search before get/update when applicable.
4. Execute tool calls using schemas from the integration; never invent tool output.
5. Summarize results and offer logical follow-ups.

# Skill: Implement Feature

## Description
Build new features from specifications and requirements, ensuring production-ready, maintainable, and well-integrated code using GitHub and Jira.

---

## Purpose
This skill is responsible for translating product requirements into working software. It ensures that new features are implemented correctly, aligned with system architecture, and integrated smoothly into the existing codebase while maintaining high standards of quality, readability, and reliability.

---

## Responsibilities

- Understand feature requirements from Jira tickets and related documentation
- Design and implement clean, maintainable, and scalable solutions
- Align with existing architecture, coding standards, and patterns
- Collaborate implicitly with other agents (e.g., QA, Docs, Review)
- Ensure code is testable and supports downstream validation
- Keep Jira updated with progress, assumptions, and outcomes

---

## Workflow

### 1. Understand the Task (Jira)
- Read the Jira ticket thoroughly
- Identify:
  - Feature scope
  - Acceptance criteria
  - Constraints and dependencies
- Clarify ambiguities by documenting assumptions in Jira
- Break down the feature into logical implementation steps if needed

---

### 2. Explore the Codebase (GitHub)
- Locate relevant modules, services, and components
- Identify:
  - Existing patterns and conventions
  - Similar implementations
  - Integration points (APIs, DB, services, etc.)
- Avoid introducing new patterns unless necessary

---

### 3. Design the Implementation
- Define:
  - Data flow and structure
  - Interfaces and contracts
  - Required changes across components
- Ensure:
  - Consistency with architecture
  - Minimal coupling
  - Clear separation of concerns

---

### 4. Implement the Feature
- Write clean, readable, and maintainable code
- Follow:
  - Project conventions (naming, structure, formatting)
  - Existing abstractions and utilities
- Ensure:
  - Backward compatibility (unless explicitly not required)
  - Proper error handling and edge case coverage
- Avoid unnecessary complexity or premature optimization

---

### 5. Integrate with System Components
- Ensure proper integration with:
  - APIs
  - Databases
  - External services
  - Internal modules
- Validate that the feature works within real system flows, not just in isolation

---

### 6. Enable Testability
- Structure code so it can be easily tested by the testing agent
- If tests are missing or required:
  - Coordinate implicitly by leaving clear structure and boundaries
- Do not tightly couple logic in ways that block testing

---

### 7. Validate Implementation
- Review your own changes:
  - Does the implementation fully satisfy acceptance criteria?
  - Are edge cases handled?
  - Is the code understandable by others?
- Ensure no unintended side effects were introduced

---

### 8. Update Jira
- Provide a clear summary including:
  - What was implemented
  - Key design decisions
  - Assumptions made
  - Any known limitations or follow-ups needed
- Mark the task appropriately (e.g., ready for review/testing)

---

## GitHub Usage Guidelines

- Read before writing: always understand existing code first
- Prefer modifying existing structures over creating new ones
- Keep commits focused and meaningful
- Maintain consistency with repository standards
- Avoid large, unrelated changes in a single implementation

---

## Jira Usage Guidelines

- Treat Jira as the source of truth for requirements
- Document:
  - Assumptions
  - Ambiguities
  - Decisions
  - Progress
- Ensure the ticket reflects the true implementation status

---

## Best Practices

- Think in systems, not just functions
- Optimize for clarity over cleverness
- Build for maintainability and future extension
- Respect boundaries between components
- Minimize hidden side effects
- Prefer explicitness over implicit behavior

---

## Anti-Patterns to Avoid

- Implementing without fully understanding requirements
- Ignoring existing patterns or duplicating logic
- Over-engineering simple features
- Tight coupling between unrelated components
- Skipping edge cases or error handling
- Leaving Jira outdated or incomplete

---

## Output Expectations

- Production-ready feature implementation
- Clean, maintainable, and consistent code
- Proper integration with the system
- Clear Jira update with implementation summary
- Code ready for testing and review

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Execute workflows, verify outputs, report errors. |
| Read-only | Inspect and plan; provide exact commands or dispatch request for writes. |
| No integration | State limitation; do not fabricate API results. |

### Related tool sets

- `vscode`
- `github`



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

- Legacy content migrated from `skills/old_skills.json` (`implement-features`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
