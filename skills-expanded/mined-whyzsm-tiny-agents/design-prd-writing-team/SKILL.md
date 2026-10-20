---
name: design-prd-writing-team
description: End-to-end PRD writing workflow. Use when the user wants a complete product requirements workflow that spans requirement discovery, EPIC/user-story decomposition, prioritization, professional PRD drafting, PRD-to-design handoff, and PRD review/scoring. This skill coordinates the companion skills requirements-analysis, software-manager-skill, prd, prd-writer-pro, prd-to-design-doc, and prd-reviewer.
metadata:
  short-description: Complete PRD writing workflow
---

# Design PRD Writing

Use this skill as the workflow entry point for a complete PRD package. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Use `requirements-analysis` to turn the initial idea into structured requirements, stakeholders, dependencies, user stories, and acceptance criteria.
2. Use `software-manager-skill` to select frameworks, prioritize requirements with methods such as RICE/MoSCoW/Kano, define MVP scope, and plan product direction.
3. Use `prd` to structure implementation-ready PRD items, task lists, user stories, acceptance criteria, and dependency order.
4. Use `prd-writer-pro` to produce the polished PRD with background, goals, success metrics, functional requirements, non-functional requirements, edge cases, and launch considerations.
5. Use `prd-to-design-doc` when the user needs a design handoff. Convert the PRD into design goals, information architecture, interaction flows, page layout requirements, visual requirements, empty/error states, and delivery checklist.
6. Use `prd-reviewer` to score the PRD, identify missing sections, list evidence-based deductions, and propose concrete improvements.

## Output Package

When the user asks for a full PRD package, produce these artifacts in order:

1. Requirement list: structured requirements, users, scenarios, dependencies, user stories, and acceptance criteria.
2. Prioritization and MVP: scoring table, chosen framework, MVP scope, and deferred scope.
3. PRD document: professional product requirements document ready for review.
4. Design requirement document: information architecture, interaction flows, page/layout requirements, and delivery checklist.
5. Review report: score, module-level deductions, risks, and revision recommendations.

## Operating Notes

- Ask only the clarifying questions needed to unblock the next step. If the user already gave enough context, move directly into the workflow.
- Keep assumptions explicit and mark them as assumptions.
- When converting PRD content to design handoff, preserve business rules and acceptance criteria instead of inventing interaction behavior that the PRD does not support.
- When reviewing, cite specific PRD sections or missing evidence for every deduction.
