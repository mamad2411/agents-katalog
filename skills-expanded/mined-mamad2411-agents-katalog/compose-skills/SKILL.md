---
name: compose-skills
description: Use when a request needs deterministic multi-skill composition through an explicit orchestration contract while preserving skill self-containment.
---

# Compose Skills

## Specialization

Define and execute an explicit indirection contract for requests that require multiple capabilities while keeping each participating skill self-contained.

This skill has one purpose: deterministic multi-skill composition.

## Trigger Conditions

Invoke this skill when any of the following is true:

- A request spans more than one capability area and needs phased execution.
- Shared logic appears to be duplicated across self-contained skills.
- Routing must guarantee required capability coverage without direct skill-to-skill references.

## Inputs

- User objective and required outputs.
- Scope boundaries (in-scope and out-of-scope).
- Candidate capability areas implied by the request.

## Required Outputs

- A compact composition contract with objective, boundaries, phases, and completion checks.
- A capability-to-phase coverage grid showing that all required outputs are owned.
- A deterministic execution order with explicit handoff conditions between phases.
- A phase-output ownership matrix where each required output has exactly one owning phase.
- A rejected-candidate table with deterministic reason codes for excluded capabilities or skills.

## Workflow

1. Classify the request into discrete capability areas.
2. Build a phase plan where each phase owns one objective and one output set.
3. Produce a coverage grid mapping each required output to exactly one owning phase.
4. Define phase handoff criteria that must be met before advancing.
5. Run a completion check to confirm no required output is unowned or omitted.
6. Reject the plan if any required output is unowned, multiply owned, or mapped to a rejected candidate.

## Core Rules

- Keep composition deterministic by default.
- Use indirection contracts, not direct cross-skill references.
- Keep each phase scope singular and auditable.
- Reject execution if any required output lacks an owning phase.
- Fail closed: do not start execution when ownership matrix validation fails.
- Keep capability selection deterministic by recording rejected candidates and reason codes.

## Done Criteria

- Composition contract exists and is complete.
- Coverage grid shows full required-output ownership.
- Deterministic phase order and handoff criteria are explicit.
- Phase-output ownership matrix has no unowned or multiply owned required outputs.
