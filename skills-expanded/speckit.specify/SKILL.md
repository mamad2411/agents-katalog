---
name: speckit.specify
description: Feature Definer - Generates spec.md from natural language description.
---

## Mission
Transform ambiguous natural language descriptions into a standardized, testable, implementation-agnostic specification (`spec.md`) defining WHAT the system must do without dictating HOW.

## Inputs and Outputs
- Read developer request, feature description, user constraints, and `.agents/memory/constitution.md`.
- Produce `.agents/specs/[feature]/spec.md` containing overview, actors, user scenarios, functional requirements, non-functional requirements, and measurable success criteria.

## Protocol
1. Extract core user intent, primary actors (User, Admin, System, Guest), state boundaries, and operational constraints from the request.
2. Define User Scenarios using strict `Actor + Action + Value` format with clear preconditions and failure branches.
3. Formulate measurable Functional Requirements with exact data entities, fields, relationships, and validation rules.
4. Specify Non-Functional Requirements including latency limits, security boundaries, concurrency, and internationalization requirements.
5. Define atomic, testable Success Criteria checkboxes that map directly to functional requirements.
6. Identify ambiguities or missing constraints early and mark them explicitly for clarification before planning.

## Completion Gate
`spec.md` contains measurable requirements, complete error/failure paths, testable acceptance criteria, and zero technical implementation leaks.

## Guard Rails
Do not prescribe libraries, schemas, or implementation code (HOW). Do not use technical jargon in user scenarios. Do not omit error handling or boundary cases.
