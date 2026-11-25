---
name: product-requirements
description: Use when creating, rewriting, reviewing, or decomposing product requirements, PRDs, feature specifications, user stories, acceptance criteria, release scope, product behavior, edge cases, non-goals, dependencies, rollout requirements, or product handoff material. Prefer this Skill when the task needs implementation-ready requirement clarity rather than a high-level solution brief, marketing copy, or engineering design.
meta:
  version: 1
  display_name: 产品需求
---

# Product Requirements

## Purpose

Turn a product idea, user problem, solution direction, meeting notes, research, or existing draft into clear product requirements that can be reviewed, estimated, implemented, tested, and shipped.

This Skill owns requirement clarity, scope boundaries, user value, behavior definition, acceptance criteria, edge cases, dependencies, and handoff quality. It does not own final product approval, engineering design, implementation, or release execution.

## Use When

Use for:

- PRDs, feature specs, requirement docs, user stories, acceptance criteria, release scope, and product handoff notes;
- turning a `solution-brief` into implementation-ready product requirements;
- decomposing a vague feature request into users, jobs, scenarios, behavior, data, permissions, states, errors, and edge cases;
- reviewing requirements for ambiguity, missing acceptance criteria, hidden dependencies, metric gaps, or scope creep;
- aligning product, engineering, design, QA, operations, sales, support, or customers on what should be built.

Use `solution-brief` when the user still needs to choose or explain a proposed solution. Use `code-reading-and-change` for implementation details and code changes. Use `writing-and-editing` when the central task is prose polish rather than requirement substance.

## Do Not Use When

Do not use for:

- marketing copy, sales proposals, customer announcements, or internal status updates;
- final engineering architecture, database schema, API contract, migration plan, or test implementation;
- legal, compliance, security, privacy, or financial approval;
- project planning alone where the user only needs task ordering; that belongs in the plan workflow rather than a separate Skill.

## Material Gate

Before writing requirements, identify:

- product objective, target user, user problem, trigger, desired outcome, and business context;
- source material: solution brief, ticket, research, meeting notes, customer request, incident, existing PRD, design, prototype, or code behavior;
- scope: in scope, out of scope, non-goals, assumptions, constraints, dependencies, rollout boundary, and owner;
- behavior surface: entry points, roles, permissions, data, states, error paths, notifications, audit needs, and integrations;
- success criteria: user outcome, business metric, quality bar, acceptance tests, release checks, and measurement method;
- unknowns: missing user evidence, policy/legal/security review, technical feasibility, analytics, migration, or operational ownership.

If facts are missing, write a constrained requirement draft and mark unresolved facts `待确认`. Do not invent customer commitments, metrics, dates, owners, legal approvals, technical feasibility, or implementation estimates.

## Workflow

1. Classify the requirement mode: new feature, enhancement, workflow change, platform capability, admin operation, integration, migration, experiment, bug-derived improvement, or deprecation.
2. Restate the user problem and intended outcome before listing features.
3. Separate source-backed facts, product decisions, assumptions, open questions, and implementation suggestions.
4. Define users, personas, roles, permissions, entry points, and primary scenarios.
5. Define expected behavior using `references/requirement-rules.md`: happy path, alternate flows, empty states, loading, errors, retries, validation, permissions, audit, notifications, and data lifecycle.
6. Write acceptance criteria that are observable and testable. Avoid subjective criteria such as "easy", "fast", or "better" unless they are tied to a measurable threshold.
7. State non-goals and out-of-scope items so implementation does not expand silently.
8. Identify dependencies, rollout, migration, analytics, operations, support, privacy, security, compliance, and documentation impacts when relevant.
9. Use `references/review-checklist.md` when reviewing or hardening an existing PRD.
10. Return the user's requested format without forcing a fixed PRD template.

## Checks

- The user problem, target user, desired outcome, and success criteria are visible.
- Requirements describe behavior, not only intent.
- Acceptance criteria are testable and tied to concrete states or outcomes.
- Edge cases, permissions, error states, data changes, notifications, dependencies, and rollout needs are considered when relevant.
- Non-goals and out-of-scope work are explicit.
- Unknowns are marked `待确认` rather than hidden.
- Engineering design, legal/compliance approval, and final release approval are not implied.

## Outputs

Return the form the user asks for: PRD, feature spec, user stories, acceptance criteria, requirement review notes, scope decomposition, MVP scope, edge-case list, dependency map, release checklist, or handoff context. Do not force a full document when the user needs a short requirement clarification.

## Boundary

Skill owns product requirement workflow, requirement structure, user and scenario framing, scope boundaries, acceptance criteria, edge-case coverage, dependency surfacing, and review quality.

It does not own code implementation, engineering architecture approval, UI design finalization, legal approval, compliance approval, security approval, release approval, project scheduling, customer commitment, or metric guarantee.

It must not run shell, Python, Node, npm, curl, MCP, project-management, ticketing, analytics, Figma, email, CRM, Office, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/requirement-rules.md`: requirement decomposition, acceptance criteria, edge cases, rollout, dependencies, and non-goal rules.
- `references/review-checklist.md`: PRD and requirement review checklist.
- `LICENSE`: source and license notice.
