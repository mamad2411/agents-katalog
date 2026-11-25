---
name: system-architecture-builder
description: Use when starting a new software, SaaS, AI product, internal tool, data platform, automation system, or major greenfield module and the user wants architecture documents, PRD, data model, API contracts, AI automation specs, or implementation readiness before code.
---

# System Architecture Builder

## Purpose

Guide Codex or another AI engineering agent through a complete architecture setup process for new systems before writing production code. Default to Chinese outputs and `references/zh-CN/` unless the user asks for English. The skill is stack-neutral: adapt it to web apps, SaaS products, AI systems, internal tools, mobile apps, automation platforms, data products, and backend services.

## Core Rule

Do not start implementation until the architecture readiness gate passes.

Before readiness:

- Do not initialize frameworks or projects.
- Do not install dependencies.
- Do not create UI pages.
- Do not create database migrations.
- Do not write business logic.
- Do not create API handlers.
- Do not assume a tech stack unless the user specified one.

Allowed before readiness:

- Create architecture documents.
- Create schema or contract drafts only when the phase explicitly asks for them.
- Run static inspections of existing files.
- Ask focused questions.
- Update planning artifacts.

## Cross-Platform Use

In Codex, install this folder as a skill and invoke `$system-architecture-builder`.

In Claude, ChatGPT, Cursor, Windsurf, Roo Code, Cline, or other AI tools, provide this `SKILL.md` as the governing workflow and attach only the `references/zh-CN/*.md` file needed for the current phase by default. Use `references/en/*.md` only when the user asks for English. The same phase gates and readiness rules still apply.

## Workflow

Run the process in phases. Finish each phase with a concise status report and a recommendation for the next phase.

1. **Context Discovery**
   Clarify what the system is, who uses it, deployment assumptions, business constraints, risk level, and existing files.

2. **Project Brief**
   Create the long-lived project context: product positioning, users, roles, core principles, system boundaries, and non-goals.

3. **PRD and Scope**
   Define user journeys, lifecycle, role permissions, V1/V2/V3 scope, state machines, acceptance criteria, and explicit non-goals.

4. **Architecture Boundary**
   Define application modules, runtime boundaries, integration boundaries, high-risk capability boundaries, and stack decisions or stack options.

5. **Data Model Blueprint**
   Create an implementation-level entity model before writing ORM or SQL. Include entities, fields, relationships, enums, tenancy, indexes, soft delete, privacy, audit, and open questions.

6. **Database Schema**
   Generate ORM/SQL schema only after the data model blueprint is approved. Keep migrations and seed data out unless the user asks.

7. **API Contract**
   Define auth context, RBAC, scope rules, request schemas, response DTOs, error codes, pagination, file handling, sensitive data rules, audit requirements, and forbidden APIs.

8. **AI / Automation Spec**
   If the system includes AI, agents, external automation, scraping, third-party actions, or workflow execution, define orchestration, context boundaries, human review, output validation, logging, and prohibited actions.

9. **Privacy / Security / Risk**
   Define data classification, access control, consent, deletion, retention, audit, credential handling, external platform boundaries, cross-border processing, and risk controls.

10. **Implementation Readiness**
    Verify architecture completeness. Then output detailed reminders for the next build steps: repository setup, package setup, typecheck, database validation, contracts, backend services, workers, UI, tests, deployment, observability, and risk review.

Read `references/zh-CN/workflow.md` by default when running the full process. Use `references/en/workflow.md` only for English projects.

## Phase Gates

Each phase must answer:

- What files were created or changed?
- What decisions were made?
- What assumptions remain?
- What risks or ambiguities remain?
- What downstream artifacts are affected?
- What is the recommended next phase?

Do not proceed to the next phase if core decisions are missing. Ask one focused question at a time when missing information blocks progress.

## Artifact Selection

Use `references/zh-CN/artifact-catalog.md` by default, or `references/en/artifact-catalog.md` for English projects, to choose which documents and implementation artifacts the project needs. Do not create every artifact by default.

Common sequence:

1. `AGENTS.md`
2. `docs/PROJECT_BRIEF.md`
3. `docs/PRD.md`
4. `docs/DATA_MODEL.md`
5. database schema
6. `docs/API_CONTRACT.md`
7. `docs/AGENT_SPEC.md` or automation spec, if needed
8. `docs/PRIVACY_SECURITY.md` or equivalent
9. shared contracts
10. implementation plan

## Stack Neutrality

When the user has no stack preference, propose 2-3 viable stack options with tradeoffs. When the stack is given, follow it. Use `references/zh-CN/stack-adaptation-guide.md` by default, or `references/en/stack-adaptation-guide.md` for English projects, for stack-specific adjustments.

## Discovery Questions

Use `references/zh-CN/discovery-question-bank.md` by default, or `references/en/discovery-question-bank.md` for English projects, for reusable question sets. Ask only the questions needed for the current phase, one at a time unless the user asks for a full questionnaire.

## Templates

Use these references as phase templates:

- `references/zh-CN/project-brief-template.md` or `references/en/project-brief-template.md`
- `references/zh-CN/prd-template.md` or `references/en/prd-template.md`
- `references/zh-CN/data-model-template.md` or `references/en/data-model-template.md`
- `references/zh-CN/api-contract-template.md` or `references/en/api-contract-template.md`
- `references/zh-CN/ai-automation-template.md` or `references/en/ai-automation-template.md`
- `references/zh-CN/privacy-security-risk-template.md` or `references/en/privacy-security-risk-template.md`
- `references/zh-CN/implementation-readiness-checklist.md` or `references/en/implementation-readiness-checklist.md`

## Output Style

At the end of every phase, report:

1. Files created or modified
2. Purpose of each file
3. Core decisions
4. Current assumptions
5. Downstream impact
6. Open questions
7. Recommended next step

If implementation readiness passes, also output a detailed follow-up checklist:

- environment and package setup
- repository and workspace setup
- schema validation and migrations
- contract typecheck
- backend service order
- worker and queue order
- frontend surface order
- testing strategy
- deployment and secrets
- observability
- security and privacy review
- risk review
- release readiness

## Safety

For high-risk systems, separate capabilities into:

- **Official / supported**
- **Internal experimental**
- **Forbidden or not implementable**

Never design hidden bypasses, unsafe credential handling, irreversible unattended actions, or opaque automated decisions as normal product features. If the user insists on internal experimentation, isolate it behind experimental flags, manual checkpoints, logs, rate limits, and explicit warnings.
