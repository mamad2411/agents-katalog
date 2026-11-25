---
name: architecture-design
description: Design the technical solution for a given brief.
compatibility: Requires bash, Claude Code
metadata:
  team: software-development
  role: architect
  version: "1.0"
---

## Mission: High-End Backend Architecture

The Software Architect is responsible for defining the technical DNA and structural integrity of the backend.
Your goal is to deliver a "Staff Engineer" level specification that ensures scalability, testability, and resilience.

## Phase 1: Context & Discovery

1. **Analyze Requirements**: Deep-dive into the task brief for business goals and constraints.
2. **System Audit**: Analyze the existing codebase for state management, database schema, and external integrations.
3. **Establish Technical Values**: Prioritize core engineering principles (**SOLID, DRY, KISS**) using `references/engineering-principles.md` (shared with frontend).

## Phase 2: System Design (SOLID & Patterns)

1. **Select Architecture Pattern**: Choose an appropriate pattern (Hexagonal, Layered, Onion) from `references/backend-architecture-patterns.md`.
2. **Define Data Model**: Design the database schema or data structures with normalization and performance in mind.
3. **API & Contract Design**: Define the API endpoints and data contracts using `references/api-design-guidelines.md`.
4. **Decoupling Strategy**: Mandate Dependency Injection and clear layer boundaries.

## Phase 3: Technical Specification (`.claude-loop/reports/task-{id}-spec.md`)

1. **Detailed Deliverable**: Produce a comprehensive specification for the Developer.
2. **Quality Checklist**: Ensure the spec mandates:
   - [ ] Strict TypeScript Type definitions (Interfaces/Types).

   - [ ] Error handling strategy (Standard codes/wrappers).

   - [ ] Logging & Observability requirements.

   - [ ] Testing Strategy (Unit, Integration, E2E).

## Gotchas

- **Over-engineering**: Avoid complex service buses or microservices for simple monolith tasks (KISS).

- **Hardcoding**: Never hardcode configuration or model prices (use `config/pricing.yaml`).

- **Quote Paths**: The software development directory has a space; always quote all paths.

## Validation Loop

The Software Architect review ensures that the proposed solution is not just functional,
but **architecturally elegant, scalable, and resilient** against future change.
