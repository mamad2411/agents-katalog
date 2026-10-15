---
name: tedflow-create-plan
description: Create implementation plans for coding tasks through codebase research, clarification questions, phased scope, and verification criteria. Use when the user asks to create a plan, plan a feature, make an implementation plan, prepare coding work, write a technical plan, break down a task into phases, or convert a Linear ticket into a plan.
---

# Workflow Create Plan

Use this skill to create a complete implementation plan. Do not implement code changes while using this skill.

## Guardrails

- Write plans only to `plans/YYYY-MM-DD-description.md`.
- Do not write plans to `.context/`, `.claude/`, or agent-private directories.
- Do not auto-approve the plan or continue into implementation.
- Stop after presenting the plan for review.
- The final plan must not contain unresolved open questions.

## Inputs

Treat the user's current request as the input.

If the request includes a Linear-style ticket ID such as `ADP-123` or `ENG-456`:

1. Try to fetch the issue using any available Linear MCP server, connector, plugin, or integration.
2. If fetching succeeds, show the title and description, then ask whether the ticket is sufficient or whether the user wants to add context such as relevant directories, constraints, dependencies, or acceptance criteria.
3. If fetching fails or no Linear integration is available, read `references/linear.md` and follow its fallback/setup guidance.

If there is no useful task input, ask for:

1. The task description.
2. Relevant context, constraints, and requirements.
3. Links or paths to related research, plans, or prior implementations.

After asking for ticket confirmation or missing task input, wait for the user's response before researching.

## Project Guidance

Before planning, read the repo's guidance files when present:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `.cursor/rules`
- Any equivalent project documentation that describes architecture, tests, build commands, or conventions.

Use the current agent's native guidance first when multiple files overlap.

## Portable Interaction Pattern

For discrete choices, prefer the agent's structured question capability when available. If none exists, ask in chat with numbered options:

```markdown
**Decision Needed: [Header]**
[Question]

1. [Recommended option] - [tradeoff]
2. [Alternative] - [tradeoff]
3. [Alternative] - [tradeoff]

Reply with a number or describe another preference.
```

Use open-ended text questions only when the answer cannot reasonably be expressed as 2-4 choices.

Track progress with the agent's native todo/plan mechanism. If none exists, maintain a short visible Markdown checklist.

## Research Workflow

1. Read all user-mentioned files fully before delegation or synthesis.
2. Review project guidance and identify relevant directories.
3. Research the codebase with `rg`, `fd`, `ast-grep`, file reads, and git commands as appropriate.
4. Use native subagents only when available and allowed. Keep delegated research narrow, read-only, and focused on file:line findings.
5. Verify delegated findings in the main context before using them in the plan.
6. Cross-check requirements against actual code and identify assumptions, mismatches, edge cases, and scope boundaries.
7. Present the current understanding and ask clarifying questions before writing the plan.

If the user corrects your understanding, verify the correction against code or provided source material before proceeding.

## Planning Rules

- Minimize phases. Each phase should be a meaningful, testable milestone.
- Combine tightly coupled layers into one phase. For example, schema, models, store methods, service logic, API endpoints, and unit tests often belong in one backend phase.
- Put unit tests in the same phase as the code they test.
- Use a separate integration or E2E phase only when it spans multiple earlier phases.
- Separate automated verification from manual verification.
- Include explicit out-of-scope items to prevent scope creep.
- Include file paths and file:line references where they are known.
- Make success criteria measurable and actionable.

## Plan Template

When ready to write the final plan, read `references/plan-template.md` and follow that structure.

## Completion

After writing the plan:

1. Tell the user the plan path.
2. Summarize the major phases.
3. Ask them to review the plan.
4. Do not start implementation.
