---
title: CalamityAppDemo Copilot Instructions
description: Repository-specific coding guidance for GitHub Copilot in the CalamityAppDemo Aspire solution
author: CalamityAppDemo Team
ms.date: 2026-07-16
ms.topic: reference
keywords:
  - github copilot
  - aspire
  - dotnet
  - react
  - vite
estimated_reading_time: 6
---

## Project Overview

This repository is a .NET Aspire distributed application with three main parts:

* App orchestration in CalamityAppDemo.AppHost
* Backend API in CalamityAppDemo.Server
* Frontend SPA in frontend using React, TypeScript, and Vite

Use these instructions when generating or editing code in this repo.

## Tech Stack

This project targets the following technology stack:

* .NET Aspire
* React (frontend)
* ASP.NET (backend)
* SQL Server (database)
* Redis Cache
* Azure (deployment)

## Specification & Planning Authority

All specifications, implementation plans, and task breakdowns are generated and maintained **exclusively by GitHub Spec-Kit agents**:

* **Spec-Kit Agents**: Own `/specs/rescue-ph/` directory and all documentation within
* **Authority**: Treat all specifications as source-of-truth; do not edit directly
* **Versioning**: Spec-Kit manages versions, updates, and consistency
* **Read-Only for Implementation**: Implementation agents (developers, builders) read specifications to inform work but do NOT modify them

**For non-Spec-Kit agents** (implementation teams, developers, builders):
* Reference specs at `/specs/rescue-ph/spec.md`, `/specs/rescue-ph/plan.md`, `/specs/rescue-ph/tasks.md` as read-only guidance
* If specifications need updates or clarifications, request changes via GitHub issues or contact the Spec-Kit agent
* Use the Spec-Kit CLI (`specify`) to validate or query specifications when needed

## Constitution & Governing Principles

The project is governed by **7 Core Principles** defined in `.github/SPECKIT-CONSTITUTION.md`:

1. **Specification-Driven Development** — All implementation follows specifications as source-of-truth
2. **Human-Approved Critical Actions** — No autonomous dispatch, allocation, or communication without explicit human approval
3. **Agentic AI with Guardrails** — All AI recommendations include confidence scores and validation; low-confidence outputs flagged for manual review
4. **Specification Authority & Separation of Concerns** — Clear boundary: Spec-Kit generates/maintains specifications → Implementation executes → Specifications supersede preferences
5. **Complete Audit Trail** — Every decision logged with actor identity, timestamp, and rationale; immutable audit log maintained
6. **Vertical Slice Execution** — Tasks organized by features, not technical layers; enables parallel team work
7. **Demo-Ready Quality** — Every deliverable works end-to-end; mock data seeded; demo script drives feature prioritization

**Implementation Guide**: When developing, reference the Constitution to understand project values and governance framework. Each specification document includes a "Constitution Alignment" section showing how it implements these principles.

**CLI Access for All Agents**:
```bash
# All agents can query and validate specs via CLI
specify validate specs/rescue-ph/
specify generate --preview  # Preview changes without applying
specify status              # Check Spec-Kit state and version
```

## Architecture And Runtime

* Start the system from CalamityAppDemo.AppHost, not from individual projects
* Redis is provisioned by the AppHost and referenced by the API as cache
* The API exposes endpoints under /api
* The frontend uses Vite proxy rules to forward /api to the backend service URL
* The API publishes frontend build artifacts into the server wwwroot during distributed app publish

## Backend Guidelines

* Keep backend code in CalamityAppDemo.Server focused on minimal API patterns already used in Program.cs
* Reuse AddServiceDefaults, MapDefaultEndpoints, and existing OpenTelemetry setup patterns
* Prefer extending existing endpoint groups, for example app.MapGroup("/api"), before adding new top-level route maps
* Use ProblemDetails-compatible error handling for new endpoints
* Keep nullable reference types enabled and avoid suppressing nullability warnings without clear reason
* Do not remove or bypass output caching setup unless explicitly requested
* Avoid changing generated files under bin or obj

## GitHub Issue Hierarchy & PR Workflow

The project uses a **4-level GitHub issue hierarchy** to organize work and track progress:

**Hierarchy Levels** (see [`.github/ISSUE-HIERARCHY.md`](.github/ISSUE-HIERARCHY.md) for details):
- **EPIC** (labeled `epic`) — Major feature area; highest level
- **FEATURE** (labeled `feature`) — Cohesive technical feature; child of Epic
- **USER STORY** (labeled `user-story`) — User-facing value; child of Feature
- **TASK** (labeled `task`) — Granular work item; child of User Story; **assignable to individuals**

**Assigning Work**:
- Find a **TASK** issue labeled `task` in the appropriate Epic/Feature/User Story
- Assign the **TASK** to yourself (do NOT assign Features or User Stories)
- Leave Features and User Stories unassigned; they track via sub-issue completion

**PR Linking Strategy**:
When you create a pull request, include **closing keywords** in your PR description to auto-close related issues:

1. **Close the TASK** (primary link):
   ```
   Closes #TASK-01
   ```
   When PR is merged to default branch, TASK-01 auto-closes.

2. **Close the USER STORY** (if all tasks complete):
   ```
   Closes #TASK-01, #TASK-02, #US-05
   ```
   Close all related tasks AND the user story.

3. **Reference the FEATURE** (for cross-team visibility):
   ```
   Related to #FT-03
   ```
   Links PR to feature for coordination (does NOT close).

**Example PR Description**:
```markdown
## Description
Implements approval workflow for resource allocation with audit logging.

Closes #TASK-12, #TASK-13, #US-08

Related to #FT-04

## Changes
- Created AllocationService with approval logic
- Added POST /api/allocations/approve endpoint
- Integrated AuditService for logging all decisions
- Tested approval constraints per spec
```

**Result After Merge**:
- TASK-12 and TASK-13 auto-close
- US-08 auto-closes (if all sub-tasks complete)
- FT-04 shows progress (1 of N PRs complete)
- EPIC-02 shows overall completion %

For complete details on hierarchy creation, CLI usage, and best practices, see [`.github/ISSUE-HIERARCHY.md`](.github/ISSUE-HIERARCHY.md).

## Frontend Guidelines

* Use function components with React hooks
* Keep strict TypeScript typing for API contracts and component state
* Continue existing accessibility patterns such as aria labels, semantic elements, and reduced-motion support
* Keep visual tokens in CSS custom properties before introducing hardcoded values
* Preserve existing Vite proxy behavior for /api calls
* Do not add large state libraries unless the user asks for one
* Avoid editing dist, node_modules, or generated assets

## API Contract Conventions

* Keep API and frontend contracts aligned when changing response shapes
* For new DTO-like structures in the API, mirror interface updates in frontend TypeScript
* Use predictable JSON naming and stable response formats
* When introducing breaking API changes, update both backend and frontend in the same change

## Build, Run, And Validation

Prefer these commands when validating generated changes:

* Restore and build solution: dotnet build CalamityAppDemo.slnx
* Run distributed app: dotnet run --project CalamityAppDemo.AppHost
* Frontend install: npm install --prefix frontend
* Frontend lint: npm run lint --prefix frontend
* Frontend build: npm run build --prefix frontend

If a change affects both backend and frontend, run at least one backend build and one frontend lint or build command.

## Change Scope And Safety

* Make minimal, targeted edits that preserve existing style
* Do not refactor unrelated files during feature work
* Do not modify bin, obj, or tool-generated files
* Do not introduce new infrastructure packages unless required by the task
* Keep comments concise and only where logic is not obvious

## File Placement

* Backend feature code belongs in CalamityAppDemo.Server
* Orchestration and service wiring changes belong in CalamityAppDemo.AppHost
* UI, styling, and browser-only logic belong in frontend/src
* Shared documentation and repo automation files belong under .github when needed

## Preferred Assistant Behavior For This Repo

* **FDE Mindset**: Act like a Forward Deployed Engineer—be outcome-driven, unblock quickly, prioritize pragmatic solutions that deliver user impact
* **Spec-Kit Respect**: Recognize that specifications, plans, and tasks are generated and maintained exclusively by Spec-Kit agents:
  - Implementation agents treat specs as **read-only guidance**
  - Spec-Kit agents are the sole authority on `/specs/rescue-ph/` content
  - If specifications conflict with implementation realities, raise issues for Spec-Kit agents to resolve
* **Before Major Edits**: Inspect neighboring files for local patterns and check spec alignment
* **API & UI Completeness**: When adding new endpoints, include request and error-path handling; when adding UI features, include loading and error states
* **Clear Naming**: Keep naming clear and domain-oriented throughout
* **Validation Reporting**: Mention validation status in final summaries when commands were run
* **Workflow Separation**: Maintain clean boundaries—Spec-Kit generates/maintains docs; implementation agents execute against those specs

## Clarification & Assumptions Protocol

Before answering requests, identify any missing context, ambiguities, constraints, or decisions that materially affect the result:

* **Missing Information**: Explicitly ask only essential clarifying questions; avoid over-asking
* **Assumptions**: State any assumptions you will make if information is not provided
* **Specification Alignment**: If a request seems to conflict with `/specs/rescue-ph/` specifications, call this out and ask for clarification before proceeding
* **Spec-Kit Deference**: For requests affecting specifications, plans, or tasks, defer to Spec-Kit agents as the authority

### Example Assumptions to State

* "I assume this feature aligns with the resource allocation triage described in spec.md§ Functional Requirements"
* "I'm assuming we should NOT edit `/specs/rescue-ph/` files; if you need spec changes, we should involve Spec-Kit agents"
* "I assume the 'Safety' requirements in the spec (human approval mandates, audit trails) apply to this endpoint"

