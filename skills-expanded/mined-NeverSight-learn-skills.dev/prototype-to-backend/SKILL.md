---
name: prototype-to-backend
description: Use when converting HTML product prototypes, Axure HTML packages, online prototype URLs, PRDs, screenshots, or enterprise business mockups into backend-ready analysis, database, API, workflow, permission, task breakdown, open-question, and design-review artifacts.
---

# Prototype To Backend

## Overview

Use this skill to turn product prototypes and requirement materials into backend implementation artifacts. Focus on business meaning, data, APIs, workflows, permissions, validation, delivery planning, and backend design review. Do not generate frontend code unless the user explicitly asks for it.

## Input Priority

Prefer source artifacts in this order:

1. Axure HTML package or other exported HTML prototype.
2. Online prototype URL with accessible pages, sitemap, notes, and interactions.
3. Product requirement document, user story, process document, or spreadsheet.
4. Screenshots only when richer artifacts are unavailable.

For Axure HTML packages, inspect the page tree, sitemap files, page titles, notes, interactions, visible text, form controls, table headers, buttons, and navigation before deriving backend artifacts.

## Working Rules

- Preserve Chinese business terms when analyzing Chinese enterprise systems, and add English technical names beside them, for example `采购申请 (PurchaseRequest)`.
- When the target team works primarily in Chinese, generate artifacts with Chinese-first bilingual headings and table columns, for example `系统概览 / System Overview` and `字段 / Field`.
- Separate confirmed facts, assumptions, and open questions. Never turn ambiguous prototype behavior into a definite rule.
- Put every uncertain business rule, missing field, missing permission, missing status, unclear workflow branch, or integration dependency into Open Questions.
- Prefer Spring Boot, REST, and SQL database friendly output when no stack is specified, but keep designs framework-agnostic unless the user names a stack.
- Use SQL Server compatible data types by default for database examples, unless the project clearly uses another database.
- Keep backend scope primary: no UI styling analysis, no frontend component code, no CSS, no page implementation.
- For large prototypes, analyze by module or batch and maintain a cumulative index of pages, entities, APIs, permissions, and open questions.

## Analysis Workflow

1. Inventory the input: list pages, modules, menus, forms, lists, dialogs, buttons, visible status labels, and referenced documents.
2. Extract backend signals: identify entities, identifiers, fields, search filters, table columns, actions, validations, state changes, workflow nodes, permissions, logs, and integration hints.
3. Build artifacts from evidence: map screens and actions to domain model, tables, APIs, state machine, workflow, permissions, and tasks.
4. Mark confidence: label each major rule as `Confirmed`, `Assumed`, or `Open Question`.
5. Generate outputs using the templates in `templates/`. Omit sections only when they are irrelevant, not when they are merely unknown.
6. Review phase: after generating backend artifacts, perform a grill-me style design review and output `10-design-review.md`.

## Review Phase

After generating backend artifacts, challenge the design as if preparing it for backend implementation review. Do not merely summarize the generated artifacts. Actively look for missing APIs, weak data models, incomplete workflow branches, status gaps, permission holes, ambiguous rules, and implementation risks.

Review these areas:

- API completeness.
- Database model correctness.
- Workflow closure.
- State machine completeness.
- Permission coverage.
- Validation rules.
- Transaction boundaries.
- Idempotency.
- Concurrency risks.
- Audit logging.
- Data permissions.
- Import/export behavior.
- Historical data versioning.
- Integration dependencies.
- Open questions quality.

For every issue:

- Explain why it matters to backend implementation, correctness, operations, or future maintenance.
- Give a recommended fix, redesign, or confirmation path.
- Assign a severity such as `Blocking`, `High`, `Medium`, or `Low`.
- If the correct answer cannot be determined from the source materials, add it to Open Questions instead of writing a guess as fact.

The review result must be actionable enough to guide backend rework or design completion.

## Required Output Set

Generate these files or sections unless the user asks for a narrower scope:

- `01-system-overview.md`: purpose, roles, module tree, menu tree, page inventory, capability map.
- `02-domain-model.md`: entities, aggregate roots, value objects, relationships, lifecycle, identifiers.
- `03-database-design.md`: tables, fields, SQL Server types, keys, indexes, constraints, audit fields, soft delete, dictionaries.
- `04-api-design.md`: REST APIs, DTOs, response VOs, permission codes, validation, transactions, idempotency.
- `05-state-machine.md`: statuses, actions, transitions, terminal states, rollback, revoke, reject rules.
- `06-workflow.md`: approval nodes, participants, actions, return/reject/revoke/transfer rules, variables, notifications.
- `07-permission-model.md`: menu, button, data permissions, roles, permission naming convention.
- `08-development-plan.md`: milestones, module tasks, entity/table tasks, API tasks, workflow tasks, tests, risk, priority.
- `09-open-questions.md`: unclear rules, missing fields/statuses/permissions/workflows, integrations, confirmation checklist.
- `10-design-review.md`: grill-me style backend design review with issues, why they matter, recommendations, severity, product questions, and completion checklist.

## Extraction Checklist

Prioritize these signals:

| Signal | Backend interpretation |
| --- | --- |
| Menu item or page title | Module, capability, menu permission |
| Form field | Entity property, DTO field, validation rule |
| Search condition | Query API parameter, index candidate |
| Table column | List VO field, database field candidate |
| Button or link | Command API, permission point, state transition |
| Status label | State machine value, dictionary item |
| Approval action | Workflow transition and audit record |
| Required marker | Validation rule |
| Import/export button | Batch job, file template, async task, audit requirement |
| User/department selector | Organization scope, data permission, foreign key |

## Naming Conventions

- Entity class names: English PascalCase, preserving Chinese term in description.
- Table names: lowercase snake case, for example `purchase_request`.
- API paths: resource-oriented, for example `/api/purchase-requests/{id}/submit`.
- Permission codes: `module:resource:action`, for example `procurement:request:approve`.
- Status codes: uppercase snake case, for example `PENDING_APPROVAL`.

## Template Usage

Use the templates under `templates/` as the default structure. Templates are Chinese-first bilingual so Chinese enterprise teams can review them directly while agents still see stable English technical labels. Keep evidence notes concise and practical. If a section cannot be completed from the prototype, write `未确认 / Not confirmed` and add the item to `09-open-questions.md`. After the first nine artifacts are drafted, use `10-design-review-template.md` to challenge and complete the design.

## Quality Bar

Good output is specific enough for backend developers to start implementation, but honest about uncertainty. Every proposed table, API, workflow rule, and permission should trace back to observed prototype evidence, PRD text, or an explicitly marked assumption.
