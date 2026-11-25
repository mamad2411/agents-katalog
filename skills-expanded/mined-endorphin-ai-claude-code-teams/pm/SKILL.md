---
name: pm
description: "Product management skill for PRD writing and acceptance review. Use when creating requirements documents or validating deliverables against acceptance criteria."
---

# Product Management Skill

## Purpose

This skill equips the PM agent with the knowledge and methodology to perform two critical pipeline roles:

- **Phase 0 — PRD Writing**: Transform a user request into a structured Product Requirements Document that serves as the single source of truth for all downstream agents (architect, developers, testers).
- **Phase 6 — Acceptance Review**: Compare delivered work against the PRD's acceptance criteria and produce a pass/fail verdict with actionable feedback.

The PRD is the contract between the user's intent and the squad's output. Every feature, every endpoint, every UI component traces back to a line in the PRD. If it is not in the PRD, it does not get built. If it is in the PRD, it must be delivered.

## Key Patterns

### PRD as the Single Source of Truth

The PRD is consumed by every agent in the pipeline:
- **Architect** reads it to design system architecture, define API contracts, and plan data models.
- **Go Developer** reads it to implement backend services, handlers, and business logic.
- **React Developer** reads it to build UI components, pages, and client-side logic.
- **Testers** read it to derive test cases from acceptance criteria.
- **PM (Phase 6)** reads it back to validate deliverables.

This means the PRD must be unambiguous, complete, and structured so that each agent can extract exactly the information it needs without interpretation.

### Feature Decomposition

Every user request, no matter how vague, must be decomposed into discrete, implementable features. Each feature must have:

1. **A clear name** — short, noun-based (e.g., "User Authentication", "Dashboard Analytics")
2. **A description** — what the feature does from the user's perspective
3. **User stories** — who benefits and how (format: "As a [role], I want [capability], so that [benefit]")
4. **Acceptance criteria** — testable conditions that define "done" (format: "GIVEN [context], WHEN [action], THEN [result]")
5. **Priority** — P0 (must-have), P1 (should-have), P2 (nice-to-have)

### Acceptance Criteria Standards

Every acceptance criterion must be:
- **Testable** — a tester or reviewer can objectively determine pass or fail
- **Specific** — references concrete values, states, or behaviors (not "should work well")
- **Independent** — each criterion can be verified on its own
- **Complete** — covers the happy path, error cases, and edge cases

Bad: "User can log in"
Good: "GIVEN a registered user with valid credentials, WHEN they submit the login form, THEN they receive a JWT token and are redirected to the dashboard within 2 seconds"

### Technical Constraints for Golang + React Stack

When writing PRDs for this stack, the PM must account for:

- **Backend (Go)**: REST or gRPC API contracts, request/response schemas, middleware requirements, database schema implications, error response formats
- **Frontend (React)**: Page/route structure, component hierarchy expectations, state management needs, API integration points, responsive design requirements
- **Cross-cutting**: Authentication/authorization model, environment configuration, CORS policy, data validation (client-side AND server-side), error handling strategy

The PM does not design the architecture (that is the architect's job), but the PM must specify WHAT the system must do clearly enough that the architect can determine HOW.

### Acceptance Review Methodology

During Phase 6, the PM systematically evaluates deliverables:

1. **Load the PRD** — re-read the original PRD produced in Phase 0
2. **Inventory deliverables** — list every file, endpoint, component, and test produced by the squad
3. **Map criteria to evidence** — for each acceptance criterion, find the code/test/artifact that satisfies it
4. **Evaluate** — mark each criterion as PASS, FAIL, or PARTIAL with evidence
5. **Verdict** — overall ACCEPT, REJECT, or ACCEPT WITH CONDITIONS

A single FAIL on a P0 criterion means REJECT. P1 failures may result in ACCEPT WITH CONDITIONS. P2 failures are noted but do not block acceptance.

See `references/` for detailed examples and patterns.

## Conventions

### Naming
- PRD file: `docs/prd.md` (or `docs/prd-{feature-slug}.md` for feature-specific PRDs)
- Review report file: `docs/acceptance-review.md`
- Feature slugs: lowercase, hyphen-separated (e.g., `user-authentication`, `dashboard-analytics`)

### Identifiers
- Features are numbered: F-001, F-002, etc.
- Acceptance criteria reference their feature: AC-001-01, AC-001-02, AC-002-01, etc.
- Priorities use P0/P1/P2 notation consistently

### Cross-references
- PRD sections reference each other by feature ID (e.g., "See F-003 for related error handling")
- Acceptance review references PRD criteria by ID (e.g., "AC-001-03: PASS — verified in auth_handler_test.go")

### Scope Discipline
- The PM never specifies implementation details (no "use goroutines for X" or "use useEffect for Y")
- The PM specifies WHAT and WHY, never HOW
- If a user request implies technical decisions, the PM captures the requirement and flags it as "Architect Decision Required"

## Knowledge Strategy

- **Patterns to capture:** Successful PRD structures for common feature types (CRUD, auth, file upload, real-time, etc.), effective acceptance criteria templates, common questions that arise during review
- **Examples to collect:** Completed PRDs that led to successful delivery, review reports that caught real issues, edge cases that were initially missed
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
