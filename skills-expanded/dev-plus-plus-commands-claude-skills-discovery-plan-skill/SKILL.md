---
name: discovery-plan
description: "Run product discovery before development planning using dev++ copied PM skills. Use when the user invokes /discovery-plan or asks to turn an idea, product brief, feature concept, research input, or vague request into PRD structure, user stories, job stories, assumptions, validation experiments, and development-ready handoff."
---

# discovery-plan

Prepare a pre-development discovery package for the idea, feature, product, research brief, or request supplied after the slash command.

Use the copied dev++ product discovery skills as needed:
- `create-prd` for PRD structure and release framing.
- `user-stories`, `job-stories`, and `wwas` for development-ready stories and backlog items.
- `identify-assumptions-new` or `identify-assumptions-existing` for risk mapping.
- `prioritize-assumptions` for deciding what to validate first.
- `brainstorm-experiments-new` or `brainstorm-experiments-existing` for validation plans.
- `opportunity-solution-tree` for outcome, opportunity, solution, and experiment mapping.
- `interview-script` and `summarize-interview` for discovery interviews.
- `test-scenarios` for acceptance-oriented test scenarios.

Rules:
- If the brief is missing or ambiguous, ask concise blocking questions before producing artifacts.
- Classify the work as a new product, existing product feature, research synthesis, or implementation-ready backlog.
- Do not edit files, run tests/builds, install dependencies, start services, or change git state.
- Do not save PRDs or discovery docs unless the user explicitly asks for durable files or approves a write plan.
- Use web research only when current market, competitor, legal, pricing, or other time-sensitive facts are required; cite sources when used.
- Mark assumptions and unknowns clearly. Do not invent research findings.
- Prefer behavior-based validation over opinion-only validation.
- End with a handoff section that can be passed to `/dev-plan`.

Output:
- Discovery classification and blocking questions, if any.
- Problem, users, desired outcome, and non-goals.
- PRD summary or full PRD outline, depending on the detail available.
- User stories, job stories, or WWA backlog items with acceptance criteria.
- Risk assumptions and priority.
- Suggested experiments or interview plan.
- Acceptance test scenarios for the first implementation slice.
- Development handoff: scope, open decisions, contracts to inspect, and recommended next command.
